import graphviz
import os
from config import Config
from utils.text_processing import normalize_erd_name

class ERDGenerator:
    """ERD Image Generation Service"""
    
    @staticmethod
    def convert_relationship_to_cardinality(relationship_type):
        """Convert relationship type to cardinality format"""
        cardinality_map = {
            'one-to-one': {'entity1': '1', 'entity2': '1'},
            'one-to-many': {'entity1': '1', 'entity2': 'M'},
            'many-to-one': {'entity1': 'M', 'entity2': '1'},
            'many-to-many': {'entity1': 'M', 'entity2': 'M'}
        }
        
        return cardinality_map.get(relationship_type.lower(), {'entity1': '1', 'entity2': 'M'})
    
    @staticmethod
    def generate_erd_image(erd_name, erd_data):
        """Generate ERD image with proper visualization standards"""
        dot = graphviz.Digraph(format='png')
        dot.attr(nodesep="0.8", ranksep="1.2", bgcolor="white")
        dot.attr(dpi='300')  # High resolution

        # Add entities (rectangle shape)
        for entity in erd_data['entities']:
            entity_label = entity['name']
            dot.node(entity['name'], entity_label, 
                    shape='rectangle', 
                    style='filled', 
                    fillcolor='lightblue',
                    fontname='Arial Bold',
                    fontsize='12')
            
            # Add attributes (ellipse shape)
            for attr in entity['attributes']:
                attr_node_id = f"{entity['name']}_{attr}"
                
                # Mark primary key with underline
                if 'primary_key' in entity and attr == entity['primary_key']:
                    attr_label = f"<u>{attr}</u>"
                    dot.node(attr_node_id, f"<{attr_label}>", 
                            shape='ellipse',
                            style='filled',
                            fillcolor='yellow',
                            fontname='Arial',
                            fontsize='10')
                else:
                    dot.node(attr_node_id, attr, 
                            shape='ellipse',
                            style='filled',
                            fillcolor='lightgreen',
                            fontname='Arial',
                            fontsize='10')
                
                # Connect attribute to entity
                dot.edge(entity['name'], attr_node_id, arrowhead='none', len='0.5')

        # Add relationships (diamond shape)
        relationship_counter = 0
        for relation in erd_data['relationships']:
            entity_names = [e['name'] for e in erd_data['entities']]
            if relation['entity1'] in entity_names and relation['entity2'] in entity_names:
                relationship_counter += 1
                rel_node_id = f"rel_{relationship_counter}"
                
                # Relationship node (diamond shape)
                rel_label = relation.get('name', relation['relation'])
                dot.node(rel_node_id, rel_label,
                        shape='diamond',
                        style='filled',
                        fillcolor='orange',
                        fontname='Arial',
                        fontsize='10')
                
                # Convert relationship type to cardinality
                cardinality = ERDGenerator.convert_relationship_to_cardinality(relation['type'])
                
                # Edge from entity1 to relationship
                dot.edge(relation['entity1'], rel_node_id, 
                        label=cardinality['entity1'],
                        arrowhead='none',
                        fontsize='9',
                        fontname='Arial Bold')
                
                # Edge from relationship to entity2
                dot.edge(rel_node_id, relation['entity2'],
                        label=cardinality['entity2'],
                        arrowhead='none',
                        fontsize='9',
                        fontname='Arial Bold')

        filename = normalize_erd_name(erd_name) + "_erd"
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        dot.render(filepath, format='png', cleanup=True)

        return f"{filename}.png"

# Global ERD generator instance
erd_generator = ERDGenerator()