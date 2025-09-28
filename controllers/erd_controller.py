from flask import jsonify, request, url_for, send_from_directory
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
        
        # Create ERD model
        erd_model = ERDModel(
            name=data.get("name", ""),
            entities=data.get("entities", []),
            relationships=data.get("relationships", [])
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