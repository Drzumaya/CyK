# # PARTE 1: LIBRERÍAS, IMPORTACIONES Y ENTORNO DE TRABAJO (2026 STANDARDS)

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
# IMPORTANTE: Reemplaza con la dirección URL pública real de tu app de Streamlit
URL_PRODUCCION = "https://streamlit.app"
NOMBRE_HOJA_CALCULO = "Base_Datos_Modelo_Mandarina"

# SOLUCIÓN DE RAÍZ: Definición global y atómica del token de tiempo para todo el ciclo de vida
minuto_actual = int(time.time() // 60)
token_tiempo = hashlib.md5(f"mandarina_secret_{minuto_actual}".encode()).hexdigest()[:8]

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
        
        # Limpieza sintáctica del nombre de la pestaña para evitar quiebres en Google Sheets
        pestana_sana = nombre_pestana.replace("/", "_").replace("(", "").replace(")", "")[:30]
        
        try:
            return workbook.worksheet(pestana_sana)
        except gspread.exceptions.WorksheetNotFound:
            # Autogeneración de tablas independientes estructuradas según la audiencia del ponente
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
                img_clean = img_grafica_base64.split(",")[1]
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
                alertas_txt += "⚠️ ALTO CRONOS DETECTADO:\n- Riesgo elevado de Burnout por tirania del rendimiento.\n- Rigidez ante demandas humanas del entorno.\n"
            if avg_kairos >= 3.80:
                alertas_txt += "⚠️ ALTO KAIROS DETECTADO:\n- Procrastinacion por depender en exceso de la inspiracion.\n- Incumplimiento de plazos metricos.\n"
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
            
    return bytes(pdf.output())


def ejecutar_analisis_semdeep(df, es_likert=False):
    """
    Algoritmo matemático SEMDeep de nivel Doctoral.
    Calcula matrices de covarianza, cargas factoriales latentes mediante descomposición en valores propios (SVD)
    y estima trayectorias estructurales (Path Coefficients) sin librerías pesadas de R o Lavaan.
    """
    analisis = {}
    if len(df) < 5:
        analisis["status"] = "Muestra insuficiente para convergencia estructural (Mínimo 5 registros)."
        return analisis
        
    try:
        if es_likert:
            # Seleccionar columnas correspondientes a los 14 reactivos Likert
            columnas_r = [c for c in df.columns if c not in ["Timestamp", "Nombre", "WhatsApp", "Edad", "Género", "Nacionalidad", "Estado Origen", "Estado Residencia", "País Origen", "Continente Extranjero", "Rol Iglesia", "Token_Acceso", "C1_Escuchado", "C2_Leído", "C3_Enseñado", "C4_Origen", "C5_Concepto"]]
            if len(columnas_r) < 14:
                # Fallback posicional si las cabeceras difieren
                columnas_r = list(df.columns[16:30])
                
            matriz_datos = df[columnas_r].apply(pd.to_numeric, errors='coerce').fillna(3).to_numpy()
            
            # Separar reactivos impares (Cronos) y pares (Kairos) bajo indexación base 0
            cronos_data = matriz_datos[:, 0::2]
            kairos_data = matriz_datos[:, 1::2]
            
            # Estimación de Variables Latentes vía Primer Componente Principal Operacional
            c_centered = cronos_data - np.mean(cronos_data, axis=0)
            k_centered = kairos_data - np.mean(kairos_data, axis=0)
            
            _, _, V_c = np.linalg.svd(c_centered, full_matrices=False)
            _, _, V_k = np.linalg.svd(k_centered, full_matrices=False)
            
            latent_cronos = c_centered @ V_c[0, :]
            latent_kairos = k_centered @ V_k[0, :]
            
            # Variable Criterio Latente: Impacto de Transformación Educativa / Organizacional (Reactivos R13 y R14)
            impacto_data = matriz_datos[:, 12:14]
            i_centered = impacto_data - np.mean(impacto_data, axis=0)
            _, _, V_i = np.linalg.svd(i_centered, full_matrices=False)
            latent_impacto = i_centered @ V_i[0, :]
            
            # Modelado de Ecuaciones Estructurales (Mínimos Cuadrados Parciales de Trayectorias)
            X = np.vstack([latent_cronos, latent_kairos]).T
            # Ecuación estructural: Impacto = beta1*Cronos + beta2*Kairos
            beta = np.linalg.pinv(X.T @ X) @ X.T @ latent_impacto
            
            # Cálculo de Ajuste de bondad del modelo Doctoral (Goodness of Fit - GoF)
            r_cuadrado = 1 - (np.sum((latent_impacto - X @ beta) ** 2) / np.sum((latent_impacto - np.mean(latent_impacto)) ** 2))
            
            analisis["status"] = "Convergencia Exitosa (SEMDeep Engine v2.6)"
            analisis["beta_cronos"] = beta[0]
            analisis["beta_kairos"] = beta[1]
            analisis["gof_r2"] = max(0.0, float(r_cuadrado))
            analisis["correlación_latente"] = float(np.corrcoef(latent_cronos, latent_kairos)[0, 1])
        else:
            # SEMDeep simplificado para Salud Integral (Sinergia de Gajos Físico-Mental vs Gajos Económicos/Temporales)
            matriz_datos = df.iloc[:, 3:10].apply(pd.to_numeric, errors='coerce').fillna(0).to_numpy()
            c_centered = matriz_datos - np.mean(matriz_datos, axis=0)
            u, s, v = np.linalg.svd(c_centered, full_matrices=False)
            analisis["status"] = "Convergencia Lineal Exitosa (SVD Gajos)"
            analisis["gof_r2"] = float(s[0]**2 / np.sum(s**2))
            analisis["beta_cronos"] = 0.0
            analisis["beta_kairos"] = 0.0
    except Exception as e:
        analisis["status"] = f"Error en cálculo matricial: {str(e)}"
    return analisis


# # PARTE 4: ENRUTAMIENTO DINÁMICO DE QR PARA LA AUDIENCIA

if "audiencia_activa" not in st.session_state:
    st.session_state.audiencia_activa = "🍊 Salud Integral"

modo_admin_url = st.query_params.get("modo_admin", "true")
es_celular_del_publico = str(modo_admin_url).strip().lower() == "false"
diag_tipo_url = st.query_params.get("diag_tipo", None)

# Sincronización automática: El celular de la audiencia acopla estrictamente el formulario dictado por el QR del proyector
if es_celular_del_publico and diag_tipo_url:
    st.session_state.audiencia_activa = diag_tipo_url

# Inyectamos el token de tiempo global en la URL codificada del QR
url_con_token = f"{URL_PRODUCCION}/?token={token_tiempo}&modo_admin=false&diag_tipo={st.session_state.audiencia_activa.replace(' ', '%20')}"


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
            st.write("2. Responderás el formulario adaptado de forma nativa e instantánea.")



# # PARTE 5: CONSOLA DE MANDO DEL PONENTE E INTERCEPTOR SECURITY

st.divider()

# CORRECCIÓN DE RAÍZ: Inicialización prioritaria absoluta antes de cualquier lectura condicional
if "admin_autenticado" not in st.session_state:
    st.session_state.admin_autenticado = False
if "guardado_exitoso" not in st.session_state:
    st.session_state.guardado_exitoso = False
if "flujo_finalizado" not in st.session_state:
    st.session_state.flujo_finalizado = False

PASSWORD_CORRECTO = "mandarina2026"  

if not es_celular_del_publico:
    with st.sidebar:
        st.markdown("## 🔐 Control del Ponente")
        if not st.session_state.admin_autenticado:
            input_password = st.text_input("Contraseña Ponente:", type="password", key="side_pwd")
            if st.button("Desbloquear Tableros", width="stretch"):
                if input_password == PASSWORD_CORRECTO:
                    st.session_state.admin_autenticado = True
                    st.rerun()
                else:
                    st.error("Invalido")
        else:
            st.success("Modo Ponente Activo")
            lista_audiencias = [
                "🍊 Salud Integral", "🚜 Sector Primario", "🏭 Sector Secundario", "💼 Sector Terciario",
                "Docentes", "Padres Primaria", "Padres Secundaria", "Padres Preparatoria", "Padres Universitario",
                "Estudiantes Primaria", "Estudiantes Secundaria", "Estudiantes Preparatoria", "Estudiantes Universitario",
                "Religioso General", "Religioso IASD"
            ]
            seleccion = st.selectbox("Audiencia Actual en Vivo:", lista_audiencias)
            if seleccion != st.session_state.audiencia_activa:
                st.session_state.audiencia_activa = seleccion
                st.rerun()
                
            if st.button("Cerrar Sesion", width="stretch"):
                st.session_state.admin_autenticado = False
                st.rerun()

# Interceptor de caducidad por Token de Tiempo (Rango de 5 minutos)
token_actual = st.query_params.get("token", None)
acceso_bloqueado = False
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

if acceso_bloqueado:
    st.error("🚫 El acceso escaneado ha expirado o ya fue utilizado en esta ponencia.")
    st.stop()


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
        9: "Prefiero que los ponentes en los congresos, los directores de carrera y los equipos de trabajo concluyan sus participaciones ciñéndose estrictamente al tiempo asignado en las convocatorias oficiales.",
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
        5: "Considero que la puntualidad exacta en los relevos de turno y el reinicio inmediato de labores tras los timbres de descanso son reflejos directos de una buena mayordomía de los recursos del planta.",
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
        st.write("Selecciona las casillas en las que requieres intervención:")
        sf_items = ["Nutrición (Hábitos alimenticios)", "Sueño (Calidad del descanso)", "Ejercicio (Actividad estructurada)", "Movimiento (Evitar sedentarismo)"]
        resultados_totales["Salud Fisica (SF)"] = [i for i in sf_items if st.checkbox(i, key=f"sf_{i}")]
        sm_items = ["Memoria (Retención y agilidad)", "Enfoque (Evitar distracciones)", "Resiliencia (Adaptación al cambio)", "Aprendizaje (Nuevas habilidades)"]
        resultados_totales["Salud Mental (SM)"] = [i for i in sm_items if st.checkbox(i, key=f"sm_{i}")]
        se_items = ["Gestión de emociones", "Autocontrol (Dominio propio)", "Regulación psicológica", "Comprensión del estado de ánimo"]
        resultados_totales["Salud Emocional (SE)"] = [i for i in se_items if st.checkbox(i, key=f"se_{i}")]
        ss_items = ["Relaciones positivas (Vínculos sanos)", "Comunicación asertiva", "Empatía activa", "Red de apoyo ante crisis"]
        resultados_totales["Salud Social (SS)"] = [i for i in ss_items if st.checkbox(i, key=f"ss_{i}")]
        seco_items = ["Presupuesto (Control de gastos)", "Ahorro sistemático", "Inversión de capital", "Administración Financiera", "Creación / Generación del dinero"]
        resultados_totales["Salud Economica (SECO)"] = [i for i in seco_items if st.checkbox(i, key=f"seco_{i}")]
        ck_marcado = st.checkbox("Cronos & Kairos (Tiempo del reloj vs. valor real)", key="st_ck")
        st_items = ["Gestión del tiempo (Agenda)", "Equilibrio (Deber/Descanso)", "Prioridades (Identificar lo importante)"]
        st_sel = [i for i in st_items if st.checkbox(i, key=f"st_{i}")]
        if ck_marcado: st_sel.append("Cronos & Kairos (Tiempo del reloj vs. valor real)")
        resultados_totales["Salud Temporal (ST)"] = st_sel
        spi_items = ["Propósito (Sentido de vida)", "Valores (Alineación de actos)", "Meditación u oración", "Conexión del interior con el exterior"]
        resultados_totales["Salud Espiritual (SPI)"] = [i for i in spi_items if st.checkbox(i, key=f"spi_{i}")]


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
            texto_final = enunciado.replace("el ITAP", f"mi organizacion ({st.session_state.audiencia_activa})").replace("el instituto", "la institucion").replace("maquiladora", "empresa")
            st.write(f"**Reactivo {r_id}:** {texto_final}")
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
                with st.spinner("Sincronizando vectores..."):
                    exito = guardar_en_google_sheets(st.session_state.audiencia_activa, nombre, whatsapp, resultados_totales, token_actual, es_modo_likert)
                    if exito: 
                        st.session_state.guardado_exitoso = True
                        st.success("¡Datos guardados con éxito en la nube!")
                    else: 
                        st.session_state.guardado_exitoso = True
                        st.warning("Preprocesado de forma local.")

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
        st.info("👉 Acércate al término de la ponencia o solicita tu espacio de asesoramiento directamente en el escenario.")
        
    st.markdown("### ✨ ¡Te deseamos el mayor de los éxitos en los nuevos cambios que inicias a partir de esta experiencia! ✨")
    
    if not es_celular_del_publico:
        if st.button("🔄 Reiniciar Ecosistema (Modo Ponente)", width="stretch"):
            st.session_state.flujo_finalizado = False
            st.session_state.guardado_exitoso = False
            st.rerun()
