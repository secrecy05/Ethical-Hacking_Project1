# crawler.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag

class Crawler:
    def __init__(self, base_url, max_pages=200, session=None):
        self.base_url = base_url.rstrip('/')
        self.visited = set()
        self.to_visit = [self.base_url]
        self.max_pages = max_pages
        self.session = session or requests.Session()
        self.domain = urlparse(self.base_url).netloc

    def _same_domain(self, url):
        parsed = urlparse(url)
        return parsed.netloc == "" or parsed.netloc == self.domain

    def extract_forms(self, html, page_url):
        soup = BeautifulSoup(html, "html5lib")
        forms = []
        for form in soup.find_all("form"):
            action = form.get("action") or page_url
            method = (form.get("method") or "get").lower()
            inputs = []
            for inp in form.find_all(["input", "textarea", "select"]):
                name = inp.get("name")
                input_type = inp.get("type", "text")
                value = inp.get("value", "")
                if name:
                    inputs.append({"name": name, "type": input_type, "value": value})
            forms.append({"action": urljoin(page_url, action), "method": method, "inputs": inputs})
        return forms

    def crawl(self):
        pages = []
        while self.to_visit and len(self.visited) < self.max_pages:
            url = self.to_visit.pop(0)
            url, _ = urldefrag(url)  # strip fragments
            if url in self.visited: 
                continue
            try:
                r = self.session.get(url, timeout=10)
            except requests.RequestException:
                self.visited.add(url)
                continue
            self.visited.add(url)
            html = r.text
            forms = self.extract_forms(html, url)
            pages.append({"url": url, "status_code": r.status_code, "forms": forms, "html": html})
            soup = BeautifulSoup(html, "html5lib")
            for a in soup.find_all("a", href=True):
                link = urljoin(url, a["href"])
                link, _ = urldefrag(link)
                if self._same_domain(link) and link not in self.visited and link not in self.to_visit:
                    self.to_visit.append(link)
        return pages
