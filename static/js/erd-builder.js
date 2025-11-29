// ==========================================
// ERD BUILDER JAVASCRIPT
// Real-time ERD Preview dengan @hpcc-js/wasm
// ==========================================

// Global state
let entities = [];
let relationships = [];
let entityCounter = 0;
let relationshipCounter = 0;
let currentSVG = null;
let graphviz = null;
let currentZoom = 1.0; // Zoom level (1.0 = 100%)
const ZOOM_STEP = 0.1; // 10% per step
const MIN_ZOOM = 0.3; // 30%
const MAX_ZOOM = 3.0; // 300%

// Mode & Context
let currentMode = 'manual'; // 'manual', 'from_request', 'edit'
let requestId = null;
let editingErdId = null;

// Initialize @hpcc-js/wasm Graphviz
async function initGraphviz() {
    try {
        console.log('Initializing @hpcc-js/wasm Graphviz...');
        const wasmFolder = await window["@hpcc-js/wasm"];
        graphviz = await wasmFolder.Graphviz.load();
        console.log('✅ Graphviz initialized successfully');
        return true;
    } catch (error) {
        console.error('❌ Failed to initialize Graphviz:', error);
        showErrorPopup('Gagal memuat Graphviz. Silakan refresh halaman.');
        return false;
    }
}

// Parse URL parameters
function parseURLParams() {
    const urlParams = new URLSearchParams(window.location.search);
    currentMode = urlParams.get('mode') || 'manual';
    requestId = urlParams.get('request_id') || null;
    editingErdId = urlParams.get('erd_id') || null;
    
    console.log('URL Params:', { currentMode, requestId, editingErdId });
}

// Initialize on page load
window.addEventListener('load', async function() {
    parseURLParams();
    await initGraphviz();
    
    // Load data based on mode
    if (currentMode === 'edit' && editingErdId) {
        await loadERDForEdit(editingErdId);
    } else {
        renderEntitiesForm();
        renderRelationshipsForm();
    }

    //SETUP ZOOM CONTROLS
     setupZoomControls();
});

// Add Entity
function addEntity() {
    const entity = {
        id: `entity_${++entityCounter}`,
        name: '',
        attributes: [],
        primary_key: ''
    };
    entities.push(entity);
    renderEntitiesForm();
    updatePreview();
}

// Remove Entity
function removeEntity(id) {
    const entity = entities.find(e => e.id === id);
    entities = entities.filter(e => e.id !== id);
    
    if (entity) {
        relationships = relationships.filter(r => 
            r.entity1 !== entity.name && r.entity2 !== entity.name
        );
    }
    
    renderEntitiesForm();
    renderRelationshipsForm();
    updatePreview();
}

// Add Relationship
function addRelationship() {
    if (entities.length < 2) {
        showErrorPopup('Minimal 2 entitas diperlukan untuk membuat relasi');
        return;
    }
    const rel = {
        id: `rel_${++relationshipCounter}`,
        entity1: '',
        entity2: '',
        relation: '',
        type: 'one-to-many',
        layout: 'LR',
        attributes: [] // Support for relationship attributes (many-to-many)
    };
    relationships.push(rel);
    renderRelationshipsForm();
    updatePreview();
}

// Remove Relationship
function removeRelationship(id) {
    relationships = relationships.filter(r => r.id !== id);
    renderRelationshipsForm();
    updatePreview();
}

// Update functions with debounce
function updateEntity(id, field, value) {
    const entity = entities.find(e => e.id === id);
    if (entity) {
        entity[field] = value;
        renderRelationshipsForm();
        debounceUpdate(() => updatePreview());
    }
}

function updateRelationship(id, field, value) {
    const rel = relationships.find(r => r.id === id);
    if (rel) {
        rel[field] = value;
        debounceUpdate(() => updatePreview());
    }
}

function addAttribute(entityId) {
    const input = document.getElementById(`newAttr_${entityId}`);
    const attrName = input.value.trim();
    if (!attrName) return;

    const entity = entities.find(e => e.id === entityId);
    if (entity) {
        entity.attributes.push(attrName);
        input.value = '';
        renderEntitiesForm();
        updatePreview();
    }
}

function removeAttribute(entityId, index) {
    console.log('Removing attribute:', entityId, index);
    const entity = entities.find(e => e.id === entityId);
    if (entity) {
        console.log('Before:', entity.attributes);
        entity.attributes.splice(index, 1);
        console.log('After:', entity.attributes);
        renderEntitiesForm();
        updatePreview();
    }
}

// Add Relationship Attribute (for many-to-many)
function addRelationshipAttribute(relId) {
    const input = document.getElementById(`newRelAttr_${relId}`);
    const attrName = input.value.trim();
    if (!attrName) return;

    const rel = relationships.find(r => r.id === relId);
    if (rel) {
        if (!rel.attributes) {
            rel.attributes = [];
        }
        rel.attributes.push(attrName);
        input.value = '';
        renderRelationshipsForm();
        updatePreview();
    }
}

// Remove Relationship Attribute
function removeRelationshipAttribute(relId, index) {
    const rel = relationships.find(r => r.id === relId);
    if (rel && rel.attributes) {
        rel.attributes.splice(index, 1);
        renderRelationshipsForm();
        updatePreview();
    }
}

// Render forms
function renderEntitiesForm() {
    const container = document.getElementById('entitiesContainer');
    
    if (entities.length === 0) {
        container.innerHTML = `
            <div class="empty-form">
                Belum ada entitas. Klik "Tambah" untuk membuat entitas baru.
            </div>
        `;
        return;
    }

    container.innerHTML = entities.map((entity, idx) => `
        <div class="entity-card" data-entity-id="${entity.id}">
            <div class="entity-header">
                <h4>Entitas ${idx + 1}</h4>
                <button class="btn btn-danger" onclick="removeEntity('${entity.id}')">
                    🗑️
                </button>
            </div>

            <div class="form-group">
                <label>Nama Entitas:</label>
                <input type="text" class="entity-name" value="${entity.name}" 
                       oninput="updateEntity('${entity.id}', 'name', this.value)"
                       placeholder="Nama entitas">
            </div>

            <div class="form-group">
                <label>Primary Key:</label>
                <input type="text" class="entity-pk" value="${entity.primary_key}" 
                       oninput="updateEntity('${entity.id}', 'primary_key', this.value)"
                       placeholder="Primary key (opsional)">
            </div>

            <div class="attribute-list">
                <label>Atribut:</label>
                ${entity.attributes.map((attr, i) => `
                    <div class="attribute-item ${attr === entity.primary_key ? 'primary-key' : ''}">
                        <span>${attr} ${attr === entity.primary_key ? '🔑' : ''}</span>
                        <button class="btn btn-danger btn-remove-attr" style="padding: 2px 6px; font-size: 11px;"
                                type="button"
                                data-entity-id="${entity.id}" data-attr-index="${i}">×</button>
                    </div>
                `).join('')}

                <div class="add-attribute">
                    <input type="text" id="newAttr_${entity.id}" 
                           placeholder="Atribut baru"
                           onkeypress="if(event.key==='Enter') { event.preventDefault(); addAttribute('${entity.id}'); return false; }">
                    <button class="btn btn-success" style="padding: 6px 10px;"
                            type="button"
                            onclick="addAttribute('${entity.id}'); return false;">+</button>
                </div>
            </div>
        </div>
    `).join('');
     // Add event delegation
    container.querySelectorAll('.btn-remove-attr').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const entityId = this.getAttribute('data-entity-id');
            const index = parseInt(this.getAttribute('data-attr-index'));
            removeAttribute(entityId, index);
        });
    });
}

function renderRelationshipsForm() {
    const container = document.getElementById('relationshipsContainer');
    
    if (relationships.length === 0) {
        container.innerHTML = `
            <div class="empty-form">
                Belum ada relasi. Klik "Tambah" untuk membuat relasi baru.
            </div>
        `;
        return;
    }

    container.innerHTML = relationships.map((rel, idx) => {
        const isManyToMany = rel.type === 'many-to-many';
        const relAttributes = rel.attributes || [];
        
        return `
        <div class="entity-card" data-relationship-id="${rel.id}">
            <div class="entity-header">
                <h4>Relasi ${idx + 1}</h4>
                <button class="btn btn-danger" onclick="removeRelationship('${rel.id}')">🗑️</button>
            </div>

            <div class="form-group">
                <label>Entitas 1:</label>
                <select class="relationship-entity1" onchange="updateRelationship('${rel.id}', 'entity1', this.value)">
                    <option value="">Pilih entitas</option>
                    ${entities.map(e => `
                        <option value="${e.name}" ${rel.entity1 === e.name ? 'selected' : ''}>
                            ${e.name || 'Unnamed'}
                        </option>
                    `).join('')}
                </select>
            </div>

            <div class="form-group">
                <label>Entitas 2:</label>
                <select class="relationship-entity2" onchange="updateRelationship('${rel.id}', 'entity2', this.value)">
                    <option value="">Pilih entitas</option>
                    ${entities.map(e => `
                        <option value="${e.name}" ${rel.entity2 === e.name ? 'selected' : ''}>
                            ${e.name || 'Unnamed'}
                        </option>
                    `).join('')}
                </select>
            </div>

            <div class="form-group">
                <label>Nama Relasi:</label>
                <input type="text" class="relationship-name" value="${rel.relation}"
                       oninput="updateRelationship('${rel.id}', 'relation', this.value)"
                       placeholder="Nama relasi">
            </div>

            <div class="form-group">
                <label>Kardinalitas:</label>
                <select class="relationship-type" onchange="updateRelationship('${rel.id}', 'type', this.value); renderRelationshipsForm(); updatePreview();">
                    <option value="one-to-one" ${rel.type === 'one-to-one' ? 'selected' : ''}>One to One</option>
                    <option value="one-to-many" ${rel.type === 'one-to-many' ? 'selected' : ''}>One to Many</option>
                    <option value="many-to-one" ${rel.type === 'many-to-one' ? 'selected' : ''}>Many to One</option>
                    <option value="many-to-many" ${rel.type === 'many-to-many' ? 'selected' : ''}>Many to Many</option>
                </select>
            </div>

            <div class="form-group">
                <label>Layout:</label>
                <select class="relationship-layout" onchange="updateRelationship('${rel.id}', 'layout', this.value)">
                    <option value="LR" ${rel.layout === 'LR' ? 'selected' : ''}>Left to Right</option>
                    <option value="RL" ${rel.layout === 'RL' ? 'selected' : ''}>Right to Left</option>
                    <option value="TB" ${rel.layout === 'TB' ? 'selected' : ''}>Top to Bottom</option>
                    <option value="BT" ${rel.layout === 'BT' ? 'selected' : ''}>Bottom to Top</option>
                </select>
            </div>

            ${isManyToMany ? `
            <div class="attribute-list" style="margin-top: 15px;">
                <label style="color: #2563eb; font-weight: 600;">
                    ⚡ Atribut Relasi (Many-to-Many):
                </label>
                <div style="font-size: 11px; color: #64748b; margin-bottom: 8px;">
                    Atribut yang melekat pada relasi ini
                </div>
                ${relAttributes.map((attr, i) => `
                    <div class="attribute-item">
                        <span>${attr}</span>
                        <button class="btn btn-danger btn-remove-rel-attr" style="padding: 2px 6px; font-size: 11px;"
                                type="button"
                                data-rel-id="${rel.id}" data-attr-index="${i}">×</button>
                    </div>
                `).join('')}

                <div class="add-attribute">
                    <input type="text" id="newRelAttr_${rel.id}" 
                           placeholder="Atribut relasi baru"
                           onkeypress="if(event.key==='Enter') { event.preventDefault(); addRelationshipAttribute('${rel.id}'); return false; }">
                    <button class="btn btn-success" style="padding: 6px 10px;"
                            type="button"
                            onclick="addRelationshipAttribute('${rel.id}'); return false;">+</button>
                </div>
            </div>
            ` : ''}
        </div>
        `;
    }).join('');
    
    // Add event delegation for remove buttons
    container.querySelectorAll('.btn-remove-rel-attr').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const relId = this.getAttribute('data-rel-id');
            const index = parseInt(this.getAttribute('data-attr-index'));
            removeRelationshipAttribute(relId, index);
        });
    });
}

// Calculate positions for entities
function calculateEntityPositions() {
    const numEntities = entities.length;
    if (numEntities === 0) return {};
    
    let xSpacing, ySpacing;
    if (numEntities >= 16) {
        xSpacing = 8.0;
    } else if (numEntities >= 7) {
        xSpacing = 6.0;
    } else {
        xSpacing = 4.0;
    }
    ySpacing = xSpacing - 1.1;
    
    const positions = {};
    const placed = new Set();
    
    const relGraph = {};
    relationships.forEach(rel => {
        const e1 = rel.entity1;
        const e2 = rel.entity2;
        const layout = (rel.layout || 'TB').toUpperCase();
        
        if (!relGraph[e1]) relGraph[e1] = [];
        if (!relGraph[e2]) relGraph[e2] = [];
        
        relGraph[e1].push({ to: e2, layout: layout });
        
        const reverseLayout = {
            'LR': 'RL', 'RL': 'LR', 
            'TB': 'BT', 'BT': 'TB'
        }[layout] || layout;
        relGraph[e2].push({ to: e1, layout: reverseLayout });
    });
    
    let root = null;
    for (const rel of relationships) {
        if (['TB', 'BT'].includes((rel.layout || 'TB').toUpperCase())) {
            root = rel.entity1;
            break;
        }
    }
    if (!root && entities.length > 0) {
        root = entities[0].name.trim() || 'Entitas_1';
    }
    
    if (root) {
        positions[root] = { x: 0, y: 0 };
        placed.add(root);
    }
    
    const queue = [root];
    let iteration = 0;
    const maxIterations = numEntities * 10;
    
    while (queue.length > 0 && iteration < maxIterations) {
        iteration++;
        const current = queue.shift();
        const currentPos = positions[current];
        
        if (!currentPos || !relGraph[current]) continue;
        
        relGraph[current].forEach(conn => {
            const target = conn.to;
            const layout = conn.layout;
            
            if (!placed.has(target)) {
                let newPos = { x: 0, y: 0 };
                
                switch (layout) {
                    case 'TB':
                        newPos = { x: currentPos.x, y: currentPos.y - ySpacing };
                        break;
                    case 'BT':
                        newPos = { x: currentPos.x, y: currentPos.y + ySpacing };
                        break;
                    case 'LR':
                        newPos = { x: currentPos.x + xSpacing, y: currentPos.y };
                        break;
                    case 'RL':
                        newPos = { x: currentPos.x - xSpacing, y: currentPos.y };
                        break;
                    default:
                        newPos = { x: currentPos.x + xSpacing, y: currentPos.y };
                }
                
                positions[target] = newPos;
                placed.add(target);
                queue.push(target);
            }
        });
    }

    const unconnected = entities.filter((entity, idx) => {
        const entityName = entity.name.trim() || `Entitas_${idx + 1}`;
        return !placed.has(entityName);
    });
    
    if (unconnected.length > 0 && placed.size > 0) {
        const placedPositions = Array.from(placed).map(name => positions[name]);
        const minX = Math.min(...placedPositions.map(p => p.x));
        const maxX = Math.max(...placedPositions.map(p => p.x));
        const minY = Math.min(...placedPositions.map(p => p.y));
        const maxY = Math.max(...placedPositions.map(p => p.y));
        
        const startX = minX;
        const startY = maxY + ySpacing * 1.5;
        
        unconnected.forEach((entity, idx) => {
            const entityName = entity.name.trim() || `Entitas_${entities.indexOf(entity) + 1}`;
            positions[entityName] = {
                x: startX + (idx * xSpacing),
                y: startY
            };
            placed.add(entityName);
        });
    } else if (unconnected.length > 0) {
        unconnected.forEach((entity, idx) => {
            const entityName = entity.name.trim() || `Entitas_${entities.indexOf(entity) + 1}`;
            positions[entityName] = {
                x: idx * xSpacing,
                y: 0
            };
            placed.add(entityName);
        });
    }
    
    return positions;
}

// Get relationship directions
function getRelationshipDirections(entityName, positions) {
    const directions = [];
    const entityPos = positions[entityName];
    if (!entityPos) return directions;
    
    relationships.forEach(rel => {
        let otherEntity = null;
        if (rel.entity1 === entityName) {
            otherEntity = rel.entity2;
        } else if (rel.entity2 === entityName) {
            otherEntity = rel.entity1;
        }
        
        if (otherEntity && positions[otherEntity]) {
            const otherPos = positions[otherEntity];
            const dx = otherPos.x - entityPos.x;
            const dy = otherPos.y - entityPos.y;
            const angle = Math.atan2(dy, dx) * (180 / Math.PI);
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            directions.push({ angle, distance, entity: otherEntity });
        }
    });
    
    return directions;
}

// Distribute relationship attributes around diamond (for many-to-many)
function distributeRelationshipAttributes(relId, relPos, attrs, positions, entity1, entity2) {
    const numAttrs = attrs.length;
    if (numAttrs === 0) return {};
    
    const attrPositions = {};
    const baseRadius = 1.3; // Distance from relationship center
    
    // Calculate angles to avoid (where entities connect to relationship)
    const e1Pos = positions[entity1];
    const e2Pos = positions[entity2];
    
    const blockedAngles = [];
    if (e1Pos) {
        const angle1 = Math.atan2(e1Pos.y - relPos.y, e1Pos.x - relPos.x) * (180 / Math.PI);
        blockedAngles.push(((angle1 % 360) + 360) % 360);
    }
    if (e2Pos) {
        const angle2 = Math.atan2(e2Pos.y - relPos.y, e2Pos.x - relPos.x) * (180 / Math.PI);
        blockedAngles.push(((angle2 % 360) + 360) % 360);
    }
    
    // Create clearance zones around blocked angles
    const clearance = 45; // degrees
    const blockedRanges = blockedAngles.map(angle => ({
        start: ((angle - clearance) % 360 + 360) % 360,
        end: ((angle + clearance) % 360 + 360) % 360
    }));
    
    // Find available angles
    const candidateAngles = [];
    for (let angle = 0; angle < 360; angle += 15) {
        let isBlocked = false;
        for (const range of blockedRanges) {
            if (range.start <= range.end) {
                if (angle >= range.start && angle <= range.end) {
                    isBlocked = true;
                    break;
                }
            } else {
                if (angle >= range.start || angle <= range.end) {
                    isBlocked = true;
                    break;
                }
            }
        }
        if (!isBlocked) {
            candidateAngles.push(angle);
        }
    }
    
    // Select angles for attributes
    const selectedAngles = [];
    const availableAngles = candidateAngles.length >= numAttrs 
        ? candidateAngles 
        : Array.from({ length: 24 }, (_, i) => i * 15);
    
    if (numAttrs <= availableAngles.length) {
        const step = availableAngles.length / numAttrs;
        for (let i = 0; i < numAttrs; i++) {
            selectedAngles.push(availableAngles[Math.floor(i * step)]);
        }
    } else {
        selectedAngles.push(...availableAngles);
        while (selectedAngles.length < numAttrs) {
            selectedAngles.push(90);
        }
    }
    
    // Position attributes
    attrs.forEach((attr, i) => {
        const angle = selectedAngles[i];
        const angleRad = (angle * Math.PI) / 180;
        const radius = baseRadius + (i % 2) * 0.15; // Slight variation
        
        const attrX = relPos.x + radius * Math.cos(angleRad);
        const attrY = relPos.y + radius * Math.sin(angleRad);
        
        attrPositions[attr] = { x: attrX, y: attrY };
    });
    
    return attrPositions;
}

// Distribute attributes smartly
function distributeAttributes(entityName, entityPos, attrs, positions) {
    const numAttrs = attrs.length;
    if (numAttrs === 0) return {};
    
    const attrPositions = {};
    const relDirections = getRelationshipDirections(entityName, positions);
    
    const numEntities = entities.length;

    const numRelations = relDirections.length; // ← TAMBAHAN: hitung jumlah relasi
    
    let baseRadius, clearance;
    if (numEntities >= 15) {
        baseRadius = 2.0;
        clearance = 40;
    } else if (numEntities >= 4) {
        baseRadius = 1.5;
        clearance = 35;
    } else {
        baseRadius = 1.5;
        clearance = 30;
    }
    
     // ========================================
    // ✨ ADAPTIVE CLEARANCE + RADIUS REDUCTION
    // ========================================
    let radiusMultiplier = 1.0; // Default: no reduction
    
    if (numRelations >= 2 && numAttrs >= 5) {
        // Entitas dengan 2+ relasi dan 5+ atribut
        clearance = Math.max(20, clearance * 0.6);
        console.log(`🎯 Light case for ${entityName}: clearance=${clearance}°, ${numRelations} relations, ${numAttrs} attrs`);
    }
    // ========================================
    
    const blockedRanges = [];
    relDirections.forEach(relDir => {
        const angle = ((relDir.angle % 360) + 360) % 360;
        const startBlock = ((angle - clearance) % 360 + 360) % 360;
        const endBlock = ((angle + clearance) % 360 + 360) % 360;
        blockedRanges.push({ start: startBlock, end: endBlock });
    });
    
    const candidateAngles = [];
    for (let angle = 0; angle < 360; angle += 10) {
        let isBlocked = false;
        for (const range of blockedRanges) {
            if (range.start <= range.end) {
                if (angle >= range.start && angle <= range.end) {
                    isBlocked = true;
                    break;
                }
            } else {
                if (angle >= range.start || angle <= range.end) {
                    isBlocked = true;
                    break;
                }
            }
        }
        if (!isBlocked) {
            candidateAngles.push(angle);
        }
    }
    
    const availableAngles = candidateAngles.length >= numAttrs 
        ? candidateAngles 
        : Array.from({ length: 36 }, (_, i) => i * 10);
    
    const selectedAngles = [];
    if (numAttrs <= availableAngles.length) {
        const step = availableAngles.length / numAttrs;
        for (let i = 0; i < numAttrs; i++) {
            selectedAngles.push(availableAngles[Math.floor(i * step)]);
        }
    } else {
        selectedAngles.push(...availableAngles);
        while (selectedAngles.length < numAttrs) {
            selectedAngles.push(90);
        }
    }
    
    attrs.forEach((attr, i) => {
        const angle = selectedAngles[i];
        const angleRad = (angle * Math.PI) / 180;
        
        // ========================================
        // ✨ ADAPTIVE RADIUS dengan multiplier
        // ========================================
        const radiusVariance = (i % 3) * 0.15 * radiusMultiplier;
        const radius = baseRadius * (1.0 + radiusVariance);
        // ========================================
        
        const attrX = entityPos.x + radius * Math.cos(angleRad);
        const attrY = entityPos.y + radius * Math.sin(angleRad);
        
        attrPositions[attr] = { x: attrX, y: attrY };
    });
    
    return attrPositions;
}

// Generate DOT notation
function generateDOT() {
    const erdName = document.getElementById('erdName').value.trim() || 'ERD';
    const numEntities = entities.length;
    
    let dot = 'digraph ERD {\n';
    dot += '  bgcolor="white";\n';
    dot += '  layout="neato";\n';
    
    if (numEntities <= 10) {
        dot += '  overlap="scalexy";\n';
        dot += '  sep="+0.2";\n';
    } else if (numEntities <= 15) {
        dot += '  overlap="scalexy";\n';
        dot += '  sep="+2.0";\n';
    } else if (numEntities >= 16) {
        dot += '  overlap="vpsc";\n';
        dot += '  sep="+2.5";\n';
    } else {
        dot += '  overlap="false";\n';
        dot += '  sep="+3.0";\n';
    }
    
    dot += '  splines="line";\n';
    dot += '  node [fontname="Arial"];\n';
    dot += '  edge [fontname="Arial"];\n\n';

    const positions = calculateEntityPositions();
    const usePinning = numEntities <= 7 || numEntities >= 8;
    
    entities.forEach((entity, idx) => {
        const entityName = entity.name.trim() || `Entitas_${idx + 1}`;
        const pos = positions[entityName];
        const posStr = usePinning ? `${pos.x},${pos.y}!` : `${pos.x},${pos.y}`;
        
        dot += `  "${entityName}" [\n`;
        dot += `    shape=box,\n`;
        dot += `    style=filled,\n`;
        dot += `    fillcolor="white",\n`;
        dot += `    fontcolor="black",\n`;
        dot += `    fontname="Arial Bold",\n`;
        dot += `    fontsize=11,\n`;
        dot += `    width=1.8,\n`;
        dot += `    height=0.7,\n`;
        dot += `    pos="${posStr}"\n`;
        dot += `  ];\n`;
        
        const attrPositions = distributeAttributes(
            entityName, 
            pos, 
            entity.attributes,
            positions
        );
        
        entity.attributes.forEach(attr => {
            const attrPos = attrPositions[attr];
            const attrId = `${entityName}_${attr}`.replace(/\s+/g, '_');
            const attrPosStr = usePinning 
                ? `${attrPos.x},${attrPos.y}!` 
                : `${attrPos.x},${attrPos.y}`;
            
            const isPK = attr === entity.primary_key;
            const fillcolor = 'white';
            const fontcolor = 'black';
            const fontname = isPK ? 'Arial Bold' : 'Arial';
            const label = isPK ? `<<U>${attr}</U>>` : attr;

            const numRelations = relationships.filter(r => 
                r.entity1 === entityName || r.entity2 === entityName
            ).length;
            
            let attrWidth = 1.2;
            let attrHeight = 0.5;
            let attrFontSize = 9;
            
            if (numRelations >= 3 && entity.attributes.length >= 8) {
                // Kasus ekstrem: atribut lebih kecil
                attrWidth = 0.85;
                attrHeight = 0.38;
                attrFontSize = 7.5;
            }  else if (numRelations >= 3 && entity.attributes.length >= 9) {
                // Extreme 9
                attrWidth = 0.80;
                attrHeight = 0.36;
                attrFontSize = 7.5;
            }else if (numRelations >= 3 && entity.attributes.length >= 6) {
                attrWidth = 1.2;
                attrHeight = 0.5;
                attrFontSize = 8;
            } else if (numRelations >= 2 && entity.attributes.length >= 10) {
                attrWidth = 0.90;
                attrHeight = 0.40;
                attrFontSize = 7.5;
            } else if (numRelations >= 2 && entity.attributes.length >= 8) {
                attrWidth = 1.0;
                attrHeight = 0.44;
                attrFontSize = 8;
            }
            
            dot += `  "${attrId}" [\n`;
            dot += `    shape=ellipse,\n`;
            dot += `    style=filled,\n`;
            dot += `    fillcolor="${fillcolor}",\n`;
            dot += `    fontcolor="${fontcolor}",\n`;
            dot += `    fontname="${fontname}",\n`;
            dot += `    fontsize=${attrFontSize},\n`;
            dot += `    width=${attrWidth},\n`;
            dot += `    height=${attrHeight},\n`;
            dot += `    label=${label},\n`;
            dot += `    pos="${attrPosStr}"\n`;
            dot += `  ];\n`;
            
            dot += `  "${attrId}" -> "${entityName}" [arrowhead=none, penwidth=0.5];\n`;
        });
        
        dot += '\n';
    });

    relationships.forEach((rel, i) => {
        if (!rel.entity1 || !rel.entity2) return;
        
        const e1Pos = positions[rel.entity1];
        const e2Pos = positions[rel.entity2];
        
        if (!e1Pos || !e2Pos) return;
        
        const relName = rel.relation.trim() || `Relasi_${i + 1}`;
        const relId = `rel_${i + 1}`;
        
        const relX = (e1Pos.x + e2Pos.x) / 2;
        const relY = (e1Pos.y + e2Pos.y) / 2;
        const relPosStr = usePinning ? `${relX},${relY}!` : `${relX},${relY}`;
        
        dot += `  "${relId}" [\n`;
        dot += `    shape=diamond,\n`;
        dot += `    style=filled,\n`;
        dot += `    fillcolor="white",\n`;
        dot += `    fontcolor="black",\n`;
        dot += `    fontname="Arial Bold",\n`;
        dot += `    fontsize=10,\n`;
        dot += `    label="${relName}",\n`;
        dot += `    width=1.4,\n`;
        dot += `    height=0.8,\n`;
        dot += `    pos="${relPosStr}"\n`;
        dot += `  ];\n`;
        
        // Render relationship attributes (for many-to-many)
        if (rel.type === 'many-to-many' && rel.attributes && rel.attributes.length > 0) {
            const relPos = { x: relX, y: relY };
            const relAttrPositions = distributeRelationshipAttributes(
                relId,
                relPos,
                rel.attributes,
                positions,
                rel.entity1,
                rel.entity2
            );
            
            rel.attributes.forEach(attr => {
                const attrPos = relAttrPositions[attr];
                const attrId = `${relId}_${attr}`.replace(/\s+/g, '_');
                const attrPosStr = usePinning 
                    ? `${attrPos.x},${attrPos.y}!` 
                    : `${attrPos.x},${attrPos.y}`;
                
                dot += `  "${attrId}" [\n`;
                dot += `    shape=ellipse,\n`;
                dot += `    style=filled,\n`;
                dot += `    fillcolor="white",\n`;
                dot += `    fontcolor="black",\n`;
                dot += `    fontname="Arial",\n`;
                dot += `    fontsize=9,\n`;
                dot += `    width=1.0,\n`;
                dot += `    height=0.45,\n`;
                dot += `    label="${attr}",\n`;
                dot += `    pos="${attrPosStr}"\n`;
                dot += `  ];\n`;
                
                dot += `  "${attrId}" -> "${relId}" [arrowhead=none, penwidth=0.5, style=dashed, color="#64748b"];\n`;
            });
        }
        
        const card = getCardinality(rel.type);
        
        dot += `  "${rel.entity1}" -> "${relId}" [\n`;
        dot += `    label="${card.entity1}",\n`;
        dot += `    arrowhead=none,\n`;
        dot += `    fontsize=10,\n`;
        dot += `    fontname="Arial Bold",\n`;
        dot += `    fontcolor="#2C3E50",\n`;
        dot += `    penwidth=1.5\n`;
        dot += `  ];\n`;
        
        dot += `  "${relId}" -> "${rel.entity2}" [\n`;
        dot += `    label="${card.entity2}",\n`;
        dot += `    arrowhead=none,\n`;
        dot += `    fontsize=10,\n`;
        dot += `    fontname="Arial Bold",\n`;
        dot += `    fontcolor="#2C3E50",\n`;
        dot += `    penwidth=1.5\n`;
        dot += `  ];\n\n`;
    });

    dot += '}\n';
    return dot;
}

function getCardinality(type) {
    const map = {
        'one-to-one': { entity1: '1', entity2: '1' },
        'one-to-many': { entity1: '1', entity2: 'N' },
        'many-to-one': { entity1: 'N', entity2: '1' },
        'many-to-many': { entity1: 'N', entity2: 'N' }
    };
    return map[type] || { entity1: '1', entity2: 'N' };
}

// Debounce function
let updateTimeout = null;
function debounceUpdate(func, delay = 500) {
    clearTimeout(updateTimeout);
    updateTimeout = setTimeout(func, delay);
}

// Update preview with @hpcc-js/wasm
async function updatePreview() {
    if (entities.length === 0) {
        document.getElementById('previewContainer').innerHTML = `
            <div class="empty-state">
                <h3>Preview akan muncul di sini</h3>
                <p>Tambahkan entitas untuk melihat preview</p>
            </div>
        `;
        return;
    }

    try {
        if (!graphviz) {
            console.log('Graphviz not initialized, initializing now...');
            const success = await initGraphviz();
            if (!success) {
                throw new Error('Failed to initialize Graphviz');
            }
        }

        const dot = generateDOT();
        console.log('Generated DOT:', dot);

        const svg = graphviz.dot(dot);
        
        const container = document.getElementById('previewContainer');
        const loadingOverlay = container.querySelector('.loading-overlay');
        container.innerHTML = '';
        
        if (loadingOverlay) {
            container.appendChild(loadingOverlay);
        }
        
        const svgWrapper = document.createElement('div');
        svgWrapper.className = 'svg-wrapper';
        svgWrapper.innerHTML = svg;

        container.appendChild(svgWrapper);

        if (loadingOverlay) {
            container.appendChild(loadingOverlay);
        }

        currentSVG = svgWrapper.querySelector('svg');
        
        // ============================================
        // 🔥 CRITICAL FIX: Jangan ubah style SVG!
        // ============================================
        if (currentSVG) {
            // HAPUS baris ini yang menyebabkan zoom out:
            // currentSVG.style.maxWidth = '100%';
            // currentSVG.style.height = 'auto';
            
            // GANTI dengan: Biarkan SVG menggunakan ukuran aslinya
            currentSVG.removeAttribute('style');
            
            // Optional: Tambahkan style yang tidak mengubah ukuran
            currentSVG.style.display = 'block';
        }
        // ============================================
        applyZoom();
        console.log('✅ Preview updated successfully');
    } catch (error) {
        console.error('❌ Error generating preview:', error);
        document.getElementById('previewContainer').innerHTML = `
            <div class="empty-state" style="color: #ef4444;">
                <h3>❌ Error</h3>
                <p>${error.message}</p>
                <p style="font-size: 12px; margin-top: 10px;">Check console for details</p>
            </div>
            <div class="loading-overlay" id="loadingOverlay">
                <div class="spinner"></div>
                <p style="margin-top: 15px; color: #3b82f6; font-weight: 600;">
                    Generating ERD...
                </p>
            </div>
        `;
    }
}

// Download SVG
function downloadSVG() {
    if (!currentSVG) {
        showErrorPopup('Silakan Isi ERD terlebih dahulu');
        return;
    }

    const erdName = document.getElementById('erdName').value.trim() || 'erd';
    const serializer = new XMLSerializer();
    const svgString = serializer.serializeToString(currentSVG);
    const blob = new Blob([svgString], { type: 'image/svg+xml' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${erdName}.svg`;
    a.click();
    URL.revokeObjectURL(url);
}

// Download PNG
function downloadPNG() {
    if (!currentSVG) {
        showErrorPopup('Silakan generate preview terlebih dahulu');
        return;
    }

    const erdName = document.getElementById('erdName').value.trim() || 'erd';
    const serializer = new XMLSerializer();
    const svgString = serializer.serializeToString(currentSVG);
    
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    const img = new Image();
    
    img.onload = function() {
        canvas.width = img.naturalWidth || 1200;
        canvas.height = img.naturalHeight || 800;
        
        ctx.fillStyle = 'white';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0);
        
        canvas.toBlob(function(blob) {
            if (!blob) {
                showErrorPopup('Failed to create PNG');
                return;
            }
            
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${erdName}.png`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }, 'image/png', 1.0);
    };
    
    img.onerror = function(error) {
        console.error('Image load error:', error);
        showErrorPopup('Failed to load SVG for PNG conversion');
    };
    
    const svgBlob = new Blob([svgString], { 
        type: 'image/svg+xml;charset=utf-8' 
    });
    img.src = URL.createObjectURL(svgBlob);
}

// Load ERD data for editing
async function loadERDForEdit(erdId) {
    try {
        console.log('Loading ERD for edit:', erdId);
        
        // Get token from localStorage (same as auth.js)
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('Token tidak ditemukan. Silakan login kembali.');
        }
        
        const response = await fetch(`/api/erd/${erdId}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            credentials: 'include'
        });
        
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ error: 'Server error' }));
            console.error('Error response:', errorData);
            throw new Error(errorData.error || `HTTP ${response.status}: Gagal memuat ERD`);
        }
        
        const result = await response.json();
        const erd = result.erd;
        
        console.log('ERD loaded successfully:', erd);
        
        // Reset state
        entities = [];
        relationships = [];
        entityCounter = 0;
        relationshipCounter = 0;
        
        // Set ERD name
        document.getElementById('erdName').value = erd.name;
        
        // Load entities
        erd.entities.forEach(entity => {
            addEntity();
            const currentEntityId = `entity_${entityCounter}`;
            const entityDiv = document.querySelector(`[data-entity-id="${currentEntityId}"]`);
            
            if (entityDiv) {
                entityDiv.querySelector('.entity-name').value = entity.name;
                entityDiv.querySelector('.entity-pk').value = entity.primary_key || '';
                
                // Update entity in array
                const lastEntityIndex = entities.length - 1;
                entities[lastEntityIndex].name = entity.name;
                entities[lastEntityIndex].primary_key = entity.primary_key || '';
                entities[lastEntityIndex].attributes = [];
                
                // Add attributes
                (entity.attributes || []).forEach(attr => {
                    if (!entities[lastEntityIndex].attributes.includes(attr)) {
                        entities[lastEntityIndex].attributes.push(attr);
                    }
                });
            }
        });
        
        // Render entities form to show attributes
        renderEntitiesForm();
        
        console.log('Entities loaded:', entities.length);
        
        // Wait for DOM update
        await new Promise(resolve => setTimeout(resolve, 100));
        
        // Load relationships directly to array
        erd.relationships.forEach(rel => {
            const relId = `relationship_${++relationshipCounter}`;
            relationships.push({
                id: relId,
                entity1: rel.entity1,
                entity2: rel.entity2,
                relation: rel.relation,
                type: rel.type,
                layout: rel.layout || 'LR',
                attributes: rel.attributes || [] // Load relationship attributes
            });
        });
        
        console.log('Relationships loaded:', relationships.length);
        
        // Render relationships form
        renderRelationshipsForm();
        
        // Wait a bit more for full render
        await new Promise(resolve => setTimeout(resolve, 200));
        
        // Update preview
        updatePreview();
        
        console.log('✅ ERD loaded successfully for editing');
        
    } catch (error) {
        console.error('❌ Error loading ERD:', error);
        showErrorPopup(`Error: ${error.message}`);
        window.location.href = '/advisor-dashboard';
    }
}

// Save ERD to backend
async function saveERD() {
    const erdName = document.getElementById('erdName').value.trim();
    
    if (!erdName) {
        showErrorPopup('Nama ERD harus diisi!');
        return;
    }

    if (entities.length === 0) {
        showErrorPopup('Minimal harus ada 1 entitas!');
        return;
    }

    const unnamedEntities = entities.filter(e => !e.name.trim());
    if (unnamedEntities.length > 0) {
        showErrorPopup('Semua entitas harus memiliki nama!');
        return;
    }

    const loadingOverlay = document.getElementById('loadingOverlay');
    loadingOverlay.classList.add('show');

    try {
        // Prepare ERD data
        const erdData = {
            name: erdName.toLowerCase().replace(/\s+/g, '_'),
            entities: entities.map(e => ({
                name: e.name,
                attributes: e.attributes,
                primary_key: e.primary_key || e.attributes[0] || ''
            })),
            relationships: relationships.map(r => ({
                entity1: r.entity1,
                entity2: r.entity2,
                relation: r.relation,
                type: r.type,
                layout: r.layout,
                attributes: r.attributes || [] // Include relationship attributes
            }))
        };

        console.log('Current mode:', currentMode);
        console.log('Saving ERD data:', erdData);

        // Get auth token
        const token = localStorage.getItem('token');
        if (!token) {
            showErrorPopup('❌ Token tidak ditemukan. Silakan login kembali.');
            window.location.href = '/login';
            return;
        }

        // Handle based on mode
        if (currentMode === 'edit' && editingErdId) {
            // MODE: EDIT - Update existing ERD
            const response = await fetch(`/api/erd/${editingErdId}`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify(erdData)
            });

            const result = await response.json();

            if (response.ok) {
                showSuccessPopup('✅ ERD berhasil diupdate!');
                console.log('Update successful:', result);
                
                // Redirect to advisor dashboard
                setTimeout(() => {
                    window.location.href = '/advisor-dashboard';
                }, 500);
            } else {
                showErrorPopup('❌ Error: ' + (result.error || 'Gagal mengupdate ERD'));
            }
            
        } else if (currentMode === 'from_request' && requestId) {
            // MODE: FROM_REQUEST - Create ERD from request
            erdData.mode = 'from_request';
            erdData.request_id = requestId;

            // Save ERD first
            const saveResponse = await fetch('/api/add-erd', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify(erdData)
            });

            if (!saveResponse.ok) {
                const errorData = await saveResponse.json();
                throw new Error(errorData.error || 'Gagal menyimpan ERD');
            }

            const saveData = await saveResponse.json();
            console.log('ERD saved:', saveData);

            // Complete the request
            const completeResponse = await fetch(`/api/requests/${requestId}/complete`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify({
                    erd_id: saveData.erd_id,
                    notes: ''
                })
            });

            if (completeResponse.ok) {
                showSuccessPopup('✅ ERD berhasil dibuat dan dikirim ke user!');
                console.log('Request completed successfully');
                
                // Redirect to advisor dashboard
                setTimeout(() => {
                    window.location.href = '/advisor-dashboard';
                }, 500);
            } else {
                const errorData = await completeResponse.json();
                showErrorPopup('❌ Error: ' + (errorData.error || 'Gagal menyelesaikan request'));
            }
            
        } else {
            // MODE: MANUAL - Direct ERD creation
            erdData.mode = 'manual';

            const response = await fetch('/api/add-erd', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify(erdData)
            });

            const result = await response.json();

            if (response.ok) {
                showSuccessPopup('✅ ERD berhasil dibuat!');
                console.log('Save successful:', result);
                
                // Redirect to advisor dashboard
                setTimeout(() => {
                    window.location.href = '/advisor-dashboard';
                }, 500);
            } else {
                showErrorPopup('❌ Error: ' + (result.error || 'Gagal menyimpan ERD'));
            }
        }
        
    } catch (error) {
        console.error('❌ Error saving ERD:', error);
        showErrorPopup('❌ Error: ' + error.message);
    } finally {
        loadingOverlay.classList.remove('show');
    }
}

// ========================================
// ZOOM FUNCTION
// ========================================

// Update zoom display
function updateZoomDisplay() {
    const zoomDisplay = document.getElementById('zoomLevel');
    if (zoomDisplay) {
        zoomDisplay.textContent = `${Math.round(currentZoom * 100)}%`;
    }
}

// Apply zoom transformation
function applyZoom() {
    const svgWrapper = document.querySelector('.preview-container .svg-wrapper');
    if (svgWrapper) {
        svgWrapper.style.transform = `scale(${currentZoom})`;
    }
    updateZoomDisplay();
}

// Zoom In function
function zoomIn() {
    if (currentZoom < MAX_ZOOM) {
        currentZoom = Math.min(currentZoom + ZOOM_STEP, MAX_ZOOM);
        applyZoom();
    }
}

// Zoom Out function
function zoomOut() {
    if (currentZoom > MIN_ZOOM) {
        currentZoom = Math.max(currentZoom - ZOOM_STEP, MIN_ZOOM);
        applyZoom();
    }
}

// Reset Zoom to 100%
function resetZoom() {
    currentZoom = 1.0;
    applyZoom();
}

// Setup zoom controls (panggil saat initialization)
function setupZoomControls() {
    const previewContainer = document.getElementById('previewContainer');
    if (previewContainer) {
        // Mouse wheel zoom support (Ctrl + Scroll)
        previewContainer.addEventListener('wheel', function(e) {
            // Only zoom if Ctrl key is pressed
            if (e.ctrlKey) {
                e.preventDefault();
                
                if (e.deltaY < 0) {
                    // Scroll up = Zoom in
                    zoomIn();
                } else {
                    // Scroll down = Zoom out
                    zoomOut();
                }
            }
        }, { passive: false });
    }
    
    // Initialize zoom display
    updateZoomDisplay();
}

// Reset form
function resetForm() {
    entities = [];
    relationships = [];
    entityCounter = 0;
    relationshipCounter = 0;
    currentSVG = null;
    
    document.getElementById('erdName').value = '';
    renderEntitiesForm();
    renderRelationshipsForm();
    
    document.getElementById('previewContainer').innerHTML = `
        <div class="empty-state">
            <h3>Preview akan muncul di sini</h3>
            <p>Tambahkan entitas dan klik "Update Preview"</p>
        </div>
    `;
    
    document.getElementById('successMessage').style.display = 'none';

    currentZoom = 1.0; // TAMBAHKAN INI
    updateZoomDisplay(); // TAMBAHKAN INI
}
