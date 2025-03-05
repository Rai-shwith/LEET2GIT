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
  console.info("Organizing Leetcode solutions...");
  const submissionsDump = rawSolutions.submissions_dump;
  const uniqueRecentSubmissions = {};
  const uploads = [];
  const tasks = [];
  const taskMapping = {};
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
