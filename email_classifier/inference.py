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
    # Get email message
    message = input_data.get("message", "")

    # Call LLM
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "Classify the email as spam or important. Respond only with 'spam' or 'important'."},
            {"role": "user", "content": message},
        ],
    )

    output = response.choices[0].message.content.strip().lower()

    # Ensure valid output
    if "spam" in output:
        result = "spam"
    else:
        result = "important"

    # ✅ REQUIRED FORMAT
    return {
        "action": result
    }