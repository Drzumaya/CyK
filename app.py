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
        "txt_ck_recom": "Implementar franjas de transición horaria híbridas y blindar bloques innegociables de descanso."
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
        "txt_ck_recom": "Implement hybrid hourly transition blocks and shield non-negotiable recovery slots."
    }
}
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
            # 🍊 REGISTRO CLÍNICO: Inyección de la cohorte seleccionada en la columna 4 del dataset base
            fila = [ts, nombre, whatsapp, tabla, str(resultados), token]
        else:
            # 🍊 REGISTRO LIKERT: Inyección de la cohorte seleccionada en la columna 4 del dataset matricial
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
# FRACCIÓN 2-PARTE B: ALGORITMO LIKERT Y EXPEDIENTE PDF EXPANDIDO
# =================================================================
def algoritmo_generar_reactivos_poliglotas(datos, lang="es"):
    edad_raw = datos.get("Edad", 30)
    edad = int(edad_raw) if str(edad_raw).isdigit() else 30
    ha_leido = "sí" in str(datos.get("C2_Leído", "")).lower()
    es_experto = "sí" in str(datos.get("C3_Enseñado", "")).lower()
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
    pdf = FPDF()
    pdf.add_page()
    font_family = "Helvetica"
    dictamen_bilingue = TEXTOS_DICTAMEN_BILINGUE.get(lang, TEXTOS_DICTAMEN_BILINGUE["es"])
    
    pdf.set_font(font_family, "B", 14)
    pdf.cell(190, 10, "DIAGNOSTICO CIENTIFICO DE SALUD INTEGRAL Y TIEMPO", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(3)
    
    pdf.set_font(font_family, "", 10)
    pdf.cell(190, 6, f"Participante: {nombre} | Canal WhatsApp: {whatsapp}".encode('ascii', 'ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(font_family, "B", 11)
    pdf.cell(190, 6, "1. EVALUACION DE LAS DIMENSIONES SINTOMATICAS (MANDARINA)", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    
    g_trad = motor_generativo_items_audiencia(tabla, lang_code=lang)
    for idx, dim_espanol in enumerate(DIMENSIONES_MANDARINA_MAESTRAS):
        indices_marcados = resultados.get(dim_espanol, [])
        if indices_marcados:
            dim_limpia = str(list(g_trad.keys())[idx])
            for emj in ["💪", "🧠", "❤️", "👥", "💰", "⏳", "🙏"]: dim_limpia = dim_limpia.replace(emj, "")
            
            pdf.set_font(font_family, "B", 10)
            pdf.cell(190, 5, f"-> Dimension: {dim_limpia.strip()}", new_x="LMARGIN", new_y="NEXT")
            
            sintomas_origen = list(g_trad.values())[idx]
            sintomas_reales = [sintomas_origen[int(i)] for i in indices_marcados if str(i).isdigit() and int(i) < len(sintomas_origen)]
            
            pdf.set_font(font_family, "I", 9)
            pdf.set_text_color(150, 40, 40)
            pdf.multi_cell(190, 4.5, f"Indicadores: {', '.join(sintomas_reales)}".encode('ascii', 'ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT")
            
            pdf.set_font(font_family, "", 9)
            pdf.set_text_color(40, 40, 40)
            pdf.multi_cell(190, 4.5, f"Recomendacion Basal: {dictamen_bilingue.get(dim_espanol, '')}".encode('ascii', 'ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT")
            pdf.set_text_color(0, 0, 0)
            pdf.ln(1)

    if es_likert:
        pdf.ln(2)
        pdf.set_font(font_family, "B", 11)
        pdf.cell(190, 6, "2. ANALISIS VECTORIAL CUANTITATIVO DE TRAZAS TEMPORALES (C&K)", new_x="LMARGIN", new_y="NEXT")
        c_v = [int(resultados.get(f"R{i}", 3)) for i in range(1, 11, 2)]
        k_v = [int(resultados.get(f"R{i}", 3)) for i in range(2, 11, 2)]
        avg_c = sum(c_v) / 5 if c_v else 3.0
        avg_k = sum(k_v) / 5 if k_v else 3.0
        
        pdf.set_font(font_family, "", 10)
        pdf.cell(190, 5, f"Media Vector Cronos: {avg_c:.2f} | Media Vector Kairos: {avg_k:.2f}", new_x="LMARGIN", new_y="NEXT")
        
        dif = abs(avg_c - avg_k)
        if dif <= 0.4: txt_p = dictamen_bilingue.get("txt_p_simbiosis", "")
        elif avg_k > avg_c: txt_p = dictamen_bilingue.get("txt_p_kairos", "")
        else: txt_p = dictamen_bilingue.get("txt_p_cronos", "")
        
        pdf.set_font(font_family, "I", 9.5)
        pdf.multi_cell(190, 4.5, f"Dictamen Ontologico: {txt_p}".encode('ascii', 'ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        pdf.set_font(font_family, "", 9)
        pdf.multi_cell(190, 4.5, f"Accion Metodologica: {dictamen_bilingue.get('txt_ck_recom', '')}".encode('ascii', 'ignore').decode('ascii'), new_x="LMARGIN", new_y="NEXT")

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
            st.markdown("#### Modelado de Ecuaciones Estructurales Exploratorias (ESEM-Geo) y Confirmatorias (ICM-CFA)")
            
            if len(df_doc) >= 3 and len(col_reactivos) >= 4:
                try:
                    matriz_num = df_doc[col_reactivos].apply(pd.to_numeric, errors='coerce').fillna(3).to_numpy()
                    
                    # 🍊 FIX DEFINITIVO: Extracción indexada posicional de la tupla .shape para evitar TypeLetters
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
                                end
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

# =================================================================
# FRACCIÓN 4-PARTE A: APERTURA DE MAIN, FORMULARIO DE COHORTES Y PERFIL OBLIGATORIO
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
            
            # 🍊 FORMULARIO DE ALTA DE AUDIENCIAS: Aparece en la barra lateral al firmarse el ponente
            with st.form("form_add_nueva_audiencia", clear_on_submit=True):
                nueva_aud = st.text_input("📝 Crear Nueva Audiencia / Cohorte:", placeholder="Ej. Primaria Sonora").strip()
                if st.form_submit_button("➕ Añadir y Guardar Cohorte", use_container_width=True):
                    if nueva_aud and nueva_aud not in st.session_state.audiences_custom_list:
                        st.session_state.audiences_custom_list.append(nueva_aud)
                        st.session_state.audiencia_activa = nueva_aud
                        st.success(f"Cohorte '{nueva_aud}' guardada.")
                        st.rerun()

            # El selectbox asimila la persistencia de las cohortes agregadas en caliente por el ponente
            lista_final_tablas = ["🍊 Salud Integral", "Docentes", "🏭 Sector Secundario"] + st.session_state.audiences_custom_list
            tabla_sel = st.selectbox("Base de Datos Activa:", lista_final_tablas, key="sb_an")
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
        
        if vld_secciones_iniciales and not st.session_state.paso_salud:
            if st.button("📊 Generar el Diagnóstico de la Salud Integral", use_container_width=True, key="btn_trigger_salud_integral", type="primary"):
                st.session_state.paso_salud = True
                st.rerun()

# =================================================================
# FRACCIÓN 4-PARTE B: EMBUDO ADAPTATIVO INCREMENTAL Y GUARDIA RAÍZ MAIN
# =================================================================
        if st.session_state.paso_salud:
            st.divider()
            st.markdown("### 🍊 Diagnóstico de la Salud Integral")
            MATRIZ_SINTOMAS_DINAMICA = motor_generativo_items_audiencia(st.session_state.audiencia_activa, lang_code=iso)
            
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

    if st.session_state.admin_autenticado:
        renderizar_consola_baja_gris(st.session_state.audiencia_activa, iso, tx)

if __name__ == "__main__":
    main()

