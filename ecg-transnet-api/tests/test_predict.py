from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_predict_invalid_file():
    response = client.post(
        "/api/v1/predict",
        files={"file": ("test.pdf", b"fake content", "application/pdf")},
    )
    assert response.status_code == 400

def test_predict_valid_csv():
    csv_content = "\n".join([str(i * 0.01) for i in range(1000)])
    response = client.post(
        "/api/v1/predict",
        files={"file": ("ecg.csv", csv_content.encode(), "text/csv")},
    )
    assert response.status_code == 200
    data = response.json()
    assert "predicted_class" in data
    assert "confidence" in data
