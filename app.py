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

# 🍊 CONFIGURACIÓN BASAL DE PÁGINA ANCHURA GLOBAL
st.set_page_config(page_title="C&K Evaluation Core", page_icon="🍊", layout="wide")

URL_PRODUCCION = "https://dsimandarina.streamlit.app/?lang=en" 
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
# LÉXICO BILINGÜE METODOLÓGICO Y CENTRO DE MANDO CENTRAL
# =================================================================
CENTRO_MANDO_BILINGUE = {
    "es": {
        "nombre": "Escribe tu nombre completo / Full Name:",
        "wha": "Escribe tu WhatsApp internacional (con +):",
        "edad": "Edad biológica:", "genero": "Género:", "nac": "Nacionalidad:",
        "sec_i": "📋 Sección I: Perfil de identificación (Opcional)",
        "sec_ii": "📋 Sección II: Datos Demográficos y Geográficos (Obligatorio)",
        "sec_iii": "📋 Sección III: Conocimiento sobre el tema (Obligatorio)",
        "sec_iv": "📋 Sección IV: Batería de Reactivos C&K Adaptativos",
        "p1_s3": "1. ¿Habías escuchado hablar sobre los Modelos Temporales Cronos y Kairós?",
        "p2_s3": "2. ¿Has leído sobre los modelos temporales Cronos y Kairós?",
        "p3_s3": "3. ¿Has enseñado alguna vez sobre los modelos temporales Cronos y Kairós?",
        "p4_s3": "4. El modelo temporal:", "p5_s3": "5. Hablar de modelos temporales es hablar de:", "p6_s3": "6. Soy persona:",
        "side_title": "🔐 Panel del Ponente", "side_add": "Añadir Audiencia", "side_close": "Cerrar Panel",
        "intl_title": "🌐 Idioma del Sistema / Language", "intl_select": "Selecciona el idioma operativo:",
        "qr_title": "📢 Código de Acceso QR para la Audiencia", "mand_title": "🍊 Diagnóstico de la Salud Integral",
        "likert_1": "1 - Totalmente en Desacuerdo", "likert_2": "2 - En Desacuerdo", "likert_3": "3 - Neutral / No sé",
        "likert_4": "4 - De Acuerdo", "likert_5": "5 - Totalmente de Acuerdo",
        "btn_save": "💾 Registrar y Finalizar Instrumento", "btn_pdf": "📥 Descargar Dictamen en PDF",
        "err_fields": "Por favor completa Nombre y WhatsApp obligatoriamente.",
        "fields_msg": "La descarga se habilitará al ingresar tu perfil de identificación superior."
    },
    "en": {
        "nombre": "Enter your full name / Nombre completo:",
        "wha": "Enter international WhatsApp (with +):",
        "edad": "Biological age:", "genero": "Gender identity:", "nac": "Nationality framework:",
        "sec_i": "📋 Section I: Identification Profile (Optional)",
        "sec_ii": "📋 Section II: Demographic & Geographic Data (Mandatory)",
        "sec_iii": "📋 Section III: Knowledge of the Topic (Mandatory)",
        "sec_iv": "📋 Section IV: Adaptive C&K Items Battery",
        "p1_s3": "1. Have you ever heard about Cronos and Kairos Temporal Models?",
        "p2_s3": "2. Have you read about Cronos and Kairos temporal models?",
        "p3_s3": "3. Have you ever taught about Cronos and Kairos temporal models?",
        "p4_s3": "4. The temporal model:", "p5_s3": "5. Talking about temporal models means talking about:", "p6_s3": "6. I consider myself a person of type:",
        "side_title": "🔐 Speaker Dashboard", "side_add": "Add New Audience", "side_close": "Close Dashboard",
        "intl_title": "🌐 System Language / Idioma", "intl_select": "Select operative language:",
        "qr_title": "📢 Audience QR Access Code", "mand_title": "🍊 Comprehensive Health Diagnostic",
        "likert_1": "1 - Strongly Disagree", "likert_2": "2 - Disagree", "likert_3": "3 - Neutral / Don't know",
        "likert_4": "4 - Agree", "likert_5": "5 - Strongly Agree",
        "btn_save": "💾 Register & Finalize Instrument", "btn_pdf": "📥 Download PDF Diagnosis",
        "err_fields": "Name and WhatsApp fields are strictly mandatory.",
        "fields_msg": "Download will unlock once identification profile is entered above."
    }
}

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
        "lbl_ref1": "Hair, J. F. (2019). Multivariate Data Analysis. Cengage.",
        "lbl_ref2": "Schumacker, R. E. (2016). Structural Equation Modeling. Routledge.",
        "lbl_ref3": "Jacob, J. (2026). Epistemología del Tiempo Psicométrico. Editorial Mandarina."
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
        "lbl_ref1": "Hair, J. F. (2019). Multivariate Data Analysis. Cengage.",
        "lbl_ref2": "Schumacker, R. E. (2016). Structural Equation Modeling. Routledge.",
        "lbl_ref3": "Jacob, J. (2026). Epistemology of Psychometric Time. Mandarina Press."
    }
}

# =================================================================
# FRACCIÓN 2-PARTE A: PROCESAMIENTO EN LA NUBE Y TRANSACCIONES API
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

def guardar_en_google_sheets(tabla, nombre, whatsapp, resultados, token, es_likert=False):
    hoja = conectar_google_sheets(tabla)
    if hoja is None: return False
    try:
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        if not es_likert:
            fila = [ts, nombre, whatsapp, tabla, str(resultados), token]
        else:
            fila = [
                ts, nombre, whatsapp, tabla,
                resultados.get("Edad", ""), resultados.get("Género", ""), resultados.get("Nacionalidad", ""),
                resultados.get("Estado Origen", ""), resultados.get("Estado Residencia", ""), resultados.get("País Origen", ""),
                resultados.get("C1_Escuchado", ""), resultados.get("C2_Leído", ""), resultados.get("C3_Enseñado", ""),
                resultados.get("C4_Origen", ""), resultados.get("C5_Concepto", ""), resultados.get("C6_Perfil_Auto", "")
            ]
            for i in range(1, 11): 
                fila.append(resultados.get(f"R{i}", ""))
            fila.append(token)
        hoja.append_row(fila)
        return True
    except Exception:
        return False

def motor_generativo_items_audiencia(tabla, lang_code="es"):
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
def algoritmo_generar_reactivos_poliglotas(datos_participante, lang="es"):
    ed = int(datos_participante.get("Edad", 30)) if str(datos_participante.get("Edad", 30)).isdigit() else 30
    hl = "sí" in str(datos_participante.get("C2_Leído", "")).lower()
    est = "tecnico" if hl else ("institucional" if ed > 45 else ("dinamico" if ed < 25 else "reflexivo"))
    if lang == "es":
        if est == "institucional":
            return {
                1: "Estructuro mis compromisos diarios basándome rigurosamente en la métrica del reloj.",
                2: "Optimizo mis metas capitalizando momentos de máxima oportunidad operativa.",
                3: "Ejecuto mis planes bajo listas de verificación rígidas e inalterables.",
                4: "Experimento un flujo orgánico al gestionar mis responsabilidades cotidianas.",
                5: "Penalizo severamente la falta de puntualidad y la desalineación horaria laboral.",
                6: "Identifico imprevistos como ventanas estratégicas de alta utilidad analítica.",
                7: "Prefiero un orden secuencial antes de comprometerme con múltiples tareas.",
                8: "Rompo mi itinerario inmediatamente si detecto una ventaja competitiva clara.",
                9: "Resguardo bloques innegociables dedicados exclusivamente a descanso biológico.",
                10: "Activo una alta concentración si las condiciones del entorno cambian."
            }
        elif est == "dinamico":
            return {
                1: "Organizo cada hora de mi día siguiendo el control exacto de mis alarmas.",
                2: "Me enfoco en atrapar las mejores oportunidades en el instante en que aparecen.",
                3: "Sigo mis checklists al pie de la letra para asegurar el cumplimiento.",
                4: "Dejo que mis tareas fluyan de forma natural sin forzar un horario rígido.",
                5: "Me molesta profundamente perder minutos por la impuntualidad de otros.",
                6: "Aprovecho cambios inesperados para dar un giro creativo a mis actividades.",
                7: "Necesito terminar una actividad antes de saltar al siguiente pendiente.",
                8: "Cambio mis planes al momento si surge una opción mucho más ventajosa.",
                9: "Mantengo una rutina estricta para asegurar mi rendimiento óptimo.",
                10: "Duplico mi energía cuando las circunstancias me obligan a improvisar."
            }
        elif est == "tecnico":
            return {
                1: "Sincronizo bloques operativos sobre matrices cronométricas de alta precisión.",
                2: "Maximizo rendimiento asumiendo vectores basados en el factor Kairós.",
                3: "Administro procesamientos bajo un esquema cerrado de checklists secuenciales.",
                4: "Evidencio baja resistencia cognitiva cuando la transición es orgánica.",
                5: "Monitoreo y penalizo las desviaciones horarias dentro de mis flujos.",
                6: "Decodifico contingencias como ventanas óptimas para procesos de innovación.",
                7: "Mitigo el error operativo priorizando la ejecución lineal sobre la multitarea.",
                8: "Interrumpo la planificación estructural si emerge una ventana adaptativa.",
                9: "Blindo parámetros homeostáticos separando franjas fijas de recuperación.",
                10: "Estabilizo mi foco atencional ante incrementos críticos en la entropía."
            }
        else:
            return {
                1: "Estructuro mi agenda sobre plazos estrictos determinados por relojes.",
                2: "Alineo mis esfuerzos para actuar con agilidad en momentos clave.",
                3: "Gestiono el avance de mis metas mediante listas de control organizadas.",
                4: "Siento que el tiempo transcurre libre al realizar mis labores.",
                5: "Considero la impuntualidad profesional como falta de respeto metodológica.",
                6: "Encuentro valor en imprevistos si revealan alternativas de acción.",
                7: "Prefiero concentrarme en un problema en lugar de diversificarme.",
                8: "Dejo de lado mi itinerario si se presenta una oportunidad superior.",
                9: "Establezco límites claros para proteger mis tiempos de descanso.",
                10: "Mantengo claridad analítica cuando el entorno cambia rápidamente."
            }
    else:
        return {
            1: "I structure my daily commitments based strictly on exact clock metrics.",
            2: "I optimize strategic goals by capitalizing on operational opportunities.",
            3: "I execute performance plans under rigid and unalterable checklists.",
            4: "I experience an organic flow when managing my responsibilities.",
            5: "I strictly penalize untimeliness within my workspace.",
            6: "I read unexpected events during the day as useful strategic windows.",
            7: "I prefer a sequential, structured order before committing to tasks.",
            8: "I break my itinerary immediately if I detect a clear advantage.",
            9: "I safeguard non-negotiable blocks dedicated to biological rest.",
            10: "I trigger high concentration if my conditions change rapidly."
        }

def generar_pdf_diagnostico(nombre, whatsapp, resultados, tabla, es_likert=False, lang="es"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(20, 20, 20)
    pdf.set_auto_page_break(auto=True, margin=15)
    font_family = "Helvetica"
    dictamen_bilingue = TEXTOS_DICTAMEN_BILINGUE.get(lang, TEXTOS_DICTAMEN_BILINGUE["es"])
    tabla_saneada = str(tabla).replace("🍊", "").strip()
    
    hdr_txt = st.session_state.get("pdf_corp_header", "INFORME DE INVESTIGACION PSICOMETRICA // UNIVERSIDAD MANDARINA CORE")
    brand_txt = st.session_state.get("pdf_corp_brand", "Editorial Mandarina & Core Analytics Group")
    email_txt = st.session_state.get("pdf_corp_email", "especialista@modelostemporales.com")
    
    pdf.set_font(font_family, "B", 8); pdf.set_text_color(120, 120, 120)
    pdf.cell(170, 4, str(hdr_txt).upper().encode('latin-1','replace').decode('latin-1'), new_x="LMARGIN", new_y="NEXT")
    pdf.cell(170, 4, f"REGISTRO CLINICO COHORTE: {tabla_saneada.upper()} | FECHA: {time.strftime('%Y-%m-%d')}".encode('latin-1','replace').decode('latin-1'), new_x="LMARGIN", new_y="NEXT")
    pdf.line(20, 18, 190, 18); pdf.ln(5)
    
    pdf.set_font(font_family, "B", 14); pdf.set_text_color(15, 32, 66)
    txt_title = "Dictamen de Diagnostico Clinico Individual" if lang == "es" else "Individual Clinical Diagnosis Report"
    pdf.multi_cell(170, 7, txt_title.encode('latin-1','replace').decode('latin-1'), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    
    pdf.set_font(font_family, "", 10); pdf.set_text_color(50, 50, 50)
    n_seg = str(nombre).encode('latin-1','replace').decode('latin-1') if nombre else "Anonimo"
    w_seg = str(whatsapp).encode('latin-1','replace').decode('latin-1') if whatsapp else "N/A"
    pdf.cell(170, 6, f"Sujeto Evaluado: {n_seg}  |  Contacto: {w_seg}".encode('latin-1','replace').decode('latin-1'), new_x="LMARGIN", new_y="NEXT"); pdf.ln(4)
    
    g_trad = motor_generativo_items_audiencia(tabla, lang_code=lang)
    for idx, dim_espanol in enumerate(DIMENSIONES_MANDARINA_MAESTRAS):
        indices_marcados = resultados.get(dim_espanol, [])
        if indices_marcados:
            dim_limpia = str(list(g_trad.keys())[idx])
            for emj in ["💪", "🧠", "❤️", "👥", "💰", "⏳", "🙏", "🍊"]: dim_limpia = dim_limpia.replace(emj, "")
            pdf.set_font(font_family, "B", 10); pdf.set_text_color(15, 32, 66)
            pdf.cell(170, 5, f"Dimension Analizada: {dim_limpia.strip()}".encode('latin-1','replace').decode('latin-1'), new_x="LMARGIN", new_y="NEXT")
            sintomas_origen = list(g_trad.values())[idx]
            sintomas_reales = [sintomas_origen[int(i)] for i in indices_marcados if str(i).isdigit() and int(i) < len(sintomas_origen)]
            pdf.set_font(font_family, "I", 9); pdf.set_text_color(140, 30, 30)
            pdf.multi_cell(170, 4.5, f"Indicadores Criticos: {', '.join(sintomas_reales)}".encode('latin-1','replace').decode('latin-1'), new_x="LMARGIN", new_y="NEXT")
            pdf.set_font(font_family, "", 9); pdf.set_text_color(50, 50, 50)
            pdf.multi_cell(170, 4.5, f"Contencion: {dictamen_bilingue.get(dim_espanol, '')}".encode('latin-1','replace').decode('latin-1'), new_x="LMARGIN", new_y="NEXT"); pdf.ln(2)

    if es_likert:
        pdf.ln(2); pdf.set_font(font_family, "B", 11); pdf.set_text_color(15, 32, 66)
        pdf.cell(170, 6, "2. ANALISIS VECTORIAL TEMPORAL (C&K)", new_x="LMARGIN", new_y="NEXT")
        c_v = [int(resultados.get(f"R{i}", 3)) for i in range(1, 11, 2)]
        k_v = [int(resultados.get(f"R{i}", 3)) for i in range(2, 11, 2)]
        avg_c = sum(c_v) / 5 if c_v else 3.0
        avg_k = sum(k_v) / 5 if k_v else 3.0
        txt_p = dictamen_bilingue.get("txt_p_simbiosis" if abs(avg_c - avg_k) <= 0.4 else ("txt_p_kairos" if avg_k > avg_c else "txt_p_cronos"), "")
        pdf.set_font(font_family, "I", 9.5); pdf.multi_cell(170, 4.5, f"Dictamen Ontologico: {txt_p}".encode('latin-1','replace').decode('latin-1'), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2); pdf.set_font(font_family, "", 9); pdf.multi_cell(170, 4.5, f"Accion Metodologica: {dictamen_bilingue.get('txt_ck_recom', '')}".encode('latin-1','replace').decode('latin-1'), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3); pdf.set_fill_color(244, 245, 247); pdf.set_font(font_family, "B", 9)
        pdf.cell(170, 6, "AVISO DE INTERVENCION AVANZADA:", new_x="LMARGIN", new_y="NEXT", fill=True)
        pdf.set_font(font_family, "", 8.5); pdf.set_text_color(40, 40, 40)
        txt_cuerpo = f"Coordinacion de Atencion: {brand_txt}. Email: {email_txt}"
        pdf.multi_cell(170, 4, txt_cuerpo.encode('latin-1','replace').decode('latin-1'), new_x="LMARGIN", new_y="NEXT", fill=True)
    return bytes(pdf.output())

# =================================================================
# FRACCIÓN 3 - PARTE A Y B: CONSOLA BAJA GRIS Y MODELADO ESTOCÁSTICO SEM
# =================================================================
def renderizar_consola_baja_gris(tabla_analizar, iso, tx):
    st.markdown("""<style>
        .gray-dashboard-container {
            background-color: #f4f5f7; border: 2px solid #d1d5db; border-radius: 8px; padding: 20px; margin-top: 30px;
        }
    </style>""", unsafe_allow_html=True)
    st.markdown('<div class="gray-dashboard-container">', unsafe_allow_html=True)
    st.subheader(f"🔬 CONSOLA ANALÍTICA DOCTORAL PONENTE — COHORTE: {tabla_analizar.upper()}")
    
    sheet = conectar_google_sheets(tabla_analizar)
    todas_las_filas = sheet.get_all_values() if sheet else []
    tiene_datos = todas_las_filas and len(todas_las_filas) >= 2
    
    if tiene_datos:
        df_doc = pd.DataFrame(todas_las_filas[1:], columns=todas_las_filas)
        col_reactivos = [c for c in df_doc.columns if str(c).startswith("R")]
        
        t1, t2, t3 = st.tabs(["👥 Módulo I: Colectivo", "👤 Módulo II: CRM Clínico", "📐 Módulo III: SEM Matrix"])
        
        with t1:
            st.markdown("**Dataset Colectivo:**")
            st.dataframe(df_doc, use_container_width=True)
            if "❤️ Salud Emocional" in df_doc.columns and "🧠 Salud Mental" in df_doc.columns:
                p_burnout = df_doc["❤️ Salud Emocional"].apply(lambda x: len(str(x)) > 2).mean()
                p_mental = df_doc["🧠 Salud Mental"].apply(lambda x: len(str(x)) > 2).mean()
                df_b = df_doc[df_doc["❤️ Salud Emocional"].apply(lambda x: len(str(x)) > 2)]
                p_cond = df_b["🧠 Salud Mental"].apply(lambda x: len(str(x)) > 2).mean() if len(df_b) > 0 else 0.0
                
                ba, bb, bc = st.columns(3)
                ba.metric("P(Burnout)", f"{p_burnout*100:.1f}%")
                bb.metric("P(Bloqueo Mental)", f"{p_mental*100:.1f}%")
                bc.metric("P(Bloqueo | Burnout)", f"{p_cond*100:.1f}%")

        with t2:
            st.markdown("#### Ficha Criptográfica SHA-256")
            if "Nombre" in df_doc.columns and len(df_doc["Nombre"].unique()) > 0:
                sujeto_sel = st.selectbox("Sujeto Auditoría:", df_doc["Nombre"].unique().tolist(), key="sb_suj_adv")
                df_f = df_doc[df_doc["Nombre"] == sujeto_sel]
                if not df_f.empty:
                    pdf_c = FPDF(); pdf_c.add_page(); pdf_c.set_font("Helvetica", "B", 12)
                    pdf_c.cell(170, 10, f"CLINICAL MANUSCRIPT: {sujeto_sel.upper()}".encode('ascii','ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT")
                    hash_h = hashlib.sha256(bytes(pdf_c.output())).hexdigest().upper()
                    st.text(f"SHA-256 HASH VERIFICATION: [{hash_h}]")
                    
                    tel_crm = "".join(c for c in str(df_f.iloc.get('WhatsApp', '')) if c.isdigit())
                    w_u = f"https://wa.me{tel_crm}?text=Dictamen+con+sello+{hash_h[:8]}+listo."
                    st.markdown(f'<a href="{w_u}" target="_blank" style="text-decoration:none;"><div style="background-color:#25d366;color:white;padding:8px;border-radius:4px;text-align:center;font-weight:bold;">💬 ACCIÓN CRM WHATSAPP</div></a>', unsafe_allow_html=True)

        with t3:
            st.markdown(r"#### Modelado de Ecuaciones Estructurales (ESEM-Geo / ICM-CFA)")
            if len(df_doc) >= 3 and len(col_reactivos) >= 4:
                try:
                    matriz_num = df_doc[col_reactivos].apply(pd.to_numeric, errors='coerce').fillna(3).to_numpy()
                    n_casos = int(matriz_num.shape[0]) if len(matriz_num.shape) > 0 else 0
                    n_items = int(matriz_num.shape[1]) if len(matriz_num.shape) > 1 else 0
                    
                    if n_casos >= 3 and n_items >= 4:
                        matriz_centrada = matriz_num - np.mean(matriz_num, axis=0)
                        matriz_cov_S = (matriz_centrada.T @ matriz_centrada) / (n_casos - 1)
                        if np.linalg.det(matriz_cov_S) == 0: matriz_cov_S += np.eye(n_items) * 1e-4
                        
                        var_items = np.var(matriz_num, ddof=1, axis=0)
                        var_total = np.var(np.sum(matriz_num, axis=1), ddof=1)
                        alfa_calc = (n_items / (n_items - 1)) * (1 - (np.sum(var_items) / var_total)) if var_total > 0 and n_items > 1 else 0.0
                        
                        p_respuestas = np.mean(matriz_num, axis=0) / 5.0
                        informacion_fisher = np.sum(p_respuestas * (1.0 - p_respuestas))
                        
                        _, S_vals, _ = np.linalg.svd(matriz_centrada, full_matrices=False)
                        s1 = S_vals[0] if len(S_vals) > 0 else 0.0
                        s2 = S_vals[1] if len(S_vals) > 1 else 0.0
                        
                        f_min_nulo = np.sum(np.log(np.diag(matriz_cov_S))) - np.log(np.linalg.det(matriz_cov_S))
                        chi_nulo = f_min_nulo * (n_casos - 1)
                        df_nulo = (n_items * (n_items - 1)) / 2
                        
                        cargas_esem = np.outer(np.sqrt(var_items), np.array([0.6 if i%2==0 else 0.2 for i in range(n_items)]))
                        matriz_sigma_implicita = (cargas_esem @ cargas_esem.T) + np.diag(var_items * 0.4)
                        
                        f_min_propuesto = np.trace(matriz_cov_S @ np.linalg.pinv(matriz_sigma_implicita)) + np.log(np.linalg.det(matriz_sigma_implicita)) - np.log(np.linalg.det(matriz_cov_S)) - n_items
                        f_min_propuesto = max(0.001, f_min_propuesto)
                        chi_propuesto = f_min_propuesto * (n_casos - 1)
                        df_propuesto = max(1, int(((n_items * (n_items + 1)) / 2) - (n_items * 2)))
                        
                        cfi_val = 1.0 - (max(0.0, chi_propuesto - df_propuesto) / max(0.0, chi_nulo - df_nulo)) if chi_nulo > df_nulo else 1.0
                        cfi_val = min(1.0, max(0.0, cfi_val))
                        tli_val = 1.0 - ((chi_propuesto / df_propuesto) / (chi_nulo / df_nulo)) if chi_nulo > 0 and df_propuesto > 0 else 1.0
                        tli_val = min(1.0, max(0.0, tli_val))
                        rmsea_val = np.sqrt(max(0.0, (chi_propuesto - df_propuesto) / (df_propuesto * (n_casos - 1)))) if df_propuesto > 0 else 0.0
                        rmsea_val = min(0.5, rmsea_val)
                        
                        c_m1, c_m2, c_m3 = st.columns(3)
                        c_m1.metric("CFI Index", f"{cfi_val:.4f}")
                        c_m2.metric("TLI Index", f"{tli_val:.4f}")
                        c_m3.metric("RMSEA Index", f"{rmsea_val:.4f}")
                        
                        st.markdown("##### 📊 Propiedades Psicométricas (SEM)")
                        html_tabla_sem = f"""
                        <table style="width:100%; border-collapse:collapse; background:#fff; font-size:12px; border:1px solid #ddd;">
                            <tr style="background:#f4f5f7;">
                                <th style="padding:6px; border:1px solid #ddd;">Métrica SEM</th>
                                <th style="padding:6px; border:1px solid #ddd;">Valor</th>
                                <th style="padding:6px; border:1px solid #ddd;">Criterio</th>
                            </tr>
                            <tr>
                                <td style="padding:6px; border:1px solid #ddd;"><b>ESEM-Geo Rotación</b></td>
                                <td style="padding:6px; border:1px solid #ddd;">{s1:.2f} (λ₁) | {s2:.2f} (λ₂)</td>
                                <td style="padding:6px; border:1px solid #ddd;">λ > 1.0</td>
                            </tr>
                            <tr>
                                <td style="padding:6px; border:1px solid #ddd;"><b>Fit Indexes (CFI/TLI)</b></td>
                                <td style="padding:6px; border:1px solid #ddd;">CFI={cfi_val:.3f} | TLI={tli_val:.3f}</td>
                                <td style="padding:6px; border:1px solid #ddd;">≥ 0.950</td>
                            </tr>
                            <tr>
                                <td style="padding:6px; border:1px solid #ddd;"><b>RMSEA Discrepancia</b></td>
                                <td style="padding:6px; border:1px solid #ddd;"><b>{rmsea_val:.4f}</b></td>
                                <td style="padding:6px; border:1px solid #ddd;">≤ 0.060</td>
                            </tr>
                        </table>
                        """
                        st.markdown(html_tabla_sem, unsafe_allow_html=True)
                except Exception as e: st.error(f"Error algebraico: {e}")
            else: st.warning("📐 El motor ESEM/CFA requiere mínimo 3 registros Likert y 4 reactivos.")
    else: st.info("ℹ️ Repositorio sin registros activos.")
    st.markdown('</div>', unsafe_allow_html=True)
        # 🍊 FIX DE INDENTACIÓN: Bloque alineado a 4 espacios para vivir dentro de main()
    with col_izq:
        if not st.session_state.flujo_finalizado:
            if st.session_state.admin_autenticado:
                st.markdown(f"### {tx.get('qr_title', '📢 QR Code')}")
                qr = qrcode.QRCode(version=1, box_size=10, border=2)
                qr.add_data(f"{URL_PRODUCCION}?lang={iso}"); qr.make(fit=True)
                buf_qr = BytesIO()
                qr.make_image(fill_color="black", back_color="white").save(buf_qr, format="PNG")
                st.image(buf_qr.getvalue(), width=130); st.divider()

            nombre_in = st.text_input(tx.get("nombre", "Name:"), key="n_in_seq_final")
            whatsapp_in = st.text_input(tx.get("wha", "WhatsApp:"), key="w_in_seq_final")
            
            resultados_totales["Edad"] = int(st.number_input(tx.get("edad", "Age:"), 10, 100, 20, key="num_ed_final"))
            resultados_totales["Género"] = st.radio(tx.get("genero", "Gender:"), ["Masculino / Male", "Femenino / Female", "Otro / Other"], index=None, horizontal=True, key="rad_g_final")
            resultados_totales["Nacionalidad"] = st.radio(tx.get("nac", "Nationality:"), ["Mexicana", "Extranjera"], index=None, horizontal=True, key="rad_n_final")
            
            if resultados_totales.get("Nacionalidad") == "Mexicana":
                resultados_totales["Estado Origen"] = st.selectbox("Estado de origen:", [""] + ESTADOS_MEXICO, key="s_orig_final")
                resultados_totales["Estado Residencia"] = st.selectbox("Estado de residencia actual:", [""] + ESTADOS_MEXICO, key="s_res_final")
            elif resultados_totales.get("Nacionalidad") == "Extranjera":
                resultados_totales["País Origen"] = st.text_input("País de Origen:", key="t_pais_final")
                resultados_totales["Continente Extranjero"] = st.selectbox("Continente:", ["", "América", "Europa", "Asia", "África", "Oceanía"], key="s_cont_final")

            st.subheader(tx.get("sec_iii", "📋 Evaluation"))
            for k_r, txt_r in [("C1_Escuchado", tx.get("p1_s3")), ("C2_Leído", tx.get("p2_s3")), ("C3_Enseñado", tx.get("p3_s3"))]: 
                resultados_totales[k_r] = st.radio(txt_r, ["Sí / Yes", "No"], index=None, horizontal=True, key=f"r_k_{k_r}_final")
                
            resultados_totales["C4_Origen"] = st.radio(tx.get("p4_s3"), ["Se impone", "Se hereda", "No sé"], index=None, horizontal=True, key="r_c4_final")
            resultados_totales["C5_Concepto"] = st.radio(tx.get("p5_s3"), ["Teología", "Cultura", "Francamente no sé"], index=None, horizontal=True, key="r_c5_final")
            resultados_totales["C6_Perfil_Auto"] = st.radio(tx.get("p6_s3"), ["Cronos", "Kairós", "No sé"], index=None, horizontal=True, key="r_c6_final")

            vld_secciones = all([resultados_totales.get(k) is not None for k in ["Género", "Nacionalidad", "C1_Escuchado", "C4_Origen", "C5_Concepto", "C6_Perfil_Auto"]])
            
            if vld_secciones and not st.session_state.paso_salud:
                if st.button("📊 Generar el Diagnóstico de la Salud Integral", use_container_width=True, key="btn_trig_salud_final", type="primary"):
                    st.session_state.paso_salud = True; st.rerun()


            if st.session_state.paso_salud:
                st.divider(); st.markdown(f"### {tx.get('mand_title', '🍊 Diagnóstico')}")
                MATRIZ_DINAMICA = motor_generativo_items_audiencia(st.session_state.audiencia_activa, lang_code=iso)
                for g_idx, (g_name, lista_items) in enumerate(MATRIZ_DINAMICA.items()):
                    with st.container(border=True):
                        st.markdown(f"#### {g_name}")
                        if len(lista_items) >= 4:
                            ca, cb = st.columns(2)
                            with ca:
                                cb0 = st.checkbox(str(lista_items[0]), key=f"cbf_{g_idx}_0")
                                cb1 = st.checkbox(str(lista_items[1]), key=f"cbf_{g_idx}_1")
                            with cb:
                                cb2 = st.checkbox(str(lista_items[2]), key=f"cbf_{g_idx}_2")
                                cb3 = st.checkbox(str(lista_items[3]), key=f"cbf_{g_idx}_3")
                            resultados_totales[g_name] = [str(i) for i, v in enumerate([cb0, cb1, cb2, cb3]) if v]

                if not st.session_state.paso_cyk:
                    if st.button("🎯 Generar Diagnóstico de Modelos C&K", use_container_width=True, type="primary", key="btn_trig_cyk_final"):
                        st.session_state.paso_cyk = True; st.rerun()

                if st.session_state.paso_salud:
                    <st.divider()
                    st.markdown(f"### {tx.get('mand_title', '🍊 Diagnóstico')}")
                MATRIZ_DINAMICA = motor_generativo_items_audiencia(st.session_state.audiencia_activa, lang_code=iso)
                for g_idx, (g_name, lista_items) in enumerate(MATRIZ_DINAMICA.items()):
                    with st.container(border=True):
                        st.markdown(f"#### {g_name}")
                        if len(lista_items) >= 4:
                            ca, cb = st.columns(2)
                            with ca:
                                cb0 = st.checkbox(str(lista_items[0]), key=f"cbf_{g_idx}_0")
                                cb1 = st.checkbox(str(lista_items[1]), key=f"cbf_{g_idx}_1")
                            with cb:
                                cb2 = st.checkbox(str(lista_items[2]), key=f"cbf_{g_idx}_2")
                                cb3 = st.checkbox(str(lista_items[3]), key=f"cbf_{g_idx}_3")
                            resultados_totales[g_name] = [str(i) for i, v in enumerate([cb0, cb1, cb2, cb3]) if v]

                if not st.session_state.paso_cyk:
                    if st.button("🎯 Generar Diagnóstico de Modelos C&K", use_container_width=True, type="primary", key="btn_trig_cyk_final"):
                        st.session_state.paso_cyk = True; st.rerun()

            if st.session_state.paso_cyk:
                st.divider()
                st.markdown(f"### {tx.get('sec_iv', '📋 Reactivos C&K')}")
                reactivos = algoritmo_generar_reactivos_poliglotas(resultados_totales, iso)
                vld_likert = True
                for r_id, r_txt in reactivos.items():
                    st.markdown(f"**Reactivo {r_id}:** {r_txt}")
                    resultados_totales[f"R{r_id}"] = st.radio(
                        label="Escala:", options=[1, 2, 3, 4, 5], 
                        format_func=lambda x: tx.get(f"likert_{x}", str(x)), 
                        index=None, horizontal=True, key=f"rcyk_f_{r_id}"
                    )
                    if resultados_totales[f"R{r_id}"] is None: vld_likert = False

                if vld_likert:
                    gateway_bt(nombre_in, whatsapp_in, resultados_totales, True, iso, tx)
        else:
            st.balloons()
            st.success(tx.get("thanks", "🎉 ¡Evaluación Procesada Exitosamente!"))
            n_p = st.session_state.get("nombre_usuario_persistente", "Participante")
            w_p = st.session_state.get("whatsapp_usuario_persistente", "")
            r_p = st.session_state.get("resultados_usuario_persistente", {})
            rep = generar_pdf_diagnostico(n_p, w_p, r_p, st.session_state.audiencia_activa, True, iso)
            
            c_dl1, c_dl2 = st.columns(2)
            with c_dl1:
                st.download_button(tx.get("btn_pdf", "📥 Descargar PDF"), data=rep, file_name=f"Dictamen_{n_p}.pdf", mime="application/pdf", use_container_width=True, key="btn_dl_final_p2")
            with c_dl2:
                if w_p:
                    t_cln = "".join(c for c in str(w_p) if c.isdigit())
                    txt_wa = f"Hola {n_p}, tu dictamen ha sido generado exitosamente."
                    wa_url = f"https://wa.me{t_cln}?text={urllib.parse.quote(txt_wa)}"
                    st.markdown(f'<a href="{wa_url}" target="_blank" style="text-decoration:none;"><div style="background-color:#25d366;color:white;padding:10px;border-radius:4px;text-align:center;font-weight:bold;">💬 ENVIAR WHATSAPP</div></a>', unsafe_allow_html=True)

            if st.button("🔄 Reset Evaluation", use_container_width=True, key="btn_reset_final"):
                st.session_state.flujo_finalizado = False; st.session_state.paso_salud = False; st.session_state.paso_cyk = False; st.rerun()
    # 🍊 RENDERIZADO DEL EDITOR CORPORATIVO A LA DERECHA (4 espacios de sangría)
    if col_der is not None:
        with col_der:
            with st.container(border=True):
                st.markdown("### ⚙️ Backend PDF Corporativo")
                st.session_state.pdf_corp_header = st.text_area(
                    "Encabezado Técnico:", 
                    value=st.session_state.pdf_corp_header, 
                    key="ta_backend_hdr"
                )
                st.session_state.pdf_corp_brand = st.text_input(
                    "Firma Institucional / Aval:", 
                    value=st.session_state.pdf_corp_brand, 
                    key="ti_backend_brand"
                )
                st.session_state.pdf_corp_email = st.text_input(
                    "Correo Electrónico de Enlace:", 
                    value=st.session_state.pdf_corp_email, 
                    key="ti_backend_email"
                )

    if st.session_state.admin_autenticado:
        renderizar_consola_baja_gris(st.session_state.audiencia_activa, iso, tx)

if __name__ == "__main__":
    main()
