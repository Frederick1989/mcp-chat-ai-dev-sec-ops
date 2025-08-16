from fastapi import FastAPI, Request
from pydantic import BaseModel
from transformers import pipeline
from duckduckgo_search import DDGS  # Changed from ddg to DDGS
import os

MODEL_NAME = os.getenv("MODEL_NAME", "facebook/bart-large-cnn")
chatbot = None

def search_and_summarize(question: str) -> str:
    """Search DuckDuckGo and summarize results"""
    # Create a DDGS instance and search
    with DDGS() as ddgs:
        results = list(ddgs.text(f"UFC {question}", max_results=3))
    
    if not results:
        return "No search results found"
    
    # Combine search results
    context = " ".join([r.get('body', '') for r in results])
    
    # Load summarizer if needed
    global chatbot
    if chatbot is None:
        chatbot = pipeline("summarization", model=MODEL_NAME)
    
    # Summarize search results
    summary = chatbot(context, max_length=100, min_length=30, do_sample=False)
    return summary[0]['summary_text']

app = FastAPI()

class Msg(BaseModel):
    text: str

@app.post("/chat")
async def chat(msg: Msg):
    try:
        answer = search_and_summarize(msg.text)
        return {"reply": answer}
    except Exception as e:
        return {"reply": f"Error: {str(e)}", "error": True}

@app.get("/")
def root():
    return {"status": "ok"}