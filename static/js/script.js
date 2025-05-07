document.addEventListener('DOMContentLoaded', function() {
    // Add loading animation to scan button
    const scanButton = document.querySelector('form[action="/scan"] button[type="submit"]');
    if (scanButton) {
        scanButton.addEventListener('click', function() {
            this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Scanning...';
            this.disabled = true;
        });
    }
});
