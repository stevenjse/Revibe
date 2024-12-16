$(document).ready(function () {
    $('#contactForm').submit(function (event) {
        event.preventDefault();
        let formData = {
            nombre: $('#nombre').val(),
            correo: $('#correo').val(),
            telefono: $('#telefono').val(),
            asunto: $('#asunto').val(),
            mensaje: $('#mensaje').val()
        };

        $.ajax({
            type: 'POST',
            url: '/contact',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function (response) {

                // Mostrar mensaje de éxito y limpiar el formulario si es necesario
                showToast('success', response.message);
                $('#contactForm')[0].reset(); // Opcional: limpiar el formulario
            },
            error: function (response) {
                let errorMessage = response.responseJSON.error;
                showToast('danger', errorMessage);
            }
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
        let toast = new bootstrap.Toast(toastElement, { delay: 3000 }); // 3 segundos
        toast.show();

        // Ocultar el toast después de 3 segundos
        setTimeout(() => {
            $(toastElement).remove();
        }, 5000);
    }
});
