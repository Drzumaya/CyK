
import streamlit as st
import pandas as pd
import urllib.parse

# 1. Configuración inicial de la página
st.set_page_config(
    page_title="Diagnóstico: Los 9 Frutos del Espíritu",
    page_icon="🌱",
    layout="centered"
)

# 2. Generación dinámica de Código QR en la barra lateral
st.sidebar.header("📱 Acceso para la Audiencia")
url_app = st.sidebar.text_input(
    "URL de esta aplicación:", 
    value="https://streamlit.io"
)

if url_app:
    url_codificada = urllib.parse.quote(url_app)
    qr_api_url = f"https://googleapis.com{url_codificada}&choe=UTF-8"
    st.sidebar.image(qr_api_url, caption="¡Escanea para responder en tu móvil!", use_container_width=True)

st.sidebar.markdown("---")

# 3. Estructura de Datos: Frutos, Citas y Antónimos
frutos_info = {
    "Amor": {"antonimo": "Odio", "cita": "Gálatas 5:22"},
    "Gozo": {"antonimo": "Tristeza / Amargura", "cita": "Gálatas 5:22"},
    "Paz": {"antonimo": "Discordia / Conflicto", "cita": "Gálatas 5:22"},
    "Paciencia": {"antonimo": "Impaciencia / Intolerancia", "cita": "Gálatas 5:22"},
    "Benignidad": {"antonimo": "Crueldad / Aspereza", "cita": "Gálatas 5:22"},
    "Bondad": {"antonimo": "Malicia / Maldad", "cita": "Gálatas 5:22"},
    "Fe": {"antonimo": "Infidelidad / Deslealtad", "cita": "Gálatas 5:22"},
    "Mansedumbre": {"antonimo": "Arrogancia / Ira", "cita": "Gálatas 5:23"},
    "Templanza": {"antonimo": "Descontrol / Desenfreno", "cita": "Gálatas 5:23"}
}

# 4. Diccionario de proyecciones y consecuencias
consecuencias_texto = {
    "critico": {
        "estado": "Crítico / Alerta",
        "corto": "Afectación inmediata en tus relaciones cercanas, arranques de impulsividad y pérdida de control emocional.",
        "mediano": "Desgaste de tu salud mental y física por estrés. Distanciamiento de seres queridos y estancamiento espiritual.",
        "largo": "Aislamiento emocional, decisiones destructivas crónicas y desconexión profunda de tu propósito de vida."
    },
    "atencion": {
        "estado": "En Desarrollo / Atención",
        "corto": "Inconsistencia emocional. Te mantienes a flote pero experimentas vulnerabilidad ante alta presión.",
        "mediano": "Relaciones con altibajos constantes. Sensación de cansancio por no consolidar hábitos firmes.",
        "largo": "Riesgo de estancarse en la mediocridad espiritual, viviendo por debajo de tu madurez potencial."
    },
    "fortaleza": {
        "estado": "Fortaleza Espiritual",
        "corto": "Respuestas asertivas ante problemas cotidianos, paz interior evidente e impacto positivo en tu entorno.",
        "mediano": "Relaciones interpersonales saludables y duraderas. Resiliencia fortalecida frente a las crisis.",
        "largo": "Legado de madurez espiritual, estabilidad emocional duradera y capacidad de guiar efectivamente a otros."
    }
}
# 5. Título principal de la aplicación
st.title("🌱 Diagnóstico Espiritual: Los 9 Frutos del Espíritu")
st.markdown("""
Este diagnóstico te ayudará a evaluar el estado actual de tu carácter basándose en **Gálatas 5:22-23**. 
Mueve el deslizador según cómo te identifiques hoy: el extremo izquierdo representa la tendencia negativa (antónimos) y el extremo derecho representa el fruto reflejado en tu vida.
""")

st.header("📋 Autoevaluación")
st.subheader("Escala del 0 (Antónimo) al 10 (Fruto)")

# Inicializar diccionario para capturar las respuestas del usuario
puntajes = {}

# Formulario de entrada
with st.form("diagnostico_form"):
    for fruto, info in frutos_info.items():
        st.markdown(f"#### **{fruto}** <small>({info['cita']})</small>", unsafe_allow_html=True)
        
        puntaje = st.slider(
            label=f"De {info['antonimo']} ➔ Hacia {fruto}",
            min_value=0,
            max_value=10,
            value=5,
            key=fruto
        )
        puntajes[fruto] = puntaje
        st.markdown("---")
    
    # Botón de activación del diagnóstico
    enviar = st.form_submit_button("Generar Diagnóstico")
# 6. Procesamiento posterior al envío del formulario
if enviar:
    st.header("📊 Tus Resultados")
    
    # Renderizar gráfico de barras interactivo
    df = pd.DataFrame(list(puntajes.items()), columns=["Fruto del Espíritu", "Puntaje"])
    st.bar_chart(data=df.set_index("Fruto del Espíritu"))
    
    st.subheader("🔍 Análisis Detallado")
    fortalezas, atencion, criticos = [], [], []
    tabla_html = ""
    
    # Clasificación por rangos y ensamblaje de la tabla para el PDF
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
            
        tabla_html += f"""
        <tr>
            <td style='font-weight: bold; color: #2e7d32;'>{fruto}</td>
            <td style='text-align: center; font-weight: bold;'>{score}/10</td>
            <td><strong>{cons['estado']}</strong></td>
            <td>{cons['corto']}</td>
            <td>{cons['mediano']}</td>
            <td>{cons['largo']}</td>
        </tr>
        """
        
    # Mensajes visuales en pantalla
    if fortalezas:
        st.success(f"🌟 **Fortalezas (Puntaje 8-10):** {', '.join(fortalezas)}. ¡Sigue cultivándolas!")
    if atencion:
        st.warning(f"⚠️ **Áreas en desarrollo (Puntaje 5-7):** {', '.join(atencion)}. Espacio para madurar.")
    if criticos:
        st.error(f"🚨 **Áreas críticas (Puntaje 0-4):** {', '.join(criticos)}. Alerta hacia tendencias restrictivas.")

    # Caja de recomendaciones y llamado a la acción
    st.header("💡 Recomendaciones Generales")
    st.markdown("1. **Oración Enfocada:** Prioriza en intimidad las áreas de menor puntaje.\n"
                "2. **Acción Intencional:** Elige un fruto en desarrollo y haz un acto consciente esta semana.\n"
                "3. **Rendición de Cuentas:** Comparte este diagnóstico con alguien de confianza.")
    
    st.info("🤝 **¿Deseas profundizar?** Acércate con el ponente para agendar una **consulta espiritual complementaria y 100% gratuita**.")

    # Compilación final del Reporte HTML imprimible a PDF
    html_reporte = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset='utf-8'>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; line-height: 1.4; padding: 20px; }}
            .header {{ text-align: center; border-bottom: 3px solid #2e7d32; padding-bottom: 10px; }}
            .header h1 {{ color: #2e7d32; margin: 0; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 11px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f4fbf7; color: #2e7d32; }}
            .promo-box {{ background-color: #e8f5e9; border-left: 5px solid #2e7d32; padding: 15px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class='header'>
            <h1>🌱 Reporte de Diagnóstico Espiritual</h1>
            <p>Los 9 Frutos del Espíritu (Gálatas 5:22-23)</p>
        </div>
        <table>
            <thead>
                <tr>
                    <th>Fruto</th><th>Puntaje</th><th>Estado</th><th>Corto Plazo</th><th>Mediano Plazo</th><th>Largo Plazo</th>
                </tr>
            </thead>
            <tbody>{tabla_html}</tbody>
        </table>
        <div class='promo-box'>
            <h3>🤝 Invitación Especial: Consulta Personalizada Gratuita</h3>
            <p>Si deseas profundizar en tus resultados o estructurar un plan de acción guiado, te invitamos a <strong>acercarte con el ponente</strong> para recibir una <strong>sesión de consultoría privada y completamente gratuita</strong>.</p>
        </div>
    </body>
    </html>
    """

    # Botón de Descarga
    st.markdown("### 📥 Descarga tu Reporte Oficial")
    st.download_button(
        label="Descargar Reporte Completo (PDF / HTML)",
        data=html_reporte,
        file_name="diagnostico_frutos_espiritu.html",
        mime="text/html"
    )
