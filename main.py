import os
import requests
from bs4 import BeautifulSoup

# Discord Webhook
WEBHOOK = os.environ["DISCORD_WEBHOOK"]

# Cloudflare Worker
WORKER_URL = "https://mhwilds-discord.toptoonisgood5.workers.dev"

# 取得 HTML
response = requests.get(WORKER_URL, timeout=30)
response.raise_for_status()

# 解析 HTML
soup = BeautifulSoup(response.text, "lxml")

print("✅ HTML 取得成功")

# 找所有活動列
rows = soup.select("tr")

print(f"找到 {len(rows)} 個 tr")

quests = []

for row in rows:

    level = row.select_one("td.level")
    title = row.select_one(".title span")
    overview = row.select_one("td.overview")

    if level is None or title is None or overview is None:
        continue

    quest = {
        "level": level.get_text(strip=True),
        "title": title.get_text(strip=True),
        "field": "",
        "hr": "",
        "target": "",
        "start": "",
        "end": ""
    }

    # 取得 overview 內容
    lines = [
        x.strip()
        for x in overview.get_text("\n", strip=True).split("\n")
        if x.strip() and x.strip() != ":"
    ]

    # 解析欄位
    for i in range(len(lines) - 1):

        if lines[i] == "原野":
            quest["field"] = lines[i + 1]

        elif lines[i] == "承接／參加條件":
            quest["hr"] = lines[i + 1]

        elif lines[i] == "完成條件":
            quest["target"] = lines[i + 1]

        elif lines[i] == "發佈開始時間":
            quest["start"] = lines[i + 1]

        elif lines[i] == "發佈結束時間":
            quest["end"] = lines[i + 1]

    quests.append(quest)

print(f"成功解析 {len(quests)} 個活動")

# 顯示前 5 筆確認解析是否正確
for q in quests[:5]:
    print(q)
