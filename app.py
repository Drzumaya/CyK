# =================================================================
# FRACCIÓN A DE 3: IMPORTACIONES INTERNAS Y DICCIONARIOS DOCTORALES
# =================================================================
import streamlit as st
import pandas as pd
import numpy as np
import base64
import time
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
        "nombre": "Nombre completo:", "wha": "WhatsApp internacional:", "edad": "Edad biológica:",
        "genero": "Género:", "nac": "Nacionalidad:", "side_title": "🔐 Panel Ponente",
        "qr_title": "📢 Acceso QR", "qr_sub1": "Escanea en tiempo real",
        "likert_1": "1 - Totalmente en Desacuerdo", "likert_2": "2 - En Desacuerdo", "likert_3": "3 - Neutral", "likert_4": "4 - De Acuerdo", "likert_5": "5 - Totalmente de Acuerdo",
        "btn_save": "💾 Registrar y Finalizar", "btn_pdf": "📥 Descargar PDF", "err_fields": "Nombre y WhatsApp obligatorios.",
        "fields_msg": "Completa tu perfil superior para habilitar descargas.", "thanks": "¡Procesado!", "toast_msg": "Reporte listo."
    },
    "en": {
        "nombre": "Full Name:", "wha": "International WhatsApp:", "edad": "Age:",
        "genero": "Gender:", "nac": "Nationality:", "side_title": "🔐 Speaker Panel",
        "qr_title": "📢 QR Access", "qr_sub1": "Scan in real-time",
        "likert_1": "1 - Strongly Disagree", "likert_2": "2 - Disagree", "likert_3": "3 - Neutral", "likert_4": "4 - Agree", "likert_5": "5 - Strongly Agree",
        "btn_save": "💾 Save & Finalize", "btn_pdf": "📥 Download PDF", "err_fields": "Fields are mandatory.",
        "fields_msg": "Enter identity profile to unlock downloads.", "thanks": "Processed!", "toast_msg": "Ready."
    }
}

TEXTOS_DICTAMEN_BILINGUE = {
    "es": {
        "💪 Salud Física": "Optimizar el descanso homeostático y la ergonomía postural.",
        "🧠 Salud Mental": "Mitigar la infoxicación mediante bloques de ayuno digital.",
        "❤️ Salud Emocional": "Fortalecer la autorregulación emocional y canalizar el Burnout.",
        "👥 Salud Social": "Restablecer los canales relacionales directos.",
        "💰 Salud Económica": "Diseñar una matriz estratégica de contingencia pasiva.",
        "⏳ Salud Temporal": "Reequilibrar las fronteras operativas del tiempo cronológico.",
        "🙏 Salud Espiritual": "Reconectar con los hábitos devocionales basales y el propósito esencial.",
        "txt_p_simbiosis": "Perfil de Simbiosis Temporal Equilibrada (Cronos/Kairós).",
        "txt_p_cronos": "Perfil de Dominancia Cronos Rígida dependencia extrema al reloj.",
        "txt_p_kairos": "Perfil de Dominancia Kairós Dispersa improvisación reactiva.",
        "txt_ck_recom": "Implementar franjas de transición horaria híbridas."
    },
    "en": {
        "💪 Salud Física": "Optimize homeostatic rest and postural ergonomics.",
        "🧠 Salud Mental": "Mitigate information overload through digital fasting.",
        "❤️ Salud Emocional": "Strengthen emotional self-regulation and channel Burnout.",
        "👥 Salud Social": "Restore direct relational channels and support networks.",
        "💰 Salud Económica": "Design a strategic contingency matrix to mitigate liabilities.",
        "⏳ Salud Temporal": "Rebalance operational boundaries of clock time vs opportunity.",
        "🙏 Salud Espiritual": "Reconnect with basal devotional habits and purpose.",
        "txt_p_simbiosis": "Balanced Temporal Symbiosis Profile.",
        "txt_p_cronos": "Rigid Cronos Dominance Profile.",
        "txt_p_kairos": "Dispersed Kairos Dominance Profile.",
        "txt_ck_recom": "Implement hybrid hourly transition blocks."
    }
}
# =================================================================
# FRACCIÓN B DE 3: PROCESAMIENTO EN LA NUBE Y CONSTRUCTORES MÉTRICOS
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
        if not es_likert: fila = [ts, nombre, whatsapp, str(resultados), token]
        else:
            fila = [ts, nombre, whatsapp, resultados.get("Edad",""), resultados.get("Género",""), resultados.get("Nacionalidad",""), "", "", "", "", "", "", "", "", "", ""]
            for i in range(1, 11): fila.append(resultados.get(f"R{i}", ""))
            fila.append(token)
        hoja.append_row(fila)
        return True
    except Exception: return False

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

def algoritmo_generar_reactivos_poliglotas(datos, lang="es"):
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
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(190, 10, "Reporte Psicometrico Individual", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(190, 6, f"Participante: {nombre} | Contacto: {whatsapp}", new_x="LMARGIN", new_y="NEXT")
    return bytes(pdf.output())

def gateway_bt(n, w, r, lk, lg, t):
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
                st.session_state.flujo_finalizado = True
                st.rerun()
    with c2:
        if vld:
            pdf_bytes = generar_pdf_diagnostico(n, w, r, st.session_state.audiencia_activa, lk, lg)
            st.download_button(t["btn_pdf"], data=pdf_bytes, file_name="Reporte_Diagnostico.pdf", mime="application/pdf", use_container_width=True)
        else: st.info(t["fields_msg"])
    with c3:
        if vld:
            tel = "".join(c for c in str(w) if c.isdigit())
            st.markdown(f'<a href="https://wa.me{tel}" target="_blank" style="text-decoration:none;"><div style="background-color:#25d366;color:white;padding:10px;border-radius:4px;text-align:center;font-weight:bold;">💬 ENVIAR WHATSAPP</div></a>', unsafe_allow_html=True)
# =================================================================
# FRACCIÓN C (P1): TABLERO DE MANDOS GRIS CORPORATIVO E INICIO DE MAIN
# =================================================================
def renderizar_consola_baja_gris(tabla_analizar, iso, tx):
    st.markdown("""<style>
        .gray-dashboard-container {
            background-color: #f4f5f7; border: 2px solid #d1d5db; border-radius: 8px;
            padding: 24px; margin-top: 40px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
    </style>""", unsafe_allow_html=True)
    
    st.markdown('<div class="gray-dashboard-container">', unsafe_allow_html=True)
    st.subheader(f"🔬 CONSOLA ANALÍTICA CORPORATIVA PONENTE — COHORTE: {tabla_analizar.upper()}")
    
    sheet = conectar_google_sheets(tabla_analizar)
    todas_las_filas = sheet.get_all_values() if sheet else []
    
    if todas_las_filas and len(todas_las_filas) >= 2:
        df_doc = pd.DataFrame(todas_las_filas[1:], columns=todas_las_filas)
        col_reactivos = [c for c in df_doc.columns if str(c).startswith("R")]
        
        t1, t2, t3 = st.tabs(["👥 Módulo I: Colectivos", "👤 Módulo II: CRM Individual", "📐 Módulo III: SVD Factorial"])
        with t1:
            st.dataframe(df_doc, use_container_width=True)
        with t2:
            if "Nombre" in df_doc.columns:
                sujeto = st.selectbox("Selecciona Participante:", df_doc["Nombre"].unique().tolist(), key="sb_suj_baja")
                st.dataframe(df_doc[df_doc["Nombre"] == sujeto], use_container_width=True)
        with t3:
            if len(df_doc) >= 3 and len(col_reactivos) >= 2:
                matriz_num = df_doc[col_reactivos].apply(pd.to_numeric, errors='coerce').fillna(3).to_numpy()
                var_items = np.var(matriz_num, ddof=1, axis=0)
                var_total = np.var(np.sum(matriz_num, axis=1), ddof=1)
                K = int(matriz_num.shape[1])
                alfa = (K / (K - 1)) * (1 - (np.sum(var_items) / var_total)) if var_total > 0 and K > 1 else 0.0
                st.metric("Alpha de Cronbach Computado", f"{alfa:.4f}")
            else: st.info("Se necesitan al menos 3 registros con datos Likert.")
    else:
        st.info("ℹ️ Repositorio en la nube sin registros activos. El tablero se estructurará automáticamente al recibir respuestas.")
    st.markdown('</div>', unsafe_allow_html=True)

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
    # =================================================================
    # FRACCIÓN C (P2): VISTA DEL FLUJO PÚBLICO Y GUARDIA RAÍZ MAIN
    # =================================================================
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
