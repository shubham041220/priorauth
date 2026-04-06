import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model_id = "gemini-2.0-flash" 

    def chat(self, system_instruction, user_content):
        response = self.client.models.generate_content(
            model=self.model_id,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0,
                response_mime_type="application/json" # Forces JSON output
            ),
            contents=user_content
        )
        return response.text

