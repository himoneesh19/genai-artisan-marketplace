// Basic JavaScript for Artisan AI Platform

document.addEventListener('DOMContentLoaded', function() {
    // Add any interactive functionality here

    // Example: Confirm logout
    const logoutLinks = document.querySelectorAll('a[href*="logout"]');
    logoutLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to logout?')) {
                e.preventDefault();
            }
        });
    });

    // Add more interactive features as needed
});
