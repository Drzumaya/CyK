import streamlit as st
import pandas as pd
import segno
import io
import base64
import matplotlib.pyplot as plt

# 1. Configuración de la página institucional
st.set_page_config(
    page_title="Diagnóstico: Los 9 Frutos del Espíritu",
    page_icon="🌱",
    layout="centered"
)

# Inicializar los estados de la aplicación para el control de pantallas
for var, val in [("mostrar_felicitacion", False), ("finalizado", False), ("diagnostico_generado", False), ("respuestas_usuario", {})]:
    if var not in st.session_state:
        st.session_state[var] = val

# --- INYECCIÓN DE ESTILOS CSS PARA LA REGLA NUMÉRICA VISIBLE ---
st.markdown("""
<style>
    .escala-numerica-fija {
        font-family: 'Courier New', Courier, monospace;
        display: flex;
        justify-content: space-between;
        padding-left: 12px;
        padding-right: 15px;
        color: #2e7d32;
        font-weight: bold;
        font-size: 14px;
        margin-top: -10px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# LÓGICA DE DESPEDIDA DEFINITIVA
if st.session_state.finalizado:
    st.success("👋 ¡Gracias por tu participación!")
    st.markdown("""
    ### El diagnóstico ha concluido de forma exitosa
    Tu sesión se ha cerrado de manera segura. Si descargaste tu reporte, no olvides guardarlo muy bien y ponerte en contacto con tu pastor o un anciano de confianza.
    """)
    st.caption("🎨 Diagnóstico Espiritual desarrollado por **Jacob Zumaya Prianti**.")
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
    
    st.markdown("---")
    if st.button("🔄 Nuevo diagnóstico"):
        st.session_state.diagnostico_generado = False
        st.session_state.mostrar_felicitacion = False
        st.session_state.respuestas_usuario = {}
        st.rerun()
        
    st.caption("🎨 Diagnóstico Espiritual desarrollado por **Jacob Zumaya Prianti**.")
    st.stop()
# --- RÚBRICA DOCTRINAL AMPLIADA (BASADA EN LA BIBLIA Y EGW) ---
rubrica_teologica = {
    "1-3": {
        "estado": "Estado Carnal / Alerta Crítica (Jeremías 17:9 / EGW: 'Mente sin Regenerar')",
        "criterio": "El carácter es dominado por impulsos naturales y reacciones reactivas. Falta una sumisión diaria al Espíritu Santo, lo que perpetúa los antónimos de los frutos como conductas arraigadas. EGW señala: 'La mente carnal no puede cooperar con Dios; está en enemistad con Su ley'."
    },
    "4-5": {
        "estado": "Esfuerzo Humano Inconstante / Tibieza (Apocalipsis 3:16 / EGW: 'Religiosidad de Formas')",
        "criterio": "Se intenta vivir la fe mediante la fuerza de voluntad y el legalismo humano, lo que genera una experiencia de altibajos. Hay un conocimiento teórico de la verdad, pero flaquea bajo la tentación o provocación. EGW afirma: 'Los esfuerzos propios nunca transformarán el corazón; la forma sin el poder es una burla'."
    },
    "6-7": {
        "estado": "Crecimiento en Transición / Victoria Parcial (Filipenses 1:6 / EGW: 'Conflicto del Yo')",
        "criterio": "Experiencia activa de santificación donde el 'Yo' es confrontado diariamente. Se manifiestan victorias evidentes en la paciencia y el amor, pero persisten áreas vulnerables donde la carne aún batalla por el control. EGW indica: 'La santificación es la obra de toda una vida; cada día exige morir al Yo'."
    },
    "8-9": {
        "estado": "Madurez Consecuente / Carácter Reflejado (Gálatas 2:20 / EGW: 'Reflejo de la Imagen')",
        "criterio": "Evidencia constante de una vida crucificada con Cristo. Las virtudes bíblicas brotan de manera natural y habitual, trayendo estabilidad emocional y madurez ministerial duradera. EGW resalta: 'Cuando el carácter de Cristo sea perfectamente reproducido en Su pueblo, Él vendrá'."
    },
    "10": {
        "estado": "Plenitud de Permanencia / Consagración Total (Juan 15:5 / EGW: 'Comunión Ininterrumpida')",
        "criterio": "Punto de entrega absoluta y comunión ininterrumpida con la Vid Verdadera. El dominio propio, el amor incondicional y la fe inquebrantable gobiernan cada pensamiento y acción de forma plena y santa. EGW define: 'Estar escondido con Cristo en Dios es la seguridad y el reposo perfecto del alma'."
    }
}

consecuencias_texto = {
    "1-3": "Provoca rupturas relacionales continuas, arranques de ira o amargura que dañan el hogar, debilita severamente el testimonio cristiano ante el mundo y bloquea la recepción de las bendiciones divinas.",
    "4-5": "Genera inestabilidad emocional, desánimo recurrente al fallar y una experiencia espiritual monótona o cansada que vulnera tu liderazgo ante crisis inesperadas.",
    "6-7": "Produce un impacto positivo intermitente en la iglesia y la familia, pero la falta de constancia genera confusión o desconfianza momentánea en tu entorno en momentos de alta presión.",
    "8-9": "Actúa como un faro de estabilidad emocional en tu entorno, inspira resiliencia en tu congregación frente a las pruebas comunes y edifica lazos familiares sólidos basados en el pacto eterno.",
    "10": "Funge como un canal inquebrantable de la gracia divina, desarma conflictos mediante la mansedumbre santa y deja un legado de santidad que guía efectivamente a las nuevas generaciones."
}

frutos_info = {
    "Amor": {"izq": "Guardo rencor, elijo el egoísmo o la indiferencia.", "der": "Amo, perdono y acepto a los demás sin condiciones.", "cita": "Gálatas 5:22"},
    "Gozo": {"izq": "Me domina la queja constante, la amargura o la tristeza.", "der": "Siento una alegría profunda que no depende de las circunstancias.", "cita": "Gálatas 5:22"},
    "Paz": {"izq": "Vivo atrapado en la ansiedad, la preocupación o los conflictos.", "der": "Tengo tranquilidad interna y soy un agente de reconciliación.", "cita": "Gálatas 5:22"},
    "Paciencia": {"izq": "Me desespero rápido, me irrito y soy intolerante.", "der": "Sé esperar los tiempos de Dios con calma y tolero las flaquezas ajenas.", "cita": "Gálatas 5:22"},
    "Benignidad": {"izq": "Puedo llegar a ser duro, crítico o muy cortante al hablar.", "der": "Trato a todos con extrema dulzura, empatía y afabilidad.", "cita": "Gálatas 5:22"},
    "Bondad": {"izq": "Busco primero mi propio beneficio o actúo con doblez.", "der": "Hago el bien de forma activa, generosa, íntegra y desinteresada.", "cita": "Gálatas 5:22"},
    "Fe": {"izq": "Dudo constantemente de las promesas de Dios y soy desleal.", "der": "Soy una persona fiel, plenamente confiable y con fe inquebrantable.", "cita": "Gálatas 5:22"},
    "Mansedumbre": {"izq": "Me defiendo con orgullo, soberbia, prepotencia o enojo.", "der": "Reacciono con humildad, suavidad de espíritu y total sumisión a Dios.", "cita": "Gálatas 5:23"},
    "Templanza": {"izq": "Cedo con facilidad ante los antojos, impulsos o malos hábitos.", "der": "Tengo dominio propio, gobierno mis emociones y autodisciplina.", "cita": "Gálatas 5:23"}
}

if not st.session_state.diagnostico_generado:
    st.title("🌱 Diagnóstico Espiritual: Los 9 Frutos del Espíritu")
    st.markdown("Evalúa el estado actual de tu carácter basándote en **Gálatas 5:22-23**.")
    st.caption("🎨 **Diseño y Creación:** Desarrollado por **Jacob Zumaya Prianti**.")
    nombre_usuario = st.text_input("✍️ Escribe tu nombre para personalizar tu reporte:", value="")
    st.markdown("---")

    # CONTROL DEL QR INTELIGENTE
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
            except Exception: pass
        with col_txt:
            st.markdown("*¡Al escanearlo, este recuadro desaparecerá de tu pantalla móvil para darte máxima comodidad!*")
        st.markdown("---")

    # Invitación explícita a no temerle al 1 ni al 10
    st.warning("""
    ### 🧠 Invitación a la Honestidad Profunda y Transparente
    Antes de iniciar, tómate un momento de silencio y reverencia. Este ejercicio no tiene el propósito de condenarte ni de calificarte bajo estándares humanos, sino de servir como un espejo espiritual fidedigno. 
    
    **No tengas miedo ni vergüenza de marcar un 1 o un 10.** Si hay un área donde la carne te domina por completo, marcar un **1** es el primer paso de humildad hacia la restauración. De igual manera, si el Espíritu Santo te ha dado la victoria absoluta y constante en un fruto, pon un **10** reconociendo Su poder en ti con gratitud. Responde con absoluta sinceridad delante de Dios.
    """)
   
    
    st.header("📋 Autoevaluación")
    st.subheader("Abre cada fruto y selecciona el nivel exacto que defina tu realidad hoy:")

    with st.form("diagnostico_form"):
        puntajes_temporales = {}
        # Lista de opciones con esferas semaforizadas
        esferas = ["1 🔴", "2 🔴", "3 🔴", "4 🔴", "5 🟡", "6 🟡", "7 🟡", "8 🟢", "9 🟢", "10 🟢"]
        
        for i, (fruto, info) in enumerate(frutos_info.items(), 1):
            with st.expander(f"✨ {i}. {fruto} ({info['cita']})"):
                st.markdown(f"**De:** *{info['izq']}* \n\n **Hacia:** *{info['der']}*")
                
                sel = st.select_slider(
                    f"Selecciona tu nivel para {fruto}:", 
                    options=esferas, 
                    value="5 🟡", 
                    key=f"esfera_{fruto}",
                    label_visibility="collapsed"
                )
                
                # CORRECCIÓN DEFINITIVA: Extrae de forma segura solo el carácter numérico antes del emoji
                puntajes_temporales[fruto] = int(sel.split()[0])
                
                # Escala numérica explícita y visible debajo de la barra
                st.markdown("""
                <div class="escala-numerica-fija">
                    <span>1</span><span>2</span><span>3</span><span>4</span><span>5</span>
                    <span>6</span><span>7</span><span>8</span><span>9</span><span>10</span>
                </div>
                """, unsafe_allow_html=True)
                
        st.markdown("---")
        if st.form_submit_button("Generar Diagnóstico"):
            st.session_state.update({
                "respuestas_usuario": puntajes_temporales,
                "nombre_final": nombre_usuario.strip() or "Invitado",
                "diagnostico_generado": True
            })
            st.rerun()

else:
    nombre_final = st.session_state.nombre_final
    puntajes = st.session_state.respuestas_usuario

    st.title("📊 Tu Diagnóstico Espiritual")
    st.header(f"Resultados preparados para: {nombre_final}")
    
    # --- CONSTRUCCIÓN DE LA GRÁFICA DE BARRAS VERTICALES ANCHAS ---
    st.subheader("📈 Gráfica de Crecimiento Espiritual")
    frutos_labels = list(puntajes.keys())
    valores_barras = list(puntajes.values())
    
    colores_barras = []
    for v in valores_barras:
        if v >= 8: colores_barras.append('#2E7D32')     # Verde
        elif v >= 5: colores_barras.append('#FBC02D')   # Amarillo
        else: colores_barras.append('#D32F2F')         # Rojo
        
    fig, ax = plt.subplots(figsize=(10, 4.5))
    barras = ax.bar(frutos_labels, valores_barras, color=colores_barras, edgecolor='none', width=0.7)
    ax.set_ylim(0, 11)
    ax.set_yticks(range(1, 11))
    ax.set_ylabel("Nivel de Intensidad", fontsize=10, weight='bold', color='#222222')
    ax.grid(axis='y', linestyle='--', alpha=0.6, color='#e0e0e0')
    ax.set_xmargin(0.02)
    
    for barra in barras:
        alto = barra.get_height()
        ax.annotate(f'{alto}', xy=(barra.get_x() + barra.get_width() / 2, alto),
                    xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontsize=10, weight='bold')
                    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cccccc')
    ax.spines['bottom'].set_color('#cccccc')
    plt.xticks(rotation=0, ha='center', fontsize=9, weight='bold', color='#333333')
    plt.tight_layout()
    st.pyplot(fig)
    
    buf_img = io.BytesIO()
    plt.savefig(buf_img, format='png', dpi=200, bbox_inches='tight')
    buf_img.seek(0)
    img_base64 = base64.b64encode(buf_img.read()).decode('utf-8')
    plt.close(fig)
    
    st.markdown("---")
    st.subheader("🔍 Análisis Detallado de Madurez")
    
    filas_rubrica_pdf = ""
    lista_consecuencias_pdf = ""
    
    for fruto, score in puntajes.items():
        if score == 10: rango, k = "10", "fortaleza"
        elif score >= 8: rango, k = "8-9", "fortaleza"
        elif score >= 6: rango, k = "6-7", "atencion"
        elif score >= 4: rango, k = "4-5", "atencion"
        else: rango, k = "1-3", "critico"
            
        rub = rubrica_teologica[rango]
        cons = consecuencias_texto[rango]
        
        if k == "fortaleza": st.success(f"🟢 **{fruto}:** {score}/10 — {rub['estado']}.\n\n*Criterio:* {rub['criterio']}")
        elif k == "atencion": st.warning(f"⚠️ **{fruto}:** {score}/10 — {rub['estado']}.\n\n*Criterio:* {rub['criterio']}")
        else: st.error(f"🔴 **{fruto}:** {score}/10 — {rub['estado']}.\n\n*Criterio:* {rub['criterio']}")
            
        filas_rubrica_pdf += f"""
        <tr>
            <td style='font-weight:bold; color:#2E7D32; font-size:22px; padding:12px;'>{fruto}</td>
            <td style='text-align:center; font-weight:bold; font-size:22px; background-color:#f4fbf7; padding:12px;'>{score}/10</td>
            <td style='font-size:20px; padding:12px; font-weight:bold;'>{rub['estado']}</td>
            <td style='font-size:18px; padding:12px; text-align:justify;'>{rub['criterio']}</td>
        </tr>
        """
        lista_consecuencias_pdf += f"<li><b>{fruto} ({score}/10):</b> {cons}</li>"

    st.header("💡 Recomendaciones Generales para el Crecimiento")
    st.markdown("1. **Oración de Rendición:** Lleva tus áreas más bajas a tu altar personal de oración diaria.\n2. **Pasos Prácticos de Fe:** Selecciona una sola área crítica esta semana.\n3. **Caminar en Comunidad:** Busca círculos de edificación dentro de la iglesia.")

    # --- MAQUETACIÓN EXCLUSIVA DEL REPORTE PDF CON FUENTES AL DOBLE ---
    html_reporte = f"""
    <html>
    <head>
        <meta charset='utf-8'>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 30px; color: #333; line-height: 1.5; }}
            .header {{ text-align: center; border-bottom: 4px solid #2e7d32; padding-bottom: 15px; }}
            .header h1 {{ color: #2e7d32; margin: 0; font-size: 44px; }}
            .header p {{ font-size: 24px; margin: 5px 0 0 0; color: #666; }}
            .user-info {{ text-align: right; font-style: italic; margin-top: 15px; color: #555; font-size: 22px; }}
            .grafica-box {{ text-align: center; margin: 30px 0; width: 100%; }}
            .grafica-box img {{ width: 50%; max-width: 50%; height: auto; margin: 0 auto; display: block; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 25px; table-layout: fixed; }}
            th, td {{ border: 2px solid #cccccc; padding: 14px; vertical-align: top; word-wrap: break-word; }}
            th {{ background-color: #f4fbf7; color: #2e7d32; font-size: 22px; font-weight: bold; }}
            .seccion-titulo {{ color: #2e7d32; font-size: 30px; font-weight: bold; margin-top: 45px; border-bottom: 3px solid #2e7d32; padding-bottom: 6px; }}
            .lista-estilo {{ font-size: 20px; line-height: 1.6; margin-top: 15px; padding-left: 20px; }}
            .lista-estilo li {{ margin-bottom: 14px; text-align: justify; }}
            .pastoral-box {{ background-color: #e8f5e9; padding: 25px; margin-top: 40px; border-left: 8px solid #2e7d32; border-radius: 6px; }}
            .pastoral-box h3 {{ margin-top: 0; color: #2e7d32; font-size: 26px; }}
            .pastoral-box p {{ font-size: 20px; margin: 0; line-height: 1.6; }}
            .footer-creditos {{ text-align: center; margin-top: 60px; font-size: 16px; color: #777777; border-top: 2px solid #eeeeee; padding-top: 15px; font-style: italic; }}
        </style>
    </head>
    <body>
        <div class='header'>
            <h1>🌱 Reporte de Diagnóstico Espiritual</h1>
            <p>Rúbrica Basada en la Biblia y el Espíritu de Profecía</p>
        </div>
        <div class='user-info'>Diagnóstico preparado especialmente para: <strong>{nombre_final}</strong></div>
        <div class='grafica-box'><img src='data:image/png;base64,{img_base64}'/></div>
        <div class='seccion-titulo'>🔍 1. Rúbrica de Diagnóstico del Carácter</div>
        <table>
            <thead><tr><th style='width:20%;'>Fruto</th><th style='width:12%;'>Puntaje</th><th style='width:28%;'>Clasificación Teórica</th><th style='width:40%;'>Criterio de Evaluación Real (Biblia / EGW)</th></tr></thead>
            <tbody>{filas_rubrica_pdf}</tbody>
        </table>
        <div class='seccion-titulo'>⚠️ 2. Posibles Consecuencias en la Vida y el Testimonio</div>
        <ul class='lista-estilo'>{lista_consecuencias_pdf}</ul>
        <div class='seccion-titulo'>💡 3. Recomendaciones Teocéntricas para la Restauración</div>
        <ol class='lista-estilo'>
            <li><strong>Oración de Rendición de Altar:</strong> Lleva tus áreas identificadas de forma postrada ante Dios diariamente para la crucifixión absoluta del 'Yo'.</li>
            <li><strong>Estudio Intencional del Testimonio:</strong> Dedica quince minutos diarios a escudriñar la vida de Cristo en lecturas devocionales del Espíritu de Profecía (*El Deseado de Todas las Gentes*).</li>
            <li><strong>Pasos Prácticos de Vigilancia Colectiva:</strong> Reacciona con la virtud opuesta ante la provocación inmediata sometiendo la carne.</li>
        </ol>
        <div class='pastoral-box'>
            <h3>🤝 Cuidado Pastoral y Rendición de Cuentas Confiable</h3>
            <p>Estimado(a) **{nombre_final}**, te animamos con amor cristiano a **presentar y compartir esta rúbrica diagnóstica en una sesión privada con tu pastor o con un anciano de confianza** de tu iglesia local para recibir cobertura intercesora y herramientas de discipulado idóneas para afirmar tus pasos hacia la estatura de la plenitud de Cristo.</p>
        </div>
        <div class='footer-creditos'>Este diagnóstico espiritual fue creado y desarrollado por Jacob Zumaya Prianti. © 2026 Todos los derechos reservados.</div>
    </body>
    </html>
    """

    st.markdown("### 📥 Descarga tu Reporte Oficial")
    st.download_button("Descargar Reporte Completo (PDF / HTML)", data=html_reporte, file_name=f"diagnostico_v_{nombre_final.lower()}.html", mime="text/html")
    st.markdown("---")
    st.caption("🎨 **Diseño y Creación:** Diagnóstico Espiritual desarrollado por **Jacob Zumaya Prianti**.")
    st.markdown("---")
    if st.button("✅ Ya descargué mi reporte, avanzar al siguiente paso"):
        st.session_state.mostrar_felicitacion = True
        st.rerun()
