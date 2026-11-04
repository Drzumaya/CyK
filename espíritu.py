import streamlit as st
import pandas as pd
import segno  # Generador nativo de códigos QR
import io
import base64  # Para incrustar la gráfica de mandarina en el PDF
import matplotlib.pyplot as plt # Librería para la gráfica Mandarina

# 1. Configuración de la página institucional
st.set_page_config(
    page_title="Diagnóstico: Los 9 Frutos del Espíritu",
    page_icon="🌱",
    layout="centered"
)

# Inicializar los estados de la aplicación para el control de pantallas
if "mostrar_felicitacion" not in st.session_state:
    st.session_state.mostrar_felicitacion = False
if "finalizado" not in st.session_state:
    st.session_state.finalizado = False
if "diagnostico_generado" not in st.session_state:
    st.session_state.diagnostico_generado = False
if "respuestas_usuario" not in st.session_state:
    st.session_state.respuestas_usuario = {}

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

# LÓGICA DE DESPEDIDA DEFINITIVA
if st.session_state.finalizado:
    st.success("👋 ¡Gracias por tu participación!")
    st.markdown("""
    ### El diagnóstico ha concluido de forma exitosa
    Tu sesión se ha cerrado de manera segura. Si descargaste tu reporte, no olvides guardarlo muy bien y ponerte en contacto con tu pastor o un anciano de confianza.
    
    *Que este mapa sea el inicio de un gran caminar espiritual.*
    """)
    st.stop()

# LÓGICA DE FELICITACIÓN: Se activa al terminar el flujo
if st.session_state.mostrar_felicitacion:
    st.balloons()
    st.success("🎉 ¡Muchas felicidades por completar este paso fundamental!")
    st.markdown("""
    ### 🚀 Tu camino de transformación empieza hoy
    Has descargado con éxito tu diagnóstico espiritual. El conocimiento sin acción no produce transformación; por ello, te invitamos a dar el **siguiente paso**:
    
    1. **Toma acciones para el cambio:** Elige el fruto con menor puntaje y realiza un acto consciente enfocado en él durante las próximas 48 horas.
    2. **Busca Consejo Pastoral:** No camines solo. Te animamos a acercarte directamente con tu **pastor o con un anciano de confianza** de tu iglesia para revisar juntos tu reporte personalizado, recibir guía espiritual y estructurar un plan de crecimiento guiado.
    """)
    if st.button("🏁 Terminar Diagnóstico"):
        st.session_state.finalizado = True
        st.session_state.mostrar_felicitacion = False
        st.rerun()
    st.stop()
# BASE DE DATOS LOCAL: Consecuencias según rango
consecuencias_texto = {
    "critico": {"estado": "Crítico / Alerta", "corto": "Afectación inmediata en tus relaciones, arranques de impulsividad y pérdida de control.", "mediano": "Desgaste de tu salud por estrés. Distanciamiento y estancamiento espiritual.", "largo": "Aislamiento emocional, decisiones destructivas y desconexión de tu propósito de vida."},
    "atencion": {"estado": "En Desarrollo / Atención", "corto": "Inconsistencia emocional. Vulnerabilidad ante situaciones de alta presión.", "mediano": "Relaciones con altibajos. Sensación de cansancio por falta de hábitos firmes.", "largo": "Riesgo de estancarse en la mediocridad espiritual, viviendo debajo de tu madurez potencial."},
    "fortaleza": {"estado": "Fortaleza Espiritual", "corto": "Respuestas asertivas ante problemas, paz interior e impacto positivo diario.", "mediano": "Relaciones saludables y duraderas. Resiliencia fortalecida frente a las crisis.", "largo": "Legado de madurez espiritual, estabilidad emocional y capacidad de guiar a otros."}
}

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

# FLUJO CONDICIONAL: SI NO SE HA GENERADO EL TEST, SE VISUALIZA LA BATERÍA
if not st.session_state.diagnostico_generado:
    st.title("🌱 Diagnóstico Espiritual: Los 9 Frutos del Espíritu")
    st.markdown("Este diagnóstico te ayudará a evaluar el estado actual de tu carácter basándose en **Gálatas 5:22-23**.")

    nombre_usuario = st.text_input("✍️ Escribe tu nombre para personalizar tu reporte:", value="")
    st.markdown("---")

    # CONTROL DEL QR INTELIGENTE QUE SE OCULTA AL INSTANTE EN MÓVILES
    url_base_app = "https://diagnosticofrutosdelespiritu.streamlit.app"
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

    st.warning("""
    ### 🧠 Invitación a la Honestidad Profunda
    Antes de iniciar, tómate un momento de silencio. Este diagnóstico no es una calificación ni un examen para ser juzgado, sino un mapa real de tu estado actual. 
    **Responde con total honestidad**, reconociendo tanto tus victorias como tus debilidades. La verdadera transformación comienza únicamente cuando somos capaces de aceptar nuestra realidad con humildad.
    """)

    st.header("📋 Autoevaluación")
    st.subheader("Usa el cursor del caminante (🚶) para marcar tu posición en la escala del 1 al 10:")

    with st.form("diagnostico_form"):
        puntajes_temporales = {}
        for i, (fruto, info) in enumerate(frutos_info.items(), 1):
            st.markdown(f"#### **{i}. {fruto}** <small>({info['cita']})</small>", unsafe_allow_html=True)
            st.markdown(f"*De: {info['izq']} ➔ Hacia: {info['der']}*")
            
            puntaje = st.slider(
                label=f"Nivel de {fruto}", min_value=1, max_value=10, value=5, key=fruto, label_visibility="collapsed"
            )
            puntajes_temporales[fruto] = puntaje
            
            st.markdown("""
            <div class="escala-numerica">
                <span>1</span><span>2</span><span>3</span><span>4</span><span>5</span>
                <span>6</span><span>7</span><span>8</span><span>9</span><span>10</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("---")
        
        enviar = st.form_submit_button("Generar Diagnóstico")
        
        if enviar:
            st.session_state.respuestas_usuario = puntajes_temporales
            st.session_state.nombre_final = nombre_usuario if nombre_usuario.strip() != "" else "Invitado"
            st.session_state.diagnostico_generado = True
            st.rerun()
# PANTALLA EXCLUSIVA DE RESULTADOS (CUANDO YA SE GENERÓ)
else:
    nombre_final = st.session_state.nombre_final
    puntajes = st.session_state.respuestas_usuario

    st.title("📊 Tu Diagnóstico Espiritual")
    st.header(f"Resultados preparados para: {nombre_final}")
    
    st.subheader("🍊 Distribución Porcentual (Gráfica Mandarina)")
    
    labels = list(puntajes.keys())
    valores = list(puntajes.values())
    colores_mandarina = ['#FF6B35', '#FF9F1C', '#F15BB5', '#E63946', '#FFD166', '#06D6A0', '#118AB2', '#073B4C', '#8338EC']
    
    # Crear gráfico Mandarina en memoria local del servidor
    fig, ax = plt.subplots(figsize=(5, 5))
    wedges, texts, autotexts = ax.pie(
        valores, labels=labels, autopct='%1.1f%%', startangle=90, colors=colores_mandarina,
        textprops=dict(color="black", weight="bold"), pctdistance=0.75
    )
    circulo_centro = plt.Circle((0,0), 0.55, fc='white')
    fig.gca().add_artist(circulo_centro)
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(9)
        
    ax.axis('equal')  
    plt.tight_layout()
    
    # Desplegar gráfica en pantalla
    st.pyplot(fig)
    
    # Convertir gráfica a datos puros base64 para el PDF descargable
    buffer_img = io.BytesIO()
    plt.savefig(buffer_img, format='png', dpi=150, bbox_inches='tight')
    buffer_img.seek(0)
    img_base64 = base64.b64encode(buffer_img.read()).decode('utf-8')
    plt.close(fig)
    
    st.markdown("---")
    st.subheader("🔍 Análisis Detallado")
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
        
    if fortalezas: st.success(f"🌟 **Fortalezas (Puntaje 8-10):** {', '.join(fortalezas)}.")
    if atencion: st.warning(f"⚠️ **Áreas en desarrollo (Puntaje 5-7):** {', '.join(atencion)}.")
    if criticos: st.error(f"🚨 **Áreas críticas (Puntaje 1-4):** {', '.join(criticos)}.")

    # Recomendaciones en pantalla enfocadas
    st.header("💡 Recomendaciones Generales")
    st.markdown("1. **Oración Enfocada:** Pide dirección específica por tus puntajes más bajos.\n"
                "2. **Acción Intencional:** Elige una virtud en desarrollo y practícala conscientemente esta semana.\n"
                "3. **Acompañamiento:** Comparte este mapa con tu pastor o un anciano de confianza.")
    
    st.info(f"🤝 **¿Deseas profundizar, {nombre_final}?** Te invitamos a acercarte con tu **pastor o con un anciano de confianza** para compartir estos resultados y recibir consejería espiritual personalizada.")

    # Diseño del reporte imprimible (HTML) con la gráfica y el enfoque pastoral
    html_reporte = f"""
    <html>
    <head>
        <meta charset='utf-8'>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; line-height: 1.4; padding: 20px; }}
            .header {{ text-align: center; border-bottom: 3px solid #2e7d32; padding-bottom: 10px; }}
            .header h1 {{ color: #2e7d32; margin: 0; }}
            .user-info {{ text-align: right; font-style: italic; margin-top: 10px; color: #555; }}
            .contenedor-grafica {{ text-align: center; margin: 20px 0; }}
            .contenedor-grafica img {{ width: 320px; }}
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
        
        <div class='contenedor-grafica'>
            <h3>🍊 Gráfica Mandarina de Proporciones</h3>
            <img src='data:image/png;base64,{img_base64}' />
        </div>

        <table>
            <thead>
                <tr><th>Fruto</th><th>Puntaje</th><th>Estado</th><th>Corto Plazo</th><th>Mediano Plazo</th><th>Largo Plazo</th></tr>
            </thead>
            <tbody>{tabla_html}</tbody>
        </table>
        
        <div class='promo-box'>
            <h3>🤝 Acompañamiento y Cuidado Espiritual</h3>
            <p>Si deseas profundizar en estos resultados, comprender mejor las áreas en desarrollo detectadas o estructurar un plan de madurez guiado, te invitamos a <strong>acercarte directamente con tu pastor o con un anciano de confianza</strong> de tu congregación. Compartir este reporte facilitará un espacio de oración y edificación mutua.</p>
        </div>
    </body>
    </html>
    """

    st.markdown("### 📥 Descarga tu Reporte Oficial")
    st.download_button(
        label="Descargar Reporte Completo (PDF / HTML)",
        data=html_reporte,
        file_name=f"diagnostico_{nombre_final.lower()}.html",
        mime="text/html"
    )
    
    st.markdown("---")
    if st.button("✅ Ya descargué mi reporte, avanzar al siguiente paso"):
        st.session_state.mostrar_felicitacion = True
        st.rerun()
