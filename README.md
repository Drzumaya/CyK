# 🍊 Diagnóstico de Salud Integral - Modelo Mandarina
### Desarrollado por: Jacob Zumaya Prianti (c) 2026

![Licencia](https://shields.io)
![Python](https://shields.io)
![Framework](https://shields.io)

Esta es una aplicación web interactiva y modular diseñada para dispositivos móviles que permite a los asistentes de ponencias y talleres realizar un autodiagnóstico de su bienestar en tiempo real. Basado en el **Modelo Mandarina**, el sistema evalúa las variables latentes de la salud y genera de forma inmediata un reporte analítico en formato **PDF** con pautas de interpretación clínicas.

---

## 📈 Dimensiones Evaluadas (Constructos)

El diagnóstico desglosa los "gajos" o dimensiones críticas de la salud integral a través de ítems específicos de intervención:
*   **Salud Económica (SECO):** Presupuesto, ahorro, inversión, administración financiera y creación/generación del dinero.
*   **Salud Temporal (ST):** Gestión del tiempo, equilibrio de vida, prioridades y el balance crítico entre **Cronos & Kairos**.
*   **Salud Espiritual (SPI):** Propósito de vida, valores nucleares, espacios de meditación y la conexión del interior con el exterior.

---

## 🛠️ Arquitectura y Estructura del Proyecto

El repositorio está organizado bajo un enfoque de programación modular para facilitar su mantenimiento y escalabilidad en servidores de producción:

```text
├── app.py             # Orquestador principal e interfaz táctil (Streamlit)
├── qr_utils.py        # Módulo autónomo de renderizado y lógica del Código QR
├── pdf_utils.py       # Motor de compilación binaria y diseño del reporte PDF
└── requirements.txt   # Gestor de dependencias y librerías del proyecto
```

---

## 🚀 Instalación y Despliegue Local

Si deseas clonar este repositorio y ejecutar la aplicación en tu entorno local (computadora o servidor), sigue estos sencillos pasos desde tu terminal:

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com
   cd modelo-mandarina-diagnostico
   ```

2. **Instalar las dependencias requeridas:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación de Streamlit:**
   ```bash
   streamlit run app.py
   ```

---

## 📱 Despliegue Gratuito en la Nube (Streamlit Cloud)

Para que tus participantes puedan escanear el código QR durante tus ponencias, despliega la app de la siguiente manera:
1. Sube estos 4 archivos a tu cuenta personal de **GitHub**.
2. Entra a [share.streamlit.io](https://streamlit.io) y vincula tu repositorio.
3. Configura la variable `URL_PRODUCCION` en el archivo `app.py` con el enlace público que te asigne la plataforma.

## 📄 Propiedad Intelectual y Derechos de Autor
Este modelo conceptual, sus métricas de evaluación, el diseño de los gajos de salud y el contenido de este diagnóstico son autoría exclusiva de **Jacob Zumaya Prianti**. Todos los derechos reservados (c) 2026. Queda prohibida su reproducción o explotación comercial sin el consentimiento expreso del autor.
