/* Event Subscription: Check menu format everytime window is resized */
window.addEventListener('resize', isOverflown, false)

/* Toggle responsive styling as necessary */
function isOverflown() {
    var menu = document.getElementById("nav-menu");
    var overflown = menu.scrollHeight > menu.clientHeight || menu.scrollWidth > menu.clientWidth;
    
    overflown?
        menu.classList.add("nav-responsive"):
        menu.classList.remove("nav-responsive");

    return overflown;
}