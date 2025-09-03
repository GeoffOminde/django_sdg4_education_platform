// SDG4 AI Tutor - Django Version JavaScript

// CSRF Token Helper
function getCSRFToken() {
    return document.querySelector('meta[name=csrf-token]')?.getAttribute('content') || 
           document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
}

// Show loading state
function showLoading(element, text = 'Loading...') {
    const originalContent = element.innerHTML;
    element.innerHTML = `<i class="fas fa-spinner fa-spin me-2"></i>${text}`;
    element.disabled = true;
    return originalContent;
}

// Hide loading state
function hideLoading(element, originalContent) {
    element.innerHTML = originalContent;
    element.disabled = false;
}

// Show toast notification
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove toast element after it's hidden
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '1055';
    document.body.appendChild(container);
    return container;
}

// Credit display update
function updateCreditsDisplay(credits) {
    const navCredits = document.getElementById('nav-credits');
    if (navCredits) {
        navCredits.textContent = credits;
        
        // Add visual feedback
        navCredits.parentElement.classList.add('text-warning');
        setTimeout(() => {
            navCredits.parentElement.classList.remove('text-warning');
        }, 1000);
    }
}

// API Error Handler
function handleAPIError(error, defaultMessage = 'An error occurred') {
    console.error('API Error:', error);
    
    if (error.response) {
        error.response.json().then(data => {
            showToast(data.error || defaultMessage, 'danger');
        }).catch(() => {
            showToast(defaultMessage, 'danger');
        });
    } else {
        showToast(defaultMessage, 'danger');
    }
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Auto-hide Django messages after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

