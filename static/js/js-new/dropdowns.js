document.addEventListener("DOMContentLoaded", function () {
    // Dropdowns: al pasar el mouse se muestr el contenido
    const dropdowns = document.querySelectorAll(".dropdown");

    dropdowns.forEach(function (dropdown) {
        dropdown.addEventListener("mouseenter", function () {
            const dropdownMenu = this.querySelector('.dropdown-menu');
            if (dropdownMenu) {
                dropdownMenu.classList.add('show');
            }
            this.classList.add('show');
        });

        dropdown.addEventListener("mouseleave", function () {
            const dropdownMenu = this.querySelector('.dropdown-menu');
            if (dropdownMenu) {
                dropdownMenu.classList.remove('show');
            }
            this.classList.remove('show');
        });
    });
//     Fin Dropdowns
});