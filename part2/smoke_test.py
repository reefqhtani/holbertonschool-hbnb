from app import create_app

app = create_app()

with app.test_client() as client:
    resp = client.get("/api/v1/health/")
    print("STATUS:", resp.status_code)
    print("JSON:", resp.get_json())
