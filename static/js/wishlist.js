function initializeWishlistButtons() {
    const wishlistButtons = document.querySelectorAll('.wishlist-btn');

    wishlistButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            const productId = this.dataset.productId;

            fetch('/toggle_wishlist', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 'product_id': productId })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'added') {
                        this.querySelector('i').classList.remove('text-muted');
                        this.querySelector('i').classList.add('text-danger');
                    } else if (data.status === 'removed') {
                        this.querySelector('i').classList.remove('text-danger');
                        this.querySelector('i').classList.add('text-muted');
                    }
                })
                .catch(error => console.error('Error:', error));
        });
    });
}

document.addEventListener('DOMContentLoaded', function () {
    initializeWishlistButtons();
});
