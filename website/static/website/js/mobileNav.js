const toggleMobileNav = document.querySelector('#toggleMobileNav');
const navBar = document.querySelector('#navBar');

toggleMobileNav.addEventListener('click', () => {
    navBar.classList.toggle('active');
});
