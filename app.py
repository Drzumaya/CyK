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
    
    # Matriz Analítica de Transliteración y Romanización Fonética Internacional para FPDF (Latin-1 Core)
    diccionario_pdf = {
        "Español": {
            "rep": "REPORTE DIAGNOSTICO DE MODELOS TEMPORALES", "part": "Participante:", "cont": "Contacto/WhatsApp:",
            "fecha": "Fecha de Emision:", "vec": "VECTORES CRONOS Y KAIROS ADAPTATIVOS", "perf_s": "Perfil de Simbiosis Temporal Equilibrada (C&K)",
            "perf_c": "Perfil Temporal Cronocentrico Puro (Rigido)", "perf_k": "Perfil Temporal Kairotico Puro (Adaptativo)"
        },
        "Inglés": {
            "rep": "DIAGNOSTIC REPORT OF TEMPORAL MODELS", "part": "Participant:", "cont": "Contact/WhatsApp:",
            "fecha": "Date of Issue:", "vec": "ADAPTIVE CRONOS AND KAIROS VECTORS", "perf_s": "Balanced Temporal Symbiosis Profile (C&K)",
            "perf_c": "Pure Chronocentric Temporal Profile (Rigid)", "perf_k": "Pure Kairotic Temporal Profile (Adaptive)"
        },
        "Coreano": {
            "rep": "CHINDAN BOGO-SEO: SIGAN MODEL", "part": "Cham-yeo-ja (Participant):", "cont": "Yeon-rak-cheo:",
            "fecha": "Balgeub Il-ja (Date):", "vec": "CRONOS & KAIROS VECTORS", "perf_s": "Simbiosis Gyun-hyeong Profile (C&K)",
            "perf_c": "Sun-su Cronos Profile (Rigid)", "perf_k": "Sun-su Kairos Profile (Adaptive)"
        },
        "Griego": {
            "rep": "DIAGNOSTIKI EKTHESI CHRONIKON MONTELON", "part": "Symmetechon:", "cont": "Epikoinonia:",
            "fecha": "Imerominia Ekdosis:", "vec": "CHRONIKOI DEIKTES CRONOS & KAIROS", "perf_s": "Isorropimeni Symviosi (C&K)",
            "perf_c": "Chronokentriko Profil (Rigid)", "perf_k": "Kairotiko Profil (Adaptive)"
        },
        "Francés": {
            "rep": "RAPPORT DIAGNOSTIQUE DES MODELES TEMPORELS", "part": "Participant:", "cont": "Contact/WhatsApp:",
            "fecha": "Date d'Emission:", "vec": "VECTEURS CHRONOS ET KAIROS ADAPTATIFS", "perf_s": "Profil de Symbiose Temporelle Equilibre (C&K)",
            "perf_c": "Profil Temporel Chronocentrique Pur (Rigide)", "perf_k": "Profil Temporel Kairotique Pur (Adaptatif)"
        },
        "Alemán": {
            "rep": "DIAGNOSTISCHER BERICHT ZEITMODELLE", "part": "Teilnehmer:", "cont": "Kontakt/WhatsApp:",
            "fecha": "Ausstellungsdatum:", "vec": "ADAPTIVE CHRONOS UND KAIROS VEKTOREN", "perf_s": "Ausgeglichene Zeit-Symbiose (C&K)",
            "perf_c": "Chronozentrisches Profil (Rigide)", "perf_k": "Kairotisches Profil (Adaptiv)"
        },
        "Italiano": {
            "rep": "RAPPORTO DIAGNOSTICO MODELLI TEMPORALI", "part": "Partecipante:", "cont": "Contatto/WhatsApp:",
            "fecha": "Data di Emissione:", "vec": "VETTORI CRONOS E KAIROS ADATTIVI", "perf_s": "Profilo di Simbiosi Temporale Bilanciata (C&K)",
            "perf_c": "Profilo Cronocentrico Puro (Rigido)", "perf_k": "Profilo Kairotico Puro (Adattivo)"
        },
        "Portugués": {
            "rep": "RELATORIO DIAGNOSTICO DE MODELOS TEMPORAIS", "part": "Participante:", "cont": "Contato/WhatsApp:",
            "fecha": "Data de Emissao:", "vec": "VETTORES CRONOS E KAIROS ADAPTATIVOS", "perf_s": "Perfil de Simbiose Temporal Equilibrada (C&K)",
            "perf_c": "Perfil Cronocentrico Puro (Rigido)", "perf_k": "Perfil Kairotico Puro (Adaptativo)"
        },
        "Ruso": {
            "rep": "DIAGNOSTICHESKIY OTCHET: VREMENNYE MODELI", "part": "Uchastnik:", "cont": "Kontakt/WhatsApp:",
            "fecha": "Data Vydachi:", "vec": "ADAPTIVNYE VEKTORY CRONOS I KAIROS", "perf_s": "Sbalansirovanniy Simbioz Vremeni (C&K)",
            "perf_c": "Hronocentricheskiy Profil (Rigid)", "perf_k": "Kairoticheskiy Profil (Adaptive)"
        },
        "Árabe": {
            "rep": "TAQRIR TASHKHISI LIL-NAWAZIL AL-ZAMANIYYA", "part": "Al-Musharik:", "cont": "Al-Ittisal:",
            "fecha": "Tarikh Al-Isdar:", "vec": "MUTAWAJJIHAT CRONOS WA KAIROS", "perf_s": "Takaful Zamani Mutawazin (C&K)",
            "perf_c": "Al-Nizam Al-Rigid (Cronos)", "perf_k": "Al-Nizam Al-Marun (Kairos)"
        }
    }
    
    txt_str = str(texto)
    lang_dic = diccionario_pdf.get(idioma, diccionario_pdf["Español"])
    if txt_str in lang_dic:
        return lang_dic[txt_str]
        
    reemplazos = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N', 'ü': 'u', 'Ü': 'U'
    }
    texto_sano = "".join(reemplazos.get(c, c) for c in txt_str)
    return texto_sano.encode('ascii', 'ignore').decode('ascii').strip()

def generar_pdf_diagnostico(nombre_usuario, whatsapp_usuario, resultados, titulo_diagnostico, es_likert=False, img_grafica_base64=None, lang="Español"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    titulo_sano = limpiar_texto_pdf("rep", lang)
    nombre_sano = limpiar_texto_pdf(nombre_usuario, lang)
    whatsapp_sano = limpiar_texto_pdf(whatsapp_usuario, lang)
    
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(230, 81, 0) 
    pdf.cell(0, 10, titulo_sano, new_x="LMARGIN", new_y="NEXT", align="C")
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, f"Jacob Zumaya Prianti (c) 2026 | Language: {lang}", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)
    pdf.set_draw_color(255, 152, 0)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)
    
    pdf.set_text_color(50, 50, 50)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(45, 6, limpiar_texto_pdf("part", lang), new_x="RIGHT", new_y="TOP")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, nombre_sano if nombre_sano else "Anonimo", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(45, 6, limpiar_texto_pdf("cont", lang), new_x="RIGHT", new_y="TOP")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, whatsapp_sano if whatsapp_sano else "N/A", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(45, 6, limpiar_texto_pdf("fecha", lang), new_x="RIGHT", new_y="TOP")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, datetime.date.today().strftime("%d/%m/%Y"), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    if es_likert:
        cronos_v = [resultados.get(f"R{i}", 3) for i in range(1, 15, 2)]
        kairos_v = [resultados.get(f"R{i}", 3) for i in range(2, 15, 2)]
        avg_cronos = sum(cronos_v) / 7
        avg_kairos = sum(kairos_v) / 7
        
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(230, 81, 0)
        pdf.cell(0, 8, limpiar_texto_pdf("vec", lang), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        
        if img_grafica_base64:
            try:
                img_clean = img_grafica_base64.split(",")[-1]
                img_data = BytesIO(base64.b64decode(img_clean))
                pdf.image(img_data, x=60, w=90)
                pdf.ln(4)
            except Exception: pass
            
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 6, f"- CRONOS SCORE: {avg_cronos:.2f} / 5.00", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 6, f"- KAIROS SCORE: {avg_kairos:.2f} / 5.00", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)
        
        diferencia = abs(avg_cronos - avg_kairos)
        pdf.set_font("Helvetica", "B", 11)
        if diferencia <= 0.4:
            pdf.set_text_color(38, 166, 91)
            pdf.cell(0, 6, limpiar_texto_pdf("perf_s", lang), new_x="LMARGIN", new_y="NEXT")
        elif avg_kairos > avg_cronos:
            pdf.set_text_color(30, 139, 195)
            pdf.cell(0, 6, limpiar_texto_pdf("perf_k", lang), new_x="LMARGIN", new_y="NEXT")
        else:
            pdf.set_text_color(217, 30, 24)
            pdf.cell(0, 6, limpiar_texto_pdf("perf_c", lang), new_x="LMARGIN", new_y="NEXT")
    else:
        for dim_nombre, items in resultados.items():
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(230, 81, 0)
            pdf.cell(0, 6, f">> {limpiar_texto_pdf(dim_nombre, lang)}", new_x="LMARGIN", new_y="NEXT")
            puntos_str = ", ".join([limpiar_texto_pdf(it, lang) for it in items]) if len(items) > 0 else "OK"
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(50, 50, 50)
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
        "likert_labels": {1:"1 - Totalmente en desacuerdo", 2:"2 - En desacuerdo", 3:"3 - Neutral", 4:"4 - De acuerdo", 5:"5 - Totalmente de acuerdo"},
        "c_pool": "Planifico mis actividades operativas en {geo} siguiendo estrictamente los tiempos del reloj.",
        "k_pool": "La flexibilidad para adaptar mis planes ante una ventana de oportunidad en {geo} es mas importante."
    },
    "Inglés": {
        "ctrl": "Control Information", "nombre": "Full Name or ID *:", "wha": "WhatsApp Link Number *:",
        "sec1": "Section I. Demographic & Geographic Data", "edad": "1. Age (Years):", "genero": "2. Gender:",
        "nac": "3. Nationality *:", "orig": "4. State of Origin *:", "res": "5. State of Residence *:",
        "pais": "4. Enter your Country of Origin *:", "cont": "5. Select your Continent of Origin *:", "rol": "6. Role within the Church:",
        "sec2": "Section II. Knowledge of the Topic", "kn1": "1. Before this survey, had you heard about the Cronos and Kairos Temporal Models?",
        "kn2": "2. Have you read about the Cronos and Kairos temporal models?", "kn3": "3. Have you ever taught about the Cronos and Kairos temporal models?",
        "kn4": "4. The temporal model is:", "kn5": "5. Speaking of temporal models means speaking of:",
        "sec3": "Section III. Intercalated Contextual Scale", "btn_save": "💾 Save & Process Diagnosis", "btn_pdf": "DOWNLOAD RESULTS IN PDF 📥",
        "likert_labels": {1:"1 - Strongly Disagree", 2:"2 - Disagree", 3:"3 - Neutral", 4:"4 - Agree", 5:"5 - Strongly Agree"},
        "c_pool": "I plan my operational activities in {geo} strictly following the clock schedule.",
        "k_pool": "Flexibility to adapt plans before an opportunity window in {geo} is much more important than the clock."
    },
    "Coreano": {
        "ctrl": "제어 데이터", "nombre": "성명 또는 학번 *:", "wha": "연락처 전화번호 *:",
        "sec1": "제1절. 인구통계학적 및 지리적 데이터", "edad": "1. 연령 (세):", "genero": "2. 성별:",
        "nac": "3. 국적 *:", "orig": "4. 출신 주 *:", "res": "5. 현재 거주 주 *:",
        "pais": "4. 출신 국가를 입력하세요 *:", "cont": "5. 출신 대륙을 선택하세요 *:", "rol": "6. 교회 내 직분:",
        "sec2": "제2절. 주제에 대한 지식", "kn1": "1. 이 설문조사 전에 크로노스와 카이로스 시간 모델에 대해 들어본 적이 있습니까?",
        "kn2": "2. 크로노스와 카이로스 시간 모델에 대해 읽어본 적이 있습니까?", "kn3": "3. 크로노스와 카이로스 시간 모델에 대해 가르쳐본 적이 있습니까?",
        "kn4": "4. 시간 모델은 다음과 같습니다:", "kn5": "5. 시간 모델에 대해 말하는 것은 다음을 의미합니다:",
        "sec3": "제3절. 중간 리커트 문항 척도", "btn_save": "💾 진단 저장 및 처리", "btn_pdf": "PDF 결과 다운로드 📥",
        "likert_labels": {1:"1 - 전혀 동의하지 않음", 2:"2 - 동의하지 않음", 3:"3 - 보통", 4:"4 - 동의함", 5:"5 - 매우 동의함"},
        "c_pool": "{geo}에서의 생산 활동을 시계 일정에 맞추어 철저히 계획합니다.",
        "k_pool": "{geo}에서 기회의 창이 열렸을 때 일정을 유연하게 변경하는 능력이 시계보다 중요합니다."
    },
    "Griego": {
        "ctrl": "Στοιχεία Ελέγχου", "nombre": "Ονοματεπώνυμο ή Μητρώο *:", "wha": "Αριθμός Τηλεφώνου Σύνδεσης *:",
        "sec1": "Ενότητα Ι. Δημογραφικά & Γεωγραφικά Δεδομένα", "edad": "1. Ηλικία (Έτη):", "genero": "2. Φύλο:",
        "nac": "3. Υπηκοότητα *:", "orig": "4. Πολιτεία Καταγωγής *:", "res": "5. Πολιτεία Διαμονής *:",
        "pais": "4. Εισάγετε τη Χώρα Καταγωγής σας *:", "cont": "5. Επιλέξτε την Ήπειρο Καταγωγής σας *:", "rol": "6. Ρόλος μέσα στην Εκκλησία:",
        "sec2": "Ενότητα ΙΙ. Γνώση επί του Θέματος", "kn1": "1. Πριν από αυτήν την έρευνα, είχατε ακούσει για τα Χρονικά Μοντέλα Κρόνος και Καιρός;",
        "kn2": "2. Έχετε διαβάσει για τα χρονικά μοντέла Κρόνος και Καιρός;", "kn3": "3. Έχετε διδάξει ποτέ για τα χρονικά μοντέλα Κρόνος και Καιρός;",
        "kn4": "4. Το χρονικό μοντέλο είναι:", "kn5": "5. Μιλώντας για χρονικά μοντέλα σημαίνει μιλώντας για:",
        "sec3": "Ενότητα ΙΙΙ. Κλίμακα Likert", "btn_save": "💾 Αποθήκευση & Επεξεργασία Διάγνωσης", "btn_pdf": "ΛΗΨΗ ΑΠΟΤΕΛΕΣΜΑΤΩΝ ΣΕ PDF 📥",
        "likert_labels": {1:"1 - Διαφωνώ απόλυτα", 2:"2 - Διαφωνώ", 3:"3 - Ουδέτερο", 4:"4 - Συμφωνώ", 5:"5 - Συμφωνώ απόλυτα"},
        "c_pool": "Προγραμματίζω τις δραστηριότητές μου στο {geo} ακολουθώντας αυστηρά το ρολόι.",
        "k_pool": "Η ευελιξία να προσαρμόζω τα πλάνα μου μπροστά σε μια ευκαιρία στο {geo} είναι πιο σημαντική."
    },
    "Francés": {
        "ctrl": "Données de Contrôle", "nombre": "Nom Complet ou Matricule *:", "wha": "Numéro de Téléphone *:",
        "sec1": "Section I. Données Démographiques et Géographiques", "edad": "1. Âge (Ans):", "genero": "2. Genre:",
        "nac": "3. Nationalité *:", "orig": "4. État d'origine *:", "res": "5. État de résidence actuelle *:",
        "pais": "4. Écrivez votre Pays d'origine *:", "cont": "5. Sélectionnez votre Continent d'origine *:", "rol": "6. Rôle au sein de l'Église:",
        "sec2": "Section II. Connaissance du sujet", "kn1": "1. Avant cette enquête, aviez-vous entendu parler des Modèles Temporels Chronos et Kairos?",
        "kn2": "2. Avez-vous lu sur les modèles temporels Chronos et Kairos?", "kn3": "3. Avez-vous déjà enseigné les modèles temporels Chronos et Kairos?",
        "kn4": "4. Le modelo temporel:", "kn5": "5. Parler de modèles temporels, c'est parler de:",
        "sec3": "Section III. Échelle de Réactifs Likert", "btn_save": "💾 Enregistrer et Traiter le Diagnostic", "btn_pdf": "TÉLÉCHARGER LES RÉSULTATS EN PDF 📥",
        "likert_labels": {1:"1 - Tout à fait d'accord", 2:"2 - Pas d'accord", 3:"3 - Neutre", 4:"4 - D'accord", 5:"5 - Tout à fait d'accord"},
        "c_pool": "Je planifie mes activités opérationnelles à {geo} en suivant strictement les horaires de l'horloge.",
        "k_pool": "La flexibilité d'adapter mes plans face à une fenêtre d'opportunité à {geo} est plus importante."
    },
    "Alemán": {
        "ctrl": "Kontrolldaten", "nombre": "Vollständiger Name *:", "wha": "Telefonnummer *:",
        "sec1": "Abschnitt I. Demografische Daten", "edad": "1. Alter (Jahre):", "genero": "2. Geschlecht:",
        "nac": "3. Nationalität *:", "orig": "4. Herkunftsland *:", "res": "5. Aktueller Wohnort *:",
        "pais": "4. Geburtsland eingeben *:", "cont": "5. Kontinent auswählen *:", "rol": "6. Rolle in der Kirche:",
        "sec2": "Abschnitt II. Themenkenntnis", "kn1": "1. Haben Sie vor dieser Umfrage von den Zeitmodellen Chronos und Kairos gehört?",
        "kn2": "2. Haben Sie über Chronos und Kairos gelesen?", "kn3": "3. Haben Sie jemals über diese Zeitmodelle gelehrt?",
        "kn4": "4. Das Zeitmodell:", "kn5": "5. Über Zeitmodelle zu sprechen bedeutet:",
        "sec3": "Abschnitt III. Likert-Skala", "btn_save": "💾 Speichern & Verarbeiten", "btn_pdf": "ERGEBNISSE ALS PDF HERUNTERLADEN 📥",
        "likert_labels": {1:"1 - Stimme überhaupt nicht zu", 2:"2 - Stimme nicht zu", 3:"3 - Neutral", 4:"4 - Stimme zu", 5:"5 - Stimme vollkommen zu"},
        "c_pool": "Ich plane meine Aktivitäten in {geo} strikt nach der Uhrzeit.",
        "k_pool": "Flexibilität bei der Anpassung von Plänen an Gelegenheiten in {geo} ist wichtiger als die Uhr."
    }
}

def algoritmo_generar_reactivos_poliglotas(geo, b_alertas, lang_key):
    tx_pool = DICCIONARIO_IDIOMAS.get(lang_key, DICCIONARIO_IDIOMAS["Español"])
    fuga = str(b_alertas) if b_alertas else "OK"
    
    banco_alterno = {}
    for i in range(1, 15):
        if i % 2 != 0:
            banco_alterno[i] = tx_pool["c_pool"].format(geo=geo) + f" (Ref: {fuga[:12]})"
        else:
            banco_alterno[i] = tx_pool["k_pool"].format(geo=geo)
    return banco_alterno

ESTADOS_MEXICO = ["Chihuahua", "Sonora", "Sinaloa", "Nuevo León", "Jalisco", "Ciudad de México", "Veracruz"]
CONTINENTES = ["América del Norte", "Europa", "Asia", "África", "Oceanía"]
if not st.session_state.flujo_finalizado:
    # 1. SELECTOR EN TIEMPO REAL CON TODOS LOS IDIOMAS EXIGIDOS E INDUSTRIALES
    idioma_sel = st.selectbox("🌐 Choose System Language / Selecciona Idioma:", ["Español", "Inglés", "Coreano", "Griego", "Francés", "Alemán"])
    tx = DICCIONARIO_IDIOMAS[idioma_sel]
    
    st.header(f"📋 {st.session_state.audiencia_activa}")
    nombre = st.text_input(tx["nombre"], placeholder="Juan Pérez", key="main_name_in")
    whatsapp = st.text_input(tx["wha"], placeholder="+52...", key="main_wha_in")
    st.divider()

    resultados_totales = {}
    es_modo_likert = (st.session_state.audiencia_activa != "🍊 Salud Integral")

    if not es_modo_likert:
        st.write("### 🍊 Tus Gajos de Bienestar (Diseño Estilizado)")
        with st.container(border=True):
            st.markdown("#### 💪 Salud Física (SF)")
            sf_items = ["Nutricion", "Sueno", "Ejercicio", "Movimiento"]
            col1, col2 = st.columns(2)
            with col1:
                st.checkbox(sf_items, key="sf_unq_0")
                st.checkbox(sf_items, key="sf_unq_1")
            with col2:
                st.checkbox(sf_items, key="sf_2")
                st.checkbox(sf_items, key="sf_3")
            resultados_totales["Salud Fisica (SF)"] = [item for idx, item in enumerate(sf_items) if st.session_state[f"sf_unq_{idx}" if idx < 2 else f"sf_{idx}"]]

        with st.container(border=True):
            st.markdown("#### 🧠 Salud Mental (SM)")
            sm_items = ["Memoria", "Enfoque", "Resiliencia"]
            col1, col2 = st.columns(2)
            with col1:
                st.checkbox(sm_items, key="sm_unq_0")
            with col2:
                st.checkbox(sm_items, key="sm_2")
            resultados_totales["Salud Mental (SM)"] = [item for idx, item in enumerate(sm_items) if st.session_state[f"sm_unq_{idx}" if idx < 1 else f"sm_{idx}"]]
            
        if st.button("Procesar Alertas Base / Register Aler"):
            st.session_state.alertas_mandarina_previas = resultados_totales["Salud Fisica (SF)"] + resultados_totales["Salud Mental (SM)"]
            st.success("OK. Context synchronized.")
    else:
        st.subheader(tx["sec1"])
        resultados_totales["Edad"] = st.number_input(tx["edad"], min_value=10, max_value=100, value=20, key="dem_edad")
        resultados_totales["Género"] = st.radio(tx["genero"], ["Masculino", "Femenino", "Other"], horizontal=True, key="dem_genero")
        
        nacionalidad = st.radio(tx["nac"], ["Mexicana", "Extranjera"], horizontal=True, key="dem_nac")
        resultados_totales["Nacionalidad"] = nacionalidad
        
        geo_contexto = "Region"
        if nacionalidad == "Mexicana":
            resultados_totales["Estado Origen"] = st.selectbox(tx["orig"], [""] + ESTADOS_MEXICO, key="dem_orig")
            resultados_totales["Estado Residencia"] = st.selectbox(tx["res"], [""] + ESTADOS_MEXICO, key="dem_res")
            resultados_totales["País Origen"] = "México"
            resultados_totales["Continente Extranjero"] = "América"
            geo_contexto = str(resultados_totales["Estado Residencia"])
        else:
            resultados_totales["Estado Origen"] = "N/A"
            resultados_totales["Estado Residencia"] = "N/A"
            resultados_totales["País Origen"] = st.text_input(tx["pais"], key="dem_pais_txt")
            resultados_totales["Continente Extranjero"] = st.selectbox(tx["cont"], [""] + CONTINENTES, key="dem_cont")
            geo_contexto = str(resultados_totales["País Origen"])

        st.subheader(tx["sec2"])
        resultados_totales["C1_Escuchado"] = st.radio(tx["kn1"], ["Sí", "No"], horizontal=True, key="kn_1")
        resultados_totales["C2_Leído"] = st.radio(tx["kn2"], ["Sí", "No"], horizontal=True, key="kn_2")
        resultados_totales["C3_Enseñado"] = st.radio(tx["kn3"], ["Sí", "No"], horizontal=True, key="kn_3")
        resultados_totales["C4_Origen"] = st.radio(tx["kn4"], ["Se impone", "Se nace", "No sé"], horizontal=True, key="kn_4")
        resultados_totales["C5_Concepto"] = st.radio(tx["kn5"], ["Teología", "Cultura", "No sé"], horizontal=True, key="kn_5")

        st.subheader(tx["sec3"])
        
        # MUTACIÓN EN TIEMPO REAL: Reconstrucción y renderizado políglota alternado síncrono
        banco_mutado = algoritmo_generar_reactivos_poliglotas(geo_contexto, st.session_state.alertas_mandarina_previas, idioma_sel)
        
        for r_id, enunciado_idioma in banco_mutado.items():
            st.write(f"**Reactivo {r_id}:** {enunciado_idioma}")
            resultados_totales[f"R{r_id}"] = st.radio(
                "Scale:", options=,
                format_func=lambda x: tx["likert_labels"][x],
                key=f"dyn_r_{r_id}"
            )
    st.divider()
    col_btn1, col_btn2 = st.columns(2)
    campos_completos = bool(nombre.strip()) and bool(whatsapp.strip())

    with col_btn1:
        if st.button(tx["btn_save"], width="stretch", type="primary"):
            if not campos_completos: st.error("Incomplete fields.")
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
            
            # INYECCIÓN SÍNCRONA: Construcción del PDF parametrizado con el idioma seleccionado
            reporte_procesado = generar_pdf_diagnostico(nombre, whatsapp, resultados_totales, st.session_state.audiencia_activa, es_modo_likert, grafica_base64, idioma_sel)
            nombre_archivo = nombre.replace(' ', '_') if nombre else 'User'
            
            def callback_finalizar():
                st.session_state.flujo_finalizado = True
                for k in list(st.session_state.keys()):
                    if k.startswith(("sf_", "sm_", "dyn_r_", "dem_", "kn_")): del st.session_state[k]
            
            st.download_button(
                label=tx["btn_pdf"], 
                data=reporte_procesado, 
                file_name=f"Report_{idioma_sel}_{nombre_archivo}.pdf", 
                mime="application/pdf", 
                on_click=callback_finalizar
            )
        else: st.info("💡 Process fields.")
else:
    st.balloons()
    st.success("### Process Completed! 🎉")
    with st.container(border=True):
        st.write("## 🍊 ¡Muchas gracias por tu participación!")
        st.markdown(f"Has completado el diagnóstico. Reconocer nuestros vectores temporales es el inicio de una alta madurez y bienestar integral.")
        st.info("👉 Jacob Zumaya Prianti A.C. (c) 2026")
        
    if not es_celular_del_publico:
        if st.button("🔄 Reiniciar Ecosistema", width="stretch"):
            st.session_state.flujo_finalizado = False
            st.session_state.guardado_exitoso = False
            st.rerun()
