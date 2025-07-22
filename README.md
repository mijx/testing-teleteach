# ✅ TeleTeach – Repositorio de Pruebas Automatizadas

Este repositorio contiene el conjunto de **pruebas automatizadas de integración y funcionalidad** desarrolladas para los microservicios del sistema **TeleTeach**. Las pruebas incluyen validaciones HTTP, pruebas de interfaz con Selenium y generación automática de reportes en PDF.

Forma parte del desarrollo del curso **Ingeniería de Software 2 – 2025-1**, utilizando una arquitectura SOFEA con enfoque en microservicios RESTful.

---

## 🧪 Pruebas implementadas

- ✔️ Pruebas de registro e inicio de sesión de usuarios
- ✔️ Verificación de duplicidad en registros
- ✔️ Pruebas de donaciones con datos dinámicos
- ✔️ Registro y consulta de progreso por usuario
- ✔️ Limpieza automática de datos creados en los tests
- ✔️ Generación de reportes PDF con resultados

---

## 🚀 Tecnologías y librerías utilizadas

- `pytest` – ejecución y estructura de pruebas
- `selenium` – pruebas funcionales sobre UI web
- `requests` – consumo de endpoints REST
- `reportlab` – generación de reportes PDF
- `numpy` – cálculos y visualización (gráficas)
- Python 3.11+

---

## ⚙️ Instalación y ejecución local

```bash
# 1. Clona el repositorio
git clone https://github.com/mijx/testing-teleteach.git
cd teleteach-tests

# 2. Crea el entorno virtual
python -m venv venv
venv\Scripts\activate   # En Windows PowerShell

# 3. Instala las dependencias
pip install -r requirements.txt

# 4. Ejecuta todas las pruebas
pytest tests/
```
## 🔗 Repositorios relacionados
* 🔐 [API de Autenticación](https://github.com/javiierbarco/auth-api-teleteach)
* 💸 [API de Donaciones](https://github.com/mijx/donaciones-api-teleteach)
* 🎓 [API de Cursos y Progreso](https://github.com/javiierbarco/courses-api-teleteach)
* 🧠 [Frontend TeleTeach](https://github.com/javiierbarco/frontend-teleteach)

## 👥 Equipo Castores – Ingeniería de Software 2
Diego H. Lavado G.

Estephanie Perez M.

Frank S. Pardo A.

Javier E. González V.

Juan D. Rivera B.

Victor M. Torres A.

Wullfredo J. Barco G.
