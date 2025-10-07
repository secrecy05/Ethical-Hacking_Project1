const WHITELIST_KEY = "whitelist";
const DYNAMIC_RULE_IDS_KEY = "dynamicRuleIds";

chrome.runtime.onInstalled.addListener(() => {
  chrome.declarativeNetRequest.setExtensionActionOptions({
    displayActionCountAsBadgeText: true,
  });
  console.log("Tracker Blocker installed and ready.");
});

// Listen for popup commands (update, whitelist, etc.)
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === "updateRules") {
    rebuildDynamicRules().then(() => sendResponse({ success: true }));
    return true; // keep message channel open
  }
});

// Fetch sample blocklist (you can expand later)
async function fetchTrackerList() {
  // Example static list — can be replaced with external fetch
  return [
    "googletagmanager.com",
    "ads.yahoo.com",
    "adservice.google.com",
    "analytics.twitter.com",
    "pixel.facebook.com",
  ];
}

async function rebuildDynamicRules() {
  const trackers = await fetchTrackerList();
  const data = await chrome.storage.local.get({ [WHITELIST_KEY]: [] });
  const whitelist = data[WHITELIST_KEY];
  const filtered = trackers.filter((d) => !whitelist.includes(d));

  const max = chrome.declarativeNetRequest.MAX_NUMBER_OF_DYNAMIC_RULES || 5000;
  const rules = filtered.slice(0, max).map((domain, i) => ({
    id: 1000 + i,
    priority: 1,
    action: { type: "block" },
    condition: {
      urlFilter: `||${domain}^`,
      resourceTypes: ["script", "xmlhttprequest", "image"],
    },
  }));

  const old = await chrome.storage.local.get({ [DYNAMIC_RULE_IDS_KEY]: [] });
  const oldIds = old[DYNAMIC_RULE_IDS_KEY] || [];

  await chrome.declarativeNetRequest.updateDynamicRules({
    removeRuleIds: oldIds,
    addRules: rules,
  });

  await chrome.storage.local.set({
    [DYNAMIC_RULE_IDS_KEY]: rules.map((r) => r.id),
  });

  console.log(`✅ Updated dynamic rules (${rules.length})`);
}
