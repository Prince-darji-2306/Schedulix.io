// Mobile Navigation Toggle
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.getElementById('hamburger');
    const navLinks = document.getElementById('navLinks');
    
    if (hamburger && navLinks) {
        hamburger.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            hamburger.classList.toggle('active');
        });
        
        // Close navigation when clicking on a link
        const navLinksItems = navLinks.querySelectorAll('a');
        navLinksItems.forEach(link => {
            link.addEventListener('click', function() {
                navLinks.classList.remove('active');
                hamburger.classList.remove('active');
            });
        });
        
        // Close navigation when clicking outside
        document.addEventListener('click', function(event) {
            const isClickInsideNav = navLinks.contains(event.target) || hamburger.contains(event.target);
            if (!isClickInsideNav && navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
                hamburger.classList.remove('active');
            }
        });
        
        // Close navigation when window is resized to desktop
        window.addEventListener('resize', function() {
            if (window.innerWidth >= 769) {
                navLinks.classList.remove('active');
                hamburger.classList.remove('active');
            }
        });
    }
});

// Modal functionality for tasks page
if (typeof window !== 'undefined') {
    // Close modal function
    window.closeModal = function() {
        const modal = document.getElementById('planModal');
        if (modal) {
            modal.style.display = 'none';
        }
    };
    
    // Approve plan function
    window.approveCurrentPlan = function() {
        // This will be implemented based on your backend logic
        alert('Plan approved! This would typically send data to your backend.');
        window.closeModal();
    };
}