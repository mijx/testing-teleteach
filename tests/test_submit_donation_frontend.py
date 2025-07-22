import time
import requests
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from datetime import datetime
import os

def generar_reporte_pdf(resultado, identifier, tiempo_inicio, tiempo_fin, error=None):
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    nombre_archivo = os.path.join(reports_dir, f"reporte_{identifier}_{timestamp}.pdf")
    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    ancho, alto = letter
    escudo_path = "Escudo_de_la_Universidad_Nacional_de_Colombia.png"
    try:
        escudo = ImageReader(escudo_path)
        c.drawImage(escudo, 50, alto - 80, width=50, height=50, mask='auto')
    except Exception:
        pass
    c.setFont("Helvetica-Bold", 16)
    c.drawString(120, alto - 50, "Universidad Nacional de Colombia")
    c.setFont("Helvetica", 12)
    c.drawString(120, alto - 70, "Reporte de Test – Donación Frontend - Teleteach")
    c.line(50, alto - 85, ancho - 50, alto - 85)
    y = alto - 110
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Fecha: {datetime.now():%Y-%m-%d %H:%M:%S}")
    y -= 20
    c.drawString(50, y, f"Identificador: {identifier}")
    y -= 20
    c.drawString(50, y, f"Resultado: {'✅ Éxito' if resultado else '❌ Fallo'}")
    y -= 20
    c.drawString(50, y, f"Duración: {round(tiempo_fin - tiempo_inicio, 2)} segundos")
    y -= 30
    if error:
        c.drawString(50, y, "Detalle del error:")
        y -= 20
        for line in error.splitlines():
            c.drawString(70, y, line[:90])
            y -= 15
            if y < 50:
                c.showPage()
                y = alto - 50
    c.save()
    print(f"[INFO] Reporte PDF guardado en: {nombre_archivo}")

def test_register_login_and_donate():
    tiempo_inicio = time.time()
    resultado = False
    error_msg = None
    identifier = f"donation_frontend_{int(time.time())}"
    email = f"testuser{int(time.time())}@example.com"
    password = "password123"
    donation_amount = 42
    base_url = "http://localhost:5173"
    api_url = "http://localhost:5000"
    donation_api_url = "http://localhost:8888"

    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    donation_id = None

    try:
        driver.get(f"{base_url}/register")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Juan"]')))
        driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Juan"]').send_keys("Juan")
        driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Pérez"]').send_keys("Pérez")
        driver.find_element(By.CSS_SELECTOR, 'input[placeholder="tu@email.com"]').send_keys(email)
        pass_fields = driver.find_elements(By.CSS_SELECTOR, 'input[placeholder="••••••••"]')
        pass_fields[0].send_keys(password)
        pass_fields[1].send_keys(password)
        checkbox = driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
        driver.execute_script("arguments[0].click();", checkbox)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        assert "Usuario registrado correctamente" in alert.text
        alert.accept()
        WebDriverWait(driver, 10).until(EC.url_contains("/login"))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="tu@email.com"]')))
        driver.find_element(By.CSS_SELECTOR, 'input[placeholder="tu@email.com"]').send_keys(email)
        driver.find_element(By.CSS_SELECTOR, 'input[placeholder="••••••••"]').send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
        driver.get(f"{base_url}/")
        apoyar_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Apoyar la Plataforma')]"))
        )
        apoyar_btn.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/donations"))
        custom_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Donar Cantidad Personalizada')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", custom_btn)
        driver.execute_script("arguments[0].click();", custom_btn)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h3[contains(., 'Selecciona el monto')]"))
        )
        input_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Cantidad personalizada']"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
        input_field.click()
        input_field.clear()
        input_field.send_keys(str(donation_amount))
        written = input_field.get_attribute("value")
        assert written == str(donation_amount), f"Input incorrecto: {written}"
        donar_ahora_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="donate-submit-button"]'))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", donar_ahora_btn)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", donar_ahora_btn)
        WebDriverWait(driver, 7).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        assert "¡Gracias por tu donación" in alert.text
        alert.accept()
        for _ in range(10):
            response = requests.get(f"{donation_api_url}/donations", params={"email": email})
            if response.status_code == 200 and response.json():
                donation_id = response.json()[0]["_id"]
                break
            time.sleep(1)
        assert donation_id, f"No se encontraron donaciones para el correo {email}"
        resultado = True
    except Exception:
        error_msg = traceback.format_exc()
        raise
    finally:
        driver.quit()
        if donation_id:
            try:
                requests.delete(f"{donation_api_url}/delete_donation", params={"id": donation_id})
            except:
                pass
        try:
            requests.delete(f"{api_url}/delete_user", params={"email": email})
        except:
            pass
        tiempo_fin = time.time()
        generar_reporte_pdf(resultado, identifier, tiempo_inicio, tiempo_fin, error_msg)
