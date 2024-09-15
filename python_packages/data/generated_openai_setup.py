# generated in file ipython.ipynb

import os

from dotenv import load_dotenv, find_dotenv
from openai import OpenAI


load_dotenv(find_dotenv())
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

client = OpenAI(api_key=openai_api_key)


def openai_request(prompt, system=None, model="gpt-3.5-turbo") -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system or "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()
