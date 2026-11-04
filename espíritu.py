import streamlit as st
import pandas as pd
import segno  # Generador nativo de códigos QR
import io

# 1. Configuración de la página institucional
st.set_page_config(
    page_title="Diagnóstico: Los 9 Frutos del Espíritu",
    page_icon="🌱",
    layout="centered"
)

# Inicializar los estados de la aplicación para el control de pantallas
if "mostrar_felicitacion" not in st.session_state:
    st.session_state.mostrar_felicitacion = False

# --- INYECCIÓN CSS ROBUSTA PARA REEMPLAZAR EL PUNTO POR EL MONITO ---
st.markdown("""
<style>
    /* Apuntar globalmente al controlador/manija de cualquier slider en Streamlit */
    div[data-testid="stSlider"] [role="slider"],
    div[data-testid="stSlider"] [data-thumb="true"],
    .stSlider > div [role="slider"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        width: 35px !important;
        height: 35px !important;
    }
    
    /* Forzar la inyección del monito caminando */
    div[data-testid="stSlider"] [role="slider"]::after,
    div[data-testid="stSlider"] [data-thumb="true"]::after,
    .stSlider > div [role="slider"]::after {
        content: "🚶" !important;
        font-size: 32px !important;
        position: absolute !important;
        top: -15px !important;
        left: -4px !important;
        visibility: visible !important;
        display: block !important;
    }

    /* Quitar efectos de selección azules nativos */
    div[data-testid="stSlider"] [role="slider"]:focus,
    div[data-testid="stSlider"] [role="slider"]:active {
        box-shadow: none !important;
        outline: none !important;
    }

    /* Ocultar etiquetas flotantes numéricas redundantes */
    div[data-testid="stSlider"] div[data-testid="stWidgetMarkdownClaim"],
    div[data-testid="stSlider"] div[data-testid="stSliderValue"] {
        display: none !important;
    }

    /* Regla numérica fija debajo del slider */
    .escala-numerica {
        font-family: monospace;
        display: flex;
        justify-content: space-between;
        padding-left: 8px;
        padding-right: 8px;
        color: #2e7d32;
        font-weight: bold;
        margin-top: -12px;
        margin-bottom: 18px;
    }
</style>
""", unsafe_allow_html=True)

# LÓGICA DE PANTALLAS: Si ya descargó el PDF, ocultamos todo y mostramos la felicitación
if st.session_state.mostrar_felicitacion:
    st.balloons()
    st.success("🎉 ¡Muchas felicidades por completar este paso fundamental!")
    st.markdown("""
    ### 🚀 Tu camino de transformación empieza hoy
    Has descargado con éxito tu diagnóstico espiritual. El conocimiento sin acción no produce transformación; por ello, te invitamos a dar el **siguiente paso**:
    
    1. **Toma acciones para el cambio:** Elige el fruto con menor puntaje y realiza un acto consciente enfocado en él durante las próximas 48 horas.
    2. **Agenda tu Consulta Gratuita:** No camines solo. Acércate directamente con el ponente para revisar juntos tu reporte personalizado y estructurar un plan de acción guiado y 100% gratuito.
    """)
    if st.button("🔄 Volver a realizar la prueba"):
        st.session_state.mostrar_felicitacion = False
        st.rerun()
    st.stop() # Detiene la ejecución para ocultar el test de abajo por completo

# --- PANTALLA PRINCIPAL DEL TEST ---
st.title("🌱 Diagnóstico Espiritual: Los 9 Frutos del Espíritu")
st.markdown("Este diagnóstico te ayudará a evaluar el estado actual de tu carácter basándose en **Gálatas 5:22-23**.")

# Personalización por Nombre
nombre_usuario = st.text_input("✍️ Escribe tu nombre para personalizar tu reporte:", value="")
st.markdown("---")

# ENLACE DE TU APLICACIÓN (Copia aquí tu link final de Streamlit Cloud)
url_base_app = "https://diagnosticofrutosdelespiritu.streamlit.app"

# CONTROL DEL QR INTELIGENTE
query_params = st.query_params
if "view" not in query_params:
    st.markdown("### 📱 Escanea y Responde en tu Móvil")
    col_qr, col_txt = st.columns(2)
    with col_qr:
        try:
            url_con_parametro = f"{url_base_app.strip()}?view=mobile"
            qr = segno.make_qr(url_con_parametro)
            buffer_qr = io.BytesIO()
            qr.save(buffer_qr, kind='png', scale=5)
            st.image(buffer_qr.getvalue(), use_container_width=True)
        except Exception:
            st.error("No se pudo generar el código QR.")
    with col_txt:
        st.markdown("*¡Al escanearlo, este recuadro desaparecerá de tu pantalla móvil para darte máxima comodidad!*")
    st.markdown("---")

# DICCIONARIO DE CONSECUENCIAS PARA EL PDF
consecuencias_texto = {
    "critico": {
        "estado": "Crítico / Alerta",
        "corto": "Afectación inmediata en tus relaciones, arranques de impulsividad y pérdida de control emocional.",
        "mediano": "Desgaste de tu salud mental y física por estrés. Distanciamiento y estancamiento espiritual.",
        "largo": "Aislamiento emocional, decisiones destructivas crónicas y desconexión de tu propósito de vida."
    },
    "atencion": {
        "estado": "En Desarrollo / Atención",
        "corto": "Inconsistencia emocional. Vulnerabilidad ante situaciones de alta presión.",
        "mediano": "Relaciones con altibajos constantes. Sensación de cansancio por falta de hábitos firmes.",
        "largo": "Riesgo de estancarse en la mediocridad espiritual, viviendo debajo de tu madurez potencial."
    },
    "fortaleza": {
        "estado": "Fortaleza Espiritual",
        "corto": "Respuestas asertivas ante problemas cotidianos, paz interior evidente e impacto positivo.",
        "mediano": "Relaciones interpersonales saludables y duraderas. Resiliencia fortalecida frente a las crisis.",
        "largo": "Legado de madurez espiritual, estabilidad emocional duradera y capacidad de guiar a otros."
    }
}
# REQUERIMIENTO 1: Invitación a responder con total honestidad
st.warning("""
### 🧠 Invitación a la Honestidad Profunda
Antes de iniciar, tómate un momento de silencio. Este diagnóstico no es una calificación ni un examen para ser juzgado, sino un mapa real de tu estado actual. 
**Responde con total honestidad**, reconociendo tanto tus victorias como tus debilidades. La verdadera transformación comienza únicamente cuando somos capaces de aceptar nuestra realidad con humildad.
""")

st.header("📋 Autoevaluación")
st.subheader("Usa el cursor del caminante (🚶) para marcar tu posición en la escala del 1 al 10:")

frutos_info = {
    "Amor": {"izq": "A veces guardo rencor o elijo la indiferencia.", "der": "Amo y acepto a los demás sin condiciones.", "cita": "Gálatas 5:22"},
    "Gozo": {"izq": "Me gana la queja, la amargura o la tristeza.", "der": "Siento una alegría profunda que no cambia por las crisis.", "cita": "Gálatas 5:22"},
    "Paz": {"izq": "Vivo con ansiedad, discusiones o conflictos.", "der": "Tengo tranquilidad interna y busco la reconciliación.", "cita": "Gálatas 5:22"},
    "Paciencia": {"izq": "Me desespero o me irrito con facilidad.", "der": "Sé esperar con calma y tolerar los errores ajenos.", "cita": "Gálatas 5:22"},
    "Benignidad": {"izq": "Puedo llegar a ser duro o cortante al hablar.", "der": "Trato a todos con dulzura, empatía y amabilidad.", "cita": "Gálatas 5:22"},
    "Bondad": {"izq": "Pienso primero en mi beneficio o actúo con malicia.", "der": "Busco hacer el bien de forma activa y generosa.", "cita": "Gálatas 5:22"},
    "Fe": {"izq": "Dudo con frecuencia o rompo mis promesas.", "der": "Soy alguien fiel, confiable y que confía plenamente.", "cita": "Gálatas 5:22"},
    "Mansedumbre": {"izq": "Me defiendo con orgullo, soberbia o enojo.", "der": "Reacciono con humildad, suavidad y sin prepotencia.", "cita": "Gálatas 5:23"},
    "Templanza": {"izq": "Cedo fácil a los antojos, impulsos o vicios.", "der": "Tengo dominio propio y controlo mis emociones.", "cita": "Gálatas 5:23"}
}

puntajes = {}

with st.form("diagnostico_form"):
    for i, (fruto, info) in enumerate(frutos_info.items(), 1):
        st.markdown(f"#### **{i}. {fruto}** <small>({info['cita']})</small>", unsafe_allow_html=True)
        st.markdown(f"*De: {info['izq']} ➔ Hacia: {info['der']}*")
        
        puntaje = st.slider(
            label=f"Nivel de {fruto}",
            min_value=1,
            max_value=10,
            value=5,
            key=fruto,
            label_visibility="collapsed"
        )
        puntajes[fruto] = puntaje
        
        st.markdown("""
        <div class="escala-numerica">
            <span>1</span><span>2</span><span>3</span><span>4</span><span>5</span>
            <span>6</span><span>7</span><span>8</span><span>9</span><span>10</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
    
    enviar = st.form_submit_button("Generar Diagnóstico")
if enviar or st.session_state.get("guardar_progreso", False):
    st.session_state.guardar_progreso = True
    nombre_final = nombre_usuario if nombre_usuario.strip() != "" else "Invitado"
    
    st.header(f"📊 Resultados de {nombre_final}")
    df = pd.DataFrame(list(puntajes.items()), columns=["Fruto del Espíritu", "Puntaje"])
    st.bar_chart(data=df.set_index("Fruto del Espíritu"))
    
    fortalezas, atencion, criticos = [], [], []
    tabla_html = ""
    
    for fruto, score in puntajes.items():
        if score >= 8:
            fortalezas.append(fruto)
            cons = consecuencias_texto["fortaleza"]
        elif 5 <= score <= 7:
            atencion.append(fruto)
            cons = consecuencias_texto["atencion"]
        else:
            criticos.append(fruto)
            cons = consecuencias_texto["critico"]
            
        tabla_html += f"<tr><td style='font-weight: bold; color: #2e7d32;'>{fruto}</td><td style='text-align: center; font-weight: bold;'>{score}/10</td><td><strong>{cons['estado']}</strong></td><td>{cons['corto']}</td><td>{cons['mediano']}</td><td>{cons['largo']}</td></tr>"
        
    if fortalezas:
        st.success(f"🌟 **Fortalezas (Puntaje 8-10):** {', '.join(fortalezas)}.")
    if atencion:
        st.warning(f"⚠️ **Áreas en desarrollo (Puntaje 5-7):** {', '.join(atencion)}.")
    if criticos:
        st.error(f"🚨 **Áreas críticas (Puntaje 1-4):** {', '.join(criticos)}.")

    # REQUERIMIENTO 2: Botón de descarga con actualización de pantalla integrada
    html_reporte = f"<html><head><meta charset='utf-8'><style>body{{font-family:Arial;padding:20px;}}table{{width:100%;border-collapse:collapse;font-size:11px;}}th,td{{border:1px solid #ddd;padding:8px;}}th{{background-color:#f4fbf7;color:#2e7d32;}}</style></head><body><h2>🌱 Reporte de {nombre_final}</h2><table><thead><tr><th>Fruto</th><th>Puntaje</th><th>Estado</th><th>Corto Plazo</th><th>Mediano Plazo</th><th>Largo Plazo</th></tr></thead><tbody>{tabla_html}</tbody></table></body></html>"

    st.markdown("### 📥 Descarga tu Reporte Oficial")
    
    # Al hacer clic en descargar, el navegador procesa el archivo
    descarga = st.download_button(
        label="Descargar Reporte Completo (PDF / HTML)",
        data=html_reporte,
        file_name=f"diagnostico_{nombre_final.lower()}.html",
        mime="text/html"
    )
    
    # REQUERIMIENTO 2: Un botón confirmatorio para activar el siguiente paso y limpiar la pantalla
    st.markdown("---")
    if st.button("✅ Ya descargué mi reporte, avanzar al siguiente paso"):
        st.session_state.mostrar_felicitacion = True
        st.rerun()
