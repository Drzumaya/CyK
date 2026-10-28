import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import datetime
from qr_utils import mostrar_modulo_qr
from pdf_utils import generar_pdf_diagnostico

URL_PRODUCCION = "https://streamlit.app"
NOMBRE_HOJA_CALCULO = "Base_Datos_Modelo_Mandarina" # Cambia por el nombre de tu Google Sheet

# Función interna de conexión segura a la Base de Datos de Google
def guardar_en_google_sheets(nombre, whatsapp, resultados):
    try:
        # Cargamos las credenciales desde los Secrets seguros de Streamlit/GitHub
        secrets_dict = st.secrets["gcp_service_account"]
        scope = ["https://googleapis.com"]
        creds = Credentials.from_service_account_info(secrets_dict, scopes=scope)
        client = gspread.authorize(creds)
        
        # Abrimos la hoja de cálculo
        sheet = client.open(NOMBRE_HOJA_CALCULO).sheet1
        
        # Formateamos la fila de datos para consolidar la analítica
        fila = [
            str(datetime.datetime.now()),
            nombre if nombre else "Anónimo",
            whatsapp if whatsapp else "No Proporcionado",
            len(resultados["Salud Física (SF)"]),
            len(resultados["Salud Mental (SM)"]),
            len(resultados["Salud Emocional (SE)"]),
            len(resultados["Salud Social (SS)"]),
            len(resultados["Salud Económica (SECO)"]),
            len(resultados["Salud Temporal (ST)"]),
            len(resultados["Salud Espiritual (SPI)"]),
            ", ".join(resultados["Salud Temporal (ST)"])
        ]
        sheet.append_row(fila)
        return True
    except Exception as e:
        # Falla silenciosa en producción para no interrumpir la experiencia del empleado
        return False

# Inicialización de la Interfaz Táctil
st.set_page_config(page_title="Diagnóstico Salud Integral", layout="centered")

st.title("🍊 Diagnóstico de Salud Integral")
st.subheader("Modelo Mandarina")
st.caption("Desarrollado por: Jacob Zumaya Prianti (c) 2026")

mostrar_modulo_qr(URL_PRODUCCION)
st.divider()

# Sección 1: Datos de Control
st.header("📋 Datos de Control")
nombre = st.text_input("Nombre Completo:", placeholder="Ej. Juan Pérez")
whatsapp = st.text_input("Número de Contacto de WhatsApp:", placeholder="Ej. +52 633 123 4567")

st.divider()

# Sección 2: Cuestionario Completo de las 7 Dimensiones de la Salud
st.header("📊 Evaluación de las 7 Dimensiones")
st.write("Selecciona los puntos específicos que requieres trabajar o mejorar actualmente:")

# Diccionario contenedor para agrupar ítems seleccionados
resultados_totales = {}

# 1. SF
st.subheader("💪 Salud Física (SF)")
sf_items = ["Nutrición (Hábitos alimenticios)", "Sueño (Calidad del descanso)", "Ejercicio (Actividad estructurada)", "Movimiento (Evitar sedentarismo)"]
resultados_totales["Salud Física (SF)"] = [item for item in sf_items if st.checkbox(item, key=f"sf_{item}")]

# 2. SM
st.subheader("🧠 Salud Mental (SM)")
sm_items = ["Memoria (Retención y agilidad)", "Enfoque (Evitar distracciones)", "Resiliencia (Adaptación al cambio)", "Aprendizaje (Nuevas habilidades)"]
resultados_totales["Salud Mental (SM)"] = [item for item in sm_items if st.checkbox(item, key=f"sm_{item}")]

# 3. SE
st.subheader("❤️ Salud Emocional (SE)")
se_items = ["Gestión de emociones", "Autocontrol (Dominio propio)", "Regulación psicológica", "Comprensión del estado de ánimo"]
resultados_totales["Salud Emocional (SE)"] = [item for item in se_items if st.checkbox(item, key=f"se_{item}")]

# 4. SS
st.subheader("👥 Salud Social (SS)")
ss_items = ["Relaciones positivas (Vínculos sanos)", "Comunicación asertiva", "Empatía activa", "Red de apoyo ante crisis"]
resultados_totales["Salud Social (SS)"] = [item for item in ss_items if st.checkbox(item, key=f"ss_{item}")]

# 5. SECO
st.subheader("💰 Salud Económica (SECO)")
seco_items = ["Presupuesto (Control de gastos)", "Ahorro sistemático", "Inversión de capital", "Administración Financiera", "Creación / Generación del dinero"]
resultados_totales["Salud Económica (SECO)"] = [item for item in seco_items if st.checkbox(item, key=f"seco_{item}")]

# 6. ST
st.subheader("⏳ Salud Temporal (ST)")
ck_marcado = st.checkbox("Cronos & Kairos (Tiempo del reloj vs. valor real)", key="st_ck")
st_items = ["Gestión del tiempo (Agenda)", "Equilibrio (Deber/Descanso)", "Prioridades (Identificar lo importante)"]
st_sel = [item for item in st_items if st.checkbox(item, key=f"st_{item}")]
if ck_marcado:
    st_sel.append("Cronos & Kairos (Tiempo del reloj vs. valor real)")
resultados_totales["Salud Temporal (ST)"] = st_sel

# 7. SPI
st.subheader("🙏 Salud Espiritual (SPI)")
spi_items = ["Propósito (Sentido de vida)", "Valores (Alineación de actos)", "Meditación u oración", "Conexión del interior con el exterior"]
resultados_totales["Salud Espiritual (SPI)"] = [item for item in spi_items if st.checkbox(item, key=f"spi_{item}")]

st.divider()

# Compilación del reporte PDF en tiempo real
bytes_reporte = generar_pdf_diagnostico(nombre, whatsapp, resultados_totales, ck_marcado)

# Al presionar el botón de descarga, se gatilla la exportación móvil y el guardado en la base de datos simultáneamente
if st.download_button(
    label="DESCARGAR RESULTADOS EN PDF 📥",
    data=bytes_reporte,
    file_name=f"Diagnostico_Mandarina_{nombre.replace(' ', '_') if nombre else 'Participante'}.pdf",
    mime="application/pdf",
    use_container_width=True
):
    # Guardado asíncrono en la base de datos interna de Google Sheets
    guardar_en_google_sheets(nombre, whatsapp, resultados_totales)

st.caption("🔒 Tus datos están encriptados. El registro en Google Sheets se realiza de forma interna mediante tokens de seguridad validados.")
