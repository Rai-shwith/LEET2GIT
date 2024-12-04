const wayChooser = document.getElementById('wayChooser');
const manual = document.getElementById('manual');
const automatic = document.getElementById('automatic');
const manualUploadBtn = document.getElementById('manualUploadBtn');
const automaticUploadBtn = document.getElementById('automaticUploadBtn');
const requestedQuestions = new Object() // To keep track of questions requested so that to stop the unneccessary requests

// Start cycling placeholders
cyclePlaceholders("search-question");


automaticUploadBtn.addEventListener('click', () => {
    loading(true); // Start the loading spinner
    const leetcodeAccess = document.getElementById('leetcode_session').value.trim();

    if (!leetcodeAccess ) {
        showMessage('error', 'Please fill the LEETCODE_SESSION ');
        loading(false);
        return;
    }

    const data = {
        leetcode_access_token: leetcodeAccess,
    };

    fetch(`/upload/automatic`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        loading(false);

        if (response.status === 201) {
            showMessage('success', 'Code uploaded successfully! Check your GitHub repository.');
        } else if (response.status === 401) {
            showMessage('error', 'Invalid credentials! Please check LEETCODE_SESSION token.');
        } else {
            showMessage('error', 'Something went wrong! Please try again.');
        }

        return response.json(); // Parse the response if needed
    })
    .then(data => {
        console.log('Response data:', data); // Optional debugging
    })
    .catch(error => {
        loading(false);
        console.error('Error:', error);
        showMessage('error', 'A network error occurred. Please try again later.');
    });
});


manualUploadBtn.addEventListener('click', () => {
    loading();
    const cardContainer = document.getElementById('cardContainer');
    const cards = cardContainer.querySelectorAll('.card');
    const uploadData = { uploads: [] };

    for (let index = 0; index < cards.length; index++) {
        const card = cards[index];
        
        const info = card.querySelector('.info');
        if (info == null && index == 0) {
            showMessage('error', 'Please search for a question first!');
            loading(false);
            return
        }
        const code = card.querySelector('textarea').value;
        const code_extension = card.querySelector('select').value;
        if ((code == "" || code_extension == "") && index == 0) {
            showMessage('error', 'Please fill the solution and language first!');
            loading(false);
            return
        }
        if (code == "" || code_extension == "") {
            continue;
        }
        const question = JSON.parse(info.textContent);
        upload = { question, solution: { code_extension, code } };
        uploadData.uploads.push(upload);
    }
    
    fetch(`/upload/manual`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(uploadData) // Ensure uploadData is properly structured as an object
    })
    .then(async (response) => {
        if (!response.ok) {
            // If the response status is not OK (e.g., 4xx, 5xx)
            return response.json().then(data => {
                // Handle specific error message if available in response body
                showMessage('error', data.message || 'Something went wrong! Please try again');
                throw new Error(data.message || 'Something went wrong!');
            });
        }
        showMessage('success', 'Code uploaded successfully! Check your GitHub repository');
        loading(false);
    })
    .catch(error => {
        // This will catch network or unexpected errors
        console.error('Error:', error);
        showMessage('error', 'Network error. Please try again');
    })
    .finally(() => {
        loading(false);
    });
});


wayChooser.querySelector('.manual').addEventListener('click', () => {
    wayChooser.classList.add('hidden');
    manual.classList.remove('hidden');
    manual.classList.add('flex');
});

wayChooser.querySelector('.automatic').addEventListener('click', () => {
    wayChooser.classList.add('hidden');
    automatic.classList.remove('hidden');
    automatic.classList.add('flex');
});

manual.querySelector('.automatic').addEventListener('click', () => {
    manual.classList.remove('flex');
    manual.classList.add('hidden');
    automatic.classList.remove('hidden');
    automatic.classList.add('flex');
});

automatic.querySelector('.manual').addEventListener('click', () => {
    automatic.classList.remove('flex');
    automatic.classList.add('hidden');
    manual.classList.remove('hidden');
    manual.classList.add('flex');
});

const input = document.getElementById('search-question');
const searchBtn = document.getElementById('searchBtn');

searchBtn.addEventListener('click', () => {
    handleSearch(input.value);
});

input.addEventListener('keyup', (e) => {
    if (e.key === 'Enter') {
        handleSearch(input.value);
    }
}
);

const handleSearch = (question) => {
    if (question.trim() == "") {
        showMessage('error', 'Please enter a question!');
        return
    }
    if (question.toLowerCase().replace(' ','').replace('-','') in requestedQuestions) {
        showMessage('error', 'Question already requested!');
        return
    }
    console.log(question);
    showMessage('success', 'Searching for question...');
    // Fetch the question from the API
    const encoded_url = encodeURIComponent(question);
    fetch(`/post/api?question=${encoded_url}`, {
        method: 'GET'
    }).then(response => {
        console.log(response.status);
        if (response.status == 404) {
            showMessage('error', 'Question not found!');
            throw new Error('Question not found');
        }
        return response.json();
    }).then(data => {
        console.log(data);
        fillQuestion(data);
        showMessage('success', 'Question found!');
        requestedQuestions[question.toLowerCase().replace(' ','').replace('-','')] = data.questionId; // Add the question to the set of requested questions by removing spaces and hyphens
    }).catch(error => {
        console.log(error);
        if (error.message == 'Question not found') {
            return
        }
        showMessage('error', 'Something went wrong! Please try again');
    });
}

const fillQuestion = (data) => {
    const questionId = data.questionId;
    const questionTitle = data.questionTitle;
    const difficulty = data.difficulty;
    card = document.getElementById('cardContainer').lastElementChild;
    infoDiv = document.createElement('div');
    infoDiv.classList.add('hidden', 'info');
    infoDiv.textContent = JSON.stringify(data);
    card.appendChild(infoDiv)
    card.querySelector('span#questionId').textContent = questionId;
    card.querySelector('span#questionTitle').textContent = questionTitle;
    const difficulty_span = card.querySelector('span#difficulty');
    difficulty_span.textContent = difficulty;
    console.log(difficulty);
    if (difficulty == 'Easy'){
        difficulty_span.classList.remove(...difficulty_span.classList); // Remove all classes
        difficulty_span.classList.add('bg-green-200', 'px-2', 'text-green-600','rounded-full');
    }else if(difficulty == 'Medium'){
        difficulty_span.classList.remove(...difficulty_span.classList); // Remove all classes
        difficulty_span.classList.add('bg-amber-200', 'px-2', 'text-amber-600','rounded-full');
    }else if(difficulty == 'Hard'){
        difficulty_span.classList.remove(...difficulty_span.classList); // Remove all classes
        difficulty_span.classList.add('bg-red-200', 'px-2', 'text-red-600','rounded-full');
    }
    card.querySelector('span#difficulty').textContent = difficulty;
    const textarea = card.querySelector('textarea');
    const select = card.querySelector('select');
    textarea.disabled = false;
    textarea.placeholder = "Write your solution here...";
    select.disabled = false;
}
