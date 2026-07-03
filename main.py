import os
import json
from playwright.sync_api import sync_playwright

WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

URL = "https://info.monsterhunter.com/wilds/event-quest/zh-hant/schedule"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    responses = []

    def handle_response(response):
        if "json" in response.headers.get("content-type", ""):
            responses.append(response)

    page.on("response", handle_response)

    page.goto(URL, wait_until="networkidle")

    browser.close()

# 找 JSON API
data = []
for r in responses:
    try:
        data.append(r.json())
    except:
        pass

import requests

requests.post(WEBHOOK, json={
    "content": "抓到 JSON 數量：" + str(len(data))
})
