// Admin Dashboard JavaScript

// Check authentication
document.addEventListener('DOMContentLoaded', function() {
    checkAuth();
    loadAdvisors();
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
            body: JSON.stringify({ username, email, password })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            alert(data.error || 'Gagal menambah pakar');
            return;
        }
        
        alert('Pakar berhasil ditambahkan!');
        closeAddAdvisorModal();
        loadAdvisors();
        
    } catch (error) {
        console.error('Error adding advisor:', error);
        alert('Terjadi kesalahan saat menambah pakar');
    }
});

// Edit advisor
function editAdvisor(advisor) {
    const modal = document.getElementById('editAdvisorModal');
    modal.classList.add('active');
    
    document.getElementById('editUserId').value = advisor.user_id;
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
    const username = document.getElementById('editUsername').value;
    const email = document.getElementById('editEmail').value;
    const password = document.getElementById('editPassword').value;
    
    const updateData = { user_id, username, email };
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
            alert(data.error || 'Gagal mengupdate pakar');
            return;
        }
        
        alert('Pakar berhasil diupdate!');
        closeEditAdvisorModal();
        loadAdvisors();
        
    } catch (error) {
        console.error('Error updating advisor:', error);
        alert('Terjadi kesalahan saat mengupdate pakar');
    }
});

// Delete advisor
async function deleteAdvisor(userId, username) {
    if (!confirm(`Apakah Anda yakin ingin menghapus pakar "${username}"?`)) {
        return;
    }
    
    try {
        const token = localStorage.getItem('token');
        const response = await fetch('/admin/api/advisors/delete', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ user_id: userId })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            alert(data.error || 'Gagal menghapus pakar');
            return;
        }
        
        alert('Pakar berhasil dihapus!');
        loadAdvisors();
        
    } catch (error) {
        console.error('Error deleting advisor:', error);
        alert('Terjadi kesalahan saat menghapus pakar');
    }
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
