document.addEventListener("DOMContentLoaded", function () {
    // Dropdowns: al pasar el mouse se muestr el contenido
    const dropdowns = document.querySelectorAll(".dropdown");

    dropdowns.forEach(function (dropdown) {
        dropdown.addEventListener("mouseenter", function () {
            const dropdownMenu = this.querySelector('.dropdown-menu');
            if (dropdownMenu) {
                dropdownMenu.classList.add('show');
            }
            this.classList.add('show');
        });

        dropdown.addEventListener("mouseleave", function () {
            const dropdownMenu = this.querySelector('.dropdown-menu');
            if (dropdownMenu) {
                dropdownMenu.classList.remove('show');
            }
            this.classList.remove('show');
        });
    });
//     Fin Dropdowns

    var myCarousel = document.getElementById('carouselExampleIndicators')
    var carousel = new bootstrap.Carousel(myCarousel, {
        interval: 2000, // Cambia el valor para ajustar la velocidad del carrusel en milisegundos
        wrap: true // Cambia a false si no deseas que el carrusel vuelva al principio cuando llegue al último elemento
    })
    var myTestimonialCarousel = document.getElementById('testimonialCarousel')
    var testimonialCarousel = new bootstrap.Carousel(myTestimonialCarousel, {
        interval: 5000, // Cambia el valor para ajustar la velocidad del carrusel en milisegundos
        wrap: true // Cambia a false si no deseas que el carrusel vuelva al principio cuando llegue al último elemento
    })
});
// Inicio Carrusel
// $('.carousel').carousel({
//     interval: 2000
// })
/* Inicio Corazones rojos*/
document.querySelectorAll('.heart-icon').forEach(function (heartIcon) {
    heartIcon.addEventListener('click', function (event) {
        event.preventDefault();
        this.classList.toggle('filled');
    });
});
/* Fin Corazones rojos*/

// //Fin Carrusel

//FIN CHONY NEW-ARTICLE
// Controlador categorias

/*Inicio chat*/
function selectUser(userId) {
    // Clear existing messages
    const messageContainer = document.getElementById('message-container');
    messageContainer.innerHTML = '';

    // Update the contact name
    const contactNameElement = document.getElementById('contact-name');
    contactNameElement.style.display = 'block';
    if (userId === 'user1') {
        contactNameElement.textContent = 'User 1';
    } else if (userId === 'user2') {
        contactNameElement.textContent = 'User 2';
    }

    // Add the input container to the message container
    const inputContainer = document.querySelector('.input-container');
    inputContainer.style.display = 'block';

    // Dummy messages for demonstration
    let messages = [];

    if (userId === 'user1') {
        messages = [
            {sender: 'User 1', message: '¡Hola! ¿Cómo estás?', time: '10:00 AM'},
            {sender: 'Yo', message: '¡Hola! Estoy bien, ¿y tú?', time: '10:01 AM'},
            {sender: 'Yo', message: '¡Hola! Estoy bien, ¿y tú?', time: '10:01 AM'},
            {sender: 'Yo', message: '¡Hola! Estoy bien, ¿y tú?', time: '10:01 AM'},
            {sender: 'Yo', message: '¡Hola! Estoy bien, ¿y tú?', time: '10:01 AM'},
            {sender: 'Yo', message: '¡Hola! Estoy bien, ¿y tú?', time: '10:01 AM'},
            {sender: 'Yo', message: '¡Hola! Estoy bien, ¿y tú?', time: '10:01 AM'},
            {sender: 'Yo', message: '¡Hola! Estoy bien, ¿y tú?', time: '10:01 AM'},
            {sender: 'Yo', message: '¡Hola! Estoy bien, ¿y tú?', time: '10:01 AM'},
            {sender: 'Yo', message: '¡Hola! Estoy bien, ¿y tú?', time: '10:01 AM'},
            {sender: 'Yo', message: '¡Hola! Estoy bien, ¿y tú?', time: '10:01 AM'},
            {sender: 'Yo', message: '¡Hola! Estoy bien, ¿y tú?', time: '10:01 AM'},
            {sender: 'Yo', message: '¡Hola! Estoy bien, ¿y tú?', time: '10:01 AM'},
            {sender: 'Yo', message: '¡Hola! Estoy bien, ¿y tú?', time: '10:01 AM'},
            {sender: 'Yo', message: '¡Hola! Estoy bien, ¿y tú?', time: '10:01 AM'},
            {sender: 'Yo', message: '¡Hola! Estoy bien, ¿y tú?', time: '10:01 AM'},
            {sender: 'Yo', message: '¡Hola! Estoy bien, ¿y tú?', time: '10:01 AM'},
            {sender: 'Yo', message: '¡Hola! Estoy bien, ¿y tú?', time: '10:01 AM'},
            {sender: 'Yo', message: '¡Hola! Estoy bien, ¿y tú?', time: '10:01 AM'}
        ];
    } else if (userId === 'user2') {
        messages = [
            {sender: 'User 2', message: '¡Hola! ¿Qué tal?', time: '10:05 AM'},
            {sender: 'Yo', message: '¡Hola! Todo bien por aquí.', time: '10:06 AM'}
        ];
    }

    // Add messages to the message container
    messages.forEach(message => {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        if (message.sender === 'Yo') {
            messageElement.classList.add('sent');
        } else {
            messageElement.classList.add('received');
        }
        messageElement.innerHTML = `
        <span class="sender">${message.sender}</span>
        <span class="time">${message.time}</span>
        <p>${message.message}</p>
    `;
        messageContainer.appendChild(messageElement);
    });

    messageContainer.scrollTop = messageContainer.scrollHeight;


    // Show the input container when a user is selected
    inputContainer.style.display = 'block';

    // Update active user in the user list
    const userList = document.getElementsByClassName('user');
    for (let i = 0; i < userList.length; i++) {
        userList[i].classList.remove('active');
    }
    document.querySelector(`#user-list .user[data-user="${userId}"]`).classList.add('active');
}

/*Fin chat*/

// Obtén todas las imágenes
var images = document.querySelectorAll('.product-image');

// Agrega un controlador de eventos de clic a cada imagen
images.forEach(function (img) {
    img.addEventListener('click', function () {
        // Cambia el fondo de zoomImage a la imagen en la que se hizo clic
        document.getElementById('zoomImage').style.backgroundImage = 'url(' + this.src + ')';
    });
});
/*fin zoom imagen*/

/*Inicio sign-in */

// Toogle Password
function togglePasswordVisibility() {
    var passwordField = document.getElementById("password");
    var toggleButton = document.getElementById("togglePassword");
    var toggleIcon = toggleButton.querySelector('i');

    if (passwordField.type === "password") {
        passwordField.type = "text";
        toggleIcon.classList.remove('fa-eye');
        toggleIcon.classList.add('fa-eye-slash');
    } else {
        passwordField.type = "password";
        toggleIcon.classList.remove('fa-eye-slash');
        toggleIcon.classList.add('fa-eye');
    }
}

function togglePasswordConfirmationVisibility() {
    var passwordFieldConf = document.getElementById("passwordConfirm");
    var toggleButtonConf = document.getElementById("togglePasswordConfirm");
    var toggleIconConf = toggleButtonConf.querySelector('i');

    if (passwordFieldConf.type === "password") {
        passwordFieldConf.type = "text";
        toggleIconConf.classList.remove('fa-eye');
        toggleIconConf.classList.add('fa-eye-slash');
    } else {
        passwordFieldConf.type = "password";
        toggleIconConf.classList.remove('fa-eye-slash');
        toggleIconConf.classList.add('fa-eye');
    }
}

// Fin Toogle Password
/*Fin sign-in */

/*Selecionar marca*/

function checkOther(select) {
    var otherBrandInput = document.getElementById('otherBrand');
    if (select.value === 'other') {
        otherBrandInput.style.display = 'block';
    } else {
        otherBrandInput.style.display = 'none';
    }
}
/*Fin seleccionar marca*/