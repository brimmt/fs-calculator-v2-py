import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_calculate_add():
    response = client.get(
        "/calculate", params={"num1": 2, "num2": 3, "operation": "add"}
    )
    data = response.json()
    assert response.status_code == 200
    assert data["result"] == 5


def test_calculate_subtract():
    response = client.get(
        "/calculate", params={"num1": 2, "num2": 3, "operation": "subtract"}
    )
    data = response.json()
    assert response.status_code == 200
    assert data["result"] == -1


def test_calculate_multiply():
    response = client.get(
        "/calculate", params={"num1": 10, "num2": 5, "operation": "multiply"}
    )
    data = response.json()
    assert response.status_code == 200
    assert data["result"] == 50


def test_calculate_divide():
    response = client.get(
        "/calculate", params={"num1": 10, "num2": 5, "operation": "divide"}
    )
    data = response.json()
    assert response.status_code == 200
    assert data["result"] == 2


def test_calculate_power():
    response = client.get(
        "/calculate", params={"num1": 2, "num2": 2, "operation": "power"}
    )
    data = response.json()
    assert response.status_code == 200
    assert data["result"] == 4
