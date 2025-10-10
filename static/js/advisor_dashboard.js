// Advisor Dashboard JavaScript
let currentRequest = null;
let entities = [];
let relationships = [];
let entityCounter = 0;
let relationshipCounter = 0;

// Initialize advisor dashboard
function initAdvisorDashboard() {
    // Display advisor welcome message
    const user = getUser();
    document.getElementById('advisorWelcome').textContent = `Selamat datang, ${user.username}!`;
    
    // Initialize tab navigation
    initAdvisorTabNavigation();
    
    // Initialize modals
    initAdvisorModals();
    
    // Initialize ERD form
    initERDForm();
    
    // Load initial data
    loadPendingRequests();
}

// Tab navigation
function initAdvisorTabNavigation() {
    const menuItems = document.querySelectorAll('.menu-item');
    const tabContents = document.querySelectorAll('.tab-content');
    
    menuItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all items
            menuItems.forEach(i => i.classList.remove('active'));
            tabContents.forEach(t => t.classList.remove('active'));
            
            // Add active class to clicked item
            this.classList.add('active');
            
            // Show corresponding tab content
            const tabId = this.getAttribute('data-tab') + '-tab';
            document.getElementById(tabId).classList.add('active');
            
            // Load data based on tab
            if (tabId === 'pending-tab') {
                loadPendingRequests();
            } else if (tabId === 'assigned-tab') {
                loadAssignedRequests();
            } else if (tabId === 'history-tab') {
                loadAdvisorHistory();
            }
        });
    });
}

// Initialize modals
function initAdvisorModals() {
    // Request modal
    document.getElementById('closeRequestModal').addEventListener('click', closeRequestModal);
    
    // ERD creation modal
    document.getElementById('closeERDModal').addEventListener('click', closeERDCreationModal);
    
    // Assign request button
    document.getElementById('assignRequestBtn').addEventListener('click', handleAssignRequest);
    
    // Create ERD button
    document.getElementById('createERDBtn').addEventListener('click', openERDCreationModal);
    
    // Close modals when clicking outside
    window.addEventListener('click', function(event) {
        const requestModal = document.getElementById('requestModal');
        const erdModal = document.getElementById('erdCreationModal');
        
        if (event.target === requestModal) {
            requestModal.style.display = 'none';
        }
        if (event.target === erdModal) {
            erdModal.style.display = 'none';
        }
    });
}

// Load pending requests
async function loadPendingRequests() {
    const loadingEl = document.getElementById('pendingLoading');
    const listEl = document.getElementById('pendingList');
    
    loadingEl.style.display = 'block';
    listEl.innerHTML = '';
    
    try {
        const response = await apiCall('/api/requests/pending');
        const data = await response.json();
        
        if (response.ok) {
            renderPendingRequests(data.requests);
        } else {
            listEl.innerHTML = `<div class="error-message">Gagal memuat requests: ${data.error}</div>`;
        }
    } catch (error) {
        listEl.innerHTML = '<div class="error-message">Gagal memuat requests</div>';
        console.error('Error:', error);
    } finally {
        loadingEl.style.display = 'none';
    }
}

function renderPendingRequests(requests) {
    const listEl = document.getElementById('pendingList');
    
    if (requests.length === 0) {
        listEl.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📋</div>
                <h3>Tidak ada request pending</h3>
                <p>Semua request telah diambil atau belum ada request baru dari user</p>
            </div>
        `;
        return;
    }
    
    requests.forEach(request => {
        const item = document.createElement('div');
        item.className = 'request-item';
        
        const createdDate = new Date(request.created_at).toLocaleDateString('id-ID');
        
        item.innerHTML = `
            <div class="request-header">
                <div class="request-info">
                    <div class="user-info">👤 ${request.user.username} (${request.user.email})</div>
                    <div class="request-query">${request.query}</div>
                    <div class="request-description">${request.description}</div>
                </div>
                <div class="request-actions">
                    <button class="btn-action btn-view" onclick="viewRequestDetails('${request.request_id}', 'pending')">
                        Detail
                    </button>
                    <button class="btn-action btn-assign" onclick="assignRequestFromList('${request.request_id}')">
                        Ambil Request
                    </button>
                </div>
            </div>
            <div class="request-meta">
                <span>📅 Dibuat: ${createdDate}</span>
                <div class="status-indicator pending">
                    <span class="status-dot pending"></span>
                    ${request.status_display}
                </div>
            </div>
        `;
        
        listEl.appendChild(item);
    });
}

// Load assigned requests
async function loadAssignedRequests() {
    const loadingEl = document.getElementById('assignedLoading');
    const listEl = document.getElementById('assignedList');
    
    loadingEl.style.display = 'block';
    listEl.innerHTML = '';
    
    try {
        const response = await apiCall('/api/requests/my-assigned');
        const data = await response.json();
        
        if (response.ok) {
            renderAssignedRequests(data.requests);
        } else {
            listEl.innerHTML = `<div class="error-message">Gagal memuat requests: ${data.error}</div>`;
        }
    } catch (error) {
        listEl.innerHTML = '<div class="error-message">Gagal memuat requests</div>';
        console.error('Error:', error);
    } finally {
        loadingEl.style.display = 'none';
    }
}

function renderAssignedRequests(requests) {
    const listEl = document.getElementById('assignedList');
    
    if (requests.length === 0) {
        listEl.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">⚙️</div>
                <h3>Tidak ada request yang dikerjakan</h3>
                <p>Ambil request dari tab "Request Pending" untuk mulai bekerja</p>
            </div>
        `;
        return;
    }
    
    requests.forEach(request => {
        const item = document.createElement('div');
        item.className = 'request-item';
        
        const updatedDate = new Date(request.updated_at).toLocaleDateString('id-ID');
        const statusClass = request.status.replace('_', '');
        
        item.innerHTML = `
            <div class="request-header">
                <div class="request-info">
                    <div class="user-info">👤 ${request.user.username} (${request.user.email})</div>
                    <div class="request-query">${request.query}</div>
                    <div class="request-description">${request.description}</div>
                </div>
                <div class="request-actions">
                    <button class="btn-action btn-view" onclick="viewRequestDetails('${request.request_id}', '${request.status}')">
                        Detail
                    </button>
                    ${request.status === 'on_process' ? 
                        `<button class="btn-action btn-create-erd" onclick="startERDCreation('${request.request_id}')">
                            Buat ERD
                        </button>` : 
                        ''
                    }
                </div>
            </div>
            <div class="request-meta">
                <span>📅 Update: ${updatedDate}</span>
                <div class="status-indicator ${statusClass}">
                    <span class="status-dot ${statusClass}"></span>
                    ${request.status_display}
                </div>
            </div>
        `;
        
        listEl.appendChild(item);
    });
}

// Request detail functions
async function viewRequestDetails(requestId, status) {
    try {
        // For now, we'll get the request from the current lists
        // In a real app, you might want a separate API call
        showRequestModal(requestId, status);
    } catch (error) {
        alert('Gagal memuat detail request');
        console.error('Error:', error);
    }
}

function showRequestModal(requestId, status) {
    currentRequest = { request_id: requestId, status: status };
    
    const modal = document.getElementById('requestModal');
    const assignBtn = document.getElementById('assignRequestBtn');
    const createBtn = document.getElementById('createERDBtn');
    
    // Show appropriate buttons based on status
    if (status === 'pending') {
        assignBtn.style.display = 'block';
        createBtn.style.display = 'none';
    } else if (status === 'on_process') {
        assignBtn.style.display = 'none';
        createBtn.style.display = 'block';
    } else {
        assignBtn.style.display = 'none';
        createBtn.style.display = 'none';
    }
    
    modal.style.display = 'block';
}

function closeRequestModal() {
    document.getElementById('requestModal').style.display = 'none';
    currentRequest = null;
}

// Assign request functions
async function assignRequestFromList(requestId) {
    if (!confirm('Yakin ingin mengambil request ini?')) return;
    
    try {
        const response = await apiCall(`/api/requests/${requestId}/assign`, {
            method: 'PUT'
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert('Request berhasil diambil!');
            loadPendingRequests();
            // Switch to assigned tab
            document.querySelector('[data-tab="assigned"]').click();
        } else {
            alert(data.error || 'Gagal mengambil request');
        }
    } catch (error) {
        alert('Gagal mengambil request');
        console.error('Error:', error);
    }
}

async function handleAssignRequest() {
    if (!currentRequest) return;
    
    await assignRequestFromList(currentRequest.request_id);
    closeRequestModal();
}

// ERD Creation functions
function startERDCreation(requestId) {
    currentRequest = { request_id: requestId };
    openERDCreationModal();
}

function openERDCreationModal() {
    if (!currentRequest) {
        alert('Pilih request terlebih dahulu');
        return;
    }
    
    // Reset form
    resetERDForm();
    
    const modal = document.getElementById('erdCreationModal');
    modal.style.display = 'block';
}

function closeERDCreationModal() {
    document.getElementById('erdCreationModal').style.display = 'none';
    resetERDForm();
}

// ERD Form Management
function initERDForm() {
    document.getElementById('addEntityBtn').addEventListener('click', addEntity);
    document.getElementById('addRelationshipBtn').addEventListener('click', addRelationship);
    document.getElementById('erdForm').addEventListener('submit', handleERDSubmission);
}

function resetERDForm() {
    entities = [];
    relationships = [];
    entityCounter = 0;
    relationshipCounter = 0;
    
    document.getElementById('erdName').value = '';
    document.getElementById('erdNotes').value = '';
    document.getElementById('entitiesContainer').innerHTML = '';
    document.getElementById('relationshipsContainer').innerHTML = '';
}

function addEntity() {
    const container = document.getElementById('entitiesContainer');
    const entityId = `entity_${++entityCounter}`;
    
    const entityDiv = document.createElement('div');
    entityDiv.className = 'entity-item';
    entityDiv.setAttribute('data-entity-id', entityId);
    
    entityDiv.innerHTML = `
        <div class="entity-header">
            <div class="entity-title">Entitas ${entityCounter}</div>
            <button type="button" class="remove-entity" onclick="removeEntity('${entityId}')">Hapus</button>
        </div>
        <div class="entity-form">
            <div class="form-group">
                <label>Nama Entitas:</label>
                <input type="text" class="entity-name" required placeholder="Nama entitas">
            </div>
            <div class="form-group">
                <label>Primary Key:</label>
                <input type="text" class="entity-pk" placeholder="Primary key (opsional)">
            </div>
        </div>
        <div class="attributes-section">
            <label>Atribut:</label>
            <div class="attributes-list" id="attributes_${entityId}"></div>
            <div class="add-attribute">
                <input type="text" placeholder="Nama atribut" class="new-attribute">
                <button type="button" onclick="addAttribute('${entityId}')">Tambah</button>
            </div>
        </div>
    `;
    
    container.appendChild(entityDiv);
    
    // Add entity to array
    entities.push({
        id: entityId,
        name: '',
        attributes: [],
        primary_key: ''
    });
}

function removeEntity(entityId) {
    const entityDiv = document.querySelector(`[data-entity-id="${entityId}"]`);
    if (entityDiv) {
        entityDiv.remove();
    }
    
    // Remove from array
    entities = entities.filter(e => e.id !== entityId);
    
    // Update relationship options
    updateRelationshipOptions();
}

function addAttribute(entityId) {
    const input = document.querySelector(`[data-entity-id="${entityId}"] .new-attribute`);
    const attributeName = input.value.trim();
    
    if (!attributeName) return;
    
    const attributesList = document.getElementById(`attributes_${entityId}`);
    
    const attributeSpan = document.createElement('span');
    attributeSpan.className = 'attribute-item';
    attributeSpan.innerHTML = `
        ${attributeName}
        <button type="button" class="remove-attribute" onclick="removeAttribute(this, '${entityId}', '${attributeName}')">&times;</button>
    `;
    
    attributesList.appendChild(attributeSpan);
    
    // Add to entity data
    const entity = entities.find(e => e.id === entityId);
    if (entity) {
        entity.attributes.push(attributeName);
    }
    
    input.value = '';
}

function removeAttribute(button, entityId, attributeName) {
    button.parentElement.remove();
    
    // Remove from entity data
    const entity = entities.find(e => e.id === entityId);
    if (entity) {
        entity.attributes = entity.attributes.filter(a => a !== attributeName);
    }
}

function addRelationship() {
    const container = document.getElementById('relationshipsContainer');
    const relationshipId = `relationship_${++relationshipCounter}`;
    
    const relationshipDiv = document.createElement('div');
    relationshipDiv.className = 'relationship-item';
    relationshipDiv.setAttribute('data-relationship-id', relationshipId);
    
    relationshipDiv.innerHTML = `
        <div class="relationship-header">
            <div class="relationship-title">Relasi ${relationshipCounter}</div>
            <button type="button" class="remove-relationship" onclick="removeRelationship('${relationshipId}')">Hapus</button>
        </div>
        <div class="relationship-form">
            <div class="form-group">
                <label>Entitas 1:</label>
                <select class="relationship-entity1" required>
                    <option value="">Pilih entitas</option>
                </select>
            </div>
            <div class="form-group">
                <label>Entitas 2:</label>
                <select class="relationship-entity2" required>
                    <option value="">Pilih entitas</option>
                </select>
            </div>
            <div class="form-group">
                <label>Nama Relasi:</label>
                <input type="text" class="relationship-name" required placeholder="Nama relasi">
            </div>
            <div class="form-group">
                <label>Kardinalitas:</label>
                <select class="relationship-type" required>
                    <option value="">Pilih kardinalitas</option>
                    <option value="one-to-one">One to One</option>
                    <option value="one-to-many">One to Many</option>
                    <option value="many-to-one">Many to One</option>
                    <option value="many-to-many">Many to Many</option>
                </select>
            </div>
        </div>
    `;
    
    container.appendChild(relationshipDiv);
    
    // Add relationship to array
    relationships.push({
        id: relationshipId,
        entity1: '',
        entity2: '',
        relation: '',
        type: ''
    });
    
    // Update entity options
    updateRelationshipOptions();
}

function removeRelationship(relationshipId) {
    const relationshipDiv = document.querySelector(`[data-relationship-id="${relationshipId}"]`);
    if (relationshipDiv) {
        relationshipDiv.remove();
    }
    
    // Remove from array
    relationships = relationships.filter(r => r.id !== relationshipId);
}

function updateRelationshipOptions() {
    const selects = document.querySelectorAll('.relationship-entity1, .relationship-entity2');
    
    selects.forEach(select => {
        const currentValue = select.value;
        select.innerHTML = '<option value="">Pilih entitas</option>';
        
        // Get current entity names
        entities.forEach(entity => {
            const entityNameInput = document.querySelector(`[data-entity-id="${entity.id}"] .entity-name`);
            const entityName = entityNameInput ? entityNameInput.value.trim() : '';
            
            if (entityName) {
                const option = document.createElement('option');
                option.value = entityName;
                option.textContent = entityName;
                if (entityName === currentValue) {
                    option.selected = true;
                }
                select.appendChild(option);
            }
        });
    });
}

// Form submission
async function handleERDSubmission(event) {
    event.preventDefault();
    
    if (!currentRequest) {
        alert('Tidak ada request yang dipilih');
        return;
    }
    
    // Collect form data
    const erdName = document.getElementById('erdName').value.trim();
    const erdNotes = document.getElementById('erdNotes').value.trim();
    
    if (!erdName) {
        alert('Nama ERD harus diisi');
        return;
    }
    
    // Collect entities data
    const entitiesData = [];
    entities.forEach(entity => {
        const entityDiv = document.querySelector(`[data-entity-id="${entity.id}"]`);
        const nameInput = entityDiv.querySelector('.entity-name');
        const pkInput = entityDiv.querySelector('.entity-pk');
        
        const entityName = nameInput.value.trim();
        if (entityName) {
            entitiesData.push({
                name: entityName,
                attributes: entity.attributes,
                primary_key: pkInput.value.trim() || entity.attributes[0] || ''
            });
        }
    });
    
    // Collect relationships data
    const relationshipsData = [];
    relationships.forEach(relationship => {
        const relationshipDiv = document.querySelector(`[data-relationship-id="${relationship.id}"]`);
        const entity1Select = relationshipDiv.querySelector('.relationship-entity1');
        const entity2Select = relationshipDiv.querySelector('.relationship-entity2');
        const nameInput = relationshipDiv.querySelector('.relationship-name');
        const typeSelect = relationshipDiv.querySelector('.relationship-type');
        
        const entity1 = entity1Select.value;
        const entity2 = entity2Select.value;
        const relationName = nameInput.value.trim();
        const relationType = typeSelect.value;
        
        if (entity1 && entity2 && relationName && relationType) {
            relationshipsData.push({
                entity1: entity1,
                entity2: entity2,
                relation: relationName,
                type: relationType
            });
        }
    });
    
    if (entitiesData.length === 0) {
        alert('Minimal harus ada satu entitas');
        return;
    }
    
    // Create ERD data
    const erdData = {
        name: erdName.toLowerCase().replace(/\s+/g, '_'),
        entities: entitiesData,
        relationships: relationshipsData
    };
    
    try {
        // Save ERD to database first
        const saveResponse = await apiCall('/api/add-erd', {
            method: 'POST',
            body: JSON.stringify(erdData)
        });
        
        if (!saveResponse.ok) {
            const errorData = await saveResponse.json();
            throw new Error(errorData.error || 'Gagal menyimpan ERD');
        }
        
        // Complete the request
        const completeResponse = await apiCall(`/api/requests/${currentRequest.request_id}/complete`, {
            method: 'PUT',
            body: JSON.stringify({
                erd_result: erdData,
                notes: erdNotes
            })
        });
        
        if (completeResponse.ok) {
            alert('ERD berhasil dibuat dan dikirim ke user!');
            closeERDCreationModal();
            // Switch to assigned tab to see updated status
            document.querySelector('[data-tab="assigned"]').click();
        } else {
            const errorData = await completeResponse.json();
            alert(errorData.error || 'Gagal menyelesaikan request');
        }
        
    } catch (error) {
        alert(`Gagal membuat ERD: ${error.message}`);
        console.error('Error:', error);
    }
}

// Load advisor history
async function loadAdvisorHistory() {
    const loadingEl = document.getElementById('advisorHistoryLoading');
    const listEl = document.getElementById('advisorHistoryList');
    
    loadingEl.style.display = 'block';
    listEl.innerHTML = '';
    
    try {
        const response = await apiCall('/api/requests/my-assigned');
        const data = await response.json();
        
        if (response.ok) {
            const completedRequests = data.requests.filter(req => req.status === 'complete');
            renderAdvisorHistory(completedRequests);
        } else {
            listEl.innerHTML = `<div class="error-message">Gagal memuat riwayat: ${data.error}</div>`;
        }
    } catch (error) {
        listEl.innerHTML = '<div class="error-message">Gagal memuat riwayat</div>';
        console.error('Error:', error);
    } finally {
        loadingEl.style.display = 'none';
    }
}

function renderAdvisorHistory(history) {
    const listEl = document.getElementById('advisorHistoryList');
    
    if (history.length === 0) {
        listEl.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📚</div>
                <h3>Belum ada riwayat ERD</h3>
                <p>ERD yang telah Anda selesaikan akan muncul di sini</p>
            </div>
        `;
        return;
    }
    
    history.forEach(item => {
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';
        
        const completedDate = new Date(item.completed_at).toLocaleDateString('id-ID');
        
        historyItem.innerHTML = `
            <div class="item-header">
                <div class="item-title">${item.query}</div>
                <div class="status-badge complete">${item.status_display}</div>
            </div>
            <div class="item-description">${item.description}</div>
            <div class="user-info">👤 User: ${item.user.username}</div>
            <div class="item-meta">
                <span>✅ Selesai: ${completedDate}</span>
                ${item.notes ? `<span>📝 ${item.notes}</span>` : ''}
            </div>
        `;
        
        listEl.appendChild(historyItem);
    });
}

// Update entity options when entity names change
document.addEventListener('input', function(e) {
    if (e.target.classList.contains('entity-name')) {
        updateRelationshipOptions();
    }
});