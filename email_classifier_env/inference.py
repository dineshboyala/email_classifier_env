import os
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

print("[START]")

# Reset environment
res = requests.post(f"{API_BASE_URL}/reset", json={
    "episode_id": "smart-agent",
    "seed": 42
})

try:
    data = res.json()
    print("RESET:", data)
except:
    print("RESET ERROR:", res.text)
    print("[END]")
    exit()

done = False
step_count = 0

# 🔥 Smart keyword intelligence
SPAM_KEYWORDS = ["win", "free", "offer", "click", "money", "prize"]
IMPORTANT_KEYWORDS = ["meeting", "schedule", "job", "interview", "important", "hiring"]

while not done and step_count < 10:
    obs = data.get("observation", {})
    email = obs.get("current_email")

    if email is None:
        break

    subject = email["subject"].lower()
    body = email["body"].lower()
    text = subject + " " + body

    # 🧠 scoring system
    spam_score = sum(1 for word in SPAM_KEYWORDS if word in text)
    important_score = sum(1 for word in IMPORTANT_KEYWORDS if word in text)

    # 🏆 TOP 1% DECISION LOGIC
    if spam_score >= 2:
        action = {
            "action_type": "delete",
            "email_id": email["id"],
            "value": "spam"
        }

    elif important_score >= 2:
        action = {
            "action_type": "reply",
            "email_id": email["id"],
            "value": "important"
        }

    elif spam_score > important_score:
        action = {
            "action_type": "classify",
            "email_id": email["id"],
            "value": "spam"
        }

    elif important_score > spam_score:
        action = {
            "action_type": "classify",
            "email_id": email["id"],
            "value": "important"
        }

    else:
        # fallback safe action
        action = {
            "action_type": "classify",
            "email_id": email["id"],
            "value": "important"
        }

    print(f"[STEP] {action}")

    res = requests.post(f"{API_BASE_URL}/step", json={
    "action": action
})

    try:
        data = res.json()
        print("STEP:", data)
    except:
        print("STEP ERROR:", res.text)
        break

    done = data.get("done", True)
    step_count += 1

print("[END]")