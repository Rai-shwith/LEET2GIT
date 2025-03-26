const scrollCard = (next = true) => {
  const container = document.getElementById("cardContainer");
  const cards = container.querySelectorAll(".card");
  const cardWidth = cards[0].offsetWidth + 176; // Includes gap (11rem = 176px)
  
  // Get the current scroll position
  const maxScrollLeft = (cards.length - 1) * cardWidth;
  let newScrollLeft = container.scrollLeft + (next ? cardWidth : -cardWidth);

  // Prevent overscrolling
  if (newScrollLeft < 0) newScrollLeft = 0;
  if (newScrollLeft > maxScrollLeft) newScrollLeft = maxScrollLeft;

  container.scrollTo({ left: newScrollLeft, behavior: "smooth" });
};


const loading = (show = true) => {
  const loadingElement = document.getElementById("loading");
  if (show) {
    console.log("Loading ON");
    loadingElement.classList.remove("hidden");
    loadingElement.classList.add("flex");
  } else {
    console.log("Loading OFF");
    loadingElement.classList.remove("flex");
    loadingElement.classList.add("hidden");
  }
};

const getParent = (element, className) => {
  while (element.parentElement) {
    if (element.classList.contains(className)) {
      return element;
    }
    element = element.parentElement;
  }
  return null;
};

const makeValueNull = (element) => {
  element.value = "";
};

const showMessage = (type, message, autoHide = true) => {
  console.log("Showing message:", type, message);

  const messageContainer = document.getElementById("messageContainer");
  const successMessage = document.getElementById("successMessage");
  const errorMessage = document.getElementById("errorMessage");

  // Make sure container is visible
  messageContainer.style.display = "block";

  // Hide both messages initially
  successMessage.classList.remove("show");
  errorMessage.classList.remove("show");

  if (type === "success") {
    successMessage.querySelector("span").textContent = message || "Repo created successfully!";
    successMessage.classList.add("show");
  } else if (type === "error") {
    errorMessage.querySelector("span").textContent = message || "Repo not found.";
    errorMessage.classList.add("show");
  } else {
    console.error("Invalid message type, choose between 'success' and 'error'");
    return;
  }

  // Auto-hide after 3 seconds
  if (autoHide) {
    setTimeout(() => {
      successMessage.classList.remove("show");
      errorMessage.classList.remove("show");
      messageContainer.style.display = "none";
    }, 3000);
  }
};


// Function to remove the success or error message when user clicks on webpage except the message container
document.addEventListener("click", (event) => {
  if (!messageContainer.contains(event.target)) {
    console.log("Hiding message by clicking outside the message container");
    messageContainer.classList.add("hidden");
  }
});

// When ever user clicks on the add button, a new card is added to the card container.
// The add button of clicked card is hidden when he clicks on add Card . This is because we don't want to add cards in between the cards.
// When user clicks on remove button, the add button of the last card is shown.
// User can remove any card.
// The search bar is cleared when user adds a new card or removes the card.
const addCard = (event) => {
  const currentCard = getParent(event.target, "card");
  // Check if the current card Solution or Language is empty
  const language = currentCard.querySelector("select").value;
  const solution = currentCard.querySelector("textarea").value.trim();
  if (language == "") {
    setTimeout(() => {
      showMessage("error", "Please fill the solution language first!");
    }, 250);
    return;
  } else if (solution == "") {
    setTimeout(() => {
      showMessage("error", "Please fill the solution first!");
    }, 250);
    return;
  }

  const cardContainer = document.getElementById("cardContainer");
  const card = document.createElement("div");
  card.classList.add(
    "card"
  );
  card.innerHTML = `                <div>
                    <!-- Two Main Containers -->
                    <div>

                        <!-- User Question Info -->
                        <div >
                            <h3 >Question Information</h3>
                            <p><span >ID:</span> <span id="questionId">...</span></p>
                            <p><span >Name:</span> <span id="questionTitle">...</span>
                            </p>
                            <p><span >Difficulty:</span> <span id="difficulty">...</span>
                            </p>
                        </div>

                        <!-- Solution Area -->
                        <div >
                            <div >
                                <h3 >Your Solution</h3>
                                <!-- Language Selection Dropdown -->
                                <div>
                                    <div>Choose
                                        Language</div>
                                    <select id="language" disabled >
                                        <option value="" disabled selected></option>
                                        <option value="py">Python </option>
                                        <option value="java">Java </option>
                                        <option value="c">C </option>
                                        <option value="cpp">C++ </option>
                                        <option value="cs">C# </option>
                                        <option value="js">JavaScript </option>
                                        <option value="ts">TypeScript </option>
                                        <option value="rb">Ruby </option>
                                        <option value="swift">Swift </option>
                                        <option value="go">Go </option>
                                        <option value="kt">Kotlin </option>
                                        <option value="scala">Scala </option>
                                        <option value="rs">Rust </option>
                                        <option value="php">PHP </option>
                                        <option value="sql">MySQL </option>
                                        <option value="sh">Bash </option>
                                        <option value="pl">Perl </option>
                                        <option value="hs">Haskell </option>
                                        <option value="dart">Dart </option>
                                        <option value="rkt">Racket </option>
                                        <option value="ex">Elixir </option>
                                        <option value="erl">Erlang </option>
                                        <option value="m">Objective-C </option>
                                        <option value="m">MATLAB </option>
                                        <option value="fs">F# </option>
                                        <option value="lua">Lua </option>
                                        <option value="groovy">Groovy </option>
                                        <option value="vb">VB.NET </option>
                                        <option value="f90">Fortran </option>
                                        <option value="pas">Pascal </option>
                                        <option value="jl">Julia </option>
                                        <option value="pl">Prolog </option>
                                        <option value="scm">Scheme </option>
                                        <option value="cbl">COBOL </option>
                                        <option value="sol">Solidity </option>
                                    </select>
                                </div>
                            </div>
                            <textarea id="solutionArea" placeholder="Search for a question to get started..." disabled ></textarea>
                        </div>
                    </div>
                    <div >

                        <!-- Add and Remove Buttons -->
                        <div class="button-container">
                            <!-- Remove Button -->
                            <button onclick="removeCard(event)"
                                class="remove">
                                <!-- SVG Icon for Remove -->
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"
                                    xmlns="http://www.w3.org/2000/svg">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4">
                                    </path>
                                </svg>
                                <div class="">
                                    Remove Question
                                </div>
                            </button>

                            <!-- Add Button -->
                            <button onclick="addCard(event)"
                                class="add">
                                <!-- SVG Icon for Add -->
                                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"
                                    xmlns="http://www.w3.org/2000/svg">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M12 4v16m8-8H4"></path>
                                </svg>
                                <div class="">
                                    Add Question
                                </div>
                            </button>
                        </div>
                    </div>

                </div>`;
  cardContainer.appendChild(card);
  makeValueNull(input);
  scrollCard();
  // Hide the add button of the current card
  const addBtn = currentCard.querySelector("button.add");
  addBtn.classList.add("hidden");
};

const removeCard = (e) => {
  const cardContainer = document.getElementById("cardContainer");
  if (cardContainer.childElementCount == 1) {
    return;
  }
  card = getParent(e.target, "card");
  makeValueNull(input);
  scrollCard();
  card.remove();
  // Remove the requestedQuestions from the set of requested questions
  const questionId = card.querySelector("span#questionId").textContent;
  for (let question in requestedQuestions) {
    if (requestedQuestions[question] == questionId) {
      delete requestedQuestions[question];
      break;
    }
  }
  cardContainer.lastElementChild
    .querySelector("button.add")
    .classList.remove("hidden");
};

// Function to alternate between placeholders
function cyclePlaceholders(elementId) {
  const inputElement = document.getElementById(elementId);
  // Define the placeholders and delay (in milliseconds)
  const placeholders = [
    "Search LeetCode question...",
    "Paste a LeetCode URL",
    "https://leetcode.com/problems/example/description/",
  ];
  const delay = 4000; // 4 seconds
  let index = 0;

  if (!inputElement) return; // Exit if the element is not found

  setInterval(() => {
    inputElement.placeholder = placeholders[index];
    index = (index + 1) % placeholders.length; // Cycle through the array
  }, delay);
}
