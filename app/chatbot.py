from fastapi import FastAPI, Request
from pydantic import BaseModel
from transformers import pipeline
import os

MODEL_NAME = os.getenv("MODEL_NAME", "microsoft/DialoGPT-small")
chatbot = pipeline("question-answering", model=MODEL_NAME)

app = FastAPI()

class Msg(BaseModel):
    text: str

CONTEXT_PATH = os.path.join(os.path.dirname(__file__), "context", "ufc_context.txt")
if os.path.exists(CONTEXT_PATH):
    with open(CONTEXT_PATH, "r", encoding="utf-8") as f:
        CONTEXT = f.read()
else:
    CONTEXT = "missing context"


@app.post("/chat")
def chat(msg: Msg):
    qa_input = {
        "question": msg.text,
        "context": CONTEXT  # Provide some context
    }
    result = chatbot(qa_input)
    # pipeline returns a dict like {"answer": "...", "score": ..., ...}
    answer = result.get("answer") if isinstance(result, dict) else str(result)
    return {"reply": answer}

@app.get("/")
def root():
    return {"status": "ok"}