// Authentication JavaScript

// Token management
function getToken() {
    return localStorage.getItem('token');
}

function setToken(token) {
    localStorage.setItem('token', token);
}

function removeToken() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
}

function getUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

function setUser(user) {
    localStorage.setItem('user', JSON.stringify(user));
}

// API helpers
async function apiCall(url, options = {}) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    const response = await fetch(url, {
        ...options,
        headers
    });
    
    return response;
}

// Status display
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

// Loading state management
function setLoadingState(btnId, textId, spinnerId, isLoading) {
    const btn = document.getElementById(btnId);
    const text = document.getElementById(textId);
    const spinner = document.getElementById(spinnerId);
    
    if (isLoading) {
        btn.disabled = true;
        text.style.display = 'none';
        spinner.style.display = 'inline-block';
    } else {
        btn.disabled = false;
        text.style.display = 'inline';
        spinner.style.display = 'none';
    }
}

// Login form initialization
function initLoginForm() {
    const form = document.getElementById('loginForm');
    
    form.addEventListener('submit', async function(event) {
        event.preventDefault();
        
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value;
        
        if (!username || !password) {
            showStatus('loginStatus', 'Username dan password harus diisi', 'error');
            return;
        }
        
        hideStatus('loginStatus');
        setLoadingState('loginBtn', 'loginBtnText', 'loginSpinner', true);
        
        try {
            const response = await apiCall('/auth/login', {
                method: 'POST',
                body: JSON.stringify({ username, password })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                setToken(data.access_token);
                setUser(data.user);
                
                showStatus('loginStatus', 'Login berhasil! Mengalihkan...', 'success');
                
                // Redirect berdasarkan role
                setTimeout(() => {
                    if (data.user.role === 'advisor') {
                        window.location.href = '/advisor-dashboard';
                    } else {
                        window.location.href = '/user-dashboard';
                    }
                }, 1000);
            } else {
                showStatus('loginStatus', data.error || 'Login gagal', 'error');
            }
        } catch (error) {
            showStatus('loginStatus', 'Gagal menghubungi server', 'error');
            console.error('Login error:', error);
        } finally {
            setLoadingState('loginBtn', 'loginBtnText', 'loginSpinner', false);
        }
    });
}

// Register form initialization
function initRegisterForm() {
    const form = document.getElementById('registerForm');
    
    form.addEventListener('submit', async function(event) {
        event.preventDefault();
        
        const username = document.getElementById('username').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        const role = document.getElementById('role').value;
        
        if (!username || !email || !password || !role) {
            showStatus('registerStatus', 'Semua field harus diisi', 'error');
            return;
        }
        
        if (username.length < 3) {
            showStatus('registerStatus', 'Username harus minimal 3 karakter', 'error');
            return;
        }
        
        if (password.length < 6) {
            showStatus('registerStatus', 'Password harus minimal 6 karakter', 'error');
            return;
        }
        
        hideStatus('registerStatus');
        setLoadingState('registerBtn', 'registerBtnText', 'registerSpinner', true);
        
        try {
            const response = await apiCall('/auth/register', {
                method: 'POST',
                body: JSON.stringify({ username, email, password, role })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                showStatus('registerStatus', 'Registrasi berhasil! Mengalihkan ke login...', 'success');
                
                // Redirect ke login setelah sukses
                setTimeout(() => {
                    window.location.href = '/login';
                }, 2000);
            } else {
                showStatus('registerStatus', data.error || 'Registrasi gagal', 'error');
            }
        } catch (error) {
            showStatus('registerStatus', 'Gagal menghubungi server', 'error');
            console.error('Register error:', error);
        } finally {
            setLoadingState('registerBtn', 'registerBtnText', 'registerSpinner', false);
        }
    });
}

// Logout function
function logout() {
    removeToken();
    window.location.href = '/login';
}

// Check authentication
function requireAuth() {
    const token = getToken();
    if (!token) {
        window.location.href = '/login';
        return false;
    }
    return true;
}

// Check role authorization
function requireRole(requiredRole) {
    const user = getUser();
    if (!user || user.role !== requiredRole) {
        window.location.href = '/login';
        return false;
    }
    return true;
}