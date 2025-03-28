const wayChooser = document.getElementById("wayChooser");
const manual = document.getElementById("manual");
const automatic = document.getElementById("automatic");
const manualUploadBtn = document.getElementById("manualUploadBtn");
const automaticUploadBtn = document.getElementById("automaticUploadBtn");
const copyBtn = document.getElementById("copyBtn");
const input = document.getElementById("search-question");
const searchBtn = document.getElementById("searchBtn");

let domain = document.querySelector("main").dataset.domain;
let websocketDomain;
if (domain) {
  websocketDomain = "wss://" + domain + "/upload/ws/automatic/";
} else {
  websocketDomain = "ws://localhost:8000/upload/ws/automatic/";
}

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
  messageDiv.className = "stack-message";
  messageDiv.style.width = "18rem";
  messageDiv.style.borderRadius = "2rem"
  messageDiv.style.padding = "0.5rem"
  messageDiv.style.backgroundColor = type === "success" ? "#d1e7dd" : "#f8d7da";
  messageDiv.style.border = `1px solid ${type === "success" ? "#0f5132" : "#842029"}`;
  messageDiv.style.color = type === "success" ? "#0f5132" : "#842029";

  messageDiv.innerHTML = `
        <div class="message-content">
            <svg class="icon" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm${
                  type === "success"
                    ? "3.707-10.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    : "-1-11a1 1 0 012 0v4a1 1 0 01-2 0V7zm1 8a1 1 0 110-2 1 1 0 010 2z"
                }" clip-rule="evenodd" />
            </svg>
            <span class="message-text">${message}</span>
        </div>
    `;

  stackMessageContainer.appendChild(messageDiv);

  setTimeout(() => {
    messageDiv.classList.add("show");
  }, 100);

  if (autoHide) {
    setTimeout(() => {
      messageDiv.classList.remove("show");
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

  const socket = new WebSocket(websocketDomain);

  socket.onopen = () => {
    console.log("WebSocket connection established");
    setInterval(() => {
      socket.send("ping")
      console.log("ping form frontend")
    }, 1000*30);
  };

  socket.onmessage = (event) => {
    console.log("WebSocket message from backend");
    try {
      const data = JSON.parse(event.data);
      console.log(data);
      if (data.ping) {
        socket.send(JSON.stringify({ pong: true })); // Send a pong response to the ping
        return;
      }
      if (data.error) {
        StackMessage("error", data.message, false);
      } else {
        StackMessage("success", data.message, false);
        if (data.message == automatic_websocket_messages[3]) {
          loading(true);
          setTimeout(() => {
            StackMessage(
              "success",
              "Hang tight! This might take a couple of minutes — perfect time for a snack or a victory dance. We'll be back before you know it! 🚀",
              false
            );
          }, 3000);
        }
        if (data.message == automatic_websocket_messages[4]) {
          loading(false);
          document.addEventListener("click", (event) => {
            if (!stackMessageContainer.contains(event.target)) {
              stackMessageContainer.innerHTML = "";
            }
          });
          StackMessage(
            "success",
            `Code uploaded successfully! Check your <a style="text-decoration:underline;" target="_blank" href="${data.link}">GitHub repository</a>`,
            false
          );
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

const clearUploadData = () => {
  const cardContainer = document.getElementById("cardContainer");
  const cards = cardContainer.querySelectorAll(".card");
  const card = cards[0];
  card.querySelector("textarea").value = "";
  card.querySelector("select").value = "";
  card.querySelector(".info").remove();
  card.querySelector("span#questionId").textContent = "";
  card.querySelector("span#questionTitle").textContent = "";
  card.querySelector("span#difficulty").textContent = "";
  for (let index = 1; index < cards.length; index++) {
    cards[index].remove();
  }
  input.value = "";
};

const getUploadData = () => {
  console.log("Getting upload data");
  const cardContainer = document.getElementById("cardContainer");
  const cards = cardContainer.querySelectorAll(".card");
  const uploadData = { uploads: [] };

  for (let index = 0; index < cards.length; index++) {
    const card = cards[index];

    const info = card.querySelector(".info");
    if (info == null && index == 0) {
      console.log("Please search for a question first!");
      setTimeout(() => {
        // Delay the message so that it doesn't close by the click outside event
        showMessage("error", "Please search for a question first!", false);
      }, 250);
      loading(false);
      return;
    }
    const code = card.querySelector("textarea").value;
    const code_extension = card.querySelector("select").value;
    if ((code == "" || code_extension == "") && index == 0) {
      console.log("Please fill the solution and language first!");
      setTimeout(() => {
        showMessage(
          "error",
          "Please fill the solution and language first!",
          false
        );
      }, 500);
      return;
    }
    if (code == "" || code_extension == "") {
      continue;
    }
    const question = JSON.parse(info.textContent);
    upload = { question, solution: { code_extension, code } };
    uploadData.uploads.push(upload);
  }
  return uploadData;
};

manualUploadBtn.addEventListener("click", () => {
  loading();

  const uploadData = getUploadData();
  if (uploadData == undefined || uploadData.uploads.length == 0) {
    loading(false);
    return;
  }
  fetch(`/upload/manual/`, {
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
      clearUploadData();
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
