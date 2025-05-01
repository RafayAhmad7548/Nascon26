document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            menuToggle.classList.toggle('active');
        });
    }

    const roleSelect = document.getElementById('id_role');
    if (roleSelect) {
        const urlParams = new URLSearchParams(window.location.search);
        const role = urlParams.get('role');
        if (role) {
            // Find and select the option with the matching value
            for (let option of roleSelect.options) {
                if (option.value === role) {
                    option.selected = true;
                    break;
                }
            }
        }
    }
    
});

