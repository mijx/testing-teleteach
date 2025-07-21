# test_register_and_login.py

import pytest
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_register_and_login_flow():
    # Configuración del navegador
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    # Email único para evitar duplicados
    email = f"testuser{int(time.time())}@example.com"

    try:
        #### --- REGISTRO --- ####
        driver.get("http://localhost:5174/register")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Juan"]'))
        )

        driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Juan"]').send_keys("Juan")
        driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Pérez"]').send_keys("Pérez")
        driver.find_element(By.CSS_SELECTOR, 'input[placeholder="tu@email.com"]').send_keys(email)

        password_fields = driver.find_elements(By.CSS_SELECTOR, 'input[placeholder="••••••••"]')
        password_fields[0].send_keys("password123")
        password_fields[1].send_keys("password123")

        checkbox = driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
        driver.execute_script("arguments[0].click();", checkbox)

        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        assert "Usuario registrado correctamente" in alert.text
        alert.accept()

        WebDriverWait(driver, 5).until(EC.url_contains("/login"))
        assert "/login" in driver.current_url, f"No redirigió a /login. URL actual: {driver.current_url}"

        #### --- LOGIN --- ####
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="tu@email.com"]'))
        )

        driver.find_element(By.CSS_SELECTOR, 'input[placeholder="tu@email.com"]').send_keys(email)
        driver.find_element(By.CSS_SELECTOR, 'input[placeholder="••••••••"]').send_keys("password123")
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
        assert "/dashboard" in driver.current_url, f"No redirigió a /dashboard. URL actual: {driver.current_url}"

    finally:
        driver.quit()

        # 🔥 Cleanup: eliminar el usuario desde backend
        try:
            resp = requests.delete("http://localhost:5000/delete_user", params={"email": email})
            print(f"[INFO] Eliminando usuario {email} - Status: {resp.status_code}, Body: {resp.text}")
        except Exception as e:
            print(f"[ERROR] No se pudo eliminar el usuario {email}: {e}")
