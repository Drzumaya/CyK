# =================================================================
# PARTE 1: PROTOCOLOS DE IMPORTACIÓN Y CONFIGURACIÓN DE NÚCLEO GLOBAL
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

# 🍊 CONFIGURACIÓN DE PÁGINA INMUNE A DESBORDAMIENTO EN NUBE
st.set_page_config(page_title="C&K Evaluation Core", page_icon="🍊", layout="wide")

# Parámetros logísticos fijos estáticos de producción
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
# PARTE 2: LÉXICO BILINGÜE METODOLÓGICO Y CENTRO DE MANDO
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
# PARTE 3: GLOSARIOS DE DICTAMEN EPISTEMOLÓGICO Y CITAS DOCTORALES
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
# PARTE 4: ACCESO A REPOSITORIOS EN LA NUBE Y DICCIONARIOS CLÍNICOS
# =================================================================
def conectar_google_sheets(nombre_tabla):
    """
    Establece conexión encriptada de alta seguridad con la API de Google Sheets
    utilizando las credenciales secretas guardadas en la bóveda de la app.
    """
    try:
        credenciales_dict = st.secrets["gcp_service_account"]
        scope = ["https://googleapis.com", "https://googleapis.com"]
        credenciales = Credentials.from_service_account_info(credenciales_dict, scopes=scope)
        cliente = gspread.authorize(credenciales)
        # Sincroniza dinámicamente con la hoja de cálculo maestra unificada
        libro = cliente.open_by_key("1y99f_7hGv_3mUeE4K_1m49wB7r0V4oW3mDeR4_m49pQ")
        return libro.worksheet(nombre_tabla)
    except Exception:
        return None

def guardar_en_google_sheets(tabla, nombre, whatsapp, resultados, token_seguridad, es_likert=False):
    """
    Registra los datos transaccionales del participante de forma lineal en la nube.
    """
    hoja = conectar_google_sheets(tabla)
    if hoja is None:
        return False
    try:
        marca_tiempo = time.strftime("%Y-%m-%d %H:%M:%S")
        if not es_likert:
            # Serialización en string plano para el bloque clínico multivariado
            fila = [marca_tiempo, nombre, whatsapp, str(resultados), token_seguridad]
        else:
            fila = [
                marca_tiempo, nombre, whatsapp, 
                resultados.get("Edad", ""), resultados.get("Género", ""), resultados.get("Nacionalidad", ""),
                resultados.get("Estado Origen", ""), resultados.get("Estado Residencia", ""), resultados.get("País Origen", ""),
                resultados.get("C1_Escuchado", ""), resultados.get("C2_Leído", ""), resultados.get("C3_Enseñado", ""),
                resultados.get("C4_Origen", ""), resultados.get("C5_Concepto", ""), resultados.get("C6_Perfil_Auto", "")
            ]
            for i in range(1, 11):
                fila.append(resultados.get(f"R{i}", ""))
            fila.append(token_seguridad)
        hoja.append_row(fila)
        return True
    except Exception:
        return False

def motor_generativo_items_audiencia(nombre_audiencia, lang_code="es"):
    """
    Genera el diccionario de 4 síntomas reales asignados a cada gajo dimensional
    para el formulario adaptativo de Salud Integral sin causar duplicidades.
    """
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
# PARTE 5: ALGORITMO GENERATIVO DE REACTIVOS C&K ADAPTATIVOS
# =================================================================
def algoritmo_generar_reactivos_poliglotas(datos_participante, lang="es"):
    """
    Genera la batería de 10 reactivos C&K en primera persona, adaptando 
    el estilo semántico según edad, género y conocimiento previo del usuario,
    sin exponer la audiencia de forma burda. Ítems impares = Cronos | Pares = Kairós.
    """
    edad = int(datos_participante.get("Edad", 30))
    ha_leido = "sí" in str(datos_participante.get("C2_Leído", "")).lower()
    es_experto = "sí" in str(datos_participante.get("C3_Enseñado", "")).lower()
    
    estilo = "reflexivo"
    if edad > 45: estilo = "institucional"
    elif edad < 25: estilo = "dinamico"
    if ha_leido or es_experto: estilo = "tecnico"

    if lang == "es":
        if estilo == "institucional":
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
        elif estilo == "dinamico":
            return {
                1: "Organizo cada hora de mi día siguiendo el control exacto de mis alarmas y agendas.",
                2: "Me enfoco en atrapar las mejores oportunidades en el instante preciso en que aparecen.",
                3: "Sigo mis checklists al pie de la letra para asegurar el cumplimiento de mis entregas.",
                4: "Dejo que mis tareas fluyan de forma natural sin forzar un horario rígido de oficina.",
                5: "Me molesta profundamente perder minutos valiosos debido a la impuntualidad de otros.",
                6: "Aprovecho los cambios de planes inesperados para dar un giro creativo a mis actividades.",
                7: "Necesito terminar por completo una actividad antes de saltar al siguiente pendiente.",
                8: "Cambio mis planes al momento si surge una opción mucho más atractiva o ventajosa.",
                9: "Mantengo una rutina estricta para asegurar mis horas de sueño y rendimiento óptimo.",
                10: "Duplico mi energía y foco de atención cuando las circunstancias me obligan a improvisar."
            }
        elif estilo == "tecnico":
            return {
                1: "Sincronizo mis bloques operativos sobre matrices cronométricas de alta precisión temporal.",
                2: "Maximizo mi rendimiento asumiendo vectores de oportunidad basados en el factor Kairós.",
                3: "Administro mis procesos de ejecución bajo un esquema cerrado de checklists secuenciales.",
                4: "Evidencio una baja resistencia cognitiva cuando la transición de tareas es orgánica.",
                5: "Monitoreo y penalizo las desviaciones horarias dentro de mis flujos de producción.",
                6: "Decodifico las contingencias del entorno como ventanas analíticas óptimas para innovar.",
                7: "Mitigo el error operativo priorizando la ejecución lineal sobre la multitarea saturada.",
                8: "Interrumpo la planificación estructural si emerge una ventana adaptativa preferente.",
                9: "Blindo mis parámetros homeostáticos separando franjas fijas de recuperación biológica.",
                10: "Estabilizo mi foco atencional ante incrementos críticos en la entropía del contexto."
            }
        else:
            return {
                1: "Estructuro mi agenda sobre plazos estrictos determinados por relojes exactos.",
                2: "Alineo mis esfuerzos diarios para actuar con agilidad en los momentos clave.",
                3: "Gestiono el avance de mis metas mediante el uso de listas de control organizadas.",
                4: "Siento que el tiempo transcurre de forma más libre cuando realizo mis labores.",
                5: "Considero la impuntualidad profesional como una falta de respeto metodológica.",
                6: "Encuentro un valor profundo en los imprevistos cuando revelan nuevas alternativas.",
                7: "Prefiero concentrarme en un solo problema estructurado en lugar de diversificarme.",
                8: "Dejo de lado mi itinerario si se presenta una oportunidad superior para avanzar.",
                9: "Establezco límites claros para proteger mis tiempos de descanso y desconexión laboral.",
                10: "Mantengo la calma y la claridad analítica cuando todo a mi ancestral alrededor cambia rápidamente."
            }
    else:
        if estilo == "institucional":
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
        elif estilo == "dinamico":
            return {
                1: "I organize every hour of my day following the exact control of alarms and calendars.",
                2: "I focus on catching the best opportunities at the precise instant they appear.",
                3: "I follow my checklists to the letter to ensure the timely completion of my tasks.",
                4: "I let my work flow naturally without forcing a rigid administrative office schedule.",
                5: "I get deeply annoyed by losing valuable minutes due to other people's untimeliness.",
                6: "I take advantage of unexpected changes in plans to give a creative twist to my workflow.",
                7: "I need to completely finish one activity before jumping to the next pending item.",
                8: "I change my plans on the spot if a much more attractive or advantageous option emerges.",
                9: "I maintain a strict routine to secure my hours of sleep and optimal daily performance.",
                10: "I double my focus and energy level when circumstances force me to improvise."
            }
        elif estilo == "tecnico":
            return {
                1: "I synchronize my operational blocks on highly precise chronometric time matrices.",
                2: "I maximize my output by leveraging opportunity vectors based on the Kairos factor.",
                3: "I manage my execution processes under a closed sequence of structured checklists.",
                4: "I demonstrate low cognitive resistance when the task transition is organic.",
                5: "I strictly monitor and penalize schedule deviations within my production flows.",
                6: "I decode environmental contingencies as optimal analytical windows for innovation.",
                7: "I mitigate operational errors by prioritizing linear execution over saturated multitasking.",
                8: "I interrupt structural planning if a preferential adaptive window emerges.",
                9: "I shield my homeostatic parameters by separating fixed slots for biological recovery.",
                10: "I stabilize my attentional focus during critical increases in context entropy."
            }
        else:
            return {
                1: "I structure my timeline based on strict deadlines determined by exact clocks.",
                2: "I align my daily efforts to act with agility during key opportunities.",
                3: "I manage the progress of my goals through organized checking matrices.",
                4: "I feel that time flows more freely when I perform my administrative work.",
                5: "I consider professional untimeliness as a serious methodological failure.",
                6: "I find a profound value in unexpected events when they reveal new alternatives.",
                7: "I prefer to concentrate on a single structured problem instead of dividing my focus.",
                8: "I leave my itinerary aside if a superior opportunity to advance presents itself.",
                9: "I establish clear boundaries to protect my resting time and digital fasting hours.",
                10: "I maintain my analytical clarity when everything around me changes rapidly."
            }
# =================================================================
# PARTE 6: CONSTRUCTOR REGLAMENTARIO DE REPORTES DOCTORALES EN PDF
# =================================================================
def generar_pdf_diagnostico(nombre, whatsapp, resultados, tabla, es_likert=False, lang="es"):
    """
    Ensambla el documento PDF formal bajo rigurosos criterios editoriales.
    Maneja el bloque multivariado de Salud Integral o el bloque cuantitativo C&K.
    """
    pdf = FPDF()
    pdf.core_fonts_encoding = "cp1252"
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    font_family = "Helvetica"
    dictamen_bilingue = TEXTOS_DICTAMEN_BILINGUE.get(lang, TEXTOS_DICTAMEN_BILINGUE["es"])
    
    base_title = "Reporte de Evaluacion Psicometrica Individual" if lang == "es" else "Individual Psychometric Evaluation Report"
    pdf.set_font(font_family, "B", 14)
    pdf.cell(190, 10, str(base_title).encode('ascii', 'ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(2)
    
    pdf.set_font(font_family, "", 10)
    n_seg = str(nombre).encode('ascii', 'ignore').decode('ascii') if nombre else "Anonimo"
    w_seg = str(whatsapp).encode('ascii', 'ignore').decode('ascii') if whatsapp else "N/A"
    pdf.cell(190, 6, f"Participante: {n_seg} | Contacto: {w_seg}".encode('ascii', 'ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    
    if not es_likert:
        g_trad = motor_generativo_items_audiencia(tabla, lang_code=lang)
        for idx, dim_traducida_emoji in enumerate(g_trad.keys()):
            if len(resultados.get(DIMENSIONES_MANDARINA_MAESTRAS[idx], [])) > 0:
                key_segura = str(dim_traducida_emoji).encode('cp1252', 'ignore').decode('cp1252')
                for emj in ["💪", "🧠", "❤️", "👥", "💰", "⏳", "🙏"]: 
                    key_segura = key_segura.replace(emj, "")
                
                pdf.set_font(font_family, "B", 11)
                pdf.cell(190, 6, f"Dimension: {key_segura.strip()}", new_x="LMARGIN", new_y="NEXT")
                
                indices_marcados = resultados.get(DIMENSIONES_MANDARINA_MAESTRAS[idx], [])
                sintomas_origen_nicho = list(g_trad.values())[idx]
                sintomas_reportados = [sintomas_origen_nicho[int(i)] for i in indices_marcados if int(i) < len(sintomas_origen_nicho)]
                
                pdf.set_font(font_family, "I", 9.5)
                pdf.set_text_color(120, 30, 30)
                pdf.multi_cell(190, 4.5, f"Indicadores detectados: {', '.join(sintomas_reportados)}".encode('cp1252', 'ignore').decode('cp1252'), new_x="LMARGIN", new_y="NEXT")
                
                glosario_seguro = str(dictamen_bilingue.get(DIMENSIONES_MANDARINA_MAESTRAS[idx], "")).encode('cp1252', 'ignore').decode('cp1252')
                pdf.set_font(font_family, "", 9.5)
                pdf.set_text_color(50, 50, 50)
                pdf.multi_cell(190, 4.5, f"Sugerencia base: {glosario_seguro.strip()}", new_x="LMARGIN", new_y="NEXT")
                
                if "⏳" in dim_traducida_emoji or "temporal" in dim_traducida_emoji.lower():
                    pdf.ln(1)
                    pdf.set_font(font_family, "B", 9.5)
                    pdf.set_text_color(150, 50, 0)
                    pdf.cell(190, 5, "ANÁLISIS DE RIESGO PROSPECTIVO Y CONSECUENCIAS:", new_x="LMARGIN", new_y="NEXT")
                    pdf.set_font(font_family, "", 9)
                    pdf.set_text_color(60, 60, 60)
                    
                    c_corto = "- Corto Plazo: Elevacion de fatiga cognitiva, saturacion horaria y perdida de ventanas de oportunidad."
                    c_medio = "- Mediano Plazo: Sindrome de Burnout latente, desequilibrio en dinamicas familiares y friccion operacional."
                    c_largo = "- Largo Plazo: Cronificacion del estres, colapso de efectividad y perdida del proposito estrategico vocacional."
                    pdf.multi_cell(190, 4, c_corto.encode('cp1252','ignore').decode('cp1252'), new_x="LMARGIN", new_y="NEXT")
                    pdf.multi_cell(190, 4, c_medio.encode('cp1252','ignore').decode('cp1252'), new_x="LMARGIN", new_y="NEXT")
                    pdf.multi_cell(190, 4, c_largo.encode('cp1252','ignore').decode('cp1252'), new_x="LMARGIN", new_y="NEXT")
                    
                    pdf.ln(1)
                    pdf.set_font(font_family, "B", 9.5)
                    pdf.set_text_color(180, 0, 0)
                    r_esp = "💡 RECOMENDACIÓN CRÍTICA: Debido al nivel de riesgo detectado en tu vector dimensional temporal, es indispensable solicitar una consulta especializada de forma directa con el ponente."
                    pdf.multi_cell(190, 4.5, r_esp.encode('cp1252','ignore').decode('cp1252'), new_x="LMARGIN", new_y="NEXT")
                pdf.ln(3)
                pdf.set_text_color(0, 0, 0)
# =================================================================
# PARTE 7: COMPILACIÓN CUANTITATIVA C&K EN PDF Y COMPUERTA GENERAL
# =================================================================
    else:
        k_v = [int(resultados.get(f"R{i}", 3)) for i in range(1, 11, 2)]
        c_v = [int(resultados.get(f"R{i}", 3)) for i in range(2, 11, 2)]
        avg_c = sum(c_v) / 5 if len(c_v) > 0 else 3.0
        avg_k = sum(k_v) / 5 if len(k_v) > 0 else 3.0
        
        pdf.set_font(font_family, "B", 11)
        pdf.cell(190, 6, "1. RESULTADOS DE LA EVALUACION CUANTITATIVA", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font(font_family, "", 10)
        pdf.cell(190, 5, f"Media Vector Cronos: {avg_c:.2f} | Media Vector Kairos: {avg_k:.2f}".encode('ascii','ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)
        
        pdf.set_font(font_family, "B", 11)
        pdf.cell(190, 6, "2. APARTADO DE ANALISIS Y PERFIL DOMINANTE", new_x="LMARGIN", new_y="NEXT")
        dif = abs(avg_c - avg_k)
        if dif <= 0.4: txt_p = dictamen_bilingue.get("txt_p_simbiosis", "Simbiosis")
        elif avg_k > avg_c: txt_p = dictamen_bilingue.get("txt_p_kairos", "Dominancia Kairos")
        else: txt_p = dictamen_bilingue.get("txt_p_cronos", "Dominancia Cronos")
            
        pdf.set_font(font_family, "I", 10)
        pdf.multi_cell(190, 5, str(txt_p).encode('cp1252', 'ignore').decode('cp1252'), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)
        
        pdf.set_font(font_family, "B", 11)
        pdf.cell(190, 6, "3. PROSPECTIVA DE RIESGO TEMPORAL Y CONSECUENCIAS", new_x="LMARGIN", new_y="NEXT")
        if avg_c > avg_k:
            r_c_corto = "- Corto Plazo: Incremento agudo de rigidez mental, estres ante imprevistos cotidianos."
            r_c_medio = "- Mediano Plazo: Perdida sistemica de ventanas de oportunidad (Kairos) por apego al reloj."
            r_c_largo = "- Largo Plazo: Obsolescencia adaptativa y colapso de la plasticidad cognitiva estructural."
        else:
            r_c_corto = "- Corto Plazo: Desorden administrativo inmediato, desalineacion de plazos obligatorios."
            r_c_medio = "- Mediano Plazo: Perdida de credibilidad profesional institucional por impuntualidad."
            r_c_largo = "- Largo Plazo: Crisis de estabilidad familiar e incapacidad de consolidar proyectos."
            
        pdf.multi_cell(190, 5, r_c_corto.encode('cp1252','ignore').decode('cp1252'), new_x="LMARGIN", new_y="NEXT")
        pdf.multi_cell(190, 5, r_c_medio.encode('cp1252','ignore').decode('cp1252'), new_x="LMARGIN", new_y="NEXT")
        pdf.multi_cell(190, 5, r_c_largo.encode('cp1252','ignore').decode('cp1252'), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)
        
        pdf.set_font(font_family, "B", 11)
        pdf.cell(190, 6, "4. RECOMENDACIONES METODOLOGICAS DE CONTENCION", new_x="LMARGIN", new_y="NEXT")
        gl_recom = str(dictamen_bilingue.get("txt_ck_recom", "Ajustar franjas")).encode('cp1252', 'ignore').decode('cp1252')
        pdf.multi_cell(190, 5, gl_recom, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        
        pdf.set_font(font_family, "B", 10)
        pdf.set_text_color(180, 0, 0)
        req_ponente = "🚨 ATENCION DIRECTA: Al tratarse de una asimetria dimensional temporal, se le recomienda al participante agendar una consulta especializada de caracter personal o familiar con el ponente."
        pdf.multi_cell(190, 4.5, req_ponente.encode('cp1252','ignore').decode('cp1252'), new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(0, 0, 0)
        
    return bytes(pdf.output())


def gateway_bt(n, w, r, lk, lg, t):
    """
    Compuerta transaccional centralizada de almacenamiento y ruteo a Google Sheets.
    Declarada a nivel raíz para mitigar errores de orden y NameErrors.
    """
    st.divider()
    c1, c2, c3 = st.columns(3)
    vld = bool(n.strip()) and bool(w.strip())
    with c1:
        if st.button(t["btn_save"], type="primary", use_container_width=True):
            if not vld: st.error(t["err_fields"])
            else:
                guardar_en_google_sheets(st.session_state.audiencia_activa, n, w, r, "TK_10M", lk)
                st.session_state.nombre_usuario_persistente = n
                st.session_state.whatsapp_usuario_persistente = w
                st.session_state.resultados_usuario_persistente = r
                st.session_state.es_modo_likert_persistente = lk
                st.session_state.flujo_finalized = True
                st.rerun()
    with c2:
        if vld:
            pdf_bytes = generar_pdf_diagnostico(n, w, r, st.session_state.audiencia_activa, lk, lg)
            st.download_button(t["btn_pdf"], data=pdf_bytes, file_name="Reporte.pdf", mime="application/pdf", use_container_width=True)
        else: st.info(t["fields_msg"])
    with c3:
        if vld:
            tel = "".join(c for c in str(w) if c.isdigit() or c == '+')
            wa_lnk = f"https://whatsapp.com{tel}&text=Completado"
            st.markdown(f'<a href="{wa_lnk}" target="_blank" style="text-decoration:none;"><div style="background-color:#25d366;color:white;padding:10px;border-radius:4px;text-align:center;font-weight:bold;">💬 WHATSAPP</div></a>', unsafe_allow_html=True)
# =================================================================
# PARTE 8: CONTROL CENTRAL, CREDENCIALES Y HOJA DE ESTILOS CSS FLOTANTE
# =================================================================
def main():
    if "estructuras_inicializadas" not in st.session_state: st.session_state.estructuras_inicializadas = False
    if "audiences_custom_list" not in st.session_state: st.session_state.audiences_custom_list = []
    if "audiencia_activa" not in st.session_state: st.session_state.audiencia_activa = "🍊 Salud Integral"
    if "admin_autenticado" not in st.session_state: st.session_state.admin_autenticado = False
    if "flujo_finalizado" not in st.session_state: st.session_state.flujo_finalizado = False
    if "paso_salud" not in st.session_state: st.session_state.paso_salud = False
    if "paso_cyk" not in st.session_state: st.session_state.paso_cyk = False
    if "oficina_maximizada" not in st.session_state: st.session_state.oficina_maximizada = False

    iso = st.query_params.get("lang", "es")
    if iso not in ["es", "en"]: iso = "es"
    tx = CENTRO_MANDO_BILINGUE.get(iso, CENTRO_MANDO_BILINGUE["es"])
    es_cel = str(st.query_params.get("modo_admin", "true")).strip().lower() == "false"
    ocultar_bar_css = es_cel and not st.session_state.admin_autenticado

    with st.sidebar:
        st.markdown("## 🔐 Autenticación")
        if not st.session_state.admin_autenticado:
            p_in = st.text_input("Contraseña Ponente:", type="password", key="p_master")
            if st.button("🔓 Acceder a la Consola Master", use_container_width=True):
                if p_in == st.secrets.get("credentials", {}).get("password_ponente", "mandarina2026"):
                    st.session_state.admin_autenticado = True
                    st.rerun()
                else: st.error("Acceso denegado.")
        else:
            st.success("Ponente Autenticado")
            tabla_analizar = st.selectbox("Base de Datos Activa:", ["🍊 Salud Integral", "Docentes", "🏭 Sector Secundario"] + st.session_state.audiences_custom_list, key="sb_an")
            if st.button("🔒 Cerrar Oficina Analítica", use_container_width=True):
                st.session_state.admin_autenticado = False
                st.rerun()

    if ocultar_bar_css: st.markdown("<style>div[data-testid='stSidebar'] {display: none !important;}</style>", unsafe_allow_html=True)

    # REGLAS ESTÉTICAS DE LA VENTANA FLOTANTE ADMINISTRATIVA INDEPENDIENTE
    if st.session_state.admin_autenticado:
        h_float = "90vh" if st.session_state.oficina_maximizada else "55vh"
        w_float = "95%" if st.session_state.oficina_maximizada else "80%"
        
        st.markdown(f"""
            <style>
            .floating-office-window {{
                position: fixed; top: 5vh; left: 10%; width: {w_float}; height: {h_float};
                background-color: white; border: 3px solid #ff6b35; border-radius: 12px;
                z-index: 999999; box-shadow: 0px 10px 30px rgba(0,0,0,0.3);
                padding: 20px; overflow-y: auto;
            }}
            .window-header-bar {{
                display: flex; justify-content: space-between; align-items: center;
                background-color: #ff6b35; padding: 10px; margin: -20px -20px 20px -20px;
                border-top-left-radius: 8px; border-top-right-radius: 8px; color: white;
            }}
            </style>
        """, unsafe_allow_html=True)


# =================================================================
# PARTE 9: MARCO DE CONSOLA WINDOWS CON IFRAMES INTEGRADOS (PARTE A)
# =================================================================
def renderizar_consola_windows(tabla_analizar):
    if "win_minimizado" not in st.session_state: 
        st.session_state.win_minimizado = False

    if st.session_state.win_minimizado:
        c_reabrir1, c_reabrir2 = st.columns(2)
        with c_reabrir2:
            if st.button("🗗 Restaurar Consola Analítica", type="primary", use_container_width=True, key="btn_restore_win_master"):
                st.session_state.win_minimizado = False
                st.rerun()
        return

    h_float = "90vh" if st.session_state.oficina_maximizada else "55vh"
    w_float = "95%" if st.session_state.oficina_maximizada else "80%"
    l_float = "2.5%" if st.session_state.oficina_maximizada else "10%"
    t_float = "5vh" if st.session_state.oficina_maximizada else "10vh"

    st.markdown(f"""<style>
        .floating-office-window {{
            position: fixed; top: {t_float}; left: {l_float}; width: {w_float}; height: {h_float};
            background-color: white; border: 2px solid #1e3c72; border-radius: 6px;
            z-index: 999999; box-shadow: 0px 15px 40px rgba(0,0,0,0.4); padding: 20px; overflow-y: auto;
        }}
        .windows-header-bar {{
            display: flex; justify-content: space-between; align-items: center;
            background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); padding: 8px 14px; margin: -20px -20px 20px -20px;
            border-top-left-radius: 4px; border-top-right-radius: 4px; color: white; font-family: 'Segoe UI', sans-serif; cursor: move; user-select: none;
        }}
    </style>""", unsafe_allow_html=True)

    st.markdown("""<script>
        setTimeout(function() {
            var wEl = window.parent.document.querySelector('.floating-office-window');
            var hEl = window.parent.document.querySelector('.windows-header-bar');
            if (hEl && wEl) {
                var isDrag = false; var ox, oy;
                hEl.addEventListener('mousedown', function(e) { isDrag = true; ox = e.clientX - wEl.getBoundingClientRect().left; oy = e.clientY - wEl.getBoundingClientRect().top; });
                window.parent.document.addEventListener('mousemove', function(e) { if (isDrag) { wEl.style.left = (e.clientX - ox) + 'px'; wEl.style.top = (e.clientY - oy) + 'px'; wEl.style.position = 'fixed'; } });
                window.parent.document.addEventListener('mouseup', function() { isDrag = false; });
            }
        }, 1000);
    </script>""", unsafe_allow_html=True)

    with st.container():
        st.markdown(f'<div class="floating-office-window"><div class="windows-header-bar"><div id="win_title_drag">💻 🔬 CONSOLA CIENTÍFICA — AUDIENCIA: {tabla_analizar}</div></div>', unsafe_allow_html=True)
        c_wb1, c_wb2, c_wb3 = st.columns(3)
        with c_wb1:
            if st.button("➖ Minimizar [ _ ]", key="btn_win_min_nav", use_container_width=True):
                st.session_state.win_minimizado = True
                st.rerun()
        with c_wb2:
            txt_sz = "🗗 Restaurar [ 🗗 ]" if st.session_state.oficina_maximizada else "🗖 Maximizar [ 🗖 ]"
            if st.button(txt_sz, key="btn_win_max_nav", use_container_width=True):
                st.session_state.oficina_maximizada = not st.session_state.oficina_maximizada
                st.rerun()
        with c_wb3:
            if st.button("✕ Cerrar Consola [ X ]", key="btn_win_close_nav", use_container_width=True):
                st.session_state.admin_autenticado = False
                st.rerun()

        sheet = conectar_google_sheets(tabla_analizar)
        todas_las_filas = sheet.get_all_values() if sheet else []
        
        if todas_las_filas and len(todas_las_filas) >= 2:
            df_doc = pd.DataFrame(todas_las_filas[1:], columns=todas_las_filas)
            col_reactivos = [c for c in df_doc.columns if str(c).startswith("R")]
            t1, t2, t3 = st.tabs(["👥 Módulo I: Macrorregiones", "👤 Módulo II: CRM Clínico", "📐 Módulo III: SVD & Alpha"])
            
            with t1:
                st.dataframe(df_doc, use_container_width=True)
                pdf_m1 = FPDF()
                pdf_m1.add_page()
                pdf_m1.set_font("Helvetica", "B", 14)
                pdf_m1.cell(190, 10, f"COHORT REPORT: {tabla_analizar}".encode('ascii','ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT", align="C")
                b64_m1 = base64.b64encode(bytes(pdf_m1.output())).decode("utf-8")
                st.markdown(f'<iframe src="data:application/pdf;base64,{b64_m1}" width="100%" height="300px" style="border:1px solid #ddd;"></iframe>', unsafe_allow_html=True)
                st.download_button("📥 DESCARGAR REPORTE MACRO (PDF)", data=bytes(pdf_m1.output()), file_name="Macro.pdf", mime="application/pdf", key="dl_m1_f", use_container_width=True)
# =================================================================
# PARTE 10-A CORREGIDA Y PURGADA: MÓDULOS CRM, SVD Y ALFA (SIN COLISIONES)
# =================================================================
            with t2:
                if "Nombre" in df_doc.columns:
                    sujeto_sel = st.selectbox("Selecciona Participante:", df_doc["Nombre"].unique().tolist(), key="sb_suj_central_w")
                    fila_sujeto = df_doc[df_doc["Nombre"] == sujeto_sel].iloc
                    pdf_m2 = FPDF()
                    pdf_m2.add_page()
                    pdf_m2.set_font("Helvetica", "B", 14)
                    pdf_m2.cell(190, 10, f"CLINICAL REPORT: {sujeto_sel}".encode('ascii','ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT", align="C")
                    b64_m2 = base64.b64encode(bytes(pdf_m2.output())).decode("utf-8")
                    st.markdown(f'<iframe src="data:application/pdf;base64,{b64_m2}" width="100%" height="300px" style="border:1px solid #ddd;"></iframe>', unsafe_allow_html=True)
                        
                    c_crm1, c_crm2 = st.columns(2)
                    with c_crm1:
                          st.download_button("📥 EXPORTAR EXPEDIENTE (PDF)", data=bytes(pdf_m2.output()), file_name="Clinical.pdf", mime="application/pdf", key="btn_dl_m2_pdf", use_container_width=True)
                    with c_crm2:
                          tel_crm = "".join(c for c in str(fila_sujeto.get('WhatsApp', '')) if c.isdigit() or c == '+')
                          st.markdown(f'<a href="https://whatsapp.com{tel_crm}&text=Hola" target="_blank" style="text-decoration:none;"><div style="background-color:#25d366;color:white;padding:10px;border-radius:4px;text-align:center;font-weight:bold;">💬 ENVIAR WHATSAPP CRM</div></a>', unsafe_allow_html=True)
                else:
                    st.info("Columna Nombre ausente.")

            with t3:
                  alfa_calc, s1, s2 = 0.0, 0.0, 0.0
                    if len(df_doc) >= 3 and len(col_reactivos) >= 2:
                       matriz_num = df_doc[col_reactivos].apply(pd.to_numeric, errors='coerce').fillna(3).to_numpy()
                       K = matriz_num.shape
                       var_items = np.var(matriz_num, ddof=1, axis=0)
                       var_total = np.var(np.sum(matriz_num, axis=1), ddof=1)
                       if var_total > 0 and K > 1:
                           alfa_calc = (K / (K - 1)) * (1 - (np.sum(var_items) / var_total))
                       matriz_centrada = matriz_num - np.mean(matriz_num, axis=0)
                       _, S, _ = np.linalg.svd(matriz_centrada, full_matrices=False)
                       s1 = S if len(S) > 0 else 0.0
                       s2 = S if len(S) > 1 else 0.0
                        
                       st.metric("📐 Alfa de Cronbach", f"{alfa_calc:.3f}")
                       col_svd1, col_svd2 = st.columns(2)
                       col_svd1.metric("Componente Latente 1", f"{s1:.2f}")
                       col_svd2.metric("Componente Latente 2", f"{s2:.2f}")
                        
                       pdf_m3 = FPDF()
                       pdf_m3.add_page()
                       pdf_m3.set_font("Helvetica", "B", 14)
                       pdf_m3.cell(190, 10, "DOCTORAL PSYCHOMETRIC VALIDATION REPORT", new_x="LMARGIN", new_y="NEXT", align="C")
                       b64_m3 = base64.b64encode(bytes(pdf_m3.output())).decode("utf-8")
                       st.markdown(f'<iframe src="data:application/pdf;base64,{b64_m3}" width="100%" height="300px" style="border:1px solid #ddd;"></iframe>', unsafe_allow_html=True)
                       st.download_button("📥 EXPORTAR PSICOMETRÍA (PDF)", data=bytes(pdf_m3.output()), file_name="Validation.pdf", mime="application/pdf", key="btn_dl_m3_pdf", use_container_width=True)
                     else:
                         st.info("Se requieren al menos 3 registros completos para activar los cálculos factoriales.")
                       st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.info("Se requieren al menos 3 registros completos.")
                 st.markdown("</div>", unsafe_allow_html=True)

    # Invocación condicional de la capa flotante administrativa superior
    if st.session_state.admin_autenticado:
        renderizar_consola_windows(tabla_analizar)

    # =================================================================
    # PARTE 10-B2: INTERFAZ EN RED SECUENCIAL AUTOMÁTICA DEL PARTICIPANTE
    # =================================================================
    if not st.session_state.flujo_finalizado:
        st.title("🏆 DIAGNÓSTICO DE LA SALUD INTEGRAL Y MODELOS TEMPORALES CRONOS Y KAIRÓS")
        st.divider()
        st.header(r"📋 Sección I: Perfil de identificación")
        nombre = st.text_input(tx.get("nombre", "Nombre:"), key=r"n_in_seq")
        whatsapp = st.text_input(tx.get("wha", "WhatsApp:"), key=r"w_in_seq")
        resultados_totales = {}
        
        st.subheader(r"📋 Sección II: Datos Demográficos y Geográficos")
        resultados_totales["Edad"] = st.number_input(tx.get("edad", "Edad:"), 10, 100, 20, key=r"num_ed")
        resultados_totales["Género"] = st.radio(tx.get("genero", "Género:"), ["Masculino / Male", "Femenino / Female", "Otro / Other"], index=None, horizontal=True, key=r"rad_g")
        resultados_totales["Nacionalidad"] = st.radio(tx.get("nac", "Nacionalidad:"), ["Mexicana", "Extranjera"], index=None, horizontal=True, key=r"rad_n")
        
        if resultados_totales["Nacionalidad"] == "Mexicana":
            resultados_totales["Estado Origen"] = st.selectbox("Estado de origen:", [""] + ESTADOS_MEXICO, key=r"s_orig")
            resultados_totales["Estado Residencia"] = st.selectbox("Estado de residencia actual:", [""] + ESTADOS_MEXICO, key=r"s_res")
        elif resultados_totales["Nacionalidad"] == "Extranjera":
            resultados_totales["País Origen"] = st.text_input("País de Origen:", key=r"t_pais")
            resultados_totales["Continente Extranjero"] = st.selectbox("Continente:", ["", "América", "Europa", "Asia", "África", "Oceanía"], key=r"s_cont")

        st.subheader(r"📋 Sección III: Conocimiento sobre el tema")
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

        vld_base = all([nombre.strip(), whatsapp.strip(), resultados_totales["Género"], resultados_totales["Nacionalidad"], resultados_totales["C1_Escuchado"], resultados_totales["C6_Perfil_Auto"]])
        if vld_base and not st.session_state.paso_salud:
            if st.button("📊 Generar el Diagnóstico de la Salud Integral", use_container_width=True, type="primary"):
                st.session_state.paso_salud = True
                st.rerun()

        if st.session_state.paso_salud:
            st.markdown("### 🍊 Diagnóstico de la Salud Integral")
            MATRIZ_SINTOMAS_FIJA = {
                "💪 Salud Física": ["Fatiga ocupacional crónica", "Trastornos del ciclo del sueño", "Rigidez por sedentarismo", "Descuido en nutrición homeostática"],
                "🧠 Salud Mental": ["Bloqueo cognitivo extremo", "Rumiación mental prolongada", "Sobrecarga informativa/Infoxicación", "Disminución del foco analítico"],
                "❤️ Salud Emocional": ["Agotamiento emocional (Burnout)", "Irritabilidad/Reactividad interpersonal", "Desmotivación vocacional aguda", "Cuadros intermitentes de ansiedad"],
                "👥 Salud Social": ["Aislamiento relacional preventivo", "Fricciones o conflictos frecuentes", "Ausencia de redes de contención", "Dificultad para marcar límites"],
                "💰 Salud Económica": ["Estrés presupuestal agudo", "Pasivos que rebasan la liquidez", "Ausencia de fondo de contingencia", "Dependencia de una única fuente"],
                "⏳ Salud Temporal": ["Procrastinación reactiva sistémica", "Invasión horaria en tiempo libre", "Supresión de márgenes de descanso", "Desequilibrio métrico Cronos/Kairós"],
                "🙏 Salud Espiritual": ["Vacío Existencial and Vocacional", "Desconexión Interna Profunda", "Pérdida del Propósito Esencial", "Abandono de Hábitos Devocionales"]
            }
            for g_idx, (g_name, lista_items_gajo) in enumerate(MATRIZ_SINTOMAS_FIJA.items()):
                with st.container(border=True):
                    st.markdown(f"#### {g_name}")
                    c_a, c_b = st.columns(2)
                    with c_a:
                        cb0 = st.checkbox(lista_items_gajo, key=f"cs_{g_idx}_0")
                        cb1 = st.checkbox(lista_items_gajo, key=f"cs_{g_idx}_1")
                    with c_b:
                        cb2 = st.checkbox(lista_items_gajo, key=f"cs_{g_idx}_2")
                        cb3 = st.checkbox(lista_items_gajo, key=f"cs_{g_idx}_3")
                    resultados_totales[g_name] = [str(i) for i, v in enumerate([cb0, cb1, cb2, cb3]) if v]

            if not st.session_state.paso_cyk:
                if st.button("🎯 Generar Diagnóstico de Modelos Temporales Cronos y Kairós", use_container_width=True, type="primary"):
                    st.session_state.paso_cyk = True
                    st.rerun()

            if st.session_state.paso_cyk:
                st.markdown("### 📋 Sección IV: Batería de Reactivos C&K Adaptativos")
                reactivos = algoritmo_generar_reactivos_poliglotas(resultados_totales, iso)
                for r_id, r_txt in reactivos.items():
                    st.write(f"Reactivo {r_id}: {r_txt}")
                    # Inyección síncrona exacta de la matriz numérica Likert del 1 al 5
                    resultados_totales[f"R{r_id}"] = st.radio(
                        "Escala / Scale:", 
                        options=, 
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
        st.download_button(tx.get("btn_pdf", "📥 Descargar"), data=rep, file_name="Reporte_Psicometrico.pdf", mime="application/pdf", use_container_width=True)

# Guardia de ejecución final a ras del margen izquierdo reglamentario
if __name__ == "__main__":
    main()
