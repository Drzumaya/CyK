import streamlit as st
import qrcode
from io import BytesIO
from fpdf import FPDF
import gspread
import pandas as pd
import datetime
import hashlib
import time

# Enlace web de producción de tu ponencia en Streamlit Cloud
URL_PRODUCCION = "https://streamlit.app"
NOMBRE_HOJA_CALCULO = "Base_Datos_Modelo_Mandarina"

st.set_page_config(page_title="Ecosistema Diagnóstico de Modelos Temporales", layout="centered")

st.title("🍊 Ecosistema de Diagnóstico de Salud Integral")
st.subheader("Modelo Mandarina & Modelos Temporales Sectores")
st.caption("Desarrollado por: Jacob Zumaya Prianti (c) 2026 | JACOB ZUMAYA PRIANTI, A.C.")


def conectar_google_sheets():
    try:
        if "gcp_service_account" not in st.secrets:
            return None
            
        secrets_dict = dict(st.secrets["gcp_service_account"])
        if "private_key" in secrets_dict:
            secrets_dict["private_key"] = secrets_dict["private_key"].replace("\\n", "\n")
            
        client = gspread.service_account_from_dict(secrets_dict)
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
    pdf.cell(45, 6, "Participante:", new_x="RIGHT", new_y="TOP")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, nombre_usuario if nombre_usuario else "Participante Anonimo", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(45, 6, "WhatsApp de Contacto:", new_x="RIGHT", new_y="TOP")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, whatsapp_usuario if whatsapp_usuario else "No Proporcionado", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(45, 6, "Fecha de Emision:", new_x="RIGHT", new_y="TOP")
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
    pdf.cell(0, 5, "Diseno de Metricas y Propiedad Intelectual: Jacob Zumaya Prianti (c) 2026", new_x="LMARGIN", new_y="NEXT", align="C")
    
    return bytes(pdf.output())


minuto_actual = int(time.time() // 60)
token_tiempo = hashlib.md5(f"mandarina_secret_{minuto_actual}".encode()).hexdigest()[:8]
url_con_token = f"{URL_PRODUCCION}/?token={token_tiempo}&modo_admin=false"

modo_admin_url = st.query_params.get("modo_admin", "true")
es_celular_del_publico = str(modo_admin_url).strip().lower() == "false"

# Inicializar almacenamiento de links de Google Forms en memoria de sesión
if "link_primario" not in st.session_state: st.session_state.link_primario = ""
if "link_secundario" not in st.session_state: st.session_state.link_secundario = ""
if "link_terciario" not in st.session_state: st.session_state.link_terciario = ""
if "link_educativo" not in st.session_state: st.session_state.link_educativo = ""
if "link_religioso" not in st.session_state: st.session_state.link_religioso = ""

# El código QR nativo de salud integral solo se muestra en la pantalla grande del ponente
if not es_celular_del_publico:
    with st.expander("📱 Código QR Diagnóstico Original (Salud Integral)", expanded=False):
        col1, col2 = st.columns([1, 1.5])
        with col1:
            qr = qrcode.QRCode(version=1, box_size=10, border=2)
            qr.add_data(url_con_token)
            qr.make(fit=True)
            img_qr = qr.make_image(fill_color="#e65100", back_color="white")
            buf = BytesIO()
            img_qr.save(buf, format="PNG")
            st.image(buf.getvalue(), caption="QR Salud Integral Dinámico", width="stretch")
        with col2:
            st.write("### ¡Lleva el Diagnóstico Original en tu Bolsillo!")
            st.write("Carga de forma directa el software nativo en los smartphones del auditorio sin usar formatos externos.")


st.divider()

if "guardado_exitoso" not in st.session_state:
    st.session_state.guardado_exitoso = False
if "admin_autenticado" not in st.session_state:
    st.session_state.admin_autenticado = False
if "flujo_finalizado" not in st.session_state:
    st.session_state.flujo_finalizado = False

PASSWORD_CORRECTO = "mandarina2026"  

if not es_celular_del_publico:
    with st.expander("🔐 Consola de Enlaces y Métricas del Ponente", expanded=not st.session_state.admin_autenticado):
        if not st.session_state.admin_autenticado:
            input_password = st.text_input("Contraseña de Ponente:", type="password", key="admin_pwd_input")
            if st.button("🔑 Desbloquear Consola Organizacional", width="stretch"):
                if input_password == PASSWORD_CORRECTO:
                    st.session_state.admin_autenticado = True
                    st.rerun()
                else:
                    st.error("Acceso denegado.")
        else:
            st.success("💻 Modo Ponente Activo - Configuración de Audiencia en Vivo")
            
            # Espacios dedicados para pegar y persistir los enlaces de Google Forms
            st.session_state.link_primario = st.text_input("🔗 URL Google Form - Sector Primario:", st.session_state.link_primario)
            st.session_state.link_secundario = st.text_input("🔗 URL Google Form - Sector Secundario:", st.session_state.link_secundario)
            st.session_state.link_terciario = st.text_input("🔗 URL Google Form - Sector Terciario:", st.session_state.link_terciario)
            st.session_state.link_educativo = st.text_input("🔗 URL Google Form - Sector Educativo (Docentes/ITAP):", st.session_state.link_educativo)
            st.session_state.link_religioso = st.text_input("🔗 URL Google Form - Sector Religioso:", st.session_state.link_religioso)
            
            st.write("---")
            if st.button("🔄 Actualizar Estadísticas (Salud Integral - Nube)"):
                sheet = conectar_google_sheets()
                if sheet:
                    records = sheet.get_all_records()
                    if records:
                        df = pd.DataFrame(records)
                        columnas_dimensiones = {"Salud Física (SF)": df.columns, "Salud Mental (SM)": df.columns, "Salud Emocional (SE)": df.columns, "Salud Social (SS)": df.columns, "Salud Económica (SECO)": df.columns, "Salud Temporal (ST)": df.columns, "Salud Espiritual (SPI)": df.columns}
                        promedios = {gajo: pd.to_numeric(df[col], errors='coerce').fillna(0).mean() for gajo, col in columnas_dimensiones.items()}
                        df_grafica = pd.DataFrame(list(promedios.items()), columns=["Dimension", "Promedio de Puntos de Fuga"])
                        st.write(f"**Total de participantes evaluados:** {len(df)}")
                        st.bar_chart(data=df_grafica, x="Dimension", y="Promedio de Puntos de Fuga", color="#e65100")

# Interceptor de caducidad por Token de Tiempo (Aplica solo para el formulario Mandarina Nativo)
token_actual = st.query_params.get("token", None)
acceso_bloqueado = False
if token_actual and not st.session_state.admin_autenticado:
    minuto_base = int(time.time() // 60)
    tokens_validos = [hashlib.md5(f"mandarina_secret_{minuto_base - i}".encode()).hexdigest()[:8] for i in range(5)]
    if token_actual not in tokens_validos:
        acceso_bloqueado = True
    else:
        sheet = conectar_google_sheets()
        if sheet:
            try:
                registros = sheet.get_all_records()
                if registros:
                    df_check = pd.DataFrame(registros)
                    if token_actual in [str(r.get(df_check.columns[-1], "")) for r in registros]:
                        acceso_bloqueado = True
            except Exception: pass

if acceso_bloqueado:
    st.error("🚫 El código QR escaneado ha expirado o ya fue utilizado.")
    st.stop()


# Creación formal de la matriz de pestañas del Ecosistema
tab_mandarina, tab_primario, tab_secundario, tab_terciario, tab_educativo, tab_religioso = st.tabs([
    "🍊 Salud Integral", "🚜 Sector Primario", "🏭 Sector Secundario", "💼 Sector Terciario", "🏛️ Sector Educativo", "⛪ Sector Religioso"
])

# CONTENEDOR PESTAÑA 1: CUESTIONARIO MANDARINA ORIGINAL COMPLETO
with tab_mandarina:
    if not st.session_state.flujo_finalizado:
        st.header("📋 Datos de Control")
        nombre = st.text_input("Nombre Completo *:", placeholder="Ej. Juan Pérez", key="input_nombre_unico")
        whatsapp = st.text_input("Número de Contacto de WhatsApp *:", placeholder="Ej. +52 633 123 4567", key="input_whatsapp_unico")
        st.divider()

        st.header("📊 Evaluación de las 7 Dimensiones")
        st.write("Selecciona los elementos específicos en los que requieres intervención:")
        resultados_totales = {}

        st.subheader("💪 Salud Física (SF)")
        sf_items = ["Nutrición (Hábitos alimenticios)", "Sueño (Calidad del descanso)", "Ejercicio (Actividad estructurada)", "Movimiento (Evitar sedentarismo)"]
        resultados_totales["Salud Fisica (SF)"] = [i for i in sf_items if st.checkbox(i, key=f"sf_{i}")]

        st.subheader("🧠 Salud Mental (SM)")
        sm_items = ["Memoria (Retención y agilidad)", "Enfoque (Evitar distracciones)", "Resiliencia (Adaptación al cambio)", "Aprendizaje (Nuevas habilidades)"]
        resultados_totales["Salud Mental (SM)"] = [i for i in sm_items if st.checkbox(i, key=f"sm_{i}")]

        st.subheader("❤️ Salud Emocional (SE)")
        se_items = ["Gestión de emociones", "Autocontrol (Dominio propio)", "Regulación psicológica", "Comprensión del estado de ánimo"]
        resultados_totales["Salud Emocional (SE)"] = [i for i in se_items if st.checkbox(i, key=f"se_{i}")]

        st.subheader("👥 Salud Social (SS)")
        ss_items = ["Relaciones positivas (Vínculos sanos)", "Comunicación asertiva", "Empatía activa", "Red de apoyo ante crisis"]
        resultados_totales["Salud Social (SS)"] = [i for i in ss_items if st.checkbox(i, key=f"ss_{i}")]

        st.subheader("💰 Salud Económica (SECO)")
        seco_items = ["Presupuesto (Control de gastos)", "Ahorro sistemático", "Inversión de capital", "Administración Financiera", "Creación / Generación del dinero"]
        resultados_totales["Salud Economica (SECO)"] = [i for i in seco_items if st.checkbox(i, key=f"seco_{i}")]

        st.subheader("⏳ Salud Temporal (ST)")
        ck_marcado = st.checkbox("Cronos & Kairos (Tiempo del reloj vs. valor real)", key="st_ck")
        st_items = ["Gestión del tiempo (Agenda)", "Equilibrio (Deber/Descanso)", "Prioridades (Identificar lo importante)"]
        st_sel = [i for i in st_items if st.checkbox(i, key=f"st_{i}")]
        if ck_marcado: st_sel.append("Cronos & Kairos (Tiempo del reloj vs. valor real)")
        resultados_totales["Salud Temporal (ST)"] = st_sel

        st.subheader("🙏 Salud Espiritual (SPI)")
        spi_items = ["Propósito (Sentido de vida)", "Valores (Alineación de actos)", "Meditación u oración", "Conexión del interior con el exterior"]
        resultados_totales["Salud Espiritual (SPI)"] = [i for i in spi_items if st.checkbox(i, key=f"spi_{i}")]


        st.divider()
        col_btn1, col_btn2 = st.columns(2)
        campos_completos = bool(nombre.strip()) and bool(whatsapp.strip())

        with col_btn1:
            if st.button("💾 Guardar y Procesar Diagnóstico", width="stretch", type="primary"):
                if not campos_completos: st.error("⚠️ Datos obligatorios incompletos.")
                else:
                    with st.spinner("Registrando..."):
                        exito = guardar_en_google_sheets(nombre, whatsapp, resultados_totales, token_actual)
                        if exito: st.session_state.guardado_exitoso = True; st.success("¡Guardado en la nube!")
                        else: st.session_state.guardado_exitoso = True; st.warning("Procesado localmente.")

        with col_btn2:
            if st.session_state.guardado_exitoso and campos_completos:
                reporte_procesado = generar_pdf_diagnostico(nombre, whatsapp, resultados_totales, ck_marcado)
                nombre_archivo = nombre.replace(' ', '_') if nombre else 'Participante'
                def callback_cierre():
                    st.session_state.flujo_finalizado = True
                    for k in list(st.session_state.keys()):
                        if k.startswith(("sf_", "sm_", "se_", "ss_", "seco_", "st_", "spi_")): del st.session_state[k]
                st.download_button(label="DESCARGAR RESULTADOS EN PDF 📥", data=reporte_procesado, file_name=f"Diagnostico_Mandarina_{nombre_archivo}.pdf", mime="application/pdf", on_click=callback_cierre)
            else: st.info("💡 Procesa para activar descarga.")
    else:
        st.balloons()
        st.success("### ¡Tu reporte PDF ha sido generado y descargado con éxito! 🎉")
        with st.container(border=True):
            st.write("## 🍊 ¡Muchas gracias por tu participación!")
            st.markdown("Has mapeado de forma honesta cada uno de tus gajos de bienestar. Te invitamos a agendar una sesión de consulta personalizada con el ponente.")
            st.info("👉 Acércate al término de la ponencia o solicita tu espacio de asesoramiento directamente en el escenario.")

# FUNCIÓN AUXILIAR PARA GENERAR QR DE GOOGLE FORMS SOBRE LAS PESTAÑAS RESTANTES
def renderizar_lanzador_forms(titulo_sector, url_destino):
    st.header(f"📊 Diagnóstico: {titulo_sector}")
    if url_destino.strip():
        col_x, col_y = st.columns([1, 1.5])
        with col_x:
            qr_f = qrcode.QRCode(version=1, box_size=10, border=2)
            qr_f.add_data(url_destino)
            qr_f.make(fit=True)
            img_f = qr_f.make_image(fill_color="#e65100", back_color="white")
            buf_f = BytesIO()
            img_f.save(buf_f, format="PNG")
            st.image(buf_f.getvalue(), caption=f"QR {titulo_sector}", width="stretch")
        with col_y:
            st.write(f"### ¡Escanea para responder el cuestionario del {titulo_sector}!")
            st.write("1. Enfoca el código QR con la cámara de tu móvil.")
            st.write("2. Completa los reactivos en la plataforma de Google Forms.")
            st.markdown(f'[🔗 Enlace Alterno de Acceso Directo]({url_destino})')
    else:
        st.warning("⚠️ El ponente aún no ha configurado el enlace de Google Form para este sector en la Consola de Control superior.")

# INYECCIÓN DINÁMICA DE LANZADORES EN SUS RESPECTIVAS PESTAÑAS (TABS)
with tab_primario: renderizar_lanzador_forms("Sector Primario", st.session_state.link_primario)
with tab_secundario: renderizar_lanzador_forms("Sector Secundario", st.session_state.link_secundario)
with tab_terciario: renderizar_lanzador_forms("Sector Terciario", st.session_state.link_terciario)
with tab_educativo: renderizar_lanzador_forms("Sector Educativo (Docentes)", st.session_state.link_educativo)
with tab_religioso: renderizar_lanzador_forms("Sector Religioso", st.session_state.link_religioso)
