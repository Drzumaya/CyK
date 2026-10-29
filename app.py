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

# =================================================================
# CONFIGURACIONES GENERALES Y ENLACES DE LA PONENCIA
# =================================================================
# IMPORTANTE: Reemplaza con la dirección URL pública real de tu app de Streamlit
URL_PRODUCCION = "https://dsimandarina.streamlit.app"
NOMBRE_HOJA_CALCULO = "Base_Datos_Modelo_Mandarina"

st.set_page_config(page_title="Diagnóstico Salud Integral", layout="centered")

st.title("🍊 Diagnóstico de Salud Integral")
st.subheader("Modelo Mandarina")
st.caption("Desarrollado por: Jacob Zumaya Prianti (c) 2026")

def conectar_google_sheets():
    try:
        # Validar si existen los secretos
        if "gcp_service_account" not in st.secrets:
            st.error("🚨 Error: No se encontró la sección [gcp_service_account] en st.secrets.")
            return None
            
        secrets_dict = dict(st.secrets["gcp_service_account"])
        
        # Google requiere los saltos de línea correctos en la llave privada
        if "private_key" in secrets_dict:
            secrets_dict["private_key"] = secrets_dict["private_key"].replace("\\n", "\n")
            
        scope = [
            "https://googleapis.com",
            "https://googleapis.com"
        ]
        
        creds = Credentials.from_service_account_info(secrets_dict, scopes=scope)
        client = gspread.authorize(creds)
        return client.open(NOMBRE_HOJA_CALCULO).sheet1
    except Exception as e:
        # Te muestra el error real en pantalla para saber qué pasa
        st.error(f"🚨 Error de conexión Sheets: {str(e)}")
        return None


def guardar_en_google_sheets(nombre, whatsapp, resultados, token):
    sheet = conectar_google_sheets()
    if sheet:
        try:
            fila = [
                str(datetime.datetime.now()),
                nombre if nombre else "Anonimo",
                whatsapp if whatsapp else "No Proporcionado",
                len(resultados.get("Salud Fisica (SF)", [])),
                len(resultados.get("Salud Mental (SM)", [])),
                len(resultados.get("Salud Emocional (SE)", [])),
                len(resultados.get("Salud Social (SS)", [])),
                len(resultados.get("Salud Economica (SECO)", [])),
                len(resultados.get("Salud Temporal (ST)", [])),
                len(resultados.get("Salud Espiritual (SPI)", [])),
                ", ".join(resultados.get("Salud Temporal (ST)", [])),
                token if token else "Acceso_Directo"
            ]
            sheet.append_row(fila)
            return True
        except Exception:
            return False
    return False

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
    pdf.cell(0, 5, "Diseño de Metricas y Propiedad Intelectual: Jacob Zumaya Prianti (c) 2026", new_x="LMARGIN", new_y="NEXT", align="C")
    
    return bytes(pdf.output())

minuto_actual = int(time.time() // 60)
token_tiempo = hashlib.md5(f"mandarina_secret_{minuto_actual}".encode()).hexdigest()[:8]
url_con_token = f"{URL_PRODUCCION}/?token={token_tiempo}&modo_admin=false"

modo_admin_url = st.query_params.get("modo_admin", "true")
es_celular_del_publico = str(modo_admin_url).strip().lower() == "false"

if not es_celular_del_publico:
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
            st.write("1. Abre la cámara nativa de tu smartphone.\n2. Enfoca el código QR en la pantalla.\n3. **Contesta rápido:** No necesitas registrarte ni iniciar sesión. El acceso es directo e inmediato.")

st.divider()

st.divider()

# Inicializar estados de sesión para el flujo de la aplicación
if "guardado_exitoso" not in st.session_state:
    st.session_state.guardado_exitoso = False
if "admin_autenticado" not in st.session_state:
    st.session_state.admin_autenticado = False
if "flujo_finalizado" not in st.session_state:
    st.session_state.flujo_finalizado = False


PASSWORD_CORRECTO = "mandarina2026"  

if not es_celular_del_publico:
    with st.expander("🔐 Acceso Exclusivo para el Ponente", expanded=not st.session_state.admin_autenticado):
        if not st.session_state.admin_autenticado:
            st.write("Introduce la clave de acceso para activar las métricas consolidadas del auditorio:")
            input_password = st.text_input("Contraseña de Administrador:", type="password", key="admin_pwd_input")
            
            if st.button("🔑 Verificar Identidad", use_container_width=True):
                if input_password == PASSWORD_CORRECTO:
                    st.session_state.admin_autenticado = True
                    st.success("¡Identidad verificada con éxito!")
                    st.rerun()
                else:
                    st.error("Contraseña incorrecta. Acceso denegado.")
        else:
            st.success("💻 Modo Administrador Activo")
            if st.button("🚪 Cerrar Sesión de Administrador"):
                st.session_state.admin_autenticado = False
                st.rerun()

if st.session_state.admin_autenticado and not es_celular_del_publico:
    with st.container():
        st.markdown("### 📊 Panel Analítico del Ponente (Métricas Consolidadas)")
        st.write("Análisis agregado del estado de salud de los participantes en tiempo real.")
        
        if st.button("🔄 Actualizar Estadísticas del Auditorio", type="primary"):
            sheet = conectar_google_sheets()
            if sheet:
                records = sheet.get_all_records()
                if records:
                    df = pd.DataFrame(records)
                    
                    if len(df.columns) >= 11:
                        columnas_dimensiones = {
                            "Salud Física (SF)": df.columns, "Salud Mental (SM)": df.columns,
                            "Salud Emocional (SE)": df.columns, "Salud Social (SS)": df.columns,
                            "Salud Económica (SECO)": df.columns, "Salud Temporal (ST)": df.columns,
                            "Salud Espiritual (SPI)": df.columns
                        }
                        promedios = {gajo: pd.to_numeric(df[col], errors='coerce').fillna(0).mean() for gajo, col in columnas_dimensiones.items()}
                        df_grafica = pd.DataFrame(list(promedios.items()), columns=["Dimension", "Promedio de Puntos de Fuga"])
                        
                        st.write(f"**Total de participantes evaluados en vivo:** {len(df)}")
                        st.bar_chart(data=df_grafica, x="Dimension", y="Promedio de Puntos de Fuga", color="#e65100", use_container_width=True)
                        
                        st.write("---")
                        st.write("#### 🚨 Top 3 Problemas Más Comunes en el Auditorio")
                        
                        columna_alertas = df.columns
                        todas_alertas = []
                        for lista_str in df[columna_alertas].dropna().astype(str):
                            if lista_str and lista_str != "Ninguno. Area equilibrada.":
                                elementos = [e.strip() for e in lista_str.split(",") if e.strip()]
                                todas_alertas.extend(elementos)
                        
                        if todas_alertas:
                            s_alertas = pd.Series(todas_alertas)
                            top_alertas = s_alertas.value_counts().head(3)
                            
                            for i, (alerta, conteo) in enumerate(top_alertas.items(), 1):
                                st.warning(f"**{i}. {alerta}** — Detectado en {conteo} participantes")
                        else:
                            st.success("No hay alertas críticas recurrentes acumuladas en el auditorio.")
                    else:
                        st.error("Estructura de columnas incorrecta en la hoja de cálculo.")
                else:
                    st.warning("Aún no se registran respuestas en la base de datos de Google Sheets.")
            else:
                st.error("Error de conexión con Google Sheets. Verifica tus secretos.")

st.divider()

# INTERCEPTOR DE REÚSO Y SEGURIDAD CON 5 MINUTOS DE GRACIA
token_actual = st.query_params.get("token", None)
acceso_bloqueado = False
motivo_bloqueo = ""

if token_actual and not st.session_state.admin_autenticado:
    minuto_base = int(time.time() // 60)
    tokens_validos = []
    for i in range(5):
        minuto_test = minuto_base - i
        token_test = hashlib.md5(f"mandarina_secret_{minuto_test}".encode()).hexdigest()[:8]
        tokens_validos.append(token_test)
    
    if token_actual not in tokens_validos:
        acceso_bloqueado = True
        motivo_bloqueo = "El código QR escaneado ha expirado debido al tiempo transcurrido."
    else:
        sheet = conectar_google_sheets()
        if sheet:
            try:
                registros = sheet.get_all_records()
                if registros:
                    df_check = pd.DataFrame(registros)
                    tokens_usados = [str(r.get(df_check.columns[-1], "")) for r in registros]
                    if token_actual in tokens_usados:
                        acceso_bloqueado = True
                        motivo_bloqueo = "Este acceso ya fue utilizado por otro dispositivo de la audiencia."
            except Exception:
                pass

if acceso_bloqueado:
    st.error(f"🚫 **Acceso Denegado:** {motivo_bloqueo}")
    st.info("Por favor, vuelve a escanear el código QR dinámico que el ponente está proyectando en vivo.")
    st.stop()

st.header("📋 Datos de Control")
nombre = st.text_input("Nombre Completo *:", placeholder="Ej. Juan Pérez")
whatsapp = st.text_input("Número de Contacto de WhatsApp *:", placeholder="Ej. +52 633 123 4567")

# SÓLO DESPLEGAMOS EL CUESTIONARIO SI EL USUARIO NO HA TERMINADO SU DESCARGA
if not st.session_state.flujo_finalizado:
    st.header("📋 Datos de Control")
    nombre = st.text_input("Nombre Completo *:", placeholder="Ej. Juan Pérez")
    whatsapp = st.text_input("Número de Contacto de WhatsApp *:", placeholder="Ej. +52 633 123 4567")

    st.divider()

    st.header("📊 Evaluación de las 7 Dimensiones")
    st.write("Selecciona los elementos específicos en los que requieres intervención:")

    resultados_totales = {}

    # 1. SF
    st.subheader("💪 Salud Física (SF)")
    sf_items = ["Nutrición (Hábitos alimenticios)", "Sueño (Calidad del descanso)", "Ejercicio (Actividad estructurada)", "Movimiento (Evitar sedentarismo)"]
    resultados_totales["Salud Fisica (SF)"] = [i for i in sf_items if st.checkbox(i, key=f"sf_{i}")]

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
    resultados_totales["Salud Economica (SECO)"] = [i for i in seco_items if st.checkbox(i, key=f"seco_{i}")]

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

    col_btn1, col_btn2 = st.columns(2)
    campos_completos = bool(nombre.strip()) and bool(whatsapp.strip())

    with col_btn1:
        if st.button("💾 Guardar y Procesar Diagnóstico", use_container_width=True, type="primary"):
            if not campos_completos:
                st.error("⚠️ **Faltan datos obligatorios.** Por favor ingresa tu Nombre y WhatsApp antes de continuar.")
            else:
                with st.spinner("Registrando tus gajos de salud de forma segura..."):
                    exito = guardar_en_google_sheets(nombre, whatsapp, resultados_totales, token_actual)
                    if exito:
                        st.session_state.guardado_exitoso = True
                        st.success("¡Datos guardados con éxito en la nube!")
                    else:
                        st.session_state.guardado_exitoso = True
                        st.warning("Diagnóstico procesado de forma local (Sin conexión de red temporal).")

    with col_btn2:
        if st.session_state.guardado_exitoso and campos_completos:
            reporte_procesado = generar_pdf_diagnostico(nombre, whatsapp, resultados_totales, ck_marcado)
            nombre_archivo = nombre.replace(' ', '_') if nombre else 'Participante'
            
            def finalizar_experiencia_callback():
                # Activamos la bandera de cierre de la app
                st.session_state.flujo_finalizado = True
                # Limpiamos las variables del cuestionario por privacidad
                for clave in list(st.session_state.keys()):
                    if clave.startswith(("sf_", "sm_", "se_", "ss_", "seco_", "st_", "spi_")):
                        del st.session_state[clave]

            st.download_button(
                label="DESCARGAR RESULTADOS EN PDF 📥",
                data=reporte_procesado,
                file_name=f"Diagnostico_Mandarina_{nombre_archivo}.pdf",
                mime="application/pdf",
                on_click=finalizar_experiencia_callback
            )
        elif not campos_completos:
            st.warning("⚠️ Escribe tu Nombre y WhatsApp arriba para liberar las opciones de procesamiento.")
        else:
            st.info("💡 Haz clic en 'Guardar y Procesar' para activar tu descarga.")

    st.caption("🔒 Tus datos están protegidos. El registro en Google Sheets se realiza de forma interna mediante tokens de seguridad validados.")

# --- VENTANA DE AGRADECIMIENTO Y CIERRE EXCLUSIVO (PANTALLA NUEVA) ---
else:
    st.balloons() # Lluvia de globos celebrando el éxito de su diagnóstico
    st.success("### ¡Tu reporte PDF ha sido generado y descargado con éxito! 🎉")
    
    # Caja de diseño para el mensaje de cierre
    with st.container(border=True):
        st.write("## 🍊 ¡Muchas gracias por tu participación!")
        st.markdown(
            "Has tomado un paso fundamental al mapear de forma honesta cada uno de tus gajos de bienestar. "
            "Reconocer nuestros puntos de fuga es el verdadero inicio de una transformación integral."
        )
        st.write("---")
        st.write("### 📅 ¿Te gustaría llevar tu diagnóstico al siguiente nivel?")
        st.write(
            "Te invitamos cordialmente a **agendar una sesión de consulta directa y personalizada con el ponente**. "
            "En esta asesoría individualizada analizaremos a profundidad tus resultados estratégicos y estructuraremos "
            "un plan de acción a la medida para sanar tus dimensiones críticas."
        )
        
        # Opcional: Si tienes un enlace de Calendly o WhatsApp corporativo, puedes añadir el botón directo aquí
        st.info("👉 Acércate al término de la ponencia o solicita tu espacio de asesoramiento personalizado directamente en el escenario.")
        
    st.markdown("### ✨ ¡Te deseamos el mayor de los éxitos en los nuevos cambios que inicias a partir de esta experiencia! ✨")
    
    # Botón por si el ponente necesita resetear la app manualmente en el escenario sin recargar la URL
    if es_celular_del_publico == False: 
        if st.button("🔄 Reiniciar Aplicación (Modo Ponente)"):
            st.session_state.flujo_finalizado = False
            st.session_state.guardado_exitoso = False
            st.rerun()
