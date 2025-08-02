from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.routes import ai
from app.services.db import Base, engine, get_db

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Agentic Medical Assistant API",
    description="Backend for AI-powered triage and symptom analysis",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(ai.router, prefix="/api", tags=["AI"])
