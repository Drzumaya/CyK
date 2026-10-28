from fpdf import FPDF
import datetime

def generar_pdf_diagnostico(nombre_usuario, whatsapp_usuario, resultados_totales, st_cronos_kairos):
    """Construye la estructura binaria del PDF con las 7 dimensiones."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # 1. Encabezado Institucional
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(230, 81, 0) 
    pdf.cell(0, 10, "REPORTE DE DIAGNÓSTICO DE SALUD INTEGRAL", ln=True, align="C")
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, "Modelo Mandarina | Jacob Zumaya Prianti (c) 2026", ln=True, align="C")
    pdf.ln(5)
    
    # Línea decorativa naranja
    pdf.set_draw_color(255, 152, 0)
    pdf.set_line_width(1)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(10)
    
    # 2. Datos de Identificación
    pdf.set_text_color(50, 50, 50)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(45, 6, "Participante:", 0, 0)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, nombre_usuario if nombre_usuario else "Participante Anónimo", 0, 1)
    
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(45, 6, "WhatsApp de Contacto:", 0, 0)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, whatsapp_usuario if whatsapp_usuario else "No Proporcionado", 0, 1)
    
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(45, 6, "Fecha de Emisión:", 0, 0)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, datetime.date.today().strftime("%d/%m/%Y"), 0, 1)
    pdf.ln(10)
    
    # 3. Mapeo de Diagnósticos de las 7 Dimensiones
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(255, 152, 0)
    pdf.cell(0, 8, "Resultados y Puntos Críticos Detectados", ln=True)
    pdf.line(10, pdf.get_y(), 100, pdf.get_y())
    pdf.ln(4)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(30, 30, 30)
    
    for dim_nombre, items in resultados_totales.items():
        conteo = len(items)
        estado = "Sano y Pleno (0 alertas)"
        if conteo >= 3:
            estado = "CRITICO / URGENCIA INMEDIATA"
        elif conteo > 0:
            estado = "EN ALERTA TEMPRANA"
            
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 6, f"• {dim_nombre}: {estado}", ln=True)
        pdf.set_font("Helvetica", "I", 10)
        puntos_str = ", ".join(items) if conteo > 0 else "Ninguno. Área equilibrada."
        pdf.multi_cell(0, 5, f"Puntos específicos a solucionar: {puntos_str}")
        pdf.ln(3)
        
    pdf.ln(2)
    
    # 4. Bloque de Criterio de Interpretación
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(255, 152, 0)
    pdf.cell(0, 8, "Mensaje de Confirmación e Interpretación", ln=True)
    pdf.line(10, pdf.get_y(), 100, pdf.get_y())
    pdf.ln(4)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 5, "Cada casilla que seleccionaste en tu dispositivo representa un 'punto de fuga' activo de tu bienestar integral.")
    pdf.ln(2)
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 5, "Criterio de Evaluación de Gajos:", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 5, "• 0 Puntos Seleccionados: Gajo Sano y Pleno.\n"
                         "• 1 a 2 Puntos Seleccionados: Gajo en Alerta. Requiere micro-acciones de corrección.\n"
                         "• 3 o más Puntos Seleccionados: Gajo Crítico / Urgencia Inmediata. Debe ser tu prioridad absoluta.")
    pdf.ln(4)
    
    if st_cronos_kairos:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(230, 81, 0)
        pdf.cell(0, 5, "Alerta Especial sobre la Salud Temporal (ST):", ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(50, 50, 50)
        pdf.multi_cell(0, 5, "Has marcado el elemento de 'Cronos & Kairos'. Te encuentras bajo la tiranía del rendimiento constante o en desconexión pragmática. Equilibrar de manera urgente el tiempo cuantitativo con el cualitativo aliviará la carga sistémica de tus dimensiones de inmediato.")
    
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 5, "Diseño de Métricas y Propiedad Intelectual: Jacob Zumaya Prianti (c) 2026", ln=True, align="C")
    
    return pdf.output()
