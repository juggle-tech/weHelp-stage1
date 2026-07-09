const hamMenu = document.getElementById('hamMenu');
const menu = document.getElementById('menu');
const overlay = document.getElementById('overlay');
const closeBtn = document.getElementById('closeBtn');

// Add additional attributes to menu and overlay on hamburger menu click
hamMenu.addEventListener('click', () => {
    menu.classList.add('menuOpen');
    overlay.classList.add('overlayActive');
});

// Close the popup menu by clicking the close icon
closeBtn.addEventListener('click', () => {
    menu.classList.remove('menuOpen');
    overlay.classList.remove('overlayActive');
});

