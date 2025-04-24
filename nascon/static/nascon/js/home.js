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
    
    // Event filter functionality
    const filterButtons = document.querySelectorAll('.filter-button');
    const eventCards = document.querySelectorAll('.event-card');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const filterValue = this.getAttribute('data-filter');
            
            // Update active button
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Filter events
            eventCards.forEach(card => {
                const category = card.getAttribute('data-category');
                
                if (filterValue === 'all' || category === filterValue) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // Scroll animation
    const animateElements = document.querySelectorAll('.animate-on-scroll');
    
    const checkIfInView = () => {
        const windowHeight = window.innerHeight;
        const windowTopPosition = window.scrollY;
        const windowBottomPosition = windowTopPosition + windowHeight;
        
        animateElements.forEach(element => {
            const elementHeight = element.offsetHeight;
            const elementTopPosition = element.offsetTop;
            const elementBottomPosition = elementTopPosition + elementHeight;
            
            if (
                (elementBottomPosition >= windowTopPosition) && 
                (elementTopPosition <= windowBottomPosition)
            ) {
                element.classList.add('show');
            }
        });
    };
    
    // Check on load
    checkIfInView();
    
    // Check on scroll
    window.addEventListener('scroll', checkIfInView);
});