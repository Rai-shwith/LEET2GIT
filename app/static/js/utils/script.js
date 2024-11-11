const scrollCard = (next = true) => {
    const container = document.getElementById('cardContainer');
    const cardWidth = container.querySelector('.flex-none').offsetWidth;
    if (next) {
        container.scrollBy({ left: cardWidth, behavior: 'smooth' });
    } else {
        container.scrollBy({ left: -cardWidth, behavior: 'smooth' });
    }
}

const loading = (show = true) => {
    const loadingElement = document.getElementById('loading');
    if (show) {
        loadingElement.classList.remove('hidden');
        loadingElement.classList.add('flex');
    } else {
        loadingElement.classList.remove('flex');
        loadingElement.classList.add('hidden');
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


// When ever user clicks on the add button, a new card is added to the card container.
// The add button of clicked card is hidden when he clicks on add Card . This is because we don't want to add cards in between the cards.
// When user clicks on remove button, the add button of the last card is shown.
// User can remove any card.
// The search bar is cleared when user adds a new card or removes the card.
const addCard = (event) => {
    const currentCard = getParent(event.target, 'card');
    // Check if the current card Solution or Language is empty
    const language = currentCard.querySelector('select').value;
    const solution = currentCard.querySelector('textarea').value.trim();
    if (language == "") {
        showMessage('error', 'Please fill the solution language first!');
        return
    } else if (solution == "") {
        showMessage('error', 'Please fill the solution first!');
        return
    }

    const cardContainer = document.getElementById('cardContainer');
    const card = document.createElement('div');
    card.classList.add("card", "snap-center", "flex-none", "w-full", "flex", "justify-center", "items-center");
    card.innerHTML = `<div class=" bg-white w-5/6 p-5 m-5 rounded-3xl">
                        <!-- Two Main Containers -->
                        <div class="space-y-6 md:space-y-0 md:flex md:space-x-6">

                            <!-- User Question Info -->
                            <div class="flex-1 p-5 bg-blue-50 rounded-lg shadow">
                                <h3 class="text-xl font-semibold text-gray-700 mb-3">Question Information</h3>
                                <p><span class="font-bold text-gray-600">ID:</span> <span id="questionId">...</span></p>
                                <p><span class="font-bold text-gray-600">Name:</span> <span
                                        id="questionTitle">...</span></p>
                                <p><span class="font-bold text-gray-600">Difficulty:</span> <span
                                        id="difficulty">...</span></p>
                            </div>

                            <!-- Solution Area -->
                            <div class="flex-1 p-5 bg-blue-50 rounded-lg shadow">
                                <div class="flex justify-between">
                                    <h3 class="text-xl font-semibold text-gray-700 mb-3">Your Solution</h3>
                                    <!-- Language Selection Dropdown -->
                                    <div class="text-xs">
                                        <label for="language" class="block text-gray-600 font-medium ">Choose
                                            Language</label>
                                        <select id="language" disabled
                                            class=" border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
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
                                <textarea id="solutionArea" placeholder="Search for a question to get started..."
                                    disabled
                                    class="w-full h-40 p-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"></textarea>
                            </div>
                        </div>
                        <div class="flex justify-center items-center p-4 mt-4 border-t border-gray-200">

                            <!-- Add and Remove Buttons -->
                            <div class="flex w-full justify-evenly text-sm space-x-3">
                                <!-- Remove Button -->
                                <button onclick="removeCard(event)"
                                    class="remove flex justify-center space-x-2 items-center px-6 py-3 rounded-lg bg-red-100 hover:bg-red-600 text-black hover:text-white font-semibold transition-all duration-200 ease-in-out">
                                    <!-- SVG Icon for Remove -->
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"
                                        xmlns="http://www.w3.org/2000/svg">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M20 12H4"></path>
                                    </svg>
                                    <div class="">
                                        Remove Question
                                    </div>
                                </button>

                                <!-- Add Button -->
                                <button onclick="addCard(event)"
                                    class="add flex justify-center space-x-2 items-center px-6 py-3 rounded-lg bg-blue-100 hover:bg-blue-600 text-black hover:text-white font-semibold transition-all duration-200 ease-in-out">
                                    <!-- SVG Icon for Add -->
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"
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
    const addBtn = currentCard.querySelector('button.add');
    addBtn.classList.add('hidden');


}

const removeCard = (e) => {
    const cardContainer = document.getElementById('cardContainer');
    if (cardContainer.childElementCount == 1) {
        return
    }
    card = getParent(e.target, 'card');
    makeValueNull(input);
    scrollCard();
    card.remove();
    cardContainer.lastElementChild.querySelector('button.add').classList.remove('hidden');
};