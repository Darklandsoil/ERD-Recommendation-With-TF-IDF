from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from models.database import db
from models.user_model import UserModel

class AdminController:
    """Admin controller for managing advisors"""
    
    @staticmethod
    def require_admin():
        """Decorator helper to check if user is admin"""
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({"error": "Akses ditolak. Hanya admin yang diizinkan"}), 403
        return None
    
    @staticmethod
    @jwt_required()
    def get_all_advisors():
        """Get all advisor accounts"""
        # Check if user is admin
        error_response = AdminController.require_admin()
        if error_response:
            return error_response
        
        try:
            advisors = db.get_all_users_by_role("advisor")
            advisor_list = []
            
            for advisor_data in advisors:
                advisor = UserModel.from_dict(advisor_data)
                advisor_list.append({
                    "user_id": advisor.user_id,
                    "username": advisor.username,
                    "email": advisor.email,
                    "created_at": advisor.created_at.strftime("%Y-%m-%d %H:%M") if advisor.created_at else "",
                    "is_active": advisor.is_active
                })
            
            return jsonify({"advisors": advisor_list}), 200
            
        except Exception as e:
            return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 500
    
    @staticmethod
    @jwt_required()
    def create_advisor():
        """Create new advisor account"""
        # Check if user is admin
        error_response = AdminController.require_admin()
        if error_response:
            return error_response
        
        try:
            data = request.json
            
            # Validate input data
            if not data.get('username') or not data.get('email') or not data.get('password'):
                return jsonify({"error": "Username, email, dan password diperlukan"}), 400
            
            # Create advisor user model
            advisor = UserModel(
                username=data.get('username'),
                email=data.get('email'),
                password=data.get('password'),
                role='advisor'
            )
            
            # Validate advisor data
            is_valid, errors = advisor.validate()
            if not is_valid:
                return jsonify({"error": "; ".join(errors)}), 400
            
            # Check password length
            if len(data.get('password')) < 6:
                return jsonify({"error": "Password harus minimal 6 karakter"}), 400
            
            # Save to database
            result = db.create_user(advisor.to_dict())
            if not result:
                return jsonify({"error": "Username atau email sudah digunakan"}), 409
            
            return jsonify({
                "message": "Advisor berhasil dibuat",
                "advisor": {
                    "user_id": advisor.user_id,
                    "username": advisor.username,
                    "email": advisor.email,
                    "role": advisor.role
                }
            }), 201
            
        except Exception as e:
            return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 500
    
    @staticmethod
    @jwt_required()
    def update_advisor():
        """Update advisor account"""
        # Check if user is admin
        error_response = AdminController.require_admin()
        if error_response:
            return error_response
        
        try:
            data = request.json
            user_id = data.get('user_id')
            
            if not user_id:
                return jsonify({"error": "User ID diperlukan"}), 400
            
            # Find advisor
            advisor_data = db.find_user_by_id(user_id)
            if not advisor_data:
                return jsonify({"error": "Advisor tidak ditemukan"}), 404
            
            if advisor_data.get('role') != 'advisor':
                return jsonify({"error": "User bukan advisor"}), 400
            
            # Prepare update data
            update_data = {}
            
            if data.get('username'):
                # Check if username already exists (except current user)
                existing_user = db.find_user_by_username(data.get('username'))
                if existing_user and existing_user.get('user_id') != user_id:
                    return jsonify({"error": "Username sudah digunakan"}), 409
                update_data['username'] = data.get('username')
            
            if data.get('email'):
                # Check if email already exists (except current user)
                existing_user = db.find_user_by_email(data.get('email'))
                if existing_user and existing_user.get('user_id') != user_id:
                    return jsonify({"error": "Email sudah digunakan"}), 409
                update_data['email'] = data.get('email')
            
            if data.get('password'):
                # Hash new password
                advisor = UserModel()
                advisor.set_password(data.get('password'))
                update_data['password_hash'] = advisor.password_hash
            
            if not update_data:
                return jsonify({"error": "Tidak ada data yang diubah"}), 400
            
            # Update advisor
            result = db.update_user(user_id, update_data)
            if result.modified_count > 0:
                return jsonify({"message": "Advisor berhasil diupdate"}), 200
            else:
                return jsonify({"message": "Tidak ada perubahan"}), 200
            
        except Exception as e:
            return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 500
    
    @staticmethod
    @jwt_required()
    def delete_advisor():
        """Delete advisor account"""
        # Check if user is admin
        error_response = AdminController.require_admin()
        if error_response:
            return error_response
        
        try:
            data = request.json
            user_id = data.get('user_id')
            
            if not user_id:
                return jsonify({"error": "User ID diperlukan"}), 400
            
            # Find advisor
            advisor_data = db.find_user_by_id(user_id)
            if not advisor_data:
                return jsonify({"error": "Advisor tidak ditemukan"}), 404
            
            if advisor_data.get('role') != 'advisor':
                return jsonify({"error": "User bukan advisor"}), 400
            
            # Soft delete advisor
            result = db.delete_user(user_id)
            if result.modified_count > 0:
                return jsonify({"message": "Advisor berhasil dihapus"}), 200
            else:
                return jsonify({"error": "Gagal menghapus advisor"}), 500
            
        except Exception as e:
            return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 500
