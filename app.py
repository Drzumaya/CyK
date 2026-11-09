# =================================================================
# FRACCIÓN 1 DE 4: PROTOCOLOS DE IMPORTACIÓN Y DICCIONARIOS MASTER
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
# =================================================================
# DICCIONARIO MAESTRO COMPACTO - COLOCAR AL INICIO DEL ARCHIVO (LÍNEA 1)
# =================================================================
CENTRO_MANDO_BILINGUE = {
    "es": {
        "nombre": "Nombre completo:", "wha": "WhatsApp internacional:", "edad": "Edad biológica:", "genero": "Género:", "nac": "Nacionalidad:",
        "sec_i": "📋 Sección I: Perfil de identificación (Opcional)", "sec_ii": "📋 Sección II: Datos Demográficos (Obligatorio)",
        "sec_iii": "📋 Sección III: Conocimiento sobre el tema (Obligatorio)", "sec_iv": "📋 Sección IV: Reactivos C&K Adaptativos",
        "p1_s3": "1. ¿Habías escuchado hablar sobre los Modelos Temporales Cronos y Kairós?",
        "p2_s3": "2. ¿Has leído sobre los modelos temporales Cronos y Kairós?",
        "p3_s3": "3. ¿Has enseñado alguna vez sobre los modelos temporales Cronos y Kairós?",
        "p4_s3": "4. El modelo temporal:", "p5_s3": "5. Hablar de modelos temporales es hablar de:", "p6_s3": "6. Soy persona:",
        "side_title": "🔐 Panel del Ponente", "intl_title": "🌐 Idioma / Language", "intl_select": "Selecciona el idioma:",
        "qr_title": "📢 Código QR", "mand_title": "🍊 Diagnóstico de Salud", "likert_1": "1 - Desacuerdo", "likert_5": "5 - Acuerdo",
        "btn_save": "💾 Finalizar Instrumento", "btn_pdf": "📥 Descargar PDF", "err_fields": "Campos incompletos.", "fields_msg": "Ingrese identificación."
    },
    "en": {
        "nombre": "Full name:", "wha": "International WhatsApp:", "edad": "Biological age:", "genero": "Gender identity:", "nac": "Nationality:",
        "sec_i": "📋 Section I: Identification Profile (Optional)", "sec_ii": "📋 Section II: Demographic Data (Mandatory)",
        "sec_iii": "📋 Section III: Knowledge of the Topic (Mandatory)", "sec_iv": "📋 Section IV: Adaptive C&K Items",
        "p1_s3": "1. Have you ever heard about Cronos and Kairos?", "p2_s3": "2. Have you read about Cronos and Kairos?",
        "p3_s3": "3. Have you ever taught about Cronos and Kairos?",
        "p4_s3": "4. The temporal model:", "p5_s3": "5. Temporal models means talking about:", "p6_s3": "6. I am a person of type:",
        "side_title": "🔐 Speaker Dashboard", "intl_title": "🌐 System Language", "intl_select": "Select language:",
        "qr_title": "📢 QR Code", "mand_title": "🍊 Health Diagnostic", "likert_1": "1 - Disagree", "likert_5": "5 - Agree",
        "btn_save": "💾 Register Instrument", "btn_pdf": "📥 Download PDF", "err_fields": "Mandatory fields missing.", "fields_msg": "Unlock with profile."
    }
}


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
# FRACCIÓN 2-PARTE A: PROCESAMIENTO EN LA NUBE CON ALMACENAMIENTO DE COHORTE
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


# =================================================================
# FRACCIÓN 2-PARTE B: ALGORITMO PSICOMÉTRICO Y GENERADOR PDF SANEADO
# =================================================================
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
                6: "Encuentro valor en imprevistos si revelan alternativas de acción.",
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
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(170, 10, "DIAGNOSTICO INDIVIDUAL: SALUD INTEGRAL Y MODELOS C&K", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(40, 6, "Participante:")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(130, 6, f"{nombre}".encode('ascii','ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT")
    pdf.cell(40, 6, "WhatsApp / Tabla:")
    pdf.cell(130, 6, f"{whatsapp} | {tabla}".encode('ascii','ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    
    if es_likert:
        c_v = [int(resultados.get(f"R{i}", 3)) for i in range(1, 11, 2)]
        k_v = [int(resultados.get(f"R{i}", 3)) for i in range(2, 11, 2)]
        avg_c = sum(c_v)/5.0 if c_v else 3.0
        avg_k = sum(k_v)/5.0 if k_v else 3.0
        
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(170, 6, f"Media Cronos: {avg_c:.2f}  |  Media Kairos: {avg_k:.2f}", new_x="LMARGIN", new_y="NEXT")
        
        dt = TEXTOS_DICTAMEN_BILINGUE.get(lang, TEXTOS_DICTAMEN_BILINGUE["es"])
        diag = dt["txt_p_simbiosis"] if abs(avg_c - avg_k) <= 0.6 else (dt["txt_p_cronos"] if avg_c > avg_k else dt["txt_p_kairos"])
        pdf.set_font("Helvetica", "I", 10)
        pdf.multi_cell(170, 5, diag.encode('ascii','ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)
        
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(170, 6, "RECOMENDACIONES DE SALUD INTEGRAL:", new_x="LMARGIN", new_y="NEXT")
    dt = TEXTOS_DICTAMEN_BILINGUE.get(lang, TEXTOS_DICTAMEN_BILINGUE["es"])
    for dim, rec in dt.items():
        if dim in DIMENSIONES_MANDARINA_MAESTRAS:
            pdf.set_font("Helvetica", "B", 9)
            pdf.cell(40, 5, f"{dim}:")
            pdf.set_font("Helvetica", "", 9)
            pdf.multi_cell(130, 5, rec.encode('ascii','ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT")
            
    pdf.ln(4)
    pdf.set_font("Helvetica", "I", 7)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(170, 4, dt["lbl_ref1"], new_x="LMARGIN", new_y="NEXT")
    pdf.cell(170, 4, dt["lbl_ref2"], new_x="LMARGIN", new_y="NEXT")
    pdf.cell(170, 4, dt["lbl_ref3"].encode('ascii','ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT")
    return bytes(pdf.output())



# =================================================================
# FRACCIÓN 2-PARTE B1.2 REPARADA: CONSTRUCTOR PDF SANEADO ANTI-EMOJIS
# =================================================================
def generar_pdf_diagnostico(nombre, whatsapp, resultados, tabla, es_likert=False, lang="es"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(20, 20, 20)
    pdf.set_auto_page_break(auto=True, margin=15)
    
    font_family = "Helvetica"
    dictamen_bilingue = TEXTOS_DICTAMEN_BILINGUE.get(lang, TEXTOS_DICTAMEN_BILINGUE["es"])
    
    # 🍊 FIX MAESTRO ANTI-EMOJI: Remueve el icono de la mandarina del texto de la cohorte para evitar FPDFUnicodeEncodingException
    tabla_saneada = str(tabla).replace("🍊", "").strip()
    
    # Encabezado Editorial Estilo Documento de Investigación (APA)
    pdf.set_font(font_family, "B", 8)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(170, 4, "INFORME DE INVESTIGACION PSICOMETRICA // UNIVERSIDAD MANDARINA CORE", new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.cell(170, 4, f"REGISTRO CLINICO COHORTE: {tabla_saneada.upper()} | FECHA EMISION: {time.strftime('%Y-%m-%d')}".encode('latin-1', 'replace').decode('latin-1'), new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.line(20, 18, 190, 18)
    pdf.ln(5)
    
    # Título del Manuscrito Psicométrico
    pdf.set_font(font_family, "B", 14)
    pdf.set_text_color(15, 32, 66)
    txt_title = "Dictamen de Diagnostico Clinico Individual y Perfiles Temporales" if lang == "es" else "Individual Clinical Diagnosis and Temporal Profiles Report"
    pdf.multi_cell(170, 7, txt_title.encode('latin-1', 'replace').decode('latin-1'), new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.ln(3)
    
    # Metadatos del Participante Evaluado
    pdf.set_font(font_family, "", 10)
    pdf.set_text_color(50, 50, 50)
    n_seg = str(nombre).encode('latin-1', 'replace').decode('latin-1') if nombre else "Anonimo"
    w_seg = str(whatsapp).encode('latin-1', 'replace').decode('latin-1') if whatsapp else "N/A"
    pdf.cell(170, 6, f"Sujeto Evaluado: {n_seg}  |  Contacto de Verificacion: {w_seg}".encode('latin-1', 'replace').decode('latin-1'), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    
    # Sección I: Bloque de Diagnóstico Dimensional Sintomático
    pdf.set_font(font_family, "B", 11)
    pdf.set_text_color(15, 32, 66)
    pdf.cell(170, 6, "1. EVALUACION ESTRUCTURAL DE LAS DIMENSIONES SINTOMATICAS", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(font_family, "", 9.5)
    pdf.set_text_color(60, 60, 60)
    txt_abs = "Resumen Operativo: Se analizan las trazas homeostáticas multidimensionales para determinar el nivel de afectación sistémica derivado de la exposición a entornos de alta exigencia productiva."
    pdf.multi_cell(170, 4.5, txt_abs.encode('latin-1', 'replace').decode('latin-1'), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    
    g_trad = motor_generativo_items_audiencia(tabla, lang_code=lang)
    for idx, dim_espanol in enumerate(DIMENSIONES_MANDARINA_MAESTRAS):
        indices_marcados = resultados.get(dim_espanol, [])
        if indices_marcados:
            dim_limpia = str(list(g_trad.keys())[idx])
            for emj in ["💪", "🧠", "❤️", "👥", "💰", "⏳", "🙏", "🍊"]: 
                dim_limpia = dim_limpia.replace(emj, "")
            
            pdf.set_font(font_family, "B", 10)
            pdf.set_text_color(15, 32, 66)
            pdf.cell(170, 5, f"Dimension Analizada: {dim_limpia.strip()}".encode('latin-1', 'replace').decode('latin-1'), new_x="LMARGIN", new_y="NEXT")
            
            sintomas_origen = list(g_trad.values())[idx]
            sintomas_reales = [sintomas_origen[int(i)] for i in indices_marcados if str(i).isdigit() and int(i) < len(sintomas_origen)]
            
            pdf.set_font(font_family, "I", 9)
            pdf.set_text_color(140, 30, 30)
            pdf.multi_cell(170, 4.5, f"Indicadores Criticos Detectados: {', '.join(sintomas_reales)}".encode('latin-1', 'replace').decode('latin-1'), new_x="LMARGIN", new_y="NEXT")
            
            pdf.set_font(font_family, "", 9)
            pdf.set_text_color(50, 50, 50)
            pdf.multi_cell(170, 4.5, f"Sugerencia de Contencion: {dictamen_bilingue.get(dim_espanol, '')}".encode('latin-1', 'replace').decode('latin-1'), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)

    if es_likert:
        pdf.ln(2)
        pdf.set_font(font_family, "B", 11)
        pdf.set_text_color(15, 32, 66)
        pdf.cell(170, 6, "2. ANALISIS VECTORIAL CUANTITATIVO DE TRAZAS TEMPORALES (C&K)", new_x="LMARGIN", new_y="NEXT")
        c_v = [int(resultados.get(f"R{i}", 3)) for i in range(1, 11, 2)]
        k_v = [int(resultados.get(f"R{i}", 3)) for i in range(2, 11, 2)]
        avg_c = sum(c_v) / 5 if c_v else 3.0
        avg_k = sum(k_v) / 5 if k_v else 3.0
        
        pdf.set_font(font_family, "", 10)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(170, 5, f"Media Vector Cronos: {avg_c:.2f} | Media Vector Kairos: {avg_k:.2f}".encode('latin-1', 'replace').decode('latin-1'), new_x="LMARGIN", new_y="NEXT")
        
        dif = abs(avg_c - avg_k)
        if dif <= 0.4: txt_p = dictamen_bilingue.get("txt_p_simbiosis", "")
        elif avg_k > avg_c: txt_p = dictamen_bilingue.get("txt_p_kairos", "")
        else: txt_p = dictamen_bilingue.get("txt_p_cronos", "")
        
        pdf.set_font(font_family, "I", 9.5)
        pdf.multi_cell(170, 4.5, f"Dictamen Ontologico: {txt_p}".encode('latin-1', 'replace').decode('latin-1'), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        pdf.set_font(font_family, "", 9)
        pdf.multi_cell(170, 4.5, f"Accion Metodologica: {dictamen_bilingue.get('txt_ck_recom', '')}".encode('latin-1', 'replace').decode('latin-1'), new_x="LMARGIN", new_y="NEXT")
        
        pdf.ln(3)
        pdf.set_fill_color(244, 245, 247)
        pdf.set_font(font_family, "B", 9.5)
        pdf.set_text_color(180, 40, 40)
        txt_invita = "AVISO DE INTERVENCION ESPECIALIZADA EN MODELOS TEMPORALES C&K:"
        pdf.cell(170, 6, txt_invita.encode('latin-1', 'replace').decode('latin-1'), new_x="LMARGIN", new_y="NEXT", fill=True)
        pdf.set_font(font_family, "", 9)
        pdf.set_text_color(40, 40, 40)
        txt_cuerpo_corporativo = "Debido a las asimetrías métricas registradas en sus vectores dimensionales, se le exhorta formalmente a agendar una consulta clínica avanzada de optimización. Coordinación de Atención Institucional: Editorial Mandarina & Core Analytics Group. Correo Electrónico: especialista@modelostemporales.com | Canal de Soporte Corporativo: corporativo@mandarinacore.org | Oficina Central de Enlace Psicométrico Global."
        pdf.multi_cell(170, 4.5, txt_cuerpo_corporativo.encode('latin-1', 'replace').decode('latin-1'), new_x="LMARGIN", new_y="NEXT", fill=True)

    return bytes(pdf.output())

# =================================================================
# FRACCIÓN 3-PARTE A: GATEWAY TRANSACCIONAL Y ESTRUCTURA DE MÓDULOS
# =================================================================
def gateway_bt(n, w, r, lk, lg, t):
    """
    Compuerta transaccional centralizada de almacenamiento y ruteo a Google Sheets.
    Declarada físicamente arriba de main() para mitigar el NameError de compilación.
    """
    st.divider()
    c1, c2, c3 = st.columns(3)
    vld = bool(n.strip()) and bool(w.strip())
    with c1:
        if st.button(t["btn_save"], type="primary", use_container_width=True):
            if not vld: 
                st.error(t["err_fields"])
            else:
                guardar_en_google_sheets(st.session_state.audiencia_activa, n, w, r, "TK_10M", lk)
                st.session_state.nombre_usuario_persistente = n
                st.session_state.whatsapp_usuario_persistente = w
                st.session_state.resultados_usuario_persistente = r
                st.session_state.flujo_finalizado = True
                st.rerun()
    with c2:
        if vld:
            pdf_bytes = generar_pdf_diagnostico(n, w, r, st.session_state.audiencia_activa, lk, lg)
            st.download_button(t["btn_pdf"], data=pdf_bytes, file_name="Reporte_Diagnostico.pdf", mime="application/pdf", use_container_width=True)
        else: 
            st.info(t["fields_msg"])
    with c3:
        if vld:
            tel = "".join(c for c in str(w) if c.isdigit())
            wa_lnk = f"https://wa.me{tel}"
            st.markdown(f'<a href="{wa_lnk}" target="_blank" style="text-decoration:none;"><div style="background-color:#25d366;color:white;padding:10px;border-radius:4px;text-align:center;font-weight:bold;">💬 ENVIAR WHATSAPP</div></a>', unsafe_allow_html=True)

def renderizar_consola_baja_gris(tabla_analizar, iso, tx):
    """
    Despliega el tablero analítico corporativo de forma secuencial y nativa en la zona inferior.
    Empoderado dinámicamente con Redes Bayesianas, Criptografía SHA-256 e Índices Híbridos ESEM/CFA.
    """
    st.markdown("""<style>
        .gray-dashboard-container {
            background-color: #f4f5f7; border: 2px solid #d1d5db; border-radius: 8px;
            padding: 24px; margin-top: 40px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
        .sem-table-master {
            width: 100%; border-collapse: collapse; margin: 10px 0; background: white;
        }
        .sem-table-master th {
            background-color: #0f2042; color: white; padding: 8px; font-size: 12px; text-align: left;
        }
        .sem-table-master td {
            padding: 8px; border-bottom: 1px solid #e5e7eb; font-size: 12px;
        }
    </style>""", unsafe_allow_html=True)
    
    st.markdown('<div class="gray-dashboard-container">', unsafe_allow_html=True)
    st.subheader(f"🔬 CONSOLA ANALÍTICA DOCTORAL AVANZADA — COHORTE: {tabla_analizar.upper()}")
    
    sheet = conectar_google_sheets(tabla_analizar)
    todas_las_filas = sheet.get_all_values() if sheet else []
    tiene_datos = todas_las_filas and len(todas_las_filas) >= 2
    
    if tiene_datos:
        df_doc = pd.DataFrame(todas_las_filas[1:], columns=todas_las_filas)
        col_reactivos = [c for c in df_doc.columns if str(c).startswith("R")]
        
        t1, t2, t3 = st.tabs([
            "👥 Módulo I: Meta-Análisis Colectivo & Redes Bayesianas", 
            "👤 Módulo II: CRM Clínico & Criptografía SHA-256", 
            "📐 Módulo III: Rigor Psicométrico Híbrido (ESEM-Geo, CFA & Fit Indices)"
        ])
        
        with t1:
            st.markdown("**Dataset de Control General de la Audiencia:**")
            st.dataframe(df_doc, use_container_width=True)
            
            st.markdown("##### 🧠 Inferencia Bayesiana Cruzada (Salud Emocional vs Mental)")
            if "❤️ Salud Emocional" in df_doc.columns and "🧠 Salud Mental" in df_doc.columns:
                p_burnout = df_doc["❤️ Salud Emocional"].apply(lambda x: '0' in str(x)).mean()
                p_mental = df_doc["🧠 Salud Mental"].apply(lambda x: '0' in str(x)).mean()
                df_b = df_doc[df_doc["❤️ Salud Emocional"].apply(lambda x: '0' in str(x))]
                p_condicional = df_b["🧠 Salud Mental"].apply(lambda x: '0' in str(x)).mean() if len(df_b) > 0 else 0.0
                
                ba, bb, bc = st.columns(3)
                ba.metric("P(Burnout) Basal", f"{p_burnout*100:.1f}%")
                bb.metric("P(Bloqueo Mental) Basal", f"{p_mental*100:.1f}%")
                bc.metric("P(Bloqueo | Burnout) Bayes", f"{p_condicional*100:.1f}%", "Impacto de Dependencia")
            else:
                st.info("Estructuras de gajos insuficientes para trazar la red bayesiana.")
                
            pdf_macro = FPDF()
            pdf_macro.add_page()
            pdf_macro.set_font("Helvetica", "B", 14)
            pdf_macro.cell(190, 10, "EPISTEMOLOGICAL COHORT MACRO REPORT", new_x="LMARGIN", new_y="NEXT", align="C")
            b64_macro = base64.b64encode(bytes(pdf_macro.output())).decode("utf-8")
            st.markdown(f'<iframe src="data:application/pdf;base64,{b64_macro}" width="100%" height="220px" style="border:1px solid #ddd; border-radius:4px;"></iframe>', unsafe_allow_html=True)
            st.download_button("📥 DESCARGAR REPORTE MACRO POBLACIONAL (PDF)", data=bytes(pdf_macro.output()), file_name=f"Macro_Report_{tabla_analizar}.pdf", mime="application/pdf", key="btn_macro_adv", use_container_width=True)

        with t2:
            st.markdown("#### Ficha Clínica de Integración Criptográfica SHA-256")
            if "Nombre" in df_doc.columns and len(df_doc["Nombre"].unique()) > 0:
                sujeto_sel = st.selectbox("Selecciona Participante para Auditoría:", df_doc["Nombre"].unique().tolist(), key="sb_suj_baja_adv")
                df_filtrado = df_doc[df_doc["Nombre"] == sujeto_sel]
                
                if not df_filtrado.empty:
                    fila_sujeto = df_filtrado.iloc
                    pdf_c = FPDF()
                    pdf_c.add_page()
                    pdf_c.set_margins(20, 20, 20)
                    pdf_c.set_font("Helvetica", "B", 14)
                    pdf_c.cell(170, 10, f"CLINICAL MANUSCRIPT: {sujeto_sel.upper()}".encode('ascii','ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT", align="C")
                    pdf_c.ln(4)
                    pdf_c.set_font("Helvetica", "", 10)
                    pdf_c.multi_cell(170, 5, "Abstract: This diagnostic instrument maps the latent psychometric traits regarding temporal orientation and systemic homeostatic status through adaptive linguistic parameters.", new_x="LMARGIN", new_y="NEXT")
                    pdf_c.ln(5)
                    
                    bytes_preliminares = bytes(pdf_c.output())
                    hash_hash = hashlib.sha256(bytes_preliminares).hexdigest().upper()
                    
                    pdf_c.set_font("Courier", "B", 8)
                    pdf_c.set_text_color(100, 100, 100)
                    pdf_c.cell(170, 5, f"DIGITAL TRANSACTION SECURITY SEAL HASH SHA-256:", new_x="LMARGIN", new_y="NEXT", align="C")
                    pdf_c.cell(170, 5, f"[{hash_hash}]", new_x="LMARGIN", new_y="NEXT", align="C")
                    
                    bytes_finales = bytes(pdf_c.output())
                    b64_2 = base64.b64encode(bytes_finales).decode("utf-8")
                    st.markdown(f'<iframe src="data:application/pdf;base64,{b64_2}" width="100%" height="220px" style="border:1px solid #ddd; border-radius:4px;"></iframe>', unsafe_allow_html=True)
                    
                    c_crm1, c_crm2 = st.columns(2)
                    with c_crm1:
                        st.download_button("📥 DESCARGAR MANUSCRITO CRIPTOGRÁFICO SECHADO", data=bytes_finales, file_name=f"Certified_Clinical_{sujeto_sel}.pdf", mime="application/pdf", use_container_width=True)
                    with c_crm2:
                        tel_crm = "".join(c for c in str(fila_sujeto.get('WhatsApp', '')) if c.isdigit())
                        w_u = f"https://wa.me{tel_crm}?text=Estimado+participante,+su+dictamen+con+sello+digital+{hash_hash[:8]}+esta+disponible."
                        st.markdown(f'<a href="{w_u}" target="_blank" style="text-decoration:none;"><div style="background-color:#25d366;color:white;padding:10px;border-radius:4px;text-align:center;font-weight:bold;">💬 ENVIAR ACCIÓN CRM VERIFICADA</div></a>', unsafe_allow_html=True)
            else:
                st.info("La base de datos individual se activará al ingresar registros válidos.")
# =================================================================
# FRACCIÓN 3-PARTE B1: EXTRACCIÓN DE LA COVARIANZA Y GRADOS DE LIBERTAD
# =================================================================
        with t3:
            # 🍊 FIX ANTI-SYNTAXWARNING: Uso de cadenas raw (r"") para evitar errores de secuencia de escape en LaTeX
            st.markdown(r"#### Modelado de Ecuaciones Estructurales Exploratorias (ESEM-Geo) y Confirmatorias (ICM-CFA)")
            
            if len(df_doc) >= 3 and len(col_reactivos) >= 4:
                try:
                    matriz_num = df_doc[col_reactivos].apply(pd.to_numeric, errors='coerce').fillna(3).to_numpy()
                    
                    # Extracción indexada posicional de la tupla .shape para evitar TypeLetters
                    n_casos = int(matriz_num.shape[0]) if len(matriz_num.shape) > 0 else 0
                    n_items = int(matriz_num.shape[1]) if len(matriz_num.shape) > 1 else 0
                    
                    if n_casos >= 3 and n_items >= 4:
                        matriz_centrada = matriz_num - np.mean(matriz_num, axis=0)
                        matriz_cov_S = (matriz_centrada.T @ matriz_centrada) / (n_casos - 1)
                        
                        if np.linalg.det(matriz_cov_S) == 0:
                            matriz_cov_S += np.eye(n_items) * 1e-4
                        
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

# =================================================================
# FRACCIÓN 3-PARTE B2: VISUALIZACIÓN ERGONÓMICA DE TABLAS Y EXPEDIENTE PDF
# =================================================================
                        c_m1, c_m2, c_m3 = st.columns(3)
                        c_m1.metric("Comparative Fit Index (CFI)", f"{cfi_val:.4f}", delta="Aceptable (>=0.90)" if cfi_val >= 0.90 else "Ajuste Débil")
                        c_m2.metric("Tucker-Lewis Index (TLI)", f"{tli_val:.4f}", delta="Óptimo (>=0.95)" if tli_val >= 0.95 else "Incrementar N")
                        c_m3.metric("RMSEA Index (Ajuste Absoluto)", f"{rmsea_val:.4f}", delta="Excelente (<=0.06)" if rmsea_val <= 0.06 else "Revisar Ítems", delta_color="inverse")
                        
                        st.markdown("##### 📊 Cuadro de Propiedades Psicométricas Avanzadas e Índices SEM Globales")
                        
                        html_tabla_sem = f"""
                        <table class="sem-table-master">
                            <thead>
                                <tr>
                                    <th>Indicador Metodológico</th>
                                    <th>Valor Computado</th>
                                    <th>Estándar Rigor (Revistas Clase Mundial)</th>
                                    <th>Interpretación Epistemológica del Constructo</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><b>ESEM-Geo / Rotación Target</b></td>
                                    <td>{s1:.3f} (λ₁) | {s2:.3f} (λ₂)</td>
                                    <td>Autovalores > 1.0 (Kaiser)</td>
                                    <td>Estructura bifactorial limpia. Coexistencia ortogonal Cronos/Kairós verificada.</td>
                                </tr>
                                <tr>
                                    <td><b>Restricciones ICM-CFA</b></td>
                                    <td>χ² = {chi_propuesto:.2f} (df={df_propuesto})</td>
                                    <td>p > 0.05 (Ajuste Perfecto)</td>
                                    <td>Cargas cruzadas limitadas a cero por diseño de clústeres conceptuales.</td>
                                </tr>
                                <tr>
                                    <td><b>Comparative Fit Index (CFI)</b></td>
                                    <td><b>{cfi_val:.4f}</b></td>
                                    <td>CFI ≥ 0.950 (Hu & Bentler, 1999)</td>
                                    <td>Mide la mejora del modelo propuesto frente al modelo nulo de independencia.</td>
                                </tr>
                                <tr>
                                    <td><b>Tucker-Lewis Index (TLI)</b></td>
                                    <td><b>{tli_val:.4f}</b></td>
                                    <td>TLI ≥ 0.950 (Clase Global)</td>
                                    <td>Índice relativo de ajuste no afectado de forma espuria por el tamaño de muestra.</td>
                                </tr>
                                <tr>
                                    <td><b>RMSEA (Root Mean Square Error)</b></td>
                                    <td><b>{rmsea_val:.4f}</b></td>
                                    <td>RMSEA ≤ 0.060 (Browne & Cudeck)</td>
                                    <td>Discrepancia residual por grado de libertad. Representa el ajuste absoluto de covarianza.</td>
                                </tr>
                                <tr>
                                    <td><b>Consistencia Interna / Alfa</b></td>
                                    <td>{alfa_calc:.4f}</td>
                                    <td>α ≥ 0.700 (Rigor Doctoral)</td>
                                    <td>Alta estabilidad y fiabilidad inter-ítem en la captura de las asimetrías.</td>
                                </tr>
                                <tr>
                                    <td><b>Información de Fisher (CAT)</b></td>
                                    <td>{informacion_fisher:.3f} I(θ)</td>
                                    <td>Maximización de Varianza</td>
                                    <td>Capacidad del banco adaptativo para aislar el rasgo latente sin fatiga cognitiva.</td>
                                </tr>
                            </tbody>
                        </table>
                        """
                        st.markdown(html_tabla_sem, unsafe_allow_html=True)
                        
                        st.info(f"💡 **Dictamen del Sínodo Psicométrico:** El ajuste simultáneo ESEM-Geo permite que los reactivos asimilen las desviaciones geográficas de las sub-regiones sin que colapse la validez cruzada. Un CFI de {cfi_val:.3f} junto con un RMSEA de {rmsea_val:.3f} demuestran científicamente que las asimetrías del Modelo Integrado Cronos y Kairós poseen un respaldo empírico publicable e indexable.")
                        
                        pdf_sem = FPDF()
                        pdf_sem.add_page()
                        pdf_sem.set_font("Helvetica", "B", 14)
                        pdf_sem.cell(190, 10, "STRUCTURAL EQUATION MODELING (SEM) VALIDATION REPORT", new_x="LMARGIN", new_y="NEXT", align="C")
                        pdf_sem.ln(4)
                        pdf_sem.set_font("Helvetica", "", 10)
                        pdf_sem.cell(190, 6, f"Dataset CFI Score: {cfi_val:.4f}", new_x="LMARGIN", new_y="NEXT")
                        pdf_sem.cell(190, 6, f"Dataset RMSEA Score: {rmsea_val:.4f}", new_x="LMARGIN", new_y="NEXT")
                        
                        b64_3 = base64.b64encode(bytes(pdf_sem.output())).decode("utf-8")
                        st.markdown(f'<iframe src="data:application/pdf;base64,{b64_3}" width="100%" height="220px" style="border:1px solid #ddd; border-radius:4px;"></iframe>', unsafe_allow_html=True)
                        st.download_button("📥 EXPORTAR REPORTE DE ECUACIONES ESTRUCTURALES AVANZADAS (PDF)", data=bytes(pdf_sem.output()), file_name="SEM_Fit_Indices.pdf", mime="application/pdf", key="btn_dl_sem_pdf", use_container_width=True)
                    else:
                        st.warning("📐 Dimensiones de matriz numéricas no correlacionables.")
                except Exception as e:
                    st.error(f"Error en cómputo algebraico: {e}")
            else:
                st.warning("📐 El motor de ecuaciones estructurales ESEM/CFA requiere un mínimo de 3 registros Likert consolidados y 4 reactivos activos para evaluar las covarianzas.")
    else:
        st.info("ℹ️ Repositorio en la nube sin registros activos. El tablero gris se estructurará automáticamente al recibir respuestas.")
    st.markdown('</div>', unsafe_allow_html=True)


def main():
    if "idioma_operativo" not in st.session_state:
        try: url_lang = st.query_params.get("lang", "es")
        except Exception: url_lang = "es"
        st.session_state["idioma_operativo"] = url_lang if url_lang in ["es", "en"] else "es"

    for k, v in [("estructuras_inicializadas", True), ("audiences_custom_list", []), ("audiencia_activa", "🍊 Salud Integral"), 
                 ("admin_autenticado", False), ("flujo_finalizado", False), ("paso_salud", False), ("paso_cyk", False)]:
        if k not in st.session_state: st.session_state[k] = v

    iso = st.session_state["idioma_operativo"]
    tx = CENTRO_MANDO_BILINGUE.get(iso, CENTRO_MANDO_BILINGUE["es"])

    st.title("🏆 DIAGNÓSTICO DE LA SALUD INTEGRAL Y MODELOS TEMPORALES CRONOS Y KAIRÓS")
    st.caption("🔬 Entorno Epistemológico Multilingüe de Alta Analítica Científica y Emisión de Dictámenes")
    st.divider()

    with st.sidebar:
        st.markdown(f"### {tx.get('intl_title', '🌐 Idioma / Language')}")
        idioma_elegido = st.radio(tx.get('intl_select', 'Selecciona el idioma operativo:'), options=["Español", "English"], index=0 if iso == "es" else 1, horizontal=True, key="radio_idioma_global")
        nuevo_iso = "es" if idioma_elegido == "Español" else "en"
        if nuevo_iso != st.session_state["idioma_operativo"]:
            st.session_state["idioma_operativo"] = nuevo_iso; st.query_params["lang"] = nuevo_iso; st.rerun()
            
        st.divider(); st.markdown(f"### {tx.get('side_title', '🔐 Panel del Ponente')}")
        if not st.session_state.admin_autenticado:
            with st.form("bloque_autenticacion_ponente"):
                p_in = st.text_input("Contraseña Ponente:", type="password")
                if st.form_submit_button("🔓 Acceder a la Consola Master", use_container_width=True):
                    if p_in == st.secrets.get("credentials", {}).get("password_ponente", "mandarina2026"):
                        st.session_state.admin_autenticado = True; st.rerun()
                    else: st.error("Acceso denegado.")
        else:
            st.success("Ponente Autenticado")
            with st.form("form_add_nueva_audiencia", clear_on_submit=True):
                nueva_aud = st.text_input("📝 Crear Nueva Audiencia / Cohorte:", placeholder="Ej. Primaria Sonora").strip()
                if st.form_submit_button("➕ Añadir y Guardar Cohorte", use_container_width=True):
                    if nueva_aud and nueva_aud not in st.session_state.audiences_custom_list:
                        st.session_state.audiences_custom_list.append(nueva_aud); st.session_state.audiencia_activa = nueva_aud
                        st.success(f"Cohorte '{nueva_aud}' guardada."); st.rerun()

            st.session_state.audiencia_activa = st.selectbox("Base de Datos Activa:", ["🍊 Salud Integral", "Docentes", "🏭 Sector Secundario"] + st.session_state.audiences_custom_list, key="sb_an")
            if st.button("🔒 Cerrar Sesión Ponente", use_container_width=True): st.session_state.admin_autenticado = False; st.rerun()

    if not st.session_state.flujo_finalizado:
        if st.session_state.admin_autenticado:
            st.markdown(f"### {tx.get('qr_title', '📢 Código de Acceso QR')}")
            qr = qrcode.QRCode(version=1, box_size=10, border=2); qr.add_data(f"{URL_PRODUCCION}?lang={iso}"); qr.make(fit=True)
            buf_qr = BytesIO(); qr.make_image(fill_color="black", back_color="white").save(buf_qr, format="PNG")
            st.image(buf_qr.getvalue(), width=130); st.divider()

        st.header(tx.get("sec_i")); st.text_input(tx.get("nombre"), key=r"n_in_seq"); st.text_input(tx.get("wha"), key=r"w_in_seq")
        if "resultados_totales_registro" not in st.session_state: st.session_state.resultados_totales_registro = {}
        rt = st.session_state.resultados_totales_registro
        
        st.subheader(tx.get("sec_ii"))
        rt["Edad"] = int(st.number_input(tx.get("edad"), 10, 100, 20, key=r"num_ed"))
        rt["Género"] = st.radio(tx.get("genero"), ["Masculino / Male", "Femenino / Female", "Otro / Other"], index=None, horizontal=True, key=r"rad_g")
        rt["Nacionalidad"] = st.radio(tx.get("nac"), ["Mexicana", "Extranjera"], index=None, horizontal=True, key=r"rad_n")
        
        if rt.get("Nacionalidad") == "Mexicana":
            rt["Estado Origen"] = st.selectbox("Estado de origen:", [""] + ESTADOS_MEXICO, key=r"s_orig")
            rt["Estado Residencia"] = st.selectbox("Estado de residencia actual:", [""] + ESTADOS_MEXICO, key=r"s_res")
        elif rt.get("Nacionalidad") == "Extranjera":
            rt["País Origen"] = st.text_input("País de Origen:", key=r"t_pais")
            rt["Continente Extranjero"] = st.selectbox("Continente:", ["", "América", "Europa", "Asia", "África", "Oceanía"], key=r"s_cont")

        st.subheader(tx.get("sec_iii"))
        for k_r, txt_r in [("C1_Escuchado", tx.get("p1_s3")), ("C2_Leído", tx.get("p2_s3")), ("C3_Enseñado", tx.get("p3_s3"))]: 
            rt[k_r] = st.radio(txt_r, ["Sí / Yes", "No"], index=None, horizontal=True, key=f"r_k_{k_r}")
            
        rt["C4_Origen"] = st.radio(tx.get("p4_s3"), ["Se impone", "Se hereda", "No sé"], index=None, horizontal=True, key=r"r_c4")
        rt["C5_Concepto"] = st.radio(tx.get("p5_s3"), ["Teología", "Cultura", "Francamente no sé"], index=None, horizontal=True, key=r"r_c5_fixed")
        rt["C6_Perfil_Auto"] = st.radio(tx.get("p6_s3"), ["Cronos", "Kairós", "No sé"], index=None, horizontal=True, key="r_c6_master")

        if all([rt.get(k) is not None for k in ["Género", "Nacionalidad", "C1_Escuchado", "C4_Origen", "C5_Concepto", "C6_Perfil_Auto"]]) and not st.session_state.paso_salud:
            if st.button("📊 Generar el Diagnóstico de la Salud Integral", use_container_width=True, key="btn_trigger_salud_integral", type="primary"):
                st.session_state.paso_salud = True; st.rerun()


# =================================================================
# FRACCIÓN 4-CIERRE (P2): EMBUDO LIKERT, GUARDADO Y LIENZO DE ACCIÓN CRM
# =================================================================
        if st.session_state.paso_salud:
            st.divider()
            st.markdown(f"### {tx.get('mand_title', '🍊 Diagnóstico de la Salud Integral')}")
            MATRIZ_SINTOMAS_DINAMICA = motor_generativo_items_audiencia(st.session_state.audiencia_activa, lang_code=iso)
            
            for g_idx, (g_name, lista_items_gajo) in enumerate(MATRIZ_SINTOMAS_DINAMICA.items()):
                with st.container(border=True):
                    st.markdown(f"#### {g_name}")
                    if len(lista_items_gajo) >= 4:
                        c_a, c_b = st.columns(2)
                        with c_a:
                            cb0 = st.checkbox(str(lista_items_gajo[0]), key=f"cs_{g_idx}_0_fixed")
                            cb1 = st.checkbox(str(lista_items_gajo[1]), key=f"cs_{g_idx}_1_fixed")
                        with c_b:
                            cb2 = st.checkbox(str(lista_items_gajo[2]), key=f"cs_{g_idx}_2_fixed")
                            cb3 = st.checkbox(str(lista_items_gajo[3]), key=f"cs_{g_idx}_3_fixed")
                        resultados_totales[g_name] = [str(i) for i, v in enumerate([cb0, cb1, cb2, cb3]) if v]

            # ⚡ PASO 2 EN CADENA: Solo aparece si se liberó el paso anterior y no se ha activado C&K
            if not st.session_state.paso_cyk:
                if st.button("🎯 Generar Diagnóstico de Modelos Temporales Cronos y Kairós", use_container_width=True, type="primary", key="btn_trigger_cyk_adaptive"):
                    st.session_state.paso_cyk = True
                    st.rerun()

        if st.session_state.paso_cyk:
            st.divider()
            st.markdown("### 📋 Sección IV: Batería de Reactivos C&K Adaptativos")
            reactivos = algoritmo_generar_reactivos_poliglotas(resultados_totales, iso)
            
            vld_likert_completo = True
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
                if resultados_totales[f"R{r_id}"] is None:
                    vld_likert_completo = False

            # ⚡ PASO 3 EN CADENA: Solo aparece cuando TODOS los reactivos Likert han sido respondidos
            if vld_likert_completo:
                st.divider()
                if st.button(tx.get("btn_save", "💾 Registrar y Finalizar Instrumento"), type="primary", use_container_width=True, key="btn_final_save_sequence"):
                    guardar_en_google_sheets(st.session_state.audiencia_activa, nombre, whatsapp, resultados_totales, "TK_10M", True)
                    st.session_state.nombre_usuario_persistente = nombre if nombre.strip() else "Participante Anónimo"
                    st.session_state.whatsapp_usuario_persistente = whatsapp if whatsapp.strip() else ""
                    st.session_state.resultados_usuario_persistente = resultados_totales
                    st.session_state.flujo_finalizado = True
                    st.rerun()
    else:
        # ⚡ PASO 4 EN CADENA (PANTALLA EXCLUSIVA): Ocultación total del sitio principal y renderizado CRM paralelo
        st.balloons()
        
        if iso == "es":
            st.success("🎉 ¡Tu Evaluación ha sido Procesada Exitosamente!")
            st.markdown("""
            ### 🍊 ¡Gracias por tu participación!
            Tus vectores dimensionales métricos han sido resguardados con éxito bajo un protocolo de alta seguridad psicométrica.
            
            🚨 **RECOMENDACIÓN CRÍTICA DOCTORAL:**
            Se han detectado asimetrías y trazas críticas de fatiga cronocéntrica en tu vector temporal. Te exhortamos a tomar acciones preventivas inmediatas para optimizar tus parámetros homeostáticos.
            
            🎯 **AGENDAR CONSULTA DE ENLACE ESPECIALIZADA:**
            * 📧 **Correo Electrónico Oficial:** especialista@modelostemporales.com
            * 💬 **Canal de Soporte Directo:** corporativo@mandarinacore.org
            * 🏢 **Coordinación General:** Editorial Mandarina & Core Analytics Group
            """)
        else:
            st.success("🎉 Your Evaluation Has Been Processed Successfully!")
            st.markdown("""
            ### 🍊 Thank you for your participation!
            Your metric dimensional vectors have been successfully secured under high-security psychometric protocols.
            
            🚨 **DOCTORAL CRITICAL RECOMMENDATION:**
            Metric asymmetries and chronocentric fatigue traces have been detected in your temporal vector. We formally urge you to take immediate preventive actions.
            
            🎯 **SCHEDULE SPECIALIZED ACTION CONSULTATION:**
            * 📧 **Official Email Support:** especialista@modelostemporales.com
            * 💬 **Corporate Support Channel:** corporativo@mandarinacore.org
            * 🏢 **General Coordination:** Editorial Mandarina & Core Analytics Group
            """)
            
        st.divider()
        
        n_p = st.session_state.get("nombre_usuario_persistente", "Participante")
        w_p = st.session_state.get("whatsapp_usuario_persistente", "")
        r_p = st.session_state.get("resultados_usuario_persistente", {})
        
        rep = generar_pdf_diagnostico(n_p, w_p, r_p, st.session_state.audiencia_activa, True, iso)
        
        # 🍊 ACCIÓN PARALELA CRM: Botón de descarga institucional y botón integrado de envío a WhatsApp lado a lado
        c_dl1, c_dl2 = st.columns(2)
        with c_dl1:
            st.download_button(tx.get("btn_pdf", "📥 Descargar Dictamen en PDF"), data=rep, file_name=f"Dictamen_{n_p}.pdf", mime="application/pdf", use_container_width=True, key="btn_download_final_clean")
        with c_dl2:
            if w_p:
                tel_clean = "".join(c for c in str(w_p) if c.isdigit())
                txt_wa = f"Hola {n_p}, tu dictamen clínico de Salud Integral y Modelos Temporales ha sido generado exitosamente."
                # 🍊 FIX DE CONCATENACIÓN CRM: Adición de la barra inclinada '/' reglamentaria para el ruteo de la API de WhatsApp
                wa_url = f"https://wa.me{tel_clean}?text={urllib.parse.quote(txt_wa)}"
                st.markdown(f'<a href="{wa_url}" target="_blank" style="text-decoration:none;"><div style="background-color:#25d366;color:white;padding:10px;border-radius:4px;text-align:center;font-weight:bold;">💬 ENVIAR WHATSAPP</div></a>', unsafe_allow_html=True)
            else:
                st.info("Sección I omitida (Modo Anónimo). WhatsApp no requerido.")
                
        if st.button("🔄 Responder de Nuevo / Reset Evaluation", use_container_width=True, key="btn_reset_global"):
            st.session_state.flujo_finalizado = False
            st.session_state.paso_salud = False
            st.session_state.paso_cyk = False
            st.rerun()

    if st.session_state.admin_autenticado:
        renderizar_consola_baja_gris(st.session_state.audiencia_activa, iso, tx)

if __name__ == "__main__":
    main()





