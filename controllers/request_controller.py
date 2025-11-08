from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.database import db
from models.request_model import RequestModel
from models.user_model import UserModel
from datetime import datetime

class RequestController:
    """Request management controller"""
    
    @staticmethod
    @jwt_required()
    def create_request():
        """Create new ERD request"""
        try:
            data = request.json
            user_id = get_jwt_identity()
            
            # Create request model
            erd_request = RequestModel(
                user_id=user_id,
                query=data.get('query'),
                description=data.get('description'),
                notes_from_user=data.get('notes_from_user')
            )
            
            # Validate request data
            is_valid, errors = erd_request.validate()
            if not is_valid:
                return jsonify({"error": "; ".join(errors)}), 400
            
            # Save to database
            result = db.create_request(erd_request.to_dict())
            if result:
                return jsonify({
                    "message": "Request berhasil dibuat",
                    "request": {
                        "request_id": erd_request.request_id,
                        "query": erd_request.query,
                        "description": erd_request.description,
                        "status": erd_request.status,
                        "notes_from_user": erd_request.notes_from_user,
                        "created_at": erd_request.created_at.isoformat()
                    }
                }), 201
            else:
                return jsonify({"error": "Gagal membuat request"}), 500
                
        except Exception as e:
            return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 500
    
    @staticmethod
    @jwt_required()
    def get_user_requests():
        """Get all requests by current user"""
        try:
            user_id = get_jwt_identity()
            requests_data = db.get_requests_by_user(user_id)
            
            requests = []
            for req_data in requests_data:
                req = RequestModel.from_dict(req_data)
                requests.append({
                    "request_id": req.request_id,
                    "query": req.query,
                    "description": req.description,
                    "status": req.status,
                    "status_display": req.get_status_display(),
                    "created_at": req.created_at.isoformat() if req.created_at else None,
                    "updated_at": req.updated_at.isoformat() if req.updated_at else None,
                    "completed_at": req.completed_at.isoformat() if req.completed_at else None,
                    "erd_id": req.erd_id,
                    "notes_from_user": req.notes_from_user,
                    "notes_from_advisor": req.notes_from_advisor
                })
            
            return jsonify({"requests": requests}), 200
            
        except Exception as e:
            return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 500
    
    @staticmethod
    @jwt_required()
    def cancel_request(request_id):
        """Cancel pending request"""
        try:
            user_id = get_jwt_identity()
            
            # Find request
            request_data = db.find_request_by_id(request_id)
            if not request_data:
                return jsonify({"error": "Request tidak ditemukan"}), 404
            
            req = RequestModel.from_dict(request_data)
            
            # Check if user owns the request
            if req.user_id != user_id:
                return jsonify({"error": "Tidak memiliki akses ke request ini"}), 403
            
            # Cancel request
            if req.cancel_request():
                db.update_request(request_id, {
                    "status": req.status,
                    "updated_at": req.updated_at
                })
                return jsonify({"message": "Request berhasil dibatalkan"}), 200
            else:
                return jsonify({"error": "Request tidak dapat dibatalkan"}), 400
                
        except Exception as e:
            return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 500
    
    @staticmethod
    @jwt_required() 
    def get_pending_requests():
        """Get all pending requests (for advisors)"""
        try:
            # Check if user is advisor
            claims = get_jwt()
            if claims.get('role') != 'advisor':
                return jsonify({"error": "Akses ditolak - hanya advisor"}), 403
            
            requests_data = db.get_pending_requests()
            
            requests = []
            for req_data in requests_data:
                req = RequestModel.from_dict(req_data)
                
                # Get user info
                user_data = db.find_user_by_id(req.user_id)
                user = UserModel.from_dict(user_data) if user_data else None
                
                requests.append({
                    "request_id": req.request_id,
                    "query": req.query,
                    "description": req.description,
                    "status": req.status,
                    "status_display": req.get_status_display(),
                    "created_at": req.created_at.isoformat() if req.created_at else None,
                    "user": {
                        "username": user.username if user else "Unknown",
                        "email": user.email if user else "Unknown"
                    }
                })
            
            return jsonify({"requests": requests}), 200
            
        except Exception as e:
            return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 500
    
    @staticmethod
    @jwt_required()
    def assign_request(request_id):
        """Assign request to current advisor"""
        try:
            advisor_id = get_jwt_identity()
            
            # Check if user is advisor
            claims = get_jwt()
            if claims.get('role') != 'advisor':
                return jsonify({"error": "Akses ditolak - hanya advisor"}), 403
            
            # Find request
            request_data = db.find_request_by_id(request_id)
            if not request_data:
                return jsonify({"error": "Request tidak ditemukan"}), 404
            
            req = RequestModel.from_dict(request_data)
            
            # Check if request is pending
            if req.status != 'pending':
                return jsonify({"error": "Request sudah diassign atau selesai"}), 400
            
            # Assign advisor
            req.assign_advisor(advisor_id)
            
            # Update in database
            db.update_request(request_id, {
                "advisor_id": req.advisor_id,
                "status": req.status,
                "updated_at": req.updated_at
            })
            
            return jsonify({"message": "Request berhasil diassign"}), 200
            
        except Exception as e:
            return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 500
    
    @staticmethod
    @jwt_required()
    def get_advisor_requests():
        """Get requests assigned to current advisor"""
        try:
            advisor_id = get_jwt_identity()
            
            # Check if user is advisor
            claims = get_jwt()
            if claims.get('role') != 'advisor':
                return jsonify({"error": "Akses ditolak - hanya advisor"}), 403
            
            requests_data = db.get_requests_by_advisor(advisor_id)
            
            requests = []
            for req_data in requests_data:
                req = RequestModel.from_dict(req_data)
                
                # Get user info
                user_data = db.find_user_by_id(req.user_id)
                user = UserModel.from_dict(user_data) if user_data else None
                
                requests.append({
                    "request_id": req.request_id,
                    "query": req.query,
                    "description": req.description,
                    "status": req.status,
                    "status_display": req.get_status_display(),
                    "created_at": req.created_at.isoformat() if req.created_at else None,
                    "updated_at": req.updated_at.isoformat() if req.updated_at else None,
                    "completed_at": req.completed_at.isoformat() if req.completed_at else None,
                    "user": {
                        "username": user.username if user else "Unknown",
                        "email": user.email if user else "Unknown"
                    },
                    "erd_id": req.erd_id,
                    "notes_from_user": req.notes_from_user,
                    "notes_from_advisor": req.notes_from_advisor
                })
            
            return jsonify({"requests": requests}), 200
            
        except Exception as e:
            return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 500
    
    @staticmethod
    @jwt_required()
    def complete_request(request_id):
        """Complete request with ERD ID"""
        try:
            advisor_id = get_jwt_identity()
            data = request.json
            
            # Check if user is advisor
            claims = get_jwt()
            if claims.get('role') != 'advisor':
                return jsonify({"error": "Akses ditolak - hanya advisor"}), 403
            
            # Find request
            request_data = db.find_request_by_id(request_id)
            if not request_data:
                return jsonify({"error": "Request tidak ditemukan"}), 404
            
            req = RequestModel.from_dict(request_data)
            
            # Check if advisor owns the request
            if req.advisor_id != advisor_id:
                return jsonify({"error": "Tidak memiliki akses ke request ini"}), 403
            
            # Check if request is in progress
            if req.status != 'on_process':
                return jsonify({"error": "Request tidak dalam status on_process"}), 400
            
            # Get ERD ID from request (ERD should be created beforehand)
            erd_id = data.get('erd_id')
            notes = data.get('notes', '')
            
            if not erd_id:
                return jsonify({"error": "ERD ID diperlukan"}), 400
            
            # Verify ERD exists and belongs to this advisor
            erd_data = db.find_erd_by_id(erd_id)
            if not erd_data:
                return jsonify({"error": "ERD tidak ditemukan"}), 404
            
            if erd_data.get('advisor_id') != advisor_id:
                return jsonify({"error": "ERD tidak dimiliki oleh advisor ini"}), 403
            
            # Complete request with erd_id reference
            req.complete_request(erd_id, notes)
            
            # Update request in database
            db.update_request(request_id, {
                "erd_id": req.erd_id,
                "notes_from_advisor": req.notes_from_advisor,
                "status": req.status,
                "completed_at": req.completed_at,
                "updated_at": req.updated_at
            })
            
            return jsonify({
                "message": "Request berhasil diselesaikan",
                "erd_id": erd_id
            }), 200
            
        except Exception as e:
            return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 500