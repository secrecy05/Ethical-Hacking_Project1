const WHITELIST_KEY = "whitelist";
const listEl = document.getElementById("whitelist");
const inputEl = document.getElementById("domainInput");

async function renderList() {
  const data = await chrome.storage.local.get({ [WHITELIST_KEY]: [] });
  const whitelist = data[WHITELIST_KEY];
  listEl.innerHTML = "";
  whitelist.forEach((domain) => {
    const li = document.createElement("li");
    li.textContent = domain + " ";
    const btn = document.createElement("button");
    btn.textContent = "❌";
    btn.addEventListener("click", () => removeDomain(domain));
    li.appendChild(btn);
    listEl.appendChild(li);
  });
}

async function addDomain() {
  const domain = inputEl.value.trim();
  if (!domain) return;
  const data = await chrome.storage.local.get({ [WHITELIST_KEY]: [] });
  const whitelist = data[WHITELIST_KEY];
  if (!whitelist.includes(domain)) {
    whitelist.push(domain);
    await chrome.storage.local.set({ [WHITELIST_KEY]: whitelist });
    inputEl.value = "";
    renderList();
  }
}

async function removeDomain(domain) {
  const data = await chrome.storage.local.get({ [WHITELIST_KEY]: [] });
  const whitelist = data[WHITELIST_KEY].filter((d) => d !== domain);
  await chrome.storage.local.set({ [WHITELIST_KEY]: whitelist });
  renderList();
}

document.getElementById("addDomain").addEventListener("click", addDomain);
renderList();
