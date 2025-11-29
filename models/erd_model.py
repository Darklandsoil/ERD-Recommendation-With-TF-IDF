from utils.text_processing import normalize_erd_name
from datetime import datetime
import uuid

class ERDModel:
    """ERD data model"""
    
    def __init__(self, name, entities, relationships, advisor_id=None, mode="manual", request_id=None):
        self.erd_id = str(uuid.uuid4())
        self.name = normalize_erd_name(name)
        self.entities = entities
        self.relationships = relationships
        self.advisor_id = advisor_id  # ID of advisor who created this ERD
        self.mode = mode  # "manual" or "from_request"
        self.request_id = request_id  # Reference to request if mode is "from_request"
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def to_dict(self):
        """Convert ERD model to dictionary"""
        return {
            "erd_id": self.erd_id,
            "name": self.name,
            "entities": self.entities,
            "relationships": self.relationships,
            "advisor_id": self.advisor_id,
            "mode": self.mode,
            "request_id": self.request_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def validate(self):
        """Validate ERD data"""
        if not self.name or not self.entities or not self.relationships:
            return False, "Data tidak lengkap"
        
        # Validate mode
        if self.mode not in ["manual", "from_request"]:
            return False, "Mode harus 'manual' atau 'from_request'"
        
        # Validate entities
        for entity in self.entities:
            if 'name' not in entity or 'attributes' not in entity:
                return False, "Format entitas tidak valid"
        
        # Validate relationships
        entity_names = [e['name'] for e in self.entities]
        for rel in self.relationships:
            if 'entity1' not in rel or 'entity2' not in rel or 'type' not in rel:
                return False, "Format relasi tidak valid"
            if rel['entity1'] not in entity_names or rel['entity2'] not in entity_names:
                return False, "Relasi mengacu pada entitas yang tidak ada"
            
            # Validate relationship attributes (only for many-to-many)
            if 'attributes' in rel:
                if not isinstance(rel['attributes'], list):
                    return False, "Atribut relasi harus berupa list"
                # Only many-to-many relationships should have attributes
                if rel['type'] != 'many-to-many' and len(rel['attributes']) > 0:
                    return False, "Hanya relasi many-to-many yang dapat memiliki atribut"
        
        return True, "Valid"
    
    @classmethod
    def from_dict(cls, data):
        """Create ERDModel from dictionary"""
        erd = cls(
            name=data.get("name"),
            entities=data.get("entities", []),
            relationships=data.get("relationships", []),
            advisor_id=data.get("advisor_id"),
            mode=data.get("mode", "manual"),
            request_id=data.get("request_id")
        )
        erd.erd_id = data.get("erd_id", str(uuid.uuid4()))
        erd.created_at = data.get("created_at", datetime.now())
        erd.updated_at = data.get("updated_at", datetime.now())
        return erd
    
    def create_document_text(self):
        """Create text document for TF-IDF processing"""
        doc_parts = []
        
        # Add ERD name
        doc_parts.append(self.name.replace('_', ' '))
        
        # Add entity names and attributes
        for entity in self.entities:
            doc_parts.append(entity['name'])
            doc_parts.extend(entity['attributes'])
        
        # Add relationship information
        for rel in self.relationships:
            doc_parts.append(f"{rel['entity1']} {rel['entity2']} {rel['type']} {rel['layout']}")
            # Add relationship attributes (for many-to-many)
            if 'attributes' in rel and rel['attributes']:
                doc_parts.extend(rel['attributes'])
        
        return ' '.join(doc_parts).lower()