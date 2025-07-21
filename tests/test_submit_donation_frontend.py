# import time
# import requests
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC


# def test_register_login_and_donate():
#     email = f"testuser{int(time.time())}@example.com"
#     password = "password123"
#     donation_amount = 42  # personalizado
#     base_url = "http://localhost:5174"
#     api_url = "http://localhost:5000"

#     options = Options()
#     options.add_argument("--start-maximized")
#     driver = webdriver.Chrome(options=options)

#     donation_id = None

#     try:
#         # -------- Registro --------
#         driver.get(f"{base_url}/register")

#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Juan"]')))
#         driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Juan"]').send_keys("Juan")
#         driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Pérez"]').send_keys("Pérez")
#         driver.find_element(By.CSS_SELECTOR, 'input[placeholder="tu@email.com"]').send_keys(email)

#         pass_fields = driver.find_elements(By.CSS_SELECTOR, 'input[placeholder="••••••••"]')
#         pass_fields[0].send_keys(password)
#         pass_fields[1].send_keys(password)

#         checkbox = driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
#         driver.execute_script("arguments[0].click();", checkbox)

#         driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

#         WebDriverWait(driver, 5).until(EC.alert_is_present())
#         alert = driver.switch_to.alert
#         assert "Usuario registrado correctamente" in alert.text
#         alert.accept()

#         WebDriverWait(driver, 10).until(EC.url_contains("/login"))

#         # -------- Login --------
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="tu@email.com"]')))
#         driver.find_element(By.CSS_SELECTOR, 'input[placeholder="tu@email.com"]').send_keys(email)
#         driver.find_element(By.CSS_SELECTOR, 'input[placeholder="••••••••"]').send_keys(password)
#         driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

#         WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))

#         # -------- Donación desde home --------
#         driver.get(f"{base_url}/")  # ir al root

#         # Esperar que aparezca el botón de "Apoyar la Plataforma"
#         apoyar_btn = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Apoyar la Plataforma')]"))
#         )
#         apoyar_btn.click()

#         # Esperar que haya redirigido a la página de donaciones
#         WebDriverWait(driver, 10).until(EC.url_contains("/donations"))

#                 # -------- Donación personalizada --------
#         # Esperar que aparezca el botón de "Donar Cantidad Personalizada"
#                 # Esperar que el botón esté presente en DOM
#         custom_btn = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Donar Cantidad Personalizada')]"))
#         )

#         # Scroll hacia el botón para evitar intercepción
#         driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", custom_btn)
#         time.sleep(1)  # espera mínima para evitar interferencia por animación

#         # Click usando JavaScript para evitar overlays invisibles
#         driver.execute_script("arguments[0].click();", custom_btn)


#         # Esperar que aparezca el campo de cantidad personalizada
#         input_field = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Cantidad personalizada']"))
#         )
#         input_field.send_keys(str(donation_amount))

#         # Hacer clic en el botón de donar
#         donate_now_btn = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Donar Ahora')]"))
#         )
#         donate_now_btn.click()

#         # Esperar y aceptar la alerta de confirmación
#         WebDriverWait(driver, 5).until(EC.alert_is_present())
#         alert = driver.switch_to.alert
#         assert "¡Gracias por tu donación" in alert.text
#         alert.accept()

#         # -------- Buscar y eliminar la donación --------
#         time.sleep(2)  # esperar que el backend procese
#         response = requests.get(f"{api_url}/donations", params={"email": email})
#         assert response.status_code == 200
#         donations = response.json()

#         # Buscar la donación recién creada
#         match = next((d for d in donations if d["amount"] == donation_amount), None)
#         assert match, f"No se encontró la donación con cantidad {donation_amount}"
#         donation_id = match["_id"]

#     finally:
#         driver.quit()

#         # -------- Eliminar donación --------
#         if donation_id:
#             try:
#                 del_donation = requests.delete(f"{api_url}/delete_donation", params={"id": donation_id})
#                 print(f"[INFO] Donación eliminada: {del_donation.status_code} - {del_donation.text}")
#             except Exception as e:
#                 print(f"[ERROR] No se pudo eliminar la donación: {e}")

#         # -------- Eliminar usuario --------
#         try:
#             del_user = requests.delete(f"{api_url}/delete_user", params={"email": email})
#             print(f"[INFO] Usuario eliminado: {del_user.status_code} - {del_user.text}")
#         except Exception as e:
#             print(f"[ERROR] No se pudo eliminar el usuario {email}: {e}")



import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_register_login_and_donate():
    email = f"testuser{int(time.time())}@example.com"
    password = "password123"
    donation_amount = 42  # personalizado
    base_url = "http://localhost:5173"
    api_url = "http://localhost:5000"
    donation_api_url = "http://localhost:8888"  # corregido

    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    donation_id = None

    try:
        # -------- Registro --------
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

        # -------- Login --------
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="tu@email.com"]')))
        driver.find_element(By.CSS_SELECTOR, 'input[placeholder="tu@email.com"]').send_keys(email)
        driver.find_element(By.CSS_SELECTOR, 'input[placeholder="••••••••"]').send_keys(password)
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))

        # -------- Donación desde home --------
        driver.get(f"{base_url}/")  # ir al root

        # Esperar que aparezca el botón de "Apoyar la Plataforma"
        apoyar_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Apoyar la Plataforma')]"))
        )
        apoyar_btn.click()

        # Esperar que haya redirigido a la página de donaciones
        WebDriverWait(driver, 10).until(EC.url_contains("/donations"))

                # -------- Donación personalizada --------
        # Esperar y presionar el botón "Donar Cantidad Personalizada"
        custom_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Donar Cantidad Personalizada')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", custom_btn)
        driver.execute_script("arguments[0].click();", custom_btn)

        # Esperar que aparezca el título del modal
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h3[contains(., 'Selecciona el monto')]"))
        )

        # Esperar que el input aparezca
        input_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Cantidad personalizada']"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
        input_field.click()
        input_field.clear()
        input_field.send_keys(str(donation_amount))

        # Verificar que el valor fue ingresado
        written = input_field.get_attribute("value")
        assert written == str(donation_amount), f"Input incorrecto: {written}"

        # Esperar botón "Donar Ahora" dentro del modal (visible)
        donar_ahora_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="donate-submit-button"]'))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", donar_ahora_btn)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", donar_ahora_btn)

        # Esperar la alerta
        WebDriverWait(driver, 7).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        assert "¡Gracias por tu donación" in alert.text
        alert.accept()


        # -------- Buscar y eliminar la donación --------
        # time.sleep(2)  # dar tiempo al backend
        # response = requests.get(f"{donation_api_url}/donations", params={"email": email})
        # assert response.status_code == 200
        # donations = response.json()

        # assert len(donations) > 0, f"No se encontraron donaciones para el correo {email}"
        # donation_id = donations[0]["_id"]
        # Esperar hasta 10 segundos por una donación registrada
        donation_id = None
        for _ in range(10):  # intenta durante 10 segundos como máximo
            response = requests.get(f"{donation_api_url}/donations", params={"email": email})
            if response.status_code == 200:
                donations = response.json()
                if donations:
                    donation_id = donations[0]["_id"]
                    break
            time.sleep(1)

        assert donation_id, f"No se encontraron donaciones para el correo {email}"


    finally:
        driver.quit()

        # -------- Eliminar donación --------
        if donation_id:
            try:
                del_donation = requests.delete(f"{donation_api_url}/delete_donation", params={"id": donation_id})
                print(f"[INFO] Donación eliminada: {del_donation.status_code} - {del_donation.text}")
            except Exception as e:
                print(f"[ERROR] No se pudo eliminar la donación: {e}")

        # -------- Eliminar usuario --------
        try:
            del_user = requests.delete(f"{api_url}/delete_user", params={"email": email})
            print(f"[INFO] Usuario eliminado: {del_user.status_code} - {del_user.text}")
        except Exception as e:
            print(f"[ERROR] No se pudo eliminar el usuario {email}: {e}")
