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
URL_PRODUCCION = "https://streamlit.app"
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
    if idioma_sel not in ["es", "en"]:
        idioma_sel = "es"
    st.session_state.idioma_activo_actual = idioma_sel

    # Mapeo inmediato y directo sin APIs desde el Centro de Mando Bilingüe
    tx = CENTRO_MANDO_BILINGUE.get(idioma_sel, CENTRO_MANDO_BILINGUE["es"])
    dictamen_bilingue = TEXTOS_DICTAMEN_BILINGUE.get(idioma_sel, TEXTOS_DICTAMEN_BILINGUE["es"])

    # Forzamos la mutación algorítmica exacta cada 10 minutos (600 segundos)
    minuto_bloque_10 = int(time.time() // 600)
    token_tiempo = hashlib.md5(f"mandarina_secret_{minuto_bloque_10}".encode()).hexdigest()[:8]
    
    modo_admin_url = st.query_params.get("modo_admin", "true")
    es_celular_del_publico = str(modo_admin_url).strip().lower() == "false"
    
    if es_celular_del_publico and st.query_params.get("diag_tipo", None): 
        st.session_state.audiencia_activa = st.query_params.get("diag_tipo")

    url_con_token = f"{URL_PRODUCCION}/?token={token_tiempo}&modo_admin=false&diag_tipo={st.session_state.audiencia_activa.replace(' ', '%20')}&lang={idioma_sel}"

    if not st.session_state.estructuras_inicializadas:
        for t in ["🍊 Salud Integral", "Docentes", "🏭 Sector Secundario"]: conectar_google_sheets(t)
        st.session_state.estructuras_inicializadas = True

    with st.sidebar:
        st.markdown(tx.get("side_title", "## 🔐 Control"))
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
    # PARTE 5B: MOTOR DE INTERFAZ INTEGRAL BILINGÜE Y RECONOCIMIENTO
    # =================================================================
    interruptor_movil = es_celular_del_publico

    if not st.session_state.flujo_finalizado:
        with st.container(border=True):
            st.markdown(f"### {tx.get('intl_title')}")
            idioma_seleccionado_combo = st.selectbox(
                tx.get("intl_select"), 
                options=["Spanish", "English"], 
                index=0 if idioma_sel == "es" else 1,
                key="combo_bilingue_universal_unq"
            )
            if st.button(tx.get("intl_btn"), key="disparador_refresco_bilingue_master"):
                st.query_params["lang"] = "es" if "span" in idioma_seleccionado_combo.lower() else "en"
                st.session_state.idioma_activo_actual = st.query_params["lang"]
                st.rerun()

        if not interruptor_movil:
            with st.container(border=True):
                st.markdown(f"### {tx.get('qr_title')}")
                objeto_qr = qrcode.QRCode(version=1, box_size=10, border=4)
                objeto_qr.add_data(url_con_token)
                objeto_qr.make(fit=True)
                buffer_grafico_qr = BytesIO()
                objeto_qr.make_image(fill_color="black", back_color="white").save(buffer_grafico_qr, format="PNG")
                st.image(buffer_grafico_qr.getvalue(), width=260, caption=tx.get('qr_sub1'))

        st.header(f"📋 {st.session_state.audiencia_activa}")
        campo_nombre_usuario = st.text_input(tx.get("nombre"), key="input_nombre_registro_unq")
        campo_whatsapp_usuario = st.text_input(tx.get("wha"), key="input_whatsapp_registro_unq")
        es_modo_formulario_likert = st.session_state.audiencia_activa != "🍊 Salud Integral"
        
        contenedor_variables_analiticas = {}
        if not es_modo_formulario_likert:
            st.write(tx.get("mand_title"))
            diccionario_matriz_ia = motor_generativo_items_audiencia(st.session_state.audiencia_activa, idioma_sel)
            for indice_iteracion_gajo, (nombre_gajo, lista_sintomas_ia) in enumerate(diccionario_matriz_ia.items()):
                with st.container(border=True):
                    st.markdown(f"#### {nombre_gajo}")
                    bloque_columna_izquierda, bloque_columna_derecha = st.columns(2)
                    with bloque_columna_izquierda:
                        casilla_verificacion_0 = st.checkbox(lista_sintomas_ia[0] if len(lista_sintomas_ia)>0 else "S0", key=f"casilla_verif_{indice_iteracion_gajo}_0")
                        casilla_verificacion_1 = st.checkbox(lista_sintomas_ia[1] if len(lista_sintomas_ia)>1 else "S1", key=f"casilla_verif_{indice_iteracion_gajo}_1")
                    with bloque_columna_derecha:
                        casilla_verificacion_2 = st.checkbox(lista_sintomas_ia[2] if len(lista_sintomas_ia)>2 else "S2", key=f"casilla_verif_{indice_iteracion_gajo}_2")
                        casilla_verificacion_3 = st.checkbox(lista_sintomas_ia[3] if len(lista_sintomas_ia)>3 else "S3", key=f"casilla_verif_{indice_iteracion_gajo}_3")
                    contenedor_variables_analiticas[nombre_gajo] = [str(pos) for pos, interruptor_activo in enumerate([casilla_verificacion_0, casilla_verificacion_1, casilla_verificacion_2, casilla_verificacion_3]) if interruptor_activo]
        else:
            st.subheader(tx.get("sec1"))
            contenedor_variables_analiticas["Edad"] = st.number_input(tx.get("edad"), 10, 100, 20)
            contenedor_variables_analiticas["Género"] = st.radio(tx.get("genero"), ["Masculino / Male", "Femenino / Female", "Otro / Other"], horizontal=True)
            contenedor_variables_analiticas["Nacionalidad"] = st.radio(tx.get("nac"), ["Mexicana", "Extranjera"], horizontal=True)
            
            if "mex" in contenedor_variables_analiticas["Nacionalidad"].lower():
                contenedor_variables_analiticas["Estado Residencia"] = st.selectbox(tx.get("res"), [""] + ESTADOS_MEXICO)
                contenedor_variables_analiticas["País Origen"] = "México"
            else: 
                contenedor_variables_analiticas["País Origen"] = st.text_input(tx.get("pais"))
                
            st.subheader(tx.get("sec2"))
            contenedor_variables_analiticas["C1_Escuchado"] = st.radio(tx.get("kn1"), ["Sí / Yes", "No"], horizontal=True)
            contenedor_variables_analiticas["C2_Leído"] = st.radio(tx.get("kn2"), ["Sí / Yes", "No"], horizontal=True)
            contenedor_variables_analiticas["C3_Enseñado"] = st.radio(tx.get("kn3"), ["Sí / Yes", "No"], horizontal=True)
            contenedor_variables_analiticas["C4_Origen"] = st.radio(tx.get("kn4"), [tx.get("kn4_opt0"), tx.get("kn4_opt1"), tx.get("kn4_opt2")], horizontal=True)
            contenedor_variables_analiticas["C5_Concepto"] = st.radio(tx.get("kn5"), [tx.get("kn5_opt0"), tx.get("kn5_opt1"), tx.get("kn5_opt2")], horizontal=True)
            
            st.write("### 📋 BATERÍA DE REACTIVOS C&K")
            diccionario_reactivos_estaticos = algoritmo_generar_reactivos_poliglotas(str(contenedor_variables_analiticas.get("País Origen", "Región")), idioma_sel)
            for id_reactivo_num, texto_reactivo_trad in diccionario_reactivos_estaticos.items():
                st.write(f"Reactivo {id_reactivo_num}: {texto_reactivo_trad}")
                contenedor_variables_analiticas[f"R{id_reactivo_num}"] = st.radio("Escala / Scale:", options=[1, 2, 3, 4, 5], format_func=lambda valor_x: tx.get(f"likert_{valor_x}", str(valor_x)), horizontal=True, key=f"llave_reactivo_radiogroup_{id_reactivo_num}")

        renderizar_botones_transaccionales(campo_nombre_usuario, campo_whatsapp_usuario, contenedor_variables_analiticas, es_modo_formulario_likert, idioma_sel, tx)
    else:
        st.balloons()
        st.success(tx.get("thanks"))
        st.markdown(tx.get("thanks_sub"))
        st.toast(tx.get("toast_msg"), icon="📥")
        
        objeto_archivo_pdf_individual = generar_pdf_diagnostico(st.session_state.get("nombre_usuario_persistente", "Participante"), st.session_state.get("whatsapp_usuario_persistente", ""), st.session_state.get("resultados_usuario_persistente", {}), st.session_state.audiencia_activa, st.session_state.get("es_modo_likert_persistente", False), idioma_sel)
        st.download_button(tx.get("btn_pdf"), data=objeto_archivo_pdf_individual, file_name="Reporte_Psicometrico.pdf", mime="application/pdf", use_container_width=True)
        
        objeto_archivo_diploma_honor = generar_reconocimiento_honorifico_dinamico()
        st.download_button(tx.get("lbl_btn_download_diploma"), data=objeto_archivo_diploma_honor, file_name="Diploma_Excelencia.pdf", mime="application/pdf", use_container_width=True)
        if st.button("🔄 Volver al Diagnóstico Principal", key="reajuste_flujo_vista_principal_bilingue"): 
            st.session_state.flujo_finalizado = False
            st.rerun()

    # --- INVESTIGACIÓN ALTA ANALÍTICA DEL PONENTE ---
    if st.session_state.admin_autenticado and not interruptor_movil:
        st.markdown("---")
        st.header(tx.get("lbl_titulo_aud"))
        tabla_analizar = st.selectbox(tx.get("lbl_tabla_select"), ["🍊 Salud Integral", "Docentes", "🏭 Sector Secundario"], key="selector_analitico_tablas_ponente_unq")
        manejador_pestana_sheets = conectar_google_sheets(tabla_analizar)
        coleccion_filas_matriz = manejador_pestana_sheets.get_all_values() if manejador_pestana_sheets else []
        if coleccion_filas_matriz and len(coleccion_filas_matriz) >= 2:
            data_frame_investigacion = pd.DataFrame(coleccion_filas_matriz[1:], columns=coleccion_filas_matriz[0])
            st.subheader(tx.get("lbl_crm_buscar"))
            criterio_busqueda_crm = st.text_input(tx.get("lbl_crm_input"), key="input_texto_filtro_crm_analisis").strip().lower()
            if criterio_busqueda_crm and not data_frame_investigacion.empty:
                st.write(data_frame_investigacion[data_frame_investigacion[data_frame_investigacion.columns].astype(str).str.lower().str.contains(criterio_busqueda_crm)])

        if st.button(tx.get("lbl_btn_auditoria"), key="ejecutor_compilacion_macro_informe_doctoral"):
            pdf_macro_auditoria = FPDF()
            pdf_macro_auditoria.add_page()
            pdf_macro_auditoria.set_font("Helvetica", "B", 14)
            pdf_macro_auditoria.cell(190, 10, str(tx.get("lbl_pdf_dictamen")).encode('ascii','ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT", align="C")
            pdf_macro_auditoria.ln(6)
            pdf_macro_auditoria.set_font("Helvetica", "B", 12)
            pdf_macro_auditoria.cell(190, 7, str(tx.get("lbl_pdf_ref_title")).encode('ascii','ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT")
            pdf_macro_auditoria.set_font("Helvetica", "", 9)
            for identificador_referencia_key in ["lbl_ref1", "lbl_ref2", "lbl_ref3"]:
                pdf_macro_auditoria.multi_cell(190, 4.5, str(dictamen_bilingue.get(identificador_referencia_key)).encode('cp1252','ignore').decode('cp1252'), new_x="LMARGIN", new_y="NEXT")
                pdf_macro_auditoria.ln(2)
            st.download_button(label=tx.get("lbl_btn_download_macro"), data=bytes(pdf_macro_auditoria.output()), file_name="Dictamen_Doctoral.pdf", mime="application/pdf", key="descarga_final_dictamen_pdf_macro_doctoral")



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
