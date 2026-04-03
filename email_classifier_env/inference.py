import os
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

print("[START]")

# ✅ RESET
res = requests.post(f"{API_BASE_URL}/reset", json={})
print("RESET:", res.text)

data = res.json()

done = data.get("done", False)
step_count = 0

while not done and step_count < 10:
    obs = data.get("observation", {})
    email = obs.get("current_email")

    if not email:
        break

    subject = email["subject"].lower()

    # simple agent
    if "win" in subject:
        value = "spam"
    else:
        value = "important"

    action = {
        "action_type": "classify",
        "email_id": email["id"],
        "value": value
    }

    print("[STEP]", action)

    # ✅ IMPORTANT FIX (correct payload)
    res = requests.post(
        f"{API_BASE_URL}/step",
        json={
            "action": action,
            "session_id": data.get("session_id")   # 🔥 REQUIRED
        }
    )

    print("STEP:", res.text)

    try:
        data = res.json()
    except:
        print("ERROR parsing response")
        break

    done = data.get("done", False)
    step_count += 1

print("[END]")