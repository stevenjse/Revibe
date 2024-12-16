document.addEventListener('DOMContentLoaded', function() {
    const thumbnails = document.querySelectorAll('.thumbnail img');
    const mainImage = document.getElementById('mainImage');

    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('click', function() {
            // Remove 'active' class from all thumbnails
            thumbnails.forEach(img => img.classList.remove('active'));

            // Add 'active' class to the clicked thumbnail
            thumbnail.classList.add('active');

            // Change the main image to the clicked thumbnail's source
            mainImage.src = thumbnail.src;
        });
    });

    const enviarProductoBtn = document.getElementById('enviarProducto');

    enviarProductoBtn.addEventListener('click', function() {
        const pedidoId = enviarProductoBtn.dataset.pedidoId; // Asegúrate de tener el ID del producto en un atributo data-product-id

        fetch('/enviar_producto', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'pedido_id': pedidoId })
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    enviarProductoBtn.disabled = true; // Deshabilitar el botón después de enviar el producto

                    // Mostrar el toast
                    showToast('success', data.message);
                } else {
                    showToast('success', data.message);
                }
            })
            .catch(error => console.error('Error:', error));
    });

    function showToast(type, message) {
        let toastHtml = `
    <div class="toast bg-${type} text-white" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="toast-body">
            ${message}
        </div>
    </div>
`;
        $('#toastContainer').html(toastHtml);

        // Mostrar el toast y ocultarlo después de un tiempo
        let toastElement = $('#toastContainer .toast')[0];
        let toast = new bootstrap.Toast(toastElement, {delay: 3000}); // 3 segundos
        toast.show();

        // Desplazar la vista hacia el toast
        toastElement.scrollIntoView({behavior: 'smooth', block: 'center'});

        // Ocultar el toast después de 3 segundos
        setTimeout(() => {
            $(toastElement).remove();
        }, 5000);
    }
});