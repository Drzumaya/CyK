# BEGIN: PARTE 1
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
# END: PARTE 1
# BEGIN: PARTE 2
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
# END: PARTE 2
# BEGIN: PARTE 3
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
# END: PARTE 3
# BEGIN: PARTE 4
def conectar_google_sheets(nombre_tabla):
    """
    Establece conexión encriptada de alta seguridad con la API de Google Sheets.
    CORREGIDO: Usa los scopes oficiales de Spreadsheets y Drive para evitar el error 404.
    """
    try:
        # Extrae las credenciales de la bóveda de secretos de Streamlit
        credenciales_dict = dict(st.secrets["gcp_service_account"])
        
        # Sanitiza los saltos de línea de la clave privada de forma síncrona
        if "private_key" in credenciales_dict:
            raw_key = credenciales_dict["private_key"]
            credenciales_dict["private_key"] = raw_key.replace("\\n", "\n").strip()

        # CORREGIDO: Direcciones URL exactas requeridas por Google Cloud Platform
        scope = [
            "https://googleapis.com",
            "https://googleapis.com"
        ]
        
        credenciales = Credentials.from_service_account_info(credenciales_dict, scopes=scope)
        cliente = gspread.authorize(credenciales)
        
        # Conexión síncrona con la hoja de cálculo maestra unificada
        libro = cliente.open_by_key("1y99f_7hGv_3mUeE4K_1m49wB7r0V4oW3mDeR4_m49pQ")
        return libro.worksheet(nombre_tabla)
    except Exception as e:
        st.sidebar.error(f"Error de conexión en Google Cloud: {e}")
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
    except Exception as e:
        st.sidebar.error(f"Error al escribir fila en base de datos: {e}")
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
            "🙏 Salud Espiritual": ["Vacío Existencial y Vocacional", "Desconexión Interna Profunda", "Pérdida del Propósito Esencial", "Abandono de Habits Devocionales"]
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
# END: PARTE 4
# BEGIN: PARTE 5
def algoritmo_generar_reactivos_poliglotas(datos_participante, lang="es"):
    """
    Genera la batería de 10 reactivos C&K en primera persona, adaptando 
    el estilo semántico según edad, género y conocimiento previo del usuario.
    Ítems impares = Cronos | Pares = Kairós.
    """
    edad_raw = datos_participante.get("Edad", 30)
    edad = int(edad_raw) if str(edad_raw).isdigit() else 30
    
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
                10: "Mantengo la calma y la claridad analítica cuando todo a mi alrededor cambia rápidamente."
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
# END: PARTE 5
# BEGIN: PARTE 6
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
    pdf.cell(190, 10, str(base_title).encode('cp1252', 'ignore').decode('cp1252'), ln=1, align="C")
    pdf.ln(2)
    
    pdf.set_font(font_family, "", 10)
    n_seg = str(nombre).encode('ascii', 'ignore').decode('ascii') if nombre else "Anonimo"
    w_seg = str(whatsapp).encode('ascii', 'ignore').decode('ascii') if whatsapp else "N/A"
    pdf.cell(190, 6, f"Participante: {n_seg} | Contacto: {w_seg}".encode('cp1252', 'ignore').decode('cp1252'), ln=1)
    pdf.ln(4)
    
    if not es_likert:
        g_trad = motor_generativo_items_audiencia(tabla, lang_code=lang)
        for idx, dim_espanol in enumerate(DIMENSIONES_MANDARINA_MAESTRAS):
            indices_marcados = resultados.get(dim_espanol, [])
            
            if len(indices_marcados) > 0:
                dim_traducida_emoji = list(g_trad.keys())[idx]
                key_segura = str(dim_traducida_emoji).encode('cp1252', 'ignore').decode('cp1252')
                for emj in ["💪", "🧠", "❤️", "👥", "💰", "⏳", "🙏"]: 
                    key_segura = key_segura.replace(emj, "")
                
                pdf.set_font(font_family, "B", 11)
                pdf.cell(190, 6, f"Dimension: {key_segura.strip()}", ln=1)
                
                sintomas_origen_nicho = list(g_trad.values())[idx]
                sintomas_reportados = [sintomas_origen_nicho[int(i)] for i in indices_marcados if str(i).isdigit() and int(i) < len(sintomas_origen_nicho)]
                
                pdf.set_font(font_family, "I", 9.5)
                pdf.set_text_color(120, 30, 30)
                pdf.multi_cell(190, 4.5, f"Indicadores detectados: {', '.join(sintomas_reportados)}".encode('cp1252', 'ignore').decode('cp1252'))
                
                glosario_seguro = str(dictamen_bilingue.get(dim_espanol, "")).encode('cp1252', 'ignore').decode('cp1252')
                pdf.set_font(font_family, "", 9.5)
                pdf.set_text_color(50, 50, 50)
                pdf.multi_cell(190, 4.5, f"Sugerencia base: {glosario_seguro.strip()}")
                
                if "⏳" in dim_espanol or "temporal" in dim_espanol.lower():
                    pdf.ln(1)
                    pdf.set_font(font_family, "B", 9.5)
                    pdf.set_text_color(150, 50, 0)
                    pdf.cell(190, 5, "ANALISIS DE RIESGO PROSPECTIVO Y CONSECUENCIAS:", ln=1)
                    pdf.set_font(font_family, "", 9)
                    pdf.set_text_color(60, 60, 60)
                    
                    c_corto = "- Corto Plazo: Elevacion de fatiga cognitiva, saturacion horaria y perdida de ventanas de oportunidad."
                    c_medio = "- Mediano Plazo: Sindrome de Burnout latente, desequilibrio en dinamicas familiares and friccion operacional."
                    c_largo = "- Largo Plazo: Cronificacion del estres, colapso de efectividad y perdida del proposito estrategico vocacional."
                    pdf.multi_cell(190, 4, c_corto.encode('cp1252','ignore').decode('cp1252'))
                    pdf.multi_cell(190, 4, c_medio.encode('cp1252','ignore').decode('cp1252'))
                    pdf.multi_cell(190, 4, c_largo.encode('cp1252','ignore').decode('cp1252'))
                    
                    pdf.ln(1)
                    pdf.set_font(font_family, "B", 9.5)
                    pdf.set_text_color(180, 0, 0)
                    r_esp = "RECOMENDACION CRITICA: Debido al nivel de riesgo detectado en tu vector dimensional temporal, es indispensable solicitar una consulta especializada de forma directa con el ponente."
                    pdf.multi_cell(190, 4.5, r_esp.encode('cp1252','ignore').decode('cp1252'))
                pdf.ln(3)
                pdf.set_text_color(0, 0, 0)
# END: PARTE 6
# BEGIN: PARTE 7
    else:
        c_v = [int(resultados.get(f"R{i}", 3)) for i in range(1, 11, 2)]
        k_v = [int(resultados.get(f"R{i}", 3)) for i in range(2, 11, 2)]
        avg_c = sum(c_v) / 5 if len(c_v) > 0 else 3.0
        avg_k = sum(k_v) / 5 if len(k_v) > 0 else 3.0
        
        pdf.set_font(font_family, "B", 11)
        pdf.cell(190, 6, "1. RESULTADOS DE LA EVALUACION CUANTITATIVA", ln=1)
        pdf.set_font(font_family, "", 10)
        pdf.cell(190, 5, f"Media Vector Cronos: {avg_c:.2f} | Media Vector Kairos: {avg_k:.2f}".encode('cp1252','ignore').decode('cp1252'), ln=1)
        pdf.ln(3)
        
        pdf.set_font(font_family, "B", 11)
        pdf.cell(190, 6, "2. APARTADO DE ANALISIS Y PERFIL DOMINANTE", ln=1)
        dif = abs(avg_c - avg_k)
        if dif <= 0.4: txt_p = dictamen_bilingue.get("txt_p_simbiosis", "Simbiosis")
        elif avg_k > avg_c: txt_p = dictamen_bilingue.get("txt_p_kairos", "Dominancia Kairos")
        else: txt_p = dictamen_bilingue.get("txt_p_cronos", "Dominancia Cronos")
            
        pdf.set_font(font_family, "I", 10)
        pdf.multi_cell(190, 5, str(txt_p).encode('cp1252', 'ignore').decode('cp1252'))
        pdf.ln(3)
        
        pdf.set_font(font_family, "B", 11)
        pdf.cell(190, 6, "3. PROSPECTIVA DE RIESGO TEMPORAL Y CONSECUENCIAS", ln=1)
        if avg_c > avg_k:
            r_c_corto = "- Corto Plazo: Incremento agudo de rigidez mental, estres ante imprevistos cotidianos."
            r_c_medio = "- Mediano Plazo: Perdida sistemica de ventanas de oportunidad (Kairos) por apego al reloj."
            r_c_largo = "- Largo Plazo: Obsolescencia adaptativa y colapso de la plasticidad cognitiva estructural."
        else:
            r_c_corto = "- Corto Plazo: Desorden administrativo inmediato, desalineacion de plazos obligatorios."
            r_c_medio = "- Mediano Plazo: Perdida de credibilidad profesional institucional por impuntualidad."
            r_c_largo = "- Largo Plazo: Crisis de estabilidad familiar e incapacidad de consolidar proyectos."
            
        pdf.multi_cell(190, 5, r_c_corto.encode('cp1252','ignore').decode('cp1252'))
        pdf.multi_cell(190, 5, r_c_medio.encode('cp1252','ignore').decode('cp1252'))
        pdf.multi_cell(190, 5, r_c_largo.encode('cp1252','ignore').decode('cp1252'))
        pdf.ln(3)
        
        pdf.set_font(font_family, "B", 11)
        pdf.cell(190, 6, "4. RECOMENDACIONES METODOLÓGICAS DE CONTENCION", ln=1)
        gl_recom = str(dictamen_bilingue.get("txt_ck_recom", "Ajustar franjas")).encode('cp1252', 'ignore').decode('cp1252')
        pdf.multi_cell(190, 5, gl_recom)
        pdf.ln(2)
        
        pdf.set_font(font_family, "B", 10)
        pdf.set_text_color(180, 0, 0)
        req_ponente = "ATENCION DIRECTA: Al tratarse de una asimetria dimensional temporal, se le recomienda al participante agendar una consulta especializada de caracter personal o familiar con el ponente."
        pdf.multi_cell(190, 4.5, req_ponente.encode('cp1252','ignore').decode('cp1252'))
        pdf.set_text_color(0, 0, 0)
        
    pdf_output = pdf.output()
    return bytes(pdf_output) if not isinstance(pdf_output, bytes) else pdf_output


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
            tel = "".join(c for c in str(w) if c.isdigit())
            wa_lnk = f"https://wa.me{tel}?text=He%20completado%20mi%20Evaluaci%C3%B3n%20Psicom%C3%A9trica"
            st.markdown(f'<a href="{wa_lnk}" target="_blank" style="text-decoration:none;"><div style="background-color:#25d366;color:white;padding:10px;border-radius:4px;text-align:center;font-weight:bold;">💬 WHATSAPP</div></a>', unsafe_allow_html=True)
# END: PARTE 7
# BEGIN: PARTE 8
def main():
    if "estructuras_inicializadas" not in st.session_state: st.session_state.estructuras_inicializadas = True
    if "audiences_custom_list" not in st.session_state: st.session_state.audiences_custom_list = []
    if "audiencia_activa" not in st.session_state: st.session_state.audiencia_activa = "🍊 Salud Integral"
    if "admin_autenticado" not in st.session_state: st.session_state.admin_autenticado = False
    if "flujo_finalized" not in st.session_state: st.session_state.flujo_finalized = False
    if "paso_salud" not in st.session_state: st.session_state.paso_salud = False
    if "paso_cyk" not in st.session_state: st.session_state.paso_cyk = False

    iso = st.query_params.get("lang", "es")
    if iso not in ["es", "en"]: iso = "es"
    tx = CENTRO_MANDO_BILINGUE.get(iso, CENTRO_MANDO_BILINGUE["es"])

    with st.sidebar:
        st.markdown(f"### {tx.get('side_title', '🔐 Panel del Ponente')}")
        if not st.session_state.admin_autenticado:
            with st.form("bloque_autenticacion_ponente"):
                p_in = st.text_input("Contraseña Ponente:", type="password")
                btn_acceso = st.form_submit_button("🔓 Acceder a la Consola Master", use_container_width=True)
                
                if btn_acceso:
                    pwd_seguro = st.secrets.get("credentials", {}).get("password_ponente", "mandarina2026")
                    if p_in == pwd_seguro:
                        st.session_state.admin_autenticado = True
                        st.rerun()
                    else: 
                        st.error("Acceso denegado.")
        else:
            st.success("Ponente Autenticado")
            st.selectbox(
                "Base de Datos Activa:", 
                ["🍊 Salud Integral", "Docentes", "🏭 Sector Secundario"] + st.session_state.audiences_custom_list, 
                key="sb_an"
            )
            
            if st.button("📊 ABRIR OFICINA ANALÍTICA", type="primary", use_container_width=True):
                invocar_consola_modal_nativa(st.session_state.sb_an, iso, tx)
                
            if st.button("🔒 Cerrar Sesión Ponente", use_container_width=True):
                st.session_state.admin_autenticado = False
                st.rerun()

    if st.session_state.admin_autenticado:
        st.sidebar.info("💡 Consola abierta. Puedes volver a invocarla usando el botón superior azul.")
# END: PARTE 8
# BEGIN: PARTE 9
@st.dialog("💻 CONSOLA CIENTÍFICA MASTER — ESTUDIO METODOLÓGICO", width="large")
def invocar_consola_modal_nativa(tabla_analizar, iso, tx):
    st.markdown(f"**Cohorte Activa en Bóveda:** `{tabla_analizar.upper()}`")
    st.divider()

    sheet = conectar_google_sheets(tabla_analizar)
    todas_las_filas = sheet.get_all_values() if sheet else []
    
    if todas_las_filas and len(todas_las_filas) >= 2:
        df_doc = pd.DataFrame(todas_las_filas[1:], columns=todas_las_filas)
        col_reactivos = [c for c in df_doc.columns if str(c).startswith("R")]
        
        st.markdown("""<style>
            .kpi-card-master-modal {
                background: #ffffff; border-top: 3px solid #0f2042; padding: 12px; 
                border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center;
            }
        </style>""", unsafe_allow_html=True)
        
        ejecutar_modulos_analiticos_consola(df_doc, col_reactivos, tabla_analizar, iso, tx)
    else:
        st.warning("⚠️ Se requieren un mínimo de 3 registros transaccionales linealizados en la nube para activar el motor de matrices algebraicas.")
# END: PARTE 9
# BEGIN: PARTE 10-A
def ejecutar_modulos_analiticos_consola(df_doc, col_reactivos, tabla_analizar, iso, tx):
    t1, t2, t3 = st.tabs([
        "📊 MÓDULO I: MACRO-REGIONES", 
        "👤 MÓDULO II: CRM CLÍNICO", 
        "📐 MÓDULO III: ALFA & SVD"
    ])
    
    with t1:
        st.markdown("#### Análisis de la Población de la Cohorte")
        km1, km2, km3 = st.columns(3)
        with km1:
            st.markdown('<div class="kpi-card-master-modal">', unsafe_allow_html=True)
            st.metric("Muestra Registrada", f"{len(df_doc)} Ss", "N Total")
            st.markdown('</div>', unsafe_allow_html=True)
        with km2:
            st.markdown('<div class="kpi-card-master-modal">', unsafe_allow_html=True)
            p_burnout = 0.0
            if "❤️ Salud Emocional" in df_doc.columns:
                con_b = df_doc["❤️ Salud Emocional"].apply(lambda x: '0' in str(x)).sum()
                p_burnout = (con_b / len(df_doc)) * 100
            st.metric("Fatiga Emocional", f"{p_burnout:.1f}%", "Prevalencia Burnout", delta_color="inverse")
            st.markdown('</div>', unsafe_allow_html=True)
        with km3:
            st.markdown('<div class="kpi-card-master-modal">', unsafe_allow_html=True)
            p_temporal = 0.0
            if "⏳ Salud Temporal" in df_doc.columns:
                con_t = df_doc["⏳ Salud Temporal"].apply(lambda x: len(str(x)) > 2).sum()
                p_temporal = (con_t / len(df_doc)) * 100
            st.metric("Vector Temporal", f"{p_temporal:.1f}%", "Asimetría Activa", delta_color="inverse")
            st.markdown('</div>', unsafe_allow_html=True)

        st.dataframe(df_doc, use_container_width=True)
        
        pdf1 = FPDF()
        pdf1.add_page()
        pdf1.set_margins(20, 20, 20)
        pdf1.set_font("Times", "B", 14)
        pdf1.cell(170, 10, f"COHORT REPORT: {tabla_analizar}".encode('cp1252','ignore').decode('cp1252'), ln=1, align="C")
        pdf_output = pdf1.output()
        bytes_pdf1 = bytes(pdf_output) if not isinstance(pdf_output, bytes) else pdf_output
        b64_1 = base64.b64encode(bytes_pdf1).decode("utf-8")
        
        st.markdown(f'<iframe src="data:application/pdf;base64,{b64_1}" width="100%" height="200px" style="border:1px solid #ddd; border-radius:4px;"></iframe>', unsafe_allow_html=True)
        st.download_button("📥 DESCARGAR REPORTE MACRO (PDF)", data=bytes_pdf1, file_name=f"Macro_Report_{tabla_analizar}.pdf", mime="application/pdf", use_container_width=True)

    with t2:
        st.markdown("#### Ficha Clínica de Diagnóstico Cruzado")
        if "Nombre" in df_doc.columns:
            sujeto_sel = st.selectbox("Selecciona Participante:", df_doc["Nombre"].unique().tolist(), key="sb_suj_modal")
            df_filtrado = df_doc[df_doc["Nombre"] == sujeto_sel]
            
            if not df_filtrado.empty:
                fila_sujeto = df_filtrado.iloc
                perfil_auto = str(fila_sujeto.get("C6_Perfil_Auto", "No sé"))
                
                c_v = [int(fila_sujeto.get(f"R{i}", 3)) for i in range(1, 11, 2) if f"R{i}" in df_doc.columns]
                k_v = [int(fila_sujeto.get(f"R{i}", 3)) for i in range(2, 11, 2) if f"R{i}" in df_doc.columns]
                avg_c = sum(c_v) / 5 if c_v else 3.0
                avg_k = sum(k_v) / 5 if k_v else 3.0
                
                perfil_calc = "Simbiosis" if abs(avg_c - avg_k) <= 0.4 else ("Kairós" if avg_k > avg_c else "Cronos")
                
                cc1, cc2 = st.columns(2)
                with cc1: st.info(f"**Declarado:** Tipo {perfil_auto.upper()}")
                with cc2:
                    if perfil_auto in perfil_calc: st.success(f"**Coherencia:** Alineado ({perfil_calc.upper()})")
                    else: st.warning(f"**Asimetría:** Computado {perfil_calc.upper()}")

                pdf2 = FPDF()
                pdf2.add_page()
                pdf2.set_font("Times", "B", 14)
                pdf2.cell(170, 10, f"CLINICAL EXPEDIENT: {sujeto_sel.upper()}".encode('cp1252','ignore').decode('cp1252'), ln=1, align="C")
                pdf_output_m2 = pdf2.output()
                bytes_pdf2 = bytes(pdf_output_m2) if not isinstance(pdf_output_m2, bytes) else pdf_output_m2
                b64_2 = base64.b64encode(bytes_pdf2).decode("utf-8")
                
                st.markdown(f'<iframe src="data:application/pdf;base64,{b64_2}" width="100%" height="200px" style="border:1px solid #ddd; border-radius:4px;"></iframe>', unsafe_allow_html=True)
                
                c_c1, c_c2 = st.columns(2)
                with c_c1:
                    st.download_button("📥 EXPORTAR EXPEDIENTE INDIVIDUAL (PDF)", data=bytes_pdf2, file_name=f"Clinical_{sujeto_sel}.pdf", mime="application/pdf", use_container_width=True)
                with c_c2:
                    t_c = "".join(c for c in str(fila_sujeto.get('WhatsApp', '')) if c.isdigit())
                    w_u = f"https://wa.me{t_c}?text=Hola%20{urllib.parse.quote(sujeto_sel)}%2C%20se%20ha%20generado%20su%20dictamen."
                    st.markdown(f'<a href="{w_u}" target="_blank" style="text-decoration:none;"><div style="background-color:#25d366;color:white;padding:10px;border-radius:4px;text-align:center;font-weight:bold;">💬 ENVIAR ACCIÓN CRM</div></a>', unsafe_allow_html=True)

    with t3:
        st.markdown("#### Rigor Métrico e Índices Factoriales")
        if len(df_doc) >= 3 and len(col_reactivos) >= 2:
            matriz_num = df_doc[col_reactivos].apply(pd.to_numeric, errors='coerce').fillna(3).to_numpy()
            K = int(matriz_num.shape)
            var_items = np.var(matriz_num, ddof=1, axis=0)
            var_total = np.var(np.sum(matriz_num, axis=1), ddof=1)
            alfa_calc = (K / (K - 1)) * (1 - (np.sum(var_items) / var_total)) if var_total > 0 and K > 1 else 0.0
            
            matriz_centrada = matriz_num - np.mean(matriz_num, axis=0)
            _, S, _ = np.linalg.svd(matriz_centrada, full_matrices=False)
            s1 = S if len(S) > 0 else 0.0
            s2 = S if len(S) > 1 else 0.0
                
            m_c1, m_c2 = st.columns(2)
            with m_c1:
                st.metric("Alfa de Cronbach", f"{alfa_calc:.4f}")
                if alfa_calc >= 0.80: st.success("🟩 Excelente Fiabilidad")
                else: st.warning("🟨 Fiabilidad Básica")
            with m_c2:
                st.metric("Componente Latente 1 (SVD)", f"{s1:.2f}")
                st.metric("Componente Latente 2 (SVD)", f"{s2:.2f}")
                
            pdf3 = FPDF()
            pdf3.add_page()
            pdf3.set_font("Times", "B", 14)
            pdf3.cell(170, 10, "VALIDATION REPORT", ln=1, align="C")
            pdf_output_m3 = pdf3.output()
            bytes_pdf3 = bytes(pdf_output_m3) if not isinstance(pdf_output_m3, bytes) else pdf_output_m3
            b64_3 = base64.b64encode(bytes_pdf3).decode("utf-8")
            
            st.markdown(f'<iframe src="data:application/pdf;base64,{b64_3}" width="100%" height="200px" style="border:1px solid #ddd; border-radius:4px;"></iframe>', unsafe_allow_html=True)
            st.download_button("📥 EXPORTAR REPORTE DE FIABILIDAD (PDF)", data=bytes_pdf3, file_name="Psychometric_Validation.pdf", mime="application/pdf", use_container_width=True)
# END: PARTE 10-A
# BEGIN: PARTE 10-B
    if not st.session_state.flujo_finalized:
        st.markdown(f"### {tx.get('qr_title', '📢 Código de Acceso QR')}")
        st.caption(tx.get("qr_sub1", "Escanea para responder en tiempo real"))
        
        url_qr = f"{URL_PRODUCCION}?lang={iso}"
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(url_qr)
        qr.make(fit=True)
        img_qr = qr.make_image(fill_color="black", back_color="white")
        
        buf_qr = BytesIO()
        img_qr.save(buf_qr, format="PNG")
        st.image(buf_qr.getvalue(), width=180)
        st.divider()

        st.title("🏆 DIAGNÓSTICO DE LA SALUD INTEGRAL Y MODELOS TEMPORALES CRONOS Y KAIRÓS")
        st.divider()
        
        st.header(r"📋 Sección I: Perfil de identificación")
        nombre = st.text_input(tx.get("nombre", "Nombre:"), key=r"n_in_seq")
        whatsapp = st.text_input(tx.get("wha", "WhatsApp:"), key=r"w_in_seq")
        
        if "resultados_totales_registro" not in st.session_state: 
            st.session_state.resultados_totales_registro = {}
        resultados_totales = st.session_state.resultados_totales_registro
        
        st.subheader(r"📋 Sección II: Datos Demográficos y Geográficos")
        edad_in = st.number_input(tx.get("edad", "Edad:"), 10, 100, 20, key=r"num_ed")
        resultados_totales["Edad"] = int(edad_in)
        
        resultados_totales["Género"] = st.radio(tx.get("genero", "Género:"), ["Masculino / Male", "Femenino / Female", "Otro / Other"], index=None, horizontal=True, key=r"rad_g")
        resultados_totales["Nacionalidad"] = st.radio(tx.get("nac", "Nacionalidad:"), ["Mexicana", "Extranjera"], index=None, horizontal=True, key=r"rad_n")
        
        if resultados_totales.get("Nacionalidad") == "Mexicana":
            resultados_totales["Estado Origen"] = st.selectbox("Estado de origen:", [""] + ESTADOS_MEXICO, key=r"s_orig")
            resultados_totales["Estado Residencia"] = st.selectbox("Estado de residencia actual:", [""] + ESTADOS_MEXICO, key=r"s_res")
        elif resultados_totales.get("Nacionalidad") == "Extranjera":
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

        vld_base = all([nombre.strip(), whatsapp.strip(), resultados_totales.get("Género"), resultados_totales.get("Nacionalidad"), resultados_totales.get("C1_Escuchado"), resultados_totales.get("C6_Perfil_Auto")])
        if vld_base and not st.session_state.paso_salud:
            if st.button("📊 Generar el Diagnóstico de la Salud Integral", use_container_width=True, type="primary"):
                st.session_state.paso_salud = True
                st.rerun()

        if st.session_state.paso_salud:
            st.markdown("### 🍊 Diagnóstico de la Salud Integral")
            MATRIZ_SINTOMAS_DINAMICA = motor_generativo_items_audiencia(st.session_state.audiencia_activa, lang_code=iso)
            
            for g_idx, (g_name, lista_items_gajo) in enumerate(MATRIZ_SINTOMAS_DINAMICA.items()):
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
                    st.markdown(f"**Reactivo {r_id}:** {r_txt}")
                    # CORREGIDO: Lista explícita restablecida para garantizar la compilación sin errores
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
        
        n_p = st.session_state.get("nombre_usuario_persistente", "Participante")
        w_p = st.session_state.get("whatsapp_usuario_persistente", "")
        r_p = st.session_state.get("resultados_usuario_persistente", {})
        
        rep = generar_pdf_diagnostico(n_p, w_p, r_p, st.session_state.audiencia_activa, True, iso)
        st.download_button(tx.get("btn_pdf", "📥 Descargar"), data=rep, file_name="Reporte_Psicometrico.pdf", mime="application/pdf", use_container_width=True)

if __name__ == "__main__":
    main()
# END: PARTE 10-B
