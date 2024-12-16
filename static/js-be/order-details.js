document.addEventListener('DOMContentLoaded', function () {
    const recibidoButton = document.getElementById('recibido');
    const devolverButton = document.getElementById('devolver');

    if (recibidoButton){
        recibidoButton.addEventListener('click', function (event) {
            event.preventDefault();
            const pedidoId = this.dataset.pedidoId;

            fetch('/pedido_recibido', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 'pedido_id': pedidoId })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        recibidoButton.disabled = true;
                        showToast('success', data.message);
                    } else {
                        showToast('danger', data.message);
                    }
                })
                .catch(error => showToast('danger', 'Error: ' + error.message));
        });
    }

    if (devolverButton) {
        devolverButton.addEventListener('click', function (event) {
            event.preventDefault();
            const pedidoId = this.dataset.pedidoId;

            fetch('/pedido_devuelto', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 'pedido_id': pedidoId })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        devolverButton.disabled = true;
                        showToast('success', data.message);
                    } else {
                        showToast('danger', data.message);
                    }
                })
                .catch(error => showToast('danger', 'Error: ' + error.message));
        });
    }

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
