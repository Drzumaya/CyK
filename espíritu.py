import streamlit as st
import pandas as pd
import segno  # Generador nativo de códigos QR
import io
import base64  # Para incrustar los gráficos en el PDF
import matplotlib.pyplot as plt
import numpy as np # Para los cálculos trigonométricos de la V

# 1. Configuración de la página
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

# LÓGICA DE DESPEDIDA DEFINITIVA
if st.session_state.finalizado:
    st.success("👋 ¡Gracias por tu participación!")
    st.markdown("""
    ### El diagnóstico ha concluido de forma exitosa
    Tu sesión se ha cerrado de manera segura. Si descargaste tu reporte, te animamos a ponerte en contacto con tu pastor o un anciano de confianza.
    """)
    st.stop()

# LÓGICA DE FELICITACIÓN: Se activa al terminar el flujo
if st.session_state.mostrar_felicitacion:
    st.balloons()
    st.success("🎉 ¡Muchas felicidades por completar este paso fundamental!")
    st.markdown("""
    ### 🚀 Tu camino de transformación empieza hoy
    Has descargado con éxito tu diagnóstico espiritual en V.
    
    1. **Toma acciones para el cambio:** Observa en tu gráfica qué frutos se encuentran inclinados hacia el brazo izquierdo de debilidad y trabaja intencionalmente en ellos.
    2. **Busca Consejo Pastoral:** Te animamos a acercarte directamente con tu **pastor o con un anciano de confianza** de tu iglesia para revisar juntos este mapa geométrico de tu carácter.
    """)
    if st.button("🏁 Terminar Diagnóstico"):
        st.session_state.finalizado = True
        st.session_state.mostrar_felicitacion = False
        st.rerun()
    st.stop()
# BASE DE DATOS LOCAL: Consecuencias según rango
consecuencias_texto = {
    "critico": {"estado": "Tendencia al Antónimo", "corto": "Afectación inmediata en tus relaciones por reacciones carnales.", "mediano": "Desgaste de tu paz por vivir bajo el dominio de impulsos negativos.", "largo": "Aislamiento emocional y estancamiento crónico en tu madurez de fe."},
    "atencion": {"estado": "Estado de Transición", "corto": "Inconsistencia. Te debates constantemente entre la carne y el espíritu.", "mediano": "Relaciones con altibajos. Sensación de estancamiento en el punto de inicio.", "largo": "Riesgo de quedarte en la mediocridad sin experimentar el poder del Fruto."},
    "fortaleza": {"estado": "Tendencia al Fruto", "corto": "Respuestas sabias ante problemas, paz interior e impacto positivo diario.", "mediano": "Relaciones saludables y duraderas respaldadas por el Espíritu.", "largo": "Estabilidad espiritual duradera y capacidad de guiar a otros con tu ejemplo."}
}

frutos_info = {
    "Amor": {"izq": "Odio / Indiferencia", "der": "Amor Incondicional", "cita": "Gálatas 5:22"},
    "Gozo": {"izq": "Tristeza / Amargura", "der": "Gozo Profundo", "cita": "Gálatas 5:22"},
    "Paz": {"izq": "Discordia / Conflicto", "der": "Paz Interior", "cita": "Gálatas 5:22"},
    "Paciencia": {"izq": "Impaciencia / Intolerancia", "der": "Paciencia Calma", "cita": "Gálatas 5:22"},
    "Benignidad": {"izq": "Crueldad / Aspereza", "der": "Benignidad / Amabilidad", "cita": "Gálatas 5:22"},
    "Bondad": {"izq": "Malicia / Maldad", "der": "Bondad Generosa", "cita": "Gálatas 5:22"},
    "Fe": {"izq": "Infidelidad / Deslealtad", "der": "Fe / Fidelidad Firmes", "cita": "Gálatas 5:22"},
    "Mansedumbre": {"izq": "Arrogancia / Ira", "der": "Mansedumbre Humilde", "cita": "Gálatas 5:23"},
    "Templanza": {"izq": "Descontrol / Desenfreno", "der": "Templanza / Dominio Propio", "cita": "Gálatas 5:23"}
}

# FLUJO CONDICIONAL: EVALUACIÓN EN V
if not st.session_state.diagnostico_generated:
    st.title("🌱 Diagnóstico Espiritual en V: Los 9 Frutos")
    nombre_usuario = st.text_input("✍️ Escribe tu nombre para personalizar tu reporte:", value="")
    st.markdown("---")

    url_base_app = "https://diagnosticofrutosdelespiritu.streamlit.app"
    if "view" not in st.query_params:
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
            st.markdown("*¡Al escanearlo, el QR desaparecerá de tu móvil para tu comodidad!*")
        st.markdown("---")

    st.warning("""
    ### 🧠 Invitación a la Honestidad Profunda
    El punto **1** se encuentra en el centro de la **V**. El brazo **izquierdo** mide tu tendencia hacia el defecto, y el brazo **derecho** hacia la virtud bíblica. Responde con total transparencia.
    """)

    st.header("📋 Evaluación de Carácter")
    with st.form("diagnostico_form"):
        puntajes_temporales = {}
        
        for i, (fruto, info) in enumerate(frutos_info.items(), 1):
            st.markdown(f"#### **{i}. {fruto}** <small>({info['cita']})</small>", unsafe_allow_html=True)
            
            # Selector de orientación en la V
            lado = st.radio(
                f"¿Hacia qué lado de la V te inclinas más en tu día a día para el/la {fruto}?",
                options=["Brazo Izquierdo (Tendencia Negativa)", "Brazo Derecho (Tendencia al Fruto)"],
                key=f"lado_{fruto}"
            )
            
            # Selector de intensidad (1 al 10 iniciando en el centro)
            nivel = st.select_slider(
                "Nivel de intensidad en la escala (El 1 es el centro de la V, el 10 es el extremo):",
                options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                value=1,
                key=f"nivel_{fruto}"
            )
            
            # Guardar el valor: negativo si va a la izquierda, positivo a la derecha
            val_final = -nivel if "Izquierdo" in lado else nivel
            # Si el nivel es 1, se queda neutro en el centro (1)
            if nivel == 1: val_final = 1
                
            puntajes_temporales[fruto] = val_final
            st.markdown(f"<small>⬅️ Extremo Izquierdo: **{info['izq']}** | Extremo Derecho: **{info['der']}** ➡️</small>", unsafe_allow_html=True)
            st.markdown("---")
            
        enviar = st.form_submit_button("Generar Diagnóstico en V")
        
        if enviar:
            st.session_state.respuestas_usuario = puntajes_temporales
            st.session_state.nombre_final = nombre_usuario if nombre_usuario.strip() != "" else "Invitado"
            st.session_state.diagnostico_generado = True
            st.rerun()
else:
    nombre_final = st.session_state.nombre_final
    puntajes = st.session_state.respuestas_usuario

    st.title("📊 Tu Diagnóstico Espiritual")
    st.header(f"Resultados de la Escala en V para: {nombre_final}")
    
    # --- CONSTRUCCIÓN GEOMÉTRICA DE LA GRÁFICA EN V (60 GRADOS) ---
    fig, ax = plt.subplots(figsize=(7, 6))
    
    # Dibujar líneas guía de la V a 60° (Ángulos de 60 y 120 grados con respecto a la horizontal)
    angulo_der = np.radians(60)
    angulo_izq = np.radians(120)
    
    # Trazar ejes de la V (Del nivel 1 al 10)
    ax.plot([0, 10 * np.cos(angulo_der)], [0, 10 * np.sin(angulo_der)], color='#2e7d32', linewidth=3, label="Brazo del Fruto (Virtud)")
    ax.plot([0, 10 * np.cos(angulo_izq)], [0, 10 * np.sin(angulo_izq)], color='#d32f2f', linewidth=3, label="Brazo del Antónimo (Debilidad)")
    
    # Dibujar las marcas de graduación del 1 al 10 en la V
    for n in range(1, 11):
        ax.plot(n * np.cos(angulo_der), n * np.sin(angulo_der), 'go', mfc='white', ms=4)
        ax.plot(n * np.cos(angulo_izq), n * np.sin(angulo_izq), 'ro', mfc='white', ms=4)
        
        # SOLUCIÓN: Eliminamos la condición conflictiva y rotulamos los números de forma directa
        ax.text(n * np.cos(angulo_der) + 0.2, n * np.sin(angulo_der), str(n), color='#2e7d32', fontsize=8)
        ax.text(n * np.cos(angulo_izq) - 0.5, n * np.sin(angulo_izq), str(n), color='#d32f2f', fontsize=8)

    # Graficar las respuestas del usuario sobre la V
    colores_nodos = ['#FF6B35', '#FF9F1C', '#F15BB5', '#E63946', '#FFD166', '#06D6A0', '#118AB2', '#073B4C', '#8338EC']
    
    for idx, (fruto, valor) in enumerate(puntajes.items()):
        # Determinar en qué brazo cae según el signo guardado
        ang = angulo_izq if valor < 0 else angulo_der
        mag = abs(valor)
        
        # Calcular posición en el plano cartesiano
        x_pos = mag * np.cos(ang)
        y_pos = mag * np.sin(ang)
        
        # Dibujar punto del fruto en la V
        ax.plot(x_pos, y_pos, 'o', color=colores_nodos[idx], markersize=10, label=f"{fruto} ({mag})")
        ax.text(x_pos + 0.1, y_pos + 0.2, fruto, fontsize=8, weight='bold')

    # Estilización del plano geométrico
    ax.set_title("Mapa de Posicionamiento en V (60°)", fontsize=12, weight='bold', color='#1b5e20')
    ax.axis('off') # Quitar la cuadrícula cartesiana de fondo
    ax.set_xlim(-7, 7)
    ax.set_ylim(-1, 10)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.15), ncol=3, fontsize=7)
    
    st.pyplot(fig)
    
    # Guardar gráfico en base64 para insertarlo en el PDF
    buffer_img = io.BytesIO()
    plt.savefig(buffer_img, format='png', dpi=150, bbox_inches='tight')
    buffer_img.seek(0)
    img_base64 = base64.b64encode(buffer_img.read()).decode('utf-8')
    plt.close(fig)

    # Procesar tabla de diagnósticos cualitativos para la pantalla y el reporte
    st.subheader("🔍 Análisis de Alineación")
    tabla_html = ""
    
    for fruto, valor in puntajes.items():
        mag = abs(valor)
        if valor < 0:
            cons = consecuencias_texto["critico"]
            st.error(f"🚨 **{fruto}:** Inclinado hacia el Antónimo con intensidad {mag}/10.")
        elif valor == 1:
            cons = consecuencias_texto["atencion"]
            st.warning(f"⚠️ **{fruto}:** Te encuentras en el punto de inicio neutro (Puntaje 1/10).")
        else:
            cons = consecuencias_texto["fortaleza"]
            st.success(f"🌟 **{fruto}:** Reflejas alineación con el Fruto con intensidad {mag}/10.")
            
        tabla_html += f"<tr><td style='font-weight:bold;'>{fruto}</td><td style='text-align:center;'>{mag}/10</td><td>{cons['estado']}</td><td>{cons['corto']}</td><td>{cons['mediano']}</td><td>{cons['largo']}</td></tr>"

    # Maquetación del PDF
    html_reporte = f"""
    <html>
    <head><meta charset='utf-8'><style>body{{font-family:Arial;color:#333;}}table{{width:100%;border-collapse:collapse;font-size:11px;}}th,td{{border:1px solid #ddd;padding:6px;}}th{{background-color:#f4fbf7;color:#2e7d32;}}</style></head>
    <body>
        <h2>🌱 Reporte de Diagnóstico en V: {nombre_final}</h2>
        <div style='text-align:center; margin:20px 0;'>
            <img src='data:image/png;base64,{img_base64}' width='380'/>
        </div>
        <table>
            <thead><tr><th>Fruto</th><th>Intensidad</th><th>Alineación</th><th>Corto Plazo</th><th>Mediano Plazo</th><th>Largo Plazo</th></tr></thead>
            <tbody>{tabla_html}</tbody>
        </table>
        <div style='background-color:#e8f5e9; padding:12px; margin-top:15px; border-left:4px solid #2e7d32;'>
            <strong>🤝 Cuidado Espiritual:</strong> Te invitamos a compartir este mapa en V con tu 
            <strong>pastor o con un anciano de confianza</strong> para recibir consejería basada en tu perfil.
        </div>
    </body>
    </html>
    """

    st.markdown("### 📥 Descarga tu Reporte Oficial")
    st.download_button(label="Descargar Reporte Completo (PDF / HTML)", data=html_reporte, file_name=f"diagnostico_v_{nombre_final.lower()}.html", mime="text/html")
    
    st.markdown("---")
    if st.button("✅ Ya descargué mi reporte, avanzar al siguiente paso"):
        st.session_state.mostrar_felicitacion = True
        st.rerun()
