function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
async function fetchSubmissions() {
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
      console.log("Offset is", offset);
      offset += 20;
      hasNext = data.has_next;
      await sleep(500);
    } catch (error) {
      console.error("Error:", error);
      break;
    }
  }
  console.log("Fetching submission from leetcode completed!");
  const result = await organizeLeetcodeSolutions(submissions);
  sendDataToLeet2git(result);
}

const sendDataToLeet2git = async (uploads) => {
  fetch("http://localhost:8000/automatic", {
    method: "POST",
    body: JSON.stringify(uploads),
    headers: {
      "Content-Type": "application/json",
    },
  });
};

fetchSubmissions();
