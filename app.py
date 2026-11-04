# =================================================================
# ENTORNO BILINGÜE INMUNE: CENTRO DE MANDO ESTÁTICO (ESPAÑOL / INGLÉS)
# =================================================================
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time
import hashlib
import base64
import gspread
import qrcode 
import html
import urllib.parse
import matplotlib.pyplot as plt
from io import BytesIO
from fpdf import FPDF

# Configuración estructural de la página web en producción
st.set_page_config(
    page_title="Informe Psicometrico - Modelos Temporales y Salud Integral",
    page_icon="🍊",
    layout="wide"
)

# Inyección de estilos CSS síncronos formato APA
st.markdown(
    """<style>
    .st_radio label, div[data-testid="stMarkdownContainer"] p, .stCheckbox label { white-space: normal !important; word-break: break-word !important; overflow-wrap: break-word !important; }
    div[row-data-id="stRadioHorizontal"] { flex-wrap: wrap !important; gap: 12px !important; }
    div[data-testid="stDataFrame"] table { border-top: 2px solid #333 !important; border-bottom: 2px solid #333 !important; }
    div[data-testid="stDataFrame"] th { border-bottom: 1px solid #333 !important; background-color: #fff !important; font-weight: bold !important; }
    </style>""", 
    unsafe_allow_html=True
)

# =================================================================
# 🎛️ CENTRO DE MANDO BILINGÜE (EL CONTROL TOTAL SIN APIS EXTERNAS)
# =================================================================
CENTRO_MANDO_BILINGUE = {
    "es": {
        "intl_title": "🌐 Internationalization Gateway / Control Políglota",
        "intl_select": "Selecciona tu Idioma Objetivo / Select Language:",
        "intl_btn": "🔄 APLICAR IDIOMA SELECCIONADO / APPLY LANGUAGE",
        "nombre": "Nombre Completo / Participant Name:",
        "wha": "WhatsApp o Celular (Con lada, ej. +52):",
        "err_fields": "🚨 Por favor, rellena todos los campos obligatorios.",
        "fields_msg": "💡 Introduce Nombre y WhatsApp para habilitar la descarga.",
        "btn_save": "💾 Guardar Diagnóstico y Procesar",
        "btn_pdf": "DESCARGAR EN PDF 📥",
        "thanks": "¡Diagnóstico Completado con Éxito! 🎉",
        "thanks_sub": "Hemos compilado tu reporte individual multilingüe. Descárgalo abajo.",
        "toast_msg": "Descarga del reporte disponible en el panel inferior.",
        "mand_title": "### 🍊 Diagnóstico de Salud Adaptativo - Enfoque Ontológico",
        "mand_subtitle": "Selecciona los vectores sintomatológicos detectados de forma automatizada para tu perfil:",
        "qr_title": "📢 Proyección del Código QR para el Auditorio",
        "qr_sub1": "Escanea este código con tu smartphone para acceder al formulario en tiempo real.",
        "sec1": "Sección I. Contexto Demográfico y Geográfico",
        "sec2": "Sección II. Evaluación de Nivel de Conocimiento del Modelo",
        "edad": "Edad / Age:", "genero": "Género / Gender:", "nac": "Nacionalidad / Nationality:",
        "res": "Estado de Residencia / State of Residence:", "pais": "País de Origen / Country of Origin:",
        "part": "Participante:", "cont_label": "Contacto/WhatsApp:", "fecha": "Fecha de Emisión:",
        "lbl_descriptivos": "Resultados Descriptivos de Vectores Colectivos",
        "lbl_medias_pdf": "Media Vector Cronos: {avg_c:.2f} | Media Vector Kairos: {avg_k:.2f}",
        "lbl_nota_pdf": "Reporte de Evaluacion Psicometrica Individual",
        "side_title": "## 🔐 Control del Ponente", "side_pwd": "Contraseña Ponente:", "side_btn": "Desbloquear Tableros",
        "side_success": "Modo Ponente Activo", "side_add": "➕ Crear Nueva Audiencia Generativa (AI):",
        "side_select_aud": "Audiencia en Vivo (Foco Actual):", "side_close": "🚪 Cerrar Centro de Control", "side_pwd_err": "Contraseña incorrecta.",
        "lbl_titulo_aud": "🔬 Oficina de Investigación y Alta Analítica del Ponente", "lbl_tabla_select": "Seleccionar Tabla para Extracción Histórica:",
        "lbl_crm_buscar": "🔍 Buscador Exclusivo de Participantes", "lbl_crm_input": "📝 Filtrar por Nombre o WhatsApp:",
        "lbl_btn_auditoria": "📊 Ejecutar Auditoría Macro-Estadística de Nivel Doctoral", "lbl_pdf_dictamen": "DICTAMEN MACRO-ESTADISTICO E INFORME PSICOMETRICO",
        "lbl_pdf_ref_title": "Referencias Bibliográficas (APA Format)", "lbl_btn_download_macro": "📥 DESCARGAR INFORME DOCTORAL", "lbl_btn_download_diploma": "🏆 DESCARGAR RECONOCIMIENTO HONORÍFICO",
        "kn1": "1. ¿Has escuchado hablar del modelo temporal Cronos y Kairós?", "kn2": "2. ¿Has leído algún libro o artículo científico sobre estos constructos?",
        "kn3": "3. ¿Te han enseñado formalmente a gestionar tus metas bajo este enfoque?", "kn4": "4. El modelo temporal dominante en tu entorno:", "kn5": "5. Hablar de modelos temporales es hablar de:",
        "kn4_opt0": "Se impone", "kn4_opt1": "Se hereda", "kn4_opt2": "No sé", "kn5_opt0": "Teología", "kn5_opt1": "Cultura", "kn5_opt2": "No sé",
        "likert_1": "1 - Totalmente en Desacuerdo", "likert_2": "2 - En Desacuerdo", "likert_3": "3 - Neutral", "likert_4": "4 - De Acuerdo", "likert_5": "5 - Totalmente de Acuerdo"
    },
    "en": {
        "intl_title": "🌐 Internationalization Gateway / Polyglot Control",
        "intl_select": "Select tu Idioma Objetivo / Select Language:",
        "intl_btn": "🔄 APLICAR IDIOMA SELECCIONADO / APPLY LANGUAGE",
        "nombre": "Full Name / Nombre Completo:",
        "wha": "WhatsApp or Cellphone (With country code, e.g. +1):",
        "err_fields": "🚨 Please, fill in all required fields.",
        "fields_msg": "💡 Enter Name and WhatsApp to enable the download resource.",
        "btn_save": "💾 Save Diagnosis and Process Data",
        "btn_pdf": "DOWNLOAD PDF REPORT 📥",
        "thanks": "Diagnosis Successfully Completed! 🎉",
        "thanks_sub": "We have compiled your individual multilingual report. Download it below.",
        "toast_msg": "Report download is now available in the bottom panel.",
        "mand_title": "### 🍊 Adaptive Health Diagnosis - Ontological Approach",
        "mand_subtitle": "Select the symptomatological vectors automatically detected for your profile:",
        "qr_title": "📢 QR Code Projection for the Audience",
        "qr_sub1": "Scan this code with your smartphone to access the form in real time.",
        "sec1": "Section I. Demographic and Geographic Context",
        "sec2": "Section II. Evaluation of Level of Knowledge of the Model",
        "edad": "Age / Edad:", "genero": "Gender / Género:", "nac": "Nationality / Nacionalidad:",
        "res": "State of Residence / Estado de Residencia:", "pais": "Country of Origin / País de Origen:",
        "part": "Participant:", "cont_label": "Contact/WhatsApp:", "fecha": "Date of Issuance:",
        "lbl_descriptivos": "Descriptive Results of Collective Vectors",
        "lbl_medias_pdf": "Cronos Vector Mean: {avg_c:.2f} | Kairos Vector Mean: {avg_k:.2f}",
        "lbl_nota_pdf": "Individual Psychometric Evaluation Report",
        "side_title": "## 🔐 Speaker Control Panel", "side_pwd": "Speaker Password:", "side_btn": "Unlock Dashboards",
        "side_success": "Speaker Mode Active", "side_add": "➕ Create New Generative Audience (AI):",
        "side_select_aud": "Live Audience (Current Focus):", "side_close": "🚪 Close Control Center", "side_pwd_err": "Incorrect password.",
        "lbl_titulo_aud": "🔬 Speaker's Research and High Analytics Office", "lbl_tabla_select": "Select Table for Historical Extraction:",
        "lbl_crm_buscar": "🔍 Exclusive Participant Search Engine", "lbl_crm_input": "📝 Filter by Name or WhatsApp:",
        "lbl_btn_auditoria": "📊 Run Doctoral Level Macro-Statistical Audit", "lbl_pdf_dictamen": "MACRO-STATISTICAL DICTAMEN AND PSYCHOMETRIC REPORT",
        "lbl_pdf_ref_title": "Bibliographic References (APA Format)", "lbl_btn_download_macro": "📥 DOWNLOAD DOCTORAL REPORT", "lbl_btn_download_diploma": "🏆 DOWNLOAD HONORARY RECOGNITION",
        "kn1": "1. Have you ever heard of the Cronos and Kairos temporal model?", "kn2": "2. Have you read any book or scientific article on these constructs?",
        "kn3": "3. Have you been formally taught to manage your goals under this approach?", "kn4": "4. The dominant temporal model in your environment:", "kn5": "5. Talking about temporal models means talking about:",
        "kn4_opt0": "Is imposed", "kn4_opt1": "Is inherited", "kn4_opt2": "I don't know", "kn5_opt0": "Theology", "kn5_opt1": "Culture", "kn5_opt2": "I don't know",
        "likert_1": "1 - Strongly Disagree", "likert_2": "2 - Disagree", "likert_3": "3 - Neutral", "likert_4": "4 - Agree", "likert_5": "5 - Strongly Agree"
    }
}

# =================================================================
# PARTE 3: PASARELA NEURONAL GRATUITA Y CONFIGURACIÓN GOOGLE SHEETS
# =================================================================
@st.cache_data(show_spinner=False)
def traducir_lote_neuronal_master(lista_textos, codigo_destino):
    """ Realiza una petición por lote (Batch) utilizando la pasarela gratuita de deep-translator. """
    if not lista_textos or codigo_destino == "es":
        return lista_textos
    try:
        from deep_translator import GoogleTranslator
        lista_limpia = [str(t) for t in lista_textos if str(t).strip()]
        traductor = GoogleTranslator(source='auto', target=codigo_destino)
        return [html.unescape(str(r)) for r in traductor.translate_batch(lista_limpia)]
    except Exception as e:
        st.sidebar.error(f"Error en traducción por lote: {str(e)}")
        return lista_textos

@st.cache_data(show_spinner=False)
def ejecutar_traduccion_neuronal(texto_origen, codigo_destino):
    """ Interceptación atómica para cadenas individuales en caliente sin costo. """
    if not texto_origen or codigo_destino == "es":
        return str(texto_origen)
    try:
        from deep_translator import GoogleTranslator
        res = GoogleTranslator(source='auto', target=codigo_destino).translate(str(texto_origen))
        return html.unescape(res) if res else str(texto_origen)
    except Exception:
        return str(texto_origen)

def conectar_google_sheets(nombre_pestana):
    """ Establece conexión segura con la API de Google Sheets empleando Service Account. """
    if "gcp_service_account" not in st.secrets:
        return None
    try:
        sd = dict(st.secrets["gcp_service_account"])
        if "private_key" in sd: 
            sd["private_key"] = sd["private_key"].replace("\\n", "\n")
        sheet = gspread.service_account_from_dict(sd).open(NOMBRE_HOJA_CALCULO)
        try: 
            return sheet.worksheet(nombre_pestana)
        except gspread.exceptions.WorksheetNotFound:
            h = ["Timestamp", "Nombre", "WhatsApp", "💪 Salud Física", "🧠 Salud Mental", "❤️ Salud Emocional", "👥 Salud Social", "💰 Salud Económica", "⏳ Salud Temporal", "🙏 Salud Espiritual", "Token"] if nombre_pestana == "🍊 Salud Integral" else ["Timestamp", "Nombre", "WhatsApp", "Edad", "Género", "Nacionalidad", "Estado Origen", "Estado Residencia", "País Origen", "Continente Extranjero", "C1_Escuchado", "C2_Leído", "C3_Enseñado", "C4_Origen", "C5_Concepto"] + [f"R{i}" for i in range(1, 11)] + ["Token"]
            ws = sheet.add_worksheet(title=nombre_pestana, rows="1000", cols="40")
            ws.append_row(h)
            return ws
    except Exception: 
        return None

def guardar_en_google_sheets(pestana, nom, wha, res, token, es_likert):
    """ Almacena la información normalizada forzando siempre los strings en español en la base de datos """
    sheet = conectar_google_sheets(pestana)
    if not sheet: 
        return False
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if not es_likert:
        # Requisito 3: El motor lee la matriz generada nativa en ESPAÑOL y la mapea por posición absoluta
        matriz_nativa_es = motor_generativo_items_audiencia(pestana, lang_code="es")
        fila = [ts, nom, wha]
        for dim_clave in DIMENSIONES_MANDARINA_MAESTRAS:
            indices_seleccionados = res.get(dim_clave, [])
            sintomas_nativos_es = matriz_nativa_es.get(dim_clave, [])
            sintomas_reportados_es = [sintomas_nativos_es[int(idx)] for idx in indices_seleccionados if int(idx) < len(sintomas_nativos_es)]
            fila.append(", ".join(sintomas_reportados_es))
        fila.append(str(token))
    else:
        gen_es = "Masculino" if "masc" in str(res.get("Género", "")).lower() else "Femenino" if "fem" in str(res.get("Género", "")).lower() else "Otro"
        nac_es = "Mexicana" if "mex" in str(res.get("Nacionalidad", "")).lower() else "Extranjera"
        c1_es = "Sí" if "s" in str(res.get("C1_Escuchado", "")).lower() else "No"
        c2_es = "Sí" if "s" in str(res.get("C2_Leído", "")).lower() else "No"
        c3_es = "Sí" if "s" in str(res.get("C3_Enseñado", "")).lower() else "No"
        
        fila = [
            ts, nom, wha,
            str(res.get("Edad", "")), gen_es, nac_es,
            str(res.get("Estado Origen", "")), str(res.get("Estado Residencia", "")),
            str(res.get("País Origen", "México")), str(res.get("Continente Extranjero", "América")),
            c1_es, c2_es, c3_es,
            "Se impone" if "imp" in str(res.get("C4_Origen", "")).lower() else "Se hereda" if "her" in str(res.get("C4_Origen", "")).lower() else "No sé",
            "Teología" if "teol" in str(res.get("C5_Concepto", "")).lower() else "Cultura" if "cult" in str(res.get("C5_Concepto", "")).lower() else "No sé"
        ]
        for i in range(1, 11): 
            fila.append(int(res.get(f"R{i}", 3)))
        fila.append(str(token))
        
    try: 
        sheet.append_row(fila)
        return True
    except Exception: 
        return False
# =================================================================
# PARTE 4: MOTOR GENERATIVO DE EXTRACCIÓN PSICOMÉTRICA Y COMPILACIÓN PDF
# =================================================================
def limpiar_texto_pdf(texto, lang="es"):
    if not texto: return ""
    txt = ejecutar_traduccion_neuronal(CENTRO_MANDO_TEXTOS[texto], lang) if texto in CENTRO_MANDO_TEXTOS else str(texto)
    for emj in ["💪", "🧠", "❤️", "👥", "💰", "⏳", "🙏", "🏭", "🍊"]: txt = txt.replace(emj, "")
    return txt.strip()

def generar_pdf_diagnostico(nombre, whatsapp, resultados, tabla, es_likert=False, lang="es"):
    pdf = FPDF()
    pdf.core_fonts_encoding = "cp1252"
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    font_family = "Helvetica"
    
    # Sincronización con la caché del Centro de Mando
    tx_pdf = st.session_state.get("tx_traducido_cache", {}) if lang != "es" else CENTRO_MANDO_TEXTOS
    tx_dictamen = st.session_state.get("tx_dictamen_cache", {}) if lang != "es" else TEXTOS_DICTAMEN_COMPLEMENTARIOS
    
    base_title = tx_pdf.get("lbl_nota_pdf", "Reporte de Evaluacion Psicometrica Individual")
    titulo_seguro = str(base_title).encode('ascii', 'ignore').decode('ascii')
    
    pdf.set_font(font_family, "B", 14)
    pdf.cell(190, 10, titulo_seguro, new_x="LMARGIN", new_y="NEXT", align="C")
    
    pdf.set_font(font_family, "", 10)
    nombre_seguro = str(nombre).encode('ascii', 'ignore').decode('ascii') if nombre else "Anonimo"
    whatsapp_seguro = str(whatsapp).encode('ascii', 'ignore').decode('ascii') if whatsapp else "N/A"
    
    lbl_part_pdf = str(tx_pdf.get("part", "Participante:")).encode('ascii', 'ignore').decode('ascii')
    lbl_cont_pdf = str(tx_pdf.get("cont_label", "Contacto/WhatsApp:")).encode('ascii', 'ignore').decode('ascii')
    
    pdf.cell(190, 6, f"{lbl_part_pdf} {nombre_seguro} | {lbl_cont_pdf} {whatsapp_seguro}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    
    if not es_likert:
        # Generación de la matriz ontológica dinámica en el idioma seleccionado por el participante
        g_trad = motor_generativo_items_audiencia(tabla, lang_code=lang)
        
        for idx, dim_traducida_emoji in enumerate(g_trad.keys()):
            if len(resultados.get(DIMENSIONES_MANDARINA_MAESTRAS[idx], [])) > 0:
                key_segura = str(dim_traducida_emoji).encode('cp1252', 'ignore').decode('cp1252')
                for emj in ["💪", "🧠", "❤️", "👥", "💰", "⏳", "🙏"]: 
                    key_segura = key_segura.replace(emj, "")
                    
                pdf.set_font(font_family, "B", 11)
                pdf.cell(190, 6, key_segura.strip(), new_x="LMARGIN", new_y="NEXT")
                
                # Inyección descriptiva de las alertas marcadas por el usuario extraídas de la IA
                indices_marcados = resultados.get(DIMENSIONES_MANDARINA_MAESTRAS[idx], [])
                sintomas_origen_nicho = list(g_trad.values())[idx]
                sintomas_reportados = [sintomas_origen_nicho[int(i)] for i in indices_marcados if int(i) < len(sintomas_origen_nicho)]
                
                pdf.set_font(font_family, "I", 9.5)
                pdf.set_text_color(100, 100, 100)
                pdf.multi_cell(190, 4.5, str(", ".join(sintomas_reportados)).encode('cp1252', 'ignore').decode('cp1252'), new_x="LMARGIN", new_y="NEXT")
                
                # Directriz clínica de contención adaptada
                raw_glosario = GLOSARIO_CLINICO_ESTÁTICO.get(DIMENSIONES_MANDARINA_MAESTRAS[idx], "")
                glosario_seguro = str(ejecutar_traduccion_neuronal(raw_glosario, lang)).encode('cp1252', 'ignore').decode('cp1252')
                
                pdf.set_font(font_family, "", 9.5)
                pdf.set_text_color(50, 50, 50)
                pdf.multi_cell(190, 4.5, glosario_seguro.strip(), new_x="LMARGIN", new_y="NEXT")
                pdf.ln(2)
    else:
        k_v = [int(resultados.get(f"R{i}", 3)) for i in range(1, 11, 2)]
        c_v = [int(resultados.get(f"R{i}", 3)) for i in range(2, 11, 2)]
        avg_c = sum(c_v) / 5
        avg_k = sum(k_v) / 5
        
        lbl_m_pdf = tx_pdf.get("lbl_medias_pdf", "Media Vector Cronos: {avg_c:.2f} | Media Vector Kairos: {avg_k:.2f}").format(avg_c=avg_c, avg_k=avg_k)
        pdf.cell(190, 5, str(lbl_m_pdf).encode('ascii', 'ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT")
        
        pdf.ln(4)
        pdf.set_font(font_family, "B", 11)
        pdf.cell(190, 6, str(tx_dictamen.get("lbl_interpretacion", "Interpretacion")).encode('ascii', 'ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT")
        
        dif = abs(avg_c - avg_k)
        if dif <= 0.4: txt_p = tx_dictamen.get("txt_p_simbiosis")
        elif avg_k > avg_c: txt_p = tx_dictamen.get("txt_p_kairos")
        else: txt_p = tx_dictamen.get("txt_p_cronos")
            
        pdf.set_font(font_family, "", 10)
        pdf.multi_cell(190, 5, str(txt_p).encode('cp1252', 'ignore').decode('cp1252'), new_x="LMARGIN", new_y="NEXT")
        
    return bytes(pdf.output())
# =================================================================
# PARTE 5A: PROCESAMIENTO TRANSACCIONAL Y ENRUTAMIENTO GENERAL
# =================================================================
def renderizar_botones_transaccionales(nom, wha, res, es_lk, lang, tx):
    st.divider()
    c1, c2, col3 = st.columns(3)
    ok = bool(nom.strip()) and bool(wha.strip())
    with c1:
        if st.button(tx["btn_save"], type="primary", use_container_width=True):
            if not ok: st.error(tx["err_fields"])
            else:
                guardar_en_google_sheets(st.session_state.audiencia_activa, nom, wha, res, "TOKEN_10MIN", es_lk)
                st.session_state.nombre_usuario_persistente = nom
                st.session_state.whatsapp_usuario_persistente = wha
                st.session_state.resultados_usuario_persistente = res
                st.session_state.es_modo_likert_persistente = es_lk
                st.session_state.flujo_finalizado = True
                st.rerun()
    with c2:
        if ok:
            r = generar_pdf_diagnostico(nom, wha, res, st.session_state.audiencia_activa, es_lk, lang)
            st.download_button(tx["btn_pdf"], data=r, file_name="Reporte.pdf", mime="application/pdf", use_container_width=True)
        else: st.info(tx["fields_msg"])
    with col3:
        if ok:
            # 🍊 CORRECCIÓN: API Gateway oficial de WhatsApp corregido sin concatenaciones rotas
            telefono_limpio = "".join(c for c in str(wha) if c.isdigit() or c == '+')
            u_wa = f"https://whatsapp.com{urllib.parse.quote(telefono_limpio)}&text=Diagnostico+Completado"
            st.markdown(f'<a href="{u_wa}" target="_blank" style="text-decoration:none;"><div style="background-color:#25d366;color:white;padding:10px;border-radius:4px;text-align:center;font-weight:bold;cursor:pointer;">💬 WHATSAPP</div></a>', unsafe_allow_html=True)

def main():
    if "estructuras_inicializadas" not in st.session_state: st.session_state.estructuras_inicializadas = False
    if "audiences_custom_list" not in st.session_state: st.session_state.audiences_custom_list = []
    if "audiencia_activa" not in st.session_state: st.session_state.audiencia_activa = "🍊 Salud Integral"
    if "admin_autenticado" not in st.session_state: st.session_state.admin_autenticado = False
    if "flujo_finalizado" not in st.session_state: st.session_state.flujo_finalizado = False

    idioma_sel = st.query_params.get("lang", "es")
    st.session_state.idioma_activo_actual = idioma_sel

    # Hidratación optimizada en un único paquete masivo para evitar baneos de IP
    if idioma_sel != "es":
        if "tx_traducido_cache" not in st.session_state or st.session_state.get("cache_lang_check") != idioma_sel:
            llaves_m = list(CENTRO_MANDO_TEXTOS.keys())
            valores_m = list(CENTRO_MANDO_TEXTOS.values())
            llaves_d = list(TEXTOS_DICTAMEN_COMPLEMENTARIOS.keys())
            valores_d = list(TEXTOS_DICTAMEN_COMPLEMENTARIOS.values())
            llaves_g = list(GLOSARIO_CLINICO_ESTÁTICO.keys())
            valores_g = list(GLOSARIO_CLINICO_ESTÁTICO.values())
            
            super_lote_plano = valores_m + valores_d + valores_g
            super_lote_traducido = traducir_lote_neuronal_master(super_lote_plano, idioma_sel)
            
            ptr_m = len(valores_m)
            ptr_d = ptr_m + len(valores_d)
            
            valores_m_trad = super_lote_traducido[:ptr_m]
            valores_d_trad = super_lote_traducido[ptr_m:ptr_d]
            valores_g_trad = super_lote_traducido[ptr_d:]
            
            st.session_state.tx_traducido_cache = dict(zip(llaves_m, valores_m_trad))
            st.session_state.tx_dictamen_cache = dict(zip(llaves_d, valores_d_trad))
            
            gl_tr = {}
            for idx, gk in enumerate(llaves_g):
                gl_tr[gk] = {"sig": valores_g_trad[idx], "rec": ""}
                
            st.session_state.glosario_traducido_cache = gl_tr
            st.session_state.cache_lang_check = idioma_sel
            
        tx = st.session_state.tx_traducido_cache
        tx_dictamen = st.session_state.tx_dictamen_cache
    else:
        tx = {k: str(v) for k, v in CENTRO_MANDO_TEXTOS.items()}
        tx_dictamen = {k: str(v) for k, v in TEXTOS_DICTAMEN_COMPLEMENTARIOS.items()}

    # Forzamos la mutación algorítmica exacta cada 10 minutos (600 segundos)
    minuto_bloque_10 = int(time.time() // 600)
    token_tiempo = hashlib.md5(f"mandarina_secret_{minuto_bloque_10}".encode()).hexdigest()[:8]
    
    modo_admin_url = st.query_params.get("modo_admin", "true")
    es_celular_del_publico = str(modo_admin_url).strip().lower() == "false"
    
    if es_celular_del_publico and st.query_params.get("diag_tipo", None): 
        st.session_state.audiencia_activa = st.query_params.get("diag_tipo")

    # 🍊 CORRECCIÓN: Raíz limpia del dominio para inyectar correctamente los parámetros dinámicos
    URL_PRODUCCION = "https://dsimandarina.streamlit.app"
    url_con_token = f"{URL_PRODUCCION}/?token={token_tiempo}&modo_admin=false&diag_tipo={st.session_state.audiencia_activa.replace(' ', '%20')}&lang={idioma_sel}"

    if not st.session_state.estructuras_inicializadas:
        for t in ["🍊 Salud Integral", "Docentes", "🏭 Sector Secundario"]: conectar_google_sheets(t)
        st.session_state.estructuras_inicializadas = True

    with st.sidebar:
        st.markdown(tx.get("side_title", "## 🔐 Control"))
        # 🍊 CORRECCIÓN: Se cambió es_m_pub por la variable unificada correcta de este módulo
        if not es_celular_del_publico:
            if not st.session_state.admin_autenticado:
                p_in = st.text_input(tx.get("side_pwd", "Contraseña:"), type="password", key="p_sec")
                if st.button(tx.get("side_btn", "Desbloquear")):
                    if p_in == st.secrets.get("credentials", {}).get("password_ponente", "mandarina2026"): 
                        st.session_state.admin_autenticado = True
                        st.rerun()
                    else: st.error(tx.get("side_pwd_err", "Error"))
            else:
                st.success(tx.get("side_success", "Activo"))
                n_aud = st.text_input(tx.get("side_add", "Nueva Audiencia:")).strip()
                if n_aud and n_aud not in st.session_state.audiences_custom_list: 
                    st.session_state.audiences_custom_list.append(n_aud)
                    st.rerun()
                op = ["🍊 Salud Integral", "Docentes", "🏭 Sector Secundario"] + st.session_state.audiences_custom_list
                sel_aud = st.selectbox(tx.get("side_select_aud", "Audiencia:"), op, index=op.index(st.session_state.audiencia_activa) if st.session_state.audiencia_activa in op else 0, key="sb_aud_master_ponente")
                if sel_aud != st.session_state.audiencia_activa: 
                    st.session_state.audiencia_activa = sel_aud
                    st.rerun()
                if st.button(tx.get("side_close", "Cerrar")): 
                    st.session_state.admin_autenticado = False
                    st.rerun()
        else: st.markdown("<style>div[data-testid='stSidebar'] {display: none !important;}</style>", unsafe_allow_html=True)
    # =================================================================
    # PARTE 5B: ENTORNO MULTILINGÜE, CUESTIONARIOS Y GENERACIÓN DE DIPLOMAS
    # =================================================================
    # Sincronización explícita de variables y lógica de interfaz principal
    es_m_pub = es_celular_del_publico 

    if not st.session_state.flujo_finalizado:
        with st.container(border=True):
            st.markdown(f"### {tx.get('intl_title', '🌐 Control Poliglota')}")
            from deep_translator import GoogleTranslator
            try:
                dict_idiomas = GoogleTranslator().get_supported_languages(as_dict=True)
                lista_visual = [k.title() for k in dict_idiomas.keys()]
            except Exception:
                dict_idiomas = {"spanish": "es", "english": "en", "french": "fr"}
                lista_visual = ["Spanish", "English", "French"]

            sel_v = st.selectbox(tx.get("intl_select", "Selecciona Idioma:"), options=sorted(lista_visual), key="sb_public_participant_gateway_language_unique")
            if st.button(tx.get("intl_btn", "Aplicar"), key="btn_apply_lang_master_mando_fixed_core"):
                k_clean = str(sel_v).lower().strip()
                iso_f = dict_idiomas.get(k_clean, "en")
                st.query_params["lang"] = iso_f
                st.session_state.idioma_activo_actual = iso_f
                if "tx_traducido_cache" in st.session_state: del st.session_state["tx_traducido_cache"]
                st.rerun()

        # Ocultación automática: El QR SOLO se proyecta en la pantalla maestra del ponente
        if not es_m_pub:
            with st.container(border=True):
                st.markdown(f"### {tx.get('qr_title', '📢 Proyección QR')}")
                qr = qrcode.QRCode(version=1, box_size=10, border=4)
                qr.add_data(url_con_token); qr.make(fit=True)
                buf_qr = BytesIO()
                qr.make_image(fill_color="black", back_color="white").save(buf_qr, format="PNG")
                st.image(buf_qr.getvalue(), width=260, caption=tx.get('qr_sub1', 'Escanea para acceder'))

        st.header(f"📋 {st.session_state.audiencia_activa}")
        nombre = st.text_input(tx.get("nombre", "Nombre:"), key="n_in")
        whatsapp = st.text_input(tx.get("wha", "WhatsApp:"), key="w_in")
        es_likert = st.session_state.audiencia_activa != "🍊 Salud Integral"
        
        resultados_totales = {}
        if not es_likert:
            st.write(tx.get("mand_title", "### 🍊 Diagnóstico de Salud Adaptativo"))
            # 🍊 MOTOR GENERATIVO: Los ítems se autogeneran dinámicamente según la audiencia activa en la barra del ponente
            gajos = motor_generativo_items_audiencia(st.session_state.audiencia_activa, idioma_sel)
            for g_idx, (g_name, alertas_especificas) in enumerate(gajos.items()):
                with st.container(border=True):
                    st.markdown(f"#### {g_name}")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        cb0 = st.checkbox(alertas_especificas[0] if len(alertas_especificas)>0 else "S0", key=f"c_{g_idx}_0_f")
                        cb1 = st.checkbox(alertas_especificas[1] if len(alertas_especificas)>1 else "S1", key=f"c_{g_idx}_1_f")
                    with col_b:
                        cb2 = st.checkbox(alertas_especificas[2] if len(alertas_especificas)>2 else "S2", key=f"c_{g_idx}_2_f")
                        cb3 = st.checkbox(alertas_especificas[3] if len(alertas_especificas)>3 else "S3", key=f"c_{g_idx}_3_f")
                    resultados_totales[g_name] = [str(i) for i, v in enumerate([cb0, cb1, cb2, cb3]) if v]
        else:
            st.subheader(tx.get("sec1", "Sección I"))
            resultados_totales["Edad"] = st.number_input(tx.get("edad", "Edad:"), 10, 100, 20)
            resultados_totales["Género"] = st.radio(tx.get("genero", "Género:"), ["Masculino / Male", "Femenino / Female", "Otro / Other"], horizontal=True)
            resultados_totales["Nacionalidad"] = st.radio(tx.get("nac", "Nacionalidad:"), ["Mexicana", "Extranjera"], horizontal=True)
            
            if "mex" in resultados_totales["Nacionalidad"].lower():
                resultados_totales["Estado Residencia"] = st.selectbox(tx.get("res", "Residencia:"), [""] + ESTADOS_MEXICO)
                resultados_totales["País Origen"] = "México"
            else: 
                resultados_totales["País Origen"] = st.text_input(tx.get("pais", "País:"))
                
            st.subheader(tx.get("sec2", "Sección II"))
            resultados_totales["C1_Escuchado"] = st.radio(tx.get("kn1", "Q1"), ["Sí / Yes", "No"], horizontal=True)
            resultados_totales["C2_Leído"] = st.radio(tx.get("kn2", "Q2"), ["Sí / Yes", "No"], horizontal=True)
            resultados_totales["C3_Enseñado"] = st.radio(tx.get("kn3", "Q3"), ["Sí / Yes", "No"], horizontal=True)
            resultados_totales["C4_Origen"] = st.radio(tx.get("kn4", "Q4"), [tx.get("kn4_options_0", "Se impone"), tx.get("kn4_options_1", "Se hereda"), tx.get("kn4_options_2", "No sé")], horizontal=True)
            resultados_totales["C5_Concepto"] = st.radio(tx.get("kn5", "Q5"), [tx.get("kn5_options_0", "Teología"), tx.get("kn5_options_1", "Cultura"), tx.get("kn5_options_2", "No sé")], horizontal=True)
            
            st.write("### 📋 BATERÍA DE REACTIVOS C&K")
            reactivos = algoritmo_generar_reactivos_poliglotas(str(resultados_totales.get("País Origen", "Región")), idioma_sel)
            for r_id, r_txt in reactivos.items():
                st.write(f"Reactivo {r_id}: {r_txt}")
                # 🍊 CORRECCIÓN DE SINTAXIS: Se inyectó la escala numérica explícita del 1 al 5
                resultados_totales[f"R{r_id}"] = st.radio("Escala / Scale:", options=[1, 2, 3, 4, 5], format_func=lambda x: tx.get(f"likert_{x}", str(x)), horizontal=True, key=f"r_{r_id}")

        renderizar_botones_transaccionales(nombre, whatsapp, resultados_totales, es_likert, idioma_sel, tx)
    else:
        st.balloons()
        st.success(tx.get("thanks", "¡Diagnóstico Completado con Éxito! 🎉"))
        st.markdown(tx.get("thanks_sub", "Hemos compilado tu reporte individual multilingüe."))
        st.toast(tx.get("toast_msg", "Descarga lista."), icon="📥")
        
        rep = generar_pdf_diagnostico(st.session_state.get("nombre_usuario_persistente", "Participante"), st.session_state.get("whatsapp_usuario_persistente", ""), st.session_state.get("resultados_usuario_persistente", {}), st.session_state.audiencia_activa, st.session_state.get("es_modo_likert_persistente", False), idioma_sel)
        st.download_button(tx.get("btn_pdf", "📥 DESCARGAR RECORTE"), data=rep, file_name="Reporte_Psicometrico.pdf", mime="application/pdf", use_container_width=True)
        
        dip = generar_reconocimiento_honorifico_dinamico()
        st.download_button(tx.get("lbl_btn_download_diploma", "🏆 DIPLOMA"), data=dip, file_name="Diploma_Excelencia.pdf", mime="application/pdf", use_container_width=True)
        if st.button("🔄 Volver al Diagnóstico Principal", key="btn_reset_view_final_mando"): 
            st.session_state.flujo_finalizado = False; st.rerun()

    # --- INVESTIGACIÓN ALTA ANALÍTICA DEL PONENTE ---
    if st.session_state.admin_autenticado and not es_m_pub:
        st.markdown("---")
        st.header(tx.get("lbl_titulo_aud"))
        tabla_analizar = st.selectbox(tx.get("lbl_tabla_select"), ["🍊 Salud Integral", "Docentes", "🏭 Sector Secundario"], key="sb_tabla_analizar_master_office")
        sheet = conectar_google_sheets(tabla_analizar)
        todas_las_filas = sheet.get_all_values() if sheet else []
        if todas_las_filas and len(todas_las_filas) >= 2:
            df_doc = pd.DataFrame(todas_las_filas[1:], columns=todas_las_filas)
            st.subheader(tx.get("lbl_crm_buscar"))
            c_busq = st.text_input(tx.get("lbl_crm_input"), key="crm_search_input").strip().lower()
            if c_busq and not df_doc.empty:
                st.write(df_doc[df_doc[df_doc.columns].astype(str).str.lower().str.contains(c_busq)])

        if st.button(tx.get("lbl_btn_auditoria"), key="btn_run_doctoral_macro"):
            pdf_auditoria = FPDF()
            pdf_auditoria.add_page()
            pdf_auditoria.set_font("Helvetica", "B", 14)
            pdf_auditoria.cell(190, 10, str(tx.get("lbl_pdf_dictamen")).encode('ascii','ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT", align="C")
            pdf_auditoria.ln(6); pdf_auditoria.set_font("Helvetica", "B", 12)
            pdf_auditoria.cell(190, 7, str(tx.get("lbl_pdf_ref_title")).encode('ascii','ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT")
            pdf_auditoria.set_font("Helvetica", "", 9)
            for ref_key in ["lbl_ref1", "lbl_ref2", "lbl_ref3"]:
                pdf_auditoria.multi_cell(190, 4.5, str(tx_dictamen.get(ref_key)).encode('cp1252','ignore').decode('cp1252'), new_x="LMARGIN", new_y="NEXT")
                pdf_auditoria.ln(2)
            st.download_button(label=tx.get("lbl_btn_download_macro"), data=bytes(pdf_auditoria.output()), file_name="Dictamen_Doctoral.pdf", mime="application/pdf", key="btn_download_admin_macro_report_fixed_mando")

def generar_reconocimiento_honorifico_dinamico():
    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.add_page(); pdf.set_auto_page_break(auto=False)
    pdf.set_draw_color(212, 175, 55); pdf.set_line_width(1.2); pdf.rect(10, 10, 277, 190)
    pdf.set_font("Helvetica", "B", 14); pdf.set_text_color(50, 50, 50)
    pdf.cell(277, 15, "ASOCIACION CIVIL JACOB ZUMAYA PRIANTI", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(10); pdf.set_font("Times", "B", 26)
    pdf.cell(277, 14, "RECONOCIMIENTO HONORIFICO", new_x="LMARGIN", new_y="NEXT", align="C")
    return bytes(pdf.output())




# =================================================================
# INYECTOR COMPILADOR: RECONOCIMIENTO HONORÍFICO DINÁMICO (PÁGINA ÚNICA)
# =================================================================
def generar_reconocimiento_honorifico_dinamico():
    """
    Compila y exporta el Reconocimiento Honorífico Oficial en PDF.
    Automatiza la fecha real de descarga y centra la rúbrica presidencial del Dr.
    Ajustado geométricamente a una sola página A4 horizontal (Landscape).
    """
    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.core_fonts_encoding = "cp1252"
    pdf.add_page()
    
    # Desactivamos el salto de página automático para evitar desbordamientos accidentales
    pdf.set_auto_page_break(auto=False)
    
    # 1. PALETA CROMÁTICA INSTITUCIONAL (Dorado Satinado Académico)
    ORO_SATINADO = (212, 175, 55)   
    GRIS_GRAFITO = (50, 50, 50)     
    GRIS_MITAD = (100, 100, 100)    
    
    # 2. DISEÑO DEL MARCO PERIMETRAL EN DOBLE ENCUADRE
    pdf.set_draw_color(*ORO_SATINADO)
    pdf.set_line_width(1.2)
    pdf.rect(10, 10, 277, 190)
    pdf.set_line_width(0.4)
    pdf.rect(13, 13, 271, 184)
    
    # 3. CABECERA INSTITUCIONAL
    pdf.ln(15) 
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(*GRIS_GRAFITO)
    
    tit_ac = f"ASOCIACI{chr(211)}N CIVIL JACOB ZUMAYA PRIANTI"
    pdf.cell(277, 7, tit_ac, new_x="LMARGIN", new_y="NEXT", align="C")
    
    pdf.set_font("Helvetica", "I", 9.5)
    pdf.set_text_color(*GRIS_MITAD)
    sub_ac = f"Consejo Directivo de Alta Acreditaci{chr(243)}n Tecnol{chr(243)}gica y Ciencias del Comportamiento"
    pdf.cell(277, 5, sub_ac, new_x="LMARGIN", new_y="NEXT", align="C")
    
    # Línea divisoria heráldica central en dorado
    pdf.ln(4)
    pdf.set_draw_color(*ORO_SATINADO)
    pdf.set_line_width(0.6)
    pdf.line(118, pdf.get_y(), 178, pdf.get_y())
    pdf.ln(8) 
    
    # 4. DECLARACIÓN DEL LAUREADO
    pdf.set_font("Times", "I", 14)
    pdf.set_text_color(*GRIS_GRAFITO)
    pdf.cell(277, 8, "Otorga el presente", new_x="LMARGIN", new_y="NEXT", align="C")
    
    pdf.ln(2)
    pdf.set_font("Times", "B", 26)
    pdf.set_text_color(*ORO_SATINADO) 
    tit_hon = f"RECONOCIMIENTO HONOR{chr(205)}FICO"
    pdf.cell(277, 14, tit_hon, new_x="LMARGIN", new_y="NEXT", align="C")
    
    pdf.ln(3) 
    pdf.set_font("Times", "I", 14)
    pdf.set_text_color(*GRIS_GRAFITO)
    sub_laur = f"Con el grado de M{chr(225)}xima Distinci{chr(243)}n en Ciencia e Ingenier{chr(237)}a de Software al:"
    pdf.cell(277, 8, sub_laur, new_x="LMARGIN", new_y="NEXT", align="C")
    
    # 5. NOMBRE DEL GALARDONADO (DR. JACOB ZUMAYA PRIANTI)
    pdf.ln(3) 
    pdf.set_font("Times", "B", 24)
    pdf.set_text_color(*GRIS_GRAFITO)
    pdf.cell(277, 12, "Dr. Jacob Zumaya Prianti", new_x="LMARGIN", new_y="NEXT", align="C")
    
    pdf.ln(2)
    pdf.line(98, pdf.get_y(), 198, pdf.get_y())
    pdf.ln(6) 
    
    # 6. TEXTO DEL DICTAMEN DE MÉRITO (C&K + MARKOV + SVD)
    pdf.set_font("Helvetica", "", 10.5)
    pdf.set_text_color(*GRIS_GRAFITO)
    
    linea1 = f"Por el dise{chr(241)}o, fundamentaci{chr(243)}n y despliegue transaccional del ecosistema psicom{chr(233)}trico global"
    linea2 = f"Mandarina & C&K Analytics, logrando un hito de vanguardia en la integraci{chr(243)}n asim{chr(233)}trica"
    linea3 = f"de modelos temporales mediante procesos estoc{chr(225)}sticos de Markov y reducci{chr(243)}n dimensional SVD."
    linea4 = f"Su aporte eleva la precisi{chr(243)}n anal{chr(237)}tica institucional a la frontera del conocimiento cient{chr(237)}fico."
    
    pdf.cell(277, 5.5, linea1, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.cell(277, 5.5, linea2, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.cell(277, 5.5, linea3, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.cell(277, 5.5, linea4, new_x="LMARGIN", new_y="NEXT", align="C")
    
    # 7. AUTOMATIZACIÓN CRONOLÓGICA DE LA FECHA DE DESCARGA
    pdf.ln(8) 
    pdf.set_font("Helvetica", "I", 9.5)
    pdf.set_text_color(*GRIS_MITAD)
    
    meses_es = {1: "enero", 2: "febrero", 3: "marzo", 4: "abril", 5: "mayo", 6: "junio", 7: "julio", 8: "agosto", 9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"}
    fecha_hoy = datetime.date.today()
    dia_txt = str(fecha_hoy.day)
    mes_txt = meses_es.get(fecha_hoy.month, "noviembre")
    anio_txt = str(fecha_hoy.year)
    
    texto_fecha_dinamica = f"Dado en la sede oficial del Consejo Directivo a los {dia_txt} d{chr(237)}as del mes de {mes_txt} del a{chr(241)}o {anio_txt}."
    pdf.cell(277, 5, texto_fecha_dinamica, new_x="LMARGIN", new_y="NEXT", align="C")
    
    # 8. MAQUETACIÓN CENTRAL DE LA RÚBRICA PRESIDENCIAL COMPACTADA
    pdf.ln(12) 
    y_firma_central = pdf.get_y()
    
    # Línea de firma centrada de 70mm de longitud
    pdf.set_draw_color(*GRIS_MITAD)
    pdf.set_line_width(0.3)
    pdf.line(113.5, y_firma_central, 183.5, y_firma_central)
    
    # Rúbrica Presidencial Autorizada
    pdf.set_xy(113.5, y_firma_central + 2)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*GRIS_GRAFITO)
    pdf.cell(70, 4, "DR. JACOB ZUMAYA PRIANTI", align="C", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(*GRIS_MITAD)
    pdf.set_x(113.5)
    pdf.cell(70, 4, "PRESIDENTE DEL CONSEJO DIRECTIVO", align="C", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_x(113.5)
    pdf.cell(70, 4, "Jacob Zumaya Prianti A.C.", align="C")
    
    return bytes(pdf.output())

# Guardia de ejecución principal reglamentaria en el entorno de Python
if __name__ == "__main__":
    main()
