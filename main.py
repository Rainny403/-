import os
import json
from playwright.sync_api import sync_playwright

WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

URL = "https://info.monsterhunter.com/wilds/event-quest/zh-hant/schedule"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(URL, wait_until="networkidle")

    # 取得 Next.js state
    next_data = page.evaluate("""
        () => {
            const el = document.getElementById("__NEXT_DATA__");
            return el ? el.textContent : null;
        }
    """)

    browser.close()

import requests

if not next_data:
    requests.post(WEBHOOK, json={
        "content": "❌ 沒抓到 __NEXT_DATA__（頁面不是 Next.js 或已改版）"
    })
else:
    data = json.loads(next_data)

    requests.post(WEBHOOK, json={
        "content": "✅ 成功抓到 Next.js 資料\n\n" + str(list(data.keys()))
    })
