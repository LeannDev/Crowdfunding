const form = document.getElementById('form');
const inputs = document.querySelectorAll('#form input, textarea');

const expressions = {
	name: /^[a-zA-ZÀ-ÿ\s]{0,40}$/,
	email: /^$|^.*@.*\..*$/, ///^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
    donation: /^[1-9]\d*$/,
    text: /^[a-zA-Z0-9\_\-]{0,150}$/,
}

const validateInputs = (e) => {
    switch (e.target.name) {
        case 'email':
            if (expressions[e.target.name].test(e.target.value)) {
                e.target.classList.remove('is-invalid');
                e.target.classList.add('is-valid');
                document.getElementById('feedback').innerHTML = '';
            } else {
                e.target.classList.remove('is-valid');
                e.target.classList.add('is-invalid');
                document.getElementById('feedback').innerHTML = 'Invalid email';
            }
        break;
        case 'name':
            if (expressions[e.target.name].test(e.target.value)) {
                e.target.classList.remove('is-invalid');
                e.target.classList.add('is-valid');
                document.getElementById('feedback').innerHTML = '';
            } else {
                e.target.classList.remove('is-valid');
                e.target.classList.add('is-invalid');
                document.getElementById('feedback').innerHTML = 'Invalid name';
            }
        break;
        case 'donation':
            if (expressions[e.target.name].test(e.target.value)) {
                e.target.classList.remove('is-invalid');
                e.target.classList.add('is-valid');
                document.getElementById('feedback').innerHTML = '';
            } else {
                e.target.classList.remove('is-valid');
                e.target.classList.add('is-invalid');
                document.getElementById('feedback').innerHTML = 'Invalid donation';
            }
        break;
        case 'text':
            if (expressions[e.target.name].test(e.target.value)) {
                e.target.classList.remove('is-invalid');
                e.target.classList.add('is-valid');
                document.getElementById('feedback').innerHTML = '';
            } else {
                e.target.classList.remove('is-valid');
                e.target.classList.add('is-invalid');
                document.getElementById('feedback').innerHTML = 'Invalid text';
            }
        break;
    }

}

inputs.forEach((input) => {
    input.addEventListener('keyup', validateInputs);
    input.addEventListener('blur', validateInputs);
});