from app import app, db, User
import time

def fix_ban():
    print("Attempting to unban user 'You' via App Context...")
    with app.app_context():
        # Check DB URI
        print(f"DB URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        
        user = User.query.filter_by(username='You').first()
        if user:
            print(f"Found user: {user.username}")
            print(f"Current Status - Banned: {user.is_banned}, Score: {user.reputation_score}, Muted: {user.muted_until}")
            
            user.is_banned = False
            user.reputation_score = 100
            user.muted_until = 0
            db.session.commit()
            print("Updates committed.")
            
            # Verify
            user = User.query.filter_by(username='You').first()
            print(f"New Status - Banned: {user.is_banned}, Score: {user.reputation_score}")
        else:
            print("User 'You' not found!")

if __name__ == "__main__":
    fix_ban()
