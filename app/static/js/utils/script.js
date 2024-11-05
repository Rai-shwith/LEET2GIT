const scrollCard = (next = true) => {
    const container = document.getElementById('cardContainer');
    const cardWidth = container.querySelector('.flex-none').offsetWidth;
    if (next) {
        container.scrollBy({ left: cardWidth, behavior: 'smooth' });
    } else {
        container.scrollBy({ left: -cardWidth, behavior: 'smooth' });
    }
}

const getParent = (element, className) => {
    while (element.parentElement) {
        if (element.classList.contains(className)) {
            return element;
        }
        element = element.parentElement;
    }
    return null;
}

const makeValueNull = (element) => {
    element.value = '';
}

const showMessage = (type, message) => {
    // Select the appropriate message element
    const successMessage = document.getElementById('successMessage');
    const errorMessage = document.getElementById('errorMessage');

    // Reset styles for both messages
    successMessage.classList.add('hidden', 'opacity-0', 'translate-y-[-100%]');
    errorMessage.classList.add('hidden', 'opacity-0', 'translate-y-[-100%]');

    if (type === 'success') {
        successMessage.querySelector('span').textContent = message || 'Repo created successfully!';
        successMessage.classList.remove('hidden', 'opacity-0', 'translate-y-[-100%]');
        successMessage.classList.add('translate-y-0', 'opacity-100');
    } else if (type === 'error') {
        errorMessage.querySelector('span').textContent = message || 'Repo not found.';
        errorMessage.classList.remove('hidden', 'opacity-0', 'translate-y-[-100%]');
        errorMessage.classList.add('translate-y-0', 'opacity-100');
    }

    // Hide the message after 3 seconds
    setTimeout(() => {
        if (type === 'success') {
            successMessage.classList.remove('translate-y-0', 'opacity-100');
            successMessage.classList.add('hidden', 'opacity-0', 'translate-y-[-100%]');
        } else {
            errorMessage.classList.remove('translate-y-0', 'opacity-100');
            errorMessage.classList.add('hidden', 'opacity-0', 'translate-y-[-100%]');
            }
    }, 3000);
}

const getCookie =   (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}