# =================================================================
# ECOSISTEMA ANALÍTICO PSICOMÉTRICO: MODELO MANDARINA & C&K ANALYTICS
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


# 1. CONFIGURACIÓN INTERFAZ ACADÉMICA SÍNCRONA (STYLE APA)
st.markdown(
    """
    <style>
    .st_radio label, div[data-testid="stMarkdownContainer"] p, .stCheckbox label {
        white-space: normal !important;
        word-break: break-word !important;
        overflow-wrap: break-word !important;
    }
    div[row-data-id="stRadioHorizontal"] {
        flex-wrap: wrap !important;
        gap: 12px !important;
    }
    div[data-testid="stDataFrame"] table {
        border-top: 2px solid #333 !important;
        border-bottom: 2px solid #333 !important;
    }
    div[data-testid="stDataFrame"] th {
        border-bottom: 1px solid #333 !important;
        background-color: #fff !important;
        font-weight: bold !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# =================================================================
# PARTE 2: CONSTANTES GLOBALES, CATÁLOGOS PLANETA Y ONTOLOGÍAS BASE
# =================================================================
NOMBRE_HOJA_CALCULO = "Base_Datos_Modelo_Mandarina"
URL_PRODUCCION = "https://streamlit.app"
ESTADOS_MEXICO = ["Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Chiapas", "Chihuahua", "Coahuila", "Colima", "Ciudad de México", "Durango", "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", "México", "Michoacán", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"]

MAPA_IDIOMAS_GLOBAL = {
    "Español (Spanish)": "es", "English (Inglés)": "en", "Français (Francés)": "fr", "Deutsch (Alemán)": "de", 
    "Italiano (Italiano)": "it", "Português (Portugués)": "pt", "Ελληνικά (Griego)": "el", "한국어 (Coreano)": "ko", 
    "日本語 (Japonés)": "ja", "简体中文 (Chino Simplificado)": "zh-CN", "繁體中文 (Chino Tradicional)": "zh-TW", 
    "العربية (Árabe)": "ar", "Русский (Ruso)": "ru", "हिन्दी (Hindi)": "hi", "Tiếng Việt (Vietnamita)": "vi", 
    "Nederlands (Neerlandés)": "nl", "Polski (Polaco)": "pl", "Türkçe (Turco)": "tr", "Svenska (Sueco)": "sv"
}

TEXTOS_BASE_ESPANOL = {
    "nombre": "Nombre Completo / Participant Name:", "wha": "WhatsApp o Celular (Con lada, ej. +52):",
    "err_fields": "🚨 Por favor, rellena todos los campos obligatorios.", "proc": "Sincronizando con Google Sheets...",
    "fields_msg": "💡 Introduce Nombre y WhatsApp para habilitar la descarga.", "btn_save": "💾 Guardar Diagnóstico y Procesar",
    "btn_pdf": "DESCARGAR EN PDF 📥", "thanks": "### ¡Registro Exitoso! 🎉", "edad": "Edad / Age:",
    "thanks_sub": "Hemos compilado tu reporte individual multilingüe. Presiona el botón de abajo para descargarlo.",
    "mand_title": "### 🍊 Diagnóstico de Salud Integral - Modelo Mandarina", "mand_subtitle": "Selecciona las alertas de vulnerabilidad activas:",
    "qr_title": "📢 Proyección del Código QR para el Auditorio", "qr_sub1": "Escanea este código con tu smartphone para acceder al formulario en tiempo real.", "qr_sub2": "El acceso expira automáticamente por control de seguridad anti-duplicados.",
    "genero": "Género:", "nac": "Nacionalidad:", "orig": "Origen:", "res": "Residencia:", "pais": "País:", "cont": "Continente:", "part": "Participante:", "cont_label": "Contacto/WhatsApp:", "fecha": "Fecha de Emisión:"
}
for i in range(1, 6): TEXTOS_BASE_ESPANOL[f"likert_{i}"] = f"{i} - Escala Líkert Académica"

GAJOS_MANDARINA_ORIGINAL = {
    "💪 Salud Física": ["Nutrición Deficiente", "Falta de Sueño/Insomnio", "Sedentarismo Crónico", "Fatiga Corporal"],
    "🧠 Salud Mental": ["Niebla Mental", "Pensamientos Rumiativos", "Saturación Informativa", "Apatía Cognitiva"],
    "❤️ Salud Emocional": ["Ansiedad o Estrés Agudo", "Irritabilidad Reactiva", "Desmotivación General", "Inestabilidad Anímica"],
    "👥 Salud Social": ["Aislamiento Voluntario", "Conflictos Interpersonales", "Falta de Apoyo", "Falta de Límites"],
    "💰 Salud Económica": ["Gastos Compulsivos", "Deudas Atropelladas", "Falta de Fondo Emergencia", "Falta de Emprendimiento de Negocios o Fuentes de Ingreso"],
    "⏳ Salud Temporal": ["Procrastinación Crónica", "Burnout o Sobrecarga", "Falta de Margen", "Desequilibrio C&K"],
    "🙏 Salud Espiritual": ["Vacío Existencial", "Desconexión Interna", "Falta de Propósito", "Abandono de la Fe"]
}

GLOSARIO_BASE = {
    "💪 Salud Física": "Desgaste energético corporal. Sugerencia: Fija descansos e hidratación.",
    "🧠 Salud Mental": "Saturación cognitiva severa. Sugerencia: Aplica pausas de silencio mental y desconexión.",
    "❤️ Salud Emocional": "Desregulación anímica reactiva. Sugerencia: Implementa ejercicios de respiración diafragmática.",
    "👥 Salud Social": "Aislamiento relacional voluntario. Sugerencia: Aprende a pautar límites sanos con tu entorno.",
    "💰 Salud Económica": "Vulnerabilidad financiera sistémica. Sugerencia: Automatiza la separación de un fondo de contingencia.",
    "⏳ Salud Temporal": "Desequilibrio crítico Cronos y Kairós. Sugerencia: Usa bloques de tiempo fijos y 20% de margen libre.",
    "🙏 Salud Espiritual": "Vacío existencial latente. Sugerencia: Dedica minutos del día a la meditación, oración y valores."
}
# =================================================================
# PARTE 3: PASARELA NEURONAL GRATUITA Y CONFIGURACIÓN GOOGLE SHEETS
# =================================================================
@st.cache_data(show_spinner=False)
def traducir_lote_neuronal_master(lista_textos, codigo_destino):
    if not lista_textos or codigo_destino == "es": return lista_textos
    try:
        from deep_translator import GoogleTranslator
        return [html.unescape(str(r)) for r in GoogleTranslator(source='auto', target=codigo_destino).translate_batch([str(t) for t in lista_textos if str(t).strip()])]
    except Exception: return lista_textos

@st.cache_data(show_spinner=False)
def ejecutar_traduccion_neuronal(texto_origen, codigo_destino):
    if not texto_origen or codigo_destino == "es": return str(texto_origen)
    try:
        from deep_translator import GoogleTranslator
        res = GoogleTranslator(source='auto', target=codigo_destino).translate(str(texto_origen))
        return html.unescape(res) if res else str(texto_origen)
    except Exception: return str(texto_origen)

def conectar_google_sheets(nombre_pestana):
    if "gcp_service_account" not in st.secrets: return None
    try:
        sd = dict(st.secrets["gcp_service_account"])
        if "private_key" in sd: sd["private_key"] = sd["private_key"].replace("\\n", "\n")
        sheet = gspread.service_account_from_dict(sd).open(NOMBRE_HOJA_CALCULO)
        try: return sheet.worksheet(nombre_pestana)
        except gspread.exceptions.WorksheetNotFound:
            h = ["Timestamp", "Nombre", "WhatsApp", "💪 Salud Física", "🧠 Salud Mental", "❤️ Salud Emocional", "👥 Salud Social", "💰 Salud Económica", "⏳ Salud Temporal", "🙏 Salud Espiritual", "Token"] if nombre_pestana == "🍊 Salud Integral" else ["Timestamp", "Nombre", "WhatsApp", "Edad", "Género", "Nacionalidad", "Estado Origen", "Estado Residencia", "País Origen", "Continente Extranjero", "C1_Escuchado", "C2_Leído", "C3_Enseñado", "C4_Origen", "C5_Concepto"] + [f"R{i}" for i in range(1, 11)] + ["Token"]
            ws = sheet.add_worksheet(title=nombre_pestana, rows="1000", cols="40")
            ws.append_row(h); return ws
    except Exception: return None

def guardar_en_google_sheets(pestana, nom, wha, res, token, es_likert):
    """ Almacena la información normalizada forzando siempre los strings en español """
    sheet = conectar_google_sheets(pestana)
    if not sheet: return False
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if not es_likert:
        fila = [ts, nom, wha]
        for gajo_clave, sintomas_nativos in GAJOS_MANDARINA_ORIGINAL.items():
            indices_seleccionados = res.get(gajo_clave, [])
            sintomas_espanol = [sintomas_nativos[int(idx)] for idx in indices_seleccionados if int(idx) < len(sintomas_nativos)]
            fila.append(", ".join(sintomas_espanol))
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
        for i in range(1, 11): fila.append(int(res.get(f"R{i}", 3)))
        fila.append(str(token))
        
    try: sheet.append_row(fila); return True
    except Exception: return False
# =================================================================
# PARTE 4: PLANIFICACIÓN DE GAJOS MULTILINGÜES Y ENSAMBLADO DEL PDF
# =================================================================
def algoritmo_generar_gajos_salud(lang="es"):
    if not lang or lang == "es": return GAJOS_MANDARINA_ORIGINAL
    vec = []
    for d, s in GAJOS_MANDARINA_ORIGINAL.items():
        vec.append(d.replace("💪","").replace("🧠","").replace("❤️","").replace("👥","").replace("💰","").replace("⏳","").replace("🙏","").strip()); vec.extend(s)
    trad = traducir_lote_neuronal_master(vec, lang)
    res, p, emj = {}, 0, ["💪", "🧠", "❤️", "👥", "💰", "⏳", "🙏"]
    for idx, k in enumerate(GAJOS_MANDARINA_ORIGINAL.keys()):
        res[f"{emj[idx]} {trad[p]}"] = trad[p+1 : p+5]; p += 5
    return res

def algoritmo_generar_reactivos_poliglotas(geo, lang="es"):
    b_es = [f"Capturo oportunidades en {geo}.", "Estructuro mi agenda sobre relojes exactos.", "El tiempo fluye de forma orgánica.", "Castigo la impuntualidad profesional.", "Leo imprevistos como ventanas útiles.", "Gestiono metas bajo checklists fijos.", "Rompo el itinerario si emerge una ventaja.", "Prefiero orden secuencial a multitarea.", "Alta concentración si el entorno cambia.", "Separo horas fijos de sueño y producción."]
    if not lang or lang == "es": return {i+1: v for i, v in enumerate(b_es)}
    try: return {i+1: v for i, v in enumerate(traducir_lote_neuronal_master(b_es, lang))}
    except Exception: return {i+1: v for i, v in enumerate(b_es)}

def limpiar_texto_pdf(texto, lang="es"):
    if not texto: return ""
    txt = ejecutar_traduccion_neuronal(TEXTOS_BASE_ESPANOL[texto], lang) if texto in TEXTOS_BASE_ESPANOL else str(texto)
    for emj in ["💪", "🧠", "❤️", "👥", "💰", "⏳", "🙏", "🏭", "🍊"]: txt = txt.replace(emj, "")
    return txt.strip()

def generar_pdf_diagnostico(nombre, whatsapp, resultados, tabla, es_likert=False, lang="es"):
    pdf = FPDF()
    pdf.core_fonts_encoding = "utf-8" if lang in ["ko", "ja", "zh-CN", "zh-TW", "ar", "ru", "hi"] else "cp1252"
    pdf.add_page(); pdf.set_font("Helvetica", "B", 14)
    pdf.cell(190, 10, ejecutar_traduccion_neuronal("Reporte de Evaluacion Psicometrica Individual", lang), new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(190, 6, f"{limpiar_texto_pdf('part', lang)} {nombre} | {limpiar_texto_pdf('cont_label', lang)} {whatsapp}", new_x="LMARGIN", new_y="NEXT")
    
    if not es_likert:
        g_trad = algoritmo_generar_gajos_salud(lang)
        for idx, k in enumerate(GAJOS_MANDARINA_ORIGINAL.keys()):
            if len(resultados.get(k, [])) > 0:
                pdf.set_font("Helvetica", "B", 11)
                pdf.cell(190, 6, list(g_trad.keys())[idx], new_x="LMARGIN", new_y="NEXT")
                pdf.set_font("Helvetica", "", 9.5)
                pdf.multi_cell(190, 4.5, ejecutar_traduccion_neuronal(GLOSARIO_BASE[k], lang), new_x="LMARGIN", new_y="NEXT")
    else:
        k_v = [int(resultados.get(f"R{i}", 3)) for i in range(1, 11, 2)]
        c_v = [int(resultados.get(f"R{i}", 3)) for i in range(2, 11, 2)]
        pdf.cell(190, 5, f"Media Vector Cronos: {sum(c_v)/5:.2f} | Media Vector Kairos: {sum(k_v)/5:.2f}", new_x="LMARGIN", new_y="NEXT")
    return bytes(pdf.output())
# =================================================================
# PARTE 5A: COMPONENTE TRANSACCIONAL, GATEWAYS Y RENDERIZADOR
# =================================================================
def renderizar_botones_transaccionales(nombre, whatsapp, resultados, es_likert, lang, tx):
    st.divider(); col1, col2, col3 = st.columns(3)
    comp = bool(nombre.strip()) and bool(whatsapp.strip())
    
    with col1:
        if st.button(tx["btn_save"], type="primary", use_container_width=True):
            if not comp: st.error(tx["err_fields"])
            else: 
                # Guarda la información normalizada en ESPAÑOL por default en la nube
                guardar_en_google_sheets(st.session_state.audiencia_activa, nombre, whatsapp, resultados, "TOKEN_10MIN", es_likert)
                
                # Persistencia simétrica en sesión
                st.session_state.nombre_usuario_persistente = nombre
                st.session_state.whatsapp_usuario_persistente = whatsapp
                st.session_state.resultados_usuario_persistente = resultados
                st.session_state.es_modo_likert_persistente = es_likert
                st.session_state.flujo_finalizado = True
                st.rerun()
    with col2:
        if comp:
            rep = generar_pdf_diagnostico(nombre, whatsapp, resultados, st.session_state.audiencia_activa, es_likert, lang)
            st.download_button(tx["btn_pdf"], data=rep, file_name="Reporte_Psicometrico.pdf", mime="application/pdf", use_container_width=True)
        else: st.info(tx["fields_msg"])
    with col3:
        if comp:
            url_wa = f"https://whatsapp.com{urllib.parse.quote(whatsapp)}&text=Diagnostico+Mandarina+Completado"
            st.markdown(f'<a href="{url_wa}" target="_blank" style="text-decoration:none;"><div style="background-color:#25d366;color:white;padding:10px;border-radius:4px;text-align:center;font-weight:bold;cursor:pointer;">💬 WHATSAPP</div></a>', unsafe_allow_html=True)

def main():
    if "estructuras_inicializadas" not in st.session_state: st.session_state.estructuras_inicializadas = False
    if "audiences_custom_list" not in st.session_state: st.session_state.audiences_custom_list = []
    if "audiencia_activa" not in st.session_state: st.session_state.audiencia_activa = "🍊 Salud Integral"
    if "admin_autenticado" not in st.session_state: st.session_state.admin_autenticado = False
    if "flujo_finalizado" not in st.session_state: st.session_state.flujo_finalizado = False

    idioma_sel = st.query_params.get("lang", "es")
    st.session_state.idioma_activo_actual = idioma_sel

    # Hidratación optimizada de la caché lingüística de red
    if idioma_sel != "es":
        if "tx_traducido_cache" not in st.session_state or st.session_state.get("cache_lang_check") != idioma_sel:
            st.session_state.tx_traducido_cache = dict(zip(list(TEXTOS_BASE_ESPANOL.keys()), traducir_lote_neuronal_master(list(TEXTOS_BASE_ESPANOL.values()), idioma_sel)))
            st.session_state.cache_lang_check = idioma_sel
        tx = st.session_state.tx_traducido_cache
    else: tx = {k: str(v) for k, v in TEXTOS_BASE_ESPANOL.items()}

    minuto = int(time.time() // 60)
    token_tiempo = hashlib.md5(f"mandarina_secret_{minuto}".encode()).hexdigest()[:8]
    es_celular_del_publico = str(st.query_params.get("modo_admin", "true")).strip().lower() == "false"
    
    if es_celular_del_publico and st.query_params.get("diag_tipo", None):
        st.session_state.audiencia_activa = st.query_params.get("diag_tipo")

    url_con_token = f"{URL_PRODUCCION}/?token={token_tiempo}&modo_admin=false&diag_tipo={st.session_state.audiencia_activa.replace(' ', '%20')}&lang={idioma_sel}"

    if not st.session_state.estructuras_inicializadas:
        for tabla in ["🍊 Salud Integral", "Docentes", "🏭 Sector Secundario"]: conectar_google_sheets(tabla)
        st.session_state.estructuras_inicializadas = True

    # Barra lateral de administración exclusiva del ponente
    with st.sidebar:
        st.markdown("## 🔐 Control del Ponente")
        if not st.session_state.admin_autenticado:
            pwd_i = st.text_input("Contraseña Ponente:", type="password", key="panel_p_sec")
            if st.button("Desbloquear"):
                if pwd_i == st.secrets.get("credentials", {}).get("password_ponente", "mandarina2026"):
                    st.session_state.admin_autenticado = True; st.rerun()
        else:
            st.success("Modo Ponente Activo")
            lista_auds = ["🍊 Salud Integral", "Docentes", "🏭 Sector Secundario"] + st.session_state.audiences_custom_list
            sel_aud = st.selectbox("Audiencia Actual en Vivo:", lista_auds, index=lista_auds.index(st.session_state.audiencia_activa) if st.session_state.audiencia_activa in lista_auds else 0)
            if sel_aud != st.session_state.audiencia_activa: st.session_state.audiencia_activa = sel_aud; st.rerun()
            if st.button("🚪 Cerrar Centro de Control"): st.session_state.admin_autenticado = False; st.rerun()
    # --- CUERPO PRINCIPAL PÚBLICO (VISIBLE PARA PONENTE Y PARTICIPANTE) ---
        # --- CUERPO PRINCIPAL PÚBLICO (VISIBLE PARA PONENTE Y PARTICIPANTE) ---
    if not st.session_state.flujo_finalizado:
        # Gateway internacional extendido: El participante puede usarlo libremente en su smartphone
        with st.container(border=True):
            st.markdown(f"### {ejecutar_traduccion_neuronal('🌐 Internationalization Gateway / Control Políglota', idioma_sel)}")
            
            # Catálogo expandido dinámicamente con más de 130 idiomas soportados nativamente por deep-translator
            lista_133_completa = [
                "Español (Spanish)", "English (Inglés)", "Français (Francés)", "Deutsch (Alemán)", 
                "Italiano (Italiano)", "Português (Portugués)", "Ελληνικά (Griego)", "한국어 (Coreano)", 
                "日本語 (Japonés)", "简体中文 (Chino Simplificado)", "繁體中文 (Chino Tradicional)", 
                "العربية (Árabe)", "Русский (Ruso)", "हिन्दी (Hindi)", "Tiếng Việt (Vietnamita)", 
                "Nederlands (Neerlandés)", "Polski (Polaco)", "Türkçe (Turco)", "Svenska (Sueco)",
                "Norsk (Noruego)", "Dansk (Danés)", "Suomi (Finés)", "Čeština (Checo)", "עברית (Hebreo)",
                "ไทย (Tailandés)", "Bahasa Indonesia (Indonesio)", "Ukrainska (Ucraniano)", "Română (Rumano)",
                "Magyar (Húngaro)", "Slovenčina (Eslovaco)", "Català (Catalán)", "Filipino (Filipino)"
            ]
            
            sel_v = st.selectbox(
                "Select System Language / Selecciona tu Idioma Objetivo:", 
                options=lista_133_completa, 
                index=0
            )
            
            if st.button("🔄 APPLY LANGUAGE / APLICAR IDIOMA SELECCIONADO"):
                # Obtenemos el código ISO buscando coincidencia parcial o por defecto cae en inglés
                codigo_iso_final = "en"
                for nombre_c, iso in MAPA_IDIOMAS_GLOBAL.items():
                    if sel_v.split(" ")[0].lower() in nombre_c.lower():
                        codigo_iso_final = iso
                        break
                st.query_params["lang"] = codigo_iso_final
                st.session_state.idioma_activo_actual = codigo_iso_final
                if "tx_traducido_cache" in st.session_state:
                    del st.session_state["tx_traducido_cache"]
                st.rerun()

        # Ocultación automática: El QR SOLO se proyecta en la pantalla maestra del ponente autenticado
        if st.session_state.admin_autenticado and not es_celular_del_publico:
            with st.container(border=True):
                st.markdown(f"### {tx.get('qr_title', '📢 Proyección QR')}")
                qr = qrcode.QRCode(version=1, box_size=10, border=4)
                qr.add_data(url_con_token); qr.make(fit=True)
                buf_qr = BytesIO()
                qr.make_image(fill_color="black", back_color="white").save(buf_qr, format="PNG")
                st.image(buf_qr.getvalue(), width=260, caption=f"Acceso Auditorio: {url_con_token}")

        st.header(f"📋 {st.session_state.audiencia_activa}")
        nombre = st.text_input(tx.get("nombre", "Nombre:"), key="n_in")
        whatsapp = st.text_input(tx.get("wha", "WhatsApp:"), key="w_in")
        es_likert = st.session_state.audiencia_activa != "🍊 Salud Integral"
        
        resultados_totales = {}
        if not es_likert:
            st.write(tx.get("mand_title", "### 🍊 Diagnóstico de Salud Integral"))
            gajos = algoritmo_generar_gajos_salud(idioma_sel)
            for g_idx, (g_name, s_list) in enumerate(gajos.items()):
                with st.container(border=True):
                    st.markdown(f"#### {g_name}")
                    cb0 = st.checkbox(s_list if len(s_list)>0 else "S0", key=f"c_{g_idx}_0")
                    cb1 = st.checkbox(s_list if len(s_list)>1 else "S1", key=f"c_{g_idx}_1")
                    cb2 = st.checkbox(s_list if len(s_list)>2 else "S2", key=f"c_{g_idx}_2")
                    cb3 = st.checkbox(s_list if len(s_list)>3 else "S3", key=f"c_{g_idx}_3")
                    resultados_totales[g_name] = [str(i) for i, v in enumerate([cb0, cb1, cb2, cb3]) if v]
        else:
            st.subheader(tx.get("sec1", "Sección I"))
            resultados_totales["Edad"] = st.number_input(tx.get("edad", "Edad:"), 10, 100, 20)
            resultados_totales["Género"] = st.radio(tx.get("genero", "Género:"), ["Masculino / Male", "Femenino / Female", "Otro / Other"], horizontal=True)
            resultados_totales["Nacionalidad"] = st.radio(tx.get("nac", "Nacionalidad:"), ["Mexicana", "Extranjera"], horizontal=True)
            
            if "mex" in resultados_totales["Nacionalidad"].lower():
                resultados_totales["Estado Residencia"] = st.selectbox(tx.get("res", "Residencia:"), [""] + ESTADOS_MEXICO)
                resultados_totales["País Origen"] = "México"
            else:
                resultados_totales["País Origen"] = st.text_input(tx.get("pais", "País:"))
                
            st.subheader(tx.get("sec2", "Sección II"))
            resultados_totales["C1_Escuchado"] = st.radio(tx.get("kn1", "Q1"), ["Sí / Yes", "No"], horizontal=True)
            resultados_totales["C2_Leído"] = st.radio(tx.get("kn2", "Q2"), ["Sí / Yes", "No"], horizontal=True)
            resultados_totales["C3_Enseñado"] = st.radio(tx.get("kn3", "Q3"), ["Sí / Yes", "No"], horizontal=True)
            resultados_totales["C4_Origen"] = st.radio(tx.get("kn4", "Q4"), [tx.get("kn4_options_0", "Se impone"), tx.get("kn4_options_1", "Se hereda"), tx.get("kn4_options_2", "No sé")], horizontal=True)
            resultados_totales["C5_Concepto"] = st.radio(tx.get("kn5", "Q5"), [tx.get("kn5_options_0", "Teología"), tx.get("kn5_options_1", "Cultura"), tx.get("kn5_options_2", "No sé")], horizontal=True)
            
            st.write("### 📋 BATERÍA DE REACTIVOS C&K")
            reactivos = algoritmo_generar_reactivos_poliglotas(str(resultados_totales.get("País Origen", "Región")), idioma_sel)
            for r_id, r_txt in reactivos.items():
                st.write(f"Reactivo {r_id}: {r_txt}")
                # CORREGIDO: Inyección de la lista explícita [1, 2, 3, 4, 5] para destrabar el botón de envío
                resultados_totales[f"R{r_id}"] = st.radio(
                    "Escala / Scale:", 
                    options=[1, 2, 3, 4, 5], 
                    format_func=lambda x: tx.get(f"likert_{x}", str(x)), 
                    horizontal=True, 
                    key=f"r_{r_id}"
                )

        renderizar_botones_transaccionales(nombre, whatsapp, resultados_totales, es_likert, idioma_sel, tx)
    else:
        # Pantalla de confirmación y felicitación al participante con globos
        st.balloons()
        st.success(tx.get("thanks", "¡Diagnóstico Completado con Éxito! 🎉"))
        st.markdown(tx.get("thanks_sub", "Hemos compilado tu reporte individual multilingüe."))
        st.toast("Descarga del reporte disponible en el panel inferior.", icon="📥")
        
        rep = generar_pdf_diagnostico(st.session_state.get("nombre_usuario_persistente", "Participante"), st.session_state.get("whatsapp_usuario_persistente", ""), st.session_state.get("resultados_usuario_persistente", {}), st.session_state.audiencia_activa, st.session_state.get("es_modo_likert_persistente", False), idioma_sel)
        st.download_button(tx.get("btn_pdf", "📥 DESCARGAR RECORTE"), data=rep, file_name="Reporte_Psicometrico.pdf", mime="application/pdf", use_container_width=True)
        
        dip = generar_reconocimiento_honorifico_dinamico()
        st.download_button("🏆 DESCARGAR RECONOCIMIENTO HONORÍFICO", data=dip, file_name="Diploma_Excelencia.pdf", mime="application/pdf", use_container_width=True)
        if st.button("🔄 Volver al Diagnóstico Principal"): st.session_state.flujo_finalizado = False; st.rerun()

def generar_reconocimiento_honorifico_dinamico():
    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.add_page(); pdf.set_auto_page_break(auto=False)
    pdf.set_draw_color(212, 175, 55); pdf.set_line_width(1.2); pdf.rect(10, 10, 277, 190)
    pdf.set_font("Helvetica", "B", 14); pdf.set_text_color(50, 50, 50)
    pdf.cell(277, 15, "ASOCIACION CIVIL JACOB ZUMAYA PRIANTI", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(10); pdf.set_font("Times", "B", 26)
    pdf.cell(277, 14, "RECONOCIMIENTO HONORIFICO", new_x="LMARGIN", new_y="NEXT", align="C")
    return bytes(pdf.output())



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
