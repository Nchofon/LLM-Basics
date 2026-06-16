import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url=os.environ["API_URL"],
    api_key=os.environ["API_KEY"],
)

response = client.chat.completions.create(
    model=os.environ["API_MODEL"],
    messages=[{"role": "user", "content": "Say hello in one sentence."}],
)

print(response.choices[0].message.content)
