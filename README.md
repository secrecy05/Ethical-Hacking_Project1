# Ethical-Hacking_Project1
It is a project which would help me to get the real world experience.
# 🛡️ TrackerExtension - Browser Extension to Block Trackers

## 📖 Introduction
**TrackExtension** is a privacy-focused browser extension built to block known tracking scripts and improve user privacy.  
It identifies and stops web requests to tracking domains, helping users browse the internet securely without being followed by trackers.

---

## 🧠 Abstract
TrackExtension uses Chrome Manifest V3 and JavaScript to monitor and intercept web requests. By maintaining a list of tracking domains and using the `declarativeNetRequest` API, it blocks those connections before they reach the user’s browser.  
The extension includes a badge counter that shows the number of blocked trackers and provides user controls for managing whitelists and blacklists.

---

## 🧰 Tools Used
- **HTML, CSS, JavaScript** – For structure, styling, and logic.  
- **Manifest V3** – For Chrome extension configuration.  
- **Declarative Net Request (DNR) API** – For efficient tracker blocking.  
- **JSON** – For storing static blocking rules.  
- **Visual Studio Code** – For writing and debugging code.  
- **Chrome Developer Tools** – For testing and debugging the extension.

---

## ⚙️ Steps to Build
1. **Project Setup**  
   Create the folder structure and define permissions in `manifest.json`.

2. **Blocking Logic**  
   Implemented `service_worker.js` to block tracker domains using DNR API.

3. **UI Design**  
   Built `popup.html`, `popup.js`, and `options.html` for analytics and user settings.

4. **Static Rules**  
   Added `rules/static_rules.json` to maintain known tracker domains.

5. **Icons Integration**  
   Added 16x16 and 48x48 pixel icons for the browser toolbar.

6. **Testing**  
   Load the extension in Chrome using “Load unpacked” and verify blocking.

---

## 📊 Features
- Blocks known tracking domains.  
- Displays blocked tracker count via toolbar badge.  
- Allows whitelisting and blacklisting of domains.  
- Lightweight and privacy-focused implementation.

---

## ✅ Conclusion
TrackExtension demonstrates how browser extensions can effectively enhance online privacy.  
It uses modern APIs from Manifest V3 to ensure efficient performance, giving users control and visibility over tracking activities.

---

## 📂 Folder Structure
```
tracker-blocker/
├─ manifest.json
├─ service_worker.js
├─ popup.html
├─ popup.js
├─ options.html
├─ options.js
├─ icons/
│  ├─ icon16.png
│  └─ icon48.png
└─ rules/
   └─ static_rules.json
```

---

## 🧑‍💻 Author
Developed by **Prince Goswami**  
© 2025 TrackExtension Project
