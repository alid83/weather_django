document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault();

    document.getElementById('passwordError').innerText = '';
    document.getElementById('confirmPasswordError').innerText = '';

    var password = document.getElementById('id_password').value;
    var confirmPassword = document.getElementById('id_confirm_password').value;

    var errorMessage;

    if (password.length < 8) {
        errorMessage = 'رمز عبور باید حداقل 8 کاراکتر باشد.';
    } else if (!/\d/.test(password)) {
        errorMessage = 'رمز عبور باید حداقل شامل یک رقم باشد.';
    } else if (!/[A-Z]/.test(password)) {
        errorMessage = 'رمز عبور باید حداقل شامل یک حرف بزرگ انگلیسی باشد.';
    } else if (!/[a-z]/.test(password)) {
        errorMessage = 'رمز عبور باید حداقل شامل یک حرف کوچک انگلیسی باشد.';
    } else if (password !== confirmPassword) {
        errorMessage = 'کلمه عبور و تکرار کلمه عبور مغایرت دارند';
    }

    if (errorMessage) {
        document.getElementById('passwordError').innerText = errorMessage;
    } else {
        this.submit();
    }
});
