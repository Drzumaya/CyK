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
# PARTE 2A: CONSTANTES GLOBALES Y CONFIGURACIÓN GENERATIVA BILINGÜE
# =================================================================
NOMBRE_HOJA_CALCULO = "Base_Datos_Modelo_Mandarina"
URL_PRODUCCION = "https://dsimandarina.streamlit.app"
ESTADOS_MEXICO = ["Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Chiapas", "Chihuahua", "Coahuila", "Colima", "Ciudad de México", "Durango", "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", "México", "Michoacán", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"]

DIMENSIONES_MANDARINA_MAESTRAS = [
    "💪 Salud Física", "🧠 Salud Mental", "❤️ Salud Emocional", 
    "👥 Salud Social", "💰 Salud Económica", "⏳ Salud Temporal", "🙏 Salud Espiritual"
]

@st.cache_data(show_spinner=False)
def motor_generativo_items_audiencia(nombre_audiencia, lang_code="es"):
    """
    Algoritmo Ontológico Generativo Bilingüe Estático. Produce una matriz de 4 vulnerabilidades
    contextualizadas sin requerir llamadas externas de red (Inmune a Rate-Limits).
    """
    audiencia_limpia = str(nombre_audiencia).strip().lower()
    es_generico = audiencia_limpia in ["", "salud integral", "🍊 salud integral", "general"]
    
    # Semillas semánticas estáticas en Español
    semillas_es = {
        "física": ["Fatiga Ocupacional por Desgaste", "Trastornos del Ciclo del Sueño", "Sedentarismo Musculoesquelético", "Descuido en Nutrición Homeostática"],
        "mental": ["Saturación y Bloqueo Cognitivo", "Rumiación Mental Prolongada", "Sobrecarga de Datos Críticos", "Apatía y Disminución del Foco"],
        "emocional": ["Síndrome de Burnout Latente", "Irritabilidad Reactiva Excesiva", "Desmotivación Vocacional", "Inestabilidad Anímica y Ansiedad Aguda"],
        "social": ["Aislamiento Relacional Preventivo", "Conflictos de Interacción", "Falta de Red de Contención", "Ausencia de Límites Asertivos"],
        "económica": ["Estrés Presupuestal Agudo", "Desorden Financiero o Deudas", "Falta de Fondo de Emergencia", "Ausencia de Diversificación de Ingresos"],
        "temporal": ["Procrastinación por Sobrecarga", "Invasión Horaria Laboral", "Ausencia de Margen de Descanso", "Desequilibrio Muestral Cronos/Kairós"],
        "espiritual": ["Vacío Existencial y Vocacional", "Desconexión Interna Profunda", "Pérdida del Propósito Esencial", "Abandono de Hábitos Devocionales"]
    }

    # Semillas semánticas estáticas en Inglés
    semillas_en = {
        "física": ["Occupational Fatigue from Wear", "Sleep Cycle Disorders", "Musculoskeletal Sedentary State", "Neglect in Homeostatic Nutrition"],
        "mental": ["Cognitive Saturation and Blockage", "Prolonged Mental Rumination", "Critical Data Overload", "Apathy and Decreased Focus"],
        "emocional": ["Latent Burnout Syndrome", "Excessive Reactive Irritability", "Vocational Demotivation", "Instability and Acute Anxiety"],
        "social": ["Preventive Relational Isolation", "Interaction Conflicts", "Lack of Containment Network", "Absence of Assertive Boundaries"],
        "económica": ["Acute Budgetary Stress", "Financial Disorder or Debts", "Lack of Emergency Fund", "Absence of Income Diversification"],
        "temporal": ["Procrastination due to Overload", "Work Hours Invasion", "Absence of Rest Margin", "Imbalance Metric Chronos/Kairos"],
        "espiritual": ["Latent Existential Void", "Deep Internal Disconnection", "Loss of Essential Purpose", "Abandonment of Devotional Habits"]
    }
    
    matriz_salida = {}
    claves_limpias = ["física", "mental", "emocional", "social", "económica", "temporal", "espiritual"]
    emojis = ["💪", "🧠", "❤️", "👥", "💰", "⏳", "🙏"]
    
    banco = semillas_es if lang_code == "es" else semillas_en
    suffix = "en Contexto" if lang_code == "es" else "in Context of"
    
    for i, dim_es in enumerate(DIMENSIONES_MANDARINA_MAESTRAS):
        clave = claves_limpias[i]
        items_base = banco[clave]
        
        dim_limpia = dim_es[2:].strip()
        dim_traducida = dim_limpia if lang_code == "es" else ["Physical Health", "Mental Health", "Emotional Health", "Social Health", "Economic Health", "Temporal Health", "Spiritual Health"][i]
        cabecera_final = f"{emojis[i]} {dim_traducida}"
        
        if es_generico:
            matriz_salida[cabecera_final] = items_base
        else:
            matriz_salida[cabecera_final] = [
                f"{items_base} {suffix} {nombre_audiencia}",
                f"{items_base} {suffix} {nombre_audiencia}",
                f"{items_base} {suffix} {nombre_audiencia}",
                f"{items_base} {suffix} {nombre_audiencia}"
            ]
            
    return matriz_salida

# =================================================================
# PARTE 2B: DICCIONARIO DE DICTAMEN E INTERPRETACIÓN BILINGÜE
# =================================================================
# =================================================================
# VERIFICACIÓN DE LLAVES DENTRO DE TU FRACCIÓN 1 (AL INICIO DEL ARCHIVO)
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
        
        # 🍊 VALIDACIÓN DOCTORAL: Asegúrate de que estas dos líneas existan aquí
        "btn_save": "💾 Guardar Diagnóstico y Procesar",
        "btn_pdf": "DESCARGAR EN PDF 📥",
        
        "thanks": "¡Diagnóstico Completado con Éxito! 🎉",
        "thanks_sub": "Hemos compilado tu reporte individual multilingüe. Descárgalo abajo.",
        "toast_msg": "Descarga del reporte disponible en el panel inferior.",
        # ... resto de tus llaves en español ...
    },
    "en": {
        "intl_title": "🌐 Internationalization Gateway / Polyglot Control",
        "intl_select": "Select tu Idioma Objetivo / Select Language:",
        "intl_btn": "🔄 APLICAR IDIOMA SELECCIONADO / APPLY LANGUAGE",
        "nombre": "Full Name / Nombre Completo:",
        "wha": "WhatsApp or Cellphone (With country code, e.g. +1):",
        "err_fields": "🚨 Please, fill in all required fields.",
        "fields_msg": "💡 Enter Name and WhatsApp to enable the download resource.",
        
        # 🍊 VALIDACIÓN DOCTORAL: Asegúrate de que estas dos líneas existan aquí en inglés
        "btn_save": "💾 Save Diagnosis and Process Data",
        "btn_pdf": "DOWNLOAD PDF REPORT 📥",
        
        "thanks": "Diagnosis Successfully Completed! 🎉",
        "thanks_sub": "We have compiled your individual multilingual report. Download it below.",
        "toast_msg": "Report download is now available in the bottom panel.",
        # ... resto de tus llaves en inglés ...
    }
}


TEXTOS_DICTAMEN_BILINGUE = {
    "es": {
        "ctrl_f0": "Vectores de Atencion Critica Detectados",
        "ctrl_f1": "Dimension Evaluada",
        "ctrl_f2": "Indicadores de vulnerabilidad reportados",
        "ctrl_f3": "Significado del constructo",
        "ctrl_f4": "Directriz de intervencion sugerida",
        "ctrl_f5": "Canalizacion y Seguimiento de Caso",
        "ctrl_f6": "Nota Clinica. El ecosistema analizado se encuentra en un estado funcional optimo. No se registraron indicadores de riesgo.",
        "lbl_interpretacion": "Interpretación de Constructo y Perfil Dominante",
        "lbl_sugerencias_ck": "Recomendaciones de Acompañamiento Metodológico",
        "txt_ck_recom": "Optimizar la simbiosis entre el tiempo métrico (Cronos) y el tempo de oportunidad (Kairós) es vital para reducir la fatiga cognitiva. Se sugiere acudir con el ponente para una asesoría estratégica.",
        "txt_p_simbiosis": "Simbiosis Temporal Equilibrada (C&K): Balanceas la precisión cronométrica con la agilidad adaptativa de ventanas de oportunidad. Sugerencia: Mantén bloques fijos para tareas repetitivas y reserva un margen diario para imprevistos.",
        "txt_p_kairos": "Perfil Temporal Kairótico Puro (Adaptativo): Destacas capturando oportunidades en caliente, pero corres el riesgo de descuidar hitos administrativos organizacionales fijos. Sugerencia: Desarrolla anclajes operativos con alarmas digitales estrictas.",
        "txt_p_cronos": "Perfil Temporal Cronocéntrico Puro (Rígido): Posees una rigidez estructural alta. Experimentas estrés cuando los checklists sufren alteraciones imprevistas. Sugerencia: Entrena la tolerancia a la incertidumbre.",
        "msg_apoyo_frecuencias": "El auto-reporte es el primer paso en la detección de vulnerabilidades institucionales. Se extiende una invitación cordial para contactar directamente al ponente para coordinar una consulta privada.",
        "lbl_ref1": "Hair, J. F., Black, W. C., Babin, B. J., & Anderson, R. E. (2019). Multivariate data analysis (8th ed.). Cengage Learning.",
        "lbl_ref2": "Kline, R. B. (2023). Principles and practice of structural equation modeling (5th ed.). Guilford Press.",
        "lbl_ref3": "Norris, J. R. (1998). Markov chains. Cambridge University Press.",
        "💪 Salud Física": "Sugerencia Corporal: Fija descansos e hidratación. Planifica colaciones balanceadas y realiza activación física regular.",
        "🧠 Salud Mental": "Sugerencia Cognitiva: Aplica pausas de silencio mental y desconexión digital de pantallas entre jornadas.",
        "❤️ Salud Emocional": "Sugerencia Anímica: Implementa ejercicios de respiración diafragmática consciente y externaliza emociones.",
        "👥 Salud Social": "Sugerencia Relacional: Aprende a decir 'no' asertivamente y agenda una actividad fija con tu núcleo cercano.",
        "💰 Salud Económica": "Sugerencia Financiera: Automatiza la separación de un fondo de contingencia básico y suprime gastos hormiga.",
        "⏳ Salud Temporal": "Sugerencia Temporal: Usa bloques de tiempo fijos y reserva intencionalmente un 20% de margen libre diario.",
        "🙏 Salud Espiritual": "Sugerencia Existencial: Dedica minutos del día a la meditación, oración y alineación con tus valores esenciales."
    },
    "en": {
        "ctrl_f0": "Critical Attention Vectors Detected",
        "ctrl_f1": "Evaluated Dimension",
        "ctrl_f2": "Vulnerability indicators reported by user",
        "ctrl_f3": "Construct meaning and implications",
        "ctrl_f4": "Suggested strategic intervention guideline",
        "ctrl_f5": "Case Channeling and Clinical Follow-up",
        "ctrl_f6": "Clinical Note. The analyzed ecosystem is in an optimal functional state. No risk indicators were recorded.",
        "lbl_interpretacion": "Construct Interpretation and Dominant Profile",
        "lbl_sugerencias_ck": "Methodological Accompaniment Recommendations",
        "txt_ck_recom": "Optimizing the symbiosis between metric time (Cronos) and opportunity time (Kairos) is vital to reduce cognitive fatigue. It is suggested to contact the speaker for strategic advice.",
        "txt_p_simbiosis": "Balanced Temporal Symbiosis (C&K): You balance chronometric precision with the adaptive agility of windows of opportunity. Suggestion: Keep fixed blocks for repetitive tasks and reserve daily margin for contingencies.",
        "txt_p_kairos": "Pure Kairotic Temporal Profile (Adaptive): You excel at capturing opportunities on the spot, but risk neglecting fixed organizational milestones. Suggestion: Develop operational anchors with strict digital alarms.",
        "txt_p_cronos": "Pure Chronocentric Temporal Profile (Rigid): You possess high structural rigidity. You experience stress when checklists suffer unexpected changes. Suggestion: Train uncertainty tolerance.",
        "msg_apoyo_frecuencias": "Self-report is the first step in detecting institutional vulnerabilities. A cordial invitation is extended to contact the speaker directly to coordinate a private consultation.",
        "lbl_ref1": "Hair, J. F., Black, W. C., Babin, B. J., & Anderson, R. E. (2019). Multivariate data analysis (8th ed.). Cengage Learning.",
        "lbl_ref2": "Kline, R. B. (2023). Principles and practice of structural equation modeling (5th ed.). Guilford Press.",
        "lbl_ref3": "Norris, J. R. (1998). Markov chains. Cambridge University Press.",
        "💪 Salud Física": "Physical Suggestion: Fix rest and hydration anchors, plan high-density nutritional snacks, and perform regular metabolic activation.",
        "🧠 Salud Mental": "Cognitive Suggestion: Restrict screen exposure through digital fasting windows and program absolute silence breaks between blocks.",
        "❤️ Salud Emocional": "Emotional Suggestion: Externalize overload indicators with your trusted networks and implement conscious diaphragmatic breathing.",
        "👥 Salud Social": "Social Suggestion: Train assertive establishment of operational boundaries and intentionally safeguard time for your close core.",
        "💰 Salud Económica": "Financial Suggestion: Automate channeling a base percentage into a shielded emergency fund and suppress impulse spending.",
        "⏳ Salud Temporal": "Temporal Suggestion: Synchronize your immovable blocks on the clock grid, intentionally reserving a 20% free margin daily.",
        "🙏 Salud Espiritual": "Spiritual Suggestion: Dedicate the first minutes of your day to deep introspection, prayer, or meditation on your essential values."
    }
}


# =================================================================
# PARTE 3: CONECTORES TRANSACCIONALES DE ALMACENAMIENTO DIRECTO
# =================================================================

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
# =================================================================
# ALGORITMO INTEGRAL: GENERADOR DE REACTIVOS C&K ADAPTATIVO POR IA (FIX)
# =================================================================
def algoritmo_generar_reactivos_poliglotas(nombre_audiencia, lang="es"):
    """
    Genera inductivamente la batería de 10 reactivos Cronos y Kairós
    acoplándolos de forma automática al nicho o audiencia creada por el ponente.
    """
    aud = str(nombre_audiencia).strip()
    
    if lang == "en":
        return {
            1: f"I optimize my high-impact goals specifically tailored for {aud}.",
            2: f"I structure my daily schedule based on the exact clock metrics required for {aud}.",
            3: f"Time flows organically when I manage administrative tasks in {aud}.",
            4: f"I strictly penalize professional untimeliness within the {aud} workspace.",
            5: f"I read unexpected events as highly useful windows of opportunity for {aud}.",
            6: f"I rigidly execute and manage performance goals under fixed checklists in {aud}.",
            7: f"I break the set itinerary immediately if a strategic advantage emerges for {aud}.",
            8: f"I prefer a sequential, structured order over multitasking when operating in {aud}.",
            9: f"I trigger high cognitive concentration if the environment changes rapidly in {aud}.",
            10: f"I protect fixed, unnegotiable hours for rest and production as part of {aud}."
        }
    else:
        return {
            1: f"Optimizo mis metas de alto impacto específicamente diseñadas para {aud}.",
            2: f"Estructuro mi agenda diaria sobre las métricas de reloj exactas requeridas en {aud}.",
            3: f"El tiempo fluye de forma orgánica cuando gestiono tareas administrativas en {aud}.",
            4: f"Castigo severamente la impuntualidad profesional dentro del entorno de {aud}.",
            5: f"Leo los imprevistos como ventanas de oportunidad altamente útiles para {aud}.",
            6: f"Ejecuto y gestiono metas de rendimiento bajo checklists fijos de forma rígida en {aud}.",
            7: f"Rompo el itinerario establecido de inmediato si emerge una ventaja estratégica para {aud}.",
            8: f"Prefiero un orden secuencial y estructurado sobre la multitarea al operar en {aud}.",
            9: f"Activo una alta concentración cognitiva si el entorno cambia rápidamente en {aud}.",
            10: f"Separo horas fijas e innegociables de sueño y producción como miembro de {aud}."
        }



def generar_pdf_diagnostico(nombre, whatsapp, resultados, tabla, es_likert=False, lang="es"):
    pdf = FPDF()
    pdf.core_fonts_encoding = "cp1252"
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    font_family = "Helvetica"
    
    # Sincronización estática con el Centro de Mando Bilingüe
    tx_pdf = CENTRO_MANDO_BILINGUE.get(lang, CENTRO_MANDO_BILINGUE["es"])
    dictamen_bilingue = TEXTOS_DICTAMEN_BILINGUE.get(lang, TEXTOS_DICTAMEN_BILINGUE["es"])
    
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
        # Recuperación de la matriz ontológica dinámica estática sin APIs de red
        g_trad = motor_generativo_items_audiencia(tabla, lang_code=lang)
        
        for idx, dim_traducida_emoji in enumerate(g_trad.keys()):
            if len(resultados.get(DIMENSIONES_MANDARINA_MAESTRAS[idx], [])) > 0:
                key_segura = str(dim_traducida_emoji).encode('cp1252', 'ignore').decode('cp1252')
                for emj in ["💪", "🧠", "❤️", "👥", "💰", "⏳", "🙏"]: 
                    key_segura = key_segura.replace(emj, "")
                    
                pdf.set_font(font_family, "B", 11)
                pdf.cell(190, 6, key_segura.strip(), new_x="LMARGIN", new_y="NEXT")
                
                # Inyección descriptiva de las alertas calculadas dinámicamente por IA
                indices_marcados = resultados.get(DIMENSIONES_MANDARINA_MAESTRAS[idx], [])
                sintomas_origen_nicho = list(g_trad.values())[idx]
                sintomas_reportados = [sintomas_origen_nicho[int(i)] for i in indices_marcados if int(i) < len(sintomas_origen_nicho)]
                
                pdf.set_font(font_family, "I", 9.5)
                pdf.set_text_color(100, 100, 100)
                pdf.multi_cell(190, 4.5, str(", ".join(sintomas_reportados)).encode('cp1252', 'ignore').decode('cp1252'), new_x="LMARGIN", new_y="NEXT")
                
                # Directriz clínica fija indexada de contención
                glosario_seguro = str(dictamen_bilingue.get(DIMENSIONES_MANDARINA_MAESTRAS[idx], "")).encode('cp1252', 'ignore').decode('cp1252')
                
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
        pdf.cell(190, 6, str(dictamen_bilingue.get("lbl_interpretacion", "Interpretacion")).encode('ascii', 'ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT")
        
        dif = abs(avg_c - avg_k)
        if dif <= 0.4: txt_p = dictamen_bilingue.get("txt_p_simbiosis")
        elif avg_k > avg_c: txt_p = dictamen_bilingue.get("txt_p_kairos")
        else: txt_p = dictamen_bilingue.get("txt_p_cronos")
            
        pdf.set_font(font_family, "", 10)
        pdf.multi_cell(190, 5, str(txt_p).encode('cp1252', 'ignore').decode('cp1252'), new_x="LMARGIN", new_y="NEXT")
        
    return bytes(pdf.output())

    # =================================================================
    # PARTE 5B: ENTORNO MULTILINGÜE, CUESTIONARIOS Y CONTROL DE EXPOSICIÓN
    # =================================================================
    if "mostrar_bateria" not in st.session_state:
        st.session_state.mostrar_bateria = True

    interruptor_movil = es_cel
    
    if not st.session_state.flujo_finalizado:
        with st.container(border=True):
            st.markdown(f"### {tx.get('intl_title', '🌐 Control Poliglota')}")
            dict_ids = {"spanish": "es", "english": "en"}
            sel_v = st.selectbox(tx.get("intl_select", "Idioma:"), options=["Spanish", "English"], index=0 if iso == "es" else 1, key="sb_part_lang_unq")
            if st.button(tx.get("intl_btn", "Aplicar"), key="btn_apply_lang_master_fixed"):
                iso_f = dict_ids.get(str(sel_v).lower().strip(), "en")
                st.query_params["lang"] = iso_f
                st.session_state.idioma_activo_actual = iso_f
                if "tx_traducido_cache" in st.session_state: del st.session_state["tx_traducido_cache"]
                st.rerun()

        if not interruptor_movil:
            with st.container(border=True):
                st.markdown(f"### {tx.get('qr_title', '📢 Proyección QR')}")
                qr = qrcode.QRCode(version=1, box_size=10, border=4)
                qr.add_data(lnk_qr)
                qr.make(fit=True)
                buf_qr = BytesIO()
                qr.make_image(fill_color="black", back_color="white").save(buf_qr, format="PNG")
                st.image(buf_qr.getvalue(), width=260, caption=tx.get('qr_sub1', 'Escanea'))

        txt_toggle = "🙈 OCULTAR CUESTIONARIO ADAPTATIVO" if st.session_state.mostrar_bateria else "👁️ MOSTRAR CUESTIONARIO PARA EXPLICAR"
        if st.button(txt_toggle, type="secondary", use_container_width=True, key="btn_toggle_visibility_bateria_master"):
            st.session_state.mostrar_bateria = not st.session_state.mostrar_bateria
            st.rerun()

        st.header(f"📋 {st.session_state.audiencia_activa}")
        nombre = st.text_input(tx.get("nombre", "Nombre:"), key="n_in")
        whatsapp = st.text_input(tx.get("wha", "WhatsApp:"), key="w_in")
        es_likert = st.session_state.audiencia_activa != "🍊 Salud Integral"
        
        resultados_totales = {}
        
        if st.session_state.mostrar_bateria:
            if not es_likert:
                st.write(tx.get("mand_title", "### 🍊 Diagnóstico"))
                gajos = motor_generativo_items_audiencia(st.session_state.audiencia_activa, iso)
                for g_idx, (g_name, lista_items_gajo) in enumerate(gajos.items()):
                    with st.container(border=True):
                        st.markdown(f"#### {g_name}")
                        col_a, col_b = st.columns(2)
                        with col_a:
                            t0 = lista_items_gajo if len(lista_items_gajo) > 0 else "S0"
                            t1 = lista_items_gajo if len(lista_items_gajo) > 1 else "S1"
                            cb0 = st.checkbox(t0, key=f"c_{g_idx}_0_f")
                            cb1 = st.checkbox(t1, key=f"c_{g_idx}_1_f")
                        with col_b:
                            t2 = lista_items_gajo if len(lista_items_gajo) > 2 else "S2"
                            t3 = lista_items_gajo if len(lista_items_gajo) > 3 else "S3"
                            cb2 = st.checkbox(t2, key=f"c_{g_idx}_2_f")
                            cb3 = st.checkbox(t3, key=f"c_{g_idx}_3_f")
                        resultados_totales[g_name] = [str(i) for i, v in enumerate([cb0, cb1, cb2, cb3]) if v]
            else:
                # 📋 SECCIÓN II: DATOS DEMOGRÁFICOS Y GEOGRÁFICOS REALES
                st.subheader("📋 Sección II: Datos Demográficos y Geográficos")
                resultados_totales["Edad"] = st.number_input(tx.get("edad", "Edad:"), 10, 100, 20)
                resultados_totales["Género"] = st.radio(tx.get("genero", "Género:"), ["Masculino / Male", "Femenino / Female", "Otro / Other"], horizontal=True)
                resultados_totales["Nacionalidad"] = st.radio(tx.get("nac", "Nacionalidad:"), ["Mexicana", "Extranjera"], horizontal=True, key="nacionalidad_unq_choice")
                
                if "mex" in resultados_totales["Nacionalidad"].lower():
                    resultados_totales["Estado Origen"] = st.selectbox("4. Estado mexicano de origen:", [""] + ESTADOS_MEXICO, key="sel_origen_mex_unq")
                    resultados_totales["Estado Residencia"] = st.selectbox("5. Estado mexicano de residencia actual:", [""] + ESTADOS_MEXICO, key="sel_residencia_mex_unq")
                    resultados_totales["País Origen"] = "México"
                    resultados_totales["Continente Extranjero"] = "América"
                else:
                    resultados_totales["País Origen"] = st.text_input("País de Origen / Country of Origin:", key="txt_pais_origen_extranjero")
                    resultados_totales["Continente Extranjero"] = st.selectbox("6. Para extranjeros: Continente de Origen:", ["", "América", "Europa", "Asia", "África", "Oceanía"], key="sel_continente_extranjero_unq")
                    resultados_totales["Estado Origen"] = "N/A"
                    resultados_totales["Estado Residencia"] = "N/A"
                                                  # 📋 SECCIÓN III: CONOCIMIENTO SOBRE EL TEMA (RESTAURADO EXACTO)
                st.subheader("📋 Sección III: Conocimiento sobre el tema")
                
                k1_txt = "1. Antes de esta encuesta ya había escuchado hablar sobre los Modelos Temporales Cronos y Kairós" if iso == "es" else "1. Before this survey, I had already heard about the Cronos and Kairos Temporal Models"
                k2_txt = "2. He leído sobre los modelos temporales Cronos y Kairós" if iso == "es" else "2. I have read about the Cronos and Kairos temporal models"
                k3_txt = "3. He enseñado alguna vez sobre los modelos temporales Cronos y Kairós" if iso == "es" else "3. I have ever taught about the Cronos and Kairos temporal models"
                k4_txt = "4. El modelo temporal:" if iso == "es" else "4. The temporal model:"
                k5_txt = "5. Hablar de modelos temporales es hablar de:" if iso == "es" else "5. Talking about temporal models means talking about:"
                k6_txt = "6. Soy persona:" if iso == "es" else "6. I am a person:"

                k4_opts = ["Se impone", "Se hereda", "No sé"] if iso == "es" else ["Is imposed", "Is inherited", "I don't know"]
                k5_opts = ["Teología", "Cultura", "Francamente no sé"] if iso == "es" else ["Theology", "Culture", "Frankly I don't know"]
                k6_opts = ["Cronos", "Kairós", "No sé"] if iso == "es" else ["Cronos", "Kairos", "I don't know"]

                resultados_totales["C1_Escuchado"] = st.radio(k1_txt, ["Sí / Yes", "No"], horizontal=True, key="rad_kn1_unq_sec3")
                resultados_totales["C2_Leído"] = st.radio(k2_txt, ["Sí / Yes", "No"], horizontal=True, key="rad_kn2_unq_sec3")
                resultados_totales["C3_Enseñado"] = st.radio(k3_txt, ["Sí / Yes", "No"], horizontal=True, key="rad_kn3_unq_sec3")
                resultados_totales["C4_Origen"] = st.radio(k4_txt, k4_opts, horizontal=True, key="rad_kn4_unq_sec3")
                resultados_totales["C5_Concepto"] = st.radio(k5_txt, k5_opts, horizontal=True, key="rad_kn5_unq_sec3")
                resultados_totales["C6_Perfil_Auto"] = st.radio(k6_txt, k6_opts, horizontal=True, key="rad_kn6_unq_sec3")
                
                # 📋 SECCIÓN IV: BATERÍA DE REACTIVOS PSICOMÉTRICOS ADAPTATIVOS C&K
                st.subheader("📋 Sección IV: Batería de Reactivos C&K Adaptativos")
                reactivos = algoritmo_generar_reactivos_poliglotas(st.session_state.audiencia_activa, iso)
                for r_id, r_txt in reactivos.items():
                    st.write(f"Reactivo {r_id}: {r_txt}")
                    resultados_totales[f"R{r_id}"] = st.radio("Escala / Scale:", options=[1, 2, 3, 4, 5], format_func=lambda x: tx.get(f"likert_{x}", str(x)), horizontal=True, key=f"r_{r_id}_unq_active")

        gateway_bt(nombre, whatsapp, resultados_totales, es_likert, iso, tx)
    else:
        st.balloons()
        st.success(tx.get("thanks", "¡Completado!"))
        st.markdown(tx.get("thanks_sub", "Descarga tu reporte abajo."))
        st.toast(tx.get("toast_msg", "Descarga lista."), icon="📥")
        
        rep = generar_pdf_diagnostico(st.session_state.get("nombre_usuario_persistente", "Participante"), st.session_state.get("whatsapp_usuario_persistente", ""), st.session_state.get("resultados_usuario_persistente", {}), st.session_state.audiencia_activa, st.session_state.get("es_modo_likert_persistente", False), iso)
        st.download_button(tx.get("btn_pdf", "📥 Descargar"), data=rep, file_name="Reporte_Psicometrico.pdf", mime="application/pdf", use_container_width=True)
        
        if st.button("🔄 Volver al Diagnóstico Principal", key="btn_reset_view_final_mando"): 
            st.session_state.flujo_finalizado = False
            st.rerun()

    # --- INVESTIGACIÓN ALTA ANALÍTICA DEL PONENTE ---
    if st.session_state.admin_autenticado and not es_cel:
        st.markdown("---")
        st.header(tx.get("lbl_titulo_aud", "🔬 Oficina Analítica"))
        tabla_analizar = st.selectbox(tx.get("lbl_tabla_select", "Tabla:"), ["🍊 Salud Integral", "Docentes", "🏭 Sector Secundario"], key="sb_tabla_analizar_master_office")
        sheet = conectar_google_sheets(tabla_analizar)
        todas_las_filas = sheet.get_all_values() if sheet else []
        if todas_las_filas and len(todas_las_filas) >= 2:
            df_doc = pd.DataFrame(todas_las_filas[1:], columns=todas_las_filas[0])
            st.subheader(tx.get("lbl_crm_buscar", "Buscar"))
            c_busq = st.text_input(tx.get("lbl_crm_input", "Filtro:"), key="crm_search_input").strip().lower()
            if c_busq and not df_doc.empty:
                st.write(df_doc[df_doc[df_doc.columns].astype(str).str.lower().str.contains(c_busq)])
            else:
                st.dataframe(df_doc)

        if st.button(tx.get("lbl_btn_auditoria", "📊 Auditoría"), key="btn_run_doctoral_macro"):
            pdf_auditoria = FPDF()
            pdf_auditoria.add_page()
            pdf_auditoria.set_font("Helvetica", "B", 14)
            pdf_auditoria.cell(190, 10, str(tx.get("lbl_pdf_dictamen", "DICTAMEN")).encode('ascii','ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT", align="C")
            pdf_auditoria.ln(6)
            pdf_auditoria.set_font("Helvetica", "B", 12)
            pdf_auditoria.cell(190, 7, str(tx.get("lbl_pdf_ref_title", "Referencias")).encode('ascii','ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT")
            pdf_auditoria.set_font("Helvetica", "", 9)
            
            dc_bil_local = TEXTOS_DICTAMEN_BILINGUE.get(iso, TEXTOS_DICTAMEN_BILINGUE["es"])
            for ref_key in ["lbl_ref1", "lbl_ref2", "lbl_ref3"]:
                txt_bib = dc_bil_local.get(ref_key, "Hair, J. F., Black, W. C. (2019).")
                pdf_auditoria.multi_cell(190, 4.5, str(txt_bib).encode('cp1252','ignore').decode('cp1252'), new_x="LMARGIN", new_y="NEXT")
                pdf_auditoria.ln(2)
            st.download_button(label=tx.get("lbl_btn_download_macro", "📥 DESCARGAR"), data=bytes(pdf_auditoria.output()), file_name="Dictamen_Doctoral.pdf", mime="application/pdf", key="btn_download_admin_macro_report")

# Cierre reglamentario de la aplicación a nivel raíz (Sin sangrías iniciales)
if __name__ == "__main__": 
    main()

