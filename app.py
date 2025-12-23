import streamlit as st
from fpdf import FPDF
import qrcode
import tempfile
import os

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Generador de Topoguías", layout="wide")
st.title("🏔️ Generador de Topoguías (Estilo PR-GU)")
st.info("Sube las imágenes y textos para generar el PDF automáticamente.")

# --- BARRA LATERAL (DATOS) ---
with st.sidebar:
    st.header("1. Textos Generales")
    codigo_ruta = st.text_input("Código de Ruta", "PR-GU 08")
    titulo = st.text_input("Nombre del Sendero", "MANDAYONA-MIRABUENO-ARAGOSA")
    
    st.header("2. Ficha Técnica (Texto)")
    # Datos extraídos del ejemplo 
    col1, col2 = st.columns(2)
    distancia = col1.text_input("Distancia", "11,0 Km")
    tiempo = col2.text_input("Tiempo", "2h 35m")
    desnivel = col1.text_input("Desnivel (+/-)", "167 m")
    tipo = col2.text_input("Tipo", "Circular")

    st.header("3. Contenidos y QR")
    url_web = st.text_input("Web para el QR", "http://areasprotegidas.castillalamancha.es")
    # Texto de ejemplo basado en 
    desc_texto = st.text_area("Descripción", height=200, 
        value="Este sendero circular comienza en el Centro de Interpretación...")

    st.header("4. Subir Imágenes")
    st.warning("Sube imágenes en formato JPG o PNG")
    # Subida de imágenes basada en la estructura visual del PDF [cite: 40, 97, 55]
    img_mide = st.file_uploader("Imagen Tabla MIDE", type=['png', 'jpg', 'jpeg'])
    img_mapa = st.file_uploader("Imagen Mapa", type=['png', 'jpg', 'jpeg'])
    img_perfil = st.file_uploader("Imagen Perfil Elevación", type=['png', 'jpg', 'jpeg'])
    img_banner = st.file_uploader("Foto Panorámica (Opcional)", type=['png', 'jpg', 'jpeg'])

# --- GENERADOR DE PDF ---
class PDF(FPDF):
    def header(self):
        # Franja verde superior estilo [cite: 1]
        self.set_fill_color(0, 128, 0) # Verde
        self.rect(0, 0, 210, 25, 'F')
        self.set_font('Helvetica', 'B', 24)
        self.set_text_color(255, 255, 255)
        self.set_xy(10, 5)
        self.cell(0, 10, codigo_ruta, new_x="LMARGIN", new_y="NEXT", align='L')
        self.set_font('Helvetica', '', 12)
        self.cell(0, 6, titulo, new_x="LMARGIN", new_y="NEXT", align='L')

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Generado con herramienta web interna', align='C')

def crear_pdf():
    pdf = PDF()
    pdf.add_page()
    
    # 1. Foto Panorámica (Si se sube)
    y_inicio = 35
    if img_banner:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(img_banner.getvalue())
            pdf.image(tmp.name, x=10, y=30, w=190, h=40)
        y_inicio = 75

    # 2. Descripción (Izquierda)
    pdf.set_xy(10, y_inicio)
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(0)
    # Ajustamos ancho para dejar hueco a la derecha
    pdf.multi_cell(115, 5, desc_texto)
    y_fin_texto = pdf.get_y()

    # 3. Columna Derecha (Datos, MIDE, QR)
    # Coordenada X fija para la columna derecha
    x_col_der = 130
    
    # Cuadro Gris con datos 
    pdf.set_xy(x_col_der, y_inicio)
    pdf.set_fill_color(240, 240, 240)
    pdf.rect(x_col_der, y_inicio, 70, 25, 'F')
    
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_xy(x_col_der + 2, y_inicio + 2)
    pdf.cell(30, 5, f"Distancia: {distancia}")
    pdf.set_xy(x_col_der + 2, y_inicio + 7)
    pdf.cell(30, 5, f"Tiempo: {tiempo}")
    pdf.set_xy(x_col_der + 35, y_inicio + 2)
    pdf.cell(30, 5, f"Desnivel: {desnivel}")
    pdf.set_xy(x_col_der + 35, y_inicio + 7)
    pdf.cell(30, 5, f"Tipo: {tipo}")

    y_actual_der = y_inicio + 28

    # Imagen MIDE (Se coloca debajo de los datos)
    if img_mide:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(img_mide.getvalue())
            # Ajustamos tamaño del MIDE
            pdf.image(tmp.name, x=x_col_der, y=y_actual_der, w=70)
            y_actual_der += 35 # Espacio que ocupa el MIDE aprox

    # Código QR (Debajo del MIDE)
    if url_web:
        qr = qrcode.make(url_web)
        qr_path = "temp_qr.png"
        qr.save(qr_path)
        pdf.image(qr_path, x=x_col_der + 20, y=y_actual_der + 5, w=25)
        os.remove(qr_path)

    # 4. Mapa y Perfil (Debajo de todo lo anterior)
    # Calculamos cuál es el punto más bajo: texto izquierda o columna derecha
    y_siguiente = max(y_fin_texto, y_actual_der + 35) + 10

    if img_mapa:
        pdf.set_xy(10, y_siguiente)
        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(0, 10, "MAPA DE RUTA", new_x="LMARGIN", new_y="NEXT")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(img_mapa.getvalue())
            pdf.image(tmp.name, x=10, w=190)
            # FPDF no devuelve altura de imagen directamente, sumamos estimado
            y_siguiente = pdf.get_y() + 5

    # Control de salto de página si no cabe el perfil
    if y_siguiente > 240:
        pdf.add_page()
        y_siguiente = 30

    if img_perfil:
        pdf.set_xy(10, y_siguiente)
        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(0, 10, "PERFIL DE ELEVACIÓN", new_x="LMARGIN", new_y="NEXT")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(img_perfil.getvalue())
            pdf.image(tmp.name, x=10, h=35) # Altura fija para perfil

    return pdf.output()

# --- BOTÓN FINAL ---
st.divider()
st.markdown("### Generar Documento")
if st.button("CREAR PDF", type="primary"):
    if not img_mapa or not img_mide:
        st.error("¡Faltan imágenes! Por favor sube al menos el Mapa y el MIDE.")
    else:
        pdf_bytes = crear_pdf()
        st.success("¡Folleto creado correctamente!")
        st.download_button(
            label="⬇️ Descargar PDF Final",
            data=pdf_bytes,
            file_name=f"Folleto_{codigo_ruta}.pdf",
            mime="application/pdf"
        )
