import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

WORKER_URL = "https://mhwilds-discord.toptoonisgood5.workers.dev"

response = requests.get(WORKER_URL, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "lxml")

print("✅ HTML 取得成功")

rows = soup.select("tr")

print(f"找到 {len(rows)} 個 tr")

quests = []
seen = set()

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

    lines = [
        x.strip()
        for x in overview.get_text("\n", strip=True).split("\n")
        if x.strip() and x.strip() != ":"
    ]

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

    key = (
        quest["title"],
        quest["start"],
        quest["end"]
    )

    if key not in seen:
        seen.add(key)
        quests.append(quest)

print(f"去除重複後，共 {len(quests)} 個活動")
