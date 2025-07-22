import requests
import time
import pytest

BASE_URL = "http://localhost:5000"
REGISTER_URL = f"{BASE_URL}/register"
DELETE_URL = f"{BASE_URL}/delete_user"

# Email único basado en timestamp para evitar colisiones
TEST_EMAIL = f"testuser{int(time.time())}@example.com"
TEST_USER = {
    "full_name": "Test User",
    "email": TEST_EMAIL,
    "password": "securepass123"
}

@pytest.fixture(scope="module")
def cleanup_user():
    yield
    # Cleanup final: borrar el usuario si quedó creado
    try:
        res = requests.delete(DELETE_URL, params={"email": TEST_EMAIL})
        print(f"[CLEANUP] Usuario eliminado: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"[CLEANUP] Falló al eliminar usuario: {e}")

def test_create_user_success(cleanup_user):
    res = requests.post(REGISTER_URL, json=TEST_USER)
    assert res.status_code == 201
    assert "Usuario registrado exitosamente" in res.json()["msg"]

def test_create_user_duplicate(cleanup_user):
    res = requests.post(REGISTER_URL, json=TEST_USER)
    assert res.status_code == 400
    assert "ya está registrado" in res.json()["msg"]

def test_login_success(cleanup_user):
    login_payload = {
        "email": TEST_USER["email"],
        "password": TEST_USER["password"]
    }
    response = requests.post(f"{BASE_URL}/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["msg"] == "Inicio de sesión exitoso"
    assert data["user"]["email"] == TEST_USER["email"]
    assert data["user"]["full_name"] == TEST_USER["full_name"]


def test_delete_user_success(cleanup_user):
    res = requests.delete(DELETE_URL, params={"email": TEST_EMAIL})
    assert res.status_code == 200
    assert f"Usuario con correo {TEST_EMAIL} eliminado" in res.json()["msg"]
