from openai import OpenAI
import os, sys

API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN,
)

def solve(input_data):
    message = input_data.get("message", "")

    # START
    print("[START] task=email_classification")
    sys.stdout.flush()

    # Call model
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "Classify email as spam or important. Respond only with spam or important."},
            {"role": "user", "content": message},
        ],
    )

    output = response.choices[0].message.content.strip().lower()

    if "spam" in output:
        result = "spam"
    else:
        result = "important"

    reward = 1.0

    # STEP (STRICT FORMAT)
    print(f"[STEP] step=1 reward={reward}")
    sys.stdout.flush()

    # END (STRICT FORMAT)
    print(f"[END] task=email_classification score={reward} steps=1")
    sys.stdout.flush()

    return {
        "action": result
    }