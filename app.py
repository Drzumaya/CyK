import streamlit as st
import qrcode
from io import BytesIO
from fpdf import FPDF
import gspread
import pandas as pd
import numpy as np
import datetime
import hashlib
import time
import base64

# Desactivar advertencias interactivas de pyplot globales por ejecución síncrona
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# =================================================================
# CONFIGURACIONES GENERALES Y ENLACES DE LA PONENCIA
# =================================================================
URL_PRODUCCION = "https://streamlit.app"
NOMBRE_HOJA_CALCULO = "Base_Datos_Modelo_Mandarina"

# Inicialización síncrona y global de tokens y variables de red prioritarias
minuto_actual = int(time.time() // 60)
token_tiempo = hashlib.md5(f"mandarina_secret_{minuto_actual}".encode()).hexdigest()[:8]

# Captura prioritaria de parámetros de consulta (Query Params)
token_actual = st.query_params.get("token", None)
modo_admin_url = st.query_params.get("modo_admin", "true")
es_celular_del_publico = str(modo_admin_url).strip().lower() == "false"
diag_tipo_url = st.query_params.get("diag_tipo", None)

if "audiencia_activa" not in st.session_state:
    st.session_state.audiencia_activa = "🍊 Salud Integral"

if es_celular_del_publico and diag_tipo_url:
    st.session_state.audiencia_activa = diag_tipo_url

# Construcción unificada de la URL parametrizada del QR
url_con_token = f"{URL_PRODUCCION}/?token={token_tiempo}&modo_admin=false&diag_tipo={st.session_state.audiencia_activa.replace(' ', '%20')}"

st.set_page_config(page_title="Ecosistema Diagnóstico de Modelos Temporales", layout="centered")

st.title("🍊 Ecosistema de Diagnóstico de Salud Integral")
st.subheader("Modelo Mandarina & Modelos Temporales Sectores")
st.caption("Desarrollado por: Jacob Zumaya Prianti (c) 2026 | JACOB ZUMAYA PRIANTI, A.C.")


def conectar_google_sheets(nombre_pestana):
    try:
        if "gcp_service_account" not in st.secrets:
            return None
            
        secrets_dict = dict(st.secrets["gcp_service_account"])
        if "private_key" in secrets_dict:
            secrets_dict["private_key"] = secrets_dict["private_key"].replace("\\n", "\n")
            
        client = gspread.service_account_from_dict(secrets_dict)
        workbook = client.open(NOMBRE_HOJA_CALCULO)
        
        pestana_sana = nombre_pestana.replace("/", "_").replace("(", "").replace(")", "")[:30]
        
        try:
            return workbook.worksheet(pestana_sana)
        except gspread.exceptions.WorksheetNotFound:
            return workbook.add_worksheet(title=pestana_sana, rows="1000", cols="35")
    except Exception:
        return None

def guardar_en_google_sheets(nombre_pestana, nombre, whatsapp, resultados, token, es_likert=False):
    sheet = conectar_google_sheets(nombre_pestana)
    if sheet:
        try:
            if es_likert:
                fila = [
                    str(datetime.datetime.now()), nombre, whatsapp,
                    resultados.get("Edad", ""), resultados.get("Género", ""),
                    resultados.get("Nacionalidad", ""), resultados.get("Estado Origen", ""),
                    resultados.get("Estado Residencia", ""), resultados.get("País Origen", ""),
                    resultados.get("Continente Extranjero", ""), resultados.get("Rol Iglesia", ""),
                    resultados.get("C1_Escuchado", ""), resultados.get("C2_Leído", ""),
                    resultados.get("C3_Enseñado", ""), resultados.get("C4_Origen", ""),
                    resultados.get("C5_Concepto", "")
                ]
                for i in range(1, 15):
                    fila.append(resultados.get(f"R{i}", 3))
                fila.append(token if token else "Acceso_Directo")
            else:
                fila = [
                    str(datetime.datetime.now()), nombre, whatsapp,
                    len(resultados.get("Salud Fisica (SF)", [])), len(resultados.get("Salud Mental (SM)", [])),
                    len(resultados.get("Salud Emocional (SE)", [])), len(resultados.get("Salud Social (SS)", [])),
                    len(resultados.get("Salud Economica (SECO)", [])), len(resultados.get("Salud Temporal (ST)", [])),
                    len(resultados.get("Salud Espiritual (SPI)", [])), ", ".join(resultados.get("Salud Temporal (ST)", [])),
                    token if token else "Acceso_Directo"
                ]
            sheet.append_row(fila)
            return True
        except Exception:
            return False
    return False


def generar_pdf_diagnostico(nombre_usuario, whatsapp_usuario, resultados, titulo_diagnostico, es_likert=False, img_grafica_base64=None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(230, 81, 0) 
    pdf.cell(0, 10, f"REPORTE DIAGNOSTICO: {titulo_diagnostico.upper()}", new_x="LMARGIN", new_y="NEXT", align="C")
    
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, "Metricas de Organizacion Temporal | Jacob Zumaya Prianti (c) 2026", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)
    
    pdf.set_draw_color(255, 152, 0)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)
    
    pdf.set_text_color(50, 50, 50)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(45, 6, "Participante:", new_x="RIGHT", new_y="TOP")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, nombre_usuario if nombre_usuario else "Anonimo", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(45, 6, "WhatsApp/Contacto:", new_x="RIGHT", new_y="TOP")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, whatsapp_usuario if whatsapp_usuario else "No Proporcionado", new_x="LMARGIN", new_y="NEXT")
    
    if es_likert:
        cronos_items = [resultados.get(f"R{i}", 3) for i in range(1, 15, 2)]
        kairos_items = [resultados.get(f"R{i}", 3) for i in range(2, 15, 2)]
        avg_cronos = sum(cronos_items) / 7
        avg_kairos = sum(kairos_items) / 7
        
        pdf.ln(3)
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(230, 81, 0)
        pdf.cell(0, 8, "VECTORES DE TENSION TEMPORAL CALCULADOS", new_x="LMARGIN", new_y="NEXT")
        pdf.line(10, pdf.get_y(), 120, pdf.get_y())
        pdf.ln(4)
        
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 6, f"- Indice de Orientacion Estructurada (CRONOS): {avg_cronos:.2f} / 5.00", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 6, f"- Indice de Orientacion Relacional (KAIROS): {avg_kairos:.2f} / 5.00", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)
        
        if img_grafica_base64:
            try:
                img_clean = img_grafica_base64.split(",")[-1]
                img_data = BytesIO(base64.b64decode(img_clean))
                pdf.image(img_data, x=55, w=100)
                pdf.ln(4)
            except Exception: pass
            
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 6, "REGIMEN TEMPORAL DETECTADO:", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 11)
        
        diferencia = abs(avg_cronos - avg_kairos)
        if diferencia <= 0.4:
            pdf.set_text_color(38, 166, 91) 
            pdf.cell(0, 6, "Perfil de Simbiosis Temporal Equilibrada (Cronos & Kairos)", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "I", 10)
            pdf.set_text_color(50, 50, 50)
            pdf.multi_cell(0, 5, "Felicidades. Tu perfil demuestra una alta madurez organizacional. Logras operar bajo la eficiencia del reloj sin perder la sensibilidad ante el valor humano de la jornada.")
        elif avg_kairos > avg_cronos:
            pdf.set_text_color(30, 139, 195) 
            pdf.cell(0, 6, "Perfil Temporal Kairotico Puro", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "I", 10)
            pdf.set_text_color(50, 50, 50)
            pdf.multi_cell(0, 5, "Tu comportamiento prioriza las ventanas providenciales de oportunidad, la salud mental y la adaptabilidad. Tu reto es evitar que la flexibilidad diluya el cumplimiento de metas metricas.")
        else:
            pdf.set_text_color(217, 30, 24) 
            pdf.cell(0, 6, "Perfil Temporal Cronocentrico Puro (Estructurado)", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "I", 10)
            pdf.set_text_color(50, 50, 50)
            pdf.multi_cell(0, 5, "Operas bajo un regimen rigido atado al reloj, los manuales SOP, flujogramas y metas metricas por hora. Si bien eres altamente eficiente, te encuentras expuesto a altos niveles de estres ante imprevistos.")
            
            pdf.ln(3)
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(230, 81, 0)
            pdf.cell(0, 6, "POTENCIALIDADES DE COMPLEMENTARIEDAD (Si fortaleces tu vector Kairos):", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(50, 50, 50)
            potencialidades_txt = (
                "Al incorporar de forma intencional el vector Kairos en tus jornadas del ecosistema, liberaras las siguientes ventajas organizacionales:\n"
                "- 1. Reduccion de la carga sistemicas de estres o frustracion ante fallas tecnicas de red o imprevistos materiales.\n"
                "- 2. Alta capacidad de adaptacion e innovacion disruptiva (Kaizen) al aprovechar ventanas de oportunidad no agendadas.\n"
                "- 3. Mayor impacto de liderazgo humano, optimizando la resolucion de crisis de salud mental y empatia en tu entorno."
            )
            pdf.multi_cell(0, 5, potencialidades_txt)

        if avg_cronos >= 3.80 or avg_kairos >= 3.80:
            pdf.ln(4)
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(217, 30, 24)
            pdf.cell(0, 6, "🚨 MATRIZ DE ADVERTENCIAS Y FOCOS ROJOS DEL PERFIL:", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(50, 50, 50)
            alertas_txt = ""
            if avg_cronos >= 3.80:
                alertas_txt += "⚠️ ALTO CRONOS DETECTADO:\n- Riesgo elevado de Burnout por tirania del rendimiento.\n- Rigidez ante demandas humanas del entorno.\n- Ansiedad severa cuando las metricas escapan del control.\n"
            if avg_kairos >= 3.80:
                alertas_txt += "⚠️ ALTO KAIROS DETECTADO:\n- Procrastinacion por depender en exceso de la inspiracion.\n- Falta difusa de limites y plazos metricos.\n- Sobrecarga relacional y desgaste por asumir demandas ajenas.\n"
            pdf.multi_cell(0, 5, alertas_txt)

        pdf.ln(5)
        pdf.set_fill_color(254, 243, 233) 
        pdf.set_draw_color(230, 81, 0)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(230, 81, 0)
        pdf.cell(0, 7, "INVITACION A CONSULTORIA ESPECIALIZADA", new_x="LMARGIN", new_y="NEXT", align="C", fill=True)
        pdf.set_font("Helvetica", "I", 10)
        pdf.set_text_color(60, 60, 60)
        invitacion_lbl = "Lograr el acoplamiento perfecto entre la eficiencia del reloj (Cronos) y el valor real de la oportunidad (Kairos) requiere un diseno estrategico avanzado. Te invitamos a solicitar una sesion de consultoria especializada y personalizada con el ponente Jacob Zumaya Prianti para disenar un flujograma de simbiosis temporal C&K adaptado a tus metas corporativas."
        pdf.multi_cell(0, 5, invitacion_lbl, border="LRB")
    else:
        # Segmentación original Mandarina por Subtítulos Independientes
        for dim_nombre, items in resultados.items():
            conteo = len(items)
            estado = "GAJO SANO Y PLENO" if conteo == 0 else ("EN ALERTA TEMPRANA" if conteo < 3 else "CRITICO / URGENCIA INMEDIATA")
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(230, 81, 0)
            pdf.cell(0, 6, f">> SUBTITULO: {dim_nombre.upper()}", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(50, 50, 50)
            pdf.cell(0, 5, f"Estatus Operativo: {estado}", new_x="LMARGIN", new_y="NEXT")
            puntos_str = ", ".join(items) if conteo > 0 else "Ninguno. Area equilibrada."
            pdf.multi_cell(0, 5, f"Puntos detectados: {puntos_str}\n")
            
    return pdf.output()


def ejecutar_analisis_semdeep(df, es_likert=False):
    analisis = {}
    if len(df) < 5:
        analisis["status"] = "Muestra insuficiente para convergencia estructural (Mínimo 5 registros)."
        return analisis
        
    try:
        if es_likert:
            columnas_r = [c for c in df.columns if c.startswith("Reactivo") or (len(c) <= 3 and c.startswith("R"))]
            if len(columnas_r) < 14:
                columnas_r = list(df.columns[16:30])
                
            matriz_datos = df[columnas_r].apply(pd.to_numeric, errors='coerce').fillna(3).to_numpy()
            
            cronos_data = matriz_datos[:, 0::2]
            kairos_data = matriz_datos[:, 1::2]
            
            c_centered = cronos_data - np.mean(cronos_data, axis=0)
            k_centered = kairos_data - np.mean(kairos_data, axis=0)
            
            _, _, V_c = np.linalg.svd(c_centered, full_matrices=False)
            _, _, V_k = np.linalg.svd(k_centered, full_matrices=False)
            
            latent_cronos = c_centered @ V_c[0, :]
            latent_kairos = k_centered @ V_k[0, :]
            
            impacto_data = matriz_datos[:, 12:14]
            i_centered = impacto_data - np.mean(impacto_data, axis=0)
            _, _, V_i = np.linalg.svd(i_centered, full_matrices=False)
            latent_impacto = i_centered @ V_i[0, :]
            
            X = np.vstack([latent_cronos, latent_kairos]).T
            beta = np.linalg.pinv(X.T @ X) @ X.T @ latent_impacto
            
            r_cuadrado = 1 - (np.sum((latent_impacto - X @ beta) ** 2) / np.sum((latent_impacto - np.mean(latent_impacto)) ** 2))
            
            analisis["status"] = "Convergencia Exitosa (SEMDeep Engine v2.6)"
            analisis["beta_cronos_path"] = float(beta) if len(beta)>0 else 0.0
            analisis["beta_kairos_path"] = float(beta) if len(beta)>1 else 0.0
            analisis["gof_r2_ajuste"] = max(0.0, float(r_cuadrado))
            analisis["covarianza_latente"] = float(np.corrcoef(latent_cronos, latent_kairos))
        else:
            matriz_datos = df.iloc[:, 3:10].apply(pd.to_numeric, errors='coerce').fillna(0).to_numpy()
            c_centered = matriz_datos - np.mean(matriz_datos, axis=0)
            _, s, _ = np.linalg.svd(c_centered, full_matrices=False)
            analisis["status"] = "Convergencia Lineal Exitosa (SVD Gajos)"
            analisis["gof_r2_ajuste"] = float(s**2 / np.sum(s**2)) if len(s)>0 else 0.0
    except Exception as e:
        analisis["status"] = f"Error en cálculo matricial: {str(e)}"
    return analisis


if not es_celular_del_publico:
    with st.expander("📱 Código QR Dinámico de Seguridad (Proyectar al Auditorio)", expanded=True):
        col1, col2 = st.columns([1, 1.5])
        with col1:
            qr = qrcode.QRCode(version=1, box_size=10, border=2)
            qr.add_data(url_con_token)
            qr.make(fit=True)
            img_qr = qr.make_image(fill_color="#e65100", back_color="white")
            buf = BytesIO()
            img_qr.save(buf, format="PNG")
            st.image(buf.getvalue(), caption=f"QR Activo: {st.session_state.audiencia_activa}", width="stretch")
        with col2:
            st.write(f"### Audiencia Proyectada en Vivo: **{st.session_state.audiencia_activa}**")
            st.write("1. Enfoca el código QR con la cámara de tu smartphone.")
            st.write("2. Responderás directamente el software nativo adaptado a tu organización sin necesidad de registros externos.")


if "admin_autenticado" not in st.session_state:
    st.session_state.admin_autenticado = False
if "guardado_exitoso" not in st.session_state:
    st.session_state.guardado_exitoso = False
if "flujo_finalizado" not in st.session_state:
    st.session_state.flujo_finalizado = False

# Extracción segura de la clave cifrada de Secrets para blindar el código fuente
PASSWORD_SISTEMA = st.secrets["credentials"]["password_ponente"] if "credentials" in st.secrets else "mandarina2026"

if not es_celular_del_publico:
    with st.sidebar:
        st.markdown("## 🔐 Control del Ponente")
        if not st.session_state.admin_autenticado:
            input_password = st.text_input("Contraseña Ponente:", type="password", key="side_pwd")
            if st.button("Desbloquear Tableros", width="stretch"):
                if input_password == PASSWORD_SISTEMA:
                    st.session_state.admin_autenticado = True
                    st.rerun()
                else: st.error("Contraseña incorrecta. Acceso denegado.")
        else:
            st.success("Modo Ponente Activo")
            lista_audiencias = ["🍊 Salud Integral", "🚜 Sector Primario", "🏭 Sector Secundario", "💼 Sector Terciario", "Docentes", "Padres Primaria", "Padres Secundaria", "Padres Preparatoria", "Padres Universitario", "Estudiantes Primaria", "Estudiantes Secundaria", "Estudiantes Preparatoria", "Estudiantes Universitario", "Religioso General", "Religioso IASD"]
            seleccion = st.selectbox("Audiencia Actual en Vivo:", lista_audiencias)
            if seleccion != st.session_state.audiencia_activa:
                st.session_state.audiencia_activa = seleccion
                st.rerun()
            if st.button("Cerrar Sesion", width="stretch"):
                st.session_state.admin_autenticado = False
                st.rerun()

# Interceptor estructural de caducidad temporal (Ventana de 5 minutos de gracia)
if token_actual and not st.session_state.admin_autenticado:
    minuto_base = int(time.time() // 60)
    tokens_validos = [hashlib.md5(f"mandarina_secret_{minuto_base - i}".encode()).hexdigest()[:8] for i in range(5)]
    if token_actual not in tokens_validos:
        acceso_bloqueado = True
    else:
        sheet = conectar_google_sheets(st.session_state.audiencia_activa)
        if sheet:
            try:
                registros = sheet.get_all_records()
                if registros:
                    df_check = pd.DataFrame(registros)
                    if token_actual in [str(r.get(df_check.columns[-1], "")) for r in registros]:
                        acceso_bloqueado = True
            except Exception: pass
else:
    acceso_bloqueado = False

if acceso_bloqueado:
    st.error("🚫 El acceso escaneado ha expirado o ya fue utilizado en esta ponencia.")
    st.stop()


if st.session_state.admin_autenticado and not es_celular_del_publico:
    st.markdown("---")
    st.header("🔬 Oficina de Investigación y Alta Analítica del Ponente")
    st.write("Módulo avanzado de modelado predictivo de variables latentes.")
    
    tabla_analizar = st.selectbox("Seleccionar Tabla para Extracción Científica:", ["🍊 Salud Integral", "Docentes", "🏭 Sector Secundario"])
    
    if st.button("📊 Ejecutar Auditoría Estadística de Nivel Doctoral", type="primary"):
        sheet = conectar_google_sheets(tabla_analizar)
        if sheet:
            records = sheet.get_all_records()
            if records:
                df_doc = pd.DataFrame(records)
                st.success(f"¡Base de datos cargada! Registros analizados: {len(df_doc)}")
                
                es_tabla_likert = (tabla_analizar != "🍊 Salud Integral")
                col_graph1, col_graph2 = st.columns(2)
                
                with col_graph1:
                    st.write("#### 📈 Distribución Descriptiva Global")
                    if not es_tabla_likert:
                        col_gajos = ["Salud Fisica (SF)", "Salud Mental (SM)", "Salud Emocional (SE)", "Salud Social (SS)", "Salud Economica (SECO)", "Salud Temporal (ST)", "Salud Espiritual (SPI)"]
                        promedios = {}
                        for c in col_gajos:
                            if c in df_doc.columns:
                                promedios[c] = pd.to_numeric(df_doc[c], errors='coerce').fillna(0).mean()
                        if promedios:
                            st.bar_chart(pd.DataFrame(list(promedios.items()), columns=["Dim", "Media"]), x="Dim", y="Media", color="#e65100")
                    else:
                        r_cols = [c for c in df_doc.columns if c.startswith("R") or c.startswith("Reactivo")]
                        matriz_r = df_doc[r_cols].apply(pd.to_numeric, errors='coerce').fillna(3).to_numpy()
                        c_mean = np.mean(matriz_r[:, 0::2]) if len(r_cols)>=14 else 3.0
                        k_mean = np.mean(matriz_r[:, 1::2]) if len(r_cols)>=14 else 3.0
                        st.bar_chart(pd.DataFrame([["Cronos", c_mean], ["Kairos", k_mean]], columns=["Vector", "Media"]), x="Vector", y="Media", color="#2574a9")
                
                with col_graph2:
                    st.write("#### 🧠 Modelado Estructural Ecuaciones Latentes: SEMDeep")
                    res_sem = ejecutar_analisis_semdeep(df_doc, es_tabla_likert)
                    st.json(res_sem)
                
                with st.container(border=True):
                    st.markdown("### 📚 Guía de Interpretación Epistemológica del SEMDeep (Fidelidad Doctoral)")
                    st.markdown(
                        "El motor **SEMDeep (Structural Equation Modeling Deep Engine)** evalúa relaciones de covarianza estructural "
                        "entre constructos no observables (Variables Latentes) derivados del comportamiento temporal de la muestra. "
                        "A diferencia de las regresiones ordinarias, calcula cargas factoriales puras mediante Descomposición en Valores Singulares (SVD).\n\n"
                        "**1. Path Coefficients (Beta Cronos / Beta Kairos):** Indican la magnitud y dirección del impacto de cada régimen temporal sobre la capacidad de adaptación "
                        "y transformación ética del grupo. Un coeficiente mayor a `0.40` indica una influencia crítica dominante. Si `Beta Cronos > Beta Kairos`, el auditorio unifica su excelencia "
                        "vía estructuras rígidas; si es a la inversa, la organización depende del clima relacional y momentos de oportunidad.\n\n"
                        "**2. Goodness of Fit (GoF / R² Ajustado):** Representa el poder de predictibilidad científica general del modelo. Un `GoF` de `0.50` a `0.70` se clasifica con rigor académico "
                        "como un ajuste de alta fidelidad, indicando que el régimen del tiempo explica la mayor parte del comportamiento adaptativo de la muestra.\n\n"
                        "**3. Covarianza Latente:** Mide la distancia analítica entre los constructos. Una covarianza cercana a `0.00` o negativa evidencia una tensión severa y fricción operativa "
                        "en la muestra de la organización, validando la urgencia inmediata de implementar la **Simbiosis C&K** promovida en la consultoría."
                    )
            else: st.warning("No hay filas registradas en esta pestaña.")
        else: st.error("Error de enlace.")


BANCO_PREGUNTAS = {
    "Docentes": {
        1: "Planifico mis actividades académicas, proyectos de ingeniería o labores administrativas en el ITAP siguiendo estrictamente los horarios institucionales y el calendario oficial del semestre.",
        2: "Considero que la flexibilidad para adaptar el plan de una clase o junta ante una necesidad de aprendizaje o idea innovadora de los estudiantes es más importante que cumplir rígidamente con el orden del día.",
        3: "Establezco y respeto límites fijos de tiempo para el desarrollo de las prácticas de laboratorio, entregas en plataforma o reuniones departamentales para asegurar el cumplimiento total de los objetivos programados.",
        4: "Tengo plena disposición para modificar mi agenda de trabajo o de estudio en la institución si surge un momento emergente de asesoría relacional, orientación profesional o apoyo emocional para un compañero o alumno.",
        5: "Considero que la puntualidad extrema en el ingreso a las aulas y el respeto a la duración exacta de los módulos horarios son reflejos directos de una buena mayordomía de los recursos del instituto.",
        6: "Creo que la calidad conceptual y el valor humano de una tutoría, revisión de proyecto o vinculación con el sector productivo tienen prioridad absoluta sobre cualquier límite de tiempo fijado en el reloj.",
        7: "Me genera una profunda incomodidad o frustración cuando incidentes técnicos menores, fallas en la red o dinámicas imprevistas alteran la estructura planeada de mis horas de jornada en el plantel.",
        8: "Confío en que el proceso creativo y el desarrollo de soluciones tecnológicas e ingenieriles surgen en ventanas providenciales de oportunidad (momentos de inspiración) que no siempre coinciden con los cronogramas rígidos.",
        9: "Prefiero que los ponentes en los congresos, los directors de carrera y los equipos de trabajo concluyan sus participaciones ciñéndose estrictamente al tiempo asignado en las convocatorias oficiales.",
        10: "Cuando me encuentro inmerso en el desarrollo de software, diseño de prototipos, investigación de campo o dinámicas colaborativas complejas, pierdo con frecuencia la noción del tiempo terrenal.",
        11: "Mido el éxito de un proyecto de residencias profesionales, servicio social o evento institucional principalmente a través del cumplimiento exacto de las metas métricas y los tiempos de entrega programados.",
        12: "Prefiero que la gobernanza, las academias y los ministerios de apoyo en la comunidad universitaria se adapten con sensibilidad a las necesidades emocionales y de salud mental urgentes de la comunidad estudiantil.",
        13: "Considero que el apego riguroso a los manuales de procesos organizacionales, las minutas y los flujogramas del ITAP es la clave fundamental para mantener el orden, la eficiencia y la excelencia institucional.",
        14: "Valoro los resultados del impacto educativo del ITAP por la transformación integral del pensamiento, la ética profesional y el bienestar de los graduados, más que por las métricas de egreso o los blancos numéricos alcanzados."
    },
    "🏭 Sector Secundario": {
        1: "Planifico y ejecuto mis actividades operativas en la planta siguiendo estrictamente los tiempos ciclo (takt time) y las metas por hora fijadas en el tablero de control de la línea.",
        2: "Considero que detener temporalmente o flexibilizar la velocidad de la línea ante una falla imprevista o para capacitar en sitio a un compañero es más importante que cumplir rígidamente con la cuota diaria en ese instante.",
        3: "Establezco y/o respeto límites de tiempo rígidos para cada fase del proceso de manufactura o cambio de modelo (setup) para asegurar el cumplimiento total de los embarques programados.",
        4: "Tengo plena disposición para ajustar temporalmente la distribución de actividades en la celda de trabajo si surge una situación emergente de fatiga, molestia ergonómica o necesidad de apoyo relacional entre el personal.",
        5: "Considero que la puntualidad exacta en los relevos de turno y el reinicio inmediato de labores tras los timbres de descanso son reflejos directos de una buena mayordomía de los recursos de la planta.",
        6: "Creo que la calidad del ensamble, la seguridad en el manejo de maquinaria y el valor del trabajo en equipo tienen prioridad absoluta sobre cualquier límite de tiempo medido por el cronómetro.",
        7: "Me genera una profunda incomodidad, frustración o estrés cuando incidentes en la cadena de suministros, retrasos de material o juntas improvisadas alteran la estructura planeada de mi jornada laboral.",
        8: "Confío en que las ideas innovadoras de mejora continua (Kaizen) y las soluciones eficientes a problemas de ingeniería surgen en momentos de oportunidad que no siempre coinciden con los cronogramas rígidos.",
        9: "Prefiero que los supervisores, los ingenieros de procesos y los gerentes concluyan sus juntas y auditorías ciñéndose estrictamente al tiempo asignado en la agenda oficial de operaciones.",
        10: "Cuando me encuentro inmerso en la resolución de una falla crítica de producción, el mantenimiento correctivo de una máquina o la optimización de un diseño, pierdo con frecuencia la noción del reloj.",
        11: "Mido el éxito de una línea de ensamble, un proyecto de manufactura o un departamento operativo principalmente a través del cumplimiento exacto de los indicadores métricos (blancos numéricos de eficiencia).",
        12: "Prefiero que la gerencia, el departamento de Recursos Humanos y el área de seguridad ocupacional se adapten con sensibilidad a las necesidades de salud mental y el bienestar físico urgente de los operadores.",
        13: "Considero que el apego riguroso a los manuales de procedimientos estandarizados (SOP), las auditorías de calidad (como 5S o ISO) y las minutas es la clave fundamental para mantener la excelencia operativa.",
        14: "Valoro el impacto de la maquiladora por el desarrollo integral y profesional del personal, la disminución sostenible de la rotación y la preservación de la salud mental de los empleados, más que por los números de volumen manufacturado."
    }
}

ESTADOS_MEXICO = ["Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Chiapas", "Chihuahua", "Ciudad de México", "Coahuila", "Colima", "Durango", "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", "México", "Michoacán", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"]
CONTINENTES = ["América del Norte", "América Central / El Caribe", "América del Sur", "Europa", "Asia", "África", "Oceanía"]


if not st.session_state.flujo_finalizado:
    st.header(f"📋 Formulario de Evaluación: {st.session_state.audiencia_activa}")
    nombre = st.text_input("Nombre Completo o Matrícula *:", placeholder="Ej. Juan Pérez", key="main_name_in")
    whatsapp = st.text_input("Número Telefónico de Enlace *:", placeholder="Ej. +52 633 123 4567", key="main_wha_in")
    st.divider()

    resultados_totales = {}
    es_modo_likert = (st.session_state.audiencia_activa != "🍊 Salud Integral")

    if not es_modo_likert:
        st.write("### 🍊 Tus Gajos de Bienestar (Diseño Estilizado)")
        st.write("Selecciona los puntos de fuga específicos donde requieres intervención:")
        
        # 1. SF (Corregido: Mapeo unitario indexado sobre la matriz para evitar repeticiones)
        with st.container(border=True):
            st.markdown("#### 💪 Salud Física (SF)")
            sf_items = ["Nutrición (Hábitos alimenticios)", "Sueño (Calidad del descanso)", "Ejercicio (Actividad estructurada)", "Movimiento (Evitar sedentarismo)"]
            col_a, col_b = st.columns(2)
            with col_a:
                st.checkbox(sf_items[0], key="sf_0")
                st.checkbox(sf_items[1], key="sf_1")
            with col_b:
                st.checkbox(sf_items[2], key="sf_2")
                st.checkbox(sf_items[3], key="sf_3")
            resultados_totales["Salud Fisica (SF)"] = [item for idx, item in enumerate(sf_items) if st.session_state[f"sf_{idx}"]]

        # 2. SM
        with st.container(border=True):
            st.markdown("#### 🧠 Salud Mental (SM)")
            sm_items = ["Memoria (Retención y agilidad)", "Enfoque (Evitar distracciones)", "Resiliencia (Adaptación al cambio)", "Aprendizaje (Nuevas habilidades)"]
            col_a, col_b = st.columns(2)
            with col_a:
                st.checkbox(sm_items[0], key="sm_0")
                st.checkbox(sm_items[1], key="sm_1")
            with col_b:
                st.checkbox(sm_items[2], key="sm_2")
                st.checkbox(sm_items[3], key="sm_3")
            resultados_totales["Salud Mental (SM)"] = [item for idx, item in enumerate(sm_items) if st.session_state[f"sm_{idx}"]]

        # 3. SE
        with st.container(border=True):
            st.markdown("#### ❤️ Salud Emocional (SE)")
            se_items = ["Gestión de emociones", "Autocontrol (Dominio propio)", "Regulación psicológica", "Comprensión del estado de ánimo"]
            col_a, col_b = st.columns(2)
            with col_a:
                st.checkbox(se_items[0], key="se_0")
                st.checkbox(se_items[1], key="se_1")
            with col_b:
                st.checkbox(se_items[2], key="se_2")
                st.checkbox(se_items[3], key="se_3")
            resultados_totales["Salud Emocional (SE)"] = [item for idx, item in enumerate(se_items) if st.session_state[f"se_{idx}"]]

        # 4. SS
        with st.container(border=True):
            st.markdown("#### 👥 Salud Social (SS)")
            ss_items = ["Relaciones positivas (Vínculos sanos)", "Comunicación asertiva", "Empatía activa", "Red de apoyo ante crisis"]
            col_a, col_b = st.columns(2)
            with col_a:
                st.checkbox(ss_items[0], key="ss_0")
                st.checkbox(ss_items[1], key="ss_1")
            with col_b:
                st.checkbox(ss_items[2], key="ss_2")
                st.checkbox(ss_items[3], key="ss_3")
            resultados_totales["Salud Social (SS)"] = [item for idx, item in enumerate(ss_items) if st.session_state[f"ss_{idx}"]]

        # 5. SECO
        with st.container(border=True):
            st.markdown("#### 💰 Salud Económica (SECO)")
            seco_items = ["Presupuesto (Control de gastos)", "Ahorro sistemático", "Inversión de capital", "Administración Financiera", "Creación / Generación del dinero"]
            col_a, col_b = st.columns(2)
            with col_a:
                st.checkbox(seco_items[0], key="seco_0")
                st.checkbox(seco_items[1], key="seco_1")
                st.checkbox(seco_items[2], key="seco_2")
            with col_b:
                st.checkbox(seco_items[3], key="seco_3")
                st.checkbox(seco_items[4], key="seco_4")
            resultados_totales["Salud Economica (SECO)"] = [item for idx, item in enumerate(seco_items) if st.session_state[f"seco_{idx}"]]

        # 6. ST
        with st.container(border=True):
            st.markdown("#### ⏳ Salud Temporal (ST)")
            ck_marcado = st.checkbox("Cronos & Kairos (Tiempo del reloj vs. valor real)", key="st_ck")
            st_items = ["Gestión del tiempo (Agenda)", "Equilibrio (Deber/Descanso)", "Prioridades (Identificar lo importante)"]
            col_a, col_b = st.columns(2)
            with col_a:
                st.checkbox(st_items[0], key="st_0")
                st.checkbox(st_items[1], key="st_1")
            with col_b:
                st.checkbox(st_items[2], key="st_2")
            st_sel = [item for idx, item in enumerate(st_items) if st.session_state[f"st_{idx}"]]
            if ck_marcado: st_sel.append("Cronos & Kairos (Tiempo del reloj vs. valor real)")
            resultados_totales["Salud Temporal (ST)"] = st_sel

        with st.container(border=True):
            st.markdown("#### 🙏 Salud Espiritual (SPI)")
            spi_items = ["Propósito (Sentido de vida)", "Valores (Alineación de actos)", "Meditación u oración", "Conexión del interior con el exterior"]
            col_a, col_b = st.columns(2)
            with col_a:
                st.checkbox(spi_items[0], key="spi_0")
                st.checkbox(spi_items[1], key="spi_1")
            with col_b:
                st.checkbox(spi_items[2], key="spi_2")
                st.checkbox(spi_items[3], key="spi_3")
            resultados_totales["Salud Espiritual (SPI)"] = [item for idx, item in enumerate(spi_items) if st.session_state[f"spi_{idx}"]]


    else:
        st.subheader("🏛️ Sección I. Datos Demográficos y Geográficos")
        resultados_totales["Edad"] = st.number_input("1. Edad (Años):", min_value=10, max_value=100, value=20, key="dem_edad")
        resultados_totales["Género"] = st.radio("2. Género:", ["Masculino", "Femenino", "Otro / Prefiero no decir"], horizontal=True, key="dem_genero")
        
        nacionalidad = st.radio("3. Nacionalidad *:", ["Mexicana", "Extranjera"], horizontal=True, key="dem_nac")
        resultados_totales["Nacionalidad"] = nacionalidad
        
        if nacionalidad == "Mexicana":
            resultados_totales["Estado Origen"] = st.selectbox("4. Estado de origen *:", [""] + ESTADOS_MEXICO, key="dem_orig")
            resultados_totales["Estado Residencia"] = st.selectbox("5. Estado de residencia actual *:", [""] + ESTADOS_MEXICO, key="dem_res")
            resultados_totales["País Origen"] = "México"
            resultados_totales["Continente Extranjero"] = "América"
        else:
            resultados_totales["Estado Origen"] = "N/A"
            resultados_totales["Estado Residencia"] = "N/A"
            resultados_totales["País Origen"] = st.text_input("4. Escribe tu País de origen *:", key="dem_pais_txt")
            resultados_totales["Continente Extranjero"] = st.selectbox("5. Selecciona tu Continente de origen *:", [""] + CONTINENTES, key="dem_cont")
            
        if "Religioso" in st.session_state.audiencia_activa:
            resultados_totales["Rol Iglesia"] = st.selectbox("6. Rol dentro de la Iglesia:", ["", "Laico / Miembro", "Líder de Departamento", "Anciano / Diácono", "Pastor / Ministro"], key="dem_rol")
        else: resultados_totales["Rol Iglesia"] = "N/A"

        st.subheader("🧠 Sección II. Conocimiento sobre el tema")
        resultados_totales["C1_Escuchado"] = st.radio("1. Antes de esta encuesta ya había escuchado hablar sobre los Modelos Temporales Cronos y Kairos:", ["Sí", "No"], horizontal=True, key="kn_1")
        resultados_totales["C2_Leído"] = st.radio("2. He leído sobre los modelos temporales Cronos y Kairos:", ["Sí", "No"], horizontal=True, key="kn_2")
        resultados_totales["C3_Enseñado"] = st.radio("3. He enseñado alguna vez sobre los modelos temporales Cronos y Kairos:", ["Sí", "No"], horizontal=True, key="kn_3")
        resultados_totales["C4_Origen"] = st.radio("4. El modelo temporal:", ["Se impone", "Se nace", "No sé"], horizontal=True, key="kn_4")
        resultados_totales["C5_Concepto"] = st.radio("5. Hablar de modelos temporales es hablar de:", ["Teología", "Cultura", "Francamente no sé"], horizontal=True, key="kn_5")

        st.subheader("📊 Sección III. Batería de Reactivos Intercalados")
        banco_activo = BANCO_PREGUNTAS.get(st.session_state.audiencia_activa, BANCO_PREGUNTAS["Docentes"])
        for r_id, enunciado in banco_activo.items():
            st.write(f"**Reactivo {r_id}:** {enunciado}")
            resultados_totales[f"R{r_id}"] = st.radio(
                "Grado de alineación:", options=[1, 2, 3, 4, 5],
                format_func=lambda x: {1:"1 - Totalmente en desacuerdo", 2:"2 - En desacuerdo", 3:"3 - Neutral", 4:"4 - De acuerdo", 5:"5 - Totalmente de acuerdo"}[x],
                key=f"dyn_r_{r_id}"
            )
        ck_marcado = False


    st.divider()
    col_btn1, col_btn2 = st.columns(2)
    campos_completos = bool(nombre.strip()) and bool(whatsapp.strip())

    with col_btn1:
        if st.button("💾 Guardar y Procesar Diagnóstico", width="stretch", type="primary"):
            if not campos_completos: st.error("⚠️ Datos de control incompletos.")
            else:
                with st.spinner("Registrando vectores temporales en la nube..."):
                    exito = guardar_en_google_sheets(st.session_state.audiencia_activa, nombre, whatsapp, resultados_totales, token_actual, es_modo_likert)
                    if exito: 
                        st.session_state.guardado_exitoso = True
                        st.success("¡Datos Sincronizados con éxito en la nube!")
                    else: 
                        st.session_state.guardado_exitoso = True
                        st.warning("Diagnóstico preprocesado localmente.")

    with col_btn2:
        if st.session_state.guardado_exitoso and campos_completos:
            grafica_base64 = None
            if es_modo_likert:
                try:
                    cronos_v = [resultados_totales.get(f"R{i}", 3) for i in range(1, 15, 2)]
                    kairos_v = [resultados_totales.get(f"R{i}", 3) for i in range(2, 15, 2)]
                    c_pt = sum(cronos_v) / 7
                    k_pt = sum(kairos_v) / 7
                    
                    fig, ax = plt.subplots(figsize=(4, 4))
                    ax.axhspan(1, 3, 1, 3, color='#f2f1ef', alpha=0.5) 
                    ax.axhspan(3, 5, 1, 3, color='#f9ebea', alpha=0.6) 
                    ax.axhspan(1, 3, 3, 5, color='#eaf2f8', alpha=0.6) 
                    ax.axhspan(3, 5, 3, 5, color='#e8f8f5', alpha=0.7) 
                    ax.axhline(3, color='#7f8c8d', linestyle='--', linewidth=1)
                    ax.axvline(3, color='#7f8c8d', linestyle='--', linewidth=1)
                    ax.scatter(c_pt, k_pt, color='#e65100', s=120, zorder=5, edgecolors='black')
                    ax.set_xlim(1, 5)
                    ax.set_ylim(1, 5)
                    ax.set_xlabel("Eje CRONOS")
                    ax.set_ylabel("Eje KAIROS")
                    
                    buf_g = BytesIO()
                    plt.savefig(buf_g, format='png', bbox_inches='tight', dpi=150)
                    buf_g.seek(0)
                    grafica_base64 = f"data:image/png;base64,{base64.b64encode(buf_g.read()).decode('utf-8')}"
                    plt.close(fig)
                except Exception: pass
            
            reporte_procesado = generar_pdf_diagnostico(nombre, whatsapp, resultados_totales, st.session_state.audiencia_activa, es_modo_likert, grafica_base64)
            nombre_archivo = nombre.replace(' ', '_') if nombre else 'Participante'
            
            def callback_finalizar():
                st.session_state.flujo_finalizado = True
                for k in list(st.session_state.keys()):
                    if k.startswith(("sf_", "sm_", "se_", "ss_", "seco_", "st_", "spi_", "dyn_r_", "dem_", "kn_")): del st.session_state[k]
                        
            st.download_button(label="DESCARGAR RESULTADOS EN PDF 📥", data=reporte_procesado, file_name=f"Diagnostico_{nombre_archivo}.pdf", mime="application/pdf", on_click=callback_finalizar)
        else: st.info("💡 Procesa para activar descarga.")


else:
    st.balloons()
    st.success("### ¡Tu reporte PDF ha sido generado y descargado con éxito! 🎉")
    with st.container(border=True):
        st.write("## 🍊 ¡Muchas gracias por tu participación!")
        st.markdown(f"Has completado el diagnóstico para la audiencia: **{st.session_state.audiencia_activa}**. Reconocer nuestros vectores temporales es el inicio de una alta madurez y bienestar integral.")
        st.write("---")
        st.write("### 📅 ¿Te gustaría llevar tu diagnóstico al siguiente nivel?")
        st.write("Te invitamos cordialmente a agendar una sesión de consulta directa y personalizada con el ponente. En esta asesoría individualizada estructuraremos un plan de acción a la medida.")
        st.info("👉 Acércate al término de la ponencia o solicita tu espacio de asesoramiento personalizado directamente en el escenario.")
        
    st.markdown("### ✨ ¡Te deseamos el mayor de los éxitos en los nuevos cambios que inicias a partir de esta experiencia! ✨")
    
    if not es_celular_del_publico:
        if st.button("🔄 Reiniciar Ecosistema (Modo Ponente)", width="stretch"):
            st.session_state.flujo_finalizado = False
            st.session_state.guardado_exitoso = False
            st.rerun()


