import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Beautiful Logging Imports
from rich.console import Console
from rich.panel import Panel
from rich.logging import RichHandler
import logging
from logger import MokuseiLogger
# --- Setup Jupiter-Themed Logger ---
console = Console()
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("rich")

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = ChatOpenAI(
    model="gpt-4o-mini", 
    openai_api_key=os.getenv("GITHUB_TOKEN"), 
    base_url="https://models.inference.ai.azure.com" 
)

def load_prompt(filename):
    path = os.path.join("prompt", filename)
    with open(path, "r") as f:
        return f.read()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Use your custom logger methods
        MokuseiLogger.log_request(request.message)
        
        persona = load_prompt("persona.xml")
        instructions = load_prompt("mokusei_instructions.xml")
        
        messages = [
            SystemMessage(content=f"PERSONA:\n{persona}\n\nINSTRUCTIONS:\n{instructions}"),
            HumanMessage(content=request.message)
        ]
        
        MokuseiLogger.log_info("Processing atmospheric data...")
        
        response = llm.invoke(messages)
        
        MokuseiLogger.log_success("Transmission successful. Data returned to orbit.")
        
        return {"reply": response.content}
        
    except Exception as e:
        MokuseiLogger.log_error(str(e))
        return {"reply": "Connection lost to planetary core."}
