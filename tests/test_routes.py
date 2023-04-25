import json

from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.main import app

client = TestClient(app)


def test_upload():
    response = client.post("/documents/upload")
    assert response.status_code == 200
    assert response.json() == {"detail": "Document uploaded successfully."}


def test_login():
    response = client.post("/auth/login")
    assert response.status_code == 200
