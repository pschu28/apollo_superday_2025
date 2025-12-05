from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def test_create():
    payload = {
        "manufacturer_name": "manufacturer",
        "description": "descr",
        "horse_power": 10,
        "model_name": "name",
        "model_year": 20,
        "purchase_price": 1.5,
        "fuel_type": "fast"
    }
    post_response = client.post("/vehicle", json=payload)

    assert post_response.status_code == 201
    post_data = post_response.json()
    assert "vin" in post_data
    assert post_data["manufacturer_name"] == payload["manufacturer_name"]
    assert post_data["description"] == payload["description"]
    assert post_data["horse_power"] == payload["horse_power"]
    assert post_data["model_name"] == payload["model_name"]
    assert post_data["model_year"] == payload["model_year"]
    assert post_data["purchase_price"] == payload["purchase_price"]
    assert post_data["fuel_type"] == payload["fuel_type"]

def test_empty_payload():
    response = client.post("/vehicle", json={})
    assert response.status_code == 422

def test_malformed_payload():
    payload = {
        "manufacturer_name": 20
    }
    response = client.post("/vehicle", json=payload)
    assert response.status_code == 422

def test_get_by_id():
    payload = {
        "manufacturer_name": "manufacturer",
        "description": "descr",
        "horse_power": 10,
        "model_name": "name",
        "model_year": 20,
        "purchase_price": 1.5,
        "fuel_type": "fast"
    }
    post_response = client.post("/vehicle", json=payload)
    post_data = post_response.json()
    # use .lower() with the vin to check for case sensitivity since
    # by default, all vins are in upper case
    get_response = client.get(f"/vehicle/{post_data["vin"].lower()}")
    assert get_response.status_code == 200
    get_data = get_response.json()
    assert get_data["vin"] == post_data["vin"]
    assert get_data["manufacturer_name"] == payload["manufacturer_name"]
    assert get_data["description"] == payload["description"]
    assert get_data["horse_power"] == payload["horse_power"]
    assert get_data["model_name"] == payload["model_name"]
    assert get_data["model_year"] == payload["model_year"]
    assert get_data["purchase_price"] == payload["purchase_price"]
    assert get_data["fuel_type"] == payload["fuel_type"]

def test_put():
    payload = {
        "manufacturer_name": "manufacturer",
        "description": "descr",
        "horse_power": 10,
        "model_name": "name",
        "model_year": 20,
        "purchase_price": 1.5,
        "fuel_type": "fast"
    }
    post_response = client.post("/vehicle", json=payload)
    post_data = post_response.json()
    changed_payload = {
        "manufacturer_name": "abc"
    }
    put_response = client.put(f"/vehicle/{post_data["vin"].lower()}", json=changed_payload)
    assert put_response.status_code == 200
    put_data = put_response.json()
    assert put_data["vin"] == post_data["vin"]
    assert put_data["manufacturer_name"] == changed_payload["manufacturer_name"]
    assert put_data["description"] == payload["description"]
    assert put_data["horse_power"] == payload["horse_power"]
    assert put_data["model_name"] == payload["model_name"]
    assert put_data["model_year"] == payload["model_year"]
    assert put_data["purchase_price"] == payload["purchase_price"]
    assert put_data["fuel_type"] == payload["fuel_type"]

def test_delete():
    payload = {
        "manufacturer_name": "manufacturer",
        "description": "descr",
        "horse_power": 10,
        "model_name": "name",
        "model_year": 20,
        "purchase_price": 1.5,
        "fuel_type": "fast"
    }
    post_response = client.post("/vehicle", json=payload)
    post_data = post_response.json()

    delete_response = client.delete(f"/vehicle/{post_data["vin"].lower()}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/vehicle/{post_data["vin"].lower()}")
    assert get_response.status_code == 404

def test_get_all():
    payload = {
        "manufacturer_name": "manufacturer",
        "description": "descr",
        "horse_power": 10,
        "model_name": "name",
        "model_year": 20,
        "purchase_price": 1.5,
        "fuel_type": "fast"
    }
    post_response = client.post("/vehicle", json=payload)
    get_response = client.get("/vehicle/")
    get_data = get_response.json()

    assert get_response.status_code == 200
    assert len(get_data) >= 1
