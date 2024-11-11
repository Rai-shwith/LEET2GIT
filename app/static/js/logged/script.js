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