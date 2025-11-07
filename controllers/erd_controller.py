from flask import jsonify, request, url_for, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.database import db
from models.erd_model import ERDModel
from services.recommendation_service import recommendation_service
from services.erd_generator import erd_generator
from config import Config

class ERDController:
    """Controller for ERD operations"""
    
    @staticmethod
    def search_erd():
        """Search ERDs with similarity scoring"""
        data = request.json
        query = data.get("text", "").strip()
        top_k = data.get("top_k", Config.DEFAULT_TOP_K)
        min_similarity = data.get("min_similarity", Config.DEFAULT_MIN_SIMILARITY)
        
        if not query:
            return jsonify({"error": "Query tidak boleh kosong"}), 400
        
        recommendations = recommendation_service.recommend_erds(query, top_k, min_similarity)
        
        results = []
        for rec in recommendations:
            erd = rec['erd']
            results.append({
                'name': erd['name'].replace('_', ' ').title(),
                'similarity': round(rec['similarity'], 4),
                'entities': [entity['name'] for entity in erd['entities']],
                'entity_count': len(erd['entities']),
                'relationship_count': len(erd['relationships'])
            })
        
        return jsonify({
            "query": query,
            "results": results,
            "total_found": len(results)
        })
    
    @staticmethod
    @jwt_required()
    def add_erd():
        """Add new ERD to database (manual mode for advisors)"""
        try:
            data = request.json
            user_id = get_jwt_identity()
            claims = get_jwt()
            user_role = claims.get('role')
            
            # Only advisors can create manual ERDs
            if user_role != 'advisor':
                return jsonify({"error": "Hanya advisor yang dapat membuat ERD manual"}), 403
            
            # Create ERD model with manual mode
            erd_model = ERDModel(
                name=data.get("name", ""),
                entities=data.get("entities", []),
                relationships=data.get("relationships", []),
                advisor_id=user_id,
                mode="manual"
            )
            
            # Validate ERD data
            is_valid, message = erd_model.validate()
            if not is_valid:
                return jsonify({"error": message}), 400
            
            # Save to database
            result = db.save_erd(erd_model.to_dict())
            if result:
                # Reload recommendation system
                recommendation_service.reload_system()
                return jsonify({
                    "message": "ERD berhasil disimpan",
                    "erd_id": erd_model.erd_id
                }), 201
            else:
                return jsonify({"error": "Gagal menyimpan ERD"}), 500
                
        except Exception as e:
            return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 500
    
    @staticmethod
    def list_erds():
        """List all ERDs"""
        erds = db.get_erds_for_display()
        return jsonify({"erds": erds})
    
    @staticmethod
    def generate_erd_image(erd_name):
        """Generate ERD image by name"""
        try:
            # Find ERD by name
            erd = db.find_erd_by_name(erd_name)
            if not erd:
                return jsonify({"error": "ERD tidak ditemukan"}), 404
            
            # Generate ERD image
            filename = erd_generator.generate_erd_image(erd_name, erd)
            
            return jsonify({
                "erd_image": url_for('static', filename=f'image/{filename}'),
                "erd_name": erd['name'].replace('_', ' ').title(),
                "download_url": url_for('api.download_erd', filename=filename)
            })
            
        except Exception as e:
            return jsonify({"error": f"Gagal generate ERD: {str(e)}"}), 500
    
    @staticmethod
    def download_erd(filename):
        """Download ERD file"""
        try:
            return send_from_directory(Config.UPLOAD_FOLDER, filename, as_attachment=True)
        except Exception as e:
            return jsonify({"error": "File tidak ditemukan"}), 404
    
    @staticmethod
    def reload_system():
        """Reload recommendation system"""
        try:
            recommendation_service.reload_system()
            return jsonify({"message": "Sistem rekomendasi berhasil di-reload"}), 200
        except Exception as e:
            return jsonify({"error": f"Gagal reload sistem: {str(e)}"}), 500
    
    @staticmethod
    @jwt_required()
    def delete_erd():
        """Delete ERD (only by advisor who created it)"""
        try:
            data = request.json
            erd_name = data.get("erd_name")
            
            if not erd_name:
                return jsonify({"error": "Nama ERD diperlukan"}), 400
            
            # Get current user
            user_id = get_jwt_identity()
            claims = get_jwt()
            user_role = claims.get('role')
            
            # Find ERD
            erd = db.find_erd_by_name(erd_name)
            if not erd:
                return jsonify({"error": "ERD tidak ditemukan"}), 404
            
            # Check if user is advisor and is the creator
            if user_role != 'advisor':
                return jsonify({"error": "Hanya advisor yang dapat menghapus ERD"}), 403
            
            if erd.get('advisor_id') != user_id:
                return jsonify({"error": "Anda hanya dapat menghapus ERD yang Anda buat"}), 403
            
            # Delete ERD
            result = db.delete_erd(erd_name)
            if result.deleted_count > 0:
                # Reload recommendation system
                recommendation_service.reload_system()
                return jsonify({"message": "ERD berhasil dihapus"}), 200
            else:
                return jsonify({"error": "Gagal menghapus ERD"}), 500
            
        except Exception as e:
            return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 500
    
    @staticmethod
    @jwt_required()
    def get_advisor_erds():
        """Get all ERDs created by current advisor"""
        try:
            user_id = get_jwt_identity()
            claims = get_jwt()
            user_role = claims.get('role')
            
            if user_role != 'advisor':
                return jsonify({"error": "Hanya advisor yang dapat mengakses ini"}), 403
            
            # Get ERDs from ERD collection by advisor_id
            erds = db.get_erds_by_advisor_id(user_id)
            erd_list = []
            
            for erd_data in erds:
                entities = erd_data.get("entities", [])
                relationships = erd_data.get("relationships", [])
        
                erd_list.append({
                    "erd_id": erd_data.get("erd_id"),
                    "name": erd_data.get("name"),
                    "display_name": erd_data.get("name", "").replace('_', ' ').title(),
                    "entity_count": len(entities),
                    "relationship_count": len(relationships),
                    "mode": erd_data.get("mode"),
                    "created_at": erd_data.get("created_at").isoformat() if erd_data.get("created_at") else None,
                    "updated_at": erd_data.get("updated_at").isoformat() if erd_data.get("updated_at") else None
                })
            
            return jsonify({"erds": erd_list}), 200
            
        except Exception as e:
            print(f"Error in get_advisor_erds: {str(e)}")  # Untuk debugging
            return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 500
    
    @staticmethod
    @jwt_required()
    def get_erd_detail(erd_id):
        """Get ERD detail by ID"""
        try:
            user_id = get_jwt_identity()
            claims = get_jwt()
            user_role = claims.get('role')
            
            # Find ERD
            erd_data = db.find_erd_by_id(erd_id)
            if not erd_data:
                return jsonify({"error": "ERD tidak ditemukan"}), 404
            
            # Check access: advisors can only view their own ERDs
            if user_role == 'advisor' and erd_data.get('advisor_id') != user_id:
                return jsonify({"error": "Anda tidak memiliki akses ke ERD ini"}), 403
            
            return jsonify({
                "erd": {
                    "erd_id": erd_data.get("erd_id"),
                    "name": erd_data.get("name"),
                    "entities": erd_data.get("entities"),
                    "relationships": erd_data.get("relationships"),
                    "mode": erd_data.get("mode"),
                    "advisor_id": erd_data.get("advisor_id"),
                    "request_id": erd_data.get("request_id"),
                    "created_at": erd_data.get("created_at").isoformat() if erd_data.get("created_at") else None,
                    "updated_at": erd_data.get("updated_at").isoformat() if erd_data.get("updated_at") else None
                }
            }), 200
            
        except Exception as e:
            return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 500
    
    @staticmethod
    @jwt_required()
    def update_erd(erd_id):
        """Update ERD (only by advisor who created it)"""
        try:
            user_id = get_jwt_identity()
            claims = get_jwt()
            user_role = claims.get('role')
            data = request.json
            
            if user_role != 'advisor':
                return jsonify({"error": "Hanya advisor yang dapat mengedit ERD"}), 403
            
            # Find ERD
            erd_data = db.find_erd_by_id(erd_id)
            if not erd_data:
                return jsonify({"error": "ERD tidak ditemukan"}), 404
            
            # Check if advisor owns the ERD
            if erd_data.get('advisor_id') != user_id:
                return jsonify({"error": "Anda hanya dapat mengedit ERD yang Anda buat"}), 403
            
            # Prepare update data
            from datetime import datetime
            update_data = {
                "updated_at": datetime.now()
            }
            
            if data.get('name'):
                from utils.text_processing import normalize_erd_name
                update_data['name'] = normalize_erd_name(data.get('name'))
            
            if data.get('entities'):
                update_data['entities'] = data.get('entities')
            
            if data.get('relationships'):
                update_data['relationships'] = data.get('relationships')
            
            # Update ERD
            result = db.update_erd(erd_id, update_data)
            if result.modified_count > 0:
                # Reload recommendation system
                recommendation_service.reload_system()
                return jsonify({"message": "ERD berhasil diupdate"}), 200
            else:
                return jsonify({"message": "Tidak ada perubahan"}), 200
            
        except Exception as e:
            return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 500
    
    @staticmethod
    @jwt_required()
    def delete_erd_by_id(erd_id):
        """Delete ERD by ID (only by advisor who created it)"""
        try:
            user_id = get_jwt_identity()
            claims = get_jwt()
            user_role = claims.get('role')
            
            if user_role != 'advisor':
                return jsonify({"error": "Hanya advisor yang dapat menghapus ERD"}), 403
            
            # Find ERD
            erd_data = db.find_erd_by_id(erd_id)
            if not erd_data:
                return jsonify({"error": "ERD tidak ditemukan"}), 404
            
            # Check if advisor owns the ERD
            if erd_data.get('advisor_id') != user_id:
                return jsonify({"error": "Anda hanya dapat menghapus ERD yang Anda buat"}), 403
            
            # Delete ERD
            result = db.delete_erd_by_id(erd_id)
            if result.deleted_count > 0:
                # Reload recommendation system
                recommendation_service.reload_system()
                return jsonify({"message": "ERD berhasil dihapus"}), 200
            else:
                return jsonify({"error": "Gagal menghapus ERD"}), 500
            
        except Exception as e:
            return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 500