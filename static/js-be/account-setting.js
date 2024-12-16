$(document).ready(function () {
    const form = document.getElementById('account-settings-form');

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        let formData = new FormData(form);
        formData.append('fotoPerfil', document.getElementById('imageUploadSetting').files[0]);

        $.ajax({
            url: '/update_account',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                showToast('success', response.message);

                // Vaciar los campos del formulario y establecer los nuevos datos como placeholder
                document.getElementById('nombre').value = '';
                document.getElementById('nombre').placeholder = response.userData.nombre || 'Nombre';
                document.getElementById('apellido').value = '';
                document.getElementById('apellido').placeholder = response.userData.apellido || 'Apellido';
                document.getElementById('correo').value = '';
                document.getElementById('correo').placeholder = response.userData.correo || 'Correo';
                document.getElementById('telefono').value = '';
                document.getElementById('telefono').placeholder = response.userData.telefono || 'Teléfono';
                document.getElementById('acercaDe').value = '';
                document.getElementById('acercaDe').placeholder = response.userData.acercaDe || 'Acerca de';


                // Actualizar la imagen de perfil, si se ha proporcionado una nueva
                if (response.userData.fotoPerfil) {
                    document.getElementById('imagenUsuarioConfiguracion').src = 'static/uploads/' + response.userData.fotoPerfil;
                }
            },
            error: function(xhr) {
                let errorMessage = xhr.responseJSON.error;  // Cambié 'response' por 'xhr'
                showToast('danger', errorMessage);
            }
        });
    });

    document.getElementById('imageUploadSetting').addEventListener('change', function (event) {
        var file = event.target.files[0];
        var imageUrl = URL.createObjectURL(file);
        document.getElementById('imagenUsuarioConfiguracion').src = imageUrl;
    });

    document.querySelectorAll('.verContraseña').forEach(function (button) {
        button.addEventListener('click', function () {
            var input = button.previousElementSibling;
            var img = button.querySelector('img');
            if (input.type === 'password') {
                input.type = 'text';
                img.src = '../static/assets/img/account-setting/ocultar-contrasena.svg';
            } else {
                input.type = 'password';
                img.src = '../static/assets/img/account-setting/ver-contraseña.svg';
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

document.addEventListener('DOMContentLoaded', function () {
    const direccionSeleccionada = document.getElementById('direccionSeleccionada');
    const nombreF = document.getElementById('nombreF');
    const apellidoF = document.getElementById('apellidoF');
    const empresa = document.getElementById('empresa');
    const direccion = document.getElementById('direccion');
    const pais = document.getElementById('pais');
    const estado = document.getElementById('estado');
    const codigoPostal = document.getElementById('codigoPostal');
    const emailF = document.getElementById('emailF');
    const telefonoF = document.getElementById('telefonoF');
    const direccionFormFields = document.getElementById('direccionFormFields');
    const btnAgregarDireccion = document.getElementById('btnAgregarDireccion');
    const btnCancelar = document.getElementById('btnCancelarDf');
    const btnGuardar = document.getElementById('btnGuardarDf');
    const btnEditar = document.getElementById('btnEditarDf');
    const btnEliminar = document.getElementById('btnEliminarDf');
    
    function habilitarCampos(habilitar) {
        nombreF.disabled = !habilitar;
        apellidoF.disabled = !habilitar;
        empresa.disabled = !habilitar;
        direccion.disabled = !habilitar;
        pais.disabled = !habilitar;
        estado.disabled = !habilitar;
        codigoPostal.disabled = !habilitar;
        emailF.disabled = !habilitar;
        telefonoF.disabled = !habilitar;
    }

    direccionSeleccionada.addEventListener('change', function () {
        const selectedOption = direccionSeleccionada.options[direccionSeleccionada.selectedIndex];
        
        if (selectedOption.value) {
            direccionFormFields.style.display = 'block';
            btnAgregarDireccion.style.display = 'none';
            btnGuardar.style.display = 'none';
            btnEditar.style.display = 'block';
            btnEliminar.style.display = 'block';
            habilitarCampos(false);
            nombreF.value = selectedOption.getAttribute('data-nombre');
            apellidoF.value = selectedOption.getAttribute('data-apellido');
            empresa.value = selectedOption.getAttribute('data-empresa');
            direccion.value = selectedOption.getAttribute('data-direccion');
            pais.value = selectedOption.getAttribute('data-pais');
            estado.value = selectedOption.getAttribute('data-ciudad');
            codigoPostal.value = selectedOption.getAttribute('data-codigo_postal');
            emailF.value = selectedOption.getAttribute('data-email');
            telefonoF.value = selectedOption.getAttribute('data-telefono');
        } else {
            direccionFormFields.style.display = 'none';
            btnAgregarDireccion.style.display = 'block';
        }
    });

    btnAgregarDireccion.addEventListener('click', function () {
        direccionFormFields.style.display = 'block';
        btnAgregarDireccion.style.display = 'none';
        btnGuardar.style.display = 'block';
        btnEditar.style.display = 'none';
        btnEliminar.style.display = 'none';
        habilitarCampos(true);
        direccionSeleccionada.value = '';  // Asegúrate de que el valor esté vacío
        nombreF.value = '';
        apellidoF.value = '';
        empresa.value = '';
        direccion.value = '';
        pais.value = '';
        estado.value = '';
        codigoPostal.value = '';
        emailF.value = '';
        telefonoF.value = '';
    });

    btnCancelar.addEventListener('click', function () {
        direccionFormFields.style.display = 'none';
        btnAgregarDireccion.style.display = 'block';
        btnGuardar.style.display = 'none';
        btnEditar.style.display = 'none';
        btnEliminar.style.display = 'none';
        habilitarCampos(false);
        direccionSeleccionada.value = '';
    });

    btnEditar.addEventListener('click', function () {
        habilitarCampos(true);
        btnGuardar.style.display = 'block';
        btnEditar.style.display = 'none';
    });

    btnEliminar.addEventListener('click', function () {
        Swal.fire({
            title: '¿Estás seguro?',
            text: "¡No podrás revertir esto!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sí, eliminarlo',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                const direccionId = direccionSeleccionada.value;
                fetch(`/direcciones-facturacion/${direccionId}`, {
                    method: 'DELETE'
                }).then(response => {
                    if (response.ok) {
                        direccionSeleccionada.options[direccionSeleccionada.selectedIndex].remove();
                        direccionFormFields.style.display = 'none';
                        btnAgregarDireccion.style.display = 'block';
                        btnGuardar.style.display = 'none';
                        btnEditar.style.display = 'none';
                        btnEliminar.style.display = 'none';
                        Swal.fire(
                            'Eliminado',
                            'La dirección ha sido eliminada.',
                            'success'
                        )
                    } else {
                        Swal.fire(
                            'Error',
                            'No se pudo eliminar la dirección.',
                            'error'
                        )
                    }
                });
            }
        });
    });
});

///////////////////////////////////////////////////////////
document.addEventListener('DOMContentLoaded', function () {
    const direccionSeleccionadaE = document.getElementById('direccionSeleccionadaEnvio');
    const nombreE = document.getElementById('nombreEnvio');
    const apellidoE = document.getElementById('apellidoEnvio');
    const empresaE = document.getElementById('lugarEnvio');
    const direccionE = document.getElementById('direccionEnvio');
    const paisE = document.getElementById('paisEnvio');
    const ciudadE = document.getElementById('ciudadEnvio');
    const codigoPostalE = document.getElementById('zipEnvio');
    const emailE = document.getElementById('emailEnvio');
    // const prefijoCelularE = document.getElementById('prefijoCelular');
    const telefonoE = document.getElementById('celularEnvio');
    const direccionFormFieldsE = document.getElementById('direccionEnvioFormFields');
    const btnAgregarDE = document.getElementById('btnAgregarDE');
    const btnCancelarE = document.getElementById('btnCancelarDE');
    const btnGuardarE = document.getElementById('btnGuardarDE');
    const btnEditarE = document.getElementById('btnEditarDE');
    const btnEliminarE = document.getElementById('btnEliminarDE');
    
    function habilitarCamposE(habilitar) {
        nombreE.disabled = !habilitar;
        apellidoE.disabled = !habilitar;
        empresaE.disabled = !habilitar;
        direccionE.disabled = !habilitar;
        paisE.disabled = !habilitar;
        ciudadE.disabled = !habilitar;
        codigoPostalE.disabled = !habilitar;
        emailE.disabled = !habilitar;
        // prefijoCelularE.disabled = !habilitar;
        telefonoE.disabled = !habilitar;
    }

    direccionSeleccionadaE.addEventListener('change', function () {
        const selectedOptionE = direccionSeleccionadaE.options[direccionSeleccionadaE.selectedIndex];
        
        if (selectedOptionE.value) {
            direccionFormFieldsE.style.display = 'block';
            btnAgregarDE.style.display = 'none';
            btnGuardarE.style.display = 'none';
            btnEditarE.style.display = 'block';
            btnEliminarE.style.display = 'block';
            habilitarCamposE(false);
            nombreE.value = selectedOptionE.getAttribute('data-nombreE');
            apellidoE.value = selectedOptionE.getAttribute('data-apellidoE');
            empresaE.value = selectedOptionE.getAttribute('data-lugarE');
            direccionE.value = selectedOptionE.getAttribute('data-direccionE');
            paisE.value = selectedOptionE.getAttribute('data-paisE');
            ciudadE.value = selectedOptionE.getAttribute('data-ciudadE');
            codigoPostalE.value = selectedOptionE.getAttribute('data-codigo_postalE');
            emailE.value = selectedOptionE.getAttribute('data-emailE');
            // prefijoCelularE.value = selectedOptionE.getAttribute('data-prefijoE');
            telefonoE.value = selectedOptionE.getAttribute('data-telefonoE');
        } else {
            direccionFormFieldsE.style.display = 'none';
            btnAgregarDE.style.display = 'block';
        }
    });

    btnAgregarDE.addEventListener('click', function () {
        direccionFormFieldsE.style.display = 'block';
        btnAgregarDE.style.display = 'none';
        btnGuardarE.style.display = 'block';
        btnEditarE.style.display = 'none';
        btnEliminarE.style.display = 'none';
        habilitarCamposE(true);
        direccionSeleccionadaE.value = '';  // Asegúrate de que el valor esté vacío
        nombreE.value = '';
        apellidoE.value = '';
        empresaE.value = '';
        direccionE.value = '';
        paisE.value = '';
        ciudadE.value = '';
        codigoPostalE.value = '';
        emailE.value = '';
        // prefijoCelularE.value = '+593';
        telefonoE.value = '';
    });

    btnCancelarE.addEventListener('click', function () {
        direccionFormFieldsE.style.display = 'none';
        btnAgregarDE.style.display = 'block';
        btnGuardarE.style.display = 'none';
        btnEditarE.style.display = 'none';
        btnEliminarE.style.display = 'none';
        habilitarCamposE(false);
        direccionSeleccionadaE.value = '';
    });

    btnEditarE.addEventListener('click', function () {
        habilitarCamposE(true);
        btnGuardarE.style.display = 'block';
        btnEditarE.style.display = 'none';
    });

    btnEliminarE.addEventListener('click', function () {
        Swal.fire({
            title: '¿Estás seguro?',
            text: "¡No podrás revertir esto!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sí, eliminarlo',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                const direccionId = direccionSeleccionadaE.value;
                fetch(`/direcciones-envio/${direccionId}`, {
                    method: 'DELETE'
                }).then(response => {
                    if (response.ok) {
                        direccionSeleccionadaE.options[direccionSeleccionadaE.selectedIndex].remove();
                        direccionFormFieldsE.style.display = 'none';
                        btnAgregarDE.style.display = 'block';
                        btnGuardarE.style.display = 'none';
                        btnEditarE.style.display = 'none';
                        btnEliminarE.style.display = 'none';
                        Swal.fire(
                            'Eliminado',
                            'La dirección ha sido eliminada.',
                            'success'
                        )
                    } else {
                        Swal.fire(
                            'Error',
                            'No se pudo eliminar la dirección.',
                            'error'
                        )
                    }
                });
            }
        });
    });
});


// Cambio de Contraseña
$(document).ready(function () {
    $('#changePasswordForm').on('submit', function (e) {
        e.preventDefault();  // Evita el envío normal del formulario

        var currentPassword = $('#currentPassword').val();
        var newPassword = $('#newPassword').val();
        var confirmPassword = $('#confirmPassword').val();

        console.log(currentPassword, newPassword, confirmPassword);

        $.ajax({
            url: '/change-password',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                currentpassword: currentPassword,
                newpassword: newPassword,
                confirmpassword: confirmPassword,
            }),
            success: function (response) {
                showToast('success', response.message);
                $('#changePasswordForm')[0].reset(); // Opcional: limpiar el formulario
            },
            error: function (response) {
                let errorMessage = response.responseJSON.error;
                showToast('danger', errorMessage);
                $('#currentPassword').focus();

                // Enfocar el campo relevante
                if (errorMessage.includes('contraseña actual')) {
                    $('#currentPassword').focus();
                } else if (errorMessage.includes('contraseñas no coinciden')) {
                    $('#newPassword').focus();
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