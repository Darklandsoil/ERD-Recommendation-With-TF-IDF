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
    def add_erd():
        """Add new ERD to database"""
        data = request.json
        
        # Get advisor_id if provided (for direct creation by advisor)
        advisor_id = data.get("advisor_id", None)
        
        # Create ERD model
        erd_model = ERDModel(
            name=data.get("name", ""),
            entities=data.get("entities", []),
            relationships=data.get("relationships", []),
            advisor_id=advisor_id
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
            return jsonify({"message": "ERD berhasil disimpan"}), 201
        else:
            return jsonify({"error": "ERD dengan nama tersebut sudah ada"}), 409
    
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
            
            erds = db.get_erds_by_advisor(user_id)
            erd_list = []
            
            for erd in erds:
                erd_result = erd.get('erd_result')
                
                #jika tidak ada erd result maka skip
                if not erd_result:
                    continue
                
                entities = erd_result.get("entities", [])
                relationships = erd_result.get("relationships", [])
        
                erd_list.append({
                    "nama" : erd_result.get("name"),
                    "entity_count" : len(entities),
                    "relationship_count" : len(relationships),
                    "created_at" : erd.get('created_at')
                })
            
            return jsonify({"erds": erd_list}), 200
            
        except Exception as e:
             print(f"Error in get_advisor_erds: {str(e)}")  # Untuk debugging
             return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 500

        """Reload recommendation system"""
        try:
            recommendation_service.reload_system()
            return jsonify({"message": "Sistem rekomendasi berhasil di-reload"}), 200
        except Exception as e:
            return jsonify({"error": f"Gagal reload sistem: {str(e)}"}), 500