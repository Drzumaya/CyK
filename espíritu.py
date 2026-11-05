# [Nota de Integración]: El código fuente completo de la aplicación en Streamlit abarca la configuración inicial,
# la matriz doctrinal con los 45 criterios únicos (Amor, Gozo, Paz, Paciencia, Benignidad, Bondad, Fe, Mansedumbre y Templanza)
# con sus respectivas citas bíblicas y referencias de Elena G. de White, el sistema de autoevaluación con código QR para móviles,
# y la generación del reporte HTML/PDF con estilo semaforizado y doble tamaño tipográfico.
# Puedes consultar o copiar la estructura modular completa en el desarrollo técnico provisto para Jacob Zumaya Prianti.

import streamlit as st
import pandas as pd
import segno
import io
import base64
import matplotlib.pyplot as plt

# 1. Configuración de la página institucional y estados de sesión
st.set_page_config(
    page_title="Diagnóstico: Los 9 Frutos del Espíritu",
    page_icon="🌱",
    layout="centered"
)

for var, val in [("mostrar_felicitacion", False), ("finalizado", False), ("diagnostico_generado", False), ("respuestas_usuario", {})]:
    if var not in st.session_state:
        st.session_state[var] = val

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

# Control de pantallas finales y reinicio
if st.session_state.finalizado:
    st.success("👋 ¡Gracias por tu participación!")
    st.markdown("### El diagnóstico ha concluido de forma exitosa")
    st.caption("🎨 Diagnóstico Espiritual desarrollado por **Jacob Zumaya Prianti**.")
    st.stop()

if st.session_state.mostrar_felicitacion:
    st.balloons()
    st.success("🎉 ¡Muchas felicidades por completar este paso fundamental!")
    if st.button("🔄 Nuevo diagnóstico"):
        st.session_state.update({"diagnostico_generado": False, "mostrar_felicitacion": False, "respuestas_usuario": {}})
        st.rerun()
    st.stop()
# --- SEGMENTO 2A: MATRIZ DE CRITERIOS ESPECÍFICOS (AMOR, GOZO Y PAZ) ---
rubrica_detallada = {
    "Amor": {
        "1-3": {
            "estado": "Amor Carnal o Indiferencia 🔴",
            "criterio": "Afecto condicional, resentimiento oculto o apatía hacia las faltas del prójimo. Cita: 1 Juan 4:20. EGW: 'El egoísmo es un cáncer frío que destruye los lazos del alma' (Joyas de los Testimonios, Vol. 1)."
        },
        "4-5": {
            "estado": "Esfuerzo Humano Inconstante 🟡",
            "criterio": "Amas cuando recibes aprobación, pero te cuesta manifestar gracia ante la ofensa o el desprecio. Cita: Mateo 5:46. EGW: 'El amor puramente humano se desvanece ante la prueba' (El Deseado de Todas las Gentes)."
        },
        "6-7": {
            "estado": "Crecimiento en Transición 🟡",
            "criterio": "Buscas amar intencionalmente y perdonar con prontitud, batallando activamente contra el orgullo herido. Cita: 1 Corintios 13:4. EGW: 'El amor cristiano es un principio divino, no una emoción fugaz' (El Discurso Maestro de Jesucristo)."
        },
        "8-9": {
            "estado": "Madurez Consecuente 🟢",
            "criterio": "El sacrificio y la aceptación incondicional del prójimo son rasgos habituales y firmes en tu carácter. Cita: Romanos 12:9. EGW: 'El amor es la base de la piedad y la semejanza con Dios' (Palabras de Vida del Gran Maestro)."
        },
        "10": {
            "estado": "Plenitud de Permanencia 🟢",
            "criterio": "Reflejas perfectamente el amor agape; estás crucificado al 'Yo' y vives solo para bendecir. Cita: Gálatas 2:20. EGW: 'Cuando el amor de Cristo inunde el alma, fluirá como un manantial' (El Camino a Cristo)."
        }
    },
    "Gozo": {
        "1-3": {
            "estado": "Amargura o Queja Constante 🔴",
            "criterio": "Tu estado de ánimo depende enteramente de las circunstancias; caes fácil en la murmuración. Cita: Filipenses 2:14. EGW: 'La melancolía y la queja deshonran al Redentor' (Mente, Carácter y Personalidad, Vol. 2)."
        },
        "4-5": {
            "estado": "Alegría Superficial e Inestable 🟡",
            "criterio": "Sientes gozo en el culto o momentos buenos, pero las dificultades diarias te hunden en el desánimo. Cita: Santiago 1:2. EGW: 'La fe inmadura busca solo el sol y se acobarda ante la tormenta' (Testimonios para la Iglesia, Vol. 4)."
        },
        "6-7": {
            "estado": "Regocijo en Desarrollo 🟡",
            "criterio": "Decides alabar a Dios en la prueba, logrando estabilizar tus emociones mediante la gratitud activa. Cita: Habacuc 3:17-18. EGW: 'La alabanza expulsa las sombras sembradas por el enemigo' (El Ministerio de Curación)."
        },
        "8-9": {
            "estado": "Gozo Profundo y Firme 🟢",
            "criterio": "Posees una paz gozosa e inalterable basada en las promesas divinas, que inspira a los demás. Cita: Salmo 16:11. EGW: 'Un espíritu alegre es un tónico permanente para el alma y el cuerpo' (La Educación)."
        },
        "10": {
            "estado": "Plenitud de Regocijo Santo 🟢",
            "criterio": "Vives en un estado permanente de alabanza y regocijo celestial, sin importar la prueba física o mental. Cita: 1 Pedro 1:8. EGW: 'El gozo del Señor en el corazón es una luz incombustible' (Hijos e Hijas de Dios)."
        }
    },
    "Paz": {
        "1-3": {
            "estado": "Ansiedad Crónica o Discordia 🔴",
            "criterio": "Vives esclavo del temor al futuro, el control obsesivo o promueves tensiones en tu entorno. Cita: Isaías 57:21. EGW: 'La preocupación es ciega e incapaz de vislumbrar el mañana' (El Ministerio de Curación)."
        },
        "4-5": {
            "estado": "Calma Condicionada 🟡",
            "criterio": "Tienes tranquilidad solo cuando no hay imprevistos ni tensiones financieras o familiares en el hogar. Cita: Juan 14:27. EGW: 'La paz del mundo es un barniz que se agrieta al menor sismo' (El Camino a Cristo)."
        },
        "6-7": {
            "estado": "Tranquilidad en Transición 🟡",
            "criterio": "Logras calmar tu mente mediante la oración constante, entregando tus cargas al Señor con mayor rapidez. Cita: Filipenses 4:6-7. EGW: 'Entregar la voluntad a Dios aquieta las tempestades del alma' (El Discurso Maestro de Jesucristo)."
        },
        "8-9": {
            "estado": "Paz Sobrenatural Estables 🟢",
            "criterio": "Reflejas serenidad en medio de crisis graves, actuando con madurez como un agente pacificador activo. Cita: Isaías 26:3. EGW: 'La paz de Cristo es un escudo que las saetas del mundo no pueden penetrar' (Testimonios para la Iglesia, Vol. 5)."
        },
        "10": {
            "estado": "Reposo Absoluto en el Señor 🟢",
            "criterio": "Comunión perfecta que produce un sosiego idéntico al de Cristo durmiendo en la barca en medio de la tempestad. Cita: Salmo 119:165. EGW: 'Estar escondido con Cristo en Dios es el descanso supremo' (Joyas de los Testimonios, Vol. 3)."
        }
    },
    # --- SEGMENTO 2B: MATRIZ DE CRITERIOS ESPECÍFICOS (PACIENCIA, BENIGNIDAD Y BONDAD) ---
    "Paciencia": {
        "1-3": {
            "estado": "Intolerancia o Irritabilidad Directa 🔴",
            "criterio": "Reaccionas con enojo inmediato ante retrasos, errores de otros o cambios de planes. Cita: Proverbios 14:29. EGW: 'Un espíritu impaciente disipa la fragancia de la piedad' (Palabras de Vida del Gran Maestro)."
        },
        "4-5": {
            "estado": "Resistencia Humana Limitada 🟡",
            "criterio": "Soportas las dificultades por un tiempo, pero terminas explotando si la presión o la espera se alargan. Cita: Eclesiastés 7:8. EGW: 'La paciencia no es solo silencio externo, sino quietud en el corazón' (Consejos para la Iglesia)."
        },
        "6-7": {
            "estado": "Soportar Intencional 🟡",
            "criterio": "Controlas tus reacciones ásperas pidiendo paciencia en silencio, tolerando las debilidades del prójimo. Cita: Colosenses 3:13. EGW: 'Dominar la lengua en el momento del desespero es una victoria santa' (Mensajes para los Jóvenes)."
        },
        "8-9": {
            "estado": "Longanimidad Madura 🟢",
            "criterio": "Soportas con mansedumbre las pruebas prolongadas y tratas con profunda calma a las personas difíciles. Cita: Santiago 5:7-8. EGW: 'La paciencia madura es el oro purificado en el fuego de la prueba' (Testimonios para la Iglesia, Vol. 1)."
        },
        "10": {
            "estado": "Paciencia Perfecta de Cristo 🟢",
            "criterio": "Vives la constancia perfecta; ninguna provocación altera tu amor ni quiebra tu quietud espiritual. Cita: Apocalipsis 14:12. EGW: 'La longanimidad divina reflejada en el hombre es el mayor milagro' (El Deseado de Todas las Gentes)."
        }
    },
    "Benignidad": {
        "1-3": {
            "estado": "Aspereza o Severidad en el Trato 🔴",
            "criterio": "Usas palabras cortantes, gestos duros o actúas con frialdad y distanciamiento emocional hacia los demás. Cita: Proverbios 12:18. EGW: 'La aspereza en el hablar aleja a las almas del redil de Dios' (El Ministerio de la Bondad)."
        },
        "4-5": {
            "estado": "Amabilidad de Conveniencia 🟡",
            "criterio": "Eres gentil y suave con quienes te agradan o te benefician, pero rudo e indiferente con el resto. Cita: Lucas 6:33. EGW: 'La cortesía mundana es hipocresía; la benignidad del alma es sincera' (La Educación)."
        },
        "6-7": {
            "estado": "Gentileza en Desarrollo 🟡",
            "criterio": "Te esfuerzas por suavizar tu tono de voz y mostrar empatía, frenando las críticas inmediatas del corazón. Cita: Efesios 4:32. EGW: 'Una palabra bondadosa dicha con amor es como un bálsamo celestial' (Testimonios para la Iglesia, Vol. 3)."
        },
        "8-9": {
            "estado": "Dulzura y Empatía Constantes 🟢",
            "criterio": "Tu trato habitual denota una simpatía genuina, ganando la confianza de los afligidos con tu ternura. Cita: Colosenses 3:12. EGW: 'Los modales gentiles de Cristo deben ser reproducidos en Sus hijos' (El Discurso Maestro de Jesucristo)."
        },
        "10": {
            "estado": "Benignidad Celestial Plena 🟢",
            "criterio": "Manifiestas una compasión y gracia inagotables; tus palabras y presencia transmiten sanidad divina. Cita: Tito 3:4. EGW: 'La cortesía celestial es el idioma de los que vivirán con Dios' (Hijos e Hijas de Dios)."
        }
    },
    "Bondad": {
        "1-3": {
            "estado": "Egoísmo Arraigado o Doblez 🔴",
            "criterio": "Actúas movido solo por tu interés personal, mostrando indiferencia o malicia hacia la necesidad ajena. Cita: Proverbios 21:13. EGW: 'El egoísmo endurece el corazón y cierra los canales del alma' (Joyas de los Testimonios, Vol. 2)."
        },
        "4-5": {
            "estado": "Generosidad Calculada o Selectiva 🟡",
            "criterio": "Haces buenas obras para cumplir un deber o recibir reconocimiento, pero te cuesta sacrificarte por otros. Cita: Mateo 6:1. EGW: 'Dios no acepta el servicio motivado por el deseo de alabanza humana' (Palabras de Vida del Gran Maestro)."
        },
        "6-7": {
            "estado": "Rectitud Benevolente 🟡",
            "criterio": "Buscas oportunidades para hacer el bien de forma anónima, invirtiendo tus recursos materiales en el necesitado. Cita: Gálatas 6:9. EGW: 'El verdadero servicio requiere desprendimiento y una abnegación constante' (El Ministerio de la Bondad)."
        },
        "8-9": {
            "estado": "Integridad y Benevolencia Activas 🟢",
            "criterio": "Tu vida se caracteriza por una búsqueda constante de la justicia y acciones nobles y generosas desinteresadas. Cita: Efesios 5:9. EGW: 'Las obras de beneficencia constante revelan la vida de Cristo en el alma' (Testimonios para la Iglesia, Vol. 6)."
        },
        "10": {
            "estado": "Plenitud de Abnegación Santa 🟢",
            "criterio": "Consagración total al bienestar de la humanidad; tu felicidad radica enteramente en gastarte por otros. Cita: Hechos 10:38. EGW: 'El desinterés de Cristo es la norma suprema de la verdadera bondad' (El Deseado de Todas las Gentes)."
        }
    },
    # --- SEGMENTO 2C: MATRIZ DE CRITERIOS ESPECÍFICOS (FE, MANSEDUMBRE Y TEMPLANZA) E INVITACIÓN AL TEST ---
    "Fe": {
        "1-3": {
            "estado": "Incredulidad o Deslealtad Manifiesta 🔴",
            "criterio": "Vives dominado por la duda de las verdades eternas o eres inconstante y desleal en tus promesas y pactos. Cita: Hebreos 3:12. EGW: 'La desconfianza en las promesas divinas debilita las fuerzas del alma' (El Camino a Cristo)."
        },
        "4-5": {
            "estado": "Confianza Intelectual o Tambaleante 🟡",
            "criterio": "Crees en la doctrina de memoria, pero tu fidelidad se quiebra cuando surgen crisis financieras o de salud. Cita: Santiago 2:19. EGW: 'Una fe nominal no salva; se requiere un asimiento vivo de la gracia' (Testimonios para la Iglesia, Vol. 5)."
        },
        "6-7": {
            "estado": "Fidelidad en Desarrollo 🟡",
            "criterio": "Mantienes tus pactos con esfuerzo y avanzas en obediencia aun cuando no comprendes el camino del Señor. Cita: Hebreos 11:1. EGW: 'La fe verdadera avanza a pesar de las nubes y las dificultades' (Mensajes para los Jóvenes)."
        },
        "8-9": {
            "estado": "Fidelidad Firme e Inquebrantable 🟢",
            "criterio": "Eres una persona plenamente confiable y mantienes una confianza firme en Dios en medio del dolor o la escasez. Cita: 2 Timoteo 4:7. EGW: 'La fe madura prefiere perder la vida antes que violar un principio sagrado' (El Conflicto de los Siglos)."
        },
        "10": {
            "estado": "Plenitud de Confianza Absoluta 🟢",
            "criterio": "Posees la fe de Jesús de forma total; nada te hace dudar y tu obediencia al pacto es perfecta y santa. Cita: Habacuc 2:4. EGW: 'Una fe total une la debilidad humana con el poder omnipotente' (Palabras de Vida del Gran Maestro)."
        }
    },
    "Mansedumbre": {
        "1-3": {
            "estado": "Orgullo, Soberbia o Ira Reactiva 🔴",
            "criterio": "Sufres de susceptibilidad extrema; te ofendes por todo y buscas defender con prepotencia tus derechos. Cita: Proverbios 16:18. EGW: 'El orgullo es el peor enemigo del crecimiento y el discipulado' (El Discurso Maestro de Jesucristo)."
        },
        "4-5": {
            "estado": "Humildad Externa o Forzada 🟡",
            "criterio": "Callas externamente para evitar problemas, pero por dentro hierves de resentimiento o deseos de venganza. Cita: Mateo 11:29. EGW: 'La mansedumbre no es cobardía, es la fuerza bajo el control divino' (Consejos para la Iglesia)."
        },
        "6-7": {
            "estado": "Suavidad en Desarrollo 🟡",
            "criterio": "Aceptas la corrección con calma y buscas responder con un tono suave frente a los insultos o ataques. Cita: Proverbios 15:1. EGW: 'Recibir injurias sin tomar represalias es una gran lección del cielo' (Mensajes Selectos, Vol. 1)."
        },
        "8-9": {
            "estado": "Humildad y Suavidad de Carácter 🟢",
            "criterio": "Tu espíritu está libre de susceptibilidades; estimas a los demás como superiores y perdonas de corazón. Cita: Efesios 4:2. EGW: 'La mansedumbre adorna el alma con una hermosura imperecedera' (Joyas de los Testimonios, Vol. 1)."
        },
        "10": {
            "estado": "Mansedumbre Perfecta de Cristo 🟢",
            "criterio": "Absoluta ausencia de egoísmo; ante la crucifixión u ofensa extrema, solo respondes con intercesión santa. Cita: 1 Pedro 2:23. EGW: 'El espíritu sumiso de Cristo es la corona de la santificación' (El Deseado de Todas las Gentes)."
        }
    },
    "Templanza": {
        "1-3": {
            "estado": "Descontrol, Desenfreno o Indulgencia 🔴",
            "criterio": "Cedes con facilidad ante apetitos físicos, adicciones digitales, gastos compulsivos o pasiones desordenadas. Cita: Proverbios 25:28. EGW: 'La complacencia del apetito corrompe las facultades morales superiores' (Consejos sobre el Régimen Alimenticio)."
        },
        "4-5": {
            "estado": "Abstinencia Intermitente o Legalista 🟡",
            "criterio": "Te cuidas por miedo a enfermarte o por cumplir normas estrictas, pero experimentas batallas internas constantes. Cita: 1 Corintios 9:25. EGW: 'El dominio propio impuesto externamente no cambia las inclinaciones del alma' (La Educación)."
        },
        "6-7": {
            "estado": "Dominio Propio en Desarrollo 🟡",
            "criterio": "Gobiernas activamente tus apetitos mediante la autodisciplina diaria, sometiendo tu cuerpo en oración. Cita: 2 Pedro 1:6. EGW: 'La templanza bíblica abarca el uso moderado de lo bueno y la abstinencia total de lo malo' (La Temperancia)."
        },
        "8-9": {
            "estado": "Autocontrol y Equilibrio Estable 🟢",
            "criterio": "Tus pensamientos, deseos físicos y uso del tiempo se encuentran equilibrados bajo una autodisciplina santa. Cita: Gálatas 5:23. EGW: 'Una mente temperante preserva la claridad necesaria para oír la voz de Dios' (Mente, Carácter y Personalidad, Vol. 1)."
        },
        "10": {
            "estado": "Plenitud de Dominio Propio 🟢",
            "criterio": "Consagración física y mental absoluta; tu cuerpo y mente son templos perfectamente limpios y santos. Cita: 1 Corintios 6:19-20. EGW: 'El dominio propio perfecto pone al hombre en armonía con las leyes del cielo' (Consejos para la Iglesia)."
        }
    }
}

# Diccionario resumido de consecuencias globales por rangos para uso en la lógica
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
        "mediano": "Consolidación de relaciones interpersonales sanas y estables. Resiliencia fortalecida frente a las pruebas.",
        "largo": "Construcción de un legado de integridad espiritual duradero y capacidad madura para guiar efectivamente a otros."
    },
    "10": {
        "estado": "Plenitud de Permanencia 🟢",
        "corto": "Reflejo nítido de la gracia divina, respuestas llenas de mansedumbre y paz inalterable ante cualquier ofensa.",
        "mediano": "Lazos comunitarios maduros sustentados por el amor agape. Cobertura espiritual e intercesión permanente.",
        "largo": "Legado de santidad intachable que glorifica a Dios y sirve como un modelo vivo de discipulado generacional."
    }
}

# --- CONTROL CONDICIONAL DE PANTALLAS ---
if not st.session_state.diagnostico_generado:
    st.title("🌱 Diagnóstico Espiritual: Los 9 Frutos del Espíritu")
    st.markdown("Evalúa el estado actual de tu carácter basándote en **Gálatas 5:22-23**.")
    st.caption("🎨 **Diseño y Creación:** Desarrollado por **Jacob Zumaya Prianti**.")
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
            except Exception: pass
        with col_txt:
            st.markdown("*¡Al escanearlo, este recuadro desaparecerá de tu pantalla móvil para darte máxima comodidad!*")
        st.markdown("---")

    st.warning("""
    ### 🧠 Invitación a la Honestidad Profunda y Transparente
    Antes de iniciar, tómate un momento de silencio y reverencia. Este ejercicio no tiene el propósito de condenarte ni de calificarte bajo estándares humanos, sino de servir como un espejo espiritual fidedigno. 
    
    **No tengas miedo ni vergüenza de marcar un 1 o un 10.** Si hay un área donde la carne te domina por completo, marcar un **1** es el primer paso de humildad hacia la restauración. De igual manera, si el Espíritu Santo te ha dado la victoria absoluta y constante en un fruto, pon un **10** reconociendo Su poder en ti con gratitud. Responde con absoluta sinceridad delante de Dios.
    """)
    # --- PARTE 3: CUESTIONARIO MODULAR INTERACTIVO (ESFERAS INICIANDO EN 3) ---
    st.header("📋 Autoevaluación")
    st.subheader("Abre cada fruto y selecciona el nivel exacto que defina tu realidad hoy:")

    with st.form("diagnostico_form"):
        puntajes_temporales = {}
        # Lista estructurada de esferas semaforizadas
        esferas = ["1 🔴", "2 🔴", "3 🔴", "4 🔴", "5 🟡", "6 🟡", "7 🟡", "8 🟢", "9 🟢", "10 🟢"]
        
        for i, (fruto, info) in enumerate(frutos_info.items(), 1):
            with st.expander(f"✨ {i}. {fruto} ({info['cita']})"):
                st.markdown(f"**De:** *{info['izq']}* \n\n **Hacia:** *{info['der']}*")
                
                # Control deslizante nativo oculto bajo estilos CSS personalizados
                sel = st.select_slider(
                    f"Selecciona tu nivel para {fruto}:", 
                    options=esferas, 
                    value="3 🔴", # Inicialización fija solicitada en el nivel 3
                    key=f"esfera_{fruto}",
                    label_visibility="collapsed"
                )
                
                # Conversión segura extrayendo el entero inicial antes del emoji
                puntajes_temporales[fruto] = int(sel.split()[0])
                
                # Escala numérica explícita y perfectamente alineada debajo de la barra
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
        if v >= 8: colores_barras.append('#2E7D32')     # Verde Esmeralda
        elif v >= 5: colores_barras.append('#FBC02D')   # Amarillo Oro
        else: colores_barras.append('#D32F2F')         # Rojo Carmesí
        
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
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, weight='bold', color='#111111')
                    
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
    
    # Procesar los 45 criterios únicos dinámicamente según la respuesta individual
    for fruto, score in puntajes.items():
        if score == 10: rango = "10"
        elif score >= 8: rango = "8-9"
        elif score >= 6: rango = "6-7"
        elif score >= 4: rango = "4-5"
        else: rango = "1-3"
            
        # Extraer criterio hiper-específico de la matriz de la Parte 2
        info_rubrica = rubrica_detallada[fruto][rango]
        cons_global = consecuencias_texto[rango]
        
        # Despliegue condicional semaforizado en la interfaz web
        if score >= 8:
            st.success(f"🟢 **{fruto}:** {score}/10 — {info_rubrica['estado']}.\n\n*Criterio Específico:* {info_rubrica['criterio']}")
        elif score >= 5:
            st.warning(f"⚠️ **{fruto}:** {score}/10 — {info_rubrica['estado']}.\n\n*Criterio Específico:* {info_rubrica['criterio']}")
        else:
            st.error(f"🚨 **{fruto}:** {score}/10 — {info_rubrica['estado']}.\n\n*Criterio Específico:* {info_rubrica['criterio']}")
            
        # Compilación simétrica de las filas para la Rúbrica del PDF
        filas_rubrica_pdf += f"""
        <tr>
            <td style='font-weight:bold; color:#2E7D32; font-size:22px; padding:12px;'>{fruto}</td>
            <td style='text-align:center; font-weight:bold; font-size:22px; background-color:#f4fbf7; padding:12px;'>{score}/10</td>
            <td style='font-size:20px; padding:12px; font-weight:bold;'>{info_rubrica['estado']}</td>
            <td style='font-size:20px; padding:12px; text-align:justify;'>{info_rubrica['criterio']}</td>
        </tr>
        """
        
        # Compilación de la sección aislada de consecuencias breves
        lista_consecuencias_pdf += f"""
        <li style='font-size:20px; margin-bottom:12px; text-align:justify;'>
            <b>{fruto} ({score}/10):</b> {cons_global['corto']} {cons_global['mediano']}
        </li>
        """

    st.header("💡 Recomendaciones Generales para el Crecimiento")
    st.markdown("1. **Oración de Rendición:** Lleva tus áreas más bajas a tu altar personal de oración diaria.\n2. **Pasos Prácticos de Fe:** Selecciona una sola área crítica esta semana y ejecuta acciones intencionales de cambio.\n3. **Caminar en Comunidad:** Busca círculos de edificación dentro de la iglesia.")
    
    st.info(f"""
    ### 🤝 Una Invitación Especial a Caminar Juntos
    Querido(a) **{nombre_final}**, te extendemos una invitación sincera, afectuosa y completamente confidencial para acercarte de manera prioritaria con tu **pastor o con un anciano de confianza de nuestra congregación** para recibir herramientas bíblicas personalizadas.
    """)

    # --- MAQUETACIÓN FINAL DEL REPORTE PDF (ESTRUCTURA SOLICITADA) ---
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
            
            /* Gráfica compacta al 50% centrada de forma simétrica */
            .grafica-box {{ text-align: center; margin: 25px auto; width: 50%; }}
            .grafica-box img {{ width: 100%; max-width: 100%; height: auto; display: block; }}
            
            /* Tabla extendida simétricamente al 100% */
            table {{ width: 100%; border-collapse: collapse; margin-top: 25px; table-layout: fixed; }}
            th, td {{ border: 2px solid #cccccc; padding: 14px; vertical-align: top; word-wrap: break-word; }}
            th {{ background-color: #f4fbf7; color: #2e7d32; font-size: 22px; font-weight: bold; }}
            
            .seccion-titulo {{ color: #2e7d32; font-size: 30px; font-weight: bold; margin-top: 45px; border-bottom: 3px solid #2e7d32; padding-bottom: 6px; }}
            .lista-estilo {{ padding-left: 25px; margin-top: 15px; }}
            .lista-estilo li {{ font-size: 20px; margin-bottom: 14px; line-height: 1.6; text-align: justify; }}
            
            .pastoral-box {{ background-color: #e8f5e9; padding: 25px; margin-top: 40px; border-left: 8px solid #2e7d32; border-radius: 6px; }}
            .pastoral-box h3 {{ margin-top: 0; color: #2e7d32; font-size: 26px; }}
            .pastoral-box p {{ font-size: 20px; margin: 0; line-height: 1.6; }}
            
            .footer-creditos {{ text-align: center; margin-top: 60px; font-size: 16px; color: #777777; border-top: 2px solid #eeeeee; padding-top: 15px; font-style: italic; }}
        </style>
    </head>
    <body>
        <div class='header'>
            <h1>🌱 Reporte de Diagnóstico Espiritual</h1>
            <p>Los 9 Frutos del Espíritu (Gálatas 5:22-23)</p>
        </div>
        <div class='user-info'>Diagnóstico preparado especialmente para: <strong>{nombre_final}</strong></div>
        
        <div class='grafica-box'>
            <img src='data:image/png;base64,{img_base64}'/>
        </div>

        <!-- APARTADO 1: RÚBRICA CON DETALLE EXCLUSIVO INDIVIDUAL -->
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
                {filas_rubrica_pdf}
            </tbody>
        </table>
        
        <!-- APARTADO 2: CONSECUENCIAS BREVES SEPARADAS -->
        <div class='seccion-titulo'>⚠️ 2. Posibles Consecuencias en el Carácter</div>
        <ul class='lista-estilo'>
            {lista_consecuencias_pdf}
        </ul>
        
        <!-- APARTADO 3: RECOMENDACIONES Y INVITACIÓN PASTORAL -->
        <div class='seccion-titulo'>💡 3. Recomendaciones Generales para el Crecimiento</div>
        <ol class='lista-estilo'>
            <li><strong>Oración de Rendición:</strong> Lleva tus áreas identificadas con puntajes más bajos a tu altar personal de oración diaria, pidiendo al Espíritu Santo que muera tu carne y florezca Su carácter.</li>
            <li><strong>Pasos Prácticos de Fe:</strong> Selecciona una sola área crítica esta semana y ejecuta de manera intencional acciones concretas que reflejen la virtud bíblica opuesta.</li>
            <li><strong>Caminar en Comunidad:</strong> Busca círculos de edificación dentro de la iglesia donde puedas abrir tu corazón de forma madura y transparente.</li>
        </ol>

        <div class='pastoral-box'>
            <h3>🤝 Un Llamado al Acompañamiento y Cuidado Espiritual</h3>
            <p>Estimado(a) **{nombre_final}**, te animamos con amor a <strong>presentar y compartir estos resultados en una cita con tu pastor o un anciano de confianza</strong> de tu iglesia local. Encontrarás un espacio sagrado de consejería, oración intercesora y cobertura pastoral idóneo para afirmar tus pasos hacia la estatura de la plenitud de Cristo.</p>
        </div>

        <div class='footer-creditos'>Este diagnóstico espiritual fue creado y desarrollado por Jacob Zumaya Prianti. © 2026 Todos los derechos reservados.</div>
    </body>
    </html>
    """

    st.markdown("### 📥 Descarga tu Reporte Oficial")
    st.download_button("Descargar Reporte Completo (PDF / HTML)", data=html_reporte, file_name=f"diagnostico_{nombre_final.lower()}.html", mime="text/html")
    
    st.markdown("---")
    st.caption("🎨 Diseño y Creación: Diagnóstico Espiritual desarrollado por Jacob Zumaya Prianti.")
    st.markdown("---")
    if st.button("✅ Ya descargué mi reporte, avanzar al siguiente paso"):
        st.session_state.mostrar_felicitacion = True
        st.rerun()
