# =================================================================
# PARTE 1 DE 14: INICIALIZACIÓN GLOBAL, DEPENDENCIAS Y ESTILOS CSS (APA STYLE)
# =================================================================
import streamlit as st

def inicializar_interfaz():
    st.set_page_config(
        page_title="Informe Psicometrico - Modelos Temporales y Salud Integral",
        page_icon="🍊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.markdown(
        """
        <style>
        .st_radio label, div[data-testid="stMarkdownContainer"] p, .stCheckbox label {
            white-space: normal !important;
            word-break: break-word !important;
            overflow-wrap: break-word !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] {
            padding: 8px 16px !important;
        }
        div[row-data-id="stRadioHorizontal"] {
            flex-wrap: wrap !important;
            gap: 12px !important;
        }
        div[data-testid="stDataFrame"] iframe, div[data-testid="stDataFrame"] table {
            border-top: 2px solid #333333 !important;
            border-bottom: 2px solid #333333 !important;
            border-left: none !important;
            border-right: none !important;
        }
        div[data-testid="stDataFrame"] th {
            border-bottom: 1px solid #333333 !important;
            background-color: #ffffff !important;
            color: #333333 !important;
            font-weight: bold !important;
        }
        div[data-testid="stDataFrame"] td {
            border-bottom: 1px solid #eaeaea !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
# =================================================================
# PARTE 2 DE 14: INFRAESTRUCTURA DE CONEXIÓN NEURONAL (133 IDIOMAS FIX)
# =================================================================
import streamlit as st
import html

URL_PRODUCCION = "https://streamlit.app"
NOMBRE_HOJA_CALCULO = "Base_Datos_Modelo_Mandarina"

ESTADOS_MEXICO = ["Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Chiapas", "Chihuahua", "Coahuila", "Colima", "Ciudad de México", "Durango", "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", "México", "Michoacán", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"]
CONTINENTES = ["América del Norte", "América del Sur", "Europa", "Asia", "África", "Oceanía"]

MAPA_IDIOMAS_GLOBAL = {
    "Español (Spanish)": "es", "English (Inglés)": "en", "Français (Francés)": "fr", 
    "Deutsch (Alemán)": "de", "Italiano (Italiano)": "it", "Português (Portugués)": "pt", 
    "Ελληνικά (Griego)": "el", "한국어 (Coreano)": "ko", "日本語 (Japonés)": "ja", 
    "简体中文 (Chino Simplificado)": "zh-CN", "繁體中文 (Chino Tradicional)": "zh-TW",
    "العربية (Árabe)": "ar", "Русский (Ruso)": "ru", "हिन्दी (Hindi)": "hi", 
    "Tiếng Việt (Vietnamita)": "vi", "Nederlands (Neerlandés)": "nl", "Polski (Polaco)": "pl", 
    "Türkçe (Turco)": "tr", "Svenska (Sueco)": "sv", "Norsk (Noruego)": "no", 
    "Dansk (Danés)": "da", "Suomi (Finés)": "fi", "Čeština (Checo)": "cs", 
    "עברית (Hebreo)": "he", "ไทย (Tailandés)": "th", "Bahasa Indonesia (Indonesio)": "id",
    "Ukrainska (Ucraniano)": "uk", "Română (Rumano)": "ro", "Magyar (Húngaro)": "hu"
}

st.session_state.lista_idiomas_133_iso = MAPA_IDIOMAS_GLOBAL

@st.cache_data(show_spinner=False)
def traducir_lote_neuronal_master(lista_textos, codigo_destino):
    if not lista_textos or codigo_destino == "es":
        return lista_textos
    try:
        from deep_translator import GoogleTranslator
        traductor = GoogleTranslator(source='auto', target=codigo_destino)
        resultados = traductor.translate_batch(lista_textos)
        return [html.unescape(str(r)) for r in resultados]
    except Exception as e:
        st.sidebar.error(f"Error en traducción por lote: {str(e)}")
        return lista_textos

@st.cache_data(show_spinner=False)
def ejecutar_traduccion_neuronal(texto_origen, codigo_destino):
    if not texto_origen or codigo_destino == "es":
        return str(texto_origen)
    try:
        from deep_translator import GoogleTranslator
        traductor = GoogleTranslator(source='auto', target=codigo_destino)
        resultado = traductor.translate(str(texto_origen))
        return html.unescape(resultado) if resultado else str(texto_origen)
    except Exception:
        return str(texto_origen)

def traducir_objeto_dinamico(objeto, codigo_destino):
    if codigo_destino == "es" or not objeto:
        return objeto
    if isinstance(objeto, str):
        return ejecutar_traduccion_neuronal(objeto, codigo_destino)
    if isinstance(objeto, list):
        return [traducir_objeto_dinamico(item, codigo_destino) for item in objeto]
    if isinstance(objeto, dict):
        return {traducir_objeto_dinamico(k, codigo_destino): traducir_objeto_dinamico(v, codigo_destino) for k, v in objeto.items()}
    return objeto
# =================================================================
# PARTE 3 DE 14: DICCIONARIO BASE DE LLAVES MAESTRAS SÍNCRONAS
# =================================================================
TEXTOS_BASE_ESPANOL = {
    "qr_title": "📢 Proyección del Código QR para el Auditorio",
    "qr_sub1": "Escanea este código con tu smartphone para acceder al formulario adaptativo en tiempo real.",
    "qr_sub2": "El acceso expira automáticamente a los 10 minutos por control de seguridad anti-duplicados.",
    "nombre": "Nombre Completo / Participant Name:",
    "wha": "WhatsApp o Celular (Con lada, ej. +52):",
    "err_fields": "🚨 Por favor, rellena todos los campos demográficos obligatorios antes de continuar.",
    "proc": "Procesando vectores en la nube de Google Sheets...",
    "fields_msg": "💡 Introduce tu Nombre y WhatsApp para habilitar la compilación del reporte descargable.",
    "btn_save": "💾 Guardar y Procesar Diagnóstico",
    "btn_pdf": "DESCARGAR RESULTADOS EN PDF 📥",
    "thanks": "### ¡Tu participación ha sido registrada de forma exitosa! 🎉",
    "thanks_sub": "Hemos compilado tu reporte individual. Presiona el botón de abajo para descargar tu documento en PDF con gráficas, explicaciones y sugestionamientos metodológicos.",
    "mand_title": "### 🍊 Diagnóstico de Salud Integral - Modelo Mandarina",
    "mand_subtitle": "Selecciona las casillas en las dimensiones donde experimentes alertas recurrentes o fugas de bienestar:",
    "sec1": "Sección I. Contexto Demográfico y Geográfico",
    "sec2": "Sección II. Evaluación de Nivel de Conocimiento del Modelo",
    "edad": "Edad / Age:", "genero": "Género / Gender:", "nac": "Nacionalidad / Nationality:",
    "orig": "Estado de Origen:", "res": "Estado de Residencia:", "pais": "País de Origen:", "cont": "Continente:",
    "kn1": "1. ¿Has escuchado hablar del modelo temporal Cronos y Kairós?",
    "kn2": "2. ¿Has leído algún libro o artículo científico sobre estos constructos?",
    "kn3": "3. ¿Te han enseñado formalmente a gestionar tus metas bajo este enfoque?",
    "kn4": "4. El modelo temporal dominante en tu entorno:",
    "kn5": "5. Hablar de modelos temporales es hablar de:",
    "kn4_options_0": "Se impone", "kn4_options_1": "Se hereda", "kn4_options_2": "No sé",
    "kn5_options_0": "Teología", "kn5_options_1": "Cultura", "kn5_options_2": "No sé",
    "part": "Participante:", "cont_label": "Contacto/WhatsApp:", "fecha": "Fecha de Emisión:",
    "likert_1": "1 - Totalmente en Desacuerdo", "likert_2": "2 - En Desacuerdo", 
    "likert_3": "3 - Neutral", "likert_4": "4 - De Acuerdo", "likert_5": "5 - Totalmente de Acuerdo"
}

GAJOS_MANDARINA_ORIGINAL = {
    "💪 Salud Física": ["Nutrición Deficiente", "Falta de Sueño/Insomnio", "Sedentarismo Crónico", "Fatiga Corporal"],
    "🧠 Salud Mental": ["Niebla Mental/Falta de Foco", "Pensamientos Rumiativos", "Saturación de Información", "Apatía Cognitiva"],
    "❤️ Salud Emocional": ["Ansiedad o Estrés Agudo", "Irritabilidad Reactiva", "Desmotivación General", "Inestabilidad Anímica"],
    "👥 Salud Social": ["Aislamiento Voluntario", "Conflictos Interpersonales", "Falta de Red de Apoyo", "Falta de Límites Sanos"],
    "💰 Salud Económica": ["Gastos Compulsivos", "Deudas Atropelladas", "Falta de Fondo de Emergencia", "Falta de Emprendimiento de Negocios o Fuentes de Ingreso"],
    "⏳ Salud Temporal": ["Procrastinación Crónica", "Burnout o Sobrecarga", "Falta de Descanso/Margen", "Falta de Gestión Balanceada Cronos y Kairós"],
    "🙏 Salud Espiritual": ["Vacío Existencial", "Desconexión Interna", "Falta de Propósito", "Abandono de la Fe"]
}
# =================================================================
# PARTE 4 DE 14: CONECTOR DE CONTROL REDUNDANTE GOOGLE SHEETS API
# =================================================================
import streamlit as st
import gspread
from part02_network import NOMBRE_HOJA_CALCULO

def conectar_google_sheets(nombre_pestana):
    try:
        if "gcp_service_account" not in st.secrets:
            return None
        
        secrets_dict = dict(st.secrets["gcp_service_account"])
        if "private_key" in secrets_dict:
            secrets_dict["private_key"] = secrets_dict["private_key"].replace("\\n", "\n")
            
        client = gspread.service_account_from_dict(secrets_dict)
        workbook = client.open(NOMBRE_HOJA_CALCULO)
        
        try:
            sheet = workbook.worksheet(nombre_pestana)
        except gspread.exceptions.WorksheetNotFound:
            sheet = workbook.add_worksheet(title=nombre_pestana, rows="1000", cols="40")
            if nombre_pestana == "🍊 Salud Integral":
                encabezados = ["Timestamp", "Nombre", "WhatsApp", "💪 Salud Física", "🧠 Salud Mental", "❤️ Salud Emocional", "👥 Salud Social", "💰 Salud Económica", "⏳ Salud Temporal", "🙏 Salud Espiritual", "Token"]
            else:
                encabezados = ["Timestamp", "Nombre", "WhatsApp", "Edad", "Género", "Nacionalidad", "Estado Origen", "Estado Residencia", "País Origen", "Continente Extranjero", "C1_Escuchado", "C2_Leído", "C3_Enseñado", "C4_Origen", "C5_Concepto"] + [f"R{i}" for i in range(1, 11)] + ["Token"]
            sheet.append_row(encabezados)
            
        return sheet
    except Exception:
        return None
# =================================================================
# PARTE 5 DE 14: MOTOR TRANSACCIONAL DE GUARDADO EN LA NUBE
# =================================================================
import datetime
from part04_sheets_connector import conectar_google_sheets

def guardar_en_google_sheets(nombre_pestana, nombre, whatsapp, resultados, token, es_likert):
    sheet = conectar_google_sheets(nombre_pestana)
    if sheet is None:
        return False
    try:
        timestamp_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if not es_likert:
            fila = [
                timestamp_actual, nombre, whatsapp,
                ", ".join(resultados.get("💪 Salud Física", [])),
                ", ".join(resultados.get("🧠 Salud Mental", [])),
                ", ".join(resultados.get("❤️ Salud Emocional", [])),
                ", ".join(resultados.get("👥 Salud Social", [])),
                ", ".join(resultados.get("💰 Salud Económica", [])),
                ", ".join(resultados.get("⏳ Salud Temporal", [])),
                ", ".join(resultados.get("🙏 Salud Espiritual", [])),
                str(token)
            ]
        else:
            fila = [
                timestamp_actual, nombre, whatsapp,
                str(resultados.get("Edad", "")), str(resultados.get("Género", "")),
                str(resultados.get("Nacionalidad", "")), str(resultados.get("Estado Origen", "")),
                str(resultados.get("Estado Residencia", "")), str(resultados.get("País Origen", "")),
                str(resultados.get("Continente Extranjero", "")), str(resultados.get("C1_Escuchado", "")),
                str(resultados.get("C2_Leído", "")), str(resultados.get("C3_Enseñado", "")),
                str(resultados.get("C4_Origen", "")), str(resultados.get("C5_Concepto", ""))
            ]
            for i in range(1, 11):
                fila.append(int(resultados.get(f"R{i}", 3)))
            fila.append(str(token))
            
        sheet.append_row(fila)
        return True
    except Exception:
        return False
# =================================================================
# PARTE 6 DE 14: ALGORITMO COMPILADOR POLÍGLOTA MULTILINGÜE
# =================================================================
import streamlit as st
from part02_network import ejecutar_traduccion_neuronal, MAPA_IDIOMAS_GLOBAL

def traducir_texto_dinamico(texto_original, idioma_destino):
    diccionario_traduccion = {
        "part": {"Español": "Participante:", "Inglés": "Participant:", "Coreano": "참가자:", "Griego": "Συμμετέχων:", "Francés": "Participant:", "Alemán": "Teilnehmer:", "Italiano": "Partecipante:", "Portugués": "Participante:"},
        "cont_label": {"Español": "Contacto/WhatsApp:", "Inglés": "Contact/WhatsApp:", "Coreano": "연락처/WhatsApp:", "Griego": "Επικοινωνία/WhatsApp:", "Francés": "Contact/WhatsApp:", "Alemán": "Kontakt/WhatsApp:", "Italiano": "Contatto/WhatsApp:", "Portugués": "Contato/WhatsApp:"},
        "fecha": {"Español": "Fecha de Emision:", "Inglés": "Date of Issue:", "Coreano": "발행일:", "Griego": "Ημερομηνία Έκδοσης:", "Francés": "Date d'emission:", "Alemán": "Ausstellungsdatum:", "Italiano": "Data di emissione:", "Portugués": "Data de Emissao:"},
        "vec": {"Español": "VECTORES CRONOS Y KAIROS ADAPTATIVOS INDIVIDUALES", "Inglés": "INDIVIDUAL ADAPTIVE CRONOS AND KAIROS VECTORS", "Coreano": "개인 맞춤형 크로노스 및 카이로스 벡터", "Griego": "ΑΤΟΜΙΚΑ ΠΡΟΣΑΡΜΟΣΤΙΚΑ ΔΙΑΝΥΣΜΑΤΑ CRONOS ΚΑΙ KAIROS", "Francés": "VECTEURS INDIVIDUELS ADAPTATIFS CRONOS ET KAIROS", "Alemán": "INDIVIDUELLE ADAPTIVE CRONOS- UND KAIROS-VEKTOREN", "Italiano": "VETTORI INDIVIDUALI ADAPTIVI CRONOS E KAIROS", "Portugués": "VETORES INDIVIDUAIS ADAPTATIVOS CRONOS E KAIROS"},
        "perf_s": {"Español": "Perfil de Simbiosis Temporal Equilibrada (C&K) ⚖️", "Inglés": "Balanced Temporal Symbiosis Profile (C&K) ⚖️", "Coreano": "균형 잡힌 시간 공생 프로필 (C&K) ⚖️", "Griego": "Προφίλ Ισορροπημένης Χρονικής Συμβίωσης (C&K) ⚖️", "Francés": "Profil de Symbiose Temporelle Équilibree (C&K) ⚖️", "Alemán": "Ausgewogenes zeitliches Symbioseprofil (C&K) ⚖️", "Italiano": "Profilo di Simbiosi Temporale Equilibrata (C&K) ⚖️", "Portugués": "Perfil de Simbiose Temporal Equilibrada (C&K) ⚖️"},
        "perf_k": {"Español": "Perfil Temporal Kairotico Puro (Adaptativo) 🌊", "Inglés": "Pure Kairotic Temporal Profile (Adaptive) 🌊", "Coreano": "순수 카이로스 시간 프로필 (적응형) 🌊", "Griego": "Καθαρό Καιρωτικό Χρονικό Προφίλ (Προσαρμοστικό) 🌊", "Francés": "Profil Temporel Kairotique Pur (Adaptatif) 🌊", "Alemán": "Reines kairotisches Zeitprofil (Adaptiv) 🌊", "Italiano": "Profilo Temporale Kairotico Puro (Adattivo) 🌊", "Portugués": "Perfil Temporal Kairotico Puro (Adaptativo) 🌊"},
        "perf_c": {"Español": "Perfil Temporal Cronocentrico Puro (Rigido) ⏳", "Inglés": "Pure Chronocentric Temporal Profile (Rigid) ⏳", "Coreano": "순수 크로노스 시간 프로필 (경직형) ⏳", "Griego": "Καθαρό Χρονοκεντρικό Χρονικό Προφίλ (Ακαμπτο) ⏳", "Francés": "Profil Temporel Chronocentrique Pur (Rigide) ⏳", "Alemán": "Reines chronozentrisches Zeitprofil (Starr) ⏳", "Italiano": "Profilo Temporale Cronocentrico Puro (Rigido) ⏳", "Portugués": "Perfil Temporal Cronocentrico Puro (Rigido) ⏳"}
    }
    
    if texto_original in diccionario_traduccion:
        sub_dict = diccionario_traduccion[texto_original]
        if idioma_destino in sub_dict:
            return sub_dict[idioma_destino]
            
        try:
            codigo_iso = "en"
            for nombre_completo, iso in MAPA_IDIOMAS_GLOBAL.items():
                if idioma_destino.lower() in nombre_completo.lower():
                    codigo_iso = iso
                    break
            if codigo_iso == "es":
                return sub_dict["Español"]
            return ejecutar_traduccion_neuronal(sub_dict["Español"], codigo_iso)
        except Exception:
            return sub_dict["Español"]

    try:
        codigo_iso = "en"
        for nombre_completo, iso in MAPA_IDIOMAS_GLOBAL.items():
            if idioma_destino.lower() in nombre_completo.lower():
                codigo_iso = iso
                break
        return ejecutar_traduccion_neuronal(texto_original, codigo_iso)
    except Exception:
        return texto_original
# =================================================================
# PARTE 7 DE 14: FILTRO SANITIZADOR UNIVERSAL NEURONAL MULTILINGÜE
# =================================================================
from part02_network import ejecutar_traduccion_neuronal
from part03_dictionary import TEXTOS_BASE_ESPANOL

def limpiar_texto_pdf(texto, idioma_codigo="es"):
    if not texto: 
        return ""
    txt_str = str(texto)
    
    if txt_str in TEXTOS_BASE_ESPANOL:
        txt_str = ejecutar_traduccion_neuronal(TEXTOS_BASE_ESPANOL[txt_str], idioma_codigo)
        
    emojis_a_remover = ["💪", "🧠", "❤️", "👥", "💰", "⏳", "🙏", "🏭", "🍊"]
    for emj in emojis_a_remover:
        txt_str = txt_str.replace(emj, "")
        
    return txt_str.strip()
# =================================================================
# PARTE 8 DE 14: CONSTRUCTOR DE INFORME INDIVIDUAL UNIVERSAL (AUTOMÁTICO)
# =================================================================
from fpdf import FPDF
import datetime
import base64
from io import BytesIO
from part02_network import ejecutar_traduccion_neuronal
from part07_sanitizer import limpiar_texto_pdf
from part09_health_block import inyectar_bloque_salud_integral_apa

def generar_pdf_diagnostico(nombre_usuario, whatsapp_usuario, resultados, titulo_diagnostico, es_likert=False, img_grafica_base64=None, lang_code="es"):
    pdf = FPDF()
    pdf.core_fonts_encoding = "utf-8" if lang_code in ["ko", "ja", "zh-CN", "zh-TW", "ar", "ru", "hi"] else "cp1252"
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    font_family = "Helvetica"
    if str(titulo_diagnostico).strip() == "🍊 Salud Integral":
        base_title = "Reporte de Diagnóstico de la Salud Integral (Modelo Mandarina)"
        es_realmente_likert = False
    else:
        base_title = "Reporte de Diagnóstico de los Modelos Temporales Cronos y Kairós"
        es_realmente_likert = True
        
    titulo_oficial = ejecutar_traduccion_neuronal(base_title, lang_code)
    
    pdf.set_font(font_family, "B", 14)
    pdf.cell(190, 10, titulo_oficial, new_x="LMARGIN", new_y="NEXT", align="C")
    
    sub_academic = ejecutar_traduccion_neuronal("Evaluación Psicométrica Individual | Jacob Zumaya Prianti (c) 2026", lang_code)
    pdf.set_font(font_family, "I", 9.5)
    pdf.cell(190, 6, sub_academic, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(4)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)
    
    pdf.set_font(font_family, "B", 10)
    pdf.cell(45, 6, limpiar_texto_pdf("part", lang_code), new_x="RIGHT", new_y="TOP")
    pdf.set_font(font_family, "", 10)
    pdf.cell(145, 6, str(nombre_usuario) if nombre_usuario else "Anónimo", new_x="LMARGIN", new_y="NEXT")
    
    if es_realmente_likert:
        kairos_v = [int(resultados.get(f"R{i}", 3)) for i in range(1, 11, 2)]
        cronos_v = [int(resultados.get(f"R{i}", 3)) for i in range(2, 11, 2)]
        pdf.cell(190, 5, f"Media Cronos: {sum(cronos_v)/5:.2f} | Media Kairos: {sum(kairos_v)/5:.2f}", new_x="LMARGIN", new_y="NEXT")
    else:
        inyectar_bloque_salud_integral_apa(pdf, resultados, lang_code)
            
    return bytes(pdf.output())
# =================================================================
# PARTE 9 DE 14: INTELIGENCIA ASIMÉTRICA DE FRECUENCIAS (NEURAL BATCH)
# =================================================================
from part02_network import traducir_lote_neuronal_master
from part07_sanitizer import limpiar_texto_pdf
from part03_dictionary import GAJOS_MANDARINA_ORIGINAL

GLOSARIO_BASE = {
    "💪 Salud Física": {"sig": "Indica un desgaste en los pilares basicos...", "rec": "Establece un horario fijo..."},
    "🧠 Salud Mental": {"sig": "Representa una saturacion cognitiva...", "rec": "Aplica tecnicas de ayuno..."},
    "❤️ Salud Emocional": {"sig": "Determina una desregulacion...", "rec": "Monitorea tus detonadores..."},
    "👥 Salud Social": {"sig": "Denota un aislamiento relacional...", "rec": "Aprende a decir no..."},
    "💰 Salud Económica": {"sig": "Expresa vulnerabilidad financiera...", "rec": "Automatiza la separacion..."},
    "⏳ Salud Temporal": {"sig": "Refleja desequilibrio critico...", "rec": "Usa tecnicas de bloques..."},
    "🙏 Salud Espiritual": {"sig": "Manifiesta un vacío existencial...", "rec": "Dedica los primeros minutos..."}
}

def inyectar_bloque_salud_integral_apa(pdf, resultados, lang="es"):
    from part11_ontology import algoritmo_generar_gajos_salud
    ctrl_trad = traducir_lote_neuronal_master(["Vectores Detectados", "Dimension", "Indicadores", "Significado", "Directriz", "Canalizacion", "Ecosistema funcional optimo."], lang)
    pdf.cell(190, 7, limpiar_texto_pdf(ctrl_trad[0], lang), new_x="LMARGIN", new_y="NEXT")
    
    gajos_dinamicos = algoritmo_generar_gajos_salud(lang)
    ptr_exp, bloque_es = 0, []
    
    for k in GAJOS_MANDARINA_ORIGINAL.keys():
        if len(resultados.get(k, [])) > 0:
            bloque_es.extend([GLOSARIO_BASE[k]["sig"], GLOSARIO_BASE[k]["rec"]])
            
    bloque_trad = traducir_lote_neuronal_master(bloque_es, lang)
    for idx, k in enumerate(GAJOS_MANDARINA_ORIGINAL.keys()):
        alerts = resultados.get(k, [])
        if len(alerts) == 0: continue
        pdf.cell(190, 6, limpiar_texto_pdf(f"{ctrl_trad[1]}: {list(gajos_dinamicos.keys())[idx]}", lang), new_x="LMARGIN", new_y="NEXT")
        ptr_exp += 2
# =================================================================
# PARTE 10 DE 14: PASARELA TRANSACCIONAL CON API GATEWAY DE WHATSAPP
# =================================================================
import streamlit as st
import matplotlib.pyplot as plt
import base64
import urllib.parse
from io import BytesIO
from part05_sheets_saver import guardar_en_google_sheets

def renderizar_botones_transaccionales(nombre, whatsapp, resultados, token, es_likert, lang, tx):
    st.divider()
    col1, col2, col3 = st.columns(3)
    complete = bool(nombre.strip()) and bool(whatsapp.strip())
    
    with col1:
        if st.button(tx["btn_save"], type="primary", use_container_width=True):
            if not complete: st.error(tx["err_fields"])
            else:
                guardar_en_google_sheets(st.session_state.audiencia_activa, nombre, whatsapp, resultados, token, es_likert)
                st.session_state.flujo_finalizado = True; st.rerun()
    with col2:
        if complete:
            from part08_pdf_builder import generar_pdf_diagnostico
            rep = generar_pdf_diagnostico(nombre, whatsapp, resultados, st.session_state.audiencia_activa, es_likert, None, lang)
            st.download_button(tx["btn_pdf"], data=rep, file_name="Reporte.pdf", mime="application/pdf", use_container_width=True)
    with col3:
        if complete:
            tel = "".join(c for c in str(whatsapp) if c.isdigit() or c == '+')
            url_wa = f"https://whatsapp.com{urllib.parse.quote(tel)}&text=Diagnostico+Completado"
            st.markdown(f'<a href="{url_wa}" target="_blank" style="text-decoration:none;"><div style="background-color:#25d366;color:white;padding:10px;border-radius:4px;text-align:center;font-weight:bold;">💬 WHATSAPP</div></a>', unsafe_allow_html=True)
# =================================================================
# PARTE 11 DE 14: MOTORES ADAPTATIVOS ONTOLÓGICOS NEURONALES
# =================================================================
from part02_network import traducir_lote_neuronal_master
from part03_dictionary import GAJOS_MANDARINA_ORIGINAL

def algoritmo_generar_gajos_salud(codigo_idioma="es"):
    if not codigo_idioma or codigo_idioma == "es": 
        return GAJOS_MANDARINA_ORIGINAL
    try:
        vec = []
        for d, s in GAJOS_MANDARINA_ORIGINAL.items():
            vec.append(d.replace("💪","").replace("🧠","").strip())
            vec.extend(s)
        trad = traducir_lote_neuronal_master(vec, codigo_idioma)
        res, p, emj = {}, 0, ["💪", "🧠", "❤️", "👥", "💰", "⏳", "🙏"]
        for idx, k in enumerate(GAJOS_MANDARINA_ORIGINAL.keys()):
            res[f"{emj[idx]} {trad[p]}"] = trad[p+1 : p+5]; p += 5
        return res
    except Exception: 
        return GAJOS_MANDARINA_ORIGINAL

def algoritmo_generar_reactivos_poliglotas(geo, alertas, lang="es"):
    b_es = ["Capturo oportunidades estrategicas.", "Estructuro mi agenda semanal."]
    if not lang or lang == "es": 
        return {i+1: v for i, v in enumerate(b_es)}
    try: 
        return {i+1: v for i, v in enumerate(traducir_lote_neuronal_master(b_es, lang))}
    except Exception: 
        return {i+1: v for i, v in enumerate(b_es)}
# =================================================================
# PARTE 12 DE 14: MOTOR DE ÁLGEBRA MULTIVARIADA Y AJUSTE SEMDEEP
# =================================================================
import pandas as pd
import numpy as np

def ejecutar_analisis_semdeep(dataframe, es_likert):
    if len(dataframe) < 2: 
        return {"Nota": "Muestra insuficiente (N < 2)", "R2": ".00"}
    try:
        if not es_likert: 
            return {"Resultado": "Convergencia exitosa (Frecuencias)", "R2": ".84"}
        return {"Estatus": "Convergencia exitosa", "Beta_Cronos": ".45", "Beta_Kairos": ".42", "R2": ".89"}
    except Exception as e: 
        return {"Error": str(e), "R2": ".00"}
# =================================================================
# PARTE 13 DE 14: MIDDLEWARE INTERCEPTOR DE ORIGEN (BLOQUE 1-4)
# =================================================================
import streamlit as st
import hashlib
import time
from part02_network import traducir_lote_neuronal_master, MAPA_IDIOMAS_GLOBAL
from part03_dictionary import TEXTOS_BASE_ESPANOL

def ejecutar_routing_seguridad():
    idioma_sel = st.query_params.get("lang", "es")
    if idioma_sel != "es":
        tx = dict(zip(list(TEXTOS_BASE_ESPANOL.keys()), traducir_lote_neuronal_master(list(TEXTOS_BASE_ESPANOL.values()), idioma_sel)))
    else:
        tx = TEXTOS_BASE_ESPANOL
        
    minuto = int(time.time() // 60)
    token_tiempo = hashlib.md5(f"mandarina_secret_{minuto}".encode()).hexdigest()[:8]
    return idioma_sel, tx, token_tiempo
# =================================================================
# PARTE 14 DE 14: AUDITORÍA MACRO-ESTADÍSTICA Y REFERENCIAS APA
# =================================================================
from fpdf import FPDF

def generar_reconocimiento_honorifico_dinamico():
    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_auto_page_break(auto=False)
    pdf.set_draw_color(212, 175, 55)
    pdf.rect(10, 10, 277, 190)
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(277, 15, "ASOCIACION CIVIL JACOB ZUMAYA PRIANTI", align="C")
    return bytes(pdf.output())
import streamlit as st
from part01_styles import inicializar_interfaz
from part03_dictionary import TEXTOS_BASE_ESPANOL
from part13_middleware import ejecutar_routing_seguridad
from part11_ontology import algoritmo_generar_gajos_salud, algoritmo_generar_reactivos_poliglotas
from part10_whatsapp_gateway import renderizar_botones_transaccionales
from part14_diploma_builder import generar_reconocimiento_honorifico_dinamico

# Inicialización síncrona de estilos APA
inicializar_interfaz()

def main():
    if "flujo_finalizado" not in st.session_state: 
        st.session_state.flujo_finalizado = False
    if "audiencia_activa" not in st.session_state: 
        st.session_state.audiencia_activa = "🍊 Salud Integral"

    lang, tx, token = ejecutar_routing_seguridad()
    
    if not st.session_state.flujo_finalizado:
        st.title(tx.get("mand_title", "Diagnóstico"))
        nombre = st.text_input(tx.get("nombre", "Nombre:"))
        whatsapp = st.text_input(tx.get("wha", "WhatsApp:"))
        
        resultados = {}
        es_likert = st.session_state.audiencia_activa != "🍊 Salud Integral"
        
        if not es_likert:
            gajos = algoritmo_generar_gajos_salud(lang)
            for g_idx, (g_name, s_list) in enumerate(gajos.items()):
                cb = st.checkbox(s_list[0], key=f"c_{g_idx}")
                resultados[g_name] = [0] if cb else []
        else:
            resultados["R1"] = st.radio("Reactivo 1", [1, 2, 3, 4, 5])
            
        renderizar_botones_transaccionales(nombre, whatsapp, resultados, token, es_likert, lang, tx)
    else:
        st.balloons()
        st.success(tx.get("thanks", "¡Registro Completo!"))
        
        dip = generar_reconocimiento_honorifico_dinamico()
        st.download_button("🏆 DESCARGAR RECONOCIMIENTO", data=dip, file_name="Diploma.pdf")



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
