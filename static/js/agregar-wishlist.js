// Función para agregar un producto a la lista de deseos
function addToWishlist(product) {
    // Aquí necesitas escribir el código para agregar el producto a la lista de deseos
    // Esto dependerá de cómo estés almacenando la lista de deseos
    // Por ejemplo, si estás almacenando la lista de deseos en localStorage, podrías hacer algo como esto:
    let wishlist = JSON.parse(localStorage.getItem('wishlist')) || [];
    wishlist.push(product);
    localStorage.setItem('wishlist', JSON.stringify(wishlist));

    // Crea un nuevo elemento de tarjeta para el producto
    let card = document.createElement('div');
    card.className = 'col-sm-3';
    card.innerHTML = `
        <div class="card">
            <img src="${product.image}" class="card-img-top" alt="${product.name}">
            <div class="card-body">
                <h5 class="card-title">${product.name}</h5>
                <p class="card-text">${product.price}</p>
            </div>
        </div>
    `;

    // Añade la tarjeta a la página de la lista de deseos
    let wishlistContainer = document.querySelector('#wishlist .row');
    wishlistContainer.appendChild(card);
}