async function getProblemDetails(titleSlug) {
  const BASE_URL = "https://leetcode.com/graphql/";
  const query = queryGenerator(titleSlug);
  try {
    const response = await fetch(BASE_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });
    if (!response.ok) {
      console.error("Failed to retrieve page");
      throw new Error("Failed to retrieve question details");
    }
    const data = await response.json();
    if (!data || !data.data || !data.data.question) {
      console.error("Invalid URL");
      throw new Error("Invalid URL");
    }
    const problem = data.data.question;
    return {
      questionId: problem.questionId,
      questionFrontendId: problem.questionFrontendId,
      questionTitle: problem.title,
      question: problem.content,
      link: `https://leetcode.com/problems/${problem.titleSlug}`,
      difficulty: problem.difficulty,
      topicTags: problem.topicTags,
      titleSlug: problem.titleSlug,
    };
  } catch (error) {
    console.error(error.message);
    throw new Error(error.message);
  }
}
function queryGenerator(titleSlug) {
  titleSlug = titleSlug.replace(/ /g, "-").replace(/\//g, "");
  const query = `query { question(titleSlug: "${titleSlug}") { questionId questionFrontendId title titleSlug content difficulty topicTags { name slug translatedName } }}`;
  return query;
}
function getExtension(language) {
  const extensionMap = {
    python3: "py",
    python: "py",
    pandas: "py",
    java: "java",
    c: "c",
    cpp: "cpp",
    csharp: "cs",
    javascript: "js",
    typescript: "ts",
    ruby: "rb",
    swift: "swift",
    go: "go",
    kotlin: "kt",
    scala: "scala",
    rust: "rs",
    php: "php",
    mysql: "sql",
    bash: "sh",
    perl: "pl",
    haskell: "hs",
    dart: "dart",
    racket: "rkt",
    elixir: "ex",
    erlang: "erl",
    "objective-c": "m",
    matlab: "m",
    fsharp: "fs",
    lua: "lua",
    groovy: "groovy",
    "vb.net": "vb",
    fortran: "f90",
    pascal: "pas",
    julia: "jl",
    prolog: "pl",
    scheme: "scm",
    cobol: "cbl",
    solidity: "sol",
  };
  return extensionMap[language.toLowerCase()] || "txt";
}
async function organizeLeetcodeSolutions(rawSolutions) {
  console.log("Organizing Leetcode solutions...");
  const submissionsDump = rawSolutions.submissions_dump;
  const uniqueRecentSubmissions = {};
  const uploads = [];
  const tasks = [];
  const taskMapping = {};
  console.log("Starting Leetcode Question fetch.");
  for (const submission of submissionsDump) {
    if (submission.status_display !== "Accepted") continue;
    const { timestamp, title_slug, lang_name, code } = submission;
    const code_extension = getExtension(lang_name);
    const solution = { code, code_extension };
    if (!uniqueRecentSubmissions[title_slug]) {
      const task = getProblemDetails(title_slug);
      tasks.push(task);
      taskMapping[title_slug] = tasks.length - 1;
      uploads.push({ question: null, solution });
      uniqueRecentSubmissions[title_slug] = {
        timestamp,
        index: uploads.length - 1,
      };
    }
    if (uniqueRecentSubmissions[title_slug]?.timestamp < timestamp) {
      uniqueRecentSubmissions[title_slug].timestamp = timestamp;
      uploads[uniqueRecentSubmissions[title_slug].index] = {
        question: null,
        solution,
      };
    }
  }
  const problemDetailsList = await Promise.all(tasks);
  for (const [titleSlug, taskIndex] of Object.entries(taskMapping)) {
    const problemDetails = problemDetailsList[taskIndex];
    const index = uniqueRecentSubmissions[titleSlug].index;
    uploads[index].question = problemDetails;
  }
  return { uploads };
}
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
async function fetchSubmissions() {
  console.log("Starting Leetcode submission fetch");
  let offset = 0;
  let hasNext = true;
  let submissions = { submissions_dump: [] };
  while (hasNext) {
    try {
      const response = await fetch(
        `https://leetcode.com/api/submissions/?offset=${offset}`
      );
      if (!response.ok) {
        throw new Error("HTTP error! status: ${response.status}");
      }
      const data = await response.json();
      submissions.submissions_dump.push(...(data.submissions_dump || []));
      offset += 20;
      hasNext = data.has_next;
      await sleep(500);
    } catch (error) {
      console.error("Error:", error);
      break;
    }
  }
  connection_id = "xxxxxxxxxx";
  const socket = new WebSocket(
    `ws://localhost:8000/upload/ws/automatic/${connection_id}`
  );
  socket.onopen = () => {
    console.log("Socket connected");
    organizeLeetcodeSolutions(submissions)
      .then((data) => {
        console.log("Sending data to the server...");
        socket.send(JSON.stringify(data));
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };
  socket.onmessage = (event) => {
    console.log(event.message);
  };
}
fetchSubmissions();




























function connectWebSocket() {
    const socket = new WebSocket("ws://localhost:8000/upload/ws/automatic/");

    socket.onopen = () => {
        console.log("WebSocket connection established.");
    };

    socket.onmessage = (event) => {
        try {
            const message = JSON.parse(event.data);
            console.log("Received message:", message.message);
            console.log(message.code);
        } catch (error) {
            console.error("Error parsing message:", error);
        }
    };

    socket.onerror = (error) => {
        console.error("WebSocket error:", error);
    };

    socket.onclose = (event) => {
        if (event.wasClean) {
            console.log(`WebSocket closed cleanly, code=${event.code}, reason=${event.reason}`);
        } else {
            console.warn("WebSocket connection closed unexpectedly.");
        }
    };
}
