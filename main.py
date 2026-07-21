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

# ==========================
# 篩選下下週活動
# ==========================

today = datetime.now()

# 本週一
this_monday = today - timedelta(days=today.weekday())

# 下下週一
target_start = this_monday + timedelta(weeks=2)

# 下下週日
target_end = target_start + timedelta(days=7)

print("下下週開始：", target_start.strftime("%Y-%m-%d"))
print("下下週結束：", target_end.strftime("%Y-%m-%d"))

next2_quests = []

for q in quests:

    if not q["end"]:
        continue

    try:
        start_time = datetime.strptime(q["start"], "%Y.%m.%d %H:%M")
        end_time = datetime.strptime(q["end"], "%Y.%m.%d %H:%M")
    except Exception:
        continue

    # 只要下下週期間活動仍然存在
    if end_time >= target_start and start_time < target_end:
        next2_quests.append(q)

# ==========================
# 建立 Discord 訊息
# ==========================

message = "📅 下下週限定活動任務\n\n"

if len(next2_quests) == 0:
    message += "目前沒有下下週活動任務。"

else:

    # 依開始時間排序
    next2_quests.sort(key=lambda q: q["start"])

    for q in next2_quests:

        message += (
            f"{q['level']}　{q['title']}\n"
            f"原野：{q['field']}\n"
            f"承接／參加條件：{q['hr']}\n"
            f"完成條件：{q['target']}\n"
            f"發佈開始時間：{q['start']}\n"
            f"發佈結束時間：{q['end']}\n\n"
        )

print(message)

response = requests.post(
    WEBHOOK,
    json={
        "content": message
    },
    timeout=30
)

print("Discord Status:", response.status_code)

if response.status_code != 204:
    print(response.text)
print(f"下下週共有 {len(next2_quests)} 個活動")

for q in next2_quests:
    print(q)
