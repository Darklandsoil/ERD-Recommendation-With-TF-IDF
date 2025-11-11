// ==========================================
// DASHBOARD HELPER FUNCTIONS
// ==========================================

/**
 * Toggle Sidebar Collapse/Expand
 */
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('collapsed');
    
    // Save state to localStorage
    const isCollapsed = sidebar.classList.contains('collapsed');
    localStorage.setItem('sidebarCollapsed', isCollapsed);
}

/**
 * Switch between tabs
 * @param {string} tabName - Name of the tab to switch to
 */
function switchTab(tabName) {
    // Remove active class from all tabs and menu items
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.menu-item').forEach(item => {
        item.classList.remove('active');
    });

    // Add active class to selected tab and menu item
    const selectedTab = document.getElementById(tabName + '-tab');
    const selectedMenuItem = document.querySelector(`[data-tab="${tabName}"]`);
    
    if (selectedTab) selectedTab.classList.add('active');
    if (selectedMenuItem) selectedMenuItem.classList.add('active');

    // Load data based on tab
    if (tabName === 'dashboard' && typeof loadAllDiagrams === 'function') {
        loadAllDiagrams();
    } else if (tabName === 'requests' && typeof loadUserRequests === 'function') {
        loadUserRequests();
    } else if (tabName === 'history' && typeof loadUserHistory === 'function') {
        loadUserHistory();
    }

    // Update URL hash without scrolling
    history.pushState(null, null, '#' + tabName);
}

/**
 * Show/Hide Modal
 * @param {string} modalId - ID of the modal element
 * @param {boolean} show - true to show, false to hide
 */
function toggleModal(modalId, show) {
    const modal = document.getElementById(modalId);
    if (!modal) return;

    if (show) {
        modal.classList.add('active');
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
    } else {
        modal.classList.remove('active');
        setTimeout(() => {
            modal.style.display = 'none';
        }, 300);
        document.body.style.overflow = ''; // Restore scrolling
    }
}

/**
 * Close modal when clicking outside
 */
function initModalClosers() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                toggleModal(modal.id, false);
            }
        });
    });

    // Close buttons
    document.querySelectorAll('.close').forEach(closeBtn => {
        closeBtn.addEventListener('click', function() {
            const modal = this.closest('.modal');
            if (modal) toggleModal(modal.id, false);
        });
    });
}

/**
 * Initialize sidebar state from localStorage
 */
function initSidebarState() {
    const sidebarCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
    const sidebar = document.getElementById('sidebar');
    
    if (sidebarCollapsed && sidebar) {
        sidebar.classList.add('collapsed');
    }
}

/**
 * Handle responsive sidebar for mobile
 */
function initResponsiveSidebar() {
    // Add mobile menu toggle button if not exists
    const navBrand = document.querySelector('.nav-brand');
    if (navBrand && window.innerWidth <= 768) {
        const mobileToggle = document.createElement('button');
        mobileToggle.className = 'mobile-menu-toggle';
        mobileToggle.innerHTML = '<i class="bx bx-menu"></i>';
        mobileToggle.onclick = toggleMobileSidebar;
        
        if (!document.querySelector('.mobile-menu-toggle')) {
            navBrand.appendChild(mobileToggle);
        }
    }
}

/**
 * Toggle mobile sidebar
 */
function toggleMobileSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('mobile-open');
}

/**
 * Close mobile sidebar when clicking menu item
 */
function initMobileMenuCloser() {
    if (window.innerWidth <= 768) {
        document.querySelectorAll('.menu-item').forEach(item => {
            item.addEventListener('click', () => {
                const sidebar = document.getElementById('sidebar');
                sidebar.classList.remove('mobile-open');
            });
        });
    }
}

/**
 * Format date to readable format
 * @param {string} dateString - ISO date string
 * @returns {string} Formatted date
 */
function formatDate(dateString) {
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString('id-ID', options);
}

/**
 * Show notification toast
 * @param {string} message - Message to display
 * @param {string} type - Type of notification (success, error, warning)
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 90px;
        right: 20px;
        padding: 15px 25px;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        z-index: 3000;
        animation: slideInRight 0.3s ease;
        font-weight: 500;
    `;

    document.body.appendChild(notification);

    // Auto remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

/**
 * Debounce function to limit function calls
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} Debounced function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Initialize all dashboard helpers
 */
function initDashboardHelpers() {
    initSidebarState();
    initModalClosers();
    initResponsiveSidebar();
    initMobileMenuCloser();

    // Handle browser back/forward with tabs
    window.addEventListener('popstate', () => {
        const hash = window.location.hash.replace('#', '');
        if (hash) {
            switchTab(hash);
        }
    });

    // Set initial tab from URL hash
    const initialHash = window.location.hash.replace('#', '');
    if (initialHash && ['dashboard', 'search', 'requests', 'history'].includes(initialHash)) {
        switchTab(initialHash);
    }

    // Handle window resize
    const handleResize = debounce(() => {
        initResponsiveSidebar();
    }, 250);
    window.addEventListener('resize', handleResize);
}

// Add notification animations to document
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }

    .mobile-menu-toggle {
        display: none;
        background: transparent;
        border: none;
        color: var(--text-primary);
        font-size: 1.5rem;
        cursor: pointer;
        padding: 5px;
        margin-left: 10px;
    }

    @media (max-width: 768px) {
        .mobile-menu-toggle {
            display: block;
        }
    }
`;
document.head.appendChild(style);

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initDashboardHelpers);
} else {
    initDashboardHelpers();
}