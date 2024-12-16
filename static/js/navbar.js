// Selecciona el menú desplegable de "Hombre"
let dropdownHombre = document.querySelector('#dropdownHombre');

// Crea las categorías y subcategorías
let categorias = {
    'Ropa': ['Camisetas', 'Camisas', 'Polos', 'Pantalones', 'Jeans', 'Shorts', 'Trajes', 'Chaquetas', 'Sudaderas', 'Ropa interior', 'Ropa deportiva'],
    'Calzado': ['Zapatillas', 'Zapatos formales', 'Botas', 'Sandalias'],
    'Accesorios': ['Gorras y sombreros', 'Bufandas', 'Corbatas y pajaritas', 'Cinturones', 'Relojes', 'Gafas de sol', 'Bolsos y mochilas']
};

// Itera sobre las categorías y subcategorías
for (let categoria in categorias) {
    // Crea un nuevo div para la categoría
    let divCategoria = document.createElement('div');
    divCategoria.innerHTML = `<div class="dropdown-header">${categoria}</div>`;

    // Itera sobre las subcategorías
    categorias[categoria].forEach(subcategoria => {
        // Crea un nuevo elemento a para la subcategoría
        let aSubcategoria = document.createElement('a');
        aSubcategoria.className = 'dropdown-item';
        aSubcategoria.href = '#';
        aSubcategoria.textContent = subcategoria;

        // Añade la subcategoría a la categoría
        divCategoria.appendChild(aSubcategoria);
    });

    // Añade la categoría al menú desplegable
    dropdownHombre.appendChild(divCategoria);
}