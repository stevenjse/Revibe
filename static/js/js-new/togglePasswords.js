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