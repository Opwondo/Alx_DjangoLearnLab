// Basic example script to demonstrate dynamic behavior
document.addEventListener('DOMContentLoaded', function() {
    console.log('Blog page loaded');
    
    // ========== FOOTER POSITIONING - BEGIN ==========
    // Ensure footer stays at bottom even if content is short
    function adjustFooter() {
        const body = document.body;
        const html = document.documentElement;
        const content = document.querySelector('.content');
        const footer = document.querySelector('footer');
        
        // Get heights
        const contentHeight = content.offsetHeight;
        const footerHeight = footer.offsetHeight;
        const windowHeight = window.innerHeight;
        
        // Calculate minimum content height to push footer to bottom
        const minContentHeight = windowHeight - footerHeight - 100; // 100px for header
        
        if (contentHeight < minContentHeight) {
            content.style.minHeight = minContentHeight + 'px';
        }
    }
    
    // Run on load and resize
    adjustFooter();
    window.addEventListener('resize', adjustFooter);
    // ========== FOOTER POSITIONING - END ==========
});
