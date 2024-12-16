$(document).ready(function () {
    $('#registerForm').submit(function (event) {
        event.preventDefault();
        let formData = {
            nombre: $('#nombre').val(),
            apellido: $('#apellido').val(),
            correo: $('#correo').val(),
            //prefijo: $('#phonePrefix').val(),
            telefono: $('#phoneNumber').val(),
            password: $('#password').val(),
            passwordConfirmation: $('#passwordConfirm').val(),
            is_subscribed: $('#suscripcion').is(':checked')
        };

        $.ajax({
            type: 'POST',
            url: '/register',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function (response) {
                // Mostrar mensaje de éxito y limpiar el formulario si es necesario
                showToast('success', response.message);
                $('#registerForm')[0].reset(); // Opcional: limpiar el formulario
            
                // Esperar 2 segundos y redirigir a la página de inicio de sesión
                setTimeout(function () {
                    window.location.href = '/login'; // Redirige a la página de inicio de sesión
                }, 2000);
            
            },
            error: function (response) {
                let errorMessage = response.responseJSON.error;
                showToast('danger', errorMessage);
                
                // Enfocar el campo relevante
                if (errorMessage.includes('contraseñas no coinciden')) {
                    $('#password').focus();
                } else if (errorMessage.includes('correo electrónico ya está en uso')) {
                    $('#correo').focus();
                } else if (errorMessage.includes('con los requisitos')) {
                    $('#password').focus();
                }
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
