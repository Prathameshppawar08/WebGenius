// ✅ Scraping logic
document.getElementById("scrape-btn").addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const url = tab.url;
  document.getElementById("captured-url").innerText = url;

  try {
    const res = await fetch("http://127.0.0.1:8000/scrape-and-download", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url })
    });

    const data = await res.json();

    if (res.ok && data.download_url) {
      const downloadLink = document.createElement("a");
      downloadLink.href = data.download_url;
      downloadLink.download = "scraped_output.txt";
      downloadLink.innerText = "📥 Download Scraped Data";
      downloadLink.style.display = "block";
      downloadLink.style.marginTop = "10px";

      const box = document.getElementById("response-box");
      box.innerHTML = "";
      box.appendChild(downloadLink);
    } else {
      document.getElementById("response-box").innerText = data.error || "Scraping failed.";
    }
  } catch (err) {
    console.error("Scraping error:", err);
    document.getElementById("response-box").innerText = "Failed to connect to backend.";
  }
});

// ✅ Chat feature logic
document.getElementById("ask-btn").addEventListener("click", async () => {
  const question = document.getElementById("user-query").value;
  const chatBox = document.getElementById("chat-response");

  chatBox.innerText = "🤖 Thinking...";

  try {
    const res = await fetch("http://127.0.0.1:8000/ask-question", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    });

    const data = await res.json();

    if (res.ok && data.answer) {
      chatBox.innerText = "💬 " + data.answer;
    } else {
      chatBox.innerText = data.error || "❌ Failed to get a response.";
    }
  } catch (err) {
    console.error("Chat error:", err);
    chatBox.innerText = "⚠️ Failed to connect to backend.";
  }
});
