import os
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

print("[START]")

# Reset environment
res = requests.post(f"{API_BASE_URL}/reset", json={
    "episode_id": "test-1",
    "seed": 42
})

data = res.json()
done = False
step_count = 0

while not done and step_count < 10:
    obs = data.get("observation", {})
    email = obs.get("current_email")

    if email is None:
        break

    subject = email.get("subject", "").lower()

    # 🔥 Simple agent logic (fixed)
    if "win" in subject:
        action = {
            "action_type": "classify",
            "email_id": email["id"],
            "value": "spam"
        }
    else:
        action = {
            "action_type": "classify",
            "email_id": email["id"],
            "value": "important"
        }

    print(f"[STEP] {action}")

    # Send action to environment
    res = requests.post(f"{API_BASE_URL}/step", json=action)

    # ✅ Safe JSON handling
    try:
        data = res.json()
    except:
        print("Error: Invalid response from server")
        break

    # ✅ Debug (important for hackathon validation)
    print("Response:", data)

    # ✅ Safe access (prevents crash)
    done = data.get("done", False)

    step_count += 1

print("[END]")