# embeddings/gemini_embedding.py

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

class GeminiEmbeddings(GoogleGenerativeAIEmbeddings):

    def __init__(self):
        super().__init__(model="gemini-embedding-2-preview")