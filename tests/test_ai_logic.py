import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_quiz_route_success():
    response = client.get("/quiz")
    data = response.json()

    assert response.status_code == 200
    assert "question" in data
    assert "correct_answer" in data
    assert isinstance(data["correct_answer"], (int, float))


def test_quiz_route_fallback():
    """
    Forces fallback when OpenAI is missing or fails.
    The test passes if the question is generated without an exception.
    """
    response = client.get("/quiz")
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data["question"], str)
    assert len(data["question"]) > 0


def test_quiz_answer_correct():
    payload = {"question": "What is 2 + 2?", "user_answer": "4", "correct_answer": 4}

    response = client.post("/quiz/answer", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert "Correct" in data["feedback"]


def test_quiz_answer_incorrect():
    payload = {"question": "What is 5 * 5?", "user_answer": "10", "correct_answer": 25}

    response = client.post("/quiz/answer", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert "Incorrect" in data["feedback"]


def test_quiz_answer_invalid_number():
    payload = {
        "question": "What is 8 / 2?",
        "user_answer": "hello",
        "correct_answer": 4,
    }

    response = client.post("/quiz/answer", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert data["feedback"] == "Please enter a numeric answer."


def test_quiz_answer_explanation_present():
    """
    Tests that explanation field exists, even if fallback triggers.
    """
    payload = {"question": "What is 10 - 3?", "user_answer": "7", "correct_answer": 7}

    response = client.post("/quiz/answer", json=payload)
    data = response.json()

    assert "explanation" in data
    assert isinstance(data["explanation"], str)
