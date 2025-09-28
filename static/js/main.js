// ERD Generator JavaScript
let currentERDData = null;

// Utility Functions
function showStatus(message, type) {
    const statusElement = document.getElementById('searchStatus');
    statusElement.textContent = message;
    statusElement.className = `status ${type}`;
    statusElement.style.display = 'block';
}

function clearResults() {
    document.getElementById('searchResults').style.display = 'none';
    document.getElementById('searchResultsGrid').innerHTML = '';
}

function setLoadingState(isLoading) {
    const searchBtn = document.getElementById('searchBtn');
    const searchBtnText = document.getElementById('searchBtnText');
    const searchSpinner = document.getElementById('searchSpinner');
    
    if (isLoading) {
        searchBtn.disabled = true;
        searchBtnText.style.display = 'none';
        searchSpinner.style.display = 'inline-block';
    } else {
        searchBtn.disabled = false;
        searchBtnText.style.display = 'inline';
        searchSpinner.style.display = 'none';
    }
}

// API Functions
async function searchERD(query, topK, minSimilarity) {
    clearResults();
    setLoadingState(true);
    showStatus('Mencari ERD yang sesuai...', 'loading');
    
    try {
        const response = await fetch('/api/search-erd', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                text: query,
                top_k: topK,
                min_similarity: minSimilarity
            })
        });

        const data = await response.json();
        
        if (response.ok) {
            if (data.results.length > 0) {
                showStatus(
                    `Ditemukan ${data.total_found} ERD yang sesuai dengan query: "${data.query}"`, 
                    'success'
                );
                
                document.getElementById('searchResultsTitle').textContent = 
                    `Hasil Pencarian (${data.total_found} ERD ditemukan):`;
                
                renderSearchResults(data.results);
                document.getElementById('searchResults').style.display = 'block';
            } else {
                showStatus('Tidak ditemukan ERD yang sesuai dengan query Anda. Coba kurangi nilai Min Similarity atau gunakan kata kunci yang berbeda.', 'error');
            }
            
        } else {
            showStatus(data.error || 'Terjadi kesalahan saat melakukan pencarian', 'error');
        }
        
    } catch (error) {
        showStatus('Gagal menghubungi server. Periksa koneksi internet Anda.', 'error');
        console.error('Error:', error);
    } finally {
        setLoadingState(false);
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
        const response = await fetch(`/api/generate-erd-image/${erdName}`);
        const data = await response.json();
        
        if (response.ok) {
            modalImage.src = data.erd_image;
            modalImage.onload = function() {
                modalLoading.style.display = 'none';
                modalImage.style.display = 'block';
                modalActions.style.display = 'flex';
                
                // Update download link
                document.getElementById('downloadBtn').href = data.download_url;
                
                // Store current ERD data
                currentERDData = data;
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

function openFullscreen() {
    if (currentERDData && currentERDData.erd_image) {
        window.open(currentERDData.erd_image, '_blank');
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Form submission
    document.getElementById('erdForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const query = document.getElementById('userInput').value.trim();
        const topK = parseInt(document.getElementById('topK').value) || 10;
        const minSimilarity = parseFloat(document.getElementById('minSimilarity').value) || 0.05;
        
        if (!query) return;
        
        searchERD(query, topK, minSimilarity);
    });

    // Modal event listeners
    document.getElementById('closeModal').addEventListener('click', function() {
        document.getElementById('erdModal').style.display = 'none';
    });

    document.getElementById('fullscreenBtn').addEventListener('click', openFullscreen);

    // Close modal when clicking outside
    window.addEventListener('click', function(event) {
        const modal = document.getElementById('erdModal');
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Auto-focus input on load
    document.getElementById('userInput').focus();

    // Handle Enter key in input
    document.getElementById('userInput').addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            document.getElementById('erdForm').dispatchEvent(new Event('submit'));
        }
    });
});