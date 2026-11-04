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

# --- ESTILOS CSS AVANZADOS: ÍCONO DE PERSONA EN EL CURSOR ---
st.markdown("""
<style>
    /* Cambia el punto azul del cursor de Streamlit por una persona caminando */
    div[data-testid="stSlider"] div[role="slider"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        width: 28px !important;
        height: 28px !important;
    }
    div[data-testid="stSlider"] div[role="slider"]::after {
        content: "🚶"; /* Ícono de la persona que se desplaza */
        font-size: 26px;
        position: absolute;
        top: -10px;
        left: -2px;
    }
    /* Estilización complementaria de la barra */
    div[data-testid="stSlider"] div[data-inner-slider="true"] {
        background-color: #e8f5e9 !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. Título de la aplicación y bienvenida principal
st.title("🌱 Diagnóstico Espiritual: Los 9 Frutos del Espíritu")
st.markdown("Este diagnóstico te ayudará a evaluar el estado actual de tu carácter basándose en **Gálatas 5:22-23**.")

# 3. Personalización por Nombre
nombre_usuario = st.text_input("✍️ Escribe tu nombre para personalizar tu reporte:", value="")

st.markdown("---")

# 4. ENLACE DE TU APLICACIÓN (Copia aquí tu link final de Streamlit Cloud)
url_base_app = "https://diagnosticofrutosdelespiritu.streamlit.app"

# 5. DETECCIÓN AUTOMÁTICA DEL ESCANEO: Ocultar QR al instante en el celular
# Añadimos un parámetro '?view=mobile' al QR para identificar al participante
query_params = st.query_params

if "view" not in query_params:
    st.markdown("### 📱 Escanea y Responde en tu Móvil")
    col_qr, col_txt = st.columns([1, 2])
    
    with col_qr:
        try:
            # Creamos un enlace dinámico que le avisa a la app que es un celular
            url_con_parametro = f"{url_base_app.strip()}?view=mobile"
            qr = segno.make_qr(url_con_parametro)
            buffer_qr = io.BytesIO()
            qr.save(buffer_qr, kind='png', scale=5)
            st.image(buffer_qr.getvalue(), use_container_width=True)
        except Exception:
            st.error("No se pudo generar el código QR.")
            
    with col_txt:
        st.markdown("""
        Si eres parte de la audiencia, acerca la cámara de tu celular al código QR de la izquierda. 
        
        *¡Al escanearlo, este recuadro con el QR desaparecerá por completo de tu pantalla móvil para darte máxima comodidad al responder!*
        """)
    st.markdown("---")

# 6. Diccionario de proyecciones para el reporte PDF final
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
st.header("📋 Autoevaluación")
st.subheader("Usa el cursor del caminante (🚶) para marcar tu posición en la escala del 1 al 10:")

# Diccionario con enunciados en primera persona
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

# Formulario estructurado con numeración y escala del 1 al 10
with st.form("diagnostico_form"):
    for i, (fruto, info) in enumerate(frutos_info.items(), 1):
        st.markdown(f"#### **{i}. {fruto}** <small>({info['cita']})</small>", unsafe_allow_html=True)
        
        # CORRECCIÓN: Escala explícita del 1 al 10 (mínimo 1, máximo 10)
        puntaje = st.slider(
            label=f"Desplaza el cursor: {info['izq']} ➔ {info['der']}",
            min_value=1,
            max_value=10,
            value=5,
            key=fruto
        )
        puntajes[fruto] = puntaje
        st.markdown("---")
    
    enviar = st.form_submit_button("Generar Diagnóstico")
# 7. Procesamiento posterior al envío
if enviar:
    nombre_final = nombre_usuario if nombre_usuario.strip() != "" else "Invitado"
    st.header(f"📊 Resultados de {nombre_final}")
    
    # Gráfico interactivo
    df = pd.DataFrame(list(puntajes.items()), columns=["Fruto del Espíritu", "Puntaje"])
    st.bar_chart(data=df.set_index("Fruto del Espíritu"))
    
    st.subheader("🔍 Análisis Detallado")
    fortalezas, atencion, criticos = [], [], []
    tabla_html = ""
    
    # Adaptación de rangos para la escala 1-10
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
        
    # Alertas visuales en pantalla
    if fortalezas:
        st.success(f"🌟 **Fortalezas (Puntaje 8-10):** {', '.join(fortalezas)}. ¡Sigue cultivándolas, {nombre_final}!")
    if atencion:
        st.warning(f"⚠️ **Áreas en desarrollo (Puntaje 5-7):** {', '.join(atencion)}. Tienes espacio para madurar.")
    if criticos:
        st.error(f"🚨 **Áreas críticas (Puntaje 1-4):** {', '.join(criticos)}. Mucha atención con estas conductas.")

    # Recomendaciones y cierre
    st.header("💡 Recomendaciones Generales")
    st.markdown("1. **Oración Enfocada:** Pide dirección específica por tus puntajes más bajos.\n"
                "2. **Acción Intencional:** Elige una virtud en desarrollo y practícala conscientemente esta semana.\n"
                "3. **Acompañamiento:** Comparte este mapa con un mentor o persona de confianza.")
    
    st.info(f"🤝 **¿Deseas profundizar, {nombre_final}?** Te invitamos a acercarte con el ponente para agendar una **consulta espiritual complementaria y 100% gratuita** para estructurar un plan personalizado.")

    # Reporte HTML adaptable para impresión limpia
    html_reporte = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset='utf-8'>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; line-height: 1.4; padding: 20px; }}
            .header {{ text-align: center; border-bottom: 3px solid #2e7d32; padding-bottom: 10px; }}
            .header h1 {{ color: #2e7d32; margin: 0; }}
            .user-info {{ text-align: right; font-style: italic; margin-top: 10px; color: #555; }}
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
        <div class='user-info'>Diagnóstico preparado especialmente para: <strong>{nombre_final}</strong></div>
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
            <p>Si deseas profundizar en tus resultados o estructurar un plan de acción guiado, te invitamos a <strong>acercarte directamente con el ponente</strong> para recibir una <strong>sesión de consultoría privada y completamente gratuita</strong>.</p>
        </div>
    </body>
    </html>
    """

    st.markdown("### 📥 Descarga tu Reporte Oficial")
    st.download_button(
        label=f"Descargar Reporte de {nombre_final} (PDF / HTML)",
        data=html_reporte,
        file_name=f"diagnostico_{nombre_final.lower().replace(' ', '_')}.html",
        mime="text/html"
    )
