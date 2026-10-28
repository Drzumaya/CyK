import streamlit as st
import qrcode
from io import BytesIO
from fpdf import FPDF
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import datetime

# Enlace web de producción de tu ponencia en Streamlit Cloud
URL_PRODUCCION = "https://streamlit.app"
NOMBRE_HOJA_CALCULO = "Base_Datos_Modelo_Mandarina"

# Configuración móvil-first de la interfaz táctil
st.set_page_config(page_title="Diagnóstico Salud Integral", layout="centered")

st.title("🍊 Diagnóstico de Salud Integral")
st.subheader("Modelo Mandarina")
st.caption("Desarrollado por: Jacob Zumaya Prianti (c) 2026")
# Función para enlazar la base de datos interna con Google Sheets
def conectar_google_sheets():
    try:
        secrets_dict = st.secrets["gcp_service_account"]
        scope = ["https://googleapis.com"]
        creds = Credentials.from_service_account_info(secrets_dict, scopes=scope)
        client = gspread.authorize(creds)
        return client.open(NOMBRE_HOJA_CALCULO).sheet1
    except Exception:
        return None

def guardar_en_google_sheets(nombre, whatsapp, resultados):
    sheet = conectar_google_sheets()
    if sheet:
        try:
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
        except Exception:
            return False
    return False

# Función del motor PDF para estructurar el reporte móvil
def generar_pdf_diagnostico(nombre_usuario, whatsapp_usuario, resultados_totales, st_cronos_kairos):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(230, 81, 0) 
    pdf.cell(0, 10, "REPORTE DE DIAGNÓSTICO DE SALUD INTEGRAL", ln=True, align="C")
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, "Modelo Mandarina | Jacob Zumaya Prianti (c) 2026", ln=True, align="C")
    pdf.ln(5)
    
    pdf.set_draw_color(255, 152, 0)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(10)
    
    pdf.set_text_color(50, 50, 50)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(45, 6, "Participante:", 0, 0)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, nombre_usuario if nombre_usuario else "Participante Anónimo", 0, 1)
    
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(45, 6, "WhatsApp de Contacto:", 0, 0)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, whatsapp_usuario if whatsapp_usuario else "No Proporcionado", 0, 1)
    
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(45, 6, "Fecha de Emisión:", 0, 0)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, datetime.date.today().strftime("%d/%m/%Y"), 0, 1)
    pdf.ln(10)
    
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(255, 152, 0)
    pdf.cell(0, 8, "Resultados y Puntos Críticos Detectados", ln=True)
    pdf.line(10, pdf.get_y(), 100, pdf.get_y())
    pdf.ln(4)
    
    for dim_nombre, items in resultados_totales.items():
        conteo = len(items)
        estado = "Sano y Pleno (0 alertas)"
        if conteo >= 3:
            estado = "CRITICO / URGENCIA INMEDIATA"
        elif conteo > 0:
            estado = "EN ALERTA TEMPRANA"
            
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 6, f"• {dim_nombre}: {estado}", ln=True)
        pdf.set_font("Helvetica", "I", 10)
        pdf.set_text_color(30, 30, 30)
        puntos_str = ", ".join(items) if conteo > 0 else "Ninguno. Área equilibrada."
        pdf.multi_cell(0, 5, f"Puntos específicos a solucionar: {puntos_str}")
        pdf.ln(3)
        
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(255, 152, 0)
    pdf.cell(0, 8, "Mensaje de Confirmación e Interpretación", ln=True)
    pdf.line(10, pdf.get_y(), 100, pdf.get_y())
    pdf.ln(4)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 5, "Cada casilla que seleccionaste representa un 'punto de fuga' activo de tu bienestar integral.")
    pdf.ln(2)
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 5, "Criterio de Evaluación de Gajos:", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 5, "• 0 Puntos Seleccionados: Gajo Sano y Pleno.\n"
                         "• 1 a 2 Puntos Seleccionados: Gajo en Alerta. Requiere micro-acciones de corrección.\n"
                         "• 3 o más Puntos Seleccionados: Gajo Crítico / Urgencia Inmediata. Debe ser tu prioridad absoluta.")
    pdf.ln(4)
    
    if st_cronos_kairos:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(230, 81, 0)
        pdf.cell(0, 5, "Alerta Especial sobre la Salud Temporal (ST):", ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(50, 50, 50)
        pdf.multi_cell(0, 5, "Has marcado el elemento de 'Cronos & Kairos'. Te encuentras bajo la tiranía del rendimiento constante o en desconexión pragmática. Equilibrar de manera urgente el tiempo cuantitativo con el cualitativo aliviará la carga sistémica de tus dimensiones de inmediato.")
    
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 5, "Diseño de Métricas y Propiedad Intelectual: Jacob Zumaya Prianti (c) 2026", ln=True, align="C")
    
    return pdf.output()
# Renderizado automático del módulo de Código QR
with st.expander("📱 Escanea el Código QR para contestar desde tu móvil", expanded=True):
    col1, col2 = st.columns([1, 1.5])
    with col1:
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(URL_PRODUCCION)
        qr.make(fit=True)
        img_qr = qr.make_image(fill_color="#e65100", back_color="white")
        buf = BytesIO()
        img_qr.save(buf, format="PNG")
        st.image(buf.getvalue(), caption="Escanea con tu cámara", use_container_width=True)
    with col2:
        st.write("### ¡Lleva la encuesta en tu bolsillo!")
        st.write("1. Abre la cámara nativa de tu smartphone.\n2. Enfoca el código QR.\n3. Diagnostica tus gajos en tiempo real.")

st.divider()

# Panel Analítico privado para consulta del Ponente en el escenario
with st.expander("📊 Panel Analítico del Ponente (Métricas Consolidadas)", expanded=False):
    st.write("Análisis agregado del estado de salud de los participantes de la ponencia en tiempo real.")
    if st.button("🔄 Actualizar Estadísticas del Auditorio"):
        sheet = conectar_google_sheets()
        if sheet:
            records = sheet.get_all_records()
            if records:
                df = pd.DataFrame(records)
                columnas_dimensiones = {
                    "Salud Física (SF)": df.columns[3], "Salud Mental (SM)": df.columns[4],
                    "Salud Emocional (SE)": df.columns[5], "Salud Social (SS)": df.columns[6],
                    "Salud Económica (SECO)": df.columns[7], "Salud Temporal (ST)": df.columns[8],
                    "Salud Espiritual (SPI)": df.columns[9]
                }
                promedios = {gajo: pd.to_numeric(df[col]).mean() for gajo, col in columnas_dimensiones.items()}
                df_grafica = pd.DataFrame(list(promedios.items()), columns=["Dimensión", "Promedio de Puntos de Fuga"])
                st.write(f"**Total de participantes evaluados:** {len(df)}")
                st.bar_chart(data=df_grafica, x="Dimensión", y="Promedio de Puntos de Fuga", color="#e65100", use_container_width=True)
            else:
                st.warning("Aún no se registran respuestas en la base de datos.")
        else:
            st.error("Error de conexión con Google Secrets.")

st.divider()
# Captura de datos básicos del empleado
st.header("📋 Datos de Control")
nombre = st.text_input("Nombre Completo:", placeholder="Ej. Juan Pérez")
whatsapp = st.text_input("Número de Contacto de WhatsApp:", placeholder="Ej. +52 633 123 4567")

st.divider()

# Despliegue de los 7 gajos de autoevaluación del Modelo Mandarina
st.header("📊 Evaluación de las 7 Dimensiones")
st.write("Selecciona los elementos específicos en los que requieres intervención:")

resultados_totales = {}

# 1. SF
st.subheader("💪 Salud Física (SF)")
sf_items = ["Nutrición (Hábitos alimenticios)", "Sueño (Calidad del descanso)", "Ejercicio (Actividad estructurada)", "Movimiento (Evitar sedentarismo)"]
resultados_totales["Salud Física (SF)"] = [i for i in sf_items if st.checkbox(i, key=f"sf_{i}")]

# 2. SM
st.subheader("🧠 Salud Mental (SM)")
sm_items = ["Memoria (Retención y agilidad)", "Enfoque (Evitar distracciones)", "Resiliencia (Adaptación al cambio)", "Aprendizaje (Nuevas habilidades)"]
resultados_totales["Salud Mental (SM)"] = [i for i in sm_items if st.checkbox(i, key=f"sm_{i}")]

# 3. SE
st.subheader("❤️ Salud Emocional (SE)")
se_items = ["Gestión de emociones", "Autocontrol (Dominio propio)", "Regulación psicológica", "Comprensión del estado de ánimo"]
resultados_totales["Salud Emocional (SE)"] = [i for i in se_items if st.checkbox(i, key=f"se_{i}")]

# 4. SS
st.subheader("👥 Salud Social (SS)")
ss_items = ["Relaciones positivas (Vínculos sanos)", "Comunicación asertiva", "Empatía activa", "Red de apoyo ante crisis"]
resultados_totales["Salud Social (SS)"] = [i for i in ss_items if st.checkbox(i, key=f"ss_{i}")]

# 5. SECO
st.subheader("💰 Salud Económica (SECO)")
seco_items = ["Presupuesto (Control de gastos)", "Ahorro sistemático", "Inversión de capital", "Administración Financiera", "Creación / Generación del dinero"]
resultados_totales["Salud Económica (SECO)"] = [i for i in seco_items if st.checkbox(i, key=f"seco_{i}")]

# 6. ST
st.subheader("⏳ Salud Temporal (ST)")
ck_marcado = st.checkbox("Cronos & Kairos (Tiempo del reloj vs. valor real)", key="st_ck")
st_items = ["Gestión del tiempo (Agenda)", "Equilibrio (Deber/Descanso)", "Prioridades (Identificar lo importante)"]
st_sel = [i for i in st_items if st.checkbox(i, key=f"st_{i}")]
if ck_marcado:
    st_sel.append("Cronos & Kairos (Tiempo del reloj vs. valor real)")
resultados_totales["Salud Temporal (ST)"] = st_sel

# 7. SPI
st.subheader("🙏 Salud Espiritual (SPI)")
spi_items = ["Propósito (Sentido de vida)", "Valores (Alineación de actos)", "Meditación u oración", "Conexión del interior con el exterior"]
resultados_totales["Salud Espiritual (SPI)"] = [i for i in spi_items if st.checkbox(i, key=f"spi_{i}")]

st.divider()
# Generación en caché y memoria del flujo binario del PDF
bytes_reporte = generar_pdf_diagnostico(nombre, whatsapp, resultados_totales, ck_marcado)

# Despliegue de gatillo de descarga móvil y guardado analítico simultáneo
if st.download_button(
    label="DESCARGAR RESULTADOS EN PDF 📥",
    data=bytes_reporte,
    file_name=f"Diagnostico_Mandarina_{nombre.replace(' ', '_') if nombre else 'Participante'}.pdf",
    mime="application/pdf",
    use_container_width=True
):
    # Inserta la fila de forma asíncrona en la base de datos de Google Sheets
    guardar_en_google_sheets(nombre, whatsapp, resultados_totales)

st.caption("🔒 Tus datos están protegidos. El registro en Google Sheets se realiza de forma interna mediante tokens de seguridad validados.")
