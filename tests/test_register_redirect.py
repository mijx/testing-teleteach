# test_register_redirect.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import time

def test_register_redirects_to_login():
    # Configurar Chrome
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    try:
        # Navegar al formulario de registro
        driver.get("http://localhost:5174/register")

        # Esperar un momento para asegurar que cargue
        time.sleep(1)

        # Llenar campos
        driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Juan"]').send_keys("Juan")
        driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Pérez"]').send_keys("Pérez")
        email = f"juan{int(time.time())}@example.com"  # evitar duplicados
        driver.find_element(By.CSS_SELECTOR, 'input[placeholder="tu@email.com"]').send_keys(email)

        password_fields = driver.find_elements(By.CSS_SELECTOR, 'input[placeholder="••••••••"]')
        password_fields[0].send_keys("password123")
        password_fields[1].send_keys("password123")

        # Aceptar términos
        checkbox = driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
        driver.execute_script("arguments[0].click();", checkbox)

        # Enviar formulario
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Esperar y aceptar la alerta
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert_text = alert.text
        alert.accept()

        # Verificar redirección
        WebDriverWait(driver, 5).until(EC.url_contains("/login"))
        assert "/login" in driver.current_url, f"No redirigió a /login. URL actual: {driver.current_url}"

    finally:
        driver.quit()
