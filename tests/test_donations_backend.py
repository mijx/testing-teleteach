import pytest
import requests
import time
from datetime import datetime, timezone

BASE_URL = "http://localhost:8888"
DONATE_URL = f"{BASE_URL}/donate"
GET_DONATIONS_URL = f"{BASE_URL}/donations"
DELETE_DONATION_URL = f"{BASE_URL}/delete_donation"

# Datos de prueba únicos basados en timestamp
TEST_EMAIL = f"testdonor{int(time.time())}@example.com"
TEST_DONATION = {
    "email": TEST_EMAIL,
    "paymentMethod": "Tarjeta de crédito",
    "amount": 100,
    "donationDate": datetime.now(timezone.utc).isoformat()
}

# Variable global para guardar el ID de la donación creada
donation_id = None

@pytest.fixture(scope="module", autouse=True)
def cleanup():
    """Elimina la donación creada al final del módulo."""
    yield
    if donation_id:
        try:
            res = requests.delete(DELETE_DONATION_URL, params={"id": donation_id})
            print(f"[CLEANUP] Donación eliminada: {res.status_code} - {res.text}")
        except Exception as e:
            print(f"[CLEANUP] Falló al eliminar donación: {e}")

def test_create_donation_success():
    global donation_id
    res = requests.post(DONATE_URL, json=TEST_DONATION)
    assert res.status_code == 201
    body = res.json()
    assert "donation_id" in body
    assert body["msg"] == "Donación registrada exitosamente"
    donation_id = body["donation_id"]

def test_get_donations_by_email():
    res = requests.get(GET_DONATIONS_URL, params={"email": TEST_EMAIL})
    assert res.status_code == 200
    body = res.json()
    assert isinstance(body, list)
    assert any(d["email"] == TEST_EMAIL for d in body)

def test_get_donations_missing_email():
    res = requests.get(GET_DONATIONS_URL)
    assert res.status_code == 400
    assert "Falta el parámetro" in res.json()["msg"]

def test_delete_donation_success():
    global donation_id
    assert donation_id is not None, "Se requiere una donación para esta prueba"
    res = requests.delete(DELETE_DONATION_URL, params={"id": donation_id})
    assert res.status_code == 200
    assert f"Donación {donation_id} eliminada" in res.json()["msg"]
    donation_id = None  # ya fue eliminada

def test_delete_donation_not_found():
    fake_id = "000000000000000000000000"  # ObjectId inválido (no existente)
    res = requests.delete(DELETE_DONATION_URL, params={"id": fake_id})
    assert res.status_code == 404
    assert "Donación no encontrada" in res.json()["msg"]

def test_error_route():
    res = requests.get(f"{BASE_URL}/error")
    assert res.status_code == 500
    assert "Algo falló" in res.text
