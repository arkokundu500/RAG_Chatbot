import google.generativeai as genai
from typing import List, Optional
import os
from app.config import Config

class GoogleEmbeddings:
    def __init__(self):
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        self.model = Config.EMBEDDING_MODEL

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = []
        for text in texts:
            result = genai.embed_content(
                model=self.model,
                content=text,
                task_type="RETRIEVAL_DOCUMENT"
            )
            embeddings.append(result['embedding'])
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        result = genai.embed_content(
            model=self.model,
            content=text,
            task_type="RETRIEVAL_DOCUMENT"
        )
        return result['embedding']