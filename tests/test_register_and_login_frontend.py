import pytest
import requests
import time
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

def generar_reporte_pdf(resultado, email, tiempo_inicio, tiempo_fin, error=None):
    # Asegurar que existe carpeta reports
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)

    # Nombre y ruta del PDF
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    nombre_archivo = os.path.join(reports_dir, f"reporte_test_{timestamp}.pdf")
    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    ancho, alto = letter

    # --- Membrete con escudo ---
    escudo_path = "Escudo_de_la_Universidad_Nacional_de_Colombia.png"
    try:
        escudo = ImageReader(escudo_path)
        c.drawImage(escudo, 50, alto - 80, width=50, height=50, mask='auto')
    except Exception:
        # Si no encuentra imagen, continuar sin escudo
        pass

    # Título del membrete
    c.setFont("Helvetica-Bold", 16)
    c.drawString(120, alto - 50, "Universidad Nacional de Colombia")
    c.setFont("Helvetica", 12)
    c.drawString(120, alto - 70, "Reporte de Test – Registro y Login - Teleteach")

    # Línea de separación
    c.line(50, alto - 85, ancho - 50, alto - 85)

    # --- Contenido principal ---
    y = alto - 110
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Fecha: {datetime.now():%Y-%m-%d %H:%M:%S}")
    y -= 20
    c.drawString(50, y, f"Email utilizado: {email}")
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

def test_register_and_login_flow():
    tiempo_inicio = time.time()
    resultado = False
    error_msg = None
    email = f"testuser{int(time.time())}@example.com"

    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    try:
        #### --- REGISTRO --- ####
        driver.get("http://localhost:5173/register")
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
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
        assert "/dashboard" in driver.current_url, f"No redirigió a /dashboard. URL actual: {driver.current_url}"

        resultado = True

    except Exception:
        error_msg = traceback.format_exc()
        raise

    finally:
        driver.quit()
        tiempo_fin = time.time()

        try:
            resp = requests.delete("http://localhost:5000/delete_user", params={"email": email})
            print(f"[INFO] Eliminando usuario {email} - Status: {resp.status_code}, Body: {resp.text}")
        except Exception as e:
            print(f"[ERROR] No se pudo eliminar el usuario {email}: {e}")

        generar_reporte_pdf(resultado, email, tiempo_inicio, tiempo_fin, error=error_msg)
