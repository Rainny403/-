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

# 找所有 tr
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

    text = overview.get_text("\n", strip=True)

print("=" * 50)
print(overview.prettify())
print("=" * 50)
break

    for line in text.split("\n"):

        line = line.strip()

        if line.startswith("原野"):
            quest["field"] = line.replace("原野：", "").strip()

        elif line.startswith("承接／參加條件"):
            quest["hr"] = line.replace("承接／參加條件：", "").strip()

        elif line.startswith("完成條件"):
            quest["target"] = line.replace("完成條件：", "").strip()

        elif line.startswith("發佈開始時間"):
            quest["start"] = line.replace("發佈開始時間：", "").strip()

        elif line.startswith("發佈結束時間"):
            quest["end"] = line.replace("發佈結束時間：", "").strip()

    quests.append(quest)

print(f"成功解析 {len(quests)} 個活動")

for q in quests:
    print(q)
