from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from toxicity_model import ToxicityDetector
from reputation_system import ReputationManager
from models import db, User, Message
from flask_bcrypt import Bcrypt
import time
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key-change-this-in-production' 

CORS(app) 
db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

detector = ToxicityDetector()
reputation_manager = ReputationManager() 

# Ensure DB is created
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 400
        
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token, username=username, reputation=user.reputation_score)
    
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/analyze', methods=['POST'])
def analyze_message():
    data = request.json
    user_message = data.get('message', '')
    user_name = data.get('username', 'User')
    
    return process_message(user_name, user_message)

def process_message(user_name, user_message):
    # 1. Check Reputation Status BEFORE analysis
    status = reputation_manager.get_user_status(user_name)
    if status['status'] != 'active':
        return jsonify({
            'id': int(time.time() * 1000),
            'username': 'System',
            'display_text': status['message'], 
            'warning_text': status['message'],
            'type': 'system', # Frontend treats as normal but we can style it if needed, or just let it be text
            'action': 'block',
            'timestamp': time.strftime('%I:%M %p'),
            'reputation_score': status['score'],
            'user_status': status['status']
        })

    # 2. Analyze the message
    result = detector.predict(user_message)
    
    # 3. Update Reputation Score
    toxicity_severity = result.get('severity') if result['message_type'] == 'toxic' else None
    new_score = reputation_manager.update_score(user_name, toxicity_severity)
    
    # Re-check status after update
    final_status = reputation_manager.get_user_status(user_name)

    # Construct the message object
    message_obj = {
        'id': int(time.time() * 1000),
        'username': user_name,
        'original_text': user_message,
        'display_text': result['display_text'],
        'warning_text': result.get('warning_text'),
        'type': result['message_type'],
        'action': result['action'],
        'timestamp': time.strftime('%I:%M %p'),
        'duration': result.get('duration'),
        'reason': result.get('reason'),
        'severity': result.get('severity'),
        'reputation_score': new_score,
        'user_status': final_status['status']
    }
    
    # Save to DB
    db_user = User.query.filter_by(username=user_name).first()
    user_id = db_user.id if db_user else None
    
    db_msg = Message(
        user_id=user_id,
        username=user_name,
        content=user_message,
        is_toxic=(result['message_type'] == 'toxic'),
        toxicity_score=0.0,
        severity=result.get('severity') # Save Severity
    )
    db.session.add(db_msg)
    db.session.commit()
    
    return jsonify(message_obj)

@app.route('/messages', methods=['GET'])
def get_messages():
    # Return last 50 messages
    messages = Message.query.order_by(Message.timestamp.desc()).limit(50).all()
    # Convert to list of dicts and reverse (so oldest is first for chat log)
    msg_list = []
    for m in messages[::-1]:
        # Fix: Ensure timestamp is treated as UTC before converting to epoch
        from datetime import timezone
        
        timestamp_ms = int(time.time() * 1000)
        if m.timestamp:
            timestamp_ms = int(m.timestamp.replace(tzinfo=timezone.utc).timestamp() * 1000)

        msg_data = {
            'id': timestamp_ms,
            'username': m.username,
            'display_text': m.content, 
            'type': 'toxic' if m.is_toxic else 'normal',
            'timestamp': m.timestamp.strftime('%I:%M %p') if m.timestamp else '',
            'severity': m.severity # Persisted severity
        }
        
        # Reconstruct warning fields for toxic messages so frontend hides them
        if m.is_toxic:
            # Use stored severity, default to High if missing (legacy messages)
            sev = m.severity if m.severity else "High"
            msg_data['severity'] = sev
            msg_data['warning_text'] = f"Message removed: {sev} Severity - Contains toxic content"
            msg_data['reason'] = "Violates community guidelines"
            msg_data['duration'] = "7 seconds"
            
        msg_list.append(msg_data)
    return jsonify(msg_list)

@app.route('/clear_chat', methods=['POST'])
def clear_chat():
    Message.query.delete()
    db.session.commit()
    return jsonify({'status': 'cleared'})

@app.route('/api/moderate/ban', methods=['POST'])
def ban_user_route():
    data = request.json
    username = data.get('username')
    if not username: return jsonify({'error': 'Username required'}), 400
    reputation_manager.ban_user(username)
    return jsonify({'status': 'banned', 'username': username})

@app.route('/api/moderate/unban', methods=['POST'])
def unban_user_route():
    data = request.json
    username = data.get('username')
    if not username: return jsonify({'error': 'Username required'}), 400
    reputation_manager.unban_user(username)
    return jsonify({'status': 'unbanned', 'username': username})

@app.route('/api/moderate/mute', methods=['POST'])
def mute_user_route():
    data = request.json
    username = data.get('username')
    duration = data.get('duration', 60)
    if not username: return jsonify({'error': 'Username required'}), 400
    reputation_manager.manual_timeout(username, duration)
    return jsonify({'status': 'muted', 'username': username, 'duration': duration})

@app.route('/api/moderate/unmute', methods=['POST'])
def unmute_user_route():
    data = request.json
    username = data.get('username')
    if not username: return jsonify({'error': 'Username required'}), 400
    reputation_manager.unmute_user(username)
    return jsonify({'status': 'unmuted', 'username': username})

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = []
    for u in users:
        # Check status dynamically
        status = 'active'
        if u.is_banned:
            status = 'banned'
        elif u.muted_until > time.time():
            status = 'muted'
            
        user_list.append({
            'username': u.username,
            'reputation_score': u.reputation_score,
            'status': status,
            'muted_until': u.muted_until
        })
    return jsonify(user_list)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
