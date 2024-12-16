$(document).ready(function () {
    $('#loginForm').on('submit', function (e) {
        e.preventDefault();  // Evita el envío normal del formulario

        var correo = $('#correo').val();
        var password = $('#password').val();

        const urlParams = new URLSearchParams(window.location.search);
        const nextUrl = urlParams.get('next');

        $.ajax({
            url: '/login',  // La ruta en tu servidor que maneja el inicio de sesión
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                correo: correo,
                password: password,
                next: nextUrl
            }),
            success: function (response) {
                // Mostrar mensaje de éxito y limpiar el formulario si es necesario
                showToast('success', response.message);
                $('#loginForm')[0].reset(); // Opcional: limpiar el formulario

                setTimeout(function () {
                    window.location.href = response.next;
                }, 2000);
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