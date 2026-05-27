from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mokusei_ai.api.router import router as agent_router

app = FastAPI(
    title="Mokusei AI",
    version="0.1.0",
    description="AI service backend with specialized agents (moons). Each moon serves a specific purpose — Ganymede is a portfolio assistant, others handle different domains.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agent_router, prefix="/api")