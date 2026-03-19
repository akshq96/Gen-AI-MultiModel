import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Load env variables (GEMINI_API_KEY, GCS credentials)
from pathlib import Path
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from agent_controller import AgentController

app = FastAPI(title="Multimodal Creative Director AI API")

# Allow CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    prompt: str
    image_reference: str | None = None

@app.post("/generate-story")
async def generate_story(req: GenerateRequest):
    controller = AgentController()

    try:
        result = []

        async for chunk in controller.stream_experience(req.prompt, req.image_reference):
            result.append(chunk)

        return {"output": result}

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    # Make sure to run from project root: python -m backend.main
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
