import graphviz
import os
import math
from config import Config
from utils.text_processing import normalize_erd_name

class ERDGenerator:
    """ERD Image Generation Service - Engine-Specific Optimizations"""
    
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
    def has_layout_hints(erd_data):
        """Check if ERD data contains layout hints in relationships"""
        for rel in erd_data.get('relationships', []):
            if 'layout' in rel:
                return True
        return False
    
    @staticmethod
    def calculate_complexity_score(erd_data):
        """Calculate complexity score to determine best engine"""
        num_entities = len(erd_data['entities'])
        num_relationships = len(erd_data['relationships'])
        total_attrs = sum(len(e['attributes']) for e in erd_data['entities'])
        
        complexity = (num_entities * 2) + num_relationships + (total_attrs * 0.3)
        return complexity, num_entities, num_relationships
    
    @staticmethod
    def choose_optimal_engine(erd_data):
        """
        REVOLUTIONARY: ALWAYS USE NEATO with adaptive settings!
        DOT is BANNED because it creates messy layouts for 10+ entities.
        """
        complexity, num_entities, num_relationships = ERDGenerator.calculate_complexity_score(erd_data)
        
        has_hints = ERDGenerator.has_layout_hints(erd_data)
        
        # ALWAYS NEATO - adjust settings based on size
        engine = 'neato'
        if num_entities <= 7:
            reason = "Small diagram - tight neato layout"
        elif num_entities <= 12:
            reason = "Medium diagram - relaxed neato with large spacing"
        else:
            reason = "Large diagram - neato with MAXIMUM spacing (DOT banned!)"
        
        print(f"Engine Selection: {engine} ({reason})")
        print(f"Complexity Score: {complexity:.1f} | Entities: {num_entities} | Relationships: {num_relationships}")
        
        return engine
    
    @staticmethod
    def assign_positions_for_neato(erd_data):
        """Assign explicit positions for neato engine"""
        entity_names = [entity['name'] for entity in erd_data['entities']]
        relationships = erd_data['relationships']
        
        positions = {}
        placed = set()
        
        num_entities = len(entity_names)
        
        # ADAPTIVE SPACING - semakin besar diagram, semakin besar spacing
        # Entity dimensions: width=1.8, height=0.7
        # Panjang garis horizontal: x_spacing - 1.8 (dikurangi 2x radius horizontal)
        # Panjang garis vertikal: y_spacing - 0.7 (dikurangi 2x radius vertikal)
        # Untuk menyamakan: y_spacing = x_spacing - 1.1
        
        if num_entities > 15:
            x_spacing = 35.0  # EXTRA LARGE for 16+ entities (overlap=false)
        elif num_entities > 12:
            x_spacing = 25.0  # VERY LARGE for 13-15 entities (vpsc)
        elif num_entities >= 10:
            x_spacing = 15.0  # LARGE for 10-12 entities (vpsc/scalexy)
        elif num_entities >= 4:
            x_spacing = 6.0   # MEDIUM for 4-9 entities
        else:
            x_spacing = 3.0   # SMALL for 1-3 entities
        
        # Y-spacing dibuat lebih kecil untuk mengkompensasi entity rectangular
        y_spacing = x_spacing - 1.1
        
        rel_graph = {}
        for rel in relationships:
            e1, e2 = rel['entity1'], rel['entity2']
            layout = rel.get('layout', 'TB').upper()
            
            if e1 not in rel_graph:
                rel_graph[e1] = []
            if e2 not in rel_graph:
                rel_graph[e2] = []
            
            rel_graph[e1].append({'to': e2, 'layout': layout})
            reverse_layout = {'LR': 'RL', 'RL': 'LR', 'TB': 'BT', 'BT': 'TB'}.get(layout, layout)
            rel_graph[e2].append({'to': e1, 'layout': reverse_layout})
        
        root = None
        for rel in relationships:
            if rel.get('layout', 'TB').upper() in ['TB', 'BT']:
                root = rel['entity1']
                break
        if not root:
            root = entity_names[0]
        
        positions[root] = (0, 0)
        placed.add(root)
        
        queue = [root]
        max_iterations = len(entity_names) * 10
        iteration = 0
        
        while queue and iteration < max_iterations:
            iteration += 1
            current = queue.pop(0)
            current_pos = positions[current]
            
            if current not in rel_graph:
                continue
            
            for conn in rel_graph[current]:
                target = conn['to']
                layout = conn['layout']
                
                if target not in placed:
                    if layout == 'TB':
                        positions[target] = (current_pos[0], current_pos[1] - y_spacing)
                    elif layout == 'BT':
                        positions[target] = (current_pos[0], current_pos[1] + y_spacing)
                    elif layout == 'LR':
                        positions[target] = (current_pos[0] + x_spacing, current_pos[1])
                    elif layout == 'RL':
                        positions[target] = (current_pos[0] - x_spacing, current_pos[1])
                    else:
                        positions[target] = (current_pos[0] + x_spacing, current_pos[1])
                    
                    placed.add(target)
                    queue.append(target)
        
        unplaced = [e for e in entity_names if e not in placed]
        for i, entity in enumerate(unplaced):
            positions[entity] = ((i + 1) * x_spacing, 0)
        
        return positions
    
    @staticmethod
    def get_relationship_directions(entity_name, positions, erd_data):
        """Get relationship directions from this entity"""
        entity_names = [e['name'] for e in erd_data['entities']]
        entity_pos = positions.get(entity_name)
        if not entity_pos:
            return []
        
        directions = []
        
        for rel in erd_data['relationships']:
            other_entity = None
            if rel['entity1'] == entity_name and rel['entity2'] in entity_names:
                other_entity = rel['entity2']
            elif rel['entity2'] == entity_name and rel['entity1'] in entity_names:
                other_entity = rel['entity1']
            
            if other_entity and other_entity in positions:
                other_pos = positions[other_entity]
                dx = other_pos[0] - entity_pos[0]
                dy = other_pos[1] - entity_pos[1]
                
                angle = math.degrees(math.atan2(dy, dx))
                
                directions.append({
                    'angle': angle,
                    'distance': math.sqrt(dx**2 + dy**2),
                    'entity': other_entity
                })
        
        return directions
    
    @staticmethod
    def distribute_attributes_for_neato(entity_name, entity_pos, attributes, positions, erd_data, num_entities):
        """Distribute attributes with smart positioning (ONLY for neato)"""
        entity_x, entity_y = entity_pos
        num_attrs = len(attributes)
        
        if num_attrs == 0:
            return {}
        
        attr_positions = {}
        rel_directions = ERDGenerator.get_relationship_directions(entity_name, positions, erd_data)
        
        # ADAPTIVE RADIUS - semakin besar diagram, semakin jauh atribut
        if num_entities > 15:
            base_radius, clearance = 4.0, 80  # EXTRA LARGE (overlap=false)
        elif num_entities > 12:
            base_radius, clearance = 3.5, 70  # VERY LARGE (vpsc)
        elif num_entities > 10:
            base_radius, clearance = 3.0, 50  # LARGE (vpsc/scalexy)
        elif num_entities >= 4:
            base_radius, clearance = 2.0, 35  # MEDIUM
        else:
            base_radius, clearance = 1.2, 25  # SMALL
        
        blocked_ranges = []
        for rel_dir in rel_directions:
            angle = rel_dir['angle'] % 360
            start_block = (angle - clearance) % 360
            end_block = (angle + clearance) % 360
            blocked_ranges.append((start_block, end_block))
        
        candidate_angles = []
        for angle in range(0, 360, 10):
            is_blocked = False
            for start_block, end_block in blocked_ranges:
                if start_block <= end_block:
                    if start_block <= angle <= end_block:
                        is_blocked = True
                        break
                else:
                    if angle >= start_block or angle <= end_block:
                        is_blocked = True
                        break
            
            if not is_blocked:
                candidate_angles.append(angle)
        
        if len(candidate_angles) < num_attrs:
            candidate_angles = list(range(0, 360, 10))
        
        if num_attrs <= len(candidate_angles):
            step = len(candidate_angles) / num_attrs
            selected_angles = [candidate_angles[int(i * step)] for i in range(num_attrs)]
        else:
            selected_angles = candidate_angles + [90] * (num_attrs - len(candidate_angles))
        
        for i, attr in enumerate(attributes):
            angle = selected_angles[i]
            angle_rad = math.radians(angle)
            radius = base_radius * (1.0 + (i % 3) * 0.15)
            
            attr_x = entity_x + radius * math.cos(angle_rad)
            attr_y = entity_y + radius * math.sin(angle_rad)
            
            attr_node_id = f"{entity_name}_{attr}"
            attr_positions[attr_node_id] = (attr_x, attr_y)
        
        return attr_positions
    
    @staticmethod
    def apply_rank_hints_for_dot(dot, erd_data):
        """Apply ranking hints for dot engine based on layout hints"""
        entity_names = [e['name'] for e in erd_data['entities']]
        relationships = erd_data['relationships']
        
        # Group entities by rank based on TB/BT hints
        ranks = {}
        
        for rel in relationships:
            layout = rel.get('layout', 'TB').upper()
            e1, e2 = rel['entity1'], rel['entity2']
            
            if layout == 'TB':
                if e1 not in ranks:
                    ranks[e1] = 0
                if e2 not in ranks:
                    ranks[e2] = ranks[e1] + 1
                else:
                    ranks[e2] = max(ranks[e2], ranks[e1] + 1)
            elif layout == 'BT':
                if e2 not in ranks:
                    ranks[e2] = 0
                if e1 not in ranks:
                    ranks[e1] = ranks[e2] + 1
                else:
                    ranks[e1] = max(ranks[e1], ranks[e2] + 1)
        
        # Group entities by rank
        rank_groups = {}
        for entity in entity_names:
            rank = ranks.get(entity, 0)
            if rank not in rank_groups:
                rank_groups[rank] = []
            rank_groups[rank].append(entity)
        
        # Apply subgraph ranks
        for rank, entities in rank_groups.items():
            if len(entities) > 1:
                with dot.subgraph() as s:
                    s.attr(rank='same')
                    for entity in entities:
                        s.node(entity)
        
        return dot
    
    @staticmethod
    def generate_erd_image(erd_name, erd_data):
        """Generate ERD with optimal engine selection"""
        try:
            if not erd_data or 'entities' not in erd_data or len(erd_data['entities']) == 0:
                print(f"Error: Invalid ERD data for {erd_name}")
                return None
            
            engine = ERDGenerator.choose_optimal_engine(erd_data)
            
            # ALWAYS USE NEATO NOW!
            return ERDGenerator.generate_with_neato(erd_name, erd_data)
        
        except Exception as e:
            print(f"Error generating ERD for {erd_name}: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    @staticmethod
    def generate_with_neato(erd_name, erd_data):
        """Generate with neato - uses explicit positioning"""
        print("Generating with NEATO engine (explicit positioning)...")
        
        num_entities = len(erd_data['entities'])
        
        dot = graphviz.Digraph(engine='neato', format='png')
        dot.clear()
        
        
        dot.attr(bgcolor='white', dpi='300')
        
        # ADAPTIVE SETTINGS berdasarkan ukuran diagram
        if num_entities <= 7:
            # Small: Strict positioning with scale (works well)
            dot.graph_attr.update({
                'overlap': 'scale',
                'sep': '+0.5',
                'splines': 'line',
                'mode': 'major',
                'epsilon': '0.0001'
            })
            use_pin = True
        elif num_entities <= 10:
            # Medium: Use SCALEXY - better than prism, respects positions
            dot.graph_attr.update({
                'overlap': 'scalexy',  # ✅ Respects initial positions better than prism
                'sep': '+2.0',       
                'splines': 'line',
                'epsilon': '0.001',
                'maxiter': '5000'
            })
            use_pin = False  # Allow minor adjustments
        elif num_entities <= 15:
            # Large: VPSC algorithm - maintains topology better
            dot.graph_attr.update({
                'overlap': 'vpsc',  # ✅ VPSC = Variable Placement with Separation Constraints
                'sep': '+2.5',
                'splines': 'line',
                'maxiter': '8000',
                'epsilon': '0.001'
            })
            use_pin = False
        else:
            # Very Large: Use FALSE with large spacing (no overlap removal)
            dot.graph_attr.update({
                'overlap': 'false',  # ✅ No overlap removal - relies on good spacing
                'sep': '+3.0',
                'splines': 'line',
                'maxiter': '10000',
                'epsilon': '0.0001'
            })
            use_pin = True  # Pin positions since spacing should be sufficient
        
        dot.node_attr.update({'fontname': 'Arial', 'fontsize': '10'})
        dot.edge_attr.update({'fontname': 'Arial Bold', 'fontsize': '9'})
        
        positions = ERDGenerator.assign_positions_for_neato(erd_data)
        entity_names = [e['name'] for e in erd_data['entities']]
        
        # Add entities with positions
        for entity in erd_data['entities']:
            if entity['name'] in positions:
                x, y = positions[entity['name']]
                pos_str = f'{x},{y}!' if use_pin else f'{x},{y}'
                
                dot.node(entity['name'], entity['name'],
                        shape='box', style='filled',
                        fillcolor='white', fontcolor='black',
                        fontname='Arial Bold', fontsize='11',
                        width='1.8', height='0.7',
                        pos=pos_str)
        
        # Add attributes with smart positioning
        all_attr_positions = {}
        for entity in erd_data['entities']:
            if entity['name'] in positions:
                entity_pos = positions[entity['name']]
                attr_positions = ERDGenerator.distribute_attributes_for_neato(
                    entity['name'], entity_pos, entity['attributes'],
                    positions, erd_data, num_entities
                )
                all_attr_positions.update(attr_positions)
        
        added_edges = set()
        
        # Render attributes
        for entity in erd_data['entities']:
            for attr in entity['attributes']:
                attr_node_id = f"{entity['name']}_{attr}"
                
                if attr_node_id in all_attr_positions:
                    attr_x, attr_y = all_attr_positions[attr_node_id]
                    pos_str = f'{attr_x},{attr_y}!' if use_pin else f'{attr_x},{attr_y}'
                    
                    is_pk = 'primary_key' in entity and attr == entity['primary_key']
                    is_fk = 'foreign_keys' in entity and any(
                        fk['name'] == attr if isinstance(fk, dict) else fk == attr 
                        for fk in entity.get('foreign_keys', [])
                    )
                    
                    fillcolor = 'white'
                    fontcolor = 'black'
                    fontname = 'Arial Bold' if (is_pk or is_fk) else 'Arial'
                    
                    if is_pk:
                        label = f'<<U>{attr}</U>>'
                    else :
                        label = attr
                    
                    dot.node(attr_node_id, label,
                            shape='ellipse', style='filled',
                            fillcolor=fillcolor, fontcolor=fontcolor,
                            fontname=fontname, fontsize='9',
                            width='1.2', height='0.5',
                            pos=pos_str)
                    
                    # ⚠️ CRITICAL FIX: Only add edge if not already added
                    edge_key = (attr_node_id, entity['name'])
                    if edge_key not in added_edges:
                        dot.edge(attr_node_id, entity['name'], 
                                arrowhead='none', penwidth='0.5')
                        added_edges.add(edge_key)
        
        # Add relationships
        for i, rel in enumerate(erd_data['relationships']):
            if rel['entity1'] in entity_names and rel['entity2'] in entity_names:
                rel_node_id = f"rel_{i+1}"
                
                if rel['entity1'] in positions and rel['entity2'] in positions:
                    e1_pos = positions[rel['entity1']]
                    e2_pos = positions[rel['entity2']]
                    rel_x = (e1_pos[0] + e2_pos[0]) / 2.0
                    rel_y = (e1_pos[1] + e2_pos[1]) / 2.0
                    pos_str = f'{rel_x},{rel_y}!' if use_pin else f'{rel_x},{rel_y}'
                    
                    dot.node(rel_node_id, rel.get('name', rel['relation']),
                            shape='diamond', style='filled',
                            fillcolor='white', fontcolor='black',
                            fontname='Arial Bold', fontsize='10',
                            width='1.4', height='0.8',
                            pos=pos_str)
                    
                    card = ERDGenerator.convert_relationship_to_cardinality(rel['type'])
                    edge1_key = (rel['entity1'], rel_node_id)
                    edge2_key = (rel_node_id, rel['entity2'])
                    
                    if edge1_key not in added_edges:
                        dot.edge(rel['entity1'], rel_node_id, 
                                label=card['entity1'], arrowhead='none', 
                                fontsize='10', fontname='Arial Bold',
                                fontcolor='#2C3E50', penwidth='1.5')
                        added_edges.add(edge1_key)
                    
                    if edge2_key not in added_edges:
                        dot.edge(rel_node_id, rel['entity2'], 
                                label=card['entity2'], arrowhead='none',
                                fontsize='10', fontname='Arial Bold',
                                fontcolor='#2C3E50', penwidth='1.5')
                        added_edges.add(edge2_key)
        
        return ERDGenerator._save_diagram(dot, erd_name)
    
    @staticmethod
    def generate_with_fdp(erd_name, erd_data):
        """Generate with fdp - NO explicit positioning, relies on spring model"""
        print("Generating with FDP engine (spring-based layout)...")
        
        dot = graphviz.Digraph(engine='fdp', format='png')
        dot.attr(bgcolor='white', dpi='300')
        
        # FDP-specific settings - NO positions
        dot.graph_attr.update({
            'overlap': 'false',
            'sep': '+3',
            'splines': 'curved',
            'K': '2.5',
            'maxiter': '5000',
            'start': 'random5'
        })
        
        dot.node_attr.update({'fontname': 'Arial', 'fontsize': '10'})
        dot.edge_attr.update({
            'fontname': 'Arial Bold',
            'fontsize': '9',
            'len': '3.0'
        })
        
        entity_names = [e['name'] for e in erd_data['entities']]
        
        # Add entities WITHOUT positions (let FDP decide)
        for entity in erd_data['entities']:
            dot.node(entity['name'], entity['name'],
                    shape='box', style='filled',
                    fillcolor='#2C3E50', fontcolor='white',
                    fontname='Arial Bold', fontsize='11',
                    width='1.8', height='0.7')
        
        # Add attributes
        for entity in erd_data['entities']:
            for attr in entity['attributes']:
                attr_node_id = f"{entity['name']}_{attr}"
                
                is_pk = 'primary_key' in entity and attr == entity['primary_key']
                is_fk = 'foreign_keys' in entity and any(
                    fk['name'] == attr if isinstance(fk, dict) else fk == attr 
                    for fk in entity.get('foreign_keys', [])
                )
                
                if is_pk:
                    fillcolor, fontcolor, fontname = '#F39C12', '#2C3E50', 'Arial Bold'
                elif is_fk:
                    fillcolor, fontcolor, fontname = '#E67E22', 'white', 'Arial Bold'
                else:
                    fillcolor, fontcolor, fontname = '#27AE60', 'white', 'Arial'
                
                dot.node(attr_node_id, attr,
                        shape='ellipse', style='filled',
                        fillcolor=fillcolor, fontcolor=fontcolor,
                        fontname=fontname, fontsize='9',
                        width='1.2', height='0.5')
                
                dot.edge(attr_node_id, entity['name'], 
                        arrowhead='none', penwidth='0.5',
                        weight='10')
        
        # Add relationships
        for i, rel in enumerate(erd_data['relationships']):
            if rel['entity1'] in entity_names and rel['entity2'] in entity_names:
                rel_node_id = f"rel_{i+1}"
                
                dot.node(rel_node_id, rel.get('name', rel['relation']),
                        shape='diamond', style='filled',
                        fillcolor='#F39C12', fontcolor='white',
                        fontname='Arial Bold', fontsize='10',
                        width='1.4', height='0.8')
                
                card = ERDGenerator.convert_relationship_to_cardinality(rel['type'])
                dot.edge(rel['entity1'], rel_node_id, 
                        label=card['entity1'], arrowhead='none', 
                        fontsize='10', fontname='Arial Bold',
                        fontcolor='#2C3E50', penwidth='1.5',
                        weight='5')
                dot.edge(rel_node_id, rel['entity2'], 
                        label=card['entity2'], arrowhead='none',
                        fontsize='10', fontname='Arial Bold',
                        fontcolor='#2C3E50', penwidth='1.5',
                        weight='5')
        
        return ERDGenerator._save_diagram(dot, erd_name)
    
    @staticmethod
    def generate_with_dot(erd_name, erd_data):
        """IMPROVED: Generate with dot - better spacing to reduce overlap"""
        print("Generating with DOT engine (hierarchical layout)...")
        
        dot = graphviz.Digraph(engine='dot', format='png')
        dot.attr(bgcolor='white', dpi='300')
        
        # Determine main direction from layout hints
        has_lr = any(rel.get('layout', '').upper() in ['LR', 'RL'] 
                     for rel in erd_data['relationships'])
        rankdir = 'LR' if has_lr else 'TB'
        
        # PERBAIKAN: Spacing lebih besar + GARIS TETAP LURUS
        dot.graph_attr.update({
            'rankdir': rankdir,
            'ranksep': '3.0',    # Lebih besar dari 2.5
            'nodesep': '2.5',    # Lebih besar dari 2.0
            'splines': 'line',   # GANTI ke line (garis lurus)
        })
        
        dot.node_attr.update({'fontname': 'Arial', 'fontsize': '10'})
        dot.edge_attr.update({'fontname': 'Arial Bold', 'fontsize': '9'})
        
        entity_names = [e['name'] for e in erd_data['entities']]
        
        # Apply ranking hints based on layout
        dot = ERDGenerator.apply_rank_hints_for_dot(dot, erd_data)
        
        # Add entities
        for entity in erd_data['entities']:
            dot.node(entity['name'], entity['name'],
                    shape='box', style='filled',
                    fillcolor='#2C3E50', fontcolor='white',
                    fontname='Arial Bold', fontsize='11',
                    width='1.8', height='0.7')
        
        # Add attributes grouped per entity
        for entity in erd_data['entities']:
            # Create invisible subgraph to group attributes with entity
            with dot.subgraph(name=f'cluster_{entity["name"]}_attrs') as s:
                s.attr(style='invis')
                
                for attr in entity['attributes']:
                    attr_node_id = f"{entity['name']}_{attr}"
                    
                    is_pk = 'primary_key' in entity and attr == entity['primary_key']
                    is_fk = 'foreign_keys' in entity and any(
                        fk['name'] == attr if isinstance(fk, dict) else fk == attr 
                        for fk in entity.get('foreign_keys', [])
                    )
                    
                    if is_pk:
                        fillcolor, fontcolor, fontname = '#F39C12', '#2C3E50', 'Arial Bold'
                    elif is_fk:
                        fillcolor, fontcolor, fontname = '#E67E22', 'white', 'Arial Bold'
                    else:
                        fillcolor, fontcolor, fontname = '#27AE60', 'white', 'Arial'
                    
                    s.node(attr_node_id, attr,
                          shape='ellipse', style='filled',
                          fillcolor=fillcolor, fontcolor=fontcolor,
                          fontname=fontname, fontsize='9',
                          width='1.2', height='0.5')
                    
                    dot.edge(attr_node_id, entity['name'], 
                            arrowhead='none', penwidth='0.5',
                            constraint='false')
        
        # Add relationships
        for i, rel in enumerate(erd_data['relationships']):
            if rel['entity1'] in entity_names and rel['entity2'] in entity_names:
                rel_node_id = f"rel_{i+1}"
                
                dot.node(rel_node_id, rel.get('name', rel['relation']),
                        shape='diamond', style='filled',
                        fillcolor='#F39C12', fontcolor='white',
                        fontname='Arial Bold', fontsize='10',
                        width='1.4', height='0.8')
                
                card = ERDGenerator.convert_relationship_to_cardinality(rel['type'])
                dot.edge(rel['entity1'], rel_node_id, 
                        label=card['entity1'], arrowhead='none', 
                        fontsize='10', fontname='Arial Bold',
                        fontcolor='#2C3E50', penwidth='1.5')
                dot.edge(rel_node_id, rel['entity2'], 
                        label=card['entity2'], arrowhead='none',
                        fontsize='10', fontname='Arial Bold',
                        fontcolor='#2C3E50', penwidth='1.5')
        
        return ERDGenerator._save_diagram(dot, erd_name)
    
    @staticmethod
    def _save_diagram(dot, erd_name):
        """Save diagram to file - FIXED: Remove old file first"""
        filename = normalize_erd_name(erd_name) + "_erd"
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        
        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER)
        
        # ⚠️ CRITICAL FIX: Delete old PNG file if exists
        png_path = f"{filepath}.png"
        if os.path.exists(png_path):
            try:
                os.remove(png_path)
                print(f"Removed old file: {png_path}")
            except Exception as e:
                print(f"Warning: Could not remove old file: {e}")
        
        dot.render(filepath, format='png', cleanup=True)
        print(f"Successfully generated: {filename}.png")
        return f"{filename}.png"

# Global ERD generator instance
erd_generator = ERDGenerator()