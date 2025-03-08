const wayChooser = document.getElementById("wayChooser");
const manual = document.getElementById("manual");
const automatic = document.getElementById("automatic");
const manualUploadBtn = document.getElementById("manualUploadBtn");
const automaticUploadBtn = document.getElementById("automaticUploadBtn");
const copyBtn = document.getElementById("copyBtn");
let dataExist = false;
const requestedQuestions = new Object(); // To keep track of questions requested so that to stop the unnecessary requests

// Start cycling placeholders
cyclePlaceholders("search-question");

// To stack the message only for websocket automatic upload interaction

const stackMessageContainer = document.getElementById("stackMessageContainer");
const StackMessage = (type, message, autoHide = true) => {
  const messageId = `msg-${Date.now()}`;

  const messageDiv = document.createElement("div");
  messageDiv.id = messageId;
  messageDiv.className = `min-w-xs w-full p-4 rounded-lg shadow-lg transform transition-transform translate-x-20 opacity-0 ${
    type === "success"
      ? "bg-green-100 border border-green-400 text-green-700"
      : "bg-red-100 border border-red-400 text-red-700"
  }`;
  messageDiv.style.width = "18rem";

  messageDiv.innerHTML = `
        <div class="flex items-center">
            <svg class="w-5 h-5 mr-2 ${
              type === "success" ? "text-green-600" : "text-red-600"
            }" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm${
                  type === "success"
                    ? "3.707-10.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    : "-1-11a1 1 0 012 0v4a1 1 0 01-2 0V7zm1 8a1 1 0 110-2 1 1 0 010 2z"
                }" clip-rule="evenodd" />
            </svg>
            <span style="max-width: 14rem;">${message}</span>
        </div>
    `;

  stackMessageContainer.appendChild(messageDiv);

  setTimeout(() => {
    messageDiv.classList.remove("translate-x-20", "opacity-0");
    messageDiv.classList.add("translate-x-0", "opacity-100");
  }, 100);

  if (autoHide) {
    setTimeout(() => {
      messageDiv.classList.remove("translate-x-0", "opacity-100");
      messageDiv.classList.add("translate-x-20", "opacity-0");

      setTimeout(() => {
        messageDiv.remove();
      }, 300);
    }, 3000);
  }
};

// Function to copy the code to the clipboard
function copyCode() {
  const codeBlock = document.getElementById("code-block").innerText;
  navigator.clipboard
    .writeText(codeBlock)
    .then(() => {
      StackMessage("success", "Code copied to clipboard", false);
    })
    .catch((err) => {
      console.error("Failed to copy: ", err);
      StackMessage(
        "error",
        "Failed to copy code to clipboard, try to copy manually",
        false
      );
    });
}

// Trigger the copy
copyBtn.addEventListener("click", () => {
  console.log("Copy button clicked");
  if (dataExist) {
    copyCode();
  }
});

const automatic_websocket_messages = [
  "Code sent successfully",
  "Leetcode data received",
  "Processing the data...",
  "Uploading the data to github...",
  "Upload successful checkout your repository",
];

automaticUploadBtn.addEventListener("click", () => {
  if (dataExist) return;
  console.log("Automatic upload button clicked");
  loading(true); // Start the loading spinner

  const socket = new WebSocket("ws://localhost:8000/upload/ws/automatic/");

  socket.onopen = () => {
    console.log("WebSocket connection established");
  };

  socket.onmessage = (event) => {
    console.log("WebSocket message from backend");
    try {
      const data = JSON.parse(event.data);
      console.log(data);

      if (data.error) {
        StackMessage("error", data.message, false);
      } else {
        StackMessage("success", data.message, false);
        if (data.message == automatic_websocket_messages[3]) {
          loading(true);
          StackMessage(
            "success",
            "Hold tight! This process might take a couple of minutes. Maybe grab a snack, do a little dance, or stare at the loading bar like it owes you money. We'll be back before you know it! 🚀",
            false
          );
        }
        if (data.message == automatic_websocket_messages[3]) {
          loading(false);
          document.addEventListener('click', (event) => {
            if (!stackMessageContainer.contains(event.target)) {
                stackMessageContainer.innerHTML = "";
            }
        });
        StackMessage("success", `Code uploaded successfully! Check your <a style="text-decoration: underline;" target="_blank href="${data.link}">GitHub repository</a>`, false);
        }
      }

      if (data.code) {
        loading(false);
        automaticUploadBtn.classList.add("dim");
        const codeBlock = document.getElementById("code-block");
        if (codeBlock) {
          codeBlock.innerText = data.code;
          dataExist = true;
          copyBtn.classList.remove("dim");
          document.getElementById("code-cover").hidden = false;
        } else {
          console.warn("Element with ID 'code-block' not found");
        }
      }
    } catch (error) {
      console.error("Error parsing WebSocket message:", error);
    }
  };

  socket.onerror = (error) => {
    console.error("WebSocket error:", error);
    StackMessage("error", "WebSocket connection error", false);
    loading(false); // Stop loading spinner on error
  };

  socket.onclose = (event) => {
    console.log("WebSocket connection closed", event);
    loading(false); // Stop the loading spinner when connection closes
  };
});

manualUploadBtn.addEventListener("click", () => {
  loading();
  const cardContainer = document.getElementById("cardContainer");
  const cards = cardContainer.querySelectorAll(".card");
  const uploadData = { uploads: [] };

  for (let index = 0; index < cards.length; index++) {
    const card = cards[index];

    const info = card.querySelector(".info");
    if (info == null && index == 0) {
      showMessage("error", "Please search for a question first!");
      loading(false);
      return;
    }
    const code = card.querySelector("textarea").value;
    const code_extension = card.querySelector("select").value;
    if ((code == "" || code_extension == "") && index == 0) {
      showMessage("error", "Please fill the solution and language first!");
      loading(false);
      return;
    }
    if (code == "" || code_extension == "") {
      continue;
    }
    const question = JSON.parse(info.textContent);
    upload = { question, solution: { code_extension, code } };
    uploadData.uploads.push(upload);
  }

  fetch(`/upload/manual`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(uploadData), // Ensure uploadData is properly structured as an object
  })
    .then(async (response) => {
      if (!response.ok) {
        // If the response status is not OK (e.g., 4xx, 5xx)
        return response.json().then((data) => {
          // Handle specific error message if available in response body
          showMessage(
            "error",
            data.message || "Something went wrong! Please try again",
            false
          );
          throw new Error(data.message || "Something went wrong!");
        });
      }
      showMessage(
        "success",
        "Code uploaded successfully! Check your GitHub repository",
        false
      );
      loading(false);
    })
    .catch((error) => {
      // This will catch network or unexpected errors
      console.error("Error:", error);
      showMessage("error", "Network error. Please try again", false);
    })
    .finally(() => {
      loading(false);
    });
});

wayChooser.querySelector(".manual").addEventListener("click", () => {
  wayChooser.classList.add("hidden");
  manual.classList.remove("hidden");
  manual.classList.add("flex");
});

wayChooser.querySelector(".automatic").addEventListener("click", () => {
  wayChooser.classList.add("hidden");
  automatic.classList.remove("hidden");
  automatic.classList.add("flex");
});

manual.querySelector(".automatic").addEventListener("click", () => {
  manual.classList.remove("flex");
  manual.classList.add("hidden");
  automatic.classList.remove("hidden");
  automatic.classList.add("flex");
});

automatic.querySelector(".manual").addEventListener("click", () => {
  automatic.classList.remove("flex");
  automatic.classList.add("hidden");
  manual.classList.remove("hidden");
  manual.classList.add("flex");
});

const input = document.getElementById("search-question");
const searchBtn = document.getElementById("searchBtn");

searchBtn.addEventListener("click", () => {
  handleSearch(input.value);
});

input.addEventListener("keyup", (e) => {
  if (e.key === "Enter") {
    handleSearch(input.value);
  }
});

const handleSearch = (question) => {
  if (question.trim() == "") {
    showMessage("error", "Please enter a question!");
    return;
  }
  if (
    question.toLowerCase().replace(" ", "").replace("-", "") in
    requestedQuestions
  ) {
    console.log("Question already requested!");
    showMessage("error", "Question already requested!");
    return;
  }
  console.log(question);
  showMessage("success", "Searching for question...");
  // Fetch the question from the API
  const encoded_url = encodeURIComponent(question);
  fetch(`/post/api?question=${encoded_url}`, {
    method: "GET",
  })
    .then((response) => {
      console.log(response.status);
      if (response.status == 404) {
        showMessage("error", "Question not found!");
        throw new Error("Question not found");
      }
      return response.json();
    })
    .then((data) => {
      console.log(data);
      fillQuestion(data);
      showMessage("success", "Question found!");
      requestedQuestions[
        question.toLowerCase().replace(" ", "").replace("-", "")
      ] = data.questionId; // Add the question to the set of requested questions by removing spaces and hyphens
    })
    .catch((error) => {
      console.log(error);
      if (error.message == "Question not found") {
        return;
      }
      showMessage("error", "Something went wrong! Please try again");
    });
};

const fillQuestion = (data) => {
  const questionId = data.questionId;
  const questionTitle = data.questionTitle;
  const difficulty = data.difficulty;
  card = document.getElementById("cardContainer").lastElementChild;
  infoDiv = document.createElement("div");
  infoDiv.classList.add("hidden", "info");
  infoDiv.textContent = JSON.stringify(data);
  card.appendChild(infoDiv);
  card.querySelector("span#questionId").textContent = questionId;
  card.querySelector("span#questionTitle").textContent = questionTitle;
  const difficulty_span = card.querySelector("span#difficulty");
  difficulty_span.textContent = difficulty;
  console.log(difficulty);
  if (difficulty == "Easy") {
    difficulty_span.classList.remove(...difficulty_span.classList); // Remove all classes
    difficulty_span.classList.add(
      "bg-green-200",
      "px-2",
      "text-green-600",
      "rounded-full"
    );
  } else if (difficulty == "Medium") {
    difficulty_span.classList.remove(...difficulty_span.classList); // Remove all classes
    difficulty_span.classList.add(
      "bg-amber-200",
      "px-2",
      "text-amber-600",
      "rounded-full"
    );
  } else if (difficulty == "Hard") {
    difficulty_span.classList.remove(...difficulty_span.classList); // Remove all classes
    difficulty_span.classList.add(
      "bg-red-200",
      "px-2",
      "text-red-600",
      "rounded-full"
    );
  }
  card.querySelector("span#difficulty").textContent = difficulty;
  const textarea = card.querySelector("textarea");
  const select = card.querySelector("select");
  textarea.disabled = false;
  textarea.placeholder = "Write your solution here...";
  select.disabled = false;
};
