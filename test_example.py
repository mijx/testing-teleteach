from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configurar Chrome
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# Navegar al formulario de registro
driver.get("http://localhost:5174/register")  # Ajusta si usas otro puerto

# Esperar a que cargue
time.sleep(1)

# Llenar campos del formulario
# En vez de buscar por name, usa placeholder
driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Juan"]').send_keys("Juan")
driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Pérez"]').send_keys("Pérez")
driver.find_element(By.CSS_SELECTOR, 'input[placeholder="tu@email.com"]').send_keys("juan@example.com")
# driver.find_element(By.CSS_SELECTOR, 'input[placeholder="••••••••"]').send_keys("password123")
password_fields = driver.find_elements(By.CSS_SELECTOR, 'input[placeholder="••••••••"]')
password_fields[0].send_keys("password123")   # campo de contraseña
password_fields[1].send_keys("password123")   # campo de confirmación

# Aceptar términos
checkbox = driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
driver.execute_script("arguments[0].click();", checkbox)

# Enviar el formulario
submit = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
submit.click()

# Esperar resultado o redirección
time.sleep(3)
WebDriverWait(driver, 5).until(EC.alert_is_present())

# Aceptar la alerta
alert = driver.switch_to.alert
print("Alerta:", alert.text)
alert.accept()

# Ahora sí puedes verificar la URL
print("URL actual:", driver.current_url)

# Ahora puedes obtener la URL actual, por ejemplo
current_url = driver.current_url
print("Estás en:", current_url)

# Validar navegación o mensaje
current_url = driver.current_url
print("URL después de enviar:", current_url)

# También podrías verificar texto en la página o alertas
# alert = driver.switch_to.alert
# print(alert.text)

# Cerrar navegador
driver.quit()
