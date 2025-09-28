from utils.text_processing import normalize_erd_name

class ERDModel:
    """ERD data model"""
    
    def __init__(self, name, entities, relationships):
        self.name = normalize_erd_name(name)
        self.entities = entities
        self.relationships = relationships
    
    def to_dict(self):
        """Convert ERD model to dictionary"""
        return {
            "name": self.name,
            "entities": self.entities,
            "relationships": self.relationships
        }
    
    def validate(self):
        """Validate ERD data"""
        if not self.name or not self.entities or not self.relationships:
            return False, "Data tidak lengkap"
        
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
        
        return True, "Valid"
    
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
            doc_parts.append(f"{rel['entity1']} {rel['entity2']} {rel['type']}")
        
        return ' '.join(doc_parts).lower()