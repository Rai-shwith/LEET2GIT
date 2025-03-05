(async function leetcodeSolutionFetcher() {
  let submissions = { submissions_dump: [] };
  let lastKey = "";
  try {
    while (true) {
      const data = await fetchSubmission(lastKey);
      submissions.submissions_dump.push(...(data.submissions_dump || []));
      lastKey = data.last_key;
      console.log(lastKey);
      sleep(2000);
      if (!data.has_next) {
        break;
      }
    }
  } catch (error) {
    console.error("An error occurred:", error.message);
    throw error;
  }

  return submissions;
})();

async function fetchSubmission(lastKey) {
  try {
    const response = await fetch(
      `https://leetcode.com/api/submissions/?lastkey=${lastKey}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    console.log("");
    return response.json();
    // console.log(data);
    return data;
  } catch (error) {
    console.error("Error fetching LeetCode submissions:", error);
  }
}
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
