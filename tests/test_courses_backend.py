import pytest
import requests
import uuid
from datetime import datetime, timezone

API_URL = "http://localhost:8001/api"

@pytest.fixture(scope="module")
def test_data():
    return {
        "course": {
            "title": "Curso de Prueba",
            "description": "Curso generado automáticamente para pruebas.",
            "level": "intermedio"
        },
        "user_id": f"user_{uuid.uuid4().hex[:8]}",
        "progress_id": None,
        "course_id": None
    }

def test_create_course(test_data):
    res = requests.post(f"{API_URL}/courses", json=test_data["course"])
    assert res.status_code == 200
    json = res.json()
    assert "Curso creado exitosamente" in json["message"]
    test_data["course_id"] = json["id"]

def test_get_all_courses(test_data):
    res = requests.get(f"{API_URL}/courses")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    assert any(course["id"] == test_data["course_id"] for course in res.json())

def test_get_course_by_id(test_data):
    res = requests.get(f"{API_URL}/courses/{test_data['course_id']}")
    assert res.status_code == 200
    data = res.json()
    assert data["title"] == test_data["course"]["title"]

def test_register_progress(test_data):
    payload = {
        "topic": "tema-1",
        "completed": True
    }
    res = requests.post(f"{API_URL}/courses/{test_data['course_id']}/progress", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "registrado" in data["message"]
    test_data["progress_id"] = data["id"]  # Para usar en test_delete_progress


def test_get_user_progress_not_found(test_data):
    res = requests.get(f"{API_URL}/courses/user/{test_data['user_id']}/progress")
    assert res.status_code == 404  # porque solo se guarda en 'progress', no en 'user_progress'

def test_delete_progress(test_data):
    assert test_data.get("progress_id"), "No se registró un progreso válido para eliminar"
    res = requests.delete(f"{API_URL}/progress/{test_data['progress_id']}")
    assert res.status_code == 200
    assert f"Progreso con ID {test_data['progress_id']} eliminado" in res.json()["message"]

def test_delete_course(test_data):
    res = requests.delete(f"{API_URL}/courses/{test_data['course_id']}")
    assert res.status_code == 200
    assert f"Curso con ID {test_data['course_id']} eliminado" in res.json()["message"]

def test_delete_user_progress(test_data):
    res = requests.delete(f"{API_URL}/courses/user/{test_data['user_id']}/progress")
    # Aunque no se creó en user_progress, lo intentamos para limpieza
    assert res.status_code in [200, 404]
