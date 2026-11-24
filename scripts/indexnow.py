"""Avvisa Bing e gli altri motori IndexNow delle pagine del sito (gratis, senza account)."""
import json, re, urllib.request
from pathlib import Path
R = Path(__file__).resolve().parent.parent
KEY = "96517653c573e54eff092f62ade4005e"
urls = re.findall(r"<loc>([^<]+)</loc>", (R / "sitemap.xml").read_text(encoding="utf-8"))
body = json.dumps({"host": "stipendioccnl.it", "key": KEY, "keyLocation": f"https://stipendioccnl.it/{KEY}.txt", "urlList": urls}).encode()
try:
    with urllib.request.urlopen(urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                                headers={"Content-Type": "application/json; charset=utf-8"}), timeout=30) as r:
        print("IndexNow", r.status, len(urls), "pagine")
except Exception as e:
    print("IndexNow non riuscito:", e)
