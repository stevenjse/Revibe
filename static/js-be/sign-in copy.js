document.addEventListener('DOMContentLoaded', function () {
    const registerForm = document.getElementById('registerForm');
    const signUpUrl = registerForm.getAttribute('data-signup-url');
    const loginUrl = registerForm.getAttribute('data-login-url');

    registerForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Evitar el envío del formulario por defecto

        // Recoger los datos del formulario
        const formData = new FormData(this);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });
        
        console.log(data);
        console.log(signUpUrl);

        // Enviar los datos usando fetch
        fetch(signUpUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)

        })
        .then(response => {
            if (!response.ok) {

                //console.log(JSON.stringify(data));

                throw new Error('Network response was not okk');
            }
            return response.json();
        })
        .then(data => {
            const errorMessage = document.getElementById('error-message');
            if (data.error) {
                errorMessage.textContent = data.error;
                errorMessage.style.display = 'block';
            } else {
                alert(data.success);
                window.location.href = loginUrl;
            }
        })
        .catch(error => {

            //console.log(JSON.stringify(data));

            console.error('Error:', error);
            const errorMessage = document.getElementById('error-message');
            errorMessage.textContent = 'Ocurrió un error al registrarse. Por favor, inténtelo de nuevo.';
            errorMessage.style.display = 'block';
        });
    });
});
