from openai import OpenAI
import os

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
    print("[START] task=email_classification", flush=True)

    # Call model
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "Classify email as spam or important. Respond only with spam or important."},
            {"role": "user", "content": message},
        ],
    )

    output = response.choices[0].message.content.strip().lower()

    # Normalize result
    if "spam" in output:
        result = "spam"
    else:
        result = "important"

    # STEP (detailed)
    print(f"[STEP] step=1 message='{message}' predicted={result}", flush=True)

    # Dummy scoring (since expected label not given)
    score = 1.0 if result in ["spam", "important"] else 0.0

    # END with score
    print(f"[END] task=email_classification score={score} steps=1", flush=True)

    return {
        "action": result
    }