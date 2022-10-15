/* Toggle responsive styling */
window.addEventListener('resize', function isOverflown() {
    var menu = document.getElementById("nav-menu");
    var overflown = menu.scrollHeight > menu.clientHeight || menu.scrollWidth > menu.clientWidth;
    
    // If default className only, apply responsive class
    overflown?
        menu.classList.add("nav-responsive"):
        menu.classList.remove("nav-responsive");
    
    return overflown;
})