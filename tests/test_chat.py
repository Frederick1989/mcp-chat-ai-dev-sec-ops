import os
import pytest
from fastapi.testclient import TestClient
import app.chatbot as chatbot_module

client = TestClient(chatbot_module.app)


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_chat_uses_context_and_returns_answer(monkeypatch):
    captured = {}

    def fake_chatbot(qa_input):
        # capture what the endpoint sends to the pipeline
        captured["qa_input"] = qa_input
        return {"answer": "Jon Jones is widely considered the GOAT"}

    # Replace the real pipeline with our fake
    monkeypatch.setattr(chatbot_module, "chatbot", fake_chatbot)

    question = "Who is the GOAT?"
    resp = client.post("/chat", json={"text": question})
    assert resp.status_code == 200
    assert resp.json()["reply"] == "Jon Jones is widely considered the GOAT"

    # verify the endpoint forwarded the correct question
    assert captured["qa_input"]["question"] == question

    # verify context was loaded from the context file
    context_path = os.path.join(os.path.dirname(chatbot_module.__file__), "context", "ufc_context.txt")
    with open(context_path, "r", encoding="utf-8") as f:
        expected_context = f.read()
    assert captured["qa_input"]["context"] == expected_context