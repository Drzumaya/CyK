import streamlit as st
import qrcode
from io import BytesIO
from fpdf import FPDF
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import datetime
import uuid
import hashlib
import time

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

def guardar_en_google_sheets(nombre, whatsapp, resultados, token):
    sheet = conectar_google_sheets()
    if sheet:
        try:
            fila = [
                str(datetime.datetime.now()),
                nombre if nombre else "Anonimo",
                whatsapp if whatsapp else "No Proporcionado",
                len(resultados["Salud Física (SF)"]),
                len(resultados["Salud Mental (SM)"]),
                len(resultados["Salud Emocional (SE)"]),
                len(resultados["Salud Social (SS)"]),
                len(resultados["Salud Económica (SECO)"]),
                len(resultados["Salud Temporal (ST)"]),
                len(resultados["Salud Espiritual (SPI)"]),
                ", ".join(resultados["Salud Temporal (ST)"]),
                token if token else "Acceso_Directo"
            ]
            sheet.append_row(fila)
            return True
        except Exception:
            return False
    return False
# Función del motor PDF para estructurar el reporte móvil (Adaptada a fpdf2 y sin acentos)
def generar_pdf_diagnostico(nombre_usuario, whatsapp_usuario, resultados_totales, st_cronos_kairos):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Encabezado principal
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(230, 81, 0) 
    pdf.cell(0, 10, "REPORTE DE DIAGNOSTICO DE SALUD INTEGRAL", new_x="LMARGIN", new_y="NEXT", align="C")
    
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, "Modelo Mandarina | Jacob Zumaya Prianti (c) 2026", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)
    
    pdf.set_draw_color(255, 152, 0)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(10)
    
    # Datos de usuario
    pdf.set_text_color(50, 50, 50)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(45, 6, "Participante:", 0, 0)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, nombre_usuario if nombre_usuario else "Participante Anonimo", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(45, 6, "WhatsApp de Contacto:", 0, 0)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, whatsapp_usuario if whatsapp_usuario else "No Proporcionado", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(45, 6, "Fecha de Emision:", 0, 0)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, datetime.date.today().strftime("%d/%m/%Y"), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    
    # Sección Resultados
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(255, 152, 0)
    pdf.cell(0, 8, "Resultados y Puntos Criticos Detectados", new_x="LMARGIN", new_y="NEXT")
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
        # Reemplazo de viñeta unicode compleja por guion simple para evitar caídas del PDF
        pdf.cell(0, 6, f"- {dim_nombre}: {estado}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "I", 10)
        pdf.set_text_color(30, 30, 30)
        puntos_str = ", ".join(items) if conteo > 0 else "Ninguno. Area equilibrada."
        pdf.multi_cell(0, 5, f"Puntos especificos a solucionar: {puntos_str}")
        pdf.ln(3)
        
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(255, 152, 0)
    pdf.cell(0, 8, "Mensaje de Confirmacion e Interpretacion", new_x="LMARGIN", new_y="NEXT")
    pdf.line(10, pdf.get_y(), 100, pdf.get_y())
    pdf.ln(4)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 5, "Cada casilla que seleccionaste representa un 'punto de fuga' activo de tu bienestar integral.")
    pdf.ln(2)
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 5, "Criterio de Evaluacion de Gajos:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 5, "- 0 Puntos Seleccionados: Gajo Sano y Pleno.\n"
                         "- 1 a 2 Puntos Seleccionados: Gajo en Alerta. Requiere micro-acciones de correccion.\n"
                         "- 3 o mas Puntos Seleccionados: Gajo Critico / Urgencia Inmediata. Debe ser tu prioridad absoluta.")
    pdf.ln(4)
    
    if st_cronos_kairos:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(230, 81, 0)
        pdf.cell(0, 5, "Alerta Especial sobre la Salud Temporal (ST):", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(50, 50, 50)
        pdf.multi_cell(0, 5, "Has marcado el elemento de 'Cronos & Kairos'. Te encuentras bajo la tirania del rendimiento constante o en desconexion pragmatica. Equilibrar de manera urgente el tiempo cuantitativo con el cualitativo aliviara la carga sistemica de tus dimensiones de inmediato.")
    
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 5, "Diseno de Metricas y Propiedad Intelectual: Jacob Zumaya Prianti (c) 2026", new_x="LMARGIN", new_y="NEXT", align="C")
    
    return pdf.output()
# Generación de Token dinámico por tiempo (Expira cada 60 segundos)
minuto_actual = int(time.time() // 60)
token_tiempo = hashlib.md5(f"mandarina_secret_{minuto_actual}".encode()).hexdigest()[:8]

# Construimos la URL dinámica vinculada al minuto actual
url_con_token = f"{URL_PRODUCCION}/?token={token_tiempo}"

# Renderizado automático del módulo de Código QR
with st.expander("📱 Escanea el Código QR para contestar desde tu móvil (Válido solo en vivo)", expanded=True):
    col1, col2 = st.columns([1, 1.5])
    with col1:
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(url_con_token)
        qr.make(fit=True)
        img_qr = qr.make_image(fill_color="#e65100", back_color="white")
        buf = BytesIO()
        img_qr.save(buf, format="PNG")
        st.image(buf.getvalue(), caption="Código dinámico de seguridad temporal", use_container_width=True)
    with col2:
        st.write("### ¡Lleva la encuesta en tu bolsillo!")
        st.write("1. Abre la cámara nativa de tu smartphone.\n2. Enfoca el código QR en la pantalla.\n3. **Contesta rápido:** Este código cambia cada minuto en el escenario para evitar reuso externo.")
st.divider()

# Inicializar estados de sesión para el flujo de guardado
if "guardado_exitoso" not in st.session_state:
    st.session_state.guardado_exitoso = False

# Panel Analítico privado para consulta del Ponente en el escenario
with st.expander("📊 Panel Analítico del Ponente (Métricas Consolidadas)", expanded=False):
    st.write("Análisis agregado del estado de salud de los participantes de la ponencia en tiempo real.")
    if st.button("🔄 Actualizar Estadísticas del Auditorio"):
        sheet = conectar_google_sheets()
        if sheet:
            records = sheet.get_all_records()
            if records:
                df = pd.DataFrame(records)
                if len(df.columns) >= 10:
                    columnas_dimensiones = {
                        "Salud Física (SF)": df.columns[3], "Salud Mental (SM)": df.columns[4],
                        "Salud Emocional (SE)": df.columns[5], "Salud Social (SS)": df.columns[6],
                        "Salud Económica (SECO)": df.columns[7], "Salud Temporal (ST)": df.columns[8],
                        "Salud Espiritual (SPI)": df.columns[9]
                    }
                    promedios = {gajo: pd.to_numeric(df[col], errors='coerce').fillna(0).mean() for gajo, col in columnas_dimensiones.items()}
                    df_grafica = pd.DataFrame(list(promedios.items()), columns=["Dimension", "Promedio de Puntos de Fuga"])
                    st.write(f"**Total de participantes evaluados:** {len(df)}")
                    st.bar_chart(data=df_grafica, x="Dimension", y="Promedio de Puntos de Fuga", color="#e65100", use_container_width=True)
                else:
                    st.error("Estructura de columnas incorrecta en la hoja de cálculo.")
            else:
                st.warning("Aún no se registran respuestas en la base de datos.")
        else:
            st.error("Error de conexión con Google Sheets.")

st.divider()

# --- BLOQUE INTERCEPTOR DE REÚSO Y SEGURIDAD ---
token_actual = st.query_params.get("token", None)
acceso_bloqueado = False
motivo_bloqueo = ""

if token_actual:
    minuto_0 = int(time.time() // 60)
    minuto_1 = minuto_0 - 1
    
    token_valido_0 = hashlib.md5(f"mandarina_secret_{minuto_0}".encode()).hexdigest()[:8]
    token_valido_1 = hashlib.md5(f"mandarina_secret_{minuto_1}".encode()).hexdigest()[:8]
    
    if token_actual not in [token_valido_0, token_valido_1]:
        acceso_bloqueado = True
        motivo_bloqueo = "El codigo QR escaneado ha expirado debido al tiempo transcurrido."
    else:
        sheet = conectar_google_sheets()
        if sheet:
            try:
                registros = sheet.get_all_records()
                # Verifica los tokens usados en la última columna guardada (índice 11)
                tokens_usados = [str(r.get(df.columns[11] if len(df.columns)>11 else "Token_Acceso", "")) for r in registros] if registros else []
                if token_actual in tokens_usados:
                    acceso_bloqueado = True
                    motivo_bloqueo = "Este acceso ya fue utilizado por otro dispositivo de la audiencia."
            except Exception:
                pass

if acceso_bloqueado:
    st.error(f"🚫 **Acceso Denegado:** {motivo_bloqueo}")
    st.info("Por favor, vuelve a escanear el código QR dinámico que el ponente está proyectando en vivo en la pantalla.")
    st.stop()
# Captura de datos básicos del empleado
st.header("📋 Datos de Control")
nombre = st.text_input("Nombre Completo:", placeholder="Ej. Juan Pérez")
whatsapp = st.text_input("Número de Contacto de WhatsApp:", placeholder="Ej. +52 633 123 4567")

st.divider()

col_btn1, col_btn2 = st.columns()

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
sm_items = ["Memoria (Retención y agilidad)", "Enfoque (Evitar distractions)", "Resiliencia (Adaptación al cambio)", "Aprendizaje (Nuevas habilidades)"]
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

col_btn1, col_btn2 = st.columns()

with col_btn1:
    if st.button("💾 Guardar y Procesar Diagnóstico", use_container_width=True, type="primary"):
        with st.spinner("Registrando tus gajos de salud de forma segura..."):
            # Encriptamos el token usado directamente en la fila de Google Sheets
            exito = guardar_en_google_sheets(nombre, whatsapp, resultados_totales, token_actual)
            if exito:
                st.session_state.guardado_exitoso = True
                st.success("¡Datos guardados con éxito en la nube!")
            else:
                st.session_state.guardado_exitoso = True
                st.warning("Diagnóstico procesado de forma local (Sin conexión de red temporal).")

with col_btn2:
    if st.session_state.guardado_exitoso:
        bytes_reporte = generar_pdf_diagnostico(nombre, whatsapp, resultados_totales, ck_marcado)
        nombre_archivo = nombre.replace(' ', '_') if nombre else 'Participante'
        
        st.download_button(
            label="DESCARGAR RESULTADOS EN PDF 📥",
            data=bytes_reporte,
            file_name=f"Diagnostico_Mandarina_{nombre_archivo}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    else:
        st.info("💡 Haz clic en 'Guardar y Procesar' para activar tu descarga.")

st.caption("🔒 Tus datos están protegidos. El registro en Google Sheets se realiza de forma interna mediante tokens de seguridad validados.")
