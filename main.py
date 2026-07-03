import os
from playwright.sync_api import sync_playwright

WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

URL = "https://info.monsterhunter.com/wilds/event-quest/zh-hant/schedule"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    logs = []

    def log_response(response):
        try:
            if "application/json" in response.headers.get("content-type", ""):
                logs.append(response.url)
        except:
            pass

    page.on("response", log_response)

    page.goto(URL, wait_until="networkidle")

    browser.close()

import requests

requests.post(WEBHOOK, json={
    "content": "🎯 偵測到 JSON endpoints：\n\n" + "\n".join(logs[:10])
})
