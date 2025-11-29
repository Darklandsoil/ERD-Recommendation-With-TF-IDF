// Authentication JavaScript with Auto Logout

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//                    TOKEN MANAGEMENT
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function getToken() {
    return localStorage.getItem('token');
}

function setToken(token, expiresIn) {
    localStorage.setItem('token', token);
    
    // Simpan waktu expired (sekarang + expiresIn)
    if (expiresIn) {
        const expiryTime = Date.now() + (expiresIn * 1000); // Convert ke milliseconds
        localStorage.setItem('token_expiry', expiryTime);
    }
}

function removeToken() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    localStorage.removeItem('token_expiry');
}

function getUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

function setUser(user) {
    localStorage.setItem('user', JSON.stringify(user));
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//              CHECK TOKEN EXPIRATION
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function isTokenExpired() {
    const expiryTime = localStorage.getItem('token_expiry');
    if (!expiryTime) return true;
    
    // Cek apakah sudah lewat waktu expired
    return Date.now() >= parseInt(expiryTime);
}

function getTokenRemainingTime() {
    const expiryTime = localStorage.getItem('token_expiry');
    if (!expiryTime) return 0;
    
    const remaining = parseInt(expiryTime) - Date.now();
    return remaining > 0 ? remaining : 0;
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//          AUTO LOGOUT KETIKA TOKEN EXPIRED
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

let logoutTimerId = null;

// Set timer untuk auto logout tepat saat token expired
function setAutoLogoutTimer() {
    // Clear timer sebelumnya jika ada
    if (logoutTimerId) {
        clearTimeout(logoutTimerId);
    }
    
    const remaining = getTokenRemainingTime();
    
    if (remaining > 0) {
        // Set timer untuk logout tepat saat token expired
        logoutTimerId = setTimeout(() => {
            showExpiredNotification();
            forceLogout();
        }, remaining);
        
        console.log(`Token akan expired dalam ${Math.floor(remaining / 1000)} detik`);
    } else if (getToken()) {
        // Token sudah expired tapi masih ada di localStorage
        showExpiredNotification();
        forceLogout();
    }
}

// Tampilkan notifikasi token expired
function showExpiredNotification() {
    alert('Sesi Anda telah berakhir. Silakan login kembali.');
}

// Paksa logout dan redirect ke login
function forceLogout() {
    removeToken();
    
    // Redirect ke login dengan parameter expired
    const currentPath = window.location.pathname;
    if (currentPath !== '/login' && !currentPath.includes('/login')) {
        window.location.href = '/login?expired=true';
    }
}

// Check token expiry setiap 30 detik (backup check)
setInterval(() => {
    if (getToken() && isTokenExpired()) {
        showExpiredNotification();
        forceLogout();
    }
}, 30000); // Check setiap 30 detik

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//              WARNING SEBELUM TOKEN EXPIRED
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

let warningShown = false;

// Tampilkan warning 5 menit sebelum expired
function checkTokenExpirySoon() {
    const remaining = getTokenRemainingTime();
    const fiveMinutes = 5 * 60 * 1000; // 5 menit dalam milliseconds
    
    // Jika token akan expired dalam 5 menit dan belum pernah show warning
    if (remaining > 0 && remaining <= fiveMinutes && !warningShown) {
        const minutes = Math.ceil(remaining / (1000 * 60));
        
        if (confirm(`Sesi Anda akan berakhir dalam ${minutes} menit. Tetap aktif?`)) {
            // User klik OK - bisa implement refresh token di sini
            console.log('User memilih untuk tetap aktif');
            warningShown = true;
        } else {
            // User klik Cancel - logout sekarang
            logout();
        }
    }
}

// Check warning setiap 1 menit
setInterval(checkTokenExpirySoon, 60000);

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//                    API HELPERS
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async function apiCall(url, options = {}) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (token) {
        // Check jika token expired sebelum request
        if (isTokenExpired()) {
            showExpiredNotification();
            forceLogout();
            return Promise.reject(new Error('Token expired'));
        }
        
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    try {
        const response = await fetch(url, {
            ...options,
            headers
        });
        
        // Handle 401 Unauthorized (token expired dari server)
        if (response.status === 401) {
            const data = await response.json();
            
            // Cek apakah error karena token expired
            if (data.error && (
                data.error.includes('expired') || 
                data.error.includes('kadaluarsa') ||
                data.error.includes('Token telah')
            )) {
                showExpiredNotification();
                forceLogout();
                return Promise.reject(new Error('Token expired'));
            }
        }
        
        return response;
    } catch (error) {
        console.error('API call error:', error);
        throw error;
    }
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//                  STATUS DISPLAY
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function showStatus(elementId, message, type) {
    const statusElement = document.getElementById(elementId);
    if (statusElement) {
        statusElement.textContent = message;
        statusElement.className = `status ${type}`;
        statusElement.style.display = 'block';
    }
}

function hideStatus(elementId) {
    const statusElement = document.getElementById(elementId);
    if (statusElement) {
        statusElement.style.display = 'none';
    }
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//              LOADING STATE MANAGEMENT
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function setLoadingState(btnId, textId, spinnerId, isLoading) {
    const btn = document.getElementById(btnId);
    const text = document.getElementById(textId);
    const spinner = document.getElementById(spinnerId);
    
    if (btn && text && spinner) {
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
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//              TOGGLE PASSWORD VISIBILITY
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function initPasswordToggle(password, togglePassword) {
    const passwordInput = document.getElementById(password);
    const toggleBtn = document.getElementById(togglePassword);
    
    if (passwordInput && toggleBtn) {
        toggleBtn.addEventListener('click', function() {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            
            if (type === 'password') {
                toggleBtn.innerHTML = `<i class='bx bxs-show'></i>`;
            } else {
                toggleBtn.innerHTML = `<i class='bx bxs-low-vision'></i>`;
            }
        });
    }
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//                  LOGIN FORM
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function initLoginForm() {
    const form = document.getElementById('loginForm');
    if (!form) return;
    
    initPasswordToggle('password', 'togglePassword');
    
    // Tampilkan pesan jika datang dari expired redirect
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('expired') === 'true') {
        showStatus('loginStatus', 'Sesi Anda telah berakhir. Silakan login kembali.', 'error');
        
        // Hapus parameter dari URL tanpa reload
        window.history.replaceState({}, document.title, '/login');
    }
    
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
            const response = await fetch('/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Simpan token dengan expiry time
                setToken(data.access_token, data.expires_in);
                setUser(data.user);
                
                // Set auto logout timer
                setAutoLogoutTimer();
                
                showStatus('loginStatus', 'Login berhasil! Mengalihkan...', 'success');
                
                // Redirect berdasarkan role
                setTimeout(() => {
                    if (data.user.role === 'admin') {
                        window.location.href = '/admin/dashboard';
                    } else if (data.user.role === 'advisor') {
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

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//                  REGISTER FORM
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function initRegisterForm() {
    const form = document.getElementById('registerForm');
    if (!form) return;
    
    initPasswordToggle('password', 'togglePassword');
    initPasswordToggle('cpassword', 'toggleCPassword');
    
    form.addEventListener('submit', async function(event) {
        event.preventDefault();
        
        const fullname = document.getElementById('fullname').value.trim();
        const username = document.getElementById('username').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        const cpassword = document.getElementById('cpassword').value;
        
        if (!fullname || !username || !email || !password || !cpassword) {
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

        if (password !== cpassword) {
            showStatus('registerStatus', 'Konfirmasi password tidak sesuai', 'error');
            return;
        }
        
        hideStatus('registerStatus');
        setLoadingState('registerBtn', 'registerBtnText', 'registerSpinner', true);
        
        try {
            const response = await fetch('/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ fullname, username, email, password })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                showStatus('registerStatus', 'Registrasi berhasil! Mengalihkan ke login...', 'success');
                
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

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//                  LOGOUT FUNCTION
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function logout() {
    // Clear timer
    if (logoutTimerId) {
        clearTimeout(logoutTimerId);
    }
    
    removeToken();
    window.location.href = '/login';
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//              CHECK AUTHENTICATION
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

function requireAuth() {
    const token = getToken();
    if (!token || isTokenExpired()) {
        window.location.href = '/login?expired=true';
        return false;
    }
    
    // Set auto logout timer untuk halaman yang protected
    setAutoLogoutTimer();
    return true;
}

function requireRole(requiredRole) {
    const user = getUser();
    if (!user || user.role !== requiredRole || isTokenExpired()) {
        window.location.href = '/login?expired=true';
        return false;
    }
    
    // Set auto logout timer untuk halaman yang protected
    setAutoLogoutTimer();
    return true;
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//              INITIALIZE ON PAGE LOAD
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

// Auto-run saat halaman dimuat
document.addEventListener('DOMContentLoaded', function() {
    // Jika ada token, set auto logout timer
    if (getToken() && !isTokenExpired()) {
        setAutoLogoutTimer();
    }
    
    // Check apakah token sudah expired saat page load
    if (getToken() && isTokenExpired()) {
        const currentPath = window.location.pathname;
        if (currentPath !== '/login' && !currentPath.includes('/login')) {
            showExpiredNotification();
            forceLogout();
        }
    }
});