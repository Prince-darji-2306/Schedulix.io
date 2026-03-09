// Mobile Navigation Toggle
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.getElementById('hamburger');
    const navLinks = document.getElementById('navLinks');
    
    // Check if elements exist before adding event listeners
    if (!hamburger || !navLinks) {
        console.warn('Navigation elements not found. Hamburger menu will not work.');
        return;
    }
    
    // Initialize menu state
    let isMenuOpen = false;
    
    function toggleMenu() {
        isMenuOpen = !isMenuOpen;
        
        if (isMenuOpen) {
            navLinks.classList.add('active');
            hamburger.classList.add('active');
            document.body.style.overflow = 'hidden';
            // Add ARIA attributes for accessibility
            hamburger.setAttribute('aria-expanded', 'true');
            navLinks.setAttribute('aria-hidden', 'false');
        } else {
            navLinks.classList.remove('active');
            hamburger.classList.remove('active');
            document.body.style.overflow = '';
            // Add ARIA attributes for accessibility
            hamburger.setAttribute('aria-expanded', 'false');
            navLinks.setAttribute('aria-hidden', 'true');
        }
    }
    
    // Hamburger click handler
    hamburger.addEventListener('click', function(event) {
        event.preventDefault();
        event.stopPropagation();
        toggleMenu();
    });
    
    // Close navigation when clicking on a link
    const navLinksItems = navLinks.querySelectorAll('a');
    navLinksItems.forEach(link => {
        link.addEventListener('click', function() {
            toggleMenu();
        });
    });
    
    // Close navigation when clicking outside
    document.addEventListener('click', function(event) {
        const isClickInsideNav = navLinks.contains(event.target) || hamburger.contains(event.target);
        if (!isClickInsideNav && isMenuOpen) {
            toggleMenu();
        }
    });
    
    // Close navigation when window is resized to desktop
    window.addEventListener('resize', function() {
        if (window.innerWidth >= 769 && isMenuOpen) {
            toggleMenu();
        }
    });
    
    // Add keyboard support for accessibility
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && isMenuOpen) {
            toggleMenu();
            hamburger.focus();
        }
    });
    
    // Add touch support for mobile devices
    hamburger.addEventListener('touchstart', function(event) {
        event.preventDefault();
        toggleMenu();
    }, { passive: false });
    
    // Prevent body scroll when menu is open on touch devices
    document.addEventListener('touchmove', function(event) {
        if (isMenuOpen && !navLinks.contains(event.target) && !hamburger.contains(event.target)) {
            event.preventDefault();
        }
    }, { passive: false });
    
    console.log('Navigation system initialized successfully');
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