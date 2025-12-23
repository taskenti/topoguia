import streamlit as st
from fpdf import FPDF
import qrcode
import tempfile
import os
from datetime import datetime
import json

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Generador de Topoguías PR-GU",
    layout="wide",
    page_icon="🏔️"
)

# --- CSS PERSONALIZADO ---
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #2d5016 0%, #4a7c2e 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        padding: 0 2rem;
    }
    .upload-box {
        border: 2px dashed #cccccc;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .info-box {
        background-color: #f0f9ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div class="main-header">
    <h1>🏔️ Generador de Topoguías</h1>
    <p style="font-size: 1.1rem; margin-top: 0.5rem;">Estilo PR-GU - Red de Senderos de Guadalajara</p>
</div>
""", unsafe_allow_html=True)

# --- FUNCIONES AUXILIARES ---
def cargar_plantilla():
    """Carga datos de plantilla por defecto"""
    return {
        'entidad_promotora': 'Junta de Comunidades de Castilla-La Mancha',
        'red_senderos': 'Red de Senderos de Guadalajara',
        'homologacion': 'Federación de Montañismo',
        'web_institucional': 'http://areasprotegidas.castillalamancha.es'
    }

def validar_campos(datos, imagenes):
    """Valida que los campos obligatorios estén completos"""
    errores = []
    
    if not datos.get('codigo_ruta'):
        errores.append("Código de Ruta")
    if not datos.get('nombre_sendero'):
        errores.append("Nombre del Sendero")
    if not datos.get('distancia'):
        errores.append("Distancia")
    if not datos.get('tiempo'):
        errores.append("Tiempo Estimado")
    if not imagenes.get('mapa'):
        errores.append("Imagen del Mapa")
    if not imagenes.get('perfil'):
        errores.append("Imagen del Perfil")
    if not imagenes.get('mide'):
        errores.append("Imagen de Tabla MIDE")
    
    return errores

# --- SESSION STATE INIT ---
if 'plantilla' not in st.session_state:
    st.session_state.plantilla = cargar_plantilla()

if 'form_data' not in st.session_state:
    st.session_state.form_data = {}

# --- TABS PRINCIPALES ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Datos Básicos",
    "📊 Ficha Técnica",
    "📝 Descripción",
    "🖼️ Imágenes",
    "⚙️ Configuración"
])

# Diccionario para almacenar todas las imágenes
imagenes = {}

# ==================== TAB 1: DATOS BÁSICOS ====================
with tab1:
    st.header("Información General del Sendero")
    
    col1, col2 = st.columns(2)
    
    with col1:
        codigo_ruta = st.text_input(
            "Código de Ruta *",
            value="PR-GU 08",
            help="Código identificador de la ruta (ej: PR-GU 08)"
        )
        
        punto_inicio = st.text_input(
            "Punto de Inicio",
            placeholder="Mandayona",
            help="Localidad o punto donde comienza el sendero"
        )
        
        coordenadas = st.text_input(
            "Coordenadas GPS",
            placeholder="41°01'23\"N 2°38'45\"W",
            help="Coordenadas del punto de inicio"
        )
    
    with col2:
        nombre_sendero = st.text_input(
            "Nombre del Sendero *",
            value="MANDAYONA-MIRABUENO-ARAGOSA",
            help="Nombre descriptivo de la ruta"
        )
        
        municipio = st.text_input(
            "Municipio(s)",
            placeholder="Mandayona",
            help="Municipios por los que transcurre la ruta"
        )
    
    st.subheader("Acceso")
    como_llegar = st.text_area(
        "Cómo Llegar",
        placeholder="Desde Guadalajara por la CM-101...",
        help="Descripción de cómo llegar al punto de inicio",
        height=100
    )

# ==================== TAB 2: FICHA TÉCNICA ====================
with tab2:
    st.header("Características Técnicas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        distancia = st.text_input(
            "Distancia Total *",
            value="11,0 Km",
            help="Distancia total del recorrido"
        )
        
        desnivel_positivo = st.text_input(
            "Desnivel Positivo",
            value="167 m",
            help="Metros de subida acumulada"
        )
        
        altitud_min = st.text_input(
            "Altitud Mínima",
            placeholder="850 m",
            help="Punto más bajo de la ruta"
        )
    
    with col2:
        tiempo = st.text_input(
            "Tiempo Estimado *",
            value="2h 35m",
            help="Tiempo estimado para completar la ruta"
        )
        
        desnivel_negativo = st.text_input(
            "Desnivel Negativo",
            value="167 m",
            help="Metros de bajada acumulada"
        )
        
        altitud_max = st.text_input(
            "Altitud Máxima",
            placeholder="1050 m",
            help="Punto más alto de la ruta"
        )
    
    with col3:
        tipo_ruta = st.selectbox(
            "Tipo de Ruta *",
            ["Circular", "Lineal", "Semi-circular"],
            help="Tipo de recorrido"
        )
        
        dificultad = st.selectbox(
            "Dificultad",
            ["Baja", "Media", "Alta"],
            index=1,
            help="Nivel de dificultad general"
        )
        
        tipo_firme = st.text_input(
            "Tipo de Firme",
            placeholder="Camino rural, sendero",
            help="Características del terreno"
        )
    
    st.divider()
    st.subheader("Información Adicional")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        epoca = st.text_input(
            "Época Recomendada",
            value="Todo el año",
            help="Mejor época para realizar la ruta"
        )
    
    with col2:
        agua = st.text_input(
            "Disponibilidad de Agua",
            value="No disponible en ruta",
            help="Fuentes o puntos de agua en el recorrido"
        )
    
    with col3:
        sombra = st.text_input(
            "Sombra",
            value="Escasa",
            help="Disponibilidad de zonas con sombra"
        )

# ==================== TAB 3: DESCRIPCIÓN ====================
with tab3:
    st.header("Descripción y Contenidos")
    
    descripcion = st.text_area(
        "Descripción del Sendero *",
        height=250,
        placeholder="Este sendero circular comienza en el Centro de Interpretación...",
        help="Describe el recorrido, paisajes y características principales de la ruta"
    )
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        puntos_interes = st.text_area(
            "Puntos de Interés",
            height=150,
            placeholder="• Iglesia de San Bartolomé\n• Mirador de Mirabueno\n• Ermita de Aragosa",
            help="Lugares destacados a lo largo del recorrido"
        )
    
    with col2:
        flora_fauna = st.text_area(
            "Flora y Fauna",
            height=150,
            placeholder="Encinas, quejigos, águila real, buitre leonado...",
            help="Especies vegetales y animales destacadas"
        )
    
    st.divider()
    
    consejos = st.text_area(
        "Consejos y Recomendaciones",
        height=120,
        placeholder="• Llevar agua suficiente\n• Protección solar recomendada\n• Calzado adecuado para senderismo",
        help="Recomendaciones para los senderistas"
    )
    
    precauciones = st.text_area(
        "Precauciones",
        height=120,
        placeholder="• Evitar los días de mucho calor\n• No recomendable con lluvia intensa",
        help="Advertencias importantes sobre la ruta"
    )

# ==================== TAB 4: IMÁGENES ====================
with tab4:
    st.header("Imágenes y Mapas")
    
    st.markdown("""
    <div class="info-box">
        <strong>ℹ️ Información:</strong> Las imágenes con asterisco (*) son obligatorias.
        Formatos aceptados: JPG, JPEG, PNG. Tamaño máximo recomendado: 5MB por imagen.
    </div>
    """, unsafe_allow_html=True)
    
    # Foto Panorámica
    st.subheader("📸 Foto Panorámica / Banner")
    st.caption("Imagen opcional que aparecerá en la parte superior del folleto")
    img_banner = st.file_uploader(
        "Sube la foto panorámica",
        type=['png', 'jpg', 'jpeg'],
        key="banner",
        help="Imagen panorámica del paisaje o inicio de la ruta"
    )
    if img_banner:
        st.image(img_banner, caption="Vista previa - Banner", use_container_width=True)
        imagenes['banner'] = img_banner
    
    st.divider()
    
    # Columnas para imágenes principales
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🗺️ Mapa de Ruta *")
        st.caption("Mapa con el trazado completo del sendero")
        img_mapa = st.file_uploader(
            "Sube el mapa de la ruta",
            type=['png', 'jpg', 'jpeg'],
            key="mapa",
            help="Mapa topográfico o esquemático con el recorrido marcado"
        )
        if img_mapa:
            st.image(img_mapa, caption="Vista previa - Mapa", use_container_width=True)
            imagenes['mapa'] = img_mapa
        else:
            st.warning("⚠️ Imagen obligatoria")
    
    with col2:
        st.subheader("📈 Perfil de Elevación *")
        st.caption("Gráfica del perfil altimétrico de la ruta")
        img_perfil = st.file_uploader(
            "Sube el perfil de elevación",
            type=['png', 'jpg', 'jpeg'],
            key="perfil",
            help="Gráfico que muestra las variaciones de altitud"
        )
        if img_perfil:
            st.image(img_perfil, caption="Vista previa - Perfil", use_container_width=True)
            imagenes['perfil'] = img_perfil
        else:
            st.warning("⚠️ Imagen obligatoria")
    
    st.divider()
    
    # Tabla MIDE
    st.subheader("📊 Tabla MIDE *")
    st.caption("Método de Información De Excursiones - Valoración de dificultad")
    img_mide = st.file_uploader(
        "Sube la tabla MIDE",
        type=['png', 'jpg', 'jpeg'],
        key="mide",
        help="Tabla con los valores MIDE del sendero"
    )
    if img_mide:
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.image(img_mide, caption="Vista previa - MIDE", use_container_width=True)
        imagenes['mide'] = img_mide
    else:
        st.warning("⚠️ Imagen obligatoria")
    
    st.divider()
    
    # Fotos adicionales
    st.subheader("📷 Fotografías Adicionales (Opcional)")
    col1, col2 = st.columns(2)
    
    with col1:
        img_foto1 = st.file_uploader(
            "Foto adicional 1",
            type=['png', 'jpg', 'jpeg'],
            key="foto1"
        )
        if img_foto1:
            st.image(img_foto1, caption="Foto 1", use_container_width=True)
            imagenes['foto1'] = img_foto1
    
    with col2:
        img_foto2 = st.file_uploader(
            "Foto adicional 2",
            type=['png', 'jpg', 'jpeg'],
            key="foto2"
        )
        if img_foto2:
            st.image(img_foto2, caption="Foto 2", use_container_width=True)
            imagenes['foto2'] = img_foto2

# ==================== TAB 5: CONFIGURACIÓN ====================
with tab5:
    st.header("Configuración y Datos Institucionales")
    
    st.subheader("🌐 Enlaces Web")
    col1, col2 = st.columns(2)
    
    with col1:
        url_qr = st.text_input(
            "URL para Código QR",
            value=st.session_state.plantilla['web_institucional'],
            help="URL que se mostrará en el código QR del folleto"
        )
    
    with col2:
        url_mas_info = st.text_input(
            "URL Información Adicional",
            placeholder="https://turismoguadalajara.es",
            help="URL adicional para más información"
        )
    
    st.divider()
    st.subheader("🏛️ Datos Institucionales (Plantilla)")
    st.caption("Estos datos son comunes para todas las rutas y aparecerán automáticamente en los folletos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        entidad_promotora = st.text_input(
            "Entidad Promotora",
            value=st.session_state.plantilla['entidad_promotora'],
            help="Organismo o entidad que promueve la ruta"
        )
        
        red_senderos = st.text_input(
            "Red de Senderos",
            value=st.session_state.plantilla['red_senderos'],
            help="Red o sistema de senderos al que pertenece"
        )
    
    with col2:
        homologacion = st.text_input(
            "Homologación",
            value=st.session_state.plantilla['homologacion'],
            help="Entidad que homologa el sendero"
        )
        
        contacto = st.text_input(
            "Contacto / Teléfono",
            placeholder="949 88 70 00",
            help="Teléfono de contacto o información"
        )
    
    st.divider()
    
    if st.button("💾 Guardar Configuración de Plantilla", type="secondary"):
        st.session_state.plantilla = {
            'entidad_promotora': entidad_promotora,
            'red_senderos': red_senderos,
            'homologacion': homologacion,
            'web_institucional': url_qr
        }
        st.success("✅ Configuración guardada correctamente")

# ==================== GENERACIÓN DEL PDF ====================
class PDF(FPDF):
    def __init__(self, datos):
        super().__init__()
        self.datos = datos
    
    def header(self):
        # Franja verde superior
        self.set_fill_color(45, 80, 22)  # Verde oscuro
        self.rect(0, 0, 210, 30, 'F')
        
        # Código de ruta
        self.set_font('Helvetica', 'B', 26)
        self.set_text_color(255, 255, 255)
        self.set_xy(10, 8)
        self.cell(0, 8, self.datos.get('codigo_ruta', ''), align='L')
        
        # Nombre del sendero
        self.set_font('Helvetica', 'B', 14)
        self.set_xy(10, 18)
        self.cell(0, 8, self.datos.get('nombre_sendero', ''), align='L')
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        fecha = datetime.now().strftime("%d/%m/%Y")
        self.cell(0, 10, f'Generado el {fecha} - {self.datos.get("entidad_promotora", "")}', align='C')

def crear_pdf_topoguia(datos, imgs):
    """Genera el PDF de la topoguía"""
    pdf = PDF(datos)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    y_actual = 35
    
    # 1. FOTO PANORÁMICA (si existe)
    if imgs.get('banner'):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(imgs['banner'].getvalue())
            pdf.image(tmp.name, x=10, y=y_actual, w=190, h=45)
            os.remove(tmp.name)
        y_actual += 50
    
    # 2. LAYOUT PRINCIPAL: Descripción (izq) + Datos (der)
    x_columna_izq = 10
    x_columna_der = 135
    ancho_izq = 120
    ancho_der = 65
    
    # COLUMNA IZQUIERDA: Descripción
    pdf.set_xy(x_columna_izq, y_actual)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(45, 80, 22)
    pdf.cell(0, 7, 'DESCRIPCIÓN', ln=True)
    
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(0, 0, 0)
    pdf.set_xy(x_columna_izq, pdf.get_y())
    
    desc = datos.get('descripcion', '')
    if desc:
        pdf.multi_cell(ancho_izq, 4.5, desc)
    
    y_fin_descripcion = pdf.get_y()
    
    # COLUMNA DERECHA: Ficha técnica
    y_col_der = y_actual
    
    # Cuadro gris con datos principales
    pdf.set_fill_color(240, 240, 240)
    pdf.rect(x_columna_der, y_col_der, ancho_der, 32, 'F')
    
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(0, 0, 0)
    
    # Datos en el cuadro
    items_ficha = [
        ('Distancia:', datos.get('distancia', '-')),
        ('Tiempo:', datos.get('tiempo', '-')),
        ('Desnivel (+):', datos.get('desnivel_positivo', '-')),
        ('Tipo:', datos.get('tipo_ruta', '-')),
        ('Dificultad:', datos.get('dificultad', '-')),
    ]
    
    y_item = y_col_der + 3
    for etiqueta, valor in items_ficha:
        pdf.set_xy(x_columna_der + 2, y_item)
        pdf.set_font('Helvetica', 'B', 8)
        pdf.cell(22, 4, etiqueta, align='L')
        pdf.set_font('Helvetica', '', 8)
        pdf.cell(0, 4, valor, align='L')
        y_item += 5.5
    
    y_col_der += 35
    
    # Imagen MIDE
    if imgs.get('mide'):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(imgs['mide'].getvalue())
            pdf.image(tmp.name, x=x_columna_der, y=y_col_der, w=ancho_der)
            os.remove(tmp.name)
        y_col_der += 40
    
    # Código QR
    if datos.get('url_qr'):
        qr = qrcode.QRCode(box_size=10, border=1)
        qr.add_data(datos['url_qr'])
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        qr_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        qr_img.save(qr_path.name)
        
        pdf.image(qr_path.name, x=x_columna_der + 15, y=y_col_der + 2, w=30)
        os.remove(qr_path.name)
        
        pdf.set_font('Helvetica', 'I', 7)
        pdf.set_xy(x_columna_der, y_col_der + 34)
        pdf.multi_cell(ancho_der, 3, 'Más información', align='C')
        
        y_col_der += 45
    
    # Calcular posición para siguiente sección
    y_siguiente = max(y_fin_descripcion, y_col_der) + 8
    
    # 3. PUNTOS DE INTERÉS (si existen)
    if datos.get('puntos_interes'):
        pdf.set_xy(x_columna_izq, y_siguiente)
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(45, 80, 22)
        pdf.cell(0, 7, 'PUNTOS DE INTERÉS', ln=True)
        
        pdf.set_font('Helvetica', '', 9)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(190, 4.5, datos['puntos_interes'])
        y_siguiente = pdf.get_y() + 5
    
    # 4. MAPA
    if imgs.get('mapa'):
        if y_siguiente > 240:
            pdf.add_page()
            y_siguiente = 35
        
        pdf.set_xy(x_columna_izq, y_siguiente)
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(45, 80, 22)
        pdf.cell(0, 7, 'MAPA DE RUTA', ln=True)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(imgs['mapa'].getvalue())
            pdf.image(tmp.name, x=x_columna_izq, y=pdf.get_y() + 2, w=190)
            os.remove(tmp.name)
        
        y_siguiente = pdf.get_y() + 75
    
    # 5. PERFIL DE ELEVACIÓN
    if imgs.get('perfil'):
        if y_siguiente > 230:
            pdf.add_page()
            y_siguiente = 35
        
        pdf.set_xy(x_columna_izq, y_siguiente)
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(45, 80, 22)
        pdf.cell(0, 7, 'PERFIL DE ELEVACIÓN', ln=True)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(imgs['perfil'].getvalue())
            pdf.image(tmp.name, x=x_columna_izq, y=pdf.get_y() + 2, w=190, h=40)
            os.remove(tmp.name)
        
        y_siguiente = pdf.get_y() + 48
    
    # 6. CONSEJOS (si existen)
    if datos.get('consejos'):
        if y_siguiente > 250:
            pdf.add_page()
            y_siguiente = 35
        
        pdf.set_xy(x_columna_izq, y_siguiente)
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(45, 80, 22)
        pdf.cell(0, 6, 'CONSEJOS Y RECOMENDACIONES', ln=True)
        
        pdf.set_font('Helvetica', '', 8)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(190, 4, datos['consejos'])
    
    return bytes(pdf.output())

# ==================== BARRA LATERAL Y GENERACIÓN ====================
st.sidebar.header("🎯 Acciones")

# Resumen
st.sidebar.subheader("📊 Resumen")
st.sidebar.write(f"**Ruta:** {codigo_ruta if 'codigo_ruta' in locals() else 'Sin definir'}")
st.sidebar.write(f"**Nombre:** {nombre_sendero[:30] if 'nombre_sendero' in locals() and nombre_sendero else 'Sin definir'}...")

# Validación
datos_formulario = {
    'codigo_ruta': codigo_ruta if 'codigo_ruta' in locals() else '',
    'nombre_sendero': nombre_sendero if 'nombre_sendero' in locals() else '',
    'distancia': distancia if 'distancia' in locals() else '',
    'tiempo': tiempo if 'tiempo' in locals() else '',
    'desnivel_positivo': desnivel_positivo if 'desnivel_positivo' in locals() else '',
    'desnivel_negativo': desnivel_negativo if 'desnivel_negativo' in locals() else '',
    'tipo_ruta': tipo_ruta if 'tipo_ruta' in locals() else '',
    'dificultad': dificultad if 'dificultad' in locals() else '',
    'descripcion': descripcion if 'descripcion' in locals() else '',
    'puntos_interes': puntos_interes if 'puntos_interes' in locals() else '',
    'consejos': consejos if 'consejos' in locals() else '',
    'url_qr': url_qr if 'url_qr' in locals() else '',
    'entidad_promotora': entidad_promotora if 'entidad_promotora' in locals() else '',
}

errores = validar_campos(datos_formulario, imagenes)

if errores:
    st.sidebar.error(f"⚠️ Faltan {len(errores)} campo(s):")
    for error in errores:
        st.sidebar.write(f"• {error}")
else:
    st.sidebar.success("✅ Todos los campos completos")

st.sidebar.divider()

# Botón de generación
if st.sidebar.button("🚀 GENERAR PDF", type="primary", use_container_width=True):
    if errores:
        st.error(f"❌ No se puede generar el PDF. Faltan los siguientes campos obligatorios:\n\n" + 
                "\n".join([f"• {e}" for e in errores]))
    else:
        try:
            with st.spinner("Generando PDF..."):
                pdf_bytes = crear_pdf_topoguia(datos_formulario, imagenes)
                
                st.success("✅ ¡PDF generado correctamente!")
                
                nombre_archivo = f"Topoguia_{codigo_ruta.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
                
                st.download_button(
                    label="⬇️ Descargar PDF",
                    data=pdf_bytes,
                    file_name=nombre_archivo,
                    mime="application/pdf",
                    use_container_width=True
                )
        except Exception as e:
            st.error(f"❌ Error al generar el PDF: {str(e)}")
