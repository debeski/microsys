document.addEventListener('DOMContentLoaded', function() {
    const enableBtn = document.getElementById('enable2FABtn');
    const otpSetupForm = document.getElementById('otpSetupForm');

    if (enableBtn) {
        enableBtn.addEventListener('click', initiate2FASetup);
    }

    if (otpSetupForm) {
        otpSetupForm.addEventListener('submit', submitOTPSetup);
    }
});

function initiate2FASetup() {
    const btn = document.getElementById('enable2FABtn');
    const url = btn.dataset.url;

    // 1. Request OTP via AJAX
    fetch(url + "?ajax=1", {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // 2. Show Modal
            const modalEl = document.getElementById('otpSetupModal');
            const modal = new bootstrap.Modal(modalEl);
            modal.show();
            
            // Focus after modal is shown
            modalEl.addEventListener('shown.bs.modal', function () {
                document.getElementById('otpSetupInput').focus();
            });
        } else {
            alert(data.message || 'Error sending OTP');
        }
    })
    .catch(err => {
        console.error(err);
        alert('Connection error');
    });
}

function submitOTPSetup(e) {
    e.preventDefault();
    const form = e.target;
    const url = form.dataset.url;
    const csrfToken = form.dataset.csrf;
    
    const code = document.getElementById('otpSetupInput').value;
    const errorDiv = document.getElementById('otpSetupError');
    
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: `otp_code=${code}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            window.location.reload(); // Reload to show enabled state
        } else {
            errorDiv.textContent = data.message || 'Invalid Code';
            errorDiv.classList.remove('d-none');
        }
    })
    .catch(err => {
        console.error(err);
        errorDiv.textContent = 'Connection error';
        errorDiv.classList.remove('d-none');
    });
}
