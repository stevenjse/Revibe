$(document).ready(function () {
    $('#forgotPasswordForm').on('submit', function (e) {
        e.preventDefault();  // Evita el envío normal del formulario

        var correo = $('#email').val();

        console.log(correo);

        $.ajax({
            url: '/password-reset',  // La ruta en tu servidor que maneja el inicio de sesión
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                correo: correo
            }),
            success: function (response) {
                // Mostrar mensaje de éxito y limpiar el formulario si es necesario
                showToast('success', response.message);
                $('#forgotPasswordForm')[0].reset(); // Opcional: limpiar el formulario
            
                //Esperar 2 segundos y redirigir a la página de inicio de sesión
                setTimeout(function () {
                    window.location.href = '/login'; // Redirige a la página de inicio de sesión
                }, 2000);
            },
            error: function (response) {
                let errorMessage = response.responseJSON.error;
                showToast('danger', errorMessage);
                $('#email').focus();
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
        $('#toastContainer2').html(toastHtml);

        // Mostrar el toast y ocultarlo después de un tiempo
        let toastElement = $('#toastContainer2 .toast')[0];
        let toast = new bootstrap.Toast(toastElement, { delay: 3000 }); // 3 segundos
        toast.show();

        // Ocultar el toast después de 3 segundos
        setTimeout(() => {
            $(toastElement).remove();
        }, 5000);
    }

});