# scanner.py
import requests
from urllib.parse import urljoin
from payloads import XSS_PAYLOADS, SQLI_PAYLOADS, SQL_ERROR_PATTERNS, SEVERITY

class Scanner:
    def __init__(self, base_url, pages, session=None):
        self.base_url = base_url
        self.pages = pages
        self.session = session or requests.Session()
        self.findings = []

    def _record(self, title, target, payload, evidence, ctype):
        self.findings.append({
            "title": title,
            "target": target,
            "payload": payload,
            "evidence": evidence,
            "type": ctype,
            "severity": SEVERITY.get(ctype, "Low")
        })

    def test_reflected_xss(self, page):
        for form in page["forms"]:
            for payload in XSS_PAYLOADS:
                data = {}
                for inp in form["inputs"]:
                    # inject into text-like fields only
                    if inp["type"] in ("text", "search", "email", "url", "textarea", "password", "hidden"):
                        data[inp["name"]] = payload
                    else:
                        data[inp["name"]] = inp.get("value", "")
                try:
                    if form["method"] == "post":
                        r = self.session.post(form["action"], data=data, timeout=10)
                    else:
                        r = self.session.get(form["action"], params=data, timeout=10)
                except requests.RequestException:
                    continue
                if payload in r.text:
                    self._record("Reflected XSS", form["action"], payload, f"payload found in response (len {len(r.text)})", "xss")

    def test_sqli(self, page):
        for form in page["forms"]:
            for payload in SQLI_PAYLOADS:
                data = {}
                for inp in form["inputs"]:
                    if inp["type"] in ("text", "search", "textarea", "email", "url"):
                        data[inp["name"]] = payload
                    else:
                        data[inp["name"]] = inp.get("value", "")
                try:
                    if form["method"] == "post":
                        r = self.session.post(form["action"], data=data, timeout=10)
                    else:
                        r = self.session.get(form["action"], params=data, timeout=10)
                except requests.RequestException:
                    continue
                lowered = r.text.lower()
                for sig in SQL_ERROR_PATTERNS:
                    if sig in lowered:
                        self._record("Possible SQL Injection (error-based)", form["action"], payload, f"SQL error signature: '{sig}'", "sqli")
                        break

    def test_csrf(self, page):
        # naive: check forms with method POST for presence of anti-CSRF hidden inputs like 'csrf', 'token'
        for form in page["forms"]:
            if form["method"] == "post":
                names = [inp["name"].lower() for inp in form["inputs"] if inp.get("name")]
                tokens = [n for n in names if "csrf" in n or "token" in n or "authenticity_token" in n]
                if not tokens:
                    self._record("Possible CSRF issue", form["action"], None, "POST form missing obvious CSRF token field", "csrf")

    def run(self):
        for page in self.pages:
            self.test_reflected_xss(page)
            self.test_sqli(page)
            self.test_csrf(page)
        return self.findings
