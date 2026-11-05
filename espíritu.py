import streamlit as st
import pandas as pd
import segno
import io
import base64
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime  # Para registrar la fecha de escaneo del QR

# 1. Configuración de la página institucional y estados de sesión
st.set_page_config(
    page_title="Diagnóstico: Los 9 Frutos del Espíritu",
    page_icon="🌱",
    layout="centered"
)

# Inicialización segura de variables de sesión
for var, val in [("mostrar_felicitacion", False), ("finalizado", False), ("diagnostico_generado", False), ("respuestas_usuario", {})]:
    if var not in st.session_state:
        st.session_state[var] = val

# CAPTURA AUTOMÁTICA DE FECHA: Graba la fecha del día exacto en que se abre el enlace móvil
if "fecha_apertura" not in st.session_state:
    st.session_state.fecha_apertura = datetime.now().strftime("%d/%m/%Y")

# Base de datos global fija de Gálatas 5
frutos_info = {
    "Amor": {"izq": "Guardo rencor, elijo el egoísmo o la indiferencia.", "der": "Amo, perdono y acepto a los demás sin condiciones.", "cita": "Gálatas 5:22"},
    "Gozo": {"izq": "Me domina la queja constante, la amargura o la tristeza.", "der": "Siento una alegría profunda que no depende de las circunstancias.", "cita": "Gálatas 5:22"},
    "Paz": {"izq": "Vivo atrapado en la ansiedad, la preocupación o los conflictos.", "der": "Tengo tranquilidad interna y soy un agente de reconciliación.", "cita": "Gálatas 5:22"},
    "Paciencia": {"izq": "Me desespero rápido, me irrito y soy intolerante.", "der": "Sé esperar los tiempos de Dios con calma y tolero las flaquezas ajenas.", "cita": "Gálatas 5:22"},
    "Benignidad": {"izq": "Puedo llegar a ser duro, crítico o muy cortante al hablar.", "der": "Trato a todos con extrema dulzura, empatía y afabilidad.", "cita": "Gálatas 5:22"},
    "Bondad": {"izq": "Pienso primero en mi beneficio o actúo con doblez.", "der": "Hago el bien de forma activa, generosa, íntegra y desinteresada.", "cita": "Gálatas 5:22"},
    "Fe": {"izq": "Dudo constantemente de las promesas de Dios y soy desleal.", "der": "Soy una persona fiel, plenamente confiable y con fe inquebrantable.", "cita": "Gálatas 5:22"},
    "Mansedumbre": {"izq": "Me defiendo con orgullo, soberbia, prepotencia o enojo.", "der": "Reacciono con humildad, suavidad de espíritu y total sumisión a Dios.", "cita": "Gálatas 5:23"},
    "Templanza": {"izq": "Cedo con facilidad ante los antojos, impulsos o malos hábitos.", "der": "Tengo dominio propio, gobierno mis emociones y autodisciplina.", "cita": "Gálatas 5:23"}
}

# Estilos CSS para la regla numérica visible
st.markdown("""
<style>
    .escala-numerica-fija {
        font-family: 'Courier New', Courier, monospace;
        display: flex;
        justify-content: space-between;
        padding: 0 15px 20px 12px;
        color: #2e7d32;
        font-weight: bold;
        font-size: 14px;
        margin-top: -10px;
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

# LÓGICA DE FELICITACIÓN
if st.session_state.mostrar_felicitacion:
    st.balloons()
    st.success("🎉 ¡Muchas felicidades por completar este paso fundamental!")
    st.markdown("""
    ### 🚀 Tu camino de transformación empieza hoy
    Has descargado con éxito tu diagnóstico espiritual bajo los lineamientos de la norma APA 7.
    
    1. **Toma acciones para el cambio:** Elige el fruto con menor intensidad y genera hábitos guiados de forma proactiva.
    2. **Busca Consejo Pastoral:** Te animamos a acercarte directamente con tu **pastor o con un anciano de confianza** de tu iglesia local para compartir tus resultados y recibir guía espiritual.
    """)
    st.markdown("---")
    if st.button("🔄 Nuevo diagnóstico", key="btn_reinicio_kiosco_global"):
        st.session_state.diagnostico_generado = False
        st.session_state.mostrar_felicitacion = False
        st.session_state.respuestas_usuario = {}
        st.rerun()
    st.caption("🎨 Diagnóstico Espiritual desarrollado por **Jacob Zumaya Prianti**.")
    st.stop()


# --- MATRIZ DOCTRINAL ESPECÍFICA (AMOR, GOZO Y PAZ) ---
rubrica_detallada = {
    "Amor": {
        "1-3": {
            "estado": "Amor Carnal o Indiferencia 🔴",
            "criterio": "Afecto condicional, resentment oculto o apatía hacia las faltas del prójimo (1 Juan 4:20). White (1953) señaló que 'el egoísmo es un cáncer frío que destruye los lazos del alma' (p. 200)."
        },
        "4-5": {
            "estado": "Esfuerzo Humano Inconstante 🟡",
            "criterio": "Amas cuando recibes aprobación, pero te cuesta manifestar gracia ante la ofensa o el desprecio (Mateo 5:46). White (1955) afirma que 'el amor puramente humano se desvanece ante la prueba' (p. 312)."
        },
        "6-7": {
            "estado": "Crecimiento en Transición 🟡",
            "criterio": "Buscas amar intencionalmente y perdonar con prontitud, batallando activamente contra el orgullo herido (1 Corintios 13:4). White (1954) indica que 'el amor cristiano es un principio divino, no una emoción fugaz' (p. 45)."
        },
        "8-9": {
            "estado": "Madurez Consecuente 🟢",
            "criterio": "El sacrificio y la aceptación incondicional del prójimo son rasgos habituales y firmes en tu carácter (Romanos 12:9). White (1944) resalta que 'el amor es la base de la piedad y la semejanza con Dios' (p. 115)."
        },
        "10": {
            "estado": "Plenitud de Permanencia 🟢",
            "criterio": "Reflejas perfectamente el amor agape; estás crucificado al 'Yo' y vives solo para bendecir (Gálatas 2:20). White (2007) define que 'cuando el amor de Cristo inunde el alma, fluirá como un manantial' (p. 68)."
        }
    },
    "Gozo": {
        "1-3": {
            "estado": "Amargura o Queja Constante 🔴",
            "criterio": "Tu estado de ánimo depende enteramente de las circunstancias; caes fácil en la murmuración (Filipenses 2:14). White (1980a) señaló que 'la melancolía y la queja deshonran al Redentor' (p. 240)."
        },
        "4-5": {
            "estado": "Alegría Superficial e Inestable 🟡",
            "criterio": "Sientes gozo en el culto o momentos buenos, pero las dificultades diarias te hunden en el desánimo (Santiago 1:2). White (1951) afirma que 'la fe inmadura busca solo el sol y se acobarda ante la tormenta' (p. 182)."
        },
        "6-7": {
            "estado": "Regocijo en Desarrollo 🟡",
            "criterio": "Decides alabar a Dios en la prueba, logrando estabilizar tus emociones mediante la gratitud activa (Habacuc 3:17-18). White (1947) indica que 'la alabanza expulsa las sombras sembradas por el enemigo' (p. 92)."
        },
        "8-9": {
            "estado": "Gozo Profundo y Firme 🟢",
            "criterio": "Posees una paz gozosa e inalterable basada en las promesas divinas, que inspira a los demás (Salmo 16:11). White (1959) resalta que 'un espíritu alegre es un tónico permanente para el alma y el cuerpo' (p. 55)."
        },
        "10": {
            "estado": "Plenitud de Regocijo Santo 🟢",
            "criterio": "Vives en un estado permanente de alabanza y regocijo celestial, sin importar la prueba física o mental (1 Pedro 1:8). White (1962) define que 'el gozo del Señor en el corazón es una luz incombustible' (p. 104)."
        }
    },
    "Paz": {
        "1-3": {
            "estado": "Ansiedad Crónica o Discordia 🔴",
            "criterio": "Vives esclavo del temor al futuro, el control obsesivo o promueves tensiones en tu entorno (Isaías 57:21). White (1947) señaló que 'la preocupación es ciega e incapaz de vislumbrar el mañana' (p. 210)."
        },
        "4-5": {
            "estado": "Calma Condicionada 🟡",
            "criterio": "Tienes tranquilidad solo cuando no hay imprevistos ni tensiones financieras o familiares en el hogar (Juan 14:27). White (2007) afirma que 'la paz del mundo es un barniz que se agrieta al menor sismo' (p. 74)."
        },
        "6-7": {
            "estado": "Tranquilidad en Transición 🟡",
            "criterio": "Logras calmar tu mente mediante la oración constante, entregando tus cargas al Señor con mayor rapidez (Filipenses 4:6-7). White (1954) indica que 'entregar la voluntad a Dios aquieta las tempestades del alma' (p. 81)."
        },
        "8-9": {
            "estado": "Paz Sobrenatural Estable 🟢",
            "criterio": "Reflejas serenidad en medio de crisis graves, actuando con madurez como un agente pacificador activo (Isaías 26:3). White (1952) resalta que 'la paz de Cristo es un escudo que las saetas del mundo no pueden penetrar' (p. 402)."
        },
        "10": {
            "estado": "Reposo Absoluto en el Señor 🟢",
            "criterio": "Comunión perfecta que produce un sosiego idéntico al de Cristo durmiendo en la barca en medio de la tempestad (Salmo 119:165). White (1953) define que 'estar escondido con Cristo en Dios es el descanso supremo' (p. 314)."
        }
    },
    # --- SEGMENTO 3: MATRIZ DOCTRINAL ESPECÍFICA (PACIENCIA, BENIGNIDAD Y BONDAD) ---
    "Paciencia": {
        "1-3": {
            "estado": "Intolerancia o Irritabilidad Directa 🔴",
            "criterio": "Reaccionas con enojo inmediato ante retrasos, errores de otros o cambios de planes (Proverbios 14:29). White (1944) señaló que 'un espíritu impaciente disipa la fragancia de la piedad' (p. 134)."
        },
        "4-5": {
            "estado": "Resistencia Humana Limitada 🟡",
            "criterio": "Soportas las dificultades por un tiempo, pero terminas explotando si la presión o la espera se alargan (Eclesiastés 7:8). White (2009) afirma que 'la paciencia no es solo silencio externo, sino quietud en el corazón' (p. 88)."
        },
        "6-7": {
            "estado": "Soportar Intencional 🟡",
            "criterio": "Controlas tus reacciones ásperas pidiendo paciencia en silencio, tolerando las debilidades del prójimo (Colosenses 3:13). White (1930) indica que 'dominar la lengua en el momento del desespero es una victoria santa' (p. 210)."
        },
        "8-9": {
            "estado": "Longanimidad Madura 🟢",
            "criterio": "Soportas con mansedumbre las pruebas prolongadas y tratas con profunda calma a las personas difíciles (Santiago 5:7-8). White (1953) resalta que 'la paciencia madura es el oro purificado en el fuego de la prueba' (p. 94)."
        },
        "10": {
            "estado": "Paciencia Perfecta de Cristo 🟢",
            "criterio": "Vives la constancia perfecta; ninguna provocación altera tu amor ni quiebra tu quietud espiritual (Apocalipsis 14:12). White (1955) define que 'la longanimidad divina reflejada en el hombre es el mayor milagro' (p. 420)."
        }
    },
    "Benignidad": {
        "1-3": {
            "estado": "Aspereza o Severidad en el Trato 🔴",
            "criterio": "Usas palabras cortantes, gestos duros o actúas con frialdad hacia los demás (Proverbios 12:18). White (2012) señaló que 'la aspereza en el hablar aleja a las almas del redil de Dios' (p. 56)."
        },
        "4-5": {
            "estado": "Amabilidad de Conveniencia 🟡",
            "criterio": "Eres gentil con quienes te agradan, pero rudo e indiferente con el resto (Lucas 6:33). White (1959) afirma que 'la cortesía mundana es hipocresía; la benignidad del alma es sincera' (p. 120)."
        },
        "6-7": {
            "estado": "Gentileza en Desarrollo 🟡",
            "criterio": "Te esfuerzas por suavizar tu tono de voz y mostrar empatía, frenando las críticas inmediatas del corazón (Efesios 4:32). White (1953) indica que 'una palabra bondadosa dicha con amor es como un bálsamo celestial' (p. 142)."
        },
        "8-9": {
            "estado": "Dulzura y Empatía Constantes 🟢",
            "criterio": "Tu trato habitual denota una simpatía genuina, ganando la confianza de los afligidos con tu ternura (Colosenses 3:12). White (1954) resalta que 'los modales gentiles de Cristo deben ser reproducidos en Sus hijos' (p. 98)."
        },
        "10": {
            "estado": "Benignidad Celestial Plena 🟢",
            "criterio": "Manifiestas una compasión e inagotable gracia; tus palabras transmiten sanidad divina (Tito 3:4). White (1962) define que 'la cortesía celestial es el idioma de los que vivirán con Dios' (p. 215)."
        }
    },
    "Bondad": {
        "1-3": {
            "estado": "Egoísmo Arraigado o Doblez 🔴",
            "criterio": "Actúas movido solo por tu interest personal, mostrando indiferencia hacia la necesidad ajena (Proverbios 21:13). White (1953) señaló que 'el egoísmo endurece el corazón y cierra los canales del alma' (p. 248)."
        },
        "4-5": {
            "estado": "Generosidad Calculada o Selectiva 🟡",
            "criterio": "Haces buenas obras para cumplir un deber o recibir reconocimiento, pero te cuesta el sacrificio (Mateo 6:1). White (1944) afirma que 'Dios no acepta el servicio motivado por el deseo de alabanza humana' (p. 162)."
        },
        "6-7": {
            "estado": "Rectitud Benevolente 🟡",
            "criterio": "Buscas oportunidades para hacer el bien de forma anónima, invirtiendo tus recursos en el necesitado (Gálatas 6:9). White (2012) indica que 'el verdadero servicio requiere desprendimiento y una abnegación constante' (p. 184)."
        },
        "8-9": {
            "estado": "Integridad y Benevolencia Activas 🟢",
            "criterio": "Tu vida se caracteriza por una búsqueda constante de la justicia y acciones nobles y generosas desinteresadas (Efesios 5:9). White (1943) resalta que 'las obras de beneficencia constante revelan la vida de Cristo en el alma' (p. 312)."
        },
        "10": {
            "estado": "Plenitud de Abnegación Santa 🟢",
            "criterio": "Consagración total al bienestar de la humanidad; tu felicidad radica enteramente en gastarte por otros (Hechos 10:38). White (1955) define que 'el desinterés de Cristo es la norma suprema de la verdadera bondad' (p. 530)."
        }
    },
    # --- SEGMENTO 4: MATRIZ DOCTRINAL ESPECÍFICA (FE, MANSEDUMBRE Y TEMPLANZA) E INICIALIZACIÓN DE CONSECUENCIAS ---
    "Fe": {
        "1-3": {
            "estado": "Incredulidad o Deslealtad Manifiesta 🔴",
            "criterio": "Vives dominado por la duda de las verdades eternas o eres inconstante en tus promesas (Hebreos 3:12). White (2007) señaló que 'la desconfianza en las promesas divinas debilita las fuerzas del alma' (p. 112)."
        },
        "4-5": {
            "estado": "Confianza Intelectual o Tambaleante 🟡",
            "criterio": "Crees en la doctrina de memoria, pero tu fidelidad se quiebra cuando surgen crisis (Santiago 2:19). White (1952) afirma que 'una fe nominal no salva; se requiere un asimiento vivo de la gracia' (p. 294)."
        },
        "6-7": {
            "estado": "Fidelidad en Desarrollo 🟡",
            "criterio": "Mantienes tus pactos con esfuerzo y avanzas en obediencia aun cuando no comprendes el camino (Hebreos 11:1). White (1930) indica que 'la fe verdadera avanza a pesar de las nubes y las dificultades' (p. 145)."
        },
        "8-9": {
            "estado": "Fidelidad Firme e Inquebrantable 🟢",
            "criterio": "Eres una persona plenamente confiable y mantienes una confianza firme en Dios en medio del dolor (2 Timoteo 4:7). White (1911) resalta que 'la fe madura prefiere perder la vida antes que violar un principio sagrado' (p. 455)."
        },
        "10": {
            "estado": "Plenitud de Confianza Absoluta 🟢",
            "criterio": "Posees la fe de Jesús de forma total; nada te hace dudar y tu obediencia al pacto es perfecta (Habacuc 2:4). White (1944) define que 'una fe total une la debilidad humana con el poder omnipotente' (p. 231)."
        }
    },
    "Mansedumbre": {
        "1-3": {
            "estado": "Orgullo, Soberbia o Ira Reactiva 🔴",
            "criterio": "Sufres de susceptibilidad extrema; te ofendes por todo y buscas defender tus derechos con prepotencia (Proverbios 16:18). White (1954) señaló que 'el orgullo es el peor enemigo del crecimiento y el discipulado' (p. 34)."
        },
        "4-5": {
            "estado": "Humildad Externa o Forzada 🟡",
            "criterio": "Callas externamente para evitar problemas, pero por dentro guardas deseos de venganza (Mateo 11:29). White (2009) afirma que 'la mansedumbre no es cobardía, es la fuerza bajo el control divino' (p. 140)."
        },
        "6-7": {
            "estado": "Suavidad en Desarrollo 🟡",
            "criterio": "Aceptas la corrección con calma y buscas responder con un tono suave frente a los insultos (Proverbios 15:1). White (1958) indica que 'recibir injurias sin tomar represalias es una gran lección del cielo' (p. 280)."
        },
        "8-9": {
            "estado": "Humildad y Suavidad de Carácter 🟢",
            "criterio": "Tu espíritu está libre de susceptibilidades; estimas a los demás como superiores (Efesios 4:2). White (1953) resalta que 'la mansedumbre adorna el alma con una hermosura imperecedera' (p. 172)."
        },
        "10": {
            "estado": "Mansedumbre Perfecta de Cristo 🟢",
            "criterio": "Absoluta ausencia de egoísmo; ante la ofensa extrema, solo respondes con intercesión santa (1 Pedro 2:23). White (1955) define que 'el espíritu sumiso de Cristo es la corona de la santificación' (p. 612)."
        }
    },
    "Templanza": {
        "1-3": {
            "estado": "Descontrol, Desenfreno o Indulgencia 🔴",
            "criterio": "Cedes con facilidad ante apetitos físicos, adicciones digitales o pasiones desordenadas (Proverbios 25:28). White (1934) señaló que 'la complacencia del apetito corrompe las facultades morales superiores' (p. 42)."
        },
        "4-5": {
            "estado": "Abstinencia Intermitente o Legalista 🟡",
            "criterio": "Te cuidas por miedo o por cumplir normas estrictas, pero experimentas batallas internas constantes (1 Corintios 9:25). White (1959) afirma que 'el dominio propio impuesto externamente no cambia las inclinaciones del alma' (p. 204)."
        },
        "6-7": {
            "estado": "Dominio Propio en Desarrollo 🟡",
            "criterio": "Gobiernas activamente tus apetitos mediante la autodisciplina diaria, sometiendo tu cuerpo en oración (2 Pedro 1:6). White (1900) indica que 'la templanza bíblica abarca el uso moderado de lo bueno y la abstinencia total de lo malo' (p. 15)."
        },
        "8-9": {
            "estado": "Autocontrol y Equilibrio Estable 🟢",
            "criterio": "Tus pensamientos, deseos físicos y uso del tiempo se encuentran equilibrados bajo una autodisciplina santa (Gálatas 5:23). White (1980b) resalta que 'una mente temperante preserva la claridad necesaria para oír la voz de Dios' (p. 143)."
        },
        "10": {
            "estado": "Plenitud de Dominio Propio 🟢",
            "criterio": "Consagración física y mental absoluta; tu cuerpo y mente son templos perfectamente limpios y santos (1 Corintios 6:19-20). White (2009) define que 'el dominio propio perfecto pone al hombre en armonía con las leyes del cielo' (p. 310)."
        }
    }
}

consecuencias_texto = {
    "1-3": {
        "estado": "Estado Carnal / Alerta Crítica 🔴",
        "corto": "Afectación inmediata en el entorno familiar, brotes de impulsividad y pérdida de control emocional ante la presión.",
        "mediano": "Desgaste de tu salud espiritual por vivir bajo impulsos carnales. Distanciamiento y debilitamiento del testimonio.",
        "largo": "Riesgo crónico de aislamiento emocional, endurecimiento del corazón y desconexión profunda de tu propósito de fe."
    },
    "4-5": {
        "estado": "Esfuerzo Humano Inconstante 🟡",
        "corto": "Inconsistencia en el carácter y respuestas divididas o inestables frente a los problemas cotidianos.",
        "mediano": "Relaciones con altibajos constantes. Sensación de cansancio interno por falta de hábitos de entrega diarios.",
        "largo": "Riesgo latente de estancarse en la mediocridad de una fe puramente formal y nominal, sin poder real."
    },
    "6-7": {
        "estado": "Crecimiento en Transición 🟡",
        "corto": "Respuestas sabias en momentos ordinarios, con ligeras caídas reactivas ante provocaciones extremas.",
        "mediano": "Afinamiento progresivo del carácter. Lazos interpersonales eclesiásticos y familiares más estables y sanos.",
        "largo": "Avance firme hacia una madurez espiritual integral y consolidación paulatina de tu testimonio cristiano."
    },
    "8-9": {
        "estado": "Madurez Consecuente 🟢",
        "corto": "Paz interior manifiesta, respuestas templadas ante crisis e impacto edificante inmediato en tu entorno.",
        "mediano": "Consolidación de relaciones interpersonales sanas y estables. Resiliencia fortalecida frente a las crisis.",
        "largo": "Construcción de un legado de integridad espiritual duradero y capacidad madura para guiar efectivamente a otros."
    },
    "10": {
        "estado": "Plenitud de Permanencia 🟢",
        "corto": "Reflejo nítido de la gracia divina, respuestas llenas de mansedumbre y paz inalterable ante cualquier ofensa.",
        "mediano": "Lazos comunitarios maduros sustentados por el amor agape. Cobertura espiritual e intercesión permanente.",
        "largo": "Legado de santidad intachable que glorifica a Dios y sirve como un modelo vivo de discipulado generacional."
    }
}
# --- SEGMENTO 5: CAPTURA DE DATOS, QR INTELIGENTE MODERNO E INVITACIÓN A LA HONESTIDAD ---
if not st.session_state.diagnostico_generado:
    st.title("🌱 Diagnóstico Espiritual: Los 9 Frutos del Espíritu")
    st.markdown("Evalúa el estado actual de tu carácter basándote en **Gálatas 5:22-23**.")
    st.caption("🎨 **Diseño y Creación:** Desarrollado por **Jacob Zumaya Prianti**.")
    
    nombre_usuario = st.text_input("✍️ Escribe tu nombre para personalizar tu reporte:", value="")
    st.markdown("---")

    # CONTROL DEL QR INTELIGENTE QUE SE OCULTA AL INSTANTE EN DISPOSITIVOS MÓVILES
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
                # Optimizado bajo los nuevos lineamientos requeridos por la consola del servidor
                st.image(buffer_qr.getvalue(), width='stretch')
            except Exception: pass
        with col_txt:
            st.markdown("*¡Al escanearlo, este recuadro desaparecerá de tu pantalla móvil para darte máxima comodidad al responder!*")
        st.markdown("---")

    st.warning("""
    ### 🧠 Invitación a la Honestidad Profunda y Transparente
    Antes de iniciar, tómate un momento de silencio y reverencia. Este ejercicio no tiene el propósito de condenarte ni de calificarte bajo estándares humanos, sino de servir como un espejo espiritual fidedigno. 
    
    **No tengas miedo ni vergüenza de marcar un 1 o un 10.** Si hay un área donde la carne te domina por completo, marcar un **1** es el primer paso de humildad hacia la restauración. De igual manera, si el Espíritu Santo te ha dado la victoria absoluta y constante en un fruto, pon un **10** reconociendo Su poder en ti con gratitud. Responde con absoluta sinceridad delante de Dios.
    """)
          # --- SEGMENTO 6 ACTUALIZADO: FORMULARIO INTERACTIVO ACAPARADO ---
    st.header("📋 Autoevaluación")
    st.subheader("Abre cada fruto y selecciona el nivel exacto que defina tu realidad hoy:")

    with st.form("diagnostico_form"):
        puntajes_temporales = {}
        escala_limpia = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        
        # Lee frutos_info de forma nativa desde la raíz del Segmento 1
        for i, (fruto, info) in enumerate(frutos_info.items(), 1):
            with st.expander(f"✨ {i}. {fruto} ({info['cita']})"):
                st.markdown(f"**De:** *{info['izq']}* \n\n **Hacia:** *{info['der']}*")
                
                sel = st.select_slider(
                    f"Selecciona tu nivel para {fruto}:", 
                    options=escala_limpia, 
                    value="1", 
                    key=f"esfera_{fruto}",
                    label_visibility="collapsed"
                )
                puntajes_temporales[fruto] = int(sel)
                
                st.markdown("""
                <div class="escala-numerica-fija">
                    <span>1</span><span>2</span><span>3</span><span>4</span><span>5</span>
                    <span>6</span><span>7</span><span>8</span><span>9</span><span>10</span>
                </div>
                """, unsafe_allow_html=True)
                
        st.markdown("---")
        enviar = st.form_submit_button("Generar Diagnóstico en Rúbrica")
        
        if enviar:
            st.session_state.respuestas_usuario = puntajes_temporales
            st.session_state.nombre_final = nombre_usuario.strip() if nombre_usuario.strip() != "" else "Invitado"
            st.session_state.diagnostico_generado = True
            st.rerun()


# --- SEGMENTO 7: PANTALLA EXCLUSIVA DE RESULTADOS Y CONSTRUCCIÓN DE GRÁFICA ---
else:
    # Candado de seguridad: Evita el dibujo redundante o duplicaciones lineales de hilos
    if not st.session_state.get("diagnostico_generado", False):
        st.stop()
        
    nombre_final = st.session_state.nombre_final
    puntajes = st.session_state.respuestas_usuario

    # AJUSTE OPTIMIZADO: Fuerza al navegador móvil a subir instantáneamente al inicio del título
    st.markdown("<div id='inicio-resultados'></div>", unsafe_allow_html=True)
    st.markdown("""
        <script>
            var elemento = window.parent.document.getElementById("inicio-resultados");
            if (elemento) {
                elemento.scrollIntoView({behavior: "smooth"});
            }
        </script>
    """, unsafe_allow_html=True)

    st.title("📊 Tu Diagnóstico Espiritual")
    st.header(f"Resultados preparados para: {nombre_final}")
    
    st.subheader("📈 Gráfica de Crecimiento Espiritual")
    frutos_labels = list(puntajes.keys())
    valores_barras = list(puntajes.values())
    
    # Paleta de colores vivos y de alto contraste semaforizado para el plano de barras
    colores_barras = []
    for v in valores_barras:
        if v >= 8: colores_barras.append('#2E7D32')     # Verde Esmeralda Vivo
        elif v >= 5: colores_barras.append('#FBC02D')   # Amarillo Oro Intenso
        else: colores_barras.append('#D32F2F')         # Rojo Carmesí Alerta
        
    # Dimensiones geométricas de ancho extendido (10 pulgadas) para acoplarse simétricamente
    fig, ax = plt.subplots(figsize=(10, 4.5))
    barras = ax.bar(frutos_labels, valores_barras, color=colores_barras, edgecolor='none', width=0.7)
    
    ax.set_ylim(0, 11)
    ax.set_yticks(range(1, 11))
    ax.set_ylabel("Nivel de Intensidad", fontsize=10, weight='bold', color='#222222')
    ax.grid(axis='y', linestyle='--', alpha=0.6, color='#e0e0e0')
    
    # Remoción de márgenes laterales blancos internos en el gráfico de Matplotlib
    ax.set_xmargin(0.02)
    
    # Colocar los números de los puntajes con fuente negrita arriba de cada barra
    for barra in barras:
        alto = barra.get_height()
        ax.annotate(f'{alto}', xy=(barra.get_x() + barra.get_width() / 2, alto),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, weight='bold', color='#111111')
                    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cccccc')
    ax.spines['bottom'].set_color('#cccccc')
    
    plt.xticks(rotation=0, ha='center', fontsize=9, weight='bold', color='#333333')
    plt.tight_layout()
    
    # Desplegar la gráfica simétrica en Streamlit
    st.pyplot(fig)
    
    # Guardar en la memoria volátil en base64 de alta resolución para el PDF
    buf_img = io.BytesIO()
    plt.savefig(buf_img, format='png', dpi=200, bbox_inches='tight')
    buf_img.seek(0)
    img_base64 = base64.b64encode(buf_img.read()).decode('utf-8')
    plt.close(fig)
    
    st.markdown("---")
    
    
    # --- SEGMENTO 8A ACTUALIZADO: ANÁLISIS DE RÚBRICA Y MAQUETACIÓN INICIAL DEL REPORTE CON FECHA ---
    st.subheader("🔍 Análisis Detallado de Madurez")
    
    filas_rubrica_pdf = ""
    lista_consecuencias_pdf = ""
    
    for fruto, score in puntajes.items():
        if score == 10: rango = "10"
        elif score >= 8: rango = "8-9"
        elif score >= 6: rango = "6-7"
        elif score >= 4: rango = "4-5"
        else: rango = "1-3"
            
        info_rubrica = rubrica_detallada[fruto][rango]
        cons_global = consecuencias_texto[rango]
        
        if score >= 8:
            st.success(f"🟢 **{fruto}:** {score}/10 — {info_rubrica['estado']}.\n\n*Criterio Específico:* {info_rubrica['criterio']}")
        elif score >= 5:
            st.warning(f"⚠️ **{fruto}:** {score}/10 — {info_rubrica['estado']}.\n\n*Criterio Específico:* {info_rubrica['criterio']}")
        else:
            st.error(f"🚨 **{fruto}:** {score}/10 — {info_rubrica['estado']}.\n\n*Criterio Específico:* {info_rubrica['criterio']}")
            
        filas_rubrica_pdf += "<tr>"
        filas_rubrica_pdf += "<td style='font-weight:bold; color:#2E7D32; font-size:22px; padding:14px;'>" + str(fruto) + "</td>"
        filas_rubrica_pdf += "<td style='text-align:center; font-weight:bold; font-size:22px; background-color:#f4fbf7; padding:14px;'>" + str(score) + "/10</td>"
        filas_rubrica_pdf += "<td style='font-size:20px; padding:14px; font-weight:bold;'>" + str(info_rubrica['estado']) + "</td>"
        filas_rubrica_pdf += "<td style='font-size:20px; padding:14px; text-align:justify;'>" + str(info_rubrica['criterio']) + "</td>"
        filas_rubrica_pdf += "</tr>"
        
        lista_consecuencias_pdf += "<li style='font-size:20px; margin-bottom:14px; text-align:justify;'><b>" + str(fruto) + " (" + str(score) + "/10):</b> " + str(cons_global['corto']) + " " + str(cons_global['mediano']) + "</li>"

    st.header("💡 Recomendaciones Generales para el Crecimiento")
    st.markdown("1. **Oración de Rendición:** Lleva tus áreas identificadas con puntajes más bajos a tu altar personal de oración diaria, pidiendo al Espíritu Santo que muera tu carne y florezca Su carácter.")
    st.markdown("2. **Pasos Prácticos de Fe:** Selecciona una sola área crítica esta semana y ejecuta de manera intencional acciones concretas.")
    st.markdown("3. **Caminar en Comunidad:** Busca círculos de edificación dentro de la iglesia donde puedas abrir tu corazón de forma madura.")
    
    st.info(f"### 🤝 Una Invitación Especial a Caminar Juntos\nQuerido(a) **{nombre_final}**, te extendemos una invitación sincera para acercarte de manera prioritaria con tu **pastor o con un anciano de confianza de nuestra congregación** para recibir herramientas bíblicas personalizadas.")

    # Ensamblaje modular del documento HTML con textos planos concatenados para el PDF
    html_inicial = """
    <html>
    <head>
        <meta charset='utf-8'>
        <style>
            body { font-family: Arial, sans-serif; padding: 30px; color: #333; line-height: 1.5; }
            .header { text-align: center; border-bottom: 4px solid #2e7d32; padding-bottom: 15px; }
            .header h1 { color: #2e7d32; margin: 0; font-size: 44px; }
            .header p { font-size: 24px; margin: 5px 0 0 0; color: #666; }
            
            /* REQUERIMIENTO ESPECIAL DE FECHA: Caja de flexión para mantener fecha a la izq y nombre a la der en una misma línea */
            .meta-info-row { width: 100%; margin-top: 15px; display: block; overflow: hidden; }
            .meta-fecha { float: left; font-style: italic; color: #555; font-size: 22px; font-weight: bold; }
            .meta-usuario { float: right; font-style: italic; color: #555; font-size: 22px; }
            
            .grafica-box { text-align: center; margin: 25px auto; width: 50%; clear: both; }
            .grafica-box img { width: 100%; max-width: 100%; height: auto; display: block; }
            table { width: 100%; border-collapse: collapse; margin-top: 25px; table-layout: fixed; }
            th, td { border: 2px solid #cccccc; padding: 14px; vertical-align: top; word-wrap: break-word; }
            th { background-color: #f4fbf7; color: #2e7d32; font-size: 22px; font-weight: bold; }
            .seccion-titulo { color: #2e7d32; font-size: 30px; font-weight: bold; margin-top: 45px; border-bottom: 3px solid #2e7d32; padding-bottom: 6px; }
            .lista-estilo { padding-left: 25px; margin-top: 15px; }
            .lista-estilo li { font-size: 20px; margin-bottom: 14px; line-height: 1.6; text-align: justify; }
            .pastoral-box { background-color: #e8f5e9; padding: 25px; margin-top: 40px; border-left: 8px solid #2e7d32; border-radius: 6px; }
            .pastoral-box p { font-size: 20px; margin: 0; line-height: 1.6; }
            .apa-sangria-francesa { padding-left: 35px; text-indent: -35px; font-size: 18px; line-height: 1.6; margin-bottom: 15px; text-align: justify; }
            .footer-creditos { text-align: center; margin-top: 60px; font-size: 16px; color: #777777; border-top: 2px solid #eeeeee; padding-top: 15px; font-style: italic; }
        </style>
    </head>
    <body>
        <div class='header'>
            <h1>🌱 Reporte de Diagnóstico Espiritual</h1>
            <p>Los 9 Frutos del Espíritu (Gálatas 5:22-23)</p>
        </div>
    """

    # Inyección matemática del renglón simétrico: Fecha en el extremo izquierdo y Nombre en el extremo derecho
    html_grafica = "<div class='meta-info-row'><div class='meta-fecha'>Fecha de Apertura: " + str(st.session_state.fecha_apertura) + "</div><div class='meta-usuario'>Diagnóstico preparado especialmente para: <strong>" + str(nombre_final) + "</strong></div></div><div class='grafica-box'><img src='data:image/png;base64," + str(img_base64) + "'/></div>"

    html_tabla = """
        <div class='seccion-titulo'>🔍 1. Rúbrica de Diagnóstico Personalizado del Carácter</div>
        <table>
            <thead>
                <tr>
                    <th style='width: 20%;'>Fruto</th>
                    <th style='width: 13%;'>Puntaje</th>
                    <th style='width: 27%;'>Clasificación Teórica</th>
                    <th style='width: 40%;'>Criterio de Evaluación Real (Biblia / EGW)</th>
                </tr>
            </thead>
            <tbody>
    """ + filas_rubrica_pdf + """
            </tbody>
        </table>
    """

    # --- SEGMENTO 8B: CONSECUENCIAS, BIBLIOGRAFÍA APA 7 Y BOTÓN DE DESCARGA ---
    html_bloque_final = """
    <div class='seccion-titulo'>[Alerta] 2. Posibles Consecuencias en el Carácter</div>
        <ul class='lista-estilo'>
    """ + lista_consecuencias_pdf + """
        </ul>
        
    <div class='seccion-titulo'>[Plan de Acción] 3. Recomendaciones Generales para el Crecimiento</div>
        <ol class='lista-estilo'>
            <li><strong>Oración de Rendición:</strong> Lleva tus áreas identificadas con puntajes más bajos a tu altar personal de oración diaria, pidiendo al Espíritu Santo que muera tu carne y florezca Su carácter.</li>
            <li><strong>Pasos Prácticos de Fe:</strong> Selecciona una sola área crítica esta semana y ejecuta de manera intencional acciones concretas que reflejen la virtud bíblica opuesta.</li>
            <li><strong>Caminar en Comunidad:</strong> Busca círculos de edificación dentro de la iglesia donde puedas abrir tu corazón de forma madura y transparente.</li>
        </ol>

        <div class='pastoral-box'>
            <p>Estimado(a) miembro, te animamos con amor a <strong>presentar y compartir estos resultados en una cita con tu pastor o un anciano de confianza</strong> de tu iglesia local. Encontrarás un espacio sagrado de consejería, oración intercesora y cobertura pastoral idóneo para afirmar tus pasos hacia la estatura de la plenitud de Cristo.</p>
        </div>

        <div class='seccion-titulo'>[Bibliografía] 4. Referencias</div>
        <div style='margin-top: 15px;'>
            <div class='apa-sangria-francesa'>White, E. G. d. (1900). <i>La educación</i>. Asociación Casa Editora Sudamericana.</div>
            <div class='apa-sangria-francesa'>White, E. G. d. (1911). <i>El conflicto de los siglos</i>. Publicaciones Interamericanas.</div>
            <div class='apa-sangria-francesa'>White, E. G. d. (1930). <i>Mensajes para los jóvenes</i>. Asociación Casa Editora Sudamericana.</div>
            <div class='apa-sangria-francesa'>White, E. G. d. (1934). <i>Consejos sobre el régimen alimenticio</i>. Publicaciones Interamericanas.</div>
            <div class='apa-sangria-francesa'>White, E. G. d. (1943). <i>Testimonios para la iglesia</i> (Vol. 6). Pacific Press Publishing Association.</div>
            <div class='apa-sangria-francesa'>White, E. G. d. (1944). <i>Palabras de vida del gran maestro</i>. Pacific Press Publishing Association.</div>
            <div class='apa-sangria-francesa'>White, E. G. d. (1947). <i>El ministerio de curación</i>. Publicaciones Interamericanas.</div>
            <div class='apa-sangria-francesa'>White, E. G. d. (1951). <i>Testimonios para la iglesia</i> (Vol. 4). Pacific Press Publishing Association.</div>
            <div class='apa-sangria-francesa'>White, E. G. d. (1952). <i>Testimonios para la iglesia</i> (Vol. 5). Pacific Press Publishing Association.</div>
            <div class='apa-sangria-francesa'>White, E. G. d. (1953). <i>Joyas de los testimonios</i> (Vols. 1-3). Asociación Casa Editora Sudamericana.</div>
            <div class='apa-sangria-francesa'>White, E. G. d. (1954). <i>El discurso maestro de Jesucristo</i>. Pacific Press Publishing Association.</div>
            <div class='apa-sangria-francesa'>White, E. G. d. (1955). <i>El deseado de todas las gentes</i>. Publicaciones Interamericanas.</div>
            <div class='apa-sangria-francesa'>White, E. G. d. (1958). <i>Mensajes selectos</i> (Vol. 1). Asociación Casa Editora Sudamericana.</div>
            <div class='apa-sangria-francesa'>White, E. G. d. (1959). <i>Mente, carácter y personalidad</i> (Vols. 1-2). Inter-American Division Publishing Association.</div>
            <div class='apa-sangria-francesa'>White, E. G. d. (1962). <i>Hijos e hijas de Dios</i>. Asociación Casa Editora Sudamericana.</div>
            <div class='apa-sangria-francesa'>White, E. G. d. (1980a). <i>La temperancia</i>. Pacific Press Publishing Association.</div>
            <div class='apa-sangria-francesa'>White, E. G. d. (1980b). <i>El ministerio de la bondad</i>. Asociación Casa Editora Sudamericana.</div>
            <div class='apa-sangria-francesa'>White, E. G. d. (2007). <i>El camino a Cristo</i>. Publicaciones Interamericanas.</div>
            <div class='apa-sangria-francesa'>White, E. G. d. (2009). <i>Consejos para la iglesia</i>. Pacific Press Publishing Association.</div>
            <div class='apa-sangria-francesa'>White, E. G. d. (2012). <i>Reflejemos a Jesús</i>. Asociación Casa Editora Sudamericana.</div>
        </div>

        <div class='footer-creditos'>Este diagnóstico espiritual fue creado y desarrollado por Jacob Zumaya Prianti. © 2026 Todos los derechos reservados.</div>
    </body>
    </html>
    """
    
    html_reporte_completo = html_inicial + html_grafica + html_tabla + html_bloque_final

    st.markdown("### 📥 Descarga tu Reporte Oficial")
    
    st.download_button(
        label="Descargar Reporte Completo (PDF / HTML)", 
        data=html_reporte_completo, 
        file_name=f"diagnostico_{nombre_final.lower()}.html", 
        mime="text/html",
        key="btn_descarga_reporte_apa"
    )
    
    st.markdown("---")
    st.caption("🎨 **Diseño y Creación:** Diagnóstico Espiritual desarrollado por **Jacob Zumaya Prianti**.")
    
    st.markdown("---")
    if st.button("✅ Ya descargué mi reporte, avanzar al siguiente paso", key="btn_avanzar_felicitacion"):
        st.session_state.mostrar_felicitacion = True
        st.rerun()

