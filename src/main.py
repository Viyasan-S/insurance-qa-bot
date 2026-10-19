from dotenv import load_dotenv
from fastapi import FastAPI
from src.api.routes import router

load_dotenv()

app = FastAPI(
    title="Global Life Assurance Policy Assistant",
    description="Secure RAG demo using ChromaDB and Ollama",
    version="1.0.0",
)

app.include_router(router)