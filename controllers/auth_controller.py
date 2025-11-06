from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.database import db
from models.user_model import UserModel

class AuthController:
    """Authentication controller"""
    
    @staticmethod
    def register():
        """Register new user (only 'user' role, no role selection)"""
        try:
            data = request.json
            
            # Validate input data
            if not data.get('username') or not data.get('email') or not data.get('password'):
                return jsonify({"error": "Username, email, dan password diperlukan"}), 400
            
            # Create user model with 'user' role only
            user = UserModel(
                username=data.get('username'),
                email=data.get('email'),
                password=data.get('password'),
                role='user'  # Force user role for registration
            )
            
            # Validate user data
            is_valid, errors = user.validate()
            if not is_valid:
                return jsonify({"error": "; ".join(errors)}), 400
            
            # Check password length
            if len(data.get('password')) < 6:
                return jsonify({"error": "Password harus minimal 6 karakter"}), 400
            
            # Save to database
            result = db.create_user(user.to_dict())
            if not result:
                return jsonify({"error": "Username atau email sudah digunakan"}), 409
            
            return jsonify({
                "message": "Registrasi berhasil",
                "user": {
                    "user_id": user.user_id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role
                }
            }), 201
            
        except Exception as e:
            return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 500
    
    @staticmethod
    def login():
        """Login user"""
        try:
            data = request.json
            
            if not data.get('username') or not data.get('password'):
                return jsonify({"error": "Username dan password diperlukan"}), 400
            
            # Find user
            user_data = db.find_user_by_username(data.get('username'))
            if not user_data:
                return jsonify({"error": "Username atau password salah"}), 401
            
            # Create user model from data
            user = UserModel.from_dict(user_data)
            
            # Check password
            if not user.check_password(data.get('password')):
                return jsonify({"error": "Username atau password salah"}), 401
            
            # Check if user is active
            if not user.is_active:
                return jsonify({"error": "Akun tidak aktif"}), 403
            
            # Create JWT token
            access_token = create_access_token(
                identity=user.user_id,
                additional_claims={
                    "username": user.username,
                    "role": user.role
                }
            )
            
            return jsonify({
                "message": "Login berhasil",
                "access_token": access_token,
                "user": {
                    "user_id": user.user_id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role
                }
            }), 200
            
        except Exception as e:
            return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 500
    
    @staticmethod
    @jwt_required()
    def get_current_user():
        """Get current logged in user"""
        try:
            user_id = get_jwt_identity()
            user_data = db.find_user_by_id(user_id)
            
            if not user_data:
                return jsonify({"error": "User tidak ditemukan"}), 404
            
            user = UserModel.from_dict(user_data)
            return jsonify({
                "user": {
                    "user_id": user.user_id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role
                }
            }), 200
            
        except Exception as e:
            return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 500
    
    @staticmethod
    @jwt_required()
    def logout():
        """Logout user (client-side token removal)"""
        return jsonify({"message": "Logout berhasil"}), 200