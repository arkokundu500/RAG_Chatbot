from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasicCredentials
from app.auth import security, authenticate_user
from app.rag import RAGSystem
from pydantic import BaseModel

app = FastAPI()
rag_system = RAGSystem()

class Query(BaseModel):
    message: str

@app.post("/chat")
async def chat(
    query: Query, 
    credentials: HTTPBasicCredentials = Depends(security)
):
    user = authenticate_user(credentials)
    try:
        response = rag_system.generate_response(query.message, user["access"])
        return {"response": response}
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error generating response: {str(e)}"
        )