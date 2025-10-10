// User Dashboard JavaScript
let currentQuery = '';

// Initialize user dashboard
function initUserDashboard() {
    // Display user welcome message
    const user = getUser();
    document.getElementById('userWelcome').textContent = `Selamat datang, ${user.username}!`;
    
    // Initialize tab navigation
    initTabNavigation();
    
    // Initialize search functionality
    initSearchFunctionality();
    
    // Initialize modals
    initModals();
    
    // Load initial data
    loadUserRequests();
    loadUserHistory();
}

// Tab navigation
function initTabNavigation() {
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
            if (tabId === 'requests-tab') {
                loadUserRequests();
            } else if (tabId === 'history-tab') {
                loadUserHistory();
            }
        });
    });
}

// Search functionality (enhanced from main.js)
function initSearchFunctionality() {
    const form = document.getElementById('erdForm');
    
    form.addEventListener('submit', async function(event) {
        event.preventDefault();
        
        const query = document.getElementById('userInput').value.trim();
        const topK = parseInt(document.getElementById('topK').value) || 10;
        const minSimilarity = parseFloat(document.getElementById('minSimilarity').value) || 0.05;
        
        if (!query) return;
        
        currentQuery = query;
        await searchERD(query, topK, minSimilarity);
    });
}

async function searchERD(query, topK, minSimilarity) {
    clearResults();
    setLoadingState('searchBtn', 'searchBtnText', 'searchSpinner', true);
    showStatus('searchStatus', 'Mencari ERD yang sesuai...', 'loading');
    
    try {
        const response = await apiCall('/api/search-erd', {
            method: 'POST',
            body: JSON.stringify({ 
                text: query,
                top_k: topK,
                min_similarity: minSimilarity
            })
        });

        const data = await response.json();
        
        if (response.ok) {
            if (data.results.length > 0) {
                // Ada hasil - tampilkan hasil pencarian normal
                showSuccessResults(data);
            } else {
                // Tidak ada hasil - tampilkan empty state yang centered
                showEmptyState(query);
            }
        } else {
            showStatus('searchStatus', data.error || 'Terjadi kesalahan saat melakukan pencarian', 'error');
        }
        
    } catch (error) {
        showStatus('searchStatus', 'Gagal menghubungi server. Periksa koneksi internet Anda.', 'error');
        console.error('Error:', error);
    } finally {
        setLoadingState('searchBtn', 'searchBtnText', 'searchSpinner', false);
    }
}

// Fungsi untuk menampilkan hasil sukses
function showSuccessResults(data) {
    // Sembunyikan empty state container
    const emptyStateContainer = document.getElementById('emptyStateContainer');
    if (emptyStateContainer) {
        emptyStateContainer.style.display = 'none';
    }
    
    // Tampilkan hasil pencarian
    const searchResults = document.getElementById('searchResults');
    const searchResultsTitle = document.getElementById('searchResultsTitle');
    
    showStatus('searchStatus', 
        `Ditemukan ${data.total_found} ERD yang sesuai dengan query: "${data.query}"`, 
        'success'
    );
    
    searchResultsTitle.textContent = `Hasil Pencarian (${data.total_found} ERD ditemukan):`;
    
    renderSearchResults(data.results);
    searchResults.style.display = 'block';
    
    // Sembunyikan status di dalam empty state jika ada
    const statusInEmpty = document.querySelector('#emptyStateContainer #searchStatus');
    if (statusInEmpty) {
        statusInEmpty.style.display = 'none';
    }
    
    // Sembunyikan tombol advisor di empty state
    const advisorBtnInEmpty = document.querySelector('#emptyStateContainer #askAdvisorBtn');
    if (advisorBtnInEmpty) {
        advisorBtnInEmpty.style.display = 'none';
    }
}

// Fungsi untuk menampilkan empty state yang centered
function showEmptyState(query) {
    // Sembunyikan search results normal
    const searchResults = document.getElementById('searchResults');
    searchResults.style.display = 'none';
    
    // Tampilkan empty state container
    const emptyStateContainer = document.getElementById('emptyStateContainer');
    const statusDiv = document.getElementById('searchStatus');
    const advisorBtn = document.getElementById('askAdvisorBtn');
    
    if (emptyStateContainer) {
        emptyStateContainer.style.display = 'flex';
    }
    
    // Set pesan error
    statusDiv.className = 'error';
    statusDiv.textContent = 'Tidak ditemukan ERD yang sesuai dengan query Anda.';
    statusDiv.style.display = 'block';
    
    // Tampilkan tombol ask advisor
    advisorBtn.style.display = 'inline-flex';
}

// Fungsi untuk menampilkan hasil sukses
function showSuccessResults(data) {
    // Sembunyikan empty state container
    const emptyStateContainer = document.getElementById('emptyStateContainer');
    if (emptyStateContainer) {
        emptyStateContainer.style.display = 'none';
    }
    
    // Tampilkan hasil pencarian
    const searchResults = document.getElementById('searchResults');
    const searchResultsTitle = document.getElementById('searchResultsTitle');
    
    showStatus('searchStatus', 
        `Ditemukan ${data.total_found} ERD yang sesuai dengan query: "${data.query}"`, 
        'success'
    );
    
    searchResultsTitle.textContent = `Hasil Pencarian (${data.total_found} ERD ditemukan):`;
    
    renderSearchResults(data.results);
    searchResults.style.display = 'block';
    
    // Sembunyikan status di dalam empty state jika ada
    const statusInEmpty = document.querySelector('#emptyStateContainer #searchStatus');
    if (statusInEmpty) {
        statusInEmpty.style.display = 'none';
    }
    
    // Sembunyikan tombol advisor di empty state
    const advisorBtnInEmpty = document.querySelector('#emptyStateContainer #askAdvisorBtn');
    if (advisorBtnInEmpty) {
        advisorBtnInEmpty.style.display = 'none';
    }
}

// Fungsi untuk menampilkan empty state yang centered
function showEmptyState(query) {
    // Sembunyikan search results normal
    const searchResults = document.getElementById('searchResults');
    searchResults.style.display = 'none';
    
    // Tampilkan empty state container
    const emptyStateContainer = document.getElementById('emptyStateContainer');
    const statusDiv = document.getElementById('searchStatus');
    const advisorBtn = document.getElementById('askAdvisorBtn');
    
    if (emptyStateContainer) {
        emptyStateContainer.style.display = 'flex';
    }
    
    // Set pesan error
    statusDiv.className = 'error';
    statusDiv.textContent = 'Tidak ditemukan ERD yang sesuai dengan query Anda.';
    statusDiv.style.display = 'block';
    
    // Tampilkan tombol ask advisor
    advisorBtn.style.display = 'inline-flex';
}
    
function clearResults() {
    // Sembunyikan semua container
    const searchResults = document.getElementById('searchResults');
    const emptyStateContainer = document.getElementById('emptyStateContainer');
    
    searchResults.style.display = 'none';
    if (emptyStateContainer) {
        emptyStateContainer.style.display = 'none';
    }
    
    document.getElementById('searchResultsGrid').innerHTML = '';
    
    // Sembunyikan status
    const statusDiv = document.getElementById('searchStatus');
    statusDiv.style.display = 'none';
    
    // Sembunyikan tombol advisor
    const advisorBtn = document.getElementById('askAdvisorBtn');
    if (advisorBtn) {
        advisorBtn.style.display = 'none';
    }
}

function renderSearchResults(results) {
    const resultsGrid = document.getElementById('searchResultsGrid');
    resultsGrid.innerHTML = '';
    
    results.forEach(result => {
        const card = document.createElement('div');
        card.className = 'search-result-card';
        card.innerHTML = `
            <div class="title" data-erd-name="${result.name.toLowerCase().replace(/ /g, '_')}">${result.name}</div>
            <div class="similarity-badge">
                Similarity: ${result.similarity}
            </div>
            <div class="entities">
                <strong>Entitas:</strong> ${result.entities.join(', ')}
            </div>
            <div class="stats">
                ${result.entity_count} entitas • ${result.relationship_count} relasi
            </div>
        `;
        
        // Add click event to title
        const titleElement = card.querySelector('.title');
        titleElement.addEventListener('click', function() {
            const erdName = this.getAttribute('data-erd-name');
            showERDPreview(erdName, result.name);
        });
        
        resultsGrid.appendChild(card);
    });
}

// ERD Preview (enhanced from main.js)
async function showERDPreview(erdName, displayName) {
    const modal = document.getElementById('erdModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalLoading = document.getElementById('modalLoading');
    const modalImage = document.getElementById('modalImage');
    const modalError = document.getElementById('modalError');
    const modalActions = document.getElementById('modalActions');
    
    // Show modal
    modal.style.display = 'block';
    modalTitle.textContent = `Preview ERD: ${displayName}`;
    
    // Show loading state
    modalLoading.style.display = 'block';
    modalImage.style.display = 'none';
    modalError.style.display = 'none';
    modalActions.style.display = 'none';
    
    try {
        const response = await apiCall(`/api/generate-erd-image/${erdName}`);
        const data = await response.json();
        
        if (response.ok) {
            modalImage.src = data.erd_image;
            modalImage.onload = function() {
                modalLoading.style.display = 'none';
                modalImage.style.display = 'block';
                modalActions.style.display = 'flex';
                
                // Update download link
                document.getElementById('downloadBtn').href = data.download_url;
            };
        } else {
            modalLoading.style.display = 'none';
            modalError.textContent = data.error || 'Gagal memuat ERD';
            modalError.style.display = 'block';
        }
        
    } catch (error) {
        modalLoading.style.display = 'none';
        modalError.textContent = 'Gagal memuat ERD. Periksa koneksi internet Anda.';
        modalError.style.display = 'block';
        console.error('Error:', error);
    }
}

// Initialize modals
function initModals() {
    // ERD Modal
    document.getElementById('closeModal').addEventListener('click', function() {
        document.getElementById('erdModal').style.display = 'none';
    });
    
    document.getElementById('fullscreenBtn').addEventListener('click', function() {
        const imageSrc = document.getElementById('modalImage').src;
        if (imageSrc) {
            window.open(imageSrc, '_blank');
        }
    });
    
    // Ask Advisor Modal
    const askAdvisorBtn = document.getElementById('askAdvisorBtn');
    if (askAdvisorBtn) {
        askAdvisorBtn.addEventListener('click', function() {
            document.getElementById('requestQuery').value = currentQuery;
            document.getElementById('askAdvisorModal').style.display = 'block';
        });
    }
    
    document.getElementById('closeAskAdvisorModal').addEventListener('click', closeAskAdvisorModal);
    
    // Ask Advisor Form
    document.getElementById('askAdvisorForm').addEventListener('submit', handleAskAdvisor);
    
    // Close modals when clicking outside
    window.addEventListener('click', function(event) {
        const erdModal = document.getElementById('erdModal');
        const askModal = document.getElementById('askAdvisorModal');
        
        if (event.target === erdModal) {
            erdModal.style.display = 'none';
        }
        if (event.target === askModal) {
            askModal.style.display = 'none';
        }
    });
}

function closeAskAdvisorModal() {
    document.getElementById('askAdvisorModal').style.display = 'none';
    document.getElementById('askAdvisorForm').reset();
}

async function handleAskAdvisor(event) {
    event.preventDefault();
    
    const query = document.getElementById('requestQuery').value;
    const description = document.getElementById('requestDescription').value.trim();
    
    if (!description) {
        alert('Deskripsi harus diisi');
        return;
    }
    
    try {
        const response = await apiCall('/api/requests/', {
            method: 'POST',
            body: JSON.stringify({ query, description })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert('Request berhasil dikirim ke advisor!');
            closeAskAdvisorModal();
            
            // Switch to requests tab
            document.querySelector('[data-tab="requests"]').click();
        } else {
            alert(data.error || 'Gagal mengirim request');
        }
    } catch (error) {
        alert('Gagal mengirim request. Periksa koneksi internet.');
        console.error('Error:', error);
    }
}

// Load user requests
async function loadUserRequests() {
    const loadingEl = document.getElementById('requestsLoading');
    const listEl = document.getElementById('requestsList');
    
    loadingEl.style.display = 'block';
    listEl.innerHTML = '';
    
    try {
        const response = await apiCall('/api/requests/my-requests');
        const data = await response.json();
        
        if (response.ok) {
            renderRequestsList(data.requests);
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

function renderRequestsList(requests) {
    const listEl = document.getElementById('requestsList');
    
    if (requests.length === 0) {
        listEl.innerHTML = '<div class="empty-message">Belum ada request ERD</div>';
        return;
    }
    
    requests.forEach(request => {
        const item = document.createElement('div');
        item.className = 'request-item';
        
        const statusClass = request.status.replace('_', '');
        const createdDate = new Date(request.created_at).toLocaleDateString('id-ID');
        
        item.innerHTML = `
            <div class="item-header">
                <div class="item-title">${request.query}</div>
                <div class="status-badge ${statusClass}">${request.status_display}</div>
            </div>
            <div class="item-description">${request.description}</div>
            <div class="item-meta">
                <span>Dibuat: ${createdDate}</span>
                <div class="item-actions">
                    ${request.status === 'pending' ? 
                        `<button class="btn-small btn-cancel" onclick="cancelRequest('${request.request_id}')">Batalkan</button>` : 
                        ''
                    }
                    ${request.status === 'complete' && request.notes ? 
                        `<button class="btn-small btn-primary" onclick="showRequestNotes('${request.notes}')">Lihat Catatan</button>` : 
                        ''
                    }
                </div>
            </div>
        `;
        
        listEl.appendChild(item);
    });
}

async function cancelRequest(requestId) {
    if (!confirm('Yakin ingin membatalkan request ini?')) return;
    
    try {
        const response = await apiCall(`/api/requests/${requestId}/cancel`, {
            method: 'PUT'
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert('Request berhasil dibatalkan');
            loadUserRequests();
        } else {
            alert(data.error || 'Gagal membatalkan request');
        }
    } catch (error) {
        alert('Gagal membatalkan request');
        console.error('Error:', error);
    }
}

function showRequestNotes(notes) {
    alert(`Catatan dari Advisor:\n\n${notes}`);
}

// Load user history
async function loadUserHistory() {
    const loadingEl = document.getElementById('historyLoading');
    const listEl = document.getElementById('historyList');
    
    loadingEl.style.display = 'block';
    listEl.innerHTML = '';
    
    try {
        // Get completed requests as history
        const response = await apiCall('/api/requests/my-requests');
        const data = await response.json();
        
        if (response.ok) {
            const completedRequests = data.requests.filter(req => req.status === 'complete');
            renderHistoryList(completedRequests);
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

function renderHistoryList(history) {
    const listEl = document.getElementById('historyList');
    
    if (history.length === 0) {
        listEl.innerHTML = '<div class="empty-message">Belum ada riwayat ERD</div>';
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
            <div class="item-meta">
                <span>Selesai: ${completedDate}</span>
                ${item.notes ? `<span>📝 Ada catatan advisor</span>` : ''}
            </div>
        `;
        
        if (item.notes) {
            historyItem.addEventListener('click', () => showRequestNotes(item.notes));
            historyItem.style.cursor = 'pointer';
        }
        
        listEl.appendChild(historyItem);
    });
}

// Utility functions
function showStatus(elementId, message, type) {
    const statusElement = document.getElementById(elementId);
    statusElement.textContent = message;
    statusElement.className = `status ${type}`;
    statusElement.style.display = 'block';
}

function hideStatus(elementId) {
    const statusElement = document.getElementById(elementId);
    statusElement.style.display = 'none';
}