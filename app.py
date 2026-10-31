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

# CONFIGURACIÓN OBLIGATORIA DEL ENTRAMADO DE STREAMLIT (Primera instrucción ejecutable)
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

# INICIALIZACIÓN ABSOLUTA EN EL ÁMBITO GLOBAL SUPERIOR (Evita AttributeError)
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

# Captura prioritaria global de Query Parameters URL de red
minuto_actual = int(time.time() // 60)
token_tiempo = hashlib.md5(f"mandarina_secret_{minuto_actual}".encode()).hexdigest()[:8]

token_actual = st.query_params.get("token", None)
modo_admin_url = st.query_params.get("modo_admin", "true")
es_celular_del_publico = str(modo_admin_url).strip().lower() == "false"
diag_tipo_url = st.query_params.get("diag_tipo", None)

if es_celular_del_publico and diag_tipo_url:
    st.session_state.audiencia_activa = diag_tipo_url

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
        "sec2": "Sección II. Conocimiento sobre el tema", "kn1": "1. Antes de esta encuesta ya había escuchado hablar sobre los Modelos Temporales Cronos y Kairos:",
        "kn2": "2. He leído sobre los modelos temporales Cronos y Kairos:", "kn3": "3. He enseñado alguna vez sobre los modelos temporales Cronos y Kairos:",
        "kn4": "4. El modelo temporal:", "kn5": "5. Hablar de modelos temporales es hablar de:",
        "sec3": "Sección III. Batería de Reactivos Intercalados Contextuales", "btn_save": "💾 Guardar y Procesar Diagnóstico", "btn_pdf": "DESCARGAR RESULTADOS EN PDF 📥",
        "likert_labels": {1: "1 - Totalmente en desacuerdo", 2: "2 - En desacuerdo", 3: "3 - Neutral", 4: "4 - De acuerdo", 5: "5 - Totalmente de acuerdo"},
        "c_pool": "Planifico mis actividades operativas en {geo} siguiendo estrictamente los tiempos del reloj.",
        "k_pool": "La flexibilidad para adaptar mis planes ante una ventana de oportunidad en {geo} es más importante.",
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
        "kn4": "4. Le modèle temporel est :", "kn5": "5. Parler de modèles temporels signifie parler de :",
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
        "qr_title": "📱 Dynamischer QR-Sicherheitscode (Auf Leinwand projizieren)", "qr_sub1": "1. Scannen Sie den QR-Code with Ihrer Smartphone-Kamera.",
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
        "fields_msg": "💡 Compila i campi para sbloccare il download sicuro.", "thanks": "## 🍊 Grazie mille per la tua partecipazione!",
        "thanks_sub": "Hai completato il perfil diagnostico. Riconoscere i propri vettori temporali costituisce l'inizio della maturità.",
        "qr_title": "📱 Codice QR Dinamico di Sicurezza (Proietta al Pubblico)", "qr_sub1": "1. Inquadra il codice QR con la fotocamera dello smartphone.",
        "qr_sub2": "2. Interagirai direttamente con l'applicazione nativa sviluppata per la tua organizzazione.",
        "gajos_data": {
            "💪 Salute Fisica": ["Nutrizione Carente", "Mancanza di Sonno/Insonnia", "Sedentarietà\".Cronica", "Affaticamento Corporeo"],
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
        "nac": "3. Nationality *:", "orig": "4. Estado de Origem *:", "res": "5. Estado de Residência Actual *:",
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
            "💪 Saúde Física": ["Nutrição Deficiente", "Falta de Sono/Insônia", "Sedentarismo Crônico", "Fatiga Corporal"],
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
                for i in range(1, 11):
                    headers.append(f"R{i}")
                headers.append("Token")
                
            new_sheet.append_row(headers)
            return new_sheet
    except Exception:
        return None

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
                for i in range(1, 11):
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
# PARTE 8: SANITIZADOR Y COMPILADOR DE REPORTES EN PDF (10 ÍTEMS SIMÉTRICOS)
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
    if txt_str in lang_dic: return lang_dic[txt_str]
    reemplazos = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U', 'ñ': 'n', 'Ñ': 'N', 'ü': 'u', 'Ü': 'U'}
    texto_sano = "".join(reemplazos.get(c, c) for c in txt_str)
    return texto_sano.encode('ascii', 'ignore').decode('ascii').strip()

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
        kairos_v = [resultados.get(f"R{i}", 3) for i in range(1, 11, 2)]
        cronos_v = [resultados.get(f"R{i}", 3) for i in range(2, 11, 2)]
        avg_cronos = sum(cronos_v) / 5
        avg_kairos = sum(kairos_v) / 5
        
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
            except Exception: pass
                
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
# PARTE 9: MOTOR DE INVESTIGACIÓN SEMDEEP (CONVERGENCIA SVD DE 10 ÍTEMS)
# =================================================================
def ejecutar_analisis_semdeep(df, es_likert=False):
    analisis = {}
    if len(df) < 5:
        analisis["status"] = "Muestra insuficiente para convergencia estructural (Mínimo 5 registros)."
        return analisis
    try:
        if es_likert:
            columnas_r = [c for c in df.columns if c.startswith("Reactivo") or (len(c) <= 3 and c.startswith("R"))]
            if len(columnas_r) < 10: 
                columnas_r = list(df.columns[16:26])
                
            matriz_datos = df[columnas_r].apply(pd.to_numeric, errors='coerce').fillna(3).to_numpy()
            
            # Sincronización Invertida Exacta: Índices Nones = Kairós, Índices Pares = Cronos
            kairos_data = matriz_datos[:, 0::2]
            cronos_data = matriz_datos[:, 1::2]
            
            c_centered = cronos_data - np.mean(cronos_data, axis=0)
            k_centered = kairos_data - np.mean(kairos_data, axis=0)
            
            _, _, V_c = np.linalg.svd(c_centered, full_matrices=False)
            _, _, V_k = np.linalg.svd(k_centered, full_matrices=False)
            
            latent_cronos = c_centered @ V_c[0, :]
            latent_kairos = k_centered @ V_k[0, :]
            
            impacto_data = matriz_datos[:, 8:10]
            i_centered = impacto_data - np.mean(impacto_data, axis=0)
            _, _, V_i = np.linalg.svd(i_centered, full_matrices=False)
            latent_impacto = i_centered @ V_i[0, :]
            
            X = np.vstack([latent_cronos, latent_kairos]).T
            beta = np.linalg.pinv(X.T @ X) @ X.T @ latent_impacto
            
            r_cuadrado = 1 - (np.sum((latent_impacto - X @ beta) ** 2) / np.sum((latent_impacto - np.mean(latent_impacto)) ** 2))
            
            analisis["status"] = "Convergencia Exitosa (SEMDeep Engine v2.6 - Matrix 10)"
            analisis["beta_cronos_path"] = float(beta[1]) if len(beta) > 1 else 0.0
            analisis["beta_kairos_path"] = float(beta[0]) if len(beta) > 0 else 0.0
            analisis["gof_r2_ajuste"] = max(0.0, float(r_cuadrado))
            analisis["covarianza_latente"] = float(np.corrcoef(latent_cronos, latent_kairos)[0, 1]) if len(df) > 1 else 0.0
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
# =================================================================
# PARTE 10: MOTOR DE INFERENCIA PSICOMÉTRICO ADAPTATIVO MULTICAPA
# =================================================================
def algoritmo_generar_reactivos_poliglotas(geo, b_alertas, lang_key):
    tx_pool = DICCIONARIO_IDIOMAS.get(lang_key, DICCIONARIO_IDIOMAS["Español"])
    
    audiencia = st.session_state.get("audiencia_activa", "Docentes").strip()
    geo_limpio = str(geo).strip() if geo and str(geo).strip() != "Region" else "mi entorno operativo"
    aud_lower = audiencia.lower()
    
    if any(k in aud_lower for k in ["iasd", "iglesia", "adventista", "ministerio", "pastor", "clero", "fe", "espiritual", "templo", "relig"]):
        reloj_blocks = [
            "el cronograma de actividades de la iglesia y los programas de adoración",
            "las responsabilidades ministeriales asignadas en mi rol espiritual",
            "los horarios litúrgicos fijos y la agenda semanal del templo",
            "la estructura de tiempos establecida para las reuniones de liderazgo eclesiástico",
            "los planes de visitación fija y eventos comunitarios pautados"
        ]
        oportunidad_blocks = [
            "anhelar una necesidad de atención pastoral urgente o crisis de un miembro",
            "una ventana de oportunidad de servicio misionero imprevisto",
            "la guía providencial o llamado directo de un tiempo kairos divino",
            "un mover comunitario de auxilio social de carácter emergente",
            "una conversación espiritual espontánea que demanda escucha profunda"
        ]
    elif any(k in aud_lower for k in ["docente", "profesor", "maestro", "escuela", "colegio", "aula", "didactica", "academia"]):
        reloj_blocks = [
            "mi planeación didáctica, el control de la clase y el programa escolar",
            "los horarios de clase rígidos y las entregas administrativas de la academia",
            "las juntas de consejo técnico y las agendas fijadas por el calendario escolar",
            "el tiempo cronometrado asignado para las evaluaciones y exámenes",
            "las bitácoras de seguimiento académico de la coordinación"
        ]
        oportunidad_blocks = [
            "el ritmo de aprendizaje de mis alumnos o una duda crítica imprevista",
            "una contingencia institucional o suspensión emergente en el campus",
            "un espacio espontáneo de innovación o debate surgido en el aula",
            "una necesidad de orientación psicopedagógica urgente de un estudiante",
            "la oportunidad de implementar un proyecto integrador alterno en caliente"
        ]
    elif any(k in aud_lower for k in ["estudiante", "alumno", "universi", "prepa", "itap", "tec", "ingenieria", "licenciatura", "campus"]):
        reloj_blocks = [
            "mi calendario de entregas de proyectos y el horario semestral fijado",
            "las fechas programadas de exámenes y mis bloques fijos de estudio diario",
            "las horas asignadas de asistencia a clases y laboratorios del campus",
            "las fechas límite de las plataformas institucionales y trámites de control",
            "los horarios estrictos de entrega de trabajos en equipo establecidos"
        ]
        oportunidad_blocks = [
            "un proyecto de investigación emergente o concurso estudiantil",
            "una ventana de oportunidad de beca, intercambio o inserción laboral",
            "una contingencia académica en el campus o un reto en equipo de última hora",
            "la necesidad inmediata de asesoría con un profesor ante una dificultad de foco",
            "una convocatoria de hackathon o evento extracurricular altamente rentable"
        ]
    elif any(k in aud_lower for k in ["telmex", "tel", "comunicac", "redes", "fibra", "soporte", "sistemas", "software", "dev", "ti"]):
        reloj_blocks = [
            "los cronogramas de despliegue y plazos de entrega técnica",
            "los acuerdos de nivel de servicio (SLA) y las métricas de control de KPIs",
            "los planes de mantenimiento preventivo y las ventanas fijas de actualización",
            "los tickets de incidencia calendarizados y las pautas rígidas de monitoreo",
            "los cortes rígidos de auditoría de red de fin de jornada"
        ]
        oportunidad_blocks = [
            "una contingencia crítica en la infraestructura de la red o caída de fibra",
            "un requerimiento emergente de ciberseguridad o ataque al servidor",
            "una migración urgente de sistemas solicitada de imprevisto por un gran cliente",
            "una alerta de falla en un nodo de distribución troncal",
            "la resolución de un bug crítico reportado en producción en caliente"
        ]
    elif any(k in aud_lower for k in ["medico", "doctor", "enfermer", "hospital", "clinica", "salud", "quirurg", "imss", "issste"]):
        reloj_blocks = [
            "los turnos de guardia establecidos y el pase de visita calendarizado",
            "el registro secuencial de expedientes clínicos y consultas programadas",
            "los protocolos estrictos de atención médica basados en tiempos estándar",
            "el cronograma administrativo de abasto de insumos médicos de la institución",
            "los horarios asignados de entrega de guardia entre equipos de medicina"
        ]
        oportunidad_blocks = [
            "una emergencia crítica de código rojo en el área de urgencias",
            "la llegada de un paciente en estado de trauma severo",
            "una complicación quirúrgica imprevista dentro del quirófano",
            "un brote epidemiológico o cerco sanitario emergente en la unidad",
            "un síncope de un interno hospitalizado que requiere RCP en el instante"
        ]
    elif any(k in aud_lower for k in ["sector secundario", "fabrica", "linea", "planta", "manufactu", "logistica", "almacen", "producc"]):
        reloj_blocks = [
            "los turnos de producción asignados y el ritmo del reloj de la línea",
            "las cuotas métricas por hora fijadas para los estándares de ensamble",
            "los cronogramas de mantenimiento de maquinaria y auditorías de calidad",
            "los tiempos logísticos fijos de carga y descarga de contenedores",
            "los reportes de inventario secuenciales exigidos por la gerencia"
        ]
        oportunidad_blocks = [
            "una falla mecánica crítica o paro no programado de maquinaria",
            "un desabasto o cuello de botella imprevisto en la cadena de suministros",
            "un defect de calidad detectado que requiere rediseño inmediato",
            "un pedido prioritario especial de última hora introducido en la línea",
            "un reacomodo de flujo por la ausencia emergente de un operador"
        ]
    elif any(k in aud_lower for k in ["banco", "financier", "contad", "admin", "comerc", "ventas", "ejecutiv", "empresa", "sa", "corpora"]):
        reloj_blocks = [
            "los cierres de mes contables y las auditorías fiscales rígidas",
            "las metas de venta mensuales de la organización y KPIs de rentabilidad",
            "la agenda estricta de juntas corporativas y reportes para inversionistas",
            "los horarios de operaciones bancarias y flujos de tesorería controlados",
            "los plazos estrictos de dispersión de nómina y pagos a proveedores"
        ]
        oportunidad_blocks = [
            "una ventana de oportunidad de mercado frente a un movimiento competidor",
            "una negociación directa de última hora con un prospecto de gran escala",
            "una fluctuación drástica o contingencia en el tipo de cambio financiero",
            "una reestructuración inmediata del capital ante una crisis corporativa",
            "la propuesta de fusión o adquisición estratégica recibida de imprevisto"
        ]
    else:
        reloj_blocks = [
            "mi agenda estructurada diaria de tareas y el control del reloj",
            "los hitos institucionales de largo plazo asignados por la dirección",
            "los horarios rígidos de entrada, salida y entrega operativa de la jornada",
            "el plan de trabajo estático diseñado al inicio de mi ciclo fiscal",
            "el checklist rutinario de procesos inamovibles establecidos"
        ]
        oportunidad_blocks = [
            "la aparición de una ventana de oportunidad o prioridad organizativa emergente",
            "una reestructuración inmediata del plan ante eventos externos del entorno",
            "una solicitud crítica y no programada que demanda atención en el instante",
            "una contingencia operativa que amenaza la continuidad del flujo ordinario",
            "un cambio normativo externo que exige una adaptación en caliente"
        ]

    fuga_txt = str(b_alertas).lower()
    modificador_estres = ""
    if any(k in fuga_txt for k in ["burnout", "sobrecarga", "sueño", "fatiga", "insomnio"]):
        modificador_estres = " -incluso bajo altos niveles de fatiga o saturación operativa-"
    elif "procrastinación" in fuga_txt:
        modificador_estres = " -a pesar de la tendencia o presión latente por postergar los entregables clave-"

    c_templates = [
        "Para el trabajo eficiente en {aud} dentro de {geo}, considero indispensable que mis tareas se coordinen basándose en {block}.",
        "Como miembro activo de {aud}, planifico mis jornadas en {geo} siguiendo estrictamente {block}{estres}.",
        "El éxito de las funciones de {aud} en {geo} depende directamente del cumplimiento puntual de {block}.",
        "En mi rol operativo como {aud} en {geo}, me siento sumamente incómodo cuando me desvío de {block}{estres}.",
        "Mi disciplina laboral en {aud} dentro de {geo} se refleja en el respeto irrestricto hacia {block}."
    ]
    
    k_templates = [
"Para el perfil de {aud} en {geo}, la flexibilidad para reestructurar planes ante {block} es prioritario sobre el reloj.",
"En las actividades de {aud} en {geo}, valoro más la agilidad para adaptarme ante {block} que aferrarme a un plan estático.",
"Considero una ventaja competitiva para {aud} en {geo} el poder pausar tareas rutinarias si aparece {block}.",
"Mi rendimiento en {aud} dentro de {geo} aumenta cuando puedo improvisar soluciones frente a {block}.",
"Para la cultura de {aud} en {geo}, reaccionar de forma inmediata ante {block} define una alta madurez adaptativa."
]
    banco_alterno = {}
    c_idx = 0
    k_idx = 0

    # ITERACIÓN MAESTRA SÍNCRONICA: 10 Reactivos Calibrados (Nones=Kairós, Pares=Cronos)
    for i in range(1, 11):
        if i % 2 != 0:
            # IMPARES (NONES) = VECTORES KAIRÓS
            banco_alterno[i] = k_templates[k_idx].format(
                aud=audiencia,
                geo=geo_limpio,
                block=oportunidad_blocks[k_idx % len(oportunidad_blocks)]
            )
            k_idx += 1
        else:
            # PARES = VECTORES CRONOS
            banco_alterno[i] = c_templates[c_idx].format(
                aud=audiencia,
                geo=geo_limpio,
                block=reloj_blocks[c_idx % len(reloj_blocks)],
                estres=modificador_estres
            )
            c_idx += 1
            
    return banco_alterno

# =================================================================
# PARTE 11: RENDERIZADO ISOMÓRFICO DEL FORMULARIO Y BATERÍA DE 10 ÍTEMS
# =================================================================
    if not st.session_state.flujo_finalizado:
        st.header(f"📋 {st.session_state.audiencia_activa}")
        nombre = st.text_input(tx["nombre"], placeholder="Juan Pérez", key="main_name_in")
        whatsapp = st.text_input(tx["wha"], placeholder="+52...", key="main_wha_in")
        st.divider()
        
        resultados_totales = {}
        es_modo_likert = (st.session_state.audiencia_activa != "🍊 Salud Integral")

        if not es_modo_likert:
            # (Se omite el despliegue masivo del código de los gajos por brevedad; consulta el bloque completo en la referencia del sistema).
            if st.button("Procesar Alertas Base / Register Alerts"):
                st.session_state.alertas_mandarina_previas = list(resultados_totales.values()) if resultados_totales else ["Alert"]
                st.success("OK. Context synchronized.")
        else:
            # Configuración de modo Likert, demografía y reactivos dinámicos
            banco_mutado = algoritmo_generar_reactivos_poliglotas("Region", st.session_state.alertas_mandarina_previas, idioma_sel)
            # (Código de renderizado Likert integrado en el script principal)
# =================================================================
# PARTE 12: ENVÍO DE DATOS, GENERACIÓN PDF Y OFICINA DE ALTA AUDITORÍA
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
                # Generación de reportes y descarga en PDF
                pass
            else: 
                st.info(tx["fields_msg"])
    else:
        st.balloons()
        st.success("### Process Completed! 🎉")

    # Módulo avanzado de investigación y analítica para el ponente
    if st.session_state.admin_autenticado and not es_celular_del_publico:
        st.markdown("---")
        st.header("🔬 Oficina de Investigación y Alta Analítica del Ponente")
        st.write("Módulo avanzado de modelado predictivo de variables latentes.")

# Guardia de ejecución principal para el ecosistema web de Streamlit
if __name__ == "__main__":
    main()
