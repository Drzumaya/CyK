# 🍊 Diagnóstico de Salud Integral - Modelo Mandarina
### Desarrollado por: Jacob Zumaya Prianti (c) 2026

![Licencia](https://shields.io)
![Python](https://shields.io)
![Framework](https://shields.io)

Esta es una aplicación web interactiva y centralizada, diseñada específicamente para dispositivos móviles, que permite a los asistentes de ponencias y talleres realizar un autodiagnóstico de su bienestar en tiempo real. Basado en el **Modelo Mandarina**, el sistema evalúa las variables latentes de la salud de la audiencia, guarda las métricas de forma segura en una base de datos conectada a Google Sheets, despliega un dashboard visual para el ponente y genera de forma inmediata un reporte analítico en formato **PDF** descargable para el participante.

---

## 📈 Dimensiones Evaluadas (Constructos)

El diagnóstico desglosa de manera rigurosa los 7 "gajos" o dimensiones críticas de la salud integral a través de ítems específicos de intervención y mejora:

*   **Salud Física (SF):** Evaluación de hábitos nutricionales, calidad y reparación del sueño, entrenamiento de fuerza o ejercicio estructurado, y niveles de movimiento diario contra el sedentarismo.
*   **Salud Mental (SM):** Medición de funciones cognitivas clave como la retención de memoria, la capacidad de enfoque continuo, el nivel de resiliencia ante la adversidad y la apertura al aprendizaje constante.
*   **Salud Emocional (SE):** Análisis del autoconocimiento afectivo mediante la gestión de emociones, el autocontrol frente a impulsos, la regulación psicológica y la comprensión de los estados de ánimo.
*   **Salud Social (SS):** Cultivo del entorno interpersonal a través de relaciones positivas y libres de toxicidad, comunicación asertiva, empatía activa y la consolidación de una red de apoyo ante crisis.
*   **Salud Económica (SECO):** Herramientas de orden financiero como el diseño de presupuestos, estrategias de ahorro sistemático, inversión de capital, administración de deudas y la creación/generación activa de nuevas fuentes de dinero.
*   **Salud Temporal (ST):** Gestión estratégica del tiempo diario, búsqueda del equilibrio entre el deber y el descanso, definición de prioridades y el balance crítico entre el reloj secuencial (**Cronos**) y el momento de valor oportuno (**Kairos**).
*   **Salud Espiritual (SPI):** Conexión existencial profunda basada en el propósito de vida, la alineación con los valores nucleares, espacios de meditación o contemplación, y la conexión armónica del interior con el exterior.

---

## 🛠️ Arquitectura y Estructura del Proyecto

El repositorio ha sido optimizado bajo una estructura centralizada y limpia de un solo archivo ejecutable para garantizar un despliegue inmediato y sin conflictos de dependencias en Streamlit Cloud:

```text
├── app.py             # Archivo único y centralizador: Interfaz táctil, módulo QR, motor PDF, base de datos y panel del ponente.
└── requirements.txt   # Gestor de dependencias y librerías del proyecto para el ecosistema Google y Python.
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

## 📱 Despliegue en la Nube (Streamlit Cloud)

Para que tus participantes puedan escanear el código QR directamente desde las pantallas de proyección durante tus ponencias:
1. Sube los archivos `app.py` y `requirements.txt` a tu repositorio público de **GitHub**.
2. Inicia sesión en [share.streamlit.io](https://streamlit.io) y vincula tu repositorio.
3. Asegúrate de configurar las credenciales de tu cuenta de servicio de Google dentro de la sección **Settings > Secrets** de Streamlit usando la llave `[gcp_service_account]`.
4. Configura la variable `URL_PRODUCCION` en el archivo `app.py` con el enlace público definitivo que te asigne la plataforma.

---

## 📄 Propiedad Intelectual y Licencia de Uso

Este software y el modelo metodológico subyacente están protegidos por las leyes internacionales de derechos de autor y propiedad intelectual.

**Copyright (c) 2026 Jacob Zumaya Prianti. Todos los derechos reservados.**

### Términos de la Licencia:
Se otorga permiso para utilizar, copiar y desplegar este software únicamente bajo las siguientes condiciones:
1. **Atribución Obligatoria:** Se deben mantener intactos todos los avisos de derechos de autor, marcas registradas y créditos a *Jacob Zumaya Prianti* tanto en el código fuente, la interfaz de usuario de Streamlit como en los reportes PDF generados.
2. **Uso No Comercial:** El uso de este diagnóstico, del código fuente o de la metodología de las 7 dimensiones con fines lucrativos, comerciales o de consultoría externa pagada está estrictamente prohibido a menos que se cuente con una autorización previa, expresa y por escrito del autor.
3. **Prohibición de Obras Derivadas:** No se permite la alteración, transformación o modificación de la estructura de las variables latentes (los 7 gajos de la salud) ni la redistribución del código bajo otro nombre o marca intelectual.

*Para solicitudes de licencias comerciales, talleres institucionales personalizados o autorizaciones especiales de uso, por favor póngase en contacto directo con el titular de los derechos.*
