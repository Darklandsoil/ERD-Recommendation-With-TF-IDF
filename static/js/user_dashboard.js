// User Dashboard JavaScript
let currentQuery = '';

// Initialize user dashboard
function initUserDashboard() {

    // Display User Welcome
    const user = getUser();
    const firstName = user.fullname.split(' ')[0];
    document.getElementById('userWelcome').textContent = `Selamat datang, ${firstName}!`;
    
    // Initialize tab navigation
    initTabNavigation();
    
    
    // Initialize search functionality
    initSearchFunctionality();
    
    // Initialize modals
    initModals();
    
    // Load initial data
    loadUserRequests();
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
            }
        });
    });
}

// Format date helper
function formatDate(dateString) {
    try {
        const date = new Date(dateString);
        const options = { year: 'numeric', month: 'short', day: 'numeric' };
        return date.toLocaleDateString('id-ID', options);
    } catch (e) {
        return dateString;
    }
}

// Search functionality
function initSearchFunctionality() {
    const searchInput = document.getElementById('userInput');
    
    // Handle Enter key
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            const query = this.value.trim();
            if (query) {
                const topK = parseInt(document.getElementById('topK')?.value) || 10;
                const minSimilarity = parseFloat(document.getElementById('minSimilarity')?.value) || 0.05;
                searchERD(query, topK, minSimilarity);
            }
        }
    });
}

async function searchERD(query, topK, minSimilarity) {
    // ✅ FIX: Update currentQuery
    currentQuery = query;
    
    clearResults();
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
    }
}

// ✅ FIX: Hanya satu fungsi showSuccessResults
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
}

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
    statusDiv.textContent = 'ERD Tidak Ditemukan.';
    statusDiv.style.display = 'block';
    
    // Tampilkan tombol ask advisor
    if (advisorBtn) {
        advisorBtn.style.display = 'inline-flex';
    }
}
    
function clearResults() {
    // Sembunyikan semua container
    const searchResults = document.getElementById('searchResults');
    const emptyStateContainer = document.getElementById('emptyStateContainer');
    
    if (searchResults) {
        searchResults.style.display = 'none';
    }
    if (emptyStateContainer) {
        emptyStateContainer.style.display = 'none';
    }
    
    const resultsGrid = document.getElementById('searchResultsGrid');
    if (resultsGrid) {
        resultsGrid.innerHTML = '';
    }
    
    // Sembunyikan status
    const statusDiv = document.getElementById('searchStatus');
    if (statusDiv) {
        statusDiv.style.display = 'none';
    }
    
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
        
        const erdName = result.name.toLowerCase().replace(/ /g, '_');
        
        card.innerHTML = `
            <div class="title" data-erd-name="${erdName}">${result.name}</div>
                <strong>Entitas:</strong> ${result.entities.join(', ')}
            </div>
            <div class="stats">
                ${result.entity_count} entitas • ${result.relationship_count} relasi
            </div>
        `;
        
        const titleElement = card.querySelector('.title');
        titleElement.addEventListener('click', function() {
            const erdName = this.getAttribute('data-erd-name');
            showERDPreview(erdName, result.name);
        });
        
        resultsGrid.appendChild(card);
    });
}

// ERD Preview
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
    const closeModalBtn = document.getElementById('closeModal');
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', function() {
            document.getElementById('erdModal').style.display = 'none';
        });
    }
    
    const fullscreenBtn = document.getElementById('fullscreenBtn');
    if (fullscreenBtn) {
        fullscreenBtn.addEventListener('click', function() {
            const imageSrc = document.getElementById('modalImage').src;
            if (imageSrc) {
                window.open(imageSrc, '_blank');
            }
        });
    }
    
    // Ask Advisor Modal
    const askAdvisorBtn = document.getElementById('askAdvisorBtn');
    if (askAdvisorBtn) {
        askAdvisorBtn.addEventListener('click', function() {
            document.getElementById('requestQuery').value = currentQuery;
            document.getElementById('askAdvisorModal').style.display = 'block';
        });
    }

    const closeAskAdvisorBtn = document.getElementById('closeAskAdvisorModal');
    if (closeAskAdvisorBtn) {
        closeAskAdvisorBtn.addEventListener('click', closeAskAdvisorModal);
    }

    // Ask Advisor via Request Button
    const requestBtn = document.getElementById('requestBtn')
    if (requestBtn) {
        requestBtn.addEventListener('click', function() {
            document.getElementById('requestQuery');
            document.getElementById('askAdvisorModal').style.display = 'block';
        });
    }

    //close requestBtn
    const closeRequestBtn = document.getElementById('closeAskAdvisorModal');
    if (closeRequestBtn) {
        closeRequestBtn.addEventListener('click', closeAskAdvisorModal);
    }

    
    // Ask Advisor Form
    const askAdvisorForm = document.getElementById('askAdvisorForm');
    if (askAdvisorForm) {
        askAdvisorForm.addEventListener('submit', handleAskAdvisor);
    }
    
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
        showErrorPopup('Gagal', 'Deskripsi harus diisi');
        return;
    }
    
    try {
        const response = await apiCall('/api/requests/', {
            method: 'POST',
            body: JSON.stringify({ query, description })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showSuccessPopup('Berhasil!', 'Request berhasil dikirim ke advisor!');
            closeAskAdvisorModal();
            
            // Switch to requests tab
            const requestsTab = document.querySelector('[data-tab="requests"]');
            if (requestsTab) {
                requestsTab.click();
            }
        } else {
            showErrorPopup('Gagal', data.error || 'Gagal mengirim request');
        }
    } catch (error) {
        showErrorPopup('Gagal', 'Gagal mengirim request. Periksa koneksi internet.');
        console.error('Error:', error);
    }
}

// Load user requests
async function loadUserRequests() {
    const loadingEl = document.getElementById('requestsLoading');
    const listEl = document.getElementById('requestsList');
    
    if (!loadingEl || !listEl) return;
    
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
        listEl.innerHTML = '<div class="empty-message">Belum ada request ERD yang diajukan</div>';
        return;
    }
    
    listEl.innerHTML = '';
    
    requests.forEach((request, index) => {
        const item = document.createElement('div');
        item.className = 'request-item';
        
        // Format status untuk class CSS
        const statusClass = request.status.replace('_', '').toLowerCase();
        
        // Set data-status attribute untuk border color
        item.setAttribute('data-status', statusClass);
        
        // Format tanggal
        const createdDate = new Date(request.created_at).toLocaleDateString('id-ID', {
            day: 'numeric',
            month: 'long',
            year: 'numeric'
        });
        
        // Status display mapping
        const statusDisplayMap = {
            'pending': 'Menunggu',
            'on_process': 'Sedang Dikerjakan',
            'complete': 'Selesai',
            'cancelled': 'Dibatalkan'
        };
        
        const statusDisplay = statusDisplayMap[statusClass] || request.status_display;
        
        item.innerHTML = `
            <div class="item-header">
                <div class="status-badge ${statusClass}">${statusDisplay}</div>
                <div class="item-title">${escapeHtml(request.query)}</div>
            </div>
            <div class="item-description">${escapeHtml(request.description)}</div>
            <div class="item-meta">
                <span>${createdDate}</span>
                <div class="item-actions">
                    ${request.status === 'pending' ? 
                        `<button class="btn-small btn-cancel" onclick="cancelRequest('${request.request_id}')">Batalkan</button>` : 
                        ''
                    }
                    ${request.status === 'complete' && request.notes ? 
                        `<button class="btn-small btn-primary" onclick="showRequestNotes(\`${escapeHtml(request.notes)}\`)">Lihat Catatan</button>` : 
                        ''
                    }
                </div>
            </div>
        `;
        
        listEl.appendChild(item);
    });
}

async function cancelRequest(requestId) {
    showWarningPopup(
        'Konfirmasi Hapus',
        'Apakah Anda yakin ingin membatalkan request? Tindakan ini tidak dapat dibatalkan.',
        async (confirmed) => {
            if (!confirmed) return;

            try {
                const response = await apiCall(`/api/requests/${requestId}/cancel`, {
                    method: 'DELETE'
                });

                const data = await response.json();

                if (response.ok) {
                    showSuccessPopup('Berhasil!', 'Request Berhasil Dibatalkan!');
                    loadUserRequests();
                } else {
                    showErrorPopup('Gagal', 'Gagal Membatalkan Request');
                }
            } catch (error) {
                showErrorPopup('Gagal', 'Gagal Membatalkan Request');
                console.error('Error', error);
            }
        }
    );
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;',
        '`': '&#x60;'
    };
    return text.replace(/[&<>"'`]/g, m => map[m]);
}

function showRequestNotes(notes) {
    showSuccessPopup('Catatan Advisor', notes);
}

// Utility functions
function showStatus(elementId, message, type) {
    const statusElement = document.getElementById(elementId);
    if (!statusElement) return;
    
    statusElement.textContent = message;
    statusElement.className = `status ${type}`;
    statusElement.style.display = 'block';
}

function hideStatus(elementId) {
    const statusElement = document.getElementById(elementId);
    if (statusElement) {
        statusElement.style.display = 'none';
    }
}

// ==========================================
// MODERN POPUP SYSTEM
// ==========================================

// SUCCESS POPUP (Hijau)
function showSuccessPopup(title, message) {
    document.getElementById('successPopupTitle').textContent = title;
    document.getElementById('successPopupMessage').textContent = message;
    document.getElementById('successPopup').classList.remove('hidden');
}

function closeSuccessPopup() {
    document.getElementById('successPopup').classList.add('hidden');
}

// WARNING POPUP (Orange) - dengan callback
let warningCallback = null;

function showWarningPopup(title, message, callback) {
    document.getElementById('warningPopupTitle').textContent = title;
    document.getElementById('warningPopupMessage').textContent = message;
    document.getElementById('warningPopup').classList.remove('hidden');
    warningCallback = callback;
}

function closeWarningPopup(confirmed) {
    document.getElementById('warningPopup').classList.add('hidden');
    if (warningCallback) {
        warningCallback(confirmed);
        warningCallback = null;
    }
}

// ERROR POPUP (Merah)
function showErrorPopup(title, message) {
    document.getElementById('errorPopupTitle').textContent = title;
    document.getElementById('errorPopupMessage').textContent = message;
    document.getElementById('errorPopup').classList.remove('hidden');
}

function closeErrorPopup() {
    document.getElementById('errorPopup').classList.add('hidden');
}

// Close popup on overlay click
document.addEventListener('DOMContentLoaded', function() {
    // Success popup
    const successPopup = document.getElementById('successPopup');
    if (successPopup) {
        successPopup.addEventListener('click', function(e) {
            if (e.target === this) closeSuccessPopup();
        });
    }
    
    // Warning popup
    const warningPopup = document.getElementById('warningPopup');
    if (warningPopup) {
        warningPopup.addEventListener('click', function(e) {
            if (e.target === this) closeWarningPopup(false);
        });
    }
    
    // Error popup
    const errorPopup = document.getElementById('errorPopup');
    if (errorPopup) {
        errorPopup.addEventListener('click', function(e) {
            if (e.target === this) closeErrorPopup();
        });
    }
});

// Close popup on ESC key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        if (!document.getElementById('successPopup').classList.contains('hidden')) {
            closeSuccessPopup();
        }
        if (!document.getElementById('warningPopup').classList.contains('hidden')) {
            closeWarningPopup(false);
        }
        if (!document.getElementById('errorPopup').classList.contains('hidden')) {
            closeErrorPopup();
        }
    }
});