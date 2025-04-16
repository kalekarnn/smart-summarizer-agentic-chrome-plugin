document.getElementById("summarizeBtn").addEventListener("click", async () => {
  const button = document.getElementById("summarizeBtn");
  const status = document.getElementById("status");
  const loading = document.querySelector(".loading");

  // Disable button and show loading
  button.disabled = true;
  loading.style.display = "block";
  status.className = "";
  status.textContent = "";

  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    const results = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      function: extractPageText
    });

    const pageText = results[0].result;
    const response = await fetch("http://localhost:5001/summarize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: pageText })
    });

    const data = await response.json();
    status.textContent = data.message || data.error;
    status.className = data.message ? "show success" : "show error";
  } catch (error) {
    status.textContent = "An error occurred. Please try again.";
    status.className = "show error";
  } finally {
    // Re-enable button and hide loading
    button.disabled = false;
    loading.style.display = "none";
  }
});

function extractPageText() {
  return document.body.innerText;
}
