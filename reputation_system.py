from models import db, User
import time

class ReputationManager:
    def __init__(self):
        # Storage: Database
        
        # Configuration
        self.INITIAL_SCORE = 100
        self.MAX_SCORE = 100
        self.MUTE_THRESHOLD = 30
        self.BAN_THRESHOLD = 0
        self.MUTE_DURATION = 60  # 1 minute

        # Penalties
        self.PENALTIES = {
            'High': 20,
            'Medium': 10,
            'Low': 5
        }
        self.RECOVERY_POINTS = 1

    def _get_or_create_user(self, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            # Create transient user (or they should register). 
            # For this system to work with existing un-registered flow, we might need to create them.
            # Let's auto-create for now if they don't exist, with empty password (so they can't login but have reputation)
            # OR we assume they must be registered. 
            # Given the prompt "track real users instead of just display names", strictly we should require login.
            # But to keep 'demo' checking working without login for now:
            user = User(username=username, reputation_score=self.INITIAL_SCORE)
            db.session.add(user)
            db.session.commit()
        return user

    def get_user_status(self, username):
        user = self._get_or_create_user(username)
        
        # ENABLED: Status checks for Ban/Mute
        if user.is_banned:
            return {'status': 'banned', 'score': user.reputation_score, 'message': "You are permanently banned due to repeated toxicity."}
            
        if user.muted_until > time.time():
            remaining = int(user.muted_until - time.time())
            minutes = remaining // 60
            seconds = remaining % 60
            time_str = f"{minutes}m {seconds}s" if minutes > 0 else f"{seconds}s"
            # Updated message as per request
            return {'status': 'muted', 'score': user.reputation_score, 'message': f"⚠️ You cannot send messages. Please wait {time_str}."}
            
        return {'status': 'active', 'score': user.reputation_score, 'message': "Active"}

    def update_score(self, username, toxicity_severity=None):
        user = self._get_or_create_user(username)
        
        if toxicity_severity:
            # Apply Penalty
            penalty = self.PENALTIES.get(toxicity_severity, 0)
            user.reputation_score = max(user.reputation_score - penalty, 0)
            
            # IMMEDIATE TIMEOUT: Mute for 1 minute on ANY toxic message
            user.muted_until = time.time() + self.MUTE_DURATION 
        else:
            # Recovery (Safe message)
            if user.reputation_score < self.MAX_SCORE:
                user.reputation_score += self.RECOVERY_POINTS

        # Check Thresholds
        # ENABLED: Automatic Ban is restored.
        if user.reputation_score <= self.BAN_THRESHOLD:
            user.is_banned = True
        
        # NOTE: Mute logic is now ONLY applied immediately after a toxic message (above).
        # We DO NOT apply mute just because score is low, to allow users to recover.
        # elif user.reputation_score < self.MUTE_THRESHOLD:
        #     if user.muted_until < time.time():
        #          user.muted_until = time.time() + self.MUTE_DURATION
        
        db.session.commit()
        return user.reputation_score

    def manual_timeout(self, username, duration=60):
        """Manually mute a user for a specific duration (default 60s)."""
        user = self._get_or_create_user(username)
        user.muted_until = time.time() + duration
        db.session.commit()
        return True

    def ban_user(self, username):
        user = self._get_or_create_user(username)
        user.is_banned = True
        user.reputation_score = 0
        db.session.commit()
        return True

    def unban_user(self, username):
        user = self._get_or_create_user(username)
        user.is_banned = False
        user.reputation_score = self.INITIAL_SCORE
        db.session.commit()
        return True

    def unmute_user(self, username):
        user = self._get_or_create_user(username)
        user.muted_until = 0
        db.session.commit()
        return True
