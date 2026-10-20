
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.api.routes import router

load_dotenv()

app = FastAPI(
    title="Global Life Assurance Policy Assistant",
    description="Secure RAG-based insurance policy Q&A assistant",
    version="1.0.0",
)

app.include_router(router)

FRONTEND_DIR = Path(__file__).resolve().parents[1] / "frontend"

app.mount(
    "/",
    StaticFiles(directory=str(FRONTEND_DIR), html=True),
    name="frontend",
)
