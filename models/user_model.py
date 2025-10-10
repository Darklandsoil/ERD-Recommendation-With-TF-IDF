from datetime import datetime
import bcrypt
import uuid

class UserModel:
    """User model for authentication and role management"""
    
    def __init__(self, username=None, email=None, password=None, role="user"):
        self.user_id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.password_hash = None
        self.role = role  # "user" or "advisor"
        self.created_at = datetime.now()
        self.is_active = True
        
        if password:
            self.set_password(password)
    
    def set_password(self, password):
        """Hash and set password"""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password):
        """Check if password is correct"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self):
        """Convert to dictionary for MongoDB storage"""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
            "role": self.role,
            "created_at": self.created_at,
            "is_active": self.is_active
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create UserModel from dictionary"""
        user = cls()
        user.user_id = data.get("user_id")
        user.username = data.get("username")
        user.email = data.get("email")
        user.password_hash = data.get("password_hash")
        user.role = data.get("role", "user")
        user.created_at = data.get("created_at")
        user.is_active = data.get("is_active", True)
        return user
    
    def validate(self):
        """Validate user data"""
        errors = []
        
        if not self.username or len(self.username) < 3:
            errors.append("Username harus minimal 3 karakter")
        
        if not self.email or "@" not in self.email:
            errors.append("Email tidak valid")
        
        if not self.password_hash:
            errors.append("Password diperlukan")
        
        if self.role not in ["user", "advisor"]:
            errors.append("Role harus 'user' atau 'advisor'")
        
        return len(errors) == 0, errors