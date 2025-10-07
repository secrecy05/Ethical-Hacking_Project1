document.getElementById("updateRules").addEventListener("click", () => {
  chrome.runtime.sendMessage({ action: "updateRules" }, (response) => {
    if (response && response.success) {
      document.getElementById("status").textContent = "✅ Blocklist updated!";
    } else {
      document.getElementById("status").textContent = "❌ Update failed.";
    }
  });
});
