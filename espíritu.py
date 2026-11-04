import streamlit as st
import pandas as pd
import segno
import io
import base64

# --- CONFIGURACIÓN E INICIALIZACIÓN ---
st.set_page_config(page_title="Diagnóstico: Los 9 Frutos del Espíritu", page_icon="🌱", layout="centered")

# Declaración segura de variables de sesión
for var, val in [("mostrar_felicitacion", False), ("diagnostico_generado", False), ("respuestas_usuario", {})]:
    if var not in st.session_state:
        st.session_state[var] = val

# --- PANTALLA DE FELICITACIÓN Y REINICIO ---
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
    # REQUERIMIENTO: Botón modificado para reiniciar el test al instante y volver al inicio
    if st.button("🔄 Nuevo diagnóstico"):
        # Limpieza completa de variables para regresar a la pantalla principal limpia
        st.session_state.diagnostico_generado = False
        st.session_state.mostrar_felicitacion = False
        st.session_state.respuestas_usuario = {}
        st.rerun()
        
    st.stop() # Detiene la ejecución para mantener oculta la batería de abajo

# --- DICCIONARIOS DE DATOS AMPLIADOS Y PRECISOS ---
consecuencias_texto = {
    "critico": {
        "estado": "Área de Alerta Crítica 🔴",
        "corto": "Afectación inmediata en tu entorno familiar y ministerial. Brotes recurrentes de impulsividad, respuestas ásperas, inestabilidad emocional y pérdida del autocontrol ante situaciones cotidianas de presión.",
        "mediano": "Desgaste profundo de tu paz mental y fatiga espiritual crónica. Distanciamiento de las personas que amas debido a fricciones no resueltas, debilitamiento de tu testimonio cristiano y un estancamiento evidente en tu vida de oración.",
        "largo": "Riesgo latente de aislamiento emocional, endurecimiento del corazón y decisiones destructivas arraigadas. Pérdida de comunión íntima con el Señor y una desconexión preocupante de los propósitos eternos diseñados para tu vida."
    },
    "atencion": {
        "estado": "En Crecimiento / Estado de Atención 🟡",
        "corto": "Inconsistencia en el carácter. Reflejas la virtud en momentos de tranquilidad, pero experimentas una alta vulnerabilidad y tiendes a reaccionar en la carne cuando surgen crisis o provocaciones inesperadas.",
        "mediano": "Relaciones interpersonales que experimentan altibajos constantes. Sensación de estancamiento o de 'tibieza' debido a la falta de hábitos espirituales firmes, disciplina personal y entrega diaria al Espíritu Santo.",
        "largo": "Riesgo de conformarse con la mediocridad espiritual, viviendo muy por debajo de la plenitud, la paz y la madurez transformadora que Dios ha diseñado para aquellos que caminan fielmente en Su gracia."
    },
    "fortaleza": {
        "estado": "Evidencia de Madurez Espiritual 🟢",
        "corto": "Respuestas sabias, asertivas y templadas ante los problemas diarios. Eres un canal manifiesto de paz interior, manifestando gracia, amor y cordura en tu entorno inmediato.",
        "mediano": "Consolidación de lazos familiares y eclesiásticos saludables, estables y duraderos. Desarrollo de una resiliencia espiritual inquebrantable que inspira y fortalece a tu congregación frente a las pruebas comunes.",
        "largo": "Construcción de un legado sólido de madurez espiritual. Estabilidad emocional integral a lo largo de los años y una capacidad madura para pastorear, discipular, aconsejar y guiar efectivamente a las nuevas generaciones."
    }
}

frutos_info = {
    "Amor": {"izq": "Guardo rencor, elijo el egoísmo o la indiferencia.", "der": "Amo, perdono y acepto a los demás sin condiciones.", "cita": "Gálatas 5:22"},
    "Gozo": {"izq": "Me domina la queja constante, la amargura o la tristeza.", "der": "Siento una alegría santa y profunda que no depende de las circunstancias.", "cita": "Gálatas 5:22"},
    "Paz": {"izq": "Vivo atrapado en la ansiedad, la preocupación o los conflictos.", "der": "Sustento una tranquilidad interna y soy un agente de reconciliación.", "cita": "Gálatas 5:22"},
    "Paciencia": {"izq": "Me desespero rápido, me irrito y soy intolerante con los demás.", "der": "Sé esperar los tiempos de Dios con calma y tolero las debilidades ajenas.", "cita": "Gálatas 5:22"},
    "Benignidad": {"izq": "Puedo llegar a ser duro, crítico o muy cortante al hablar.", "der": "Trato a todas las personas con extrema dulzura, empatía y afabilidad.", "cita": "Gálatas 5:22"},
    "Bondad": {"izq": "Busco primero mi propio beneficio o actúo con doblez.", "der": "Hago el bien de forma activa, generosa, íntegra y desinteresada.", "cita": "Gálatas 5:22"},
    "Fe": {"izq": "Dudo constantemente de las promesas de Dios y soy desleal.", "der": "Soy una persona fiel, plenamente confiable y con una fe inquebrantable.", "cita": "Gálatas 5:22"},
    "Mansedumbre": {"izq": "Me defiendo con orgullo, soberbia, prepotencia o enojo.", "der": "Reacciono con humildad, suavidad de espíritu y total sumisión a Dios.", "cita": "Gálatas 5:23"},
    "Templanza": {"izq": "Cedo con facilidad ante los antojos, impulsos o malos hábitos.", "der": "Tengo dominio propio, gobierno mis emociones y autodisciplina.", "cita": "Gálatas 5:23"}
}

if not st.session_state.diagnostico_generado:
    st.title("🌱 Diagnóstico Espiritual: Los 9 Frutos del Espíritu")
    st.markdown("Evalúa el estado actual de tu carácter basándote en la revelación bíblica de **Gálatas 5:22-23**.")
    nombre_usuario = st.text_input("✍️ Escribe tu nombre para personalizar tu reporte:", value="")
    st.markdown("---")

    if "view" not in st.query_params:
        st.markdown("### 📱 Escanea y Responde en tu Móvil")
        col_qr, col_txt = st.columns(2)
        with col_qr:
            try:
                qr = segno.make_qr("https://diagnosticofrutosdelespiritu.streamlit.app")
                buf = io.BytesIO(); qr.save(buf, kind='png', scale=5)
                st.image(buf.getvalue(), use_container_width=True)
            except Exception: pass
        with col_txt:
            st.markdown("*¡Al escanearlo, este recuadro desaparecerá de tu móvil para darte total comodidad!*")
        st.markdown("---")

    st.warning("### 🧠 Invitación a la Honestidad Profunda\nTómate un momento de silencio y oración antes de comenzar. Este ejercicio no tiene el propósito de condenarte ni de calificarte bajo estándares humanos, sino de servir como un espejo espiritual claro y transparente. Responde con absoluta sinceridad delante de Dios, reconociendo tanto los frutos que Él ya ha hecho madurar en ti como aquellas flaquezas que aún requieren ser transformadas por Su gracia.")

    st.header("📋 Autoevaluación")
    st.subheader("Abre cada fruto y selecciona la esfera numérica que defina tu realidad hoy:")

    with st.form("diagnostico_form"):
        puntajes_temporales = {}
        esferas = ["1 🔴", "2 🔴", "3 🔴", "4 🔴", "5 🟡", "6 🟡", "7 🟡", "8 🟢", "9 🟢", "10 🟢"]
        
        for i, (fruto, info) in enumerate(frutos_info.items(), 1):
            with st.expander(f"✨ {i}. {fruto} ({info['cita']})"):
                st.markdown(f"**De:** *{info['izq']}* \n\n **Hacia:** *{info['der']}*")
                sel = st.select_slider(f"Selecciona tu nivel para {fruto}:", options=esferas, value="5 🟡", key=f"esfera_{fruto}")
                puntajes_temporales[fruto] = int(sel.split()[0])
                
        st.markdown("---")
        if st.form_submit_button("Generar Diagnóstico"):
            st.session_state.update({
                "respuestas_usuario": puntajes_temporales,
                "nombre_final": nombre_usuario.strip() or "Invitado",
                "diagnostico_generado": True
            })
            st.rerun()
else:
    import matplotlib.pyplot as plt
    nombre_final = st.session_state.nombre_final
    puntajes = st.session_state.respuestas_usuario

    st.title("📊 Tu Diagnóstico Espiritual")
    st.header(f"Resultados preparados para: {nombre_final}")
    st.subheader("🍊 Distribución Porcentual (Gráfica Mandarina)")
    
    fig, ax = plt.subplots(figsize=(5, 5))
    colores_mandarina = ['#FF6B35', '#FF9F1C', '#F15BB5', '#E63946', '#FFD166', '#06D6A0', '#118AB2', '#073B4C', '#8338EC']
    wedges, texts, autotexts = ax.pie(
        list(puntajes.values()), labels=list(puntajes.keys()), autopct='%1.1f%%', 
        startangle=95, colors=colores_mandarina, textprops=dict(color="black", weight="bold"), pctdistance=0.75
    )
    fig.gca().add_artist(plt.Circle((0,0), 0.55, fc='white'))
    for autotext in autotexts: autotext.set_color('white'); autotext.set_fontsize(9)
    ax.axis('equal'); plt.tight_layout()
    st.pyplot(fig)
    
    buf_img = io.BytesIO(); plt.savefig(buf_img, format='png', dpi=150, bbox_inches='tight'); buf_img.seek(0)
    img_base64 = base64.b64encode(buf_img.read()).decode('utf-8')
    plt.close(fig)
    
    st.markdown("---")
    st.subheader("🔍 Análisis Detallado de Madurez")
    tabla_html = ""
    
    for fruto, score in puntajes.items():
        if score >= 8:
            cons = consecuencias_texto["fortaleza"]
            st.success(f"🟢 **{fruto}:** {score}/10 — {cons['estado']}. Presentas un reflejo sólido de la obra transformadora del Espíritu Santo en esta área.")
        elif score >= 5:
            cons = consecuencias_texto["atencion"]
            st.warning(f"🟡 **{fruto}:** {score}/10 — {cons['estado']}. Hay terreno ganado, pero requieres mayor intencionalidad y entrega para consolidar la constancia.")
        else:
            cons = consecuencias_texto["critico"]
            st.error(f"🔴 **{fruto}:** {score}/10 — {cons['estado']}. Representa un punto de quiebre que demanda atención urgente en oración y sumisión al Señor.")
        tabla_html += f"<tr><td><b>{fruto}</b></td><td>{score}/10</td><td><b>{cons['estado']}</b></td><td>{cons['corto']}</td><td>{cons['mediano']}</td><td>{cons['largo']}</td></tr>"

    st.header("💡 Recomendaciones Generales para el Crecimiento")
    st.markdown("1. **Oración de Rendición:** Lleva tus áreas identificadas con puntajes más bajos a tu altar personal de oración diaria, pidiendo al Espíritu Santo que muera tu carne y florezca Su carácter.\n2. **Pasos Prácticos de Fe:** Selecciona una sola área crítica esta semana y ejecuta de manera intencional tres acciones que reflejen la virtud bíblica opuesta (ej. responder con mansedumbre ante una crítica).\n3. **Caminar en Comunidad:** Busca círculos de edificación dentro de la iglesia donde puedas abrir tu corazón de forma madura y transparente.")
    
    # INVITACIÓN ABUNDANTE, CÁLIDA Y DETALLADA (PASTORAL)
    st.info(f"""
    ### 🤝 Una Invitación Especial a Caminar Juntos
    Querido(a) **{nombre_final}**, recuerda firmemente que el fruto del carácter cristiano no es el resultado del mero esfuerzo humano o del legalismo, sino de permanecer conectados a la Vid verdadera que es Jesucristo. Este diagnóstico es una radiografía del momento presente, pero tu historia está en constante restauración.
    
    No tienes por qué llevar este proceso a solas ni en silencio. **Te extendemos una invitación sincera, afectuosa y completamente confidencial para acercarte de manera prioritaria con tu pastor o con un anciano de confianza de nuestra congregación.** 
    
    Compartir este reporte con un líder maduro abrirá una puerta bendecida de consejería pastoral, donde serás escuchado sin juicio, cubierto en oración específica y equipado con herramientas bíblicas personalizadas para trazar una ruta clara hacia tu madurez integral. **¡El cuerpo de Cristo está aquí para sostener tus manos en este camino!**
    """)

    html_reporte = f"""<html><head><meta charset='utf-8'><style>body{{font-family:Arial,sans-serif;padding:20px;color:#333;line-height:1.4;}}table{{width:100%;border-collapse:collapse;font-size:11px;}}th,td{{border:1px solid #ddd;padding:8px;vertical-align:top;}}th{{background-color:#f4fbf7;color:#2e7d32;}} .pastoral-box{{background-color:#e8f5e9;padding:15px;margin-top:25px;border-left:5px solid #2e7d32;}}</style></head>
    <body><h2 style='text-align:center;color:#2e7d32;'>🌱 Reporte de Diagnóstico Espiritual</h2><div style='text-align:right;'>Preparado para: <b>{nombre_final}</b></div>
    <div style='text-align:center;margin:20px 0;'><img src='data:image/png;base64,{img_base64}' width='320'/></div>
    <table><thead><tr><th>Fruto</th><th>Puntaje</th><th>Estado de Madurez</th><th>Consecuencias Corto Plazo</th><th>Consecuencias Mediano Plazo</th><th>Consecuencias Largo Plazo</th></tr></thead><tbody>{tabla_html}</tbody></table>
    <div class='pastoral-box'><h3>🤝 Un Llamado al Acompañamiento y Cuidado Espiritual</h3><p>Estimado(a) miembro, este reporte representa una guía invaluable para tu crecimiento. Te animamos con amor a **presentar y compartir estos resultados en una cita con tu pastor o un anciano de confianza** de tu iglesia local. Encontrarás un espacio sagrado de consejería, oración intercesora y cobertura pastoral idóneo para afirmar tus pasos hacia la estatura de la plenitud de Cristo.</p></div></body></html>"""

    st.markdown("### 📥 Descarga tu Reporte Oficial")
    st.download_button("Descargar Reporte Completo (PDF / HTML)", data=html_reporte, file_name=f"diagnostico_{nombre_final.lower()}.html", mime="text/html")
    st.markdown("---")
    if st.button("✅ Ya descargué mi reporte, avanzar al siguiente paso"):
        st.session_state.mostrar_felicitacion = True
        st.rerun()
