# =================================================================
# PARTE 1 DE 7: PROTOCOLOS DE IMPORTACIÓN Y PROTO-CONFIGURACIÓN GLOBAL
# =================================================================
import streamlit as st
import pandas as pd
import numpy as np
import base64
import time
import hashlib
import urllib.parse
from io import BytesIO
from fpdf import FPDF
import qrcode
import gspread
from google.oauth2.service_account import Credentials

# 🍊 CONFIGURACIÓN DE PÁGINA CENTRAL INMUNE A DESBORDAMIENTO
st.set_page_config(page_title="C&K Evaluation Core", page_icon="🍊", layout="wide")

URL_PRODUCCION = "https://dsimandarina.streamlit.app" 
DIMENSIONES_MANDARINA_MAESTRAS = [
    "💪 Salud Física", "🧠 Salud Mental", "❤️ Salud Emocional", 
    "👥 Salud Social", "💰 Salud Económica", "⏳ Salud Temporal", "🙏 Salud Espiritual"
]

ESTADOS_MEXICO = [
    "Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Chiapas", 
    "Chihuahua", "Ciudad de México", "Coahuila", "Colima", "Durango", "Guanajuato", 
    "Guerrero", "Hidalgo", "Jalisco", "México", "Michoacán", "Morelos", "Nayarit", 
    "Nuevo León", "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", 
    "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"
]
# =================================================================
# PARTE 2 DE 7: LÉXICO BILINGÜE METODOLÓGICO Y CENTRO DE MANDO
# =================================================================
CENTRO_MANDO_BILINGUE = {
    "es": {
        "nombre": "Escribe tu nombre completo / Full Name:",
        "wha": "Escribe tu WhatsApp internacional (con +):",
        "edad": "1. Escribe tu edad biológica:",
        "genero": "2. Selecciona tu género identitario:",
        "nac": "3. Selecciona tu marco de nacionalidad:",
        "side_title": "🔐 Panel del Ponente",
        "side_add": "Añadir Audiencia",
        "side_close": "Cerrar Panel",
        "intl_title": "🌐 Idioma del Sistema / Language",
        "intl_select": "Selecciona el idioma operativo:",
        "intl_btn": "Aplicar Idioma",
        "qr_title": "📢 Código de Acceso QR para la Audiencia",
        "qr_sub1": "Escanea para responder en tiempo real",
        "mand_title": "### 🍊 Evaluación Diagnóstica de Salud Integral",
        "likert_1": "1 - Totalmente en Desacuerdo",
        "likert_2": "2 - En Desacuerdo",
        "likert_3": "3 - Neutral / No sé",
        "likert_4": "4 - De Acuerdo",
        "likert_5": "5 - Totalmente de Acuerdo",
        "btn_save": "💾 Registrar y Finalizar Instrumento",
        "btn_pdf": "📥 Descargar Dictamen en PDF",
        "err_fields": "Por favor completa Nombre y WhatsApp obligatoriamente.",
        "fields_msg": "La descarga se habilitará al ingresar tu perfil de identificación superior.",
        "thanks": "¡Evaluación Procesada Exitosamente!",
        "thanks_sub": "Tus vectores métricos han sido calculados de forma síncrona.",
        "toast_msg": "Documentación doctoral lista para descarga.",
        "lbl_titulo_aud": "🔬 Oficina Analítica",
        "lbl_tabla_select": "Filtro de Audiencia:",
        "lbl_crm_buscar": "Motor de Búsqueda CRM",
        "lbl_crm_input": "Filtro dinámico de coincidencia:",
        "lbl_btn_auditoria": "📊 Correr Auditoría Doctora (APA)",
        "lbl_btn_download_macro": "📥 Descargar Reporte Epistemológico"
    },
    "en": {
        "nombre": "Enter your full name / Nombre completo:",
        "wha": "Enter international WhatsApp (with +):",
        "edad": "1. Enter your biological age:",
        "genero": "2. Select your gender identity:",
        "nac": "3. Select your nationality framework:",
        "side_title": "🔐 Speaker Dashboard",
        "side_add": "Add New Audience",
        "side_close": "Close Dashboard",
        "intl_title": "🌐 System Language / Idioma",
        "intl_select": "Select operative language:",
        "intl_btn": "Apply Language",
        "qr_title": "📢 Audience QR Access Code",
        "qr_sub1": "Scan to respond in real-time",
        "mand_title": "### 🍊 Comprehensive Health Diagnostic Evaluation",
        "likert_1": "1 - Strongly Disagree",
        "likert_2": "2 - Disagree",
        "likert_3": "3 - Neutral / Don't know",
        "likert_4": "4 - Agree",
        "likert_5": "5 - Strongly Agree",
        "btn_save": "💾 Register & Finalize Instrument",
        "btn_pdf": "📥 Download PDF Diagnosis",
        "err_fields": "Name and WhatsApp fields are strictly mandatory.",
        "fields_msg": "Download will unlock once identification profile is entered above.",
        "thanks": "Evaluation Processed Successfully!",
        "thanks_sub": "Your metric vectors have been calculated synchronously.",
        "toast_msg": "Doctoral documentation ready for download.",
        "lbl_titulo_aud": "🔬 Analytical Bureau",
        "lbl_tabla_select": "Audience Filter:",
        "lbl_crm_buscar": "CRM Search Engine",
        "lbl_crm_input": "Dynamic match filter:",
        "lbl_btn_auditoria": "📊 Run Doctoral Audit (APA)",
        "lbl_btn_download_macro": "📥 Download Epistemological Report"
    }
}
# =================================================================
# PARTE 3 DE 7: GLOSARIOS DE DICTAMEN EPISTEMOLÓGICO Y CITAS DOCTORALES
# =================================================================
TEXTOS_DICTAMEN_BILINGUE = {
    "es": {
        "💪 Salud Física": "Optimizar el descanso homeostático y la ergonomía postural ante la fatiga cronocéntrica aguda.",
        "🧠 Salud Mental": "Mitigar la infoxicación mediante bloques de ayuno digital y técnicas de descompresión cognitiva.",
        "❤️ Salud Emocional": "Fortalecer la autorregulación emocional y canalizar el agotamiento laboral Burnout detectado.",
        "👥 Salud Social": "Restablecer los canales relacionales directos y reconfigurar las redes de contención mutua.",
        "💰 Salud Económica": "Diseñar una matriz estratégica de contingencia para mitigar pasivos y diversificar la liquidez.",
        "⏳ Salud Temporal": "Reequilibrar las fronteras operativas del tiempo cronológico frente a la ventana de oportunidad.",
        "🙏 Salud Espiritual": "Reconectar con los hábitos devocionales basales y el propósito esencial de vida del participante.",
        "txt_p_simbiosis": "DIAGNÓSTICO: Perfil de Simbiosis Temporal Equilibrada. Logras cohabitar de forma orgánica entre la estructura del reloj (Cronos) y la captura ágil de oportunidades (Kairós).",
        "txt_p_cronos": "DIAGNÓSTICO: Perfil de Dominancia Cronos Rígida. Presentas una dependencia extrema a las agendas y listas de verificación, perdiendo flexibilidad adaptativa.",
        "txt_p_kairos": "DIAGNÓSTICO: Perfil de Dominancia Kairós Dispersa. Privilegias la improvisación y la oportunidad reactiva, descuidando el cumplimiento lineal de plazos.",
        "txt_ck_recom": "Implementar franjas de transición horaria híbridas y blindar bloques innegociables de descanso.",
        "lbl_ref1": "Hair, J. F., Black, W. C., & Anderson, R. E. (2019). Multivariate Data Analysis (8th ed.). Cengage Learning.",
        "lbl_ref2": "Schumacker, R. E., & Lomax, R. G. (2016). A Beginner's Guide to Structural Equation Modeling. Routledge.",
        "lbl_ref3": "Jacob, J. (2026). Epistemología del Tiempo Psicométrico: El Modelo Integrado Cronos y Kairós. Editorial Mandarina."
    },
    "en": {
        "💪 Salud Física": "Optimize homeostatic rest and postural ergonomics against acute chronocentric fatigue.",
        "🧠 Salud Mental": "Mitigate information overload through digital fasting blocks and cognitive decompression.",
        "❤️ Salud Emocional": "Strengthen emotional self-regulation and channel the detected Burnout exhaustion syndrome.",
        "👥 Salud Social": "Restore direct relational channels and reconfigure support networks for effective interaction.",
        "💰 Salud Económica": "Design a strategic contingency matrix to mitigate liabilities and diversify income sources.",
        "⏳ Salud Temporal": "Rebalance operational boundaries of chronological clock time versus adaptive opportunity.",
        "🙏 Salud Espiritual": "Reconnect with basal devotional habits and the essential core life purpose of the participant.",
        "txt_p_simbiosis": "DIAGNOSIS: Balanced Temporal Symbiosis Profile. You manage to cohabit organically between clock structure (Cronos) and agile opportunity capture (Kairos).",
        "txt_p_cronos": "DIAGNOSIS: Rigid Cronos Dominance Profile. You exhibit an extreme dependence on calendars and checklists, losing adaptive flexibility.",
        "txt_p_kairos": "DIAGNOSIS: Dispersed Kairos Dominance Profile. You privilege improvisation and reactive opportunity, neglecting linear deadline compliance.",
        "txt_ck_recom": "Implement hybrid hourly transition blocks and shield non-negotiable recovery slots.",
        "lbl_ref1": "Hair, J. F., Black, W. C., & Anderson, R. E. (2019). Multivariate Data Analysis (8th ed.). Cengage Learning.",
        "lbl_ref2": "Schumacker, R. E., & Lomax, R. G. (2016). A Beginner's Guide to Structural Equation Modeling. Routledge.",
        "lbl_ref3": "Jacob, J. (2026). Epistemology of Psychometric Time: The Cronos and Kairos Integrated Model. Mandarina Press."
    }
}
# =================================================================
# PARTE 4 CORREGIDA: INSERCIÓN FLEXIBLE INMUNE A RESTRICCIONES DE COLUMNAS
# =================================================================
def conectar_google_sheets(nombre_tabla):
    try:
        credenciales_dict = dict(st.secrets["gcp_service_account"])
        if "private_key" in credenciales_dict:
            credenciales_dict["private_key"] = credenciales_dict["private_key"].replace("\\n", "\n").strip()
        scope = ["https://googleapis.com", "https://googleapis.com"]
        credenciales = Credentials.from_service_account_info(credenciales_dict, scopes=scope)
        cliente = gspread.authorize(credenciales)
        id_libro = st.secrets["gcp_service_account"].get("spreadsheet_key", "1y99f_7hGv_3mUeE4K_1m49wB7r0V4oW3mDeR4_m49pQ").strip()
        return cliente.open_by_key(id_libro).worksheet(nombre_tabla)
    except Exception:
        return None

def guardar_en_google_sheets(tabla, nombre, whatsapp, resultados, token_seguridad, es_likert=False):
    """
    Registra los datos transaccionales del participante adaptando dinámicamente
    la longitud de la fila para evitar rechazos por la API de Google.
    """
    hoja = conectar_google_sheets(tabla)
    if hoja is None: 
        return False
    try:
        marca_tiempo = time.strftime("%Y-%m-%d %H:%M:%S")
        # Estructuración lineal unificada de la fila de datos para máxima persistencia
        fila = [
            marca_tiempo, nombre, whatsapp, 
            str(resultados.get("Edad", "")), 
            str(resultados.get("Género", "")), 
            str(resultados.get("Nacionalidad", ""))
        ]
        
        # Inyección síncrona de las 7 dimensiones de la Salud Integral en texto plano
        for dimension in DIMENSIONES_MANDARINA_MAESTRAS:
            fila.append(", ".join(resultados.get(dimension, [])))
            
        # Inyección indexada de las 10 respuestas de la escala Likert C&K
        for i in range(1, 11):
            fila.append(str(resultados.get(f"R{i}", "")))
            
        fila.append(token_seguridad)
        
        # Inserción limpia sin restricciones rígidas de dimensiones en la cuadrícula
        hoja.append_row(fila)
        return True
    except Exception:
        return False

def motor_generativo_items_audiencia(nombre_audiencia, lang_code="es"):
    if lang_code == "es":
        return {
            "💪 Salud Física": ["Fatiga ocupacional crónica", "Trastornos del ciclo del sueño", "Rigidez por sedentarismo", "Descuido en nutrición homeostática"],
            "🧠 Salud Mental": ["Bloqueo cognitivo extremo", "Rumiación mental prolongada", "Sobrecarga informativa/Infoxicación", "Disminución del foco analítico"],
            "❤️ Salud Emocional": ["Agotamiento emocional (Burnout)", "Irritabilidad/Reactividad interpersonal", "Desmotivación vocacional aguda", "Cuadros intermitentes de ansiedad"],
            "👥 Salud Social": ["Aislamiento relacional preventivo", "Fricciones o conflictos frecuentes", "Ausencia de redes de contención", "Dificultad para marcar límites"],
            "💰 Salud Económica": ["Estrés presupuestal agudo", "Pasivos que rebasan la liquidez", "Ausencia de fondo de contingencia", "Dependencia de una única fuente"],
            "⏳ Salud Temporal": ["Procrastinación reactiva sistémica", "Invasión horaria en tiempo libre", "Supresión de márgenes de descanso", "Desequilibrio métrico Cronos/Kairós"],
            "🙏 Salud Espiritual": ["Vacío Existencial y Vocacional", "Desconexión Interna Profunda", "Pérdida del Propósito Esencial", "Abandono de Hábitos Devocionales"]
        }
    else:
        return {
            "💪 Salud Física": ["Occupational fatigue", "Sleep cycle disorders", "Sedentary stiffness", "Nutritional neglect"],
            "🧠 Salud Mental": ["Cognitive block", "Prolonged rumination", "Information overload", "Decreased analytical focus"],
            "❤️ Salud Emocional": ["Emotional exhaustion", "Interpersonal irritability", "Acute vocational demotivation", "Intermittent anxiety"],
            "👥 Salud Social": ["Relational isolation", "Frequent conflicts", "Lack of support networks", "Difficulty setting boundaries"],
            "💰 Salud Económica": ["Acute budget stress", "Liabilities exceeding liquidity", "No contingency fund", "Single income dependence"],
            "⏳ Salud Temporal": ["Reactive procrastination", "Work invasion of free time", "Suppressed rest margins", "Cronos/Kairos imbalance"],
            "🙏 Salud Espiritual": ["Latent Existential Void", "Deep Internal Disconnection", "Loss of Essential Purpose", "Abandonment of Devotional Habits"]
        }
# =================================================================
# PARTE 5 CORREGIDA: ALGORITMO ADAPTATIVO Y GENERADOR EXPANDIDO DE PDF
# =================================================================
def algoritmo_generar_reactivos_poliglotas(datos_participante, lang="es"):
    if lang == "es":
        return {
            1: "Estructuro mis compromisos diarios basándome rigurosamente en la métrica exacta del reloj.",
            2: "Optimizo mis metas estratégicas capitalizando los momentos de máxima oportunidad operativa.",
            3: "Ejecuto mis planes de rendimiento bajo listas de verificación rígidas e inalterables.",
            4: "Experimento un flujo orgánico y natural al gestionar mis responsabilidades cotidianas.",
            5: "Castigo severamente la falta de puntualidad y la desalineación horaria en mi entorno laboral.",
            6: "Identifico los imprevistos de la jornada como ventanas estratégicas de alta utilidad analítica.",
            7: "Prefiero un orden secuencial y visual antes de comprometerme con múltiples tareas.",
            8: "Rompo mi itinerario establecido de forma inmediata si detecto una ventaja competitiva clara.",
            9: "Resguardo bloques innegociables de tiempo dedicados exclusivamente a mi descanso biológico.",
            10: "Activo una alta concentración intelectual si las condiciones de mi entorno cambian súbitamente."
        }
    else:
        return {
            1: "I structure my daily commitments based strictly on exact clock metrics.",
            2: "I optimize my strategic goals by capitalizing on moments of maximum operational opportunity.",
            3: "I execute my performance plans under rigid and unalterable checklists.",
            4: "I experience an organic and natural flow when managing my daily responsibilities.",
            5: "I strictly penalize untimeliness and schedule misalignment within my workspace.",
            6: "I read unexpected events during the day as highly useful strategic windows.",
            7: "I prefer a sequential, structured order before committing to multiple concurrent tasks.",
            8: "I break my established itinerary immediately if I detect a clear competitive advantage.",
            9: "I safeguard non-negotiable blocks of time dedicated exclusively to biological rest.",
            10: "I trigger high intellectual concentration if my environmental conditions change rapidly."
        }

def generar_pdf_diagnostico(nombre, whatsapp, resultados, tabla, es_likert=False, lang="es"):
    """
    Ensambla el reporte epistemológico completo incluyendo Salud Integral,
    perfiles computados C&K, análisis de riesgo prospectivo y sello criptográfico SHA-256.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    f_family = "Helvetica"
    
    dictamen = TEXTOS_DICTAMEN_BILINGUE.get(lang, TEXTOS_DICTAMEN_BILINGUE["es"])
    g_items = motor_generativo_items_audiencia(tabla, lang_code=lang)
    
    # 🍊 1. ENCABEZADO INSTITUCIONAL
    pdf.set_font(f_family, "B", 14)
    pdf.cell(190, 10, "DICTAMEN PSICOMETRICO DE EXCELENCIA CIENTIFICA", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(3)
    
    pdf.set_font(f_family, "", 10)
    pdf.cell(190, 6, f"Evaluado: {nombre} | WhatsApp: {whatsapp} | Modelo: {tabla}".encode('ascii','ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(f_family, "I", 9)
    pdf.cell(190, 5, f"Fecha Emision: {time.strftime('%Y-%m-%d %H:%M:%S')}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    
    # 🍊 2. DESPLIEGUE DEL INFORME DE SALUD INTEGRAL
    pdf.set_font(f_family, "B", 11)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(190, 6, "I. DIAGNOSTICO DE SALUD INTEGRAL (MANDARINA MODEL)", new_x="LMARGIN", new_y="NEXT", fill=True)
    pdf.ln(2)
    
    for dim in DIMENSIONES_MANDARINA_MAESTRAS:
        marcados = resultados.get(dim, [])
        if marcados:
            pdf.set_font(f_family, "B", 10)
            dim_limpia = dim.encode('ascii','ignore').decode('ascii').strip()
            pdf.cell(190, 5, f" Dimension: {dim_limpia}", new_x="LMARGIN", new_y="NEXT")
            
            sintomas_origen = g_items.get(dim, [])
            reportados = [sintomas_origen[int(i)] for i in marcados if str(i).isdigit() and int(i) < len(sintomas_origen)]
            
            pdf.set_font(f_family, "I", 9)
            pdf.set_text_color(150, 40, 40)
            pdf.multi_cell(190, 4.5, f"   Indicadores reportados: {', '.join(reportados)}".encode('ascii','ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT")
            
            pdf.set_font(f_family, "", 9)
            pdf.set_text_color(40, 40, 40)
            sug_base = dictamen.get(dim, "Optimizar balance.")
            pdf.multi_cell(190, 4.5, f"   Sugerencia prescriptiva: {sug_base}".encode('ascii','ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
            
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)
    
    # 🍊 3. EXPLICACIÓN Y PERFIL DE MODELOS TEMPORALES C&K
    c_v = [int(resultados.get(f"R{i}", 3)) for i in range(1, 11, 2)]
    k_v = [int(resultados.get(f"R{i}", 3)) for i in range(2, 11, 2)]
    avg_c = sum(c_v) / 5 if c_v else 3.0
    avg_k = sum(k_v) / 5 if k_v else 3.0
    
    dif = abs(avg_c - avg_k)
    if dif <= 0.4: 
        perfil_key = "txt_p_simbiosis"
    elif avg_k > avg_c: 
        perfil_key = "txt_p_kairos"
    else: 
        perfil_key = "txt_p_cronos"
        
    pdf.set_font(f_family, "B", 11)
    pdf.cell(190, 6, "II. EVALUACION DE COMPORTAMIENTO TEMPORAL CRONOS Y KAIROS", new_x="LMARGIN", new_y="NEXT", fill=True)
    pdf.ln(2)
    
    pdf.set_font(f_family, "", 10)
    pdf.cell(190, 5, f"Media Vector Cronos (Reloj): {avg_c:.2f} | Media Vector Kairos (Oportunidad): {avg_k:.2f}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)
    
    pdf.set_font(f_family, "I", 10)
    pdf.set_text_color(30, 30, 90)
    pdf.multi_cell(190, 5, f"Dictamen Operacional: {dictamen.get(perfil_key, '')}".encode('ascii','ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    
    # 🍊 4. PROSPECTIVA DE RIESGOS Y RECOMENDACIONES
    pdf.set_font(f_family, "B", 10)
    pdf.set_text_color(150, 50, 0)
    pdf.cell(190, 5, "PROSPECTIVA DE RIESGO E IMPACTO EVOLUTIVO:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(f_family, "", 9)
    pdf.set_text_color(60, 60, 60)
    
    if avg_c > avg_k:
        c1 = "- Corto Plazo: Elevacion de rigidez cognitiva, rumiacion mental y estres ante imprevistos."
        c2 = "- Mediano Plazo: Perdida de ventajas competitivas fluidas (Kairos) por apego extremo al itinerario."
        c3 = "- Largo Plazo: Obsolescencia adaptativa y colapso de la plasticidad conductual organica."
    else:
        c1 = "- Corto Plazo: Desorden horacio inmediato, desalineacion de plazos y compromisos clave."
        c2 = "- Mediano Plazo: Perdida latente de credibilidad profesional e institucional por impuntualidad."
        c3 = "- Largo Plazo: Incapacidad de consolidar macro-proyectos estables y desequilibrio existencial."
        
    pdf.multi_cell(190, 4, c1.encode('ascii','ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT")
    pdf.multi_cell(190, 4, c2.encode('ascii','ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT")
    pdf.multi_cell(190, 4, c3.encode('ascii','ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    
    pdf.set_font(f_family, "B", 10)
    pdf.set_text_color(0, 100, 0)
    pdf.cell(190, 5, "LINEAMIENTOS RECOMENDADOS DE CONTENCION METODOLOGICA:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(f_family, "", 9.5)
    pdf.set_text_color(40, 40, 40)
    pdf.multi_cell(190, 4.5, f"Prescripcion: {dictamen.get('txt_ck_recom', '')}".encode('ascii','ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    # 🍊 5. SELLO DE INVIOLABILIDAD CRIPTOGRÁFICO SHA-256
    pdf.set_font(f_family, "B", 8)
    pdf.set_text_color(120, 120, 120)
    bytes_pre = bytes(pdf.output())
    hash_cert = hashlib.sha256(bytes_pre).hexdigest().upper()
    pdf.cell(190, 4, f"SECURITY DIGITAL TRANSACTION SEAL HASH SHA-256: [{hash_cert}]", new_x="LMARGIN", new_y="NEXT", align="C")
    
    return bytes(pdf.output())

# =================================================================
# PARTE 7-A DE 7: TÍTULOS DE CONSOLA Y PERFIL DE IDENTIFICACIÓN OBLIGATORIO
# =================================================================
def main():
    if "estructuras_inicializadas" not in st.session_state: st.session_state.estructuras_inicializadas = True
    if "audiences_custom_list" not in st.session_state: st.session_state.audiences_custom_list = []
    if "audiencia_activa" not in st.session_state: st.session_state.audiencia_activa = "🍊 Salud Integral"
    if "admin_autenticado" not in st.session_state: st.session_state.admin_autenticado = False
    if "flujo_finalizado" not in st.session_state: st.session_state.flujo_finalizado = False
    if "paso_salud" not in st.session_state: st.session_state.paso_salud = False
    if "paso_cyk" not in st.session_state: st.session_state.paso_cyk = False

    iso = st.query_params.get("lang", "es")
    if iso not in ["es", "en"]: iso = "es"
    tx = CENTRO_MANDO_BILINGUE.get(iso, CENTRO_MANDO_BILINGUE["es"])

    # 💻 TÍTULO DE LA PANTALLA PRINCIPAL DE VISUALIZACIÓN ANALÍTICA Y DESCARGAS
    st.title("🏆 DIAGNÓSTICO DE LA SALUD INTEGRAL Y MODELOS TEMPORALES CRONOS Y KAIRÓS")
    st.caption("🔬 Entorno Epistemológico Multilingüe de Alta Analítica Científica y Emisión de Dictámenes")
    st.divider()

    with st.sidebar:
        st.markdown(f"### {tx.get('side_title', '🔐 Panel del Ponente')}")
        if not st.session_state.admin_autenticado:
            with st.form("bloque_autenticacion_ponente"):
                p_in = st.text_input("Contraseña Ponente:", type="password")
                if st.form_submit_button("🔓 Acceder a la Consola Master", use_container_width=True):
                    if p_in == st.secrets.get("credentials", {}).get("password_ponente", "mandarina2026"):
                        st.session_state.admin_autenticado = True
                        st.rerun()
                    else: st.error("Acceso denegado.")
        else:
            st.success("Ponente Autenticado")
            tabla_sel = st.selectbox("Base de Datos Activa:", ["🍊 Salud Integral", "Docentes", "🏭 Sector Secundario"] + st.session_state.audiences_custom_list, key="sb_an")
            st.session_state.audiencia_activa = tabla_sel
            if st.button("🔒 Cerrar Sesión Ponente", use_container_width=True):
                st.session_state.admin_autenticado = False
                st.rerun()

    if not st.session_state.flujo_finalizado:
        st.markdown(f"### {tx.get('qr_title', '📢 Código de Acceso QR')}")
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(f"{URL_PRODUCCION}?lang={iso}")
        qr.make(fit=True)
        buf_qr = BytesIO()
        qr.make_image(fill_color="black", back_color="white").save(buf_qr, format="PNG")
        st.image(buf_qr.getvalue(), width=130)
        st.divider()

        st.header(r"📋 Sección I: Perfil de identificación (Obligatorio)")
        nombre = st.text_input(tx.get("nombre", "Nombre completo:"), key=r"n_in_seq")
        whatsapp = st.text_input(tx.get("wha", "WhatsApp internacional:"), key=r"w_in_seq")
        
        if "resultados_totales_registro" not in st.session_state: st.session_state.resultados_totales_registro = {}
        resultados_totales = st.session_state.resultados_totales_registro
        
        st.subheader(r"📋 Sección II: Datos Demográficos y Geográficos (Obligatorio)")
        resultados_totales["Edad"] = int(st.number_input(tx.get("edad", "Edad biológica:"), 10, 100, 20, key=r"num_ed"))
        resultados_totales["Género"] = st.radio(tx.get("genero", "Género:"), ["Masculino / Male", "Femenino / Female", "Otro / Other"], index=None, horizontal=True, key=r"rad_g")
        resultados_totales["Nacionalidad"] = st.radio(tx.get("nac", "Nacionalidad:"), ["Mexicana", "Extranjera"], index=None, horizontal=True, key=r"rad_n")
        
        if resultados_totales.get("Nacionalidad") == "Mexicana":
            resultados_totales["Estado Origen"] = st.selectbox("Estado de origen:", [""] + ESTADOS_MEXICO, key=r"s_orig")
            resultados_totales["Estado Residencia"] = st.selectbox("Estado de residencia actual:", [""] + ESTADOS_MEXICO, key=r"s_res")
        elif resultados_totales.get("Nacionalidad") == "Extranjera":
            resultados_totales["País Origen"] = st.text_input("País de Origen:", key=r"t_pais")
            resultados_totales["Continente Extranjero"] = st.selectbox("Continente:", ["", "América", "Europa", "Asia", "África", "Oceanía"], key=r"s_cont")

        st.subheader(r"📋 Sección III: Conocimiento sobre el tema (Obligatorio)")
        preguntas_sec3 = [
            ("C1_Escuchado", "1. ¿Habías escuchado hablar sobre los Modelos Temporales Cronos y Kairós?"), 
            ("C2_Leído", "2. ¿Has leído sobre los modelos temporales Cronos y Kairós?"), 
            ("C3_Enseñado", "3. ¿Has enseñado alguna vez sobre los modelos temporales Cronos y Kairós?")
        ]
        for key_r, txt_r in preguntas_sec3: 
            resultados_totales[key_r] = st.radio(txt_r, ["Sí / Yes", "No"], index=None, horizontal=True, key=f"r_k_{key_r}")
            
        resultados_totales["C4_Origen"] = st.radio("4. El modelo temporal:", ["Se impone", "Se hereda", "No sé"], index=None, horizontal=True, key=r"r_c4")
        resultados_totales["C5_Concepto"] = st.radio("5. Hablar de modelos temporales es hablar de:", ["Teología", "Cultura", "Francamente no sé"], index=None, horizontal=True, key=r"r_c5")
        resultados_totales["C6_Perfil_Auto"] = st.radio("6. Soy persona:", ["Cronos", "Kairós", "No sé"], index=None, horizontal=True, key=r"r_c6")

        # 🔥 INTERRUPTOR 1: Verifica que las secciones I, II y III estén completamente contestadas
        vld_secciones_iniciales = all([
            bool(nombre.strip()), 
            bool(whatsapp.strip()), 
            resultados_totales.get("Género") is not None, 
            resultados_totales.get("Nacionalidad") is not None,
            resultados_totales.get("C1_Escuchado") is not None,
            resultados_totales.get("C4_Origen") is not None,
            resultados_totales.get("C5_Concepto") is not None,
            resultados_totales.get("C6_Perfil_Auto") is not None
        ])
        
        # El botón de transición solo se renderiza si se cumple la condición estricta
        if vld_secciones_iniciales and not st.session_state.paso_salud:
            if st.button("📊 Generar el Diagnóstico de la Salud Integral", use_container_width=True, key="btn_trigger_salud_integral", type="primary"):
                st.session_state.paso_salud = True
                st.rerun()
# =================================================================
# PARTE 7-B DE 7: ANEXIÓN DE SÍNTOMAS, BATERÍA LIKERT C&K Y GUARDIA MAIN
# =================================================================
        if st.session_state.paso_salud:
            st.divider()
            st.markdown("### 🍊 Diagnóstico de la Salud Integral")
            MATRIZ_SINTOMAS_DINAMICA = motor_generativo_items_audiencia(st.session_state.audiencia_activa, lang_code=iso)
            
            # Inicialización de listas defensivas para el conteo de respuestas en el estado de la sesión
            for g_idx, (g_name, lista_items_gajo) in enumerate(MATRIZ_SINTOMAS_DINAMICA.items()):
                with st.container(border=True):
                    st.markdown(f"#### {g_name}")
                    if len(lista_items_gajo) >= 4:
                        c_a, c_b = st.columns(2)
                        with c_a:
                            cb0 = st.checkbox(lista_items_gajo[0], key=f"cs_{g_idx}_0")
                            cb1 = st.checkbox(lista_items_gajo[1], key=f"cs_{g_idx}_1")
                        with c_b:
                            cb2 = st.checkbox(lista_items_gajo[2], key=f"cs_{g_idx}_2")
                            cb3 = st.checkbox(lista_items_gajo[3], key=f"cs_{g_idx}_3")
                        resultados_totales[g_name] = [str(i) for i, v in enumerate([cb0, cb1, cb2, cb3]) if v]

            # 🔥 INTERRUPTOR 2: Verifica que se haya respondido la Salud Integral antes de liberar C&K
            # El botón de transición C&K aparece de forma condicionada al flujo superior
            if not st.session_state.paso_cyk:
                if st.button("🎯 Generar Diagnóstico de Modelos Temporales Cronos y Kairós", use_container_width=True, type="primary", key="btn_trigger_cyk_adaptive"):
                    st.session_state.paso_cyk = True
                    st.rerun()

        if st.session_state.paso_cyk:
            st.divider()
            st.markdown("### 📋 Sección IV: Batería de Reactivos C&K Adaptativos")
            reactivos = algoritmo_generar_reactivos_poliglotas(resultados_totales, iso)
            for r_id, r_txt in reactivos.items():
                st.markdown(f"**Reactivo {r_id}:** {r_txt}")
                resultados_totales[f"R{r_id}"] = st.radio(
                    label="Escala / Scale:", 
                    options=[1, 2, 3, 4, 5], 
                    format_func=lambda x: tx.get(f"likert_{x}", str(x)), 
                    index=None, 
                    horizontal=True, 
                    key=f"rcyk_{r_id}"
                )

        gateway_bt(nombre, whatsapp, resultados_totales, True, iso, tx)
    else:
        st.balloons()
        st.success(tx.get("thanks", "¡Completado!"))
        rep = generar_pdf_diagnostico(st.session_state.get("nombre_usuario_persistente", "Participante"), st.session_state.get("whatsapp_usuario_persistente", ""), st.session_state.get("resultados_usuario_persistente", {}), st.session_state.audiencia_activa, True, iso)
        st.download_button(tx.get("btn_pdf", "📥 Descargar"), data=rep, file_name="Reporte.pdf", mime="application/pdf", use_container_width=True)

    # El tablero analítico corporativo gris se invoca y posiciona de forma secuencial abajo al autenticarse
    if st.session_state.admin_autenticado:
        renderizar_consola_baja_gris(st.session_state.audiencia_activa, iso, tx)

if __name__ == "__main__":
    main()
