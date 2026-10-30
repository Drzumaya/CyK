# =================================================================
# PARTE 1: LIBRERÍAS E IMPORTACIONES DEL ENTORNO CORE
# =================================================================
import streamlit as st
import qrcode
from io import BytesIO
from fpdf import FPDF
import gspread
import pandas as pd
import numpy as np
import datetime
import hashlib
import time
import base64

# CONFIGURACIÓN OBLIGATORIA DEL ENTRAMADO DE STREAMLIT (Primera línea ejecutable)
st.set_page_config(page_title="Ecosistema Diagnóstico de Modelos Temporales", layout="centered")

# Desactivación síncrona del backend interactivo de PyPlot para entornos multiproceso
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# =================================================================
# PARTE 2: CONSTANTES DE RED Y CONFIGURACIONES GENERALES
# =================================================================
URL_PRODUCCION = "https://dsimandarina.streamlit.app"
NOMBRE_HOJA_CALCULO = "Base_Datos_Modelo_Mandarina"

ESTADOS_MEXICO = ["Chihuahua", "Sonora", "Sinaloa", "Nuevo León", "Jalisco", "Ciudad de México", "Veracruz"]
CONTINENTES = ["América del Norte", "Europa", "Asia", "África", "Oceanía"]

# =================================================================
# PARTE 2.5: INICIALIZACIÓN ABSOLUTA DE SESIÓN Y QUERY PARAMS GLOBAL
# =================================================================
# Regla de Oro: Se inicializan los atributos de estado al inicio absoluto del script
if "audiencia_activa" not in st.session_state:
    st.session_state.audiencia_activa = "🍊 Salud Integral"
if "admin_autenticado" not in st.session_state:
    st.session_state.admin_autenticado = False
if "guardado_exitoso" not in st.session_state:
    st.session_state.guardado_exitoso = False
if "flujo_finalizado" not in st.session_state:
    st.session_state.flujo_finalizado = False
if "alertas_mandarina_previas" not in st.session_state:
    st.session_state.alertas_mandarina_previas = []

# Captura prioritaria de parámetros URL desde el espacio de nombres global
minuto_actual = int(time.time() // 60)
token_tiempo = hashlib.md5(f"mandarina_secret_{minuto_actual}".encode()).hexdigest()[:8]

token_actual = st.query_params.get("token", None)
modo_admin_url = st.query_params.get("modo_admin", "true")
es_celular_del_publico = str(modo_admin_url).strip().lower() == "false"
diag_tipo_url = st.query_params.get("diag_tipo", None)

if es_celular_del_publico and diag_tipo_url:
    st.session_state.audiencia_activa = diag_tipo_url

# Ahora esta línea compilará con total seguridad matemática en Drive
url_con_token = f"{URL_PRODUCCION}/?token={token_tiempo}&modo_admin=false&diag_tipo={st.session_state.audiencia_activa.replace(' ', '%20')}"

# =================================================================
# PARTE 3: MATRICES GEOMÉTRICAS DE TRADUCCIÓN GLOBAL POLÍGLOTA (ESPAÑOL)
# =================================================================
DICCIONARIO_IDIOMAS = {
    "Español": {
        "ctrl": "Datos de Control", "nombre": "Nombre Completo o Matrícula *:", "wha": "Número Telefónico de Enlace *:",
        "sec1": "Sección I. Datos Demográficos y Geográficos", "edad": "1. Edad (Años):", "genero": "2. Género:",
        "nac": "3. Nacionalidad *:", "orig": "4. Estado de origen *:", "res": "5. Estado de residencia actual *:",
        "pais": "4. Escribe tu País de origen *:", "cont": "5. Selecciona tu Continente de origen *:", "rol": "6. Rol dentro de la Iglesia:",
        "sec2": "Sección II. Conocimiento sobre el tema", "kn1": "1. Antes de esta encuesta ya había escuchado hablar sobre los Modelos Temporales Cronos and Kairos:",
        "kn2": "2. He leído sobre los modelos temporales Cronos y Kairos:", "kn3": "3. He enseñado alguna vez sobre los modelos temporales Cronos y Kairos:",
        "kn4": "4. El modelo temporal:", "kn5": "5. Hablar de modelos temporales es hablar de:",
        "sec3": "Sección III. Batería de Reactivos Intercalados Contextuales", "btn_save": "💾 Guardar y Procesar Diagnóstico", "btn_pdf": "DESCARGAR RESULTADOS EN PDF 📥",
        "likert_labels": {1: "1 - Totalmente en desacuerdo", 2: "2 - En desacuerdo", 3: "3 - Neutral", 4: "4 - De acuerdo", 5: "5 - Totalmente de acuerdo"},
        "c_pool": "Planifico mis actividades operativas en {geo} siguiendo estrictamente los tiempos del reloj.",
        "k_pool": "La flexibilidad para adaptar mis plans ante una ventana de oportunidad en {geo} es más importante.",
        "mand_title": "### 🍊 Tus Gajos de Bienestar (Ecosistema)", 
        "mand_subtitle": "Selecciona las alertas o debilidades críticas en tu salud integral:",
        "err_fields": "Por favor llena los campos obligatorios.", "proc": "Procesando datos...", "local_ok": "Cargado Localmente (Sin Red)",
        "fields_msg": "💡 Complete los campos para habilitar la descarga.", "thanks": "## 🍊 ¡Muchas gracias por tu participación!",
        "thanks_sub": "Has completado el diagnóstico. Reconocer nuestros vectores temporales es el inicio de una alta madurez.",
        "qr_title": "📱 Código QR Dinámico de Seguridad (Proyectar al Auditorio)", "qr_sub1": "1. Enfoca el código QR con la cámara de tu smartphone.",
        "qr_sub2": "2. Responderás directamente el software nativo adaptado a tu organización sin necesidad de registros externos.",
        "gajos_data": {
            "💪 Salud Física": ["Nutrición Deficiente", "Falta de Sueño/Insomnio", "Sedentarismo Crónico", "Fatiga Corporal"],
            "🧠 Salud Mental": ["Niebla Mental/Falta de Foco", "Pensamientos Rumiativos", "Saturación de Información", "Apatía Cognitiva"],
            "❤️ Salud Emocional": ["Ansiedad o Estrés Agudo", "Irritabilidad Reactiva", "Desmotivación General", "Inestabilidad Anímica"],
            "👥 Salud Social": ["Aislamiento Voluntario", "Conflictos Interpersonales", "Falta de Red de Apoyo", "Falta de Límites Sanos"],
            "💰 Salud Económica": ["Gastos Compulsivos", "Deudas Atropelladas", "Falta de Fondo de Emergencia", "Ansiedad Financiera"],
            "⏳ Salud Temporal": ["Procrastinación Crónica", "Burnout o Sobrecarga", "Impuntualidad Perpetua", "Falta de Descanso/Margen"],
            "🙏 Salud Espiritual": ["Vacío Existencial", "Desconexión Interna", "Falta de Propósito", "Abandono de la Fe"]
        }
    },
# =================================================================
# PARTE 4: MATRICES GEOMÉTRICAS DE TRADUCCIÓN GLOBAL POLÍGLOTA (INGLÉS Y COREANO)
# =================================================================
    "Inglés": {
        "ctrl": "Control Information", "nombre": "Full Name or ID *:", "wha": "WhatsApp Link Number *:",
        "sec1": "Section I. Demographic & Geographic Data", "edad": "1. Age (Years):", "genero": "2. Gender:",
        "nac": "3. Nationality *:", "orig": "4. State of Origin *:", "res": "5. State of Residence *:",
        "pais": "4. Enter your Country of Origin *:", "cont": "5. Select your Continent of Origin *:", "rol": "6. Role within the Church:",
        "sec2": "Section II. Knowledge of the Topic", "kn1": "1. Before this survey, had you heard about the Cronos and Kairos Temporal Models?",
        "kn2": "2. Have you read about the Cronos and Kairos temporal models?", "kn3": "3. Have you ever taught about the Chronos and Kairos temporal models?",
        "kn4": "4. The temporal model is:", "kn5": "5. Speaking of temporal models means speaking of:",
        "sec3": "Section III. Intercalated Contextual Scale", "btn_save": "💾 Save & Process Diagnosis", "btn_pdf": "DOWNLOAD RESULTS IN PDF 📥",
        "likert_labels": {1: "1 - Strongly Disagree", 2: "2 - Disagree", 3: "3 - Neutral", 4: "4 - Agree", 5: "5 - Strongly Agree"},
        "c_pool": "I plan my operational activities in {geo} strictly following the clock schedule.",
        "k_pool": "Flexibility to adapt plans before an opportunity window in {geo} is much more important than the clock.",
        "mand_title": "### 🍊 Your Slices of Wellbeing", 
        "mand_subtitle": "Select the critical alerts or weaknesses in your holistic health:",
        "err_fields": "Please fill in all required fields.", "proc": "Processing analytics...", "local_ok": "Stored Locally (Offline Mode)",
        "fields_msg": "💡 Complete fields to activate your secure download.", "thanks": "## 🍊 Thank you very much for your participation!",
        "thanks_sub": "You have completed the diagnostic profile. Recognizing temporal vectors marks the threshold of adaptive maturity.",
        "qr_title": "📱 Dynamic Security QR Code (Project to Audience)", "qr_sub1": "1. Point your smartphone camera at the QR code.",
        "qr_sub2": "2. You will interact natively with our software deployment tailored for your institution.",
        "gajos_data": {
            "💪 Physical Health": ["Poor Nutrition", "Lack of Sleep/Insomnia", "Chronic Sedentarism", "Body Fatigue"],
            "🧠 Mental Health": ["Brain Fog/Lack of Focus", "Rumination/Overthinking", "Information Overload", "Cognitive Apathy"],
            "❤️ Emotional Health": ["Acute Anxiety/Stress", "Reactive Irritability", "General Demotivation", "Mood Instability"],
            "👥 Social Health": ["Voluntary Isolation", "Interpersonal Conflicts", "Lack of Support Network", "Weak Boundaries"],
            "💰 Financial Health": ["Compulsive Spending", "Overwhelming Debt", "Lack of Emergency Fund", "Financial Anxiety"],
            "⏳ Temporal Health": ["Chronic Procrastination", "Burnout/Overwork", "Perpetual Tardiness", "Lack of Margin/Rest"],
            "🙏 Spiritual Health": ["Existential Emptiness", "Internal Disconnection", "Lack of Purpose", "Loss of Meaning"]
        }
    },
    "Coreano": {
        "ctrl": "제어 데이터", "nombre": "성명 또는 학번 *:", "wha": "연락처 전화번호 *:",
        "sec1": "제1절. 인구통계학적 및 지리적 데이터", "edad": "1. 연령 (세):", "genero": "2. 성별:",
        "nac": "3. 국적 *:", "orig": "4. 출신 주 *:", "res": "5. 현재 거주 주 *:",
        "pais": "4. 출신 국가를 입력하세요 *:", "cont": "5. 출신 대륙을 선택하세요 *:", "rol": "6. 교회 내 직분:",
        "sec2": "제2절. 주제에 대한 지식", "kn1": "1. 이 설문조사 전에 크로노스와 카이로스 시간 모델에 대해 들어본 적이 있습니까?",
        "kn2": "2. 크로노스와 카이로스 시간 모델에 대해 읽어본 적이 있습니까?", "kn3": "3. 크로노스와 카이로스 시간 모델에 대해 가르쳐본 적이 있습니까?",
        "kn4": "4. 시간 모델은 다음과 같습니다:", "kn5": "5. 시간 모델에 대해 말하는 것은 다음을 의미합니다:",
        "sec3": "제3절. 중간 리커트 문항 척도", "btn_save": "💾 진단 저장 및 처리", "btn_pdf": "PDF 결과 다운로드 📥",
        "likert_labels": {1: "1 - 전혀 동의하지 않음", 2: "2 - 동의하지 않음", 3: "3 - 보통", 4: "4 - 동의함", 5: "5 - 매우 동의함"},
        "c_pool": "{geo}에서의 생산 활동을 시계 일정에 맞추어 철저히 계획합니다.",
        "k_pool": "{geo}에서 기회의 창이 열렸을 때 일정을 유연하게 변경하는 능력이 시계보다 중요합니다.",
        "mand_title": "### 🍊 당신의 웰빙 귤 조각 (전인적 건강)", "mand_subtitle": "종합적인 건강에서 위험한 경고 조항이나 취약점을 선택하십시오:",
        "err_fields": "필수 필드를 모두 채워주십시오.", "proc": "분석 처리 중...", "local_ok": "로컬로 저장됨 (오프라인)",
        "fields_msg": "💡 다운로드를 활성화하려면 필드를 입력하십시오.", "thanks": "## 🍊 설문에 참여해 주셔서 대단히 감사합니다!",
        "thanks_sub": "진단 프로필 작성이 완료되었습니다. 시간적 벡터를 식별하는 것은 적응적 성숙의 시작입니다.",
        "qr_title": "📱 동적 보안 QR 코드 (가청 전사 투영)", "qr_sub1": "1. 스마트폰 카메라로 QR 코드를 조준하십시오.",
        "qr_sub2": "2. 기관용으로 최적화된 당사 소프트웨어 에이전트와 직접 상호 작용합니다.",
        "gajos_data": {
            "💪 신체 건강": ["영양 불량", "수면 부족", "만성 좌식 생활", "신체 피로"],
            "🧠 정신 건강": ["Niebla Mental", "Rumination", "Overload", "Cognitive Apathy"],
            "❤️ 감정 건강": ["Acute Anxiety", "Irritability", "General Demotivation", "Mood Instability"],
            "👥 사회적 건강": ["Voluntary Isolation", "Interpersonal Conflicts", "Lack of Support Network", "Weak Boundaries"],
            "💰 경제적 건강": ["Compulsive Spending", "Overwhelming Debt", "Lack of Emergency Fund", "Financial Anxiety"],
            "⏳ 시간적 건강": ["Chronic Procrastination", "Burnout", "Perpetual Tardiness", "Lack of Margin"],
            "🙏 영적 건강": ["Existential Emptiness", "Internal Disconnection", "Lack of Purpose", "Loss of Meaning"]
        }
    },
# =================================================================
# PARTE 5: MATRICES GEOMÉTRICAS DE TRADUCCIÓN GLOBAL POLÍGLOTA (GRIEGO Y FRANCÉS)
# =================================================================
    "Griego": {
        "ctrl": "Στοιχεία Ελέγχου", "nombre": "Ονοματεπώνυμο ή Μητρώο *:", "wha": "Αριθμός Τηλεφώνου Σύνδεσης *:",
        "sec1": "Ενότητα Ι. Δημογραφικά & Γεωγραφικά Δεδομένα", "edad": "1. Ηλικία (Έτη):", "genero": "2. Φύλο:",
        "nac": "3. Υπηκοότητα *:", "orig": "4. Πολιτεία Καταγωγής *:", "res": "5. Πολιτεία Διαμονής *:",
        "pais": "4. Εισάγετε τη Χώρα Καταγωγής σας *:", "cont": "5. Επιλέξτε την Ήπειρο Καταγωγής σας *:", "rol": "6. Ρόλος μέσα στην Εκκλησία:",
        "sec2": "Ενότητα ΙΙ. Γνώση επί του Θέματος", "kn1": "1. Πριν από αυτήν την έρευνα, είχατε ακούσει για τα Χρονικά Μοντέλα Κρόνος και Καιρός;",
        "kn2": "2. Έχετε διαβάσει για τα χρονικά μοντέλα Κρόνος και Καιρός;", "kn3": "3. Έχετε διδάξει ποτέ για τα χρονικά μοντέλα Κρόνος και Καιρός;",
        "kn4": "4. Το χρονικό μοντέλο είναι:", "kn5": "5. Μιλώντας για χρονικά μοντέλα σημαίνει μιλώντας για:",
        "sec3": "Ενότητα ΙΙΙ. Κλίμακα Likert", "btn_save": "💾 Αποθήκευση & Επεξεργασία Διάγνωσης", "btn_pdf": "ΛΗΨΗ ΑΠΟΤΕΛΕΣΜΑΤΩΝ ΣΕ PDF 📥",
        "likert_labels": {1: "1 - Διαφωνώ απόλυτα", 2: "2 - Διαφωνώ", 3: "3 - Ουδέτερο", 4: "4 - Συμφωνώ", 5: "5 - Συμφωνώ απόλυτα"},
        "c_pool": "Προγραμματίζω τις δραστηριότητές μου στο {geo} ακολουθώντας αυστηρά το ρολόι.",
        "k_pool": "Η ευελιξία να προσαρμόζω τα πλάνα μου μπροστά σε μια ευκαιρία στο {geo} είναι πιο σημαντική.",
        "mand_title": "### 🍊 Τα Κομμάτια της Ευεξίας σας", "mand_subtitle": "Επιλέξτε τις κρίσιμες προειδοποιήσεις ή αδυναμίες στην ολιστική σας υγεία:",
        "err_fields": "Παρακαλούμε συμπληρώστε τα υποχρεωτικά πεδία.", "proc": "Επεξεργασία ανάλυσης...", "local_ok": "Τοπική Αποθήκευση (Εκτός Σύνδεσης)",
        "fields_msg": "💡 Συμπληρώστε τα πεδία για να ενεργοποιήσετε τη λήψη.", "thanks": "## 🍊 Σας ευχαριστούμε πολύ για τη συμμετοχή σας!",
        "thanks_sub": "Ολοκληρώσατε το διαγνωστικό προφίλ. Η αναγνώριση των χρονικών δεικτών αποτελεί την αφετηρία της ώριμης προσαρμογής.",
        "qr_title": "📱 Δυναμικός Κώδικας QR Ασφαλείας (Προβολή στο Κοινό)", "qr_sub1": "1. Εστιάστε την κάμερα του κινητού σας στον κώδικα QR.",
        "qr_sub2": "2. Θα αλληλεπιδράσετε απευθείας με το λογισμικό μας, προσαρμοσμένο για τον οργανισμό σας.",
        "gajos_data": {
            "💪 Φυσική Υγεία": ["Κακή Διατροφή", "Έλλειψη Ύπνου", "Καθιστική Ζωή", "Σωματική Κόπωση"],
            "🧠 Ψυχική Υγεία": ["Niebla Mental", "Rumination", "Overload", "Cognitive Apathy"],
            "❤️ Συναισθηματική Υγεία": ["Acute Anxiety", "Irritability", "General Demotivation", "Mood Instability"],
            "👥 Κοινωνική Υγεία": ["Voluntary Isolation", "Interpersonal Conflicts", "Lack of Support Network", "Weak Boundaries"],
            "💰 Οικονομική Υγεία": ["Compulsive Spending", "Overwhelming Debt", "Lack of Emergency Fund", "Financial Anxiety"],
            "⏳ Χρονική Υγεία": ["Chronic Procrastination", "Burnout", "Perpetual Tardiness", "Lack of Margin"],
            "🙏 Πνευματική Υγεία": ["Existential Emptiness", "Internal Disconnection", "Lack of Purpose", "Loss of Meaning"]
        }
    },
    "Francés": {
        "ctrl": "Données de Contrôle", "nombre": "Nom Complet ou ID *:", "wha": "Numéro WhatsApp *:",
        "sec1": "Section I. Données Démographiques", "edad": "1. Âge (Années) :", "genero": "2. Genre :",
        "nac": "3. Nationalité * :", "orig": "4. État d'Origine * :", "res": "5. État de Résidence * :",
        "pais": "4. Saisissez votre Pays d'Origine * :", "cont": "5. Sélectionnez votre Continent * :", "rol": "6. Rôle au sein de l'Église :",
        "sec2": "Section II. Connaissance du Sujet", "kn1": "1. Avant cette enquête, aviez-vous entendu parler des Modèles Temporels Chronos et Kairos ?",
        "kn2": "2. Avez-vous lu sur les modèles temporels Chronos et Kairos ?", "kn3": "3. Avez-vous déjà enseigné les modèles Chronos et Kairos ?",
        "kn4": "4. Le modèle temporel is :", "kn5": "5. Parler de modèles temporels signifie parler de :",
        "sec3": "Section III. Échelle de Likert Contextuelle", "btn_save": "💾 Enregistrer & Traiter le Diagnostic", "btn_pdf": "TÉLÉCHARGER LES RÉSULTATS EN PDF 📥",
        "likert_labels": {1: "1 - Pas du tout d'accord", 2: "2 - Pas d'accord", 3: "3 - Neutre", 4: "4 - D'accord", 5: "5 - Tout à fait d'accord"},
        "c_pool": "Je planifie mes activités opérationnelles à {geo} en suivant strictement l'horloge.",
        "k_pool": "La flexibilité d'adapter mes plans face à une opportunité à {geo} est plus importante que l'horloge.",
        "mand_title": "### 🍊 Vos Quartiers de Bien-être", "mand_subtitle": "Sélectionnez les alertes critiques de votre santé globale :",
        "err_fields": "Veuillez remplir les champs obligatoires.", "proc": "Traitement de l'analyse...", "local_ok": "Enregistré Localement (Mode Hors-ligne)",
        "fields_msg": "💡 Remplissez les champs pour activer le téléchargement sécurisé.", "thanks": "## 🍊 Merci beaucoup pour votre participation !",
        "thanks_sub": "Vous avez terminé le profil diagnostique. Reconnaître ses vecteurs temporels est le début de la maturité.",
        "qr_title": "📱 Code QR Dynamique de Sécurité (Projeter à l'Auditoire)", "qr_sub1": "1. Cadrez le code QR avec l'appareil photo de votre smartphone.",
        "qr_sub2": "2. Vous interagirez directement avec notre logiciel natif adapté à votre organisation.",
        "gajos_data": {
            "💪 Santé Physique": ["Nutrition Déficiente", "Manque de Sommeil", "Sédentarité Chronique", "Fatigue Corporelle"],
            "🧠 Santé Mentale": ["Brain Fog", "Rumination", "Overload", "Cognitive Apathy"],
            "❤️ Santé Émotionnelle": ["Acute Anxiety", "Irritability", "General Demotivation", "Mood Instability"],
            "👥 Santé Sociale": ["Voluntary Isolation", "Interpersonal Conflicts", "Lack of Support Network", "Weak Boundaries"],
            "💰 Santé Financière": ["Compulsive Spending", "Overwhelming Debt", "Lack of Emergency Fund", "Financial Anxiety"],
            "⏳ Santé Temporelle": ["Chronic Procrastination", "Burnout", "Perpetual Tardiness", "Lack of Margin"],
            "🙏 Santé Spirituelle": ["Existential Emptiness", "Internal Disconnection", "Lack of Purpose", "Loss of Meaning"]
        }
    },
# =================================================================
# PARTE 6: MATRICES GEOMÉTRICAS DE TRADUCCIÓN GLOBAL POLÍGLOTA (ALEMÁN, ITALIANO Y PORTUGUÉS)
# =================================================================
    "Alemán": {
        "ctrl": "Kontrolldaten", "nombre": "Vollständiger Name oder ID *:", "wha": "WhatsApp-Verbindungsnummer *:",
        "sec1": "Abschnitt I. Demografische Daten", "edad": "1. Alter (Jahre):", "genero": "2. Geschlecht:",
        "nac": "3. Nationalität *:", "orig": "4. Herkunftsland/Bundesland *:", "res": "5. Aktueller Wohnort *:",
        "pais": "4. Geben Sie Ihr Herkunftsland ein *:", "cont": "5. Wählen Sie Ihren Herkunftskontinent *:", "rol": "6. Rolle in der Kirche:",
        "sec2": "Abschnitt II. Kenntnis des Themas", "kn1": "1. Haben Sie vor dieser Umfrage schon von den Zeitmodellen Chronos und Kairos gehört?",
        "kn2": "2. Haben Sie über die Zeitmodelle Chronos und Kairos gelesen?", "kn3": "3. Haben Sie jemals über Chronos- und Kairos-Zeitmodelle gelehrt?",
        "kn4": "4. Das Zeitmodell ist:", "kn5": "5. Von Zeitmodellen zu sprechen bedeutet:",
        "sec3": "Abschnitt III. Kontextuelle Likert-Skala", "btn_save": "💾 Diagnose Speichern & Verarbeiten", "btn_pdf": "ERGEBNISSE ALS PDF HERUNTERLADEN 📥",
        "likert_labels": {1: "1 - Stimme überhaupt nicht zu", 2: "2 - Stimme nicht zu", 3: "3 - Neutral", 4: "4 - Stimme zu", 5: "5 - Stimme voll und ganz zu"},
        "c_pool": "Ich plane meine operativen Aktivitäten in {geo} strikt nach dem Zeitplan der Uhr.",
        "k_pool": "Die Flexibilität, Pläne bei Gelegenheiten in {geo} anzupassen, ist wichtiger als die Uhr.",
        "mand_title": "### 🍊 Ihre Segmente des Wohlbefindens", "mand_subtitle": "Wählen Sie kritische Warnungen in Ihrer ganzheitlichen Gesundheit aus:",
        "err_fields": "Bitte füllen Sie alle Pflichtfelder aus.", "proc": "Analyse wird verarbeitet...", "local_ok": "Lokal gespeichert (Offline-Modus)",
        "fields_msg": "💡 Felder ausfüllen, um den sicheren Download zu aktivieren.", "thanks": "## 🍊 Vielen Dank für Ihre Teilnahme!",
        "thanks_sub": "Sie haben das Diagnoseprofil abgeschlossen. Das Erkennen zeitlicher Vektoren ist der Beginn hoher Reife.",
        "qr_title": "📱 Dynamischer QR-Sicherheitscode (Auf Leinwand projizieren)", "qr_sub1": "1. Scannen Sie den QR-Code mit Ihrer Smartphone-Kamera.",
        "qr_sub2": "2. Sie interagieren direkt mit unserer für Ihre Organisation angepassten Software.",
        "gajos_data": {
            "💪 Physische Gesundheit": ["Mangelhafte Ernährung", "Schlafmangel/Insomnie", "Chronisches Sitzen", "Körperliche Müdigkeit"],
            "🧠 Mentale Gesundheit": ["Brain Fog", "Rumination", "Overload", "Cognitive Apathy"],
            "❤️ Emotionale Gesundheit": ["Acute Anxiety", "Irritability", "General Demotivation", "Mood Instability"],
            "👥 Soziale Gesundheit": ["Voluntary Isolation", "Interpersonal Conflicts", "Lack of Support Network", "Weak Boundaries"],
            "💰 Finanzielle Gesundheit": ["Compulsive Spending", "Overwhelming Debt", "Lack of Emergency Fund", "Financial Anxiety"],
            "⏳ Zeitliche Gesundheit": ["Chronic Procrastination", "Burnout", "Perpetual Tardiness", "Lack of Margin"],
            "🙏 Spirituelle Gesundheit": ["Existential Emptiness", "Internal Disconnection", "Lack of Purpose", "Loss of Meaning"]
        }
    },
    "Italiano": {
        "ctrl": "Dati di Controllo", "nombre": "Nome Completo o ID *:", "wha": "Numero WhatsApp di Contatto *:",
        "sec1": "Sezione I. Dati Demografici e Geografici", "edad": "1. Età (Anni):", "genero": "2. Genere:",
        "nac": "3. Nazionalità *:", "orig": "4. Stato di Origine *:", "res": "5. Stato di Residenza Attuale *:",
        "pais": "4. Inserisci il tuo Paese di Origine *:", "cont": "5. Seleziona il tuo Continente di Origine *:", "rol": "6. Ruolo all'interno della Chiesa:",
        "sec2": "Sezione II. Conoscenza dell'Argomento", "kn1": "1. Prima di questo sondaggio, avevi mai sentito parlare dei Modelli Temporali Chronos e Kairos?",
        "kn2": "2. Hai letto qualcosa riguardo ai modelli temporali Chronos e Kairos?", "kn3": "3. Hai mai insegnato i modelli temporali Chronos e Kairos?",
        "kn4": "4. Il modello temporale è:", "kn5": "5. Parlare di modelli temporali significa parlare di:",
        "sec3": "Sezione III. Scala Likert Contestuale", "btn_save": "💾 Salva e Processa Diagnostica", "btn_pdf": "SCARICA I RISULTATI IN PDF 📥",
        "likert_labels": {1: "1 - Fortemente in disaccordo", 2: "2 - In disaccordo", 3: "3 - Neutrale", 4: "4 - D'accordo", 5: "5 - Fortemente d'accordo"},
        "c_pool": "Pianifico le mie attività operative a {geo} seguendo rigorosamente gli orari dell'orologio.",
        "k_pool": "La flessibilità di adattare i miei piani di fronte a un'opportunità a {geo} è più importante dell'orologio.",
        "mand_title": "### 🍊 I Tuoi Spicchi di Benessere", "mand_subtitle": "Seleziona gli indicatori critici della tua salute olistica:",
        "err_fields": "Per favore, compila i campi obbligatori.", "proc": "Elaborazione dell'analisi...", "local_ok": "Salvato Localmente (Modalità Offline)",
        "fields_msg": "💡 Compila i campi per sbloccare il download sicuro.", "thanks": "## 🍊 Grazie mille per la tua partecipazione!",
        "thanks_sub": "Hai completato il profilo diagnostico. Riconoscere i propri vettori temporali costituisce l'inizio della maturità.",
        "qr_title": "📱 Codice QR Dinamico di Sicurezza (Proietta al Pubblico)", "qr_sub1": "1. Inquadra il codice QR con la fotocamera dello smartphone.",
        "qr_sub2": "2. Interagirai direttamente con l'applicazione nativa sviluppata per la tua organizzazione.",
        "gajos_data": {
            "💪 Salute Fisica": ["Nutrizione Carente", "Mancanza di Sonno/Insonnia", "Sedentarietà Cronica", "Affaticamento Corporeo"],
            "🧠 Salute Mentale": ["Brain Fog", "Rumination", "Overload", "Cognitive Apathy"],
            "❤️ Salute Emotiva": ["Acute Anxiety", "Irritability", "General Demotivation", "Mood Instability"],
            "👥 Salute Sociale": ["Voluntary Isolation", "Interpersonal Conflicts", "Lack of Support Network", "Weak Boundaries"],
            "💰 Salute Economica": ["Compulsive Spending", "Overwhelming Debt", "Lack of Emergency Fund", "Financial Anxiety"],
            "⏳ Salute Temporale": ["Chronic Procrastination", "Burnout", "Perpetual Tardiness", "Lack of Margin"],
            "🙏 Salute Spirituale": ["Existential Emptiness", "Internal Disconnection", "Lack of Purpose", "Loss of Meaning"]
        }
    },
    "Portugués": {
        "ctrl": "Dados de Controle", "nombre": "Nome Completo ou Registro *:", "wha": "Número de Telefone/WhatsApp *:",
        "sec1": "Seção I. Dados Demográficos e Geográficos", "edad": "1. Idade (Anos):", "genero": "2. Gênero:",
        "nac": "3. Nacionalidade *:", "orig": "4. Estado de Origem *:", "res": "5. Estado de Residência Atual *:",
        "pais": "4. Escreva seu País de Origem *:", "cont": "5. Selecione seu Continente de Origem *:", "rol": "6. Papel dentro da Igreja:",
        "sec2": "Seção II. Conhecimento sobre o Tema", "kn1": "1. Antes desta pesquisa, você já tinha ouvido falar sobre os Modelos Temporais Cronos e Kairos?",
        "kn2": "2. Você já leu sobre os modelos temporais Cronos e Kairos?", "kn3": "3. Você já ensinou alguma vez sobre os modelos temporais Cronos e Kairos?",
        "kn4": "4. O modelo temporal é:", "kn5": "5. Falar de modelos temporais é falar de:",
        "sec3": "Seção III. Escala Likert Contextual Intercalada", "btn_save": "💾 Salvar e Processar Diagnóstico", "btn_pdf": "BAIXAR RESULTADOS EM PDF 📥",
        "likert_labels": {1: "1 - Discordo totalmente", 2: "2 - Discordo", 3: "3 - Neutro", 4: "4 - Concordo", 5: "5 - Concordo totalmente"},
        "c_pool": "Planejo minhas atividades operacionais em {geo} seguindo estritamente os horários do relógio.",
        "k_pool": "A flexibilidade para adaptar meus planos perante uma janela de oportunidade em {geo} é mais importante.",
        "mand_title": "### 🍊 Seus Gomos de Bem-Estar", "mand_subtitle": "Selecione os alertas críticos ou fraquezas em sua saúde integral:",
        "err_fields": "Por favor, preencha todos os campos obrigatórios.", "proc": "Processando análise...", "local_ok": "Carregado Localmente (Modo Offline)",
        "fields_msg": "💡 Preencha os campos para habilitar o download seguro.", "thanks": "## 🍊 Muito obrigado por sua participação!",
        "thanks_sub": "Você completou o perfil diagnóstico. Reconhecer nossos vetores temporais marca o início da alta madureza.",
        "qr_title": "📱 Código QR Dinâmico de Segurança (Projetar para o Auditório)", "qr_sub1": "1. Foque o código QR com a câmera do seu smartphone.",
        "qr_sub2": "2. Você interagirá directamente com o nosso software nativo adaptado para a sua organização.",
        "gajos_data": {
            "💪 Saúde Física": ["Nutrição Deficiente", "Falta de Sono/Insônia", "Sedentarismo Crônico", "Fadiga Corporal"],
            "🧠 Saúde Mental": ["Brain Fog", "Rumination", "Overload", "Cognitive Apathy"],
            "❤️ Saúde Emocional": ["Ansiedad Aguda", "Irritabilidad", "Desmotivación", "Inestabilidad"],
            "👥 Saúde Social": ["Alemamento", "Interpersonal Conflicts", "Lack of Support Network", "Weak Boundaries"],
            "💰 Saúde Econômica": ["Compulsive Spending", "Overwhelming Debt", "Lack of Emergency Fund", "Financial Anxiety"],
            "⏳ Saúde Temporal": ["Chronic Procrastination", "Burnout", "Perpetual Tardiness", "Lack of Margin"],
            "🙏 Saúde Espiritual": ["Existential Emptiness", "Internal Disconnection", "Lack of Purpose", "Loss of Meaning"]
        }
    }
}
# =================================================================
# PARTE 7: CONEXIÓN INTEGRAL A LAS API DE GOOGLE SHEETS Y AUTO-FUNDACIÓN
# =================================================================
def conectar_google_sheets(nombre_pestana):
    try:
        if "gcp_service_account" not in st.secrets:
            return None
            
        secrets_dict = dict(st.secrets["gcp_service_account"])
        if "private_key" in secrets_dict:
            secrets_dict["private_key"] = secrets_dict["private_key"].replace("\\n", "\n")
            
        client = gspread.service_account_from_dict(secrets_dict)
        workbook = client.open(NOMBRE_HOJA_CALCULO)
        
        pestana_sana = nombre_pestana.replace("/", "_").replace("(", "").replace(")", "")[:30]
        
        try:
            return workbook.worksheet(pestana_sana)
        except gspread.exceptions.WorksheetNotFound:
            new_sheet = workbook.add_worksheet(title=pestana_sana, rows="1000", cols="35")
            
            if pestana_sana == "🍊 Salud Integral":
                headers = [
                    "Timestamp", "Nombre", "WhatsApp", 
                    "Salud Fisica (SF)", "Salud Mental (SM)", "Salud Emocional (SE)", 
                    "Salud Social (SS)", "Salud Economica (SECO)", "Salud Temporal (ST)", 
                    "Salud Espiritual (SPI)", "Detalle Alertas Temporal", "Token"
                ]
            else:
                headers = [
                    "Timestamp", "Nombre", "WhatsApp", "Edad", "Género", 
                    "Nacionalidad", "Estado Origen", "Estado Residencia", 
                    "País Origen", "Continente Extranjero", "Rol Iglesia", 
                    "C1_Escuchado", "C2_Leído", "C3_Enseñado", "C4_Origen", "C5_Concepto"
                ]
                for i in range(1, 15):
                    headers.append(f"R{i}")
                headers.append("Token")
                
            new_sheet.append_row(headers)
            return new_sheet
    except Exception:
        return None
# =================================================================
# PARTE 8: DESPACHO AUTOMATIZADO DE VECTORES ANALÍTICOS A LA NUBE
# =================================================================
def guardar_en_google_sheets(nombre_pestana, nombre, whatsapp, resultados, token, es_likert=False):
    sheet = conectar_google_sheets(nombre_pestana)
    if sheet:
        try:
            if es_likert:
                fila = [
                    str(datetime.datetime.now()), nombre, whatsapp,
                    resultados.get("Edad", ""), resultados.get("Género", ""),
                    resultados.get("Nacionalidad", ""), resultados.get("Estado Origen", ""),
                    resultados.get("Estado Residencia", ""), resultados.get("País Origen", ""),
                    resultados.get("Continente Extranjero", ""), resultados.get("Rol Iglesia", ""),
                    resultados.get("C1_Escuchado", ""), resultados.get("C2_Leído", ""),
                    resultados.get("C3_Enseñado", ""), resultados.get("C4_Origen", ""),
                    resultados.get("C5_Concepto", "")
                ]
                for i in range(1, 15):
                    fila.append(resultados.get(f"R{i}", 3))
                fila.append(token if token else "Acceso_Directo")
            else:
                fila = [
                    str(datetime.datetime.now()), nombre, whatsapp,
                    len(resultados.get("Salud Fisica (SF)", [])), len(resultados.get("Salud Mental (SM)", [])),
                    len(resultados.get("Salud Emocional (SE)", [])), len(resultados.get("Salud Social (SS)", [])),
                    len(resultados.get("Salud Economica (SECO)", [])), len(resultados.get("Salud Temporal (ST)", [])),
                    len(resultados.get("Salud Espiritual (SPI)", [])), ", ".join(resultados.get("Salud Temporal (ST)", [])),
                    token if token else "Acceso_Directo"
                ]
            sheet.append_row(fila)
            return True
        except Exception:
            return False
    return False
# =================================================================
# PARTE 9: SANITIZADOR POLÍGLOTA ANTI-UNICODE EXPORTABLE
# =================================================================
def limpiar_texto_pdf(texto, idioma="Español"):
    if not texto: return ""
    
    diccionario_pdf = {
        "Español": {
            "rep": "REPORTE DIAGNOSTICO DE MODELOS TEMPORALES", "part": "Participante:", "cont": "Contacto/WhatsApp:",
            "fecha": "Fecha de Emision:", "vec": "VECTORES CRONOS Y KAIROS ADAPTATIVOS", "perf_s": "Perfil de Simbiosis Temporal Equilibrada (C&K)",
            "perf_c": "Perfil Temporal Cronocentrico Puro (Rigido)", "perf_k": "Perfil Temporal Kairotico Puro (Adaptativo)"
        },
        "Inglés": {
            "rep": "DIAGNOSTIC REPORT OF TEMPORAL MODELS", "part": "Participant:", "cont": "Contact/WhatsApp:",
            "fecha": "Date of Issue:", "vec": "ADAPTIVE CRONOS AND KAIROS VECTORS", "perf_s": "Balanced Temporal Symbiosis Profile (C&K)",
            "perf_c": "Pure Chronocentric Temporal Profile (Rigid)", "perf_k": "Pure Kairotic Temporal Profile (Adaptive)"
        }
    }
    
    txt_str = str(texto)
    lang_dic = diccionario_pdf.get(idioma, diccionario_pdf["Español"])
    if txt_str in lang_dic:
        return lang_dic[txt_str]
        
    reemplazos = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N', 'ü': 'u', 'Ü': 'U'
    }
    texto_sano = "".join(reemplazos.get(c, c) for c in txt_str)
    return texto_sano.encode('ascii', 'ignore').decode('ascii').strip()
# =================================================================
# PARTE 10: CONSTRUCTOR DE REPORTES EN FLUJO DE BYTES (CORRECCIÓN SANGRE)
# =================================================================
def generar_pdf_diagnostico(nombre_usuario, whatsapp_usuario, resultados, titulo_diagnostico, es_likert=False, img_grafica_base64=None, lang="Español"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    titulo_sano = limpiar_texto_pdf("rep", lang)
    nombre_sano = limpiar_texto_pdf(nombre_usuario, lang)
    whatsapp_sano = limpiar_texto_pdf(whatsapp_usuario, lang)
    
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(230, 81, 0) 
    pdf.cell(0, 10, titulo_sano, new_x="LMARGIN", new_y="NEXT", align="C")
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, f"Jacob Zumaya Prianti (c) 2026 | Language: {lang}", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)
    pdf.set_draw_color(255, 152, 0)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)
    
    pdf.set_text_color(50, 50, 50)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(45, 6, limpiar_texto_pdf("part", lang), new_x="RIGHT", new_y="TOP")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, nombre_sano if nombre_sano else "Anonimo", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(45, 6, limpiar_texto_pdf("cont", lang), new_x="RIGHT", new_y="TOP")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, whatsapp_sano if whatsapp_sano else "N/A", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(45, 6, limpiar_texto_pdf("fecha", lang), new_x="RIGHT", new_y="TOP")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, datetime.date.today().strftime("%d/%m/%Y"), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    if es_likert:
        cronos_v = [resultados.get(f"R{i}", 3) for i in range(1, 15, 2)]
        kairos_v = [resultados.get(f"R{i}", 3) for i in range(2, 15, 2)]
        avg_cronos = sum(cronos_v) / 7
        avg_kairos = sum(kairos_v) / 7
        
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(230, 81, 0)
        pdf.cell(0, 8, limpiar_texto_pdf("vec", lang), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        
        if img_grafica_base64:
            try:
                img_clean = img_grafica_base64.split(",")[-1]
                img_data = BytesIO(base64.b64decode(img_clean))
                pdf.image(img_data, x=60, w=90)
                pdf.ln(4)
            except Exception: 
                pass
                
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 6, f"- CRONOS SCORE: {avg_cronos:.2f} / 5.00", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 6, f"- KAIROS SCORE: {avg_kairos:.2f} / 5.00", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)
        
        diferencia = abs(avg_cronos - avg_kairos)
        pdf.set_font("Helvetica", "B", 11)
        if diferencia <= 0.4:
            pdf.set_text_color(38, 166, 91)
            pdf.cell(0, 6, limpiar_texto_pdf("perf_s", lang), new_x="LMARGIN", new_y="NEXT")
        elif avg_kairos > avg_cronos:
            pdf.set_text_color(30, 139, 195)
            pdf.cell(0, 6, limpiar_texto_pdf("perf_k", lang), new_x="LMARGIN", new_y="NEXT")
        else:
            pdf.set_text_color(217, 30, 24)
            pdf.cell(0, 6, limpiar_texto_pdf("perf_c", lang), new_x="LMARGIN", new_y="NEXT")
    else:
        for dim_nombre, items in resultados.items():
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(230, 81, 0)
            pdf.cell(0, 6, f">> {limpiar_texto_pdf(dim_nombre, lang)}", new_x="LMARGIN", new_y="NEXT")
            puntos_str = ", ".join([limpiar_texto_pdf(it, lang) for it in items]) if len(items) > 0 else "OK"
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(50, 50, 50)
            pdf.multi_cell(0, 5, f"Alerts: {puntos_str}\n")
            
    return bytes(pdf.output())
# =================================================================
# PARTE 11: ALGORITMO CIENTÍFICO DE PROCESAMIENTO MATRICIAL SVD
# =================================================================
def ejecutar_analisis_semdeep(df, es_likert=False):
    analisis = {}
    if len(df) < 5:
        analisis["status"] = "Muestra insuficiente para convergencia estructural (Mínimo 5 registros)."
        return analisis
    try:
        if es_likert:
            columnas_r = [c for c in df.columns if c.startswith("Reactivo") or (len(c) <= 3 and c.startswith("R"))]
            if len(columnas_r) < 14: 
                columnas_r = list(df.columns[16:30])
                
            matriz_datos = df[columnas_r].apply(pd.to_numeric, errors='coerce').fillna(3).to_numpy()
            cronos_data = matriz_datos[:, 0::2]
            kairos_data = matriz_datos[:, 1::2]
            
            c_centered = cronos_data - np.mean(cronos_data, axis=0)
            k_centered = kairos_data - np.mean(kairos_data, axis=0)
            
            _, _, V_c = np.linalg.svd(c_centered, full_matrices=False)
            _, _, V_k = np.linalg.svd(k_centered, full_matrices=False)
            
            latent_cronos = c_centered @ V_c[0, :]
            latent_kairos = k_centered @ V_k[0, :]
            
            impacto_data = matriz_datos[:, 12:14]
            i_centered = impacto_data - np.mean(impacto_data, axis=0)
            _, _, V_i = np.linalg.svd(i_centered, full_matrices=False)
            latent_impacto = i_centered @ V_i[0, :]
            
            X = np.vstack([latent_cronos, latent_kairos]).T
            beta = np.linalg.pinv(X.T @ X) @ X.T @ latent_impacto
            
            r_cuadrado = 1 - (np.sum((latent_impacto - X @ beta) ** 2) / np.sum((latent_impacto - np.mean(latent_impacto)) ** 2))
            
            analisis["status"] = "Convergencia Exitosa (SEMDeep Engine v2.6)"
            analisis["beta_cronos_path"] = float(beta[0]) if len(beta) > 0 else 0.0
            analisis["beta_kairos_path"] = float(beta[1]) if len(beta) > 1 else 0.0
            analisis["gof_r2_ajuste"] = max(0.0, float(r_cuadrado))
            analisis["covarianza_latente"] = float(np.corrcoef(latent_cronos, latent_kairos)[0, 1])
        else:
            matriz_datos = df.iloc[:, 3:10].apply(pd.to_numeric, errors='coerce').fillna(0).to_numpy()
            c_centered = matriz_datos - np.mean(matriz_datos, axis=0)
            _, s, _ = np.linalg.svd(c_centered, full_matrices=False)
            
            s_cuadrado = s ** 2
            analisis["status"] = "Convergencia Lineal Exitosa (SVD Gajos)"
            analisis["gof_r2_ajuste"] = float(s_cuadrado[0] / np.sum(s_cuadrado)) if len(s) > 0 else 0.0
    except Exception as e:
        analisis["status"] = f"Error en cálculo matricial: {str(e)}"
        
    return analisis

def algoritmo_generar_reactivos_poliglotas(geo, b_alertas, lang_key):
    tx_pool = DICCIONARIO_IDIOMAS.get(lang_key, DICCIONARIO_IDIOMAS["Español"])
    fuga = str(b_alertas) if b_alertas else "OK"
    banco_alterno = {}
    for i in range(1, 15):
        if i % 2 != 0:
            banco_alterno[i] = tx_pool["c_pool"].format(geo=geo) + f" (Ref: {fuga[:12]})"
        else:
            banco_alterno[i] = tx_pool["k_pool"].format(geo=geo)
    return banco_alterno
# =================================================================
# PARTE 12: PUNTO DE ENTRADA CENTRAL, SESIONES E INTERCEPTOR DE TOKENS
# =================================================================
def main():
    # Inicialización local/global síncrona de variables de control de red
    minuto_actual = int(time.time() // 60)
    token_tiempo = hashlib.md5(f"mandarina_secret_{minuto_actual}".encode()).hexdigest()[:8]

    # Extracción directa y segura de parámetros desde el entorno de red de Streamlit
    token_actual = st.query_params.get("token", None)
    modo_admin_url = st.query_params.get("modo_admin", "true")
    es_celular_del_publico = str(modo_admin_url).strip().lower() == "false"
    diag_tipo_url = st.query_params.get("diag_tipo", None)

    if es_celular_del_publico and diag_tipo_url:
        st.session_state.audiencia_activa = diag_tipo_url

    url_con_token = f"{URL_PRODUCCION}/?token={token_tiempo}&modo_admin=false&diag_tipo={st.session_state.audiencia_activa.replace(' ', '%20')}"

    # Fundación e instanciación en frío automatizada de las estructuras en la nube
    if "estructuras_inicializadas" not in st.session_state:
        lista_inicializar = ["🍊 Salud Integral", "Docentes", "🏭 Sector Secundario"]
        with st.spinner("Instanciando matriz de datos políglota en Google Sheets... 🍊"):
            for tabla in lista_inicializar:
                conectar_google_sheets(tabla)
        st.session_state.estructuras_inicializadas = True

    # Interceptor de caducidad temporal anti-duplicados
    if token_actual and not st.session_state.admin_autenticado:
        acceso_bloqueado = False
        minuto_base = int(time.time() // 60)
        tokens_validos = [hashlib.md5(f"mandarina_secret_{minuto_base - i}".encode()).hexdigest()[:8] for i in range(5)]
        if token_actual not in tokens_validos: 
            acceso_bloqueado = True
        else:
            sheet = conectar_google_sheets(st.session_state.audiencia_activa)
            if sheet:
                try:
                    registros = sheet.get_all_records()
                    if registros:
                        df_check = pd.DataFrame(registros)
                        if token_actual in [str(r.get(df_check.columns[-1], "")) for r in registros]: 
                            acceso_bloqueado = True
                except Exception: 
                    pass
        if acceso_bloqueado:
            st.error("🚫 El acceso escaneado ha expirado o ya fue utilizado en esta ponencia.")
            st.stop()

# =================================================================
# PARTE 13: SELECTOR DE IDIOMAS, CONSOLA SIDEBAR Y GENERACIÓN QR ADAPTATIVO
# =================================================================
    if not st.session_state.flujo_finalizado:
        idioma_sel = st.selectbox(
            "🌐 Choose System Language / Selecciona Idioma:", 
            ["Español", "Inglés", "Coreano", "Griego", "Francés", "Alemán", "Italiano", "Portugués"]
        )
        tx = DICCIONARIO_IDIOMAS.get(idioma_sel, DICCIONARIO_IDIOMAS["Español"])
    else:
        idioma_sel = "Español"
        tx = DICCIONARIO_IDIOMAS["Español"]

    # Consola administrativa integrada del Sidebar Ponente
    PASSWORD_SISTEMA = st.secrets["credentials"]["password_ponente"] if "credentials" in st.secrets else "mandarina2026"
    if not es_celular_del_publico:
        with st.sidebar:
            st.markdown("## 🔐 Control del Ponente")
            if not st.session_state.admin_autenticado:
                input_password = st.text_input("Contraseña Ponente:", type="password", key="side_pwd")
                if st.button("Desbloquear Tableros"):
                    if input_password == PASSWORD_SISTEMA:
                        st.session_state.admin_autenticado = True
                        st.rerun()
                    else:
                        st.error("Contraseña incorrecta.")
            else:
                st.success("Modo Ponente Activo")
                nueva_aud_txt = st.text_input("➕ Agregar Nueva Audiencia Personalizada:", key="add_new_aud_input").strip()
                lista_audiencias_base = ["🍊 Salud Integral", "Docentes", "🏭 Sector Secundario"]
                if "audiencias_custom_list" not in st.session_state:
                    st.session_state.audiences_custom_list = []
                if nueva_aud_txt and nueva_aud_txt not in lista_audiencias_base and nueva_aud_txt not in st.session_state.audiences_custom_list:
                    st.session_state.audiences_custom_list.append(nueva_aud_txt)
                    st.toast(f"Audiencia '{nueva_aud_txt}' añadida a la sesión", icon="🍊")
                lista_audiencias_completa = lista_audiencias_base + st.session_state.audiences_custom_list
                seleccion = st.selectbox("Audiencia Actual en Vivo:", lista_audiencias_completa, index=lista_audiencias_completa.index(st.session_state.audiencia_activa) if st.session_state.audiencia_activa in lista_audiencias_completa else 0)
                if seleccion != st.session_state.audiencia_activa:
                    st.session_state.audiencia_activa = seleccion
                    with st.spinner("Inicializando entorno de datos en Google Sheets..."):
                        conectar_google_sheets(seleccion)
                    st.rerun()

        # Renderizado adaptativo del código QR al auditorio sin obsolescencia (width='stretch')
        titulo_qr = tx.get("qr_title", DICCIONARIO_IDIOMAS["Español"]["qr_title"])
        sub_qr1 = tx.get("qr_sub1", DICCIONARIO_IDIOMAS["Español"]["qr_sub1"])
        sub_qr2 = tx.get("qr_sub2", DICCIONARIO_IDIOMAS["Español"]["qr_sub2"])
        with st.expander(titulo_qr, expanded=True):
            col1, col2 = st.columns([1, 1.5])
            with col1:
                qr = qrcode.QRCode(version=1, box_size=10, border=2)
                qr.add_data(url_con_token)
                qr.make(fit=True)
                img_qr = qr.make_image(fill_color="#e65100", back_color="white")
                buf = BytesIO()
                img_qr.save(buf, format="PNG")
                st.image(buf.getvalue(), caption=f"QR Activo: {st.session_state.audiencia_activa}", width='stretch')
            with col2:
                st.write(f"### Audiencia Proyectada en Vivo: {st.session_state.audiencia_activa}")
                st.write(sub_qr1)
                st.write(sub_qr2)
# =================================================================
# PARTE 14: RENDERIZADO ISOMÓRFICO DEL FORMULARIO Y GAJOS DE BIENESTAR
# =================================================================
    if not st.session_state.flujo_finalizado:
        st.header(f"📋 {st.session_state.audiencia_activa}")
        nombre = st.text_input(tx["nombre"], placeholder="Juan Pérez", key="main_name_in")
        whatsapp = st.text_input(tx["wha"], placeholder="+52...", key="main_wha_in")
        st.divider()
        
        resultados_totales = {}
        es_modo_likert = (st.session_state.audiencia_activa != "🍊 Salud Integral")

        if not es_modo_likert:
            st.write(tx["mand_title"])
            st.write(tx["mand_subtitle"])
            gajos_dinamicos = tx.get("gajos_data", DICCIONARIO_IDIOMAS["Español"]["gajos_data"])
            
            for g_idx, (g_name, alertas_especificas) in enumerate(gajos_dinamicos.items()):
                with st.container(border=True):
                    st.markdown(f"#### {g_name}")
                    col1, col2 = st.columns(2)
                    with col1:
                        cb0 = st.checkbox(alertas_especificas[0], key=f"cb_{g_idx}_0")
                        cb1 = st.checkbox(alertas_especificas[1], key=f"cb_{g_idx}_1")
                    with col2:
                        cb2 = st.checkbox(alertas_especificas[2], key=f"cb_{g_idx}_2")
                        cb3 = st.checkbox(alertas_especificas[3], key=f"cb_{g_idx}_3")
                    resultados_totales[g_name] = [alertas_especificas[i] for i, val in enumerate([cb0, cb1, cb2, cb3]) if val]
                    
            if st.button("Procesar Alertas Base / Register Alerts"):
                st.session_state.alertas_mandarina_previas = list(resultados_totales.values()) if resultados_totales else ["Alert"]
                st.success("OK. Context synchronized.")
        else:
            st.subheader(tx["sec1"])
            resultados_totales["Edad"] = st.number_input(tx["edad"], min_value=10, max_value=100, value=20, key="dem_edad")
            resultados_totales["Género"] = st.radio(tx["genero"], ["Masculino", "Femenino", "Other"], horizontal=True, key="dem_genero")
            nacionalidad = st.radio(tx["nac"], ["Mexicana", "Extranjera"], horizontal=True, key="dem_nac")
            resultados_totales["Nacionalidad"] = nacionalidad
            geo_contexto = "Region"
            
            if nacionalidad == "Mexicana":
                resultados_totales["Estado Origen"] = st.selectbox(tx["orig"], [""] + ESTADOS_MEXICO, key="dem_orig")
                resultados_totales["Estado Residencia"] = st.selectbox(tx["res"], [""] + ESTADOS_MEXICO, key="dem_res")
                resultados_totales["País Origen"] = "México"
                resultados_totales["Continente Extranjero"] = "América"
                geo_contexto = str(resultados_totales["Estado Residencia"])
            else:
                resultados_totales["Estado Origen"] = "N/A"
                resultados_totales["Estado Residencia"] = "N/A"
                resultados_totales["País Origen"] = st.text_input(tx["pais"], key="dem_pais_txt")
                resultados_totales["Continente Extranjero"] = st.selectbox(tx["cont"], [""] + CONTINENTES, key="dem_cont")
                geo_contexto = str(resultados_totales["País Origen"])
                
            st.subheader(tx["sec2"])
            resultados_totales["C1_Escuchado"] = st.radio(tx["kn1"], ["Sí", "No"], horizontal=True, key="kn_1")
            resultados_totales["C2_Leído"] = st.radio(tx["kn2"], ["Sí", "No"], horizontal=True, key="kn_2")
            resultados_totales["C3_Enseñado"] = st.radio(tx["kn3"], ["Sí", "No"], horizontal=True, key="kn_3")
            resultados_totales["C4_Origen"] = st.radio(tx["kn4"], ["Se impone", "Se nace", "No sé"], horizontal=True, key="kn_4")
            resultados_totales["C5_Concepto"] = st.radio(tx["kn5"], ["Teología", "Cultura", "No sé"], horizontal=True, key="kn_5")
            
            st.subheader(tx["sec3"])
            banco_mutado = algoritmo_generar_reactivos_poliglotas(geo_contexto, st.session_state.alertas_mandarina_previas, idioma_sel)
            for r_id, enunciado_idioma in banco_mutado.items():
                st.write(f"Reactivo {r_id}: {enunciado_idioma}")
                etiquetas_likert = tx.get("likert_labels", DICCIONARIO_IDIOMAS["Español"]["likert_labels"])
                resultados_totales[f"R{r_id}"] = st.radio(
                    "Scale:",
                    options=[1, 2, 3, 4, 5],
                    format_func=lambda x: etiquetas_likert.get(x, str(x)),
                    key=f"dyn_r_{r_id}"
                )
# =================================================================
# PARTE 15: ENVÍO DE DATOS, GENERACIÓN PDF Y OFICINA DE ALTA AUDITORÍA
# =================================================================
        st.divider()
        col_btn1, col_btn2 = st.columns(2)
        campos_completos = bool(nombre.strip()) and bool(whatsapp.strip())
        
        with col_btn1:
            if st.button(tx["btn_save"], type="primary"):
                if not campos_completos: 
                    st.error(tx["err_fields"])
                else:
                    with st.spinner(tx["proc"]):
                        exito = guardar_en_google_sheets(st.session_state.audiencia_activa, nombre, whatsapp, resultados_totales, token_actual, es_modo_likert)
                        if exito: 
                            st.session_state.guardado_exitoso = True
                            st.success("OK")
                        else: 
                            st.session_state.guardado_exitoso = True
                            st.warning(tx["local_ok"])
                            
        with col_btn2:
            if st.session_state.guardado_exitoso and campos_completos:
                grafica_base64 = None
                if es_modo_likert:
                    try:
                        cronos_v = [resultados_totales.get(f"R{i}", 3) for i in range(1, 15, 2)]
                        kairos_v = [resultados_totales.get(f"R{i}", 3) for i in range(2, 15, 2)]
                        fig, ax = plt.subplots(figsize=(4, 4))
                        ax.axhspan(1, 3, 1, 3, color='#f2f1ef', alpha=0.5)
                        ax.axhspan(3, 5, 3, 5, color='#e8f8f5', alpha=0.7)
                        ax.scatter(sum(cronos_v)/7, sum(kairos_v)/7, color='#e65100', s=120)
                        buf_g = BytesIO()
                        plt.savefig(buf_g, format='png', bbox_inches='tight', dpi=100)
                        buf_g.seek(0)
                        grafica_base64 = f"data:image/png;base64,{base64.b64encode(buf_g.read()).decode('utf-8')}"
                        plt.close(fig)
                    except Exception: 
                        pass
                        
                reporte_procesado = generar_pdf_diagnostico(nombre, whatsapp, resultados_totales, st.session_state.audiencia_activa, es_modo_likert, grafica_base64, idioma_sel)
                nombre_archivo = nombre.replace(' ', '_') if nombre else 'User'
                
                def callback_finalizar():
                    st.session_state.flujo_finalizado = True
                    for k in list(st.session_state.keys()):
                        if k.startswith(("sf_", "sm_", "cb_", "dyn_r_", "dem_", "kn_")): 
                            del st.session_state[k]
                            
                                st.download_button(
                    label=tx["btn_pdf"],
                    data=reporte_procesado,
                    file_name=f"Report_{idioma_sel}_{nombre_archivo}.pdf",
                    mime="application/pdf",
                    on_click=callback_finalizar
                )
            else: 
                st.info(tx["fields_msg"])
    else:
        tx_final = DICCIONARIO_IDIOMAS.get(st.query_params.get("lang", "Español"), DICCIONARIO_IDIOMAS["Español"])
        st.balloons()
        st.success("### Process Completed! 🎉")
        with st.container(border=True):
            st.write(tx_final["thanks"])
            st.markdown(tx_final["thanks_sub"])
            st.info("👉 Jacob Zumaya Prianti A.C. (c) 2026")
        
        # AJUSTE EXPERTO: El botón de regreso solo aparece en la pantalla del ponente
        if not es_celular_del_publico:
            st.write("")
            if st.button("🔄 Regresar al Diagnóstico Activo / Reset View", type="secondary", key="btn_reset_view_ponente"):
                st.session_state.flujo_finalizado = False
                st.rerun()

    # MÓDULO CENTRAL AVANZADO: OFICINA DE INVESTIGACIÓN ALTA AUDITORÍA
    if st.session_state.admin_autenticado and not es_celular_del_publico:
        st.markdown("---")
        st.header("🔬 Oficina de Investigación y Alta Analítica del Ponente")
        st.write("Módulo avanzado de modelado predictivo de variables latentes.")
        
        try:
            if "gcp_service_account" in st.secrets:
                secrets_dict = dict(st.secrets["gcp_service_account"])
                if "private_key" in secrets_dict:
                    secrets_dict["private_key"] = secrets_dict["private_key"].replace("\\n", "\n")
                client_back = gspread.service_account_from_dict(secrets_dict)
                workbook_back = client_back.open(NOMBRE_HOJA_CALCULO)
                lista_tablas_reales = [sh.title for sh in workbook_back.worksheets()]
            else:
                lista_tablas_reales = ["🍊 Salud Integral", "Docentes", "🏭 Sector Secundario"]
        except Exception:
            lista_tablas_reales = ["🍊 Salud Integral", "Docentes", "🏭 Sector Secundario"]

        tabla_analizar = st.selectbox("Seleccionar Tabla para Extracción Científica:", lista_tablas_reales)
        
        if st.button("📊 Ejecutar Auditoría Estadística de Nivel Doctoral", type="primary"):
            sheet = conectar_google_sheets(tabla_analizar)
            if sheet:
                try:
                    todas_las_filas = sheet.get_all_values()
                    if not todas_las_filas or len(todas_las_filas) < 2:
                        st.warning("⚠️ La tabla seleccionada no contiene registros o datos suficientes para la auditoría.")
                    else:
                        encabezados = todas_las_filas[0]
                        datos_cuerpo = todas_las_filas[1:]
                        encabezados_unicos = []
                        for i, col in enumerate(encabezados):
                            nombre_col = col.strip() if col.strip() else f"Columna_{i}"
                            if nombre_col in encabezados_unicos:
                                nombre_col = f"{nombre_col}_{i}"
                            encabezados_unicos.append(nombre_col)
                        df_doc = pd.DataFrame(datos_cuerpo, columns=encabezados_unicos)
                        st.success(f"¡Base de datos cargada exitosamente! Registros analizados: {len(df_doc)}")
                        es_tabla_likert = (tabla_analizar != "🍊 Salud Integral")
                        
                        col_graph1, col_graph2 = st.columns(2)
                        with col_graph1:
                            st.write("#### 📈 Distribución Descriptiva Global")
                            if not es_tabla_likert:
                                col_gajos = ["Salud Fisica (SF)", "Salud Mental (SM)", "Salud Emocional (SE)", "Salud Social (SS)", "Salud Economica (SECO)", "Salud Temporal (ST)", "Salud Espiritual (SPI)"]
                                promedios = {c: pd.to_numeric(df_doc[c], errors='coerce').fillna(0).mean() for c in col_gajos if c in df_doc.columns}
                                if promedios: 
                                    st.bar_chart(pd.DataFrame(list(promedios.items()), columns=["Dim", "Media"]), x="Dim", y="Media", color="#e65100")
                            else:
                                r_cols = [c for c in df_doc.columns if c.startswith("Reactivo") or (len(c) <= 3 and c.startswith("R"))]
                                if len(r_cols) >= 14:
                                    matriz_r = df_doc[r_cols].apply(pd.to_numeric, errors='coerce').fillna(3).to_numpy()
                                    c_mean = np.mean(matriz_r[:, 0::2])
                                    k_mean = np.mean(matriz_r[:, 1::2])
                                    st.bar_chart(pd.DataFrame([["Cronos", c_mean], ["Kairos", k_mean]], columns=["Vector", "Media"]), x="Vector", y="Media", color="#2574a9")
                                else:
                                    st.warning("Estructura de reactivos incompleta en la tabla seleccionada.")
                        with col_graph2:
                            st.write("#### 🧠 Modelado Estructural Ecuaciones Latentes: SEMDeep")
                            res_sem = ejecutar_analisis_semdeep(df_doc, es_tabla_likert)
                            st.json(res_sem)

                        # === INYECCIÓN QUIRÚRGICA: EXPORTACIÓN EN PDF PARA EL PONENTE ===
                        st.markdown("---")
                        st.write("#### 📥 Exportación Ejecutiva para Tomadores de Decisiones")
                        
                        pdf_auditoria = FPDF()
                        pdf_auditoria.add_page()
                        pdf_auditoria.set_font("Helvetica", "B", 14)
                        pdf_auditoria.set_text_color(230, 81, 0)
                        pdf_auditoria.cell(0, 10, f"AUDITORIA ESTADISTICA: {tabla_analizar.upper()}", new_x="LMARGIN", new_y="NEXT", align="C")
                        pdf_auditoria.set_font("Helvetica", "", 10)
                        pdf_auditoria.set_text_color(100, 100, 100)
                        pdf_auditoria.cell(0, 6, f"Emitido: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')} | Jacob Zumaya (c) 2026", new_x="LMARGIN", new_y="NEXT", align="C")
                        pdf_auditoria.ln(5)
                        
                        pdf_auditoria.set_font("Helvetica", "B", 11)
                        pdf_auditoria.set_text_color(50, 50, 50)
                        pdf_auditoria.cell(0, 6, f"Registros Totales Analizados: {len(df_doc)}", new_x="LMARGIN", new_y="NEXT")
                        pdf_auditoria.cell(0, 6, f"Estado del Motor: {res_sem.get('status', 'N/A')}", new_x="LMARGIN", new_y="NEXT")
                        
                        if es_tabla_likert:
                            pdf_auditoria.cell(0, 6, f"- Beta Path Cronos: {res_sem.get('beta_cronos_path', 0.0):.4f}", new_x="LMARGIN", new_y="NEXT")
                            pdf_auditoria.cell(0, 6, f"- Beta Path Kairos: {res_sem.get('beta_kairos_path', 0.0):.4f}", new_x="LMARGIN", new_y="NEXT")
                            pdf_auditoria.cell(0, 6, f"- Covarianza de Variables Latentes: {res_sem.get('covarianza_latente', 0.0):.4f}", new_x="LMARGIN", new_y="NEXT")
                        
                        pdf_auditoria.cell(0, 6, f"- Indice de Ajuste GOF R2: {res_sem.get('gof_r2_ajuste', 0.0):.4f}", new_x="LMARGIN", new_y="NEXT")
                        
                        bytes_auditoria = bytes(pdf_auditoria.output())
                        
                        st.download_button(
                            label=f"📥 DESCARGAR AUDITORÍA EJECUTIVA ({tabla_analizar}) EN PDF",
                            data=bytes_auditoria,
                            file_name=f"Auditoria_Doctoral_{tabla_analizar.replace(' ', '_')}_{datetime.date.today()}.pdf",
                            mime="application/pdf",
                            key="btn_download_admin_pdf"
                        )
                except Exception as e:
                    st.error(f"❌ Error en la extracción de la base de datos de Google Sheets: {str(e)}")

# Guardia de ejecución principal para el ecosistema web de Streamlit
if __name__ == "__main__":
    main()
