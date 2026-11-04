import streamlit as st
import pandas as pd
import segno
import io
import base64

# --- CONFIGURACIÓN E INICIALIZACIÓN ---
st.set_page_config(page_title="Diagnóstico: Los 9 Frutos del Espíritu", page_icon="🌱", layout="centered")

for var, val in [("mostrar_felicitacion", False), ("finalizado", False), ("diagnostico_generado", False), ("respuestas_usuario", {})]:
    if var not in st.session_state:
        st.session_state[var] = val

# --- PANTALLAS DE CIERRE Y FELICITACIÓN ---
if st.session_state.finalizado:
    st.success("👋 ¡Gracias por tu participación!")
    st.markdown("### El diagnóstico ha concluido de forma exitosa\nTu sesión se ha cerrado de manera segura. Guárdalo y contacta a tu pastor o anciano de confianza.")
    st.stop()

if st.session_state.mostrar_felicitacion:
    st.balloons()
    st.success("🎉 ¡Muchas felicidades por completar este paso fundamental!")
    st.markdown("### 🚀 Tu camino de transformación empieza hoy\n1. **Acción:** Elige el fruto menor y actúa en 48 horas.\n2. **Consejo Pastoral:** Acércate a tu líder o pastor para revisar el reporte.")
    if st.button("🏁 Terminar Diagnóstico"):
        st.session_state.update({"finalizado": True, "mostrar_felicitacion": False})
        st.rerun()
    st.stop()
# --- DICCIONARIOS DE DATOS ---
consecuencias_texto = {
    "critico": {"estado": "Crítico / Alerta🔴", "corto": "Afectación inmediata en relaciones e impulsividad.", "mediano": "Desgaste físico y mental por estrés.", "largo": "Aislamiento emocional y desconexión."},
    "atencion": {"estado": "En Desarrollo / Atención🟡", "corto": "Inconsistencia emocional ante presión.", "mediano": "Altibajos y cansancio por falta de hábitos.", "largo": "Riesgo de estancamiento espiritual."},
    "fortaleza": {"estado": "Fortaleza Espiritual🟢", "corto": "Respuestas asertivas y paz interior.", "mediano": "Relaciones saludables y resiliencia.", "largo": "Legado de madurez y guía para otros."}
}

frutos_info = {
    "Amor": {"izq": "Guardo rencor o indiferencia.", "der": "Amo sin condiciones.", "cita": "Gálatas 5:22"},
    "Gozo": {"izq": "Me gana la queja o tristeza.", "der": "Alegría profunda ante crisis.", "cita": "Gálatas 5:22"},
    "Paz": {"izq": "Vivo con ansiedad o conflictos.", "der": "Tranquilidad y reconciliación.", "cita": "Gálatas 5:22"},
    "Paciencia": {"izq": "Me desespero con facilidad.", "der": "Sé esperar con calma.", "cita": "Gálatas 5:22"},
    "Benignidad": {"izq": "Hablo de forma dura o cortante.", "der": "Trato con dulzura y empatía.", "cita": "Gálatas 5:22"},
    "Bondad": {"izq": "Pienso solo en mi beneficio.", "der": "Hago el bien de forma generosa.", "cita": "Gálatas 5:22"},
    "Fe": {"izq": "Dudo con frecuencia.", "der": "Soy fiel y confiable.", "cita": "Gálatas 5:22"},
    "Mansedumbre": {"izq": "Me defiendo con soberbia.", "der": "Reacciono con humildad.", "cita": "Gálatas 5:23"},
    "Templanza": {"izq": "Cedo fácil a impulsos.", "der": "Tengo dominio propio.", "cita": "Gálatas 5:23"}
}

if not st.session_state.diagnostico_generado:
    st.title("🌱 Diagnóstico Espiritual: Los 9 Frutos del Espíritu")
    st.markdown("Evalúa tu carácter basándote en **Gálatas 5:22-23**.")
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
            st.markdown("*¡Al escanearlo, este recuadro desaparecerá de tu móvil!*")
        st.markdown("---")

    st.warning("### 🧠 Invitación a la Honestidad Profunda\nTómate un momento de silencio. Responde con total honestidad reconociendo victorias y debilidades.")
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
            st.success(f"🟢 **{fruto}:** {score}/10 - Fortaleza Espiritual.")
        elif score >= 5:
            cons = consecuencias_texto["atencion"]
            st.warning(f"🟡 **{fruto}:** {score}/10 - En desarrollo / Atención.")
        else:
            cons = consecuencias_texto["critico"]
            st.error(f"🔴 **{fruto}:** {score}/10 - Área crítica.")
        tabla_html += f"<tr><td><b>{fruto}</b></td><td>{score}/10</td><td><b>{cons['estado']}</b></td><td>{cons['corto']}</td><td>{cons['mediano']}</td><td>{cons['largo']}</td></tr>"

    st.header("💡 Recomendaciones Generales")
    st.markdown("1. **Oración Enfocada:** Pide dirección por tus puntajes bajos.\n2. **Acción Intencional:** Practica una virtud esta semana.\n3. **Acompañamiento:** Comparte este mapa con tu pastor.")
    st.info(f"🤝 **¿Deseas profundizar, {nombre_final}?** Acércate con tu pastor o un anciano de confianza.")

    html_reporte = f"""<html><head><meta charset='utf-8'><style>body{{font-family:Arial,sans-serif;padding:20px;}}table{{width:100%;border-collapse:collapse;font-size:11px;}}th,td{{border:1px solid #ddd;padding:8px;}}th{{background-color:#f4fbf7;color:#2e7d32;}}</style></head>
    <body><h2 style='text-align:center;'>🌱 Reporte de Diagnóstico Espiritual</h2><div style='text-align:right;'>Preparado para: <b>{nombre_final}</b></div>
    <div style='text-align:center;margin:20px 0;'><img src='data:image/png;base64,{img_base64}' width='320'/></div>
    <table><thead><tr><th>Fruto</th><th>Puntaje</th><th>Estado</th><th>Corto Plazo</th><th>Mediano Plazo</th><th>Largo Plazo</th></tr></thead><tbody>{tabla_html}</tbody></table>
    <div style='background-color:#e8f5e9;padding:15px;margin-top:20px;'><b>🤝 Acompañamiento:</b> Comparte este reporte con tu pastor o líder.</div></body></html>"""

    st.markdown("### 📥 Descarga tu Reporte Oficial")
    st.download_button("Descargar Reporte Completo (PDF / HTML)", data=html_reporte, file_name=f"diagnostico_{nombre_final.lower()}.html", mime="text/html")
    st.markdown("---")
    if st.button("✅ Ya descargué mi reporte, avanzar al siguiente paso"):
        st.session_state.mostrar_felicitacion = True
        st.rerun()
