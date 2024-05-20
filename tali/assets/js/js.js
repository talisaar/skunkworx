function check() {
    var input = document.getElementById('password_confirm');
    if (input.value != document.getElementById('password').value) {
        input.setCustomValidity('Passwords do not match.');
    } else {
        // input is valid -- reset the error message
        input.setCustomValidity('');
    }
}
