from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from app.config import Config
import google.generativeai as genai
from app.custom_embeddings import GoogleEmbeddings

class RAGSystem:
    def __init__(self):
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        self.embeddings = GoogleEmbeddings()
        self.vector_stores = self.load_vector_stores()
        
    def load_vector_stores(self):
        stores = {}
        for collection in ["engineering", "finance", "marketing", "hr", "general"]:
            try:
                stores[collection] = Chroma(
                    persist_directory=f"{Config.CHROMA_PATH}/{collection}",
                    embedding_function=self.embeddings
                )
            except:
                stores[collection] = None
        return stores
    
    def generate_response(self, query: str, collections: list):
        docs = []
        for collection in collections:
            if self.vector_stores[collection]:
                retriever = self.vector_stores[collection].as_retriever()
                docs.extend(retriever.get_relevant_documents(query))
        
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # Generate response using Gemini
        model = genai.GenerativeModel(Config.LLM_MODEL)
        prompt = f"""
        You are a helpful assistant for FinSolve Technologies. 
        Use the following context to answer the question. 
        If the question is outside the context, politely decline to answer.
        Always reference the source document in your response.
        
        Context: {context}
        
        Question: {query}
        
        Answer:
        """
        
        response = model.generate_content(prompt)
        return response.text