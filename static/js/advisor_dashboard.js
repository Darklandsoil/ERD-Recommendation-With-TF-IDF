// Advisor Dashboard JavaScript
let currentRequest = null;
let entities = [];
let relationships = [];
let entityCounter = 0;
let relationshipCounter = 0;

// Initialize advisor dashboard
// Initialize advisor dashboard
function initAdvisorDashboard() {
    // Display advisor welcome message
    const user = getUser();
    document.getElementById('advisorWelcome').textContent = `Selamat datang, ${user.fullname}!`;
    
    // Initialize tab navigation FIRST
    initAdvisorTabNavigation();
    
    // Initialize modals
    initAdvisorModals();
    
    // DON'T load data here - let tab switching handle it
    // Remove: loadPendingRequests();
    
    // Load data based on current active tab
    loadDataForActiveTab();
}

// Make closeRequestModal available globally for inline onclick
window.closeRequestModal = function() {
    const modal = document.getElementById('requestModal');
    if (modal) {
        modal.style.display = 'none';
    }
    currentRequest = null;
};

// NEW FUNCTION: Load data based on active tab
function loadDataForActiveTab() {
    const activeTab = document.querySelector('.tab-content.active');
    if (!activeTab) return;
    
    const tabId = activeTab.id;
    
    console.log('Loading data for tab:', tabId);
    
    switch(tabId) {
        case 'pending-tab':
            loadPendingRequests();
            break;
        case 'assigned-tab':
            loadAssignedRequests();
            break;
        case 'create-tab':
            loadMyERDs();
            break;
        case 'history-tab':
            loadAdvisorHistory();
            break;
    }
}



// PERBAIKI Tab navigation - Remove duplicate handlers
function initAdvisorTabNavigation() {
    const menuItems = document.querySelectorAll('.menu-item');
    const tabContents = document.querySelectorAll('.tab-content');
    
    menuItems.forEach(item => {
        // Remove inline onclick, use ONLY event listener
        item.removeAttribute('onclick');
        
        item.addEventListener('click', function(e) {
            e.preventDefault();
            
            const tabName = this.getAttribute('data-tab');
            switchTabProgrammatically(tabName);
        });
    });
}

// NEW: Centralized tab switching function
function switchTabProgrammatically(tabName) {
    console.log('Switching to tab:', tabName);
    
    const menuItems = document.querySelectorAll('.menu-item');
    const tabContents = document.querySelectorAll('.tab-content');
    
    // Remove active class from all
    menuItems.forEach(i => i.classList.remove('active'));
    tabContents.forEach(t => t.classList.remove('active'));
    
    // Add active class to selected
    const selectedMenuItem = document.querySelector(`[data-tab="${tabName}"]`);
    const selectedTab = document.getElementById(tabName + '-tab');
    
    if (selectedMenuItem) selectedMenuItem.classList.add('active');
    if (selectedTab) selectedTab.classList.add('active');
    
    // Update URL hash
    history.pushState(null, null, '#' + tabName);
    
    // Load data for this tab
    switch(tabName) {
        case 'pending':
            loadPendingRequests();
            break;
        case 'assigned':
            loadAssignedRequests();
            break;
        case 'create':
            loadMyERDs();
            break;
        case 'history':
            loadAdvisorHistory();
            break;
    }
}

// Initialize modals
function initAdvisorModals() {
    // Request modal close button
    const closeRequestModalBtn = document.getElementById('closeRequestModal');
    if (closeRequestModalBtn) {
        closeRequestModalBtn.addEventListener('click', closeRequestModal);
    }
    
    // Assign request button
    const assignRequestBtn = document.getElementById('assignRequestBtn');
    if (assignRequestBtn) {
        assignRequestBtn.addEventListener('click', handleAssignRequest);
    }
    
    // Create ERD button (redirects to erd-builder)
    const createERDBtn = document.getElementById('createERDBtn');
    if (createERDBtn) {
        createERDBtn.addEventListener('click', function() {
            if (currentRequest) {
                startERDCreation(currentRequest.request_id);
            }
        });
    }
    
    // Close modals when clicking outside
    const requestModal = document.getElementById('requestModal');
    if (requestModal) {
        requestModal.addEventListener('click', function(event) {
            if (event.target === requestModal) {
                closeRequestModal();
            }
        });
    }
}

// Load pending requests
async function loadPendingRequests() {
    const listEl = document.getElementById('pendingList');
    
    listEl.innerHTML = '';
    
    try {
        const response = await apiCall('/api/requests/pending');
        console.log('📡 API Response status:', response.status);
        
        const data = await response.json();
        console.log('📦 API Data:', data);
        
        if (response.ok) {
            console.log(`✅ Rendering ${data.requests.length} pending requests`);
            renderPendingRequests(data.requests);
        } else {
            console.error('❌ API Error:', data.error);
            listEl.innerHTML = `<div class="error-message">Gagal memuat requests: ${data.error}</div>`;
        }
    } catch (error) {
        console.error('❌ Exception:', error);
        listEl.innerHTML = '<div class="error-message">Gagal memuat requests</div>';
    }
}

function renderPendingRequests(requests) {
    const listEl = document.getElementById('pendingList');
    
    if (requests.length === 0) {
        listEl.innerHTML = `
            <div class="empty-state">
                <i class='bx bx-inbox'></i>
                <h3>Tidak Ada Request Pending</h3>
                <p>Belum ada request baru dari user saat ini</p>
            </div>
        `;
        return;
    }
    
    requests.forEach(request => {
        const item = document.createElement('div');
        item.className = 'request-item';
        
        const createdDate = new Date(request.created_at).toLocaleDateString('id-ID');
        
        // Get first letter for avatar
        const avatarLetter = request.user.username.charAt(0).toUpperCase();
        
        item.innerHTML = `
            <div class="request-header">
                <div class="user-avatar">${avatarLetter}</div>
                <div class="request-header-content">
                    <div class="request-title-row">
                        <h3 class="request-title">${request.query}</h3>
                        <span class="status-badge pending">
                            <span class="status-dot"></span>
                            ${request.status_display}
                        </span>
                    </div>
                    <div class="user-info">
                        <i class='bx bx-user'></i>
                        <span><strong>${request.user.username}</strong> (${request.user.email})</span>
                    </div>
                </div>
            </div>

            <div class="request-body">
                <p class="request-description">
                    ${request.description}
                </p>
            </div>

            <div class="request-footer">
                <div class="request-meta">
                    <div class="meta-item">
                        <i class='bx bx-calendar'></i>
                        <span>Dibuat: ${createdDate}</span>
                    </div>
                </div>
                <div class="request-actions">
                    <button class="btn btn-action" onclick="assignRequestFromList('${request.request_id}')">
                        <i class='bx bx-bookmark'></i>
                        Ambil Request
                    </button>
                </div>
            </div>
        `;
        
        listEl.appendChild(item);
    });
}

// Load assigned requests
async function loadAssignedRequests() {
    const listEl = document.getElementById('assignedList');
    
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
    } 
}

function renderAssignedRequests(requests) {
    const listEl = document.getElementById('assignedList');
    
    if (requests.length === 0) {
        listEl.innerHTML = `
            <div class="empty-state">
                <i class='bx bx-time'></i>
                <h3>Tidak Ada Request Dikerjakan</h3>
                <p>Ambil request dari tab "Request Pending" untuk mulai bekerja</p>
            </div>
        `;
        return;
    }
    
    requests.forEach(request => {
        const item = document.createElement('div');
        item.className = 'request-item';
        
        const updatedDate = new Date(request.updated_at).toLocaleDateString('id-ID');
        const statusClass = request.status === 'on_process' ? 'assigned' : 'completed';
        
        // Get first letter for avatar
        const avatarLetter = request.user.username.charAt(0).toUpperCase();
        
        item.innerHTML = `
            <div class="request-header">
                <div class="user-avatar">${avatarLetter}</div>
                <div class="request-header-content">
                    <div class="request-title-row">
                        <h3 class="request-title">${request.query}</h3>
                        <span class="status-badge ${statusClass}">
                            <span class="status-dot"></span>
                            ${request.status_display}
                        </span>
                    </div>
                    <div class="user-info">
                        <i class='bx bx-user'></i>
                        <span><strong>${request.user.username}</strong> (${request.user.email})</span>
                    </div>
                </div>
            </div>

            <div class="request-body">
                <p class="request-description">
                    ${request.description}
                </p>
            </div>

            <div class="request-footer">
                <div class="request-meta">
                    <div class="meta-item">
                        <i class='bx bx-calendar'></i>
                        <span>Update: ${updatedDate}</span>
                    </div>
                </div>
                <div class="request-actions">
                    ${request.status === 'on_process' ? 
                        `<button class="btn btn-action" onclick="startERDCreation('${request.request_id}')">
                            <i class='bx bx-plus-circle'></i>
                            Buat ERD
                        </button>` : 
                        ''
                    }
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
        showErrorPopup('Gagal memuat detail request');
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
    showWarningPopup(
        'Konfirmasi',
        'Yakin ingin mengambil request ini?',
        async (confirmed) => {
            if (!confirmed) return;
            
            try {
                const response = await apiCall(`/api/requests/${requestId}/assign`, {
                    method: 'PUT'
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    showSuccessPopup('Berhasil!', 'Request berhasil diambil!');
                    loadPendingRequests();
                    document.querySelector('[data-tab="assigned"]').click();
                } else {
                    showErrorPopup('Gagal!', data.error || 'Gagal mengambil request');
                }
            } catch (error) {
                showErrorPopup('Gagal!', 'Gagal mengambil request');
                console.error('Error:', error);
            }
        }
    );
}

async function handleAssignRequest() {
    if (!currentRequest) return;
    
    await assignRequestFromList(currentRequest.request_id);
    closeRequestModal();
}

// ERD Creation functions - Redirect to erd-builder.html
function startERDCreation(requestId) {
    // Redirect to erd-builder with from_request mode
    window.location.href = `/erd-builder?mode=from_request&request_id=${requestId}`;
}

// ERD Form Management - Not needed anymore (using erd-builder.html)

// Load advisor history
async function loadAdvisorHistory() {
    const loadingEl = document.getElementById('advisorHistoryLoading');
    const listEl = document.getElementById('advisorHistoryList');
    
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


// PERBAIKAN addAttribute
function addAttribute(entityId) {
    const input = document.querySelector(`[data-entity-id="${entityId}"] .new-attribute`);
    const attributeName = input.value.trim();
    
    if (!attributeName) return;
    
    const attributesList = document.getElementById(`attributes_${entityId}`);
    
    const attributeSpan = document.createElement('span');
    attributeSpan.className = 'attribute-item';
    attributeSpan.innerHTML = `
        ${attributeName}
        <button type="button" class="remove-attribute">&times;</button>
    `;
    
    attributesList.appendChild(attributeSpan);
    
    // Tambahkan event listener untuk button remove
    const removeBtn = attributeSpan.querySelector('.remove-attribute');
    removeBtn.addEventListener('click', function(e) {
        e.preventDefault();
        
        attributeSpan.remove();
        
        // Remove dari entity data
        const entity = entities.find(e => e.id === entityId);
        if (entity) {
            entity.attributes = entity.attributes.filter(a => a !== attributeName);
        }
    });
    
    // Add ke entity data
    const entity = entities.find(e => e.id === entityId);
    if (entity) {
        entity.attributes.push(attributeName);
    }
    
    input.value = '';
}


// PERBAIKAN RemoveAttribute
function removeAttribute(button, entityId, attributeName) {
    // Gunakan parentElement untuk mencari span yang berisi button
    const attributeSpan = button.closest('.attribute-item');
    
    if (attributeSpan) {
        attributeSpan.remove();
        
        // Remove dari entity data
        const entity = entities.find(e => e.id === entityId);
        if (entity) {
            entity.attributes = entity.attributes.filter(a => a !== attributeName);
        }
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
            <div class="form-group">
                <label>layout:</label>
                <select class="relationship-layout" required="">
                    <option value="">Pilih Layout</option>
                    <option value="RL">Right To Left</option>
                    <option value="LR">Left To Right</option>
                    <option value="TB">Top To Bottom</option>
                    <option value="BT">Bottom To Top</option>
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
        type: '',
        layout: ''
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
    
    // Collect form data
    const erdName = document.getElementById('erdName').value.trim();
    const erdNotes = document.getElementById('erdNotes').value.trim();
    
    if (!erdName) {
        showErrorPopup('Nama ERD harus diisi');
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
        const layoutSelect = relationshipDiv.querySelector('.relationship-layout')
        
        const entity1 = entity1Select.value;
        const entity2 = entity2Select.value;
        const relationName = nameInput.value.trim();
        const relationType = typeSelect.value;
        const relationLayout = layoutSelect.value;
        
        if (entity1 && entity2 && relationName && relationType && relationLayout) {
            relationshipsData.push({
                entity1: entity1,
                entity2: entity2,
                relation: relationName,
                type: relationType,
                layout: relationLayout
            });
        }
    });
    
    if (entitiesData.length === 0) {
        showErrorPopup('Minimal harus ada satu entitas');
        return;
    }
    
    // Create ERD data
    const erdData = {
        name: erdName.toLowerCase().replace(/\s+/g, '_'),
        entities: entitiesData,
        relationships: relationshipsData
    };
    
    try {
        // Check if this is an edit operation
        if (editingErdId) {
            await updateERD(editingErdId, erdData);
            return;
        }
        
        // Check if this is manual ERD creation or from request
        if (currentRequest) {
            // Mode: from_request - Include request_id
            erdData.mode = 'from_request';
            erdData.request_id = currentRequest.request_id;
            
            // Save ERD to database first
            const saveResponse = await apiCall('/api/add-erd', {
                method: 'POST',
                body: JSON.stringify(erdData)
            });
            
            if (!saveResponse.ok) {
                const errorData = await saveResponse.json();
                throw new Error(errorData.error || 'Gagal menyimpan ERD');
            }
            
            const saveData = await saveResponse.json();
            
            // Complete the request with ERD ID
            const completeResponse = await apiCall(`/api/requests/${currentRequest.request_id}/complete`, {
                method: 'PUT',
                body: JSON.stringify({
                    erd_id: saveData.erd_id,
                    notes: erdNotes
                })
            });
            
            if (completeResponse.ok) {
                showSuccessPopup('ERD berhasil dibuat dan dikirim ke user!');
                closeERDCreationModal();
                // Switch to assigned tab to see updated status
                document.querySelector('[data-tab="assigned"]').click();
            } else {
                const errorData = await completeResponse.json();
                showErrorPopup(errorData.error || 'Gagal menyelesaikan request');
            }
        } else {
            // Mode: manual - Direct ERD creation without request
            erdData.mode = 'manual';
            
            const saveResponse = await apiCall('/api/add-erd', {
                method: 'POST',
                body: JSON.stringify(erdData)
            });
            
            if (!saveResponse.ok) {
                const errorData = await saveResponse.json();
                throw new Error(errorData.error || 'Gagal menyimpan ERD');
            }
            
            showSuccessPopup('ERD manual berhasil dibuat!');
            closeERDCreationModal();
            // Reload ERD list in create tab
            loadMyERDs();
        }
        
    } catch (error) {
        showErrorPopup(`Gagal membuat ERD: ${error.message}`);
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


// ==========================================
// DIRECT ERD CREATION FUNCTIONS
// ==========================================

// Load advisor's own ERDs
async function loadMyERDs() {
    const listEl = document.getElementById('myERDsList');
    
    listEl.innerHTML = '';
    
    try {
        const response = await apiCall('/api/advisor-erds');
        const data = await response.json();
        
        if (response.ok) {
            renderMyERDs(data.erds);
        } else {
            listEl.innerHTML = `<div class="error-message">Gagal memuat ERD: ${data.error}</div>`;
        }
    } catch (error) {
        listEl.innerHTML = '<div class="error-message">Gagal memuat ERD</div>';
        console.error('Error:', error);
    } 
}

function renderMyERDs(erds) {
    const listEl = document.getElementById('myERDsList');
    
    if (erds.length === 0) {
        listEl.innerHTML = `
            <div class="empty-erds">
                <i class='bx bx-folder-open'></i>
                <p>Anda belum membuat ERD</p>
                <p style="font-size: 0.9rem; margin-top: 10px;">Klik tombol "Buat ERD Langsung" untuk membuat ERD baru</p>
            </div>
        `;
        return;
    }
    
    erds.forEach(erd => {
        const erdCard = document.createElement('div');
        erdCard.className = 'erd-card';
        
        // Format date
        const createdDate = erd.created_at ? new Date(erd.created_at).toLocaleDateString('id-ID') : '-';
        
        // Badge untuk mode
        // const modeBadge = erd.mode === 'manual' 
        //     ? '<span class="mode-badge manual">Manual</span>' 
        //     : '<span class="mode-badge from-request">Dari Request</span>';
        
        erdCard.innerHTML = `
            <div class="erd-card-header">
                <div class="erd-card-title">${erd.display_name}</div>
                <div class="erd-card-stats">
                    <div class="erd-card-stat">
                        <span>📋</span>
                        <span>${erd.entity_count} Entitas</span>
                    </div>
                    <div class="erd-card-stat">
                        <span>🔗</span>
                        <span>${erd.relationship_count} Relasi</span>
                    </div>
                    <div class="erd-card-stat">
                        <span>📆</span>
                        <span>${createdDate}</span>
                    </div>
                </div>
            </div>
            <div class="erd-card-actions">
                <button class="btn-view-erd" onclick="viewERDImage('${erd.name}')">
                    <i class='bx bxs-show'></i> Lihat
                </button>
                <button class="btn-edit-erd" onclick="editERD('${erd.erd_id}')">
                    <i class='bx bxs-edit'></i> Edit
                </button>
                <button class="btn-delete-erd" onclick="deleteERDById('${erd.erd_id}', '${erd.display_name}')">
                    <i class='bx bxs-trash'></i> Hapus
                </button>
            </div>
        `;
        
        listEl.appendChild(erdCard);
    });
}

// Open direct ERD creation - Redirect to erd-builder
function openDirectERDCreation() {
    // Redirect to erd-builder with manual mode
    window.location.href = '/erd-builder?mode=manual';
}

// View ERD image
async function viewERDImage(erdName) {
    try {
        const response = await fetch(`/api/generate-erd-image/${erdName}`);
        const data = await response.json();
        
        if (response.ok) {
            // Open in new window
            window.open(data.erd_image, '_blank');
        } else {
            showErrorPopup(`Gagal membuka ERD: ${data.error}`);
        }
    } catch (error) {
        showErrorPopup('Gagal membuka ERD');
        console.error('Error:', error);
    }
}

// Delete ERD by ID
async function deleteERDById(erdId, displayName) {
    showWarningPopup(
        'Konfirmasi Hapus',
        `Apakah Anda yakin ingin menghapus ERD "${displayName}"? Tindakan ini tidak dapat dibatalkan.`,
        async (confirmed) => {
            if (!confirmed) return;
            
            try {
                const response = await apiCall(`/api/erd/${erdId}`, {
                    method: 'DELETE'
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    showSuccessPopup('Berhasil!', 'ERD berhasil dihapus!');
                    loadMyERDs();
                } else {
                    showErrorPopup('Gagal!', data.error || 'Gagal menghapus ERD');
                }
            } catch (error) {
                showErrorPopup('Gagal!', 'Gagal menghapus ERD');
                console.error('Error:', error);
            }
        }
    );
}

// Edit ERD - Redirect to erd-builder
function editERD(erdId) {
    // Redirect to erd-builder with edit mode
    window.location.href = `/erd-builder?mode=edit&erd_id=${erdId}`;
}