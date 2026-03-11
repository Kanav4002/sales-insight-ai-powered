from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_returns_healthy():
  response = client.get("/health")
  assert response.status_code == 200
  assert response.json() == {"status": "healthy"}


def test_upload_missing_fields_returns_422():
  response = client.post("/api/upload", files={})
  assert response.status_code == 422


def test_upload_invalid_extension_rejected(tmp_path: Path):
  sample_file = tmp_path / "data.txt"
  sample_file.write_text("Header1,Header2\n1,2\n")

  with sample_file.open("rb") as f:
    response = client.post(
      "/api/upload",
      files={"file": ("data.txt", f, "text/plain")},
      data={"email": "user@example.com"},
    )

  assert response.status_code == 400
  body = response.json()
  assert isinstance(body, dict)
  assert body.get("detail") is not None

