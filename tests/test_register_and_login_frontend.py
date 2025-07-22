# test_backend_pdf.py
import pytest
import requests
import uuid
import time
import traceback
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os

API_URL = "http://localhost:8001/api"

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
        print("[WARN] No se pudo cargar el escudo.")
    c.setFont("Helvetica-Bold", 16)
    c.drawString(120, alto - 50, "Universidad Nacional de Colombia")
    c.setFont("Helvetica", 12)
    c.drawString(120, alto - 70, "Reporte de Test – Cursos Backend - Teleteach")
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

def main():
    tiempo_inicio = time.time()
    resultado = False
    error_msg = None
    identifier = f"courses_backend_{int(time.time())}"

    try:
        # Ejecutar los tests de Pytest programáticamente
        exit_code = pytest.main(["-q", "--tb=short"])
        resultado = (exit_code == 0)
    except Exception:
        error_msg = traceback.format_exc()
    finally:
        tiempo_fin = time.time()
        generar_reporte_pdf(resultado, identifier, tiempo_inicio, tiempo_fin, error_msg)

# Llamada al runner principal
if __name__ == "__main__":
    main()
