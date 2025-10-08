# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from crawler import Crawler
from scanner import Scanner
from reporter import save_scan, load_scans
import requests

app = Flask(__name__)
app.secret_key = "change_this_in_prod"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        target = request.form.get("target")
        if not target:
            flash("Enter a target URL (include http:// or https://)", "error")
            return redirect(url_for("index"))
        # basic normalization
        if not target.startswith("http"):
            target = "http://" + target
        # Crawl & scan
        sess = requests.Session()
        c = Crawler(target, max_pages=30, session=sess)
        pages = c.crawl()
        s = Scanner(target, pages, session=sess)
        findings = s.run()
        fname = save_scan(target, findings)
        flash(f"Scan complete. Saved to {fname}", "success")
        return redirect(url_for("results"))
    return render_template("index.html")

@app.route("/results")
def results():
    scans = load_scans()
    return render_template("results.html", scans=scans)

if __name__ == "__main__":
    app.run(debug=True)
