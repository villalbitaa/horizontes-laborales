document.addEventListener('DOMContentLoaded', () => {
    inicializarMenu();
});

function inicializarMenu() {
    const menuItems = document.querySelectorAll('.menu-item');
    
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            menuItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
            
            const menuText = this.querySelector('span').textContent;
            const pageTitle = document.querySelector('.page-title');
            if (pageTitle) {
                pageTitle.textContent = menuText;
            }
            
            if (this.id === 'menu-horizontes') {
                window.location.href = '/horizontes';
            }
            if (this.id === 'menu-institucion') {
                window.location.href = '/institucion';
            }
        });
    });
}
