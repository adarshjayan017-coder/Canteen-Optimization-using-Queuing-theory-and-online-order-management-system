export function initAuthValidation() {
    const passwordInput = document.querySelector('input[name="password"]');
    if (passwordInput) {
        passwordInput.addEventListener('input', function() {
            const isInvalid = this.value.length > 0 && this.value.length < 4;
            this.classList.toggle('is-invalid', isInvalid);
            this.setCustomValidity(isInvalid ? "Too short!" : "");
        });
    }
}

export function confirmLogout(event) {
    if (!confirm("Are you sure you want to logout?")) {
        event.preventDefault();
    }
}