function showMessage(type, message) {
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


const finishBtn = document.getElementById('finish');
finishBtn.addEventListener('click', () => {
    const repo = document.getElementById("repoName").value.trim();
    if (repo == "") {
        showMessage('error', 'Repo Canot be Empty');
        scrollCard(false);
        return
    }
    const isOld = document.getElementById('newOrOld').checked;
    const isPrivate = document.getElementById('visibility').checked;
    console.log("isNew", !isOld, "\nisPrivate", isPrivate, "\nrepo", repo)
    fetch(`/register/api?repo_name=${repo}&new=${!isOld}&private=${isPrivate}`, {
        method: 'GET'
    }).then(response => { // response is the result of the fetch
        if (response.status == 422) {
            showMessage('error', 'Repo already exists!');
        }
        else if (response.status == 404) {
            showMessage('error', 'Repo not found!');
        }
        else if (response.redirected) {
            showMessage('sucess', 'Repo created successfully!');
            window.location.href = response.url; // redirect to the url
        }
    });
})
//   let btn = document.querySelector('#btn');
//     btn.addEventListener('click', (e) => {
//         const isNew = document.querySelector('#new').checked;
//         const isPrivate = document.querySelector('#private').checked;
//         let repo = document.querySelector('#repo').value;
//         fetch(`/register/api?repo_name=${repo}&new=${isNew}&private=${isPrivate}`, {
//             method: 'GET'
//         }).then(response => { // response is the result of the fetch
//             if (response.status == 422){
//                 alert('Repo already exists');
//             }
//             else if (response.status == 404){
//                 alert('Repo not found');
//             }
//             else if (response.redirected) { 
//                 window.location.href = response.url; // redirect to the url
//             }
//         });
//     });