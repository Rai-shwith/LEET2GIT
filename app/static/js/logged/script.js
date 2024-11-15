const finishBtn = document.getElementById('finish');
finishBtn.addEventListener('click', async () => {
    try {
        // Disable the button immediately and start loading animation
        finishBtn.disabled = true;
        loading();

        // Validate the repository name
        const repo = document.getElementById("repoName").value.trim();
        if (repo === "") {
            showMessage('error', 'Repo cannot be empty');
            scrollCard(false);
            return;
        }

        // Get input values
        const isOld = document.getElementById('newOrOld').checked;
        const isPrivate = document.getElementById('visibility').checked;
        console.log("isNew", !isOld, "\nisPrivate", isPrivate, "\nrepo", repo);

        // Perform the fetch request
        const response = await fetch(`/register/api?repo_name=${repo}&new=${!isOld}&private=${isPrivate}`, {
            method: 'GET'
        });

        // Handle response statuses
        if (response.status === 422) {
            showMessage('error', 'Repo already exists!');
        } else if (response.status === 404) {
            showMessage('error', 'Repo not found!');
        } else if (response.redirected) {
            showMessage('success', 'Repo created successfully!');
            window.location.href = response.url; // Redirect to the URL
        }
    } catch (error) {
        console.error('An error occurred:', error);
        showMessage('error', 'Something went wrong. Please try again.');
    } finally {
        // Stop loading and re-enable the button
        loading(false);
        finishBtn.disabled = false;
    }
});
