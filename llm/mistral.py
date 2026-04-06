import os
import time
from openai import OpenAI
from dotenv import load_dotenv
from llm.llmprotocol import LLMPROTOCOL

load_dotenv()

class LLMClient:
    def __init__(self):
        # Point the OpenAI client to Mistral's endpoint
        self.client = OpenAI(
            api_key=os.getenv("MISTRAL_API_KEY"),
            base_url="https://api.mistral.ai/v1"
        )
        self.model = "mistral-large-latest"

    def chat(self, system_instruction, user_content):
        """
        Sends prompts to Mistral via the OpenAI-compatible SDK.
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": user_content}
                    ],
                    # This tells Mistral to return ONLY valid JSON
                    response_format={"type": "json_object"}
                )
                return response.choices[0].message.content

            except Exception as e:
                # Handle Mistral's Free Tier Rate Limit (2 requests per minute)
                if "429" in str(e) and attempt < max_retries - 1:
                    print(f"⚠️ Mistral Rate Limit hit. Retrying in 30s... (Attempt {attempt+1})")
                    time.sleep(30)
                else:
                    print(f"❌ LLM Error: {e}")
                    return None
