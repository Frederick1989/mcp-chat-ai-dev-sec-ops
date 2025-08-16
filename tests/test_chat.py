from fastapi.testclient import TestClient
import app.chatbot as chatbot_module

client = TestClient(chatbot_module.app)
MOCK_ANSWER = "Jon Jones is widely considered the UFC GOAT"
PASSWORD = "OPEN_API_KEY"  # Mock key for testing the pipeline with gitleaks


def test_root():
    r = client.get("/")
    assert r.status_code == 200  # nosec B101
    assert r.json() == {"status": "ok"}  # nosec B101


def test_search_and_summarize(monkeypatch):
    # Mock DDGS search
    class MockDDGS:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def text(self, *args, **kwargs):
            return [{'body': 'Jon Jones is widely considered the UFC GOAT'}]

    monkeypatch.setattr('app.chatbot.DDGS', MockDDGS)

    # Mock summarization pipeline
    def mock_pipeline(*args, **kwargs):
        return lambda text, **kw: [{'summary_text': MOCK_ANSWER}]

    monkeypatch.setattr('app.chatbot.pipeline', mock_pipeline)

    response = client.post("/chat", json={"text": "Who is the UFC GOAT?"})
    assert response.status_code == 200   # nosec B101
    assert "Jon Jones" in response.json()["reply"]   # nosec B101
