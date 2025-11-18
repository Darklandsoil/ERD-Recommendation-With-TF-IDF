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