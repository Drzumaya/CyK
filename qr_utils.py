import streamlit as st
import qrcode
from io import BytesIO

def mostrar_modulo_qr(url_app):
    """Genera y muestra visualmente el código QR en la interfaz."""
    with st.expander("📱 Escanea el Código QR para contestar desde tu móvil", expanded=True):
        col1, col2 = st.columns([1, 1.5])
        with col1:
            qr = qrcode.QRCode(version=1, box_size=10, border=2)
            qr.add_data(url_app)
            qr.make(fit=True)
            img_qr = qr.make_image(fill_color="#e65100", back_color="white")
            
            buf = BytesIO()
            img_qr.save(buf, format="PNG")
            st.image(buf.getvalue(), caption="Escanea con tu cámara", use_container_width=True)
        with col2:
            st.write("### ¡Lleva la encuesta en tu bolsillo!")
            st.write("Si estás visualizando esta presentación desde el proyector:")
            st.write("1. Abre la cámara nativa de tu smartphone.")
            st.write("2. Enfoca el código QR de la izquierda.")
            st.write("3. Completa tu diagnóstico y guarda tus resultados al instante.")
