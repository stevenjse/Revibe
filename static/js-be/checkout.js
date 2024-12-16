$(document).ready(function () {
    // Configura Stripe con tu clave pública
    var stripe = Stripe('pk_test_51PfA1pCAViqZ6hFUet8QouIrtUNY6krCLUkNXxs29vJ1c6yuqFVo82WXmhttMcqg8XXH0hf3BW9ZwsgwphBHISAw005USYG2Ul');
    var elements = stripe.elements();
    document.getElementById('card-errors').style.display = 'none';

// Crea un elemento de tarjeta y agrega al formulario
    var card = elements.create('card', {hidePostalCode: true});
    card.mount('#card-element');

// Maneja los errores de validación
    card.addEventListener('change', function(event) {
        var displayError = document.getElementById('card-errors');
        if (event.error) {
            displayError.textContent = event.error.message;
            displayError.style.display = 'block'; // Hacer visible el elemento
        } else {
            displayError.textContent = '';
            displayError.style.display = 'none'; // Ocultar el elemento
        }
    });

    document.getElementById('pay-button').addEventListener('click', function (event) {

        // Verificar campos del formulario de dirección
        const addressFields = ['firstName', 'lastName', 'address', 'country', 'city', 'zip'];
        let allFieldsFilled = true;
        for (const fieldId of addressFields) {
            if (!document.getElementById(fieldId).value.trim()) {
                showToast('warning', 'Por favor, completa todos los campos de dirección.');
                allFieldsFilled = false;
                break;
            }
        }

        // Verificar campos del formulario de pago
        if (allFieldsFilled) {
            const paymentFields = ['cardName'];
            for (const fieldId of paymentFields) {
                if (!document.getElementById(fieldId).value.trim()) {
                    showToast('warning', 'Por favor, completa todos los campos de pago.');
                    allFieldsFilled = false;
                    break;
                }
            }
        }

        // Si todos los campos están llenos, enviar datos con AJAX
        if (allFieldsFilled) {
            // Crear un token de Stripe con la información de la tarjeta
            stripe.createToken(card).then(function (result) {
                if (result.error) {
                    // Informar al usuario sobre el error
                    var errorElement = document.getElementById('card-errors');
                    errorElement.textContent = result.error.message;
                } else {
                    // Enviar el token y los datos del formulario al servidor
                    stripeTokenHandler(result.token);
                }
            });
        }

        function stripeTokenHandler(token) {
            const product_id = document.getElementById('product_id').getAttribute('data-product-id');

            const data = {
                firstName: document.getElementById('firstName').value,
                lastName: document.getElementById('lastName').value,
                address: document.getElementById('address').value,
                country: document.getElementById('country').value,
                city: document.getElementById('city').value,
                zip: document.getElementById('zip').value,
                token: token.id,  // Token de Stripe
                envio: parseFloat(document.getElementById('order-shipping').value),
                total: parseFloat(document.getElementById('order-total').value),
                product_id: product_id
            };

            console.log(data['total'])
            $.ajax({
                url: '/pay',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(data),
                success: function(response) {
                    showToast('success', response.message);

                    setTimeout(() => {
                        window.location.href = '/orders';
                    }, 3000);
                },
                error: function(response) {
                    let errorMessage = response.responseJSON.message;
                    showToast('danger', errorMessage);
                }
            });
        }
    });

    document.getElementById('savedAddresses').addEventListener('change', function() {
        var selectedOption = this.options[this.selectedIndex];

        // Lista de campos del formulario de dirección
        const addressFields = ['firstName', 'lastName', 'address', 'country', 'city', 'zip'];

        addressFields.forEach(function(field) {
            var fieldValue = selectedOption.getAttribute('data-' + field);
            document.getElementById(field).value = fieldValue ? fieldValue : '';
        });
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