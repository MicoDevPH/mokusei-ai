from fastapi import FastAPI
from mokusei_ai.api.router import router as agent_router

app = FastAPI()

app.include_router(agent_router, prefix="/api")