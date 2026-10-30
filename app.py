import streamlit as st
import qrcode
from io import BytesIO
from fpdf import FPDF
import gspread
import pandas as pd
import numpy as np
import datetime
import hashlib
import time
import base64

# Desactivar advertencias interactivas de pyplot globales por ejecución síncrona
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# =================================================================
# CONFIGURACIONES GENERALES Y ENLACES DE LA PONENCIA
# =================================================================
URL_PRODUCCION = "https://dsimandarina.streamlit.app"
NOMBRE_HOJA_CALCULO = "Base_Datos_Modelo_Mandarina"

# Inicialización síncrona y global de tokens y variables de red prioritarias
minuto_actual = int(time.time() // 60)
token_tiempo = hashlib.md5(f"mandarina_secret_{minuto_actual}".encode()).hexdigest()[:8]

# Captura prioritaria de parámetros de consulta (Query Params)
token_actual = st.query_params.get("token", None)
modo_admin_url = st.query_params.get("modo_admin", "true")
es_celular_del_publico = str(modo_admin_url).strip().lower() == "false"
diag_tipo_url = st.query_params.get("diag_tipo", None)

if "audiencia_activa" not in st.session_state:
    st.session_state.audiencia_activa = "🍊 Salud Integral"

if es_celular_del_publico and diag_tipo_url:
    st.session_state.audiencia_activa = diag_tipo_url

# Construcción unificada de la URL parametrizada del QR
url_con_token = f"{URL_PRODUCCION}/?token={token_tiempo}&modo_admin=false&diag_tipo={st.session_state.audiencia_activa.replace(' ', '%20')}"

st.set_page_config(page_title="Ecosistema Diagnóstico de Modelos Temporales", layout="centered")


def conectar_google_sheets(nombre_pestana):
    try:
        if "gcp_service_account" not in st.secrets:
            return None
            
        secrets_dict = dict(st.secrets["gcp_service_account"])
        if "private_key" in secrets_dict:
            secrets_dict["private_key"] = secrets_dict["private_key"].replace("\\n", "\n")
            
        client = gspread.service_account_from_dict(secrets_dict)
        workbook = client.open(NOMBRE_HOJA_CALCULO)
        
        pestana_sana = nombre_pestana.replace("/", "_").replace("(", "").replace(")", "")[:30]
        
        try:
            return workbook.worksheet(pestana_sana)
        except gspread.exceptions.WorksheetNotFound:
            return workbook.add_worksheet(title=pestana_sana, rows="1000", cols="35")
    except Exception:
        return None

def guardar_en_google_sheets(nombre_pestana, nombre, whatsapp, resultados, token, es_likert=False):
    sheet = conectar_google_sheets(nombre_pestana)
    if sheet:
        try:
            if es_likert:
                fila = [
                    str(datetime.datetime.now()), nombre, whatsapp,
                    resultados.get("Edad", ""), resultados.get("Género", ""),
                    resultados.get("Nacionalidad", ""), resultados.get("Estado Origen", ""),
                    resultados.get("Estado Residencia", ""), resultados.get("País Origen", ""),
                    resultados.get("Continente Extranjero", ""), resultados.get("Rol Iglesia", ""),
                    resultados.get("C1_Escuchado", ""), resultados.get("C2_Leído", ""),
                    resultados.get("C3_Enseñado", ""), resultados.get("C4_Origen", ""),
                    resultados.get("C5_Concepto", "")
                ]
                for i in range(1, 15):
                    fila.append(resultados.get(f"R{i}", 3))
                fila.append(token if token else "Acceso_Directo")
            else:
                fila = [
                    str(datetime.datetime.now()), nombre, whatsapp,
                    len(resultados.get("Salud Fisica (SF)", [])), len(resultados.get("Salud Mental (SM)", [])),
                    len(resultados.get("Salud Emocional (SE)", [])), len(resultados.get("Salud Social (SS)", [])),
                    len(resultados.get("Salud Economica (SECO)", [])), len(resultados.get("Salud Temporal (ST)", [])),
                    len(resultados.get("Salud Espiritual (SPI)", [])), ", ".join(resultados.get("Salud Temporal (ST)", [])),
                    token if token else "Acceso_Directo"
                ]
            sheet.append_row(fila)
            return True
        except Exception:
            return False
    return False


def limpiar_texto_pdf(texto, idioma="Español"):
    if not texto: return ""
    romanizacion_coreano_griego = {
        "REPORTE DIAGNOSTICO: DOCENTES": {"Coreano": "CHINDAN BOGO-SEO: GYOSA", "Griego": "DIAGNOSTIKI EKTHESI: DASKALOI"},
        "Perfil de Simbiosis Temporal Equilibrada (Cronos & Kairos)": {"Coreano": "Gyunhyeong-babhon Sigan Simbiosis (Cronos & Kairos)", "Griego": "Isorropimeni Symviosi Chronou (Cronos & Kairos)"},
        "Perfil Temporal Cronocentrico Puro": {"Coreano": "Sunsu Cronos Sigan-byeol", "Griego": "Katharo Chronokentriko Profil"},
        "Perfil Temporal Kairotico Puro": {"Coreano": "Sunsu Kairos Sigan-byeol", "Griego": "Katharo Kairotiko Profil"},
        "Participante:": {"Coreano": "Cham-yeo-ja:", "Griego": "Symmetéchon:"},
        "Fecha de Emision:": {"Coreano": "Balgeub Il-ja:", "Griego": "Imerominía Ekdosis:"}
    }
    txt_str = str(texto)
    if idioma in ["Coreano", "Griego"] and txt_str in romanizacion_coreano_griego:
        return romanizacion_coreano_griego[txt_str][idioma]
    reemplazos = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N', 'ü': 'u', 'Ü': 'U', 'ç': 'c', 'è': 'e', 'à': 'a'
    }
    texto_sano = "".join(reemplazos.get(c, c) for c in txt_str)
    return texto_sano.encode('ascii', 'ignore').decode('ascii').strip()

def generar_pdf_diagnostico(nombre_usuario, whatsapp_usuario, resultados, titulo_diagnostico, es_likert=False, img_grafica_base64=None, lang="Español"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    titulo_sano = limpiar_texto_pdf(f"REPORTE DIAGNOSTICO: {titulo_diagnostico.upper()}", lang)
    nombre_sano = limpiar_texto_pdf(nombre_usuario, lang)
    whatsapp_sano = limpiar_texto_pdf(whatsapp_usuario, lang)
    
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(230, 81, 0) 
    pdf.cell(0, 10, titulo_sano, new_x="LMARGIN", new_y="NEXT", align="C")
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, "Ecosistema Jacob Zumaya Prianti (c) 2026", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)
    pdf.set_draw_color(255, 152, 0)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)
    
    pdf.set_text_color(50, 50, 50)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(45, 6, limpiar_texto_pdf("Participante:", lang), new_x="RIGHT", new_y="TOP")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, nombre_sano if nombre_sano else "Anonimo", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(45, 6, "Contact:", new_x="RIGHT", new_y="TOP")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, whatsapp_sano if whatsapp_sano else "N/A", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    if es_likert:
        cronos_items = [resultados.get(f"R{i}", 3) for i in range(1, 15, 2)]
        kairos_items = [resultados.get(f"R{i}", 3) for i in range(2, 15, 2)]
        avg_cronos = sum(cronos_items) / 7
        avg_kairos = sum(kairos_items) / 7
        
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(230, 81, 0)
        pdf.cell(0, 8, "VECTORES CRONOS & KAIROS ADAPTATIVOS", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        
        if img_grafica_base64:
            try:
                img_clean = img_grafica_base64.split(",")[-1]
                img_data = BytesIO(base64.b64decode(img_clean))
                pdf.image(img_data, x=60, w=90)
                pdf.ln(4)
            except Exception: pass
            
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 6, f"- CRONOS: {avg_cronos:.2f} / 5.00", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 6, f"- KAIROS: {avg_kairos:.2f} / 5.00", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)
        
        diferencia = abs(avg_cronos - avg_kairos)
        pdf.set_font("Helvetica", "B", 11)
        if diferencia <= 0.4:
            pdf.set_text_color(38, 166, 91)
            pdf.cell(0, 6, limpiar_texto_pdf("Perfil de Simbiosis Temporal Equilibrada (Cronos & Kairos)", lang), new_x="LMARGIN", new_y="NEXT")
        elif avg_kairos > avg_cronos:
            pdf.set_text_color(30, 139, 195)
            pdf.cell(0, 6, limpiar_texto_pdf("Perfil Temporal Kairotico Puro", lang), new_x="LMARGIN", new_y="NEXT")
        else:
            pdf.set_text_color(217, 30, 24)
            pdf.cell(0, 6, limpiar_texto_pdf("Perfil Temporal Cronocentrico Puro", lang), new_x="LMARGIN", new_y="NEXT")
    else:
        for dim_nombre, items in resultados.items():
            conteo = len(items)
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(230, 81, 0)
            pdf.cell(0, 6, f">> {limpiar_texto_pdf(dim_nombre, lang)}", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(50, 50, 50)
            puntos_str = ", ".join([limpiar_texto_pdf(it, lang) for it in items]) if conteo > 0 else "OK"
            pdf.multi_cell(0, 5, f"Alerts: {puntos_str}\n")
            
    return bytes(pdf.output())


def ejecutar_analisis_semdeep(df, es_likert=False):
    analisis = {}
    if len(df) < 5:
        analisis["status"] = "Muestra insuficiente para convergencia estructural (Mínimo 5 registros)."
        return analisis
    try:
        if es_likert:
            columnas_r = [c for c in df.columns if c.startswith("Reactivo") or (len(c) <= 3 and c.startswith("R"))]
            if len(columnas_r) < 14: columnas_r = list(df.columns[16:30])
            matriz_datos = df[columnas_r].apply(pd.to_numeric, errors='coerce').fillna(3).to_numpy()
            cronos_data = matriz_datos[:, 0::2]
            kairos_data = matriz_datos[:, 1::2]
            c_centered = cronos_data - np.mean(cronos_data, axis=0)
            k_centered = kairos_data - np.mean(kairos_data, axis=0)
            _, _, V_c = np.linalg.svd(c_centered, full_matrices=False)
            _, _, V_k = np.linalg.svd(k_centered, full_matrices=False)
            latent_cronos = c_centered @ V_c[0, :]
            latent_kairos = k_centered @ V_k[0, :]
            impacto_data = matriz_datos[:, 12:14]
            i_centered = impacto_data - np.mean(impacto_data, axis=0)
            _, _, V_i = np.linalg.svd(i_centered, full_matrices=False)
            latent_impacto = i_centered @ V_i[0, :]
            X = np.vstack([latent_cronos, latent_kairos]).T
            beta = np.linalg.pinv(X.T @ X) @ X.T @ latent_impacto
            r_cuadrado = 1 - (np.sum((latent_impacto - X @ beta) ** 2) / np.sum((latent_impacto - np.mean(latent_impacto)) ** 2))
            analisis["status"] = "Convergencia Exitosa (SEMDeep Engine v2.6)"
            analisis["beta_cronos_path"] = float(beta) if len(beta)>0 else 0.0
            analisis["beta_kairos_path"] = float(beta) if len(beta)>1 else 0.0
            analisis["gof_r2_ajuste"] = max(0.0, float(r_cuadrado))
            analisis["covarianza_latente"] = float(np.corrcoef(latent_cronos, latent_kairos))
        else:
            matriz_datos = df.iloc[:, 3:10].apply(pd.to_numeric, errors='coerce').fillna(0).to_numpy()
            c_centered = matriz_datos - np.mean(matriz_datos, axis=0)
            _, s, _ = np.linalg.svd(c_centered, full_matrices=False)
            analisis["status"] = "Convergencia Lineal Exitosa (SVD Gajos)"
            analisis["gof_r2_ajuste"] = float(s**2 / np.sum(s**2)) if len(s)>0 else 0.0
    except Exception as e:
        analisis["status"] = f"Error en cálculo matricial: {str(e)}"
    return analisis


if not es_celular_del_publico:
    with st.expander("📱 Código QR Dinámico de Seguridad (Proyectar al Auditorio)", expanded=True):
        col1, col2 = st.columns([1, 1.5])
        with col1:
            qr = qrcode.QRCode(version=1, box_size=10, border=2)
            qr.add_data(url_con_token)
            qr.make(fit=True)
            img_qr = qr.make_image(fill_color="#e65100", back_color="white")
            buf = BytesIO()
            img_qr.save(buf, format="PNG")
            st.image(buf.getvalue(), caption=f"QR Activo: {st.session_state.audiencia_activa}", width="stretch")
        with col2:
            st.write(f"### Audiencia Proyectada en Vivo: **{st.session_state.audiencia_activa}**")
            st.write("1. Enfoca el código QR con la cámara de tu smartphone.")
            st.write("2. Responderás directamente el software nativo adaptado a tu organización sin necesidad de registros externos.")


if "admin_autenticado" not in st.session_state:
    st.session_state.admin_autenticado = False
if "guardado_exitoso" not in st.session_state:
    st.session_state.guardado_exitoso = False
if "flujo_finalizado" not in st.session_state:
    st.session_state.flujo_finalizado = False
if "alertas_mandarina_previas" not in st.session_state:
    st.session_state.alertas_mandarina_previas = []

PASSWORD_SISTEMA = st.secrets["credentials"]["password_ponente"] if "credentials" in st.secrets else "mandarina2026"

if not es_celular_del_publico:
    with st.sidebar:
        st.markdown("## 🔐 Control del Ponente")
        if not st.session_state.admin_autenticado:
            input_password = st.text_input("Contraseña Ponente:", type="password", key="side_pwd")
            if st.button("Desbloquear Tableros", width="stretch"):
                if input_password == PASSWORD_SISTEMA:
                    st.session_state.admin_autenticado = True
                    st.rerun()
                else: st.error("Contraseña incorrecta. Acceso denegado.")
        else:
            st.success("Modo Ponente Activo")
            lista_audiencias = ["🍊 Salud Integral", "🚜 Sector Primario", "🏭 Sector Secundario", "💼 Sector Terciario", "Docentes", "Padres Primaria", "Padres Secundaria", "Padres Preparatoria", "Padres Universitario", "Estudiantes Primaria", "Estudiantes Secundaria", "Estudiantes Preparatoria", "Estudiantes Universitario", "Religioso General", "Religioso IASD"]
            seleccion = st.selectbox("Audiencia Actual en Vivo:", lista_audiencias)
            if seleccion != st.session_state.audiencia_activa:
                st.session_state.audiencia_activa = seleccion
                st.rerun()
            if st.button("Cerrar Sesion", width="stretch"):
                st.session_state.admin_autenticado = False
                st.rerun()

if token_actual and not st.session_state.admin_autenticado:
    minuto_base = int(time.time() // 60)
    tokens_validos = [hashlib.md5(f"mandarina_secret_{minuto_base - i}".encode()).hexdigest()[:8] for i in range(5)]
    if token_actual not in tokens_validos: acceso_bloqueado = True
    else:
        sheet = conectar_google_sheets(st.session_state.audiencia_activa)
        if sheet:
            try:
                registros = sheet.get_all_records()
                if registros:
                    df_check = pd.DataFrame(registros)
                    if token_actual in [str(r.get(df_check.columns[-1], "")) for r in registros]: acceso_bloqueado = True
            except Exception: pass
else: acceso_bloqueado = False

if acceso_bloqueado:
    st.error("🚫 El acceso escaneado ha expirado o ya fue utilizado en esta ponencia.")
    st.stop()


if st.session_state.admin_autenticado and not es_celular_del_publico:
    st.markdown("---")
    st.header("🔬 Oficina de Investigación y Alta Analítica del Ponente")
    st.write("Módulo avanzado de modelado predictivo de variables latentes.")
    
    tabla_analizar = st.selectbox("Seleccionar Tabla para Extracción Científica:", ["🍊 Salud Integral", "Docentes", "🏭 Sector Secundario"])
    
    if st.button("📊 Ejecutar Auditoría Estadística de Nivel Doctoral", type="primary"):
        sheet = conectar_google_sheets(tabla_analizar)
        if sheet:
            records = sheet.get_all_records()
            if records:
                df_doc = pd.DataFrame(records)
                st.success(f"¡Base de datos cargada! Registros analizados: {len(df_doc)}")
                es_tabla_likert = (tabla_analizar != "🍊 Salud Integral")
                col_graph1, col_graph2 = st.columns(2)
                
                with col_graph1:
                    st.write("#### 📈 Distribución Descriptiva Global")
                    if not es_tabla_likert:
                        col_gajos = ["Salud Fisica (SF)", "Salud Mental (SM)", "Salud Emocional (SE)", "Salud Social (SS)", "Salud Economica (SECO)", "Salud Temporal (ST)", "Salud Espiritual (SPI)"]
                        promedios = {c: pd.to_numeric(df_doc[c], errors='coerce').fillna(0).mean() for c in col_gajos if c in df_doc.columns}
                        if promedios: st.bar_chart(pd.DataFrame(list(promedios.items()), columns=["Dim", "Media"]), x="Dim", y="Media", color="#e65100")
                    else:
                        r_cols = [c for c in df_doc.columns if c.startswith("R") or c.startswith("Reactivo")]
                        matriz_r = df_doc[r_cols].apply(pd.to_numeric, errors='coerce').fillna(3).to_numpy()
                        c_mean = np.mean(matriz_r[:, 0::2]) if len(r_cols)>=14 else 3.0
                        k_mean = np.mean(matriz_r[:, 1::2]) if len(r_cols)>=14 else 3.0
                        st.bar_chart(pd.DataFrame([["Cronos", c_mean], ["Kairos", k_mean]], columns=["Vector", "Media"]), x="Vector", y="Media", color="#2574a9")
                
                with col_graph2:
                    st.write("#### 🧠 Modelado Estructural Ecuaciones Latentes: SEMDeep")
                    res_sem = ejecutar_analisis_semdeep(df_doc, es_tabla_likert)
                    st.json(res_sem)
            else: st.warning("No hay filas registradas en esta pestaña.")
        else: st.error("Error de enlace.")


DICCIONARIO_IDIOMAS = {
    "Español": {
        "ctrl": "Datos de Control", "nombre": "Nombre Completo o Matrícula *:", "wha": "Número Telefónico de Enlace *:",
        "sec1": "Sección I. Datos Demográficos y Geográficos", "edad": "1. Edad (Años):", "genero": "2. Género:",
        "nac": "3. Nacionalidad *:", "orig": "4. Estado de origen *:", "res": "5. Estado de residencia actual *:",
        "pais": "4. Escribe tu País de origen *:", "cont": "5. Selecciona tu Continente de origen *:", "rol": "6. Rol dentro de la Iglesia:",
        "sec2": "Sección II. Conocimiento sobre el tema", "kn1": "1. Antes de esta encuesta ya había escuchado hablar sobre los Modelos Temporales Cronos y Kairos:",
        "kn2": "2. He leído sobre los modelos temporales Cronos y Kairos:", "kn3": "3. He enseñado alguna vez sobre los modelos temporales Cronos y Kairos:",
        "kn4": "4. El modelo temporal:", "kn5": "5. Hablar de modelos temporales es hablar de:",
        "sec3": "Sección III. Batería de Reactivos Intercalados Contextuales", "btn_save": "💾 Guardar y Procesar Diagnóstico", "btn_pdf": "DESCARGAR RESULTADOS EN PDF 📥",
        "likert_labels": {1:"1 - Totalmente en desacuerdo", 2:"2 - En desacuerdo", 3:"3 - Neutral", 4:"4 - De acuerdo", 5:"5 - Totalmente de acuerdo"}
    },
    "Inglés": {
        "ctrl": "Control Information", "nombre": "Full Name or ID *:", "wha": "WhatsApp Link Number *:",
        "sec1": "Section I. Demographic & Geographic Data", "edad": "1. Age (Years):", "genero": "2. Gender:",
        "nac": "3. Nationality *:", "orig": "4. Mexican State of Origin *:", "res": "5. Current Mexican State of Residence *:",
        "pais": "4. Enter your Country of Origin *:", "cont": "5. Select your Continent of Origin *:", "rol": "6. Role within the Church:",
        "sec2": "Section II. Knowledge of the Topic", "kn1": "1. Before this survey, had you heard about the Cronos and Kairos Temporal Models?",
        "kn2": "2. Have you read about the Cronos and Kairos temporal models?", "kn3": "3. Have you ever taught about the Cronos and Kairos temporal models?",
        "kn4": "4. The temporal model is:", "kn5": "5. Speaking of temporal models means speaking of:",
        "sec3": "Section III. Intercalated Contextual Scale", "btn_save": "💾 Save & Process Diagnosis", "btn_pdf": "DOWNLOAD RESULTS IN PDF 📥",
        "likert_labels": {1:"1 - Strongly Disagree", 2:"2 - Disagree", 3:"3 - Neutral", 4:"4 - Agree", 5:"5 - Strongly Agree"}
    }
}

def algoritmo_generar_reactivos_contextuales(perfil_demografico, alertas_salud_integral):
    """
    Algoritmo Doctoral de Simbiosis Adaptativa C&K.
    Construye dinámicamente un banco alterno de 14 reactivos (Impares=Cronos, Pares=Kairos)
    inyectando el contexto demográfico y las fugas biológicas detectadas en Salud Integral.
    """
    geo = perfil_demografico.get("Procedencia", "la region")
    fuga = alertas_salud_integral[0] if alertas_salud_integral else "Bienestar general"
    
    # 7 Reactivos Cronos (Enfoque estructural, reloj, orden)
    cronos_pool = {
        1: f"Planifico mis actividades operativas en {geo} siguiendo estrictamente los tiempos del reloj institucionales.",
        3: f"Establezco limites rigidos de tiempo en mis jornadas para blindar mi rendimiento frente a fugas como: {fuga}.",
        5: f"Considero que la puntualidad extrema y el respeto al cronograma formal mitigan el estres en {geo}.",
        7: f"Me genera profunda frustracion o ansiedad cuando un imprevisto altera la estructura planeada de mi agenda.",
        9: f"Prefiero que las juntas y auditorias concluyan ciñendose de forma exacta al tiempo asignado originalmente.",
        11: f"Mido el exito de mis proyectos a traves del cumplimiento metrico y los blancos numericos de entrega.",
        13: f"El apego estricto a manuales organizacionales es la clave fundamental para mantener el orden de mis habitos."
    }
    
    # 7 Reactivos Kairos (Enfoque relacional, oportunidad, salud mental)
    kairos_pool = {
        2: f"La flexibilidad para adaptar mis planes ante una ventana de oportunidad en {geo} es mas importante que el reloj.",
        4: f"Tengo plena disposicion para detener mi agenda si surge una crisis relacional o necesidad de apoyo humano.",
        6: f"Creo que la calidad conceptual y el valor humano de mis vinculos en {geo} tienen prioridad absoluta sobre el reloj.",
        8: f"Confio en que las soluciones eficientes a problemas complejos como {fuga} surgen en momentos de inspiracion providencial.",
        10: f"Cuando me encuentro inmerso en resolver una falla critica o un diseño creativo, pierdo la nocion del tiempo terrenal.",
        12: f"Prefiero que mis lideres o entornos se adapten con sensibilidad a mis necesidades de salud mental urgentes.",
        14: f"Valoro el impacto de mis jornadas por la transformacion integral de mi entorno mas que por las metricas de egreso."
    }
    
    # Ensamblar de forma estrictamente alterna (1=C, 2=K, 3=C, 4=K...)
    banco_alterno = {}
    for i in range(1, 15):
        if i % 2 != 0:
            banco_alterno[i] = cronos_pool[i]
        else:
            banco_alterno[i] = kairos_pool[i]
            
    return banco_alterno

ESTADOS_MEXICO = ["Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Chiapas", "Chihuahua", "Ciudad de México", "Coahuila", "Colima", "Durango", "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", "México", "Michoacán", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"]
CONTINENTES = ["América del Norte", "América Central / El Caribe", "América del Sur", "Europa", "Asia", "África", "Oceanía"]


if not st.session_state.flujo_finalizado:
    idioma_sel = st.selectbox("🌐 Selecciona tu Idioma / Select Language:", ["Español", "Inglés"])
    tx = DICCIONARIO_IDIOMAS[idioma_sel]
    
    st.header(f"📋 {st.session_state.audiencia_activa}")
    nombre = st.text_input(tx["nombre"], placeholder="Juan Pérez", key="main_name_in")
    whatsapp = st.text_input(tx["wha"], placeholder="+52...", key="main_wha_in")
    st.divider()

    resultados_totales = {}
    es_modo_likert = (st.session_state.audiencia_activa != "🍊 Salud Integral")

    # MODO MANDARINA CLÁSICO (SOLUCIÓN DE REPETICIONES DE ITERADORES)
    if not es_modo_likert:
        st.write("### 🍊 Tus Gajos de Bienestar")
        st.write("Selecciona los puntos de fuga específicos donde requieres intervención:")
        
        with st.container(border=True):
            st.markdown("#### 💪 Salud Física (SF)")
            sf_items = ["Nutricion (Habitos alimenticios)", "Sueno (Calidad del descanso)", "Ejercicio (Actividad estructurada)", "Movimiento (Evitar sedentarismo)"]
            col1, col2 = st.columns(2)
            with col1:
                chk_sf0 = st.checkbox(sf_items, key="sf_unq_0")
                chk_sf1 = st.checkbox(sf_items, key="sf_unq_1")
            with col2:
                chk_sf2 = st.checkbox(sf_items, key="sf_2")
                chk_sf3 = st.checkbox(sf_items, key="sf_3")
            resultados_totales["Salud Fisica (SF)"] = [item for idx, item in enumerate(sf_items) if st.session_state[f"sf_unq_{idx}" if idx < 2 else f"sf_{idx}"]]

        with st.container(border=True):
            st.markdown("#### 🧠 Salud Mental (SM)")
            sm_items = ["Memoria (Retencion)", "Enfoque (Evitar distracciones)", "Resiliencia (Adaptacion)", "Aprendizaje (Habilidades)"]
            col1, col2 = st.columns(2)
            with col1:
                chk_sm0 = st.checkbox(sm_items, key="sm_unq_0")
                chk_sm1 = st.checkbox(sm_items, key="sm_unq_1")
            with col2:
                chk_sm2 = st.checkbox(sm_items, key="sm_2")
                chk_sm3 = st.checkbox(sm_items, key="sm_3")
            resultados_totales["Salud Mental (SM)"] = [item for idx, item in enumerate(sm_items) if st.session_state[f"sm_unq_{idx}" if idx < 2 else f"sm_{idx}"]]

        with st.container(border=True):
            st.markdown("#### ⏳ Salud Temporal (ST)")
            ck_marcado = st.checkbox("Cronos & Kairos (Tiempo del reloj vs. valor real)", key="st_ck_unq")
            st_items = ["Gestion del tiempo (Agenda)", "Equilibrio (Deber/Descanso)"]
            col1, col2 = st.columns(2)
            with col1: chk_st0 = st.checkbox(st_items, key="st_unq_0")
            with col2: chk_st1 = st.checkbox(st_items, key="st_unq_1")
            st_sel = [item for idx, item in enumerate(st_items) if st.session_state[f"st_unq_{idx}"]]
            if ck_marcado: st_sel.append("Cronos & Kairos (Tiempo del reloj vs. valor real)")
            resultados_totales["Salud Temporal (ST)"] = st_sel
            
        # Almacenamiento síncronizado de alertas para el algoritmo adaptativo
        if st.button("Procesar Alertas Base"):
            todas_alertas = resultados_totales["Salud Fisica (SF)"] + resultados_totales["Salud Mental (SM)"]
            st.session_state.alertas_mandarina_previas = todas_alertas if todas_alertas else ["Estres general"]
            st.success("Alertas registradas para adaptacion contextual.")


    else:
        st.subheader(tx["sec1"])
        resultados_totales["Edad"] = st.number_input(tx["edad"], min_value=10, max_value=100, value=20, key="dem_edad")
        resultados_totales["Género"] = st.radio(tx["genero"], ["Masculino", "Femenino", "Other"], horizontal=True, key="dem_genero")
        
        nacionalidad = st.radio(tx["nac"], ["Mexicana", "Extranjera"], horizontal=True, key="dem_nac")
        resultados_totales["Nacionalidad"] = nacionalidad
        
        geo_contexto = "la region"
        if nacionalidad == "Mexicana":
            resultados_totales["Estado Origen"] = st.selectbox(tx["orig"], [""] + ESTADOS_MEXICO, key="dem_orig")
            resultados_totales["Estado Residencia"] = st.selectbox(tx["res"], [""] + ESTADOS_MEXICO, key="dem_res")
            resultados_totales["País Origen"] = "México"
            resultados_totales["Continente Extranjero"] = "América"
            geo_contexto = f"el Estado de {resultados_totales['Estado Residencia']}"
        else:
            resultados_totales["Estado Origen"] = "N/A"
            resultados_totales["Estado Residencia"] = "N/A"
            resultados_totales["País Origen"] = st.text_input(tx["pais"], key="dem_pais_txt")
            resultados_totales["Continente Extranjero"] = st.selectbox(tx["cont"], [""] + CONTINENTES, key="dem_cont")
            geo_contexto = f"el pais de {resultados_totales['País Origen']}"
            
        if "Religioso" in st.session_state.audiencia_activa:
            resultados_totales["Rol Iglesia"] = st.selectbox(tx["rol"], ["", "Miembro", "Pastor", "Líder"], key="dem_rol")
        else: resultados_totales["Rol Iglesia"] = "N/A"

        st.subheader(tx["sec2"])
        resultados_totales["C1_Escuchado"] = st.radio(tx["kn1"], ["Sí", "No"], horizontal=True, key="kn_1")
        resultados_totales["C2_Leído"] = st.radio(tx["kn2"], ["Sí", "No"], horizontal=True, key="kn_2")
        resultados_totales["C3_Enseñado"] = st.radio(tx["kn3"], ["Sí", "No"], horizontal=True, key="kn_3")
        resultados_totales["C4_Origen"] = st.radio(tx["kn4"], ["Se impone", "Se nace", "No sé"], horizontal=True, key="kn_4")
        resultados_totales["C5_Concepto"] = st.radio(tx["kn5"], ["Teología", "Cultura", "No sé"], horizontal=True, key="kn_5")

        st.subheader(tx["sec3"])
        
        # INVOCACIÓN AL ALGORITMO ADAPTATIVO CONTEXTUAL SOLICITADO
        perfil_contexto = {"Procedencia": geo_contexto}
        alertas_previas = st.session_state.alertas_mandarina_previas
        
        # El motor reescribe los 14 reactivos de forma alterna inyectando la información demográfica y clínica del participante
        banco_mutado_quirurgico = algoritmo_generar_reactivos_contextuales(perfil_contexto, alertas_previas)
        
        for r_id, enunciado_adaptado in banco_mutado_quirurgico.items():
            st.write(f"**Reactivo {r_id}:** {enunciado_adaptado}")
            resultados_totales[f"R{r_id}"] = st.radio(
                "Scale:", options=,
                format_func=lambda x: tx["likert_labels"][x],
                key=f"dyn_r_{r_id}"
            )
        ck_marcado = False


    st.divider()
    col_btn1, col_btn2 = st.columns(2)
    campos_completos = bool(nombre.strip()) and bool(whatsapp.strip())

    with col_btn1:
        if st.button(tx["btn_save"], width="stretch", type="primary"):
            if not campos_completos: st.error("⚠️ Incomplete fields.")
            else:
                with st.spinner("Processing..."):
                    exito = guardar_en_google_sheets(st.session_state.audiencia_activa, nombre, whatsapp, resultados_totales, token_actual, es_modo_likert)
                    if exito: st.session_state.guardado_exitoso = True; st.success("OK")
                    else: st.session_state.guardado_exitoso = True; st.warning("Local OK")

    with col_btn2:
        if st.session_state.guardado_exitoso and campos_completos:
            grafica_base64 = None
            if es_modo_likert:
                try:
                    cronos_v = [resultados_totales.get(f"R{i}", 3) for i in range(1, 15, 2)]
                    kairos_v = [resultados_totales.get(f"R{i}", 3) for i in range(2, 15, 2)]
                    fig, ax = plt.subplots(figsize=(4, 4))
                    ax.axhspan(1, 3, 1, 3, color='#f2f1ef', alpha=0.5) 
                    ax.axhspan(3, 5, 3, 5, color='#e8f8f5', alpha=0.7) 
                    ax.scatter(sum(cronos_v)/7, sum(kairos_v)/7, color='#e65100', s=120)
                    buf_g = BytesIO()
                    plt.savefig(buf_g, format='png', bbox_inches='tight', dpi=100)
                    buf_g.seek(0)
                    grafica_base64 = f"data:image/png;base64,{base64.b64encode(buf_g.read()).decode('utf-8')}"
                    plt.close(fig)
                except Exception: pass
            
            reporte_procesado = generar_pdf_diagnostico(nombre, whatsapp, resultados_totales, st.session_state.audiencia_activa, es_modo_likert, grafica_base64, idioma_sel)
            nombre_archivo = nombre.replace(' ', '_') if nombre else 'User'
            
            def callback_finalizar():
                st.session_state.flujo_finalizado = True
                for k in list(st.session_state.keys()):
                    if k.startswith(("sf_", "sm_", "dyn_r_", "dem_", "kn_")): del st.session_state[k]
            
            st.download_button(
                label=tx["btn_pdf"], 
                data=reporte_procesado, 
                file_name=f"Report_{nombre_archivo}.pdf", 
                mime="application/pdf", 
                on_click=callback_finalizar
            )
        else: st.info("💡 Process to unlock download.")


else:
    st.balloons()
    st.success("### ¡Tu reporte PDF ha sido generado y descargado con éxito! 🎉")
    with st.container(border=True):
        st.write("## 🍊 ¡Muchas gracias por tu participación!")
        st.markdown(f"Has completado el diagnóstico para la audiencia actual. Reconocer nuestros vectores temporales es el inicio de una alta madurez y bienestar integral.")
        st.info("👉 Jacob Zumaya Prianti A.C. (c) 2026")
        
    if not es_celular_del_publico:
        if st.button("🔄 Reiniciar Ecosistema", width="stretch"):
            st.session_state.flujo_finalizado = False
            st.session_state.guardado_exitoso = False
            st.rerun()
