document.addEventListener('DOMContentLoaded', function() {
    // Select all alert messages (pop-ups)
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(function(alert) {
        // Wait 2000ms (2 seconds) then fade out
        setTimeout(function() {
            // Using Bootstrap's built-in alert close method
            let bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 2000);
    });
});