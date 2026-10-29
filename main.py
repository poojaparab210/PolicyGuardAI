
from fastapi import FastAPI

from app.routes.health import router as health_router
from app.routes.policies import router as policies_router
from app.routes.document_analysis import router as document_analysis_router

app = FastAPI(
    title="PolicyGuard AI",
    description="AI-powered policy analysis using NLP, LLMs, and RAG.",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(policies_router)
app.include_router(document_analysis_router)
