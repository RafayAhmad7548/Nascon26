// Global JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    // Sticky header effect on scroll
    const header = document.querySelector('.site-header');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });
});