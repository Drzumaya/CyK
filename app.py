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
# PARTE 4 DE 7: ACCESO A REPOSITORIOS EN LA NUBE Y DICCIONARIOS CLÍNICOS
# =================================================================
def conectar_google_sheets(nombre_tabla):
    """
    Establece conexión encriptada de alta seguridad con la API de Google Sheets
    utilizando los alcances (scopes) correctos y obligatorios exigidos por OAuth2.
    """
    try:
        credenciales_dict = dict(st.secrets["gcp_service_account"])
        if "private_key" in credenciales_dict:
            credenciales_dict["private_key"] = credenciales_dict["private_key"].replace("\\n", "\n").strip()
        
        scope = [
            "https://googleapis.com",
            "https://googleapis.com"
        ]
        credenciales = Credentials.from_service_account_info(credenciales_dict, scopes=scope)
        cliente = gspread.authorize(credenciales)
        id_libro = st.secrets["gcp_service_account"].get("spreadsheet_key", "1y99f_7hGv_3mUeE4K_1m49wB7r0V4oW3mDeR4_m49pQ").strip()
        return cliente.open_by_key(id_libro).worksheet(nombre_tabla)
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
            fila = [marca_tiempo, nombre, whatsapp, str(resultados), token_seguridad]
        else:
            fila = [
                marca_tiempo, nombre, whatsapp, 
                resultados.get("Edad", ""), resultados.get("Género", ""), resultados.get("Nacionalidad", ""),
                "", "", "", "", "", "", "", "", "", ""
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
# PARTE 5 DE 7: MOTOR PSICOMÉTRICO ADAPTATIVO Y COMPILADOR DE PDF
# =================================================================
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
    if edad > 45: 
        estilo = "institucional"
    elif edad < 25: 
        estilo = "dinamico"
    if ha_leido or es_experto: 
        estilo = "tecnico"

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
                7: "Prefiero concentrarme en un solo problema estruturado en lugar de diversificarme.",
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
    """
    Genera el reporte psicométrico individual utilizando el estándar actual de FPDF.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(190, 10, "Reporte Psicometrico Individual", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(190, 6, f"Participante: {nombre} | Contacto: {whatsapp}", new_x="LMARGIN", new_y="NEXT")
    
    if es_likert:
        c_v = [int(resultados.get(f"R{i}", 3)) for i in range(1, 11, 2)]
        k_v = [int(resultados.get(f"R{i}", 3)) for i in range(2, 11, 2)]
        avg_c = sum(c_v) / 5 if c_v else 3.0
        avg_k = sum(k_v) / 5 if k_v else 3.0
        pdf.cell(190, 6, f"Media Cronos: {avg_c:.2f} | Media Kairos: {avg_k:.2f}", new_x="LMARGIN", new_y="NEXT")
        
    return bytes(pdf.output())
# =================================================================
# PARTE 6 DE 7: COMPUERTA DE ENRUTAMIENTO Y TABLERO GRIS CORPORATIVO
# =================================================================
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
            st.markdown(f'<a href="https://wa.me{tel}" target="_blank" style="text-decoration:none;"><div style="background-color:#25d366;color:white;padding:10px;border-radius:4px;text-align:center;font-weight:bold;">💬 ENVIAR WHATSAPP</div></a>', unsafe_allow_html=True)

def renderizar_consola_baja_gris(tabla_analizar, iso, tx):
    """
    Despliega el tablero analítico corporativo de forma secuencial y nativa en la zona inferior.
    Incorpora Redes Bayesianas, Inviolabilidad SHA-256 e Información de Fisher (CAT).
    """
    st.markdown("""<style>
        .gray-dashboard-container {
            background-color: #f4f5f7; border: 2px solid #d1d5db; border-radius: 8px;
            padding: 24px; margin-top: 40px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
    </style>""", unsafe_allow_html=True)
    
    st.markdown('<div class="gray-dashboard-container">', unsafe_allow_html=True)
    st.subheader(f"🔬 CONSOLA ANALÍTICA DOCTORAL PONENTE — COHORTE: {tabla_analizar.upper()}")
    
    sheet = conectar_google_sheets(tabla_analizar)
    todas_las_filas = sheet.get_all_values() if sheet else []
    tiene_datos = todas_las_filas and len(todas_las_filas) >= 2
    
    if tiene_datos:
        df_doc = pd.DataFrame(todas_las_filas[1:], columns=todas_las_filas[0])
        col_reactivos = [c for c in df_doc.columns if str(c).startswith("R")]
        
        t1, t2, t3 = st.tabs([
            "👥 Módulo I: Meta-Análisis Colectivo & Redes Bayesianas", 
            "👤 Módulo II: CRM Clínico & Criptografía SHA-256", 
            "📐 Módulo III: Información de Fisher (CAT) & SVD"
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
                    fila_sujeto = df_filtrado.iloc[0]
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

        with t3:
            st.markdown("#### Teoría de Respuesta al Ítem (CAT) & Varianza Explicada SVD")
            if len(df_doc) >= 3 and len(col_reactivos) >= 2:
                matriz_num = df_doc[col_reactivos].apply(pd.to_numeric, errors='coerce').fillna(3).to_numpy()
                var_items = np.var(matriz_num, ddof=1, axis=0)
                var_total = np.var(np.sum(matriz_num, axis=1), ddof=1)
                K = matriz_num.shape
                alfa = (K / (K - 1)) * (1 - (np.sum(var_items) / var_total)) if var_total > 0 and K > 1 else 0.0
                
                p_respuestas = np.mean(matriz_num, axis=0) / 5.0
                informacion_fisher = np.sum(p_respuestas * (1.0 - p_respuestas))
                
                matriz_centrada = matriz_num - np.mean(matriz_num, axis=0)
                _, S, _ = np.linalg.svd(matriz_centrada, full_matrices=False)
                s1 = S if len(S) > 0 else 0.0
                s2 = S if len(S) > 1 else 0.0
                
                c_st1, c_st2, c_st3 = st.columns(3)
                c_st1.metric("Alfa de Cronbach", f"{alfa:.4f}")
                c_st2.metric("Información de Fisher Total (CAT)", f"{informacion_fisher:.3f}")
                
                # 🍊 SOLUCIÓN AL SYNTAXWARNING: Inyección de prefijo 'r' para renderizado LaTeX crudo libre de errores
                c_st3.metric(r"Eje Mayor \(\sigma_1\) (SVD)", f"{s1:.2f}")
                st.metric(r"Eje Secundario \(\sigma_2\) (SVD)", f"{s2:.2f}")
            else:
                st.info("ℹ️ Módulo métrico en espera de un mínimo de 3 respuestas Likert completas.")
    else:
        st.info("ℹ️ Repositorio en la nube sin registros activos. El tablero gris se estructurará automáticamente al recibir respuestas.")
    st.markdown('</div>', unsafe_allow_html=True)
# =================================================================
# PARTE 7 DE 7: CONTROL CENTRAL, CUESTIONARIO ADAPTATIVO Y ARRANQUE CORE
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

    # 🍊 CAPA BASE SUPERIOR: EMBUDO ADAPTATIVO SECUENCIAL DEL PARTICIPANTE
    if not st.session_state.flujo_finalizado:
        st.markdown(f"### {tx.get('qr_title', '📢 Código de Acceso QR')}")
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(f"{URL_PRODUCCION}?lang={iso}")
        qr.make(fit=True)
        buf_qr = BytesIO()
        qr.make_image(fill_color="black", back_color="white").save(buf_qr, format="PNG")
        st.image(buf_qr.getvalue(), width=140)
        st.divider()

        st.header(r"📋 Sección I: Perfil de identificación")
        nombre = st.text_input(tx.get("nombre", "Nombre:"), key=r"n_in_seq")
        whatsapp = st.text_input(tx.get("wha", "WhatsApp:"), key=r"w_in_seq")
        
        if "resultados_totales_registro" not in st.session_state: st.session_state.resultados_totales_registro = {}
        resultados_totales = st.session_state.resultados_totales_registro
        
        st.subheader(r"📋 Sección II: Datos Demográficos y Geográficos")
        resultados_totales["Edad"] = int(st.number_input(tx.get("edad", "Edad:"), 10, 100, 20, key=r"num_ed"))
        resultados_totales["Género"] = st.radio(tx.get("genero", "Género:"), ["Masculino / Male", "Femenino / Female", "Otro / Other"], index=None, horizontal=True, key=r"rad_g")
        resultados_totales["Nacionalidad"] = st.radio(tx.get("nac", "Nacionalidad:"), ["Mexicana", "Extranjera"], index=None, horizontal=True, key=r"rad_n")
        
        if resultados_totales.get("Nacionalidad") == "Mexicana":
            resultados_totales["Estado Origen"] = st.selectbox("Estado de origen:", [""] + ESTADOS_MEXICO, key=r"s_orig")
            resultados_totales["Estado Residencia"] = st.selectbox("Estado de residencia actual:", [""] + ESTADOS_MEXICO, key=r"s_res")
        elif resultados_totales.get("Nacionalidad") == "Extranjera":
            resultados_totales["País Origen"] = st.text_input("País de Origen:", key=r"t_pais")
            resultados_totales["Continente Extranjero"] = st.selectbox("Continente:", ["", "América", "Europa", "Asia", "África", "Oceanía"], key=r"s_cont")

        st.subheader(r"📋 Sección III: Conocimiento sobre el tema")
        preguntas_sec3 = [("C1_Escuchado", "1. ¿Habías escuchado hablar sobre los Modelos Temporales Cronos y Kairós?"), ("C2_Leído", "2. ¿Has leído sobre los modelos temporales Cronos y Kairós?"), ("C3_Enseñado", "3. ¿Has enseñado alguna vez sobre los modelos temporales Cronos y Kairós?")]
        for key_r, txt_r in preguntas_sec3: resultados_totales[key_r] = st.radio(txt_r, ["Sí / Yes", "No"], index=None, horizontal=True, key=f"r_k_{key_r}")
        resultados_totales["C4_Origen"] = st.radio("4. El modelo temporal:", ["Se impone", "Se hereda", "No sé"], index=None, horizontal=True, key=r"r_c4")
        resultados_totales["C5_Concepto"] = st.radio("5. Hablar de modelos temporales es hablar de:", ["Teología", "Cultura", "Francamente no sé"], index=None, horizontal=True, key=r"r_c5")
        resultados_totales["C6_Perfil_Auto"] = st.radio("6. Soy persona:", ["Cronos", "Kairós", "No sé"], index=None, horizontal=True, key=r"r_c6")

        vld_base = all([nombre.strip(), whatsapp.strip(), resultados_totales.get("Género"), resultados_totales.get("Nacionalidad"), resultados_totales.get("C1_Escuchado"), resultados_totales.get("C6_Perfil_Auto")])
        if vld_base and not st.session_state.paso_salud:
            if st.button("📊 Generar el Diagnóstico de la Salud Integral", use_container_width=True, type="primary"):
                st.session_state.paso_salud = True
                st.rerun()

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
            st.divider()
            st.markdown("### 📋 Sección IV: Batería de Reactivos C&K Adaptativos")
            reactivos = algoritmo_generar_reactivos_poliglotas(resultados_totales, iso)
            for r_id, r_txt in reactivos.items():
                st.markdown(f"**Reactivo {r_id}:** {r_txt}")
                resultados_totales[f"R{r_id}"] = st.radio(label="Escala / Scale:", options=[1, 2, 3, 4, 5], format_func=lambda x: tx.get(f"likert_{x}", str(x)), index=None, horizontal=True, key=f"rcyk_{r_id}")

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
