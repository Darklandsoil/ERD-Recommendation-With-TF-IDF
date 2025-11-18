// Admin Dashboard JavaScript

// Check authentication
document.addEventListener('DOMContentLoaded', function() {
    checkAuth();
});

function checkAuth() {
    const token = localStorage.getItem('token');
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    
    if (!token || user.role !== 'admin') {
        window.location.href = '/login';
        return;
    }
    
    // Display welcome message
    document.getElementById('adminWelcome').textContent = `Selamat datang, ${user.username}`;
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login';
}

// ==========================================
// STATISTICS FUNCTIONS
// ==========================================

// Load system statistics
async function loadStatistics() {
    const loadingEl = document.getElementById('statisticsLoading');
    const cardsEl = document.getElementById('statisticsCards');
    
    loadingEl.style.display = 'block';
    cardsEl.innerHTML = '';
    
    try {
        const token = localStorage.getItem('token');
        const response = await fetch('/admin/api/statistics', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to load statistics');
        }
        
        const data = await response.json();
        loadingEl.style.display = 'none';
        
        renderStatistics(data.statistics);
        
    } catch (error) {
        console.error('Error loading statistics:', error);
        loadingEl.innerHTML = '<p style="color: var(--error-color);">Gagal memuat statistik</p>';
    }
}

function renderStatistics(stats) {
    const cardsEl = document.getElementById('statisticsCards');

    cardsEl.innerHTML = '';
    
    const statsData = [
        {
            icon: '👥',
            label: 'Total User',
            value: stats.total_users,
            color: '#3b82f6'
        },
        {
            icon: '🎓',
            label: 'Total Advisor',
            value: stats.total_advisors,
            color: '#10b981'
        },
        {
            icon: '📋',
            label: 'Total Request',
            value: stats.total_requests,
            color: '#f59e0b'
        },
        {
            icon: '🗂️',
            label: 'Total ERD',
            value: stats.total_erds,
            color: '#8b5cf6'
        },
        {
            icon: '⏳',
            label: 'Request Pending',
            value: stats.pending_requests,
            color: '#ef4444'
        },
        {
            icon: '✅',
            label: 'Request Selesai',
            value: stats.completed_requests,
            color: '#10b981'
        }
    ];
    
    statsData.forEach(stat => {
        const card = document.createElement('div');
        card.className = 'stat-card';
        card.style.borderLeftColor = stat.color;
        
        card.innerHTML = `
            <div class="stat-icon" style="background: ${stat.color}20; color: ${stat.color};">
                ${stat.icon}
            </div>
            <div class="stat-info">
                <div class="stat-label">${stat.label}</div>
                <div class="stat-value">${stat.value}</div>
            </div>
        `;
        
        cardsEl.appendChild(card);
    });
}

// ==========================================
// ADVISOR MONITORING FUNCTIONS
// ==========================================

// Load advisor monitoring data
async function loadAdvisorMonitoring() {
    const loadingEl = document.getElementById('monitoringLoading');
    const tableEl = document.getElementById('monitoringTable');
    
    loadingEl.style.display = 'block';
    tableEl.innerHTML = '';
    
    try {
        const token = localStorage.getItem('token');
        const response = await fetch('/admin/api/advisor-monitoring', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to load advisor monitoring');
        }
        
        const data = await response.json();
        loadingEl.style.display = 'none';
        
        renderAdvisorMonitoring(data.advisor_activities);
        
    } catch (error) {
        console.error('Error loading advisor monitoring:', error);
        loadingEl.innerHTML = '<p style="color: var(--error-color);">Gagal memuat data monitoring</p>';
    }
}

function renderAdvisorMonitoring(activities) {
    const tableEl = document.getElementById('monitoringTable');
    
    if (activities.length === 0) {
        tableEl.innerHTML = `
            <div class="empty-state">
                <i class='bx bx-user-x'></i>
                <p>Belum ada aktivitas advisor</p>
            </div>
        `;
        return;
    }
    
    let tableHTML = `
        <table class="monitoring-table">
            <thead>
                <tr>
                    <th>Nama Lengkap</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Total ERD Dibuat</th>
                    <th>Request Selesai</th>
                    <th>Request On Process</th>
                    <th>Total Aktivitas</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    activities.forEach(activity => {
        const totalActivity = activity.total_erds + activity.completed_requests;
        
        tableHTML += `
            <tr>
                <td><strong>${activity.fullname}</strong></td>
                <td><strong>${activity.username}</strong></td>
                <td>${activity.email}</td>
                <td><span class="badge badge-primary">${activity.total_erds}</span></td>
                <td><span class="badge badge-success">${activity.completed_requests}</span></td>
                <td><span class="badge badge-warning">${activity.in_progress_requests}</span></td>
                <td><strong>${totalActivity}</strong></td>
            </tr>
        `;
    });
    
    tableHTML += `
            </tbody>
        </table>
    `;
    
    tableEl.innerHTML = tableHTML;
}

// Load all advisors
async function loadAdvisors() {
    const loading = document.getElementById('advisorsLoading');
    const tableContainer = document.getElementById('advisorsTable');
    
    try {
        const token = localStorage.getItem('token');
        const response = await fetch('/admin/api/advisors', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to load advisors');
        }
        
        const data = await response.json();
        loading.style.display = 'none';
        
        if (data.advisors.length === 0) {
            tableContainer.innerHTML = `
                <div class="empty-state">
                    <i class='bx bx-user-x'></i>
                    <p>Belum ada pakar yang terdaftar</p>
                </div>
            `;
            return;
        }
        
        // Build table
        let tableHTML = `
            <table class="advisors-table">
                <thead>
                    <tr>
                        <th>Nama Lengkap</th>
                        <th>Username</th>
                        <th>Email</th>
                        <th>Tanggal Dibuat</th>
                        <th>Status</th>
                        <th>Aksi</th>
                    </tr>
                </thead>
                <tbody>
        `;
        
        data.advisors.forEach(advisor => {
            const statusClass = advisor.is_active ? 'status-active' : 'status-inactive';
            const statusText = advisor.is_active ? 'Aktif' : 'Nonaktif';
            
            tableHTML += `
                <tr>
                    <td>${advisor.fullname}</td>
                    <td>${advisor.username}</td>
                    <td>${advisor.email}</td>
                    <td>${advisor.created_at || '-'}</td>
                    <td><span class="status-badge ${statusClass}">${statusText}</span></td>
                    <td>
                        <div class="action-buttons">
                            <button class="btn-edit" onclick='editAdvisor(${JSON.stringify(advisor)})'>
                                <i class='bx bx-edit'></i> Edit
                            </button>
                            <button class="btn-delete" onclick="deleteAdvisor('${advisor.user_id}', '${advisor.username}')">
                                <i class='bx bx-trash'></i> Hapus
                            </button>
                        </div>
                    </td>
                </tr>
            `;
        });
        
        tableHTML += `
                </tbody>
            </table>
        `;
        
        tableContainer.innerHTML = tableHTML;
        
    } catch (error) {
        console.error('Error loading advisors:', error);
        loading.innerHTML = '<p style="color: var(--error-color);">Gagal memuat data pakar</p>';
    }
}

// Show add advisor modal
function showAddAdvisorModal() {
    const modal = document.getElementById('addAdvisorModal');
    modal.classList.add('active');
}

// Close add advisor modal
function closeAddAdvisorModal() {
    const modal = document.getElementById('addAdvisorModal');
    modal.classList.remove('active');
    document.getElementById('addAdvisorForm').reset();
}

// Handle add advisor form submission
document.getElementById('addAdvisorForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const fullname = document.getElementById('newFullname').value
    const username = document.getElementById('newUsername').value;
    const email = document.getElementById('newEmail').value;
    const password = document.getElementById('newPassword').value;
    
    try {
        const token = localStorage.getItem('token');
        const response = await fetch('/admin/api/advisors/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ fullname, username, email, password })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            showErrorPopup(data.error || 'Gagal menambah pakar');
            return;
        }
        
        showSuccessPopup('Pakar berhasil ditambahkan!');
        closeAddAdvisorModal();
        loadAdvisors();
        
    } catch (error) {
        console.error('Error adding advisor:', error);
        showErrorPopup('Terjadi kesalahan saat menambah pakar');
    }
});

// Edit advisor
function editAdvisor(advisor) {
    const modal = document.getElementById('editAdvisorModal');
    modal.classList.add('active');
    
    document.getElementById('editUserId').value = advisor.user_id;
    document.getElementById('editFullname').value = advisor.fullname;
    document.getElementById('editUsername').value = advisor.username;
    document.getElementById('editEmail').value = advisor.email;
    document.getElementById('editPassword').value = '';
}

// Close edit advisor modal
function closeEditAdvisorModal() {
    const modal = document.getElementById('editAdvisorModal');
    modal.classList.remove('active');
    document.getElementById('editAdvisorForm').reset();
}

// Handle edit advisor form submission
document.getElementById('editAdvisorForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const user_id = document.getElementById('editUserId').value;
    const fullname = document.getElementById('editFullname').value;
    const username = document.getElementById('editUsername').value;
    const email = document.getElementById('editEmail').value;
    const password = document.getElementById('editPassword').value;
    
    const updateData = { user_id, fullname, username, email };
    if (password) {
        updateData.password = password;
    }
    
    try {
        const token = localStorage.getItem('token');
        const response = await fetch('/admin/api/advisors/update', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(updateData)
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            showErrorPopup(data.error || 'Gagal mengupdate pakar');
            return;
        }
        
        showSuccessPopup('Pakar berhasil diupdate!');
        closeEditAdvisorModal();
        loadAdvisors();
        
    } catch (error) {
        console.error('Error updating advisor:', error);
        showErrorPopup('Terjadi kesalahan saat mengupdate pakar');
    }
});

// Delete advisor
async function deleteAdvisor(userId, username) {
    showWarningPopup(
        'Konfirmasi Hapus',
        `Apakah Anda yakin ingin menghapus pakar "${username}"? Tindakan ini tidak dapat dibatalkan.`,
        async (confirmed) => {
            if (!confirmed) return;
            
            try {
                const token = localStorage.getItem('token'); 
                const response = await fetch(`/admin/api/advisors/delete`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ user_id: userId })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    showSuccessPopup('Berhasil!', 'Pakar berhasil dihapus!');
                    loadAdvisors();
                } else {
                    showErrorPopup('Gagal!', data.error || 'Gagal menghapus ERD');
                }
            } catch (error) {
                showErrorPopup('Gagal!', 'Terjadi kesalahan saat menghapus pakar');
                console.error('Error:', error);
            }
        }
    );
}

// Close modal when clicking outside
window.onclick = function(event) {
    const addModal = document.getElementById('addAdvisorModal');
    const editModal = document.getElementById('editAdvisorModal');
    
    if (event.target === addModal) {
        closeAddAdvisorModal();
    }
    if (event.target === editModal) {
        closeEditAdvisorModal();
    }
}