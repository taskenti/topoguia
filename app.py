import streamlit as st
from fpdf import FPDF
import qrcode
import tempfile
import os
from datetime import datetime
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Generador de Topoguías PR-GU",
    layout="wide",
    page_icon="🏔️"
)

# --- SISTEMA DE AUTENTICACIÓN ---
# Crear config.yaml si no existe
if not os.path.exists('config.yaml'):
    config_default = """credentials:
  usernames:
    admin:
      email: admin@topoguias.es
      name: Administrador
      password: $2b$12$KIXqvB5pJH8yGmK6pZ4aEOqN7xGx1tZ4y3rJ8c5d6f7g8h9i0j1k2
    usuario1:
      email: usuario1@example.com
      name: Usuario Demo
      password: $2b$12$KIXqvB5pJH8yGmK6pZ4aEOqN7xGx1tZ4y3rJ8c5d6f7g8h9i0j1k2

cookie:
  expiry_days: 30
  key: some_signature_key_cambiar_en_produccion_12345
  name: topoguias_auth_cookie

preauthorized:
  emails: []
"""
    with open('config.yaml', 'w') as f:
        f.write(config_default)
    st.info("⚙️ Se ha creado un archivo config.yaml por defecto. Por favor, cambia las contraseñas en producción.")

# Cargar configuración de usuarios
try:
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
except FileNotFoundError:
    st.error("❌ No se encuentra el archivo config.yaml. Creando uno por defecto...")
    st.stop()

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Widget de login (API actualizado)
try:
    # Intentar con el nuevo API (v0.3.0+)
    authenticator.login()
except TypeError:
    # Fallback al API antiguo
    authenticator.login('Login', 'main')

name = st.session_state.get("name")
authentication_status = st.session_state.get("authentication_status")
username = st.session_state.get("username")

# Verificar estado de autenticación
if authentication_status == False:
    st.error('Usuario/contraseña incorrectos')
    st.stop()
elif authentication_status == None:
    st.warning('Por favor, introduce tu usuario y contraseña')
    st.info("""
    **Usuarios de prueba:**
    - Usuario: `admin` | Contraseña: `admin123`
    - Usuario: `usuario1` | Contraseña: `demo123`
    """)
    st.stop()

# Si está autenticado, mostrar la aplicación
try:
    authenticator.logout('Cerrar Sesión', 'sidebar')
except:
    authenticator.logout(location='sidebar')
    
st.sidebar.write(f'Bienvenido/a *{name}*')
st.sidebar.divider()

# --- CSS PERSONALIZADO ---
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #007A33 0%, #00a847 100%);
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
        border-left: 4px solid #007A33;
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
        'parque': 'Parque Natural Sierra Norte de Guadalajara',
        'telefono_parque': '949 88 53 00',
        'telefono_emergencias': '112',
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
    "📊 Ficha Técnica y MIDE",
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
            value="Centro de Interpretación",
            placeholder="Mandayona",
            help="Localidad o punto donde comienza el sendero"
        )
        
        lugares_interes = st.text_input(
            "Lugares de Interés (separados por coma)",
            value="Pico Ocejón, Castillo de Atienza",
            help="Lugares destacados que aparecerán etiquetados en la imagen panorámica"
        )
    
    with col2:
        nombre_sendero = st.text_input(
            "Nombre del Sendero *",
            value="MANDAYONA-MIRABUENO-ARAGOSA",
            help="Nombre descriptivo de la ruta"
        )
        
        municipio = st.text_input(
            "Municipio(s)",
            value="Mandayona",
            placeholder="Mandayona",
            help="Municipios por los que transcurre la ruta"
        )
        
        mirador_nombre = st.text_input(
            "Nombre del Mirador (opcional)",
            value="MIRADOR DEL PICO",
            help="Si hay un mirador principal, ponle nombre"
        )

# ==================== TAB 2: FICHA TÉCNICA Y MIDE ====================
with tab2:
    st.header("Características Técnicas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        distancia = st.text_input(
            "Distancia Total *",
            value="11,0 Km",
            help="Distancia total del recorrido"
        )
        
        desnivel_subida = st.text_input(
            "Desnivel Subida",
            value="167 m",
            help="Metros de subida acumulada"
        )
    
    with col2:
        tiempo = st.text_input(
            "Tiempo Estimado (Horario) *",
            value="2h 35m",
            help="Tiempo estimado para completar la ruta"
        )
        
        desnivel_bajada = st.text_input(
            "Desnivel Bajada",
            value="167 m",
            help="Metros de bajada acumulada"
        )
    
    with col3:
        tipo_ruta = st.selectbox(
            "Tipo de Ruta *",
            ["Circular", "Lineal", "Semi-circular"],
            help="Tipo de recorrido"
        )
        
        altitud_rango = st.text_input(
            "Rango Altitud",
            value="900-1100 m",
            help="Altitud mínima y máxima (ej: 900-1100 m)"
        )
    
    st.divider()
    st.subheader("Valores MIDE (Método de Información De Excursiones)")
    st.caption("Valoración del 1 al 5 para cada aspecto")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        mide_severidad = st.number_input(
            "Severidad del Medio",
            min_value=1,
            max_value=5,
            value=1,
            help="Condiciones ambientales adversas"
        )
    
    with col2:
        mide_orientacion = st.number_input(
            "Orientación",
            min_value=1,
            max_value=5,
            value=2,
            help="Dificultad para orientarse"
        )
    
    with col3:
        mide_desplazamiento = st.number_input(
            "Dificultad Desplazamiento",
            min_value=1,
            max_value=5,
            value=2,
            help="Dificultad del terreno"
        )
    
    with col4:
        mide_esfuerzo = st.number_input(
            "Esfuerzo Necesario",
            min_value=1,
            max_value=5,
            value=2,
            help="Esfuerzo físico requerido"
        )

# ==================== TAB 3: DESCRIPCIÓN ====================
with tab3:
    st.header("Descripción y Contenidos")
    
    st.subheader("Descripción del Sendero")
    st.caption("Escribe 3-4 párrafos describiendo la ruta")
    
    parrafo1 = st.text_area(
        "Párrafo 1: Introducción",
        value="Este sendero circular comienza en el Centro de Interpretación...",
        height=100,
        help="Introduce la ruta, distancia, tipo y punto de inicio"
    )
    
    parrafo2 = st.text_area(
        "Párrafo 2: Descripción del recorrido",
        value="El recorrido transcurre por caminos vecinales y sendas entre campos de cultivo...",
        height=100,
        help="Describe el trazado, paisajes y elementos arquitectónicos"
    )
    
    parrafo3 = st.text_area(
        "Párrafo 3: Vegetación y vistas",
        value="La vegetación predominante son las encinas, con miradores panorámicos...",
        height=100,
        help="Menciona la flora y los puntos con mejores vistas"
    )
    
    parrafo4 = st.text_area(
        "Párrafo 4: Fauna",
        value="En cuanto a fauna, es posible avistar buitres leonados y mirlo acuático...",
        height=100,
        help="Describe la fauna característica de la zona"
    )
    
    st.divider()
    st.subheader("Recomendaciones")
    
    recomendaciones = st.text_area(
        "Texto de Recomendaciones",
        value="Se recomienda evitar los meses de verano por las altas temperaturas. Precaución al cruzar la carretera CM-1003.",
        height=80,
        help="Advertencias importantes para los senderistas"
    )
    
    st.divider()
    st.subheader("Hitos del Recorrido (para el perfil)")
    st.caption("Puntos destacados que aparecerán etiquetados en el perfil de elevación")
    
    col1, col2 = st.columns(2)
    with col1:
        hito1 = st.text_input("Hito 1", value="INICIO DE RUTA (C.I.N.)")
        hito2 = st.text_input("Hito 2", value="MIRABUENO")
    with col2:
        hito3 = st.text_input("Hito 3", value="ARAGOSA")
        hito4 = st.text_input("Hito 4", value="FINAL DE RUTA")

# ==================== TAB 4: IMÁGENES ====================
with tab4:
    st.header("Imágenes y Mapas")
    
    st.markdown("""
    <div class="info-box">
        <strong>ℹ️ Información:</strong> Las imágenes con asterisco (*) son obligatorias.
        El diseño final es horizontal (landscape). Formatos: JPG, PNG.
    </div>
    """, unsafe_allow_html=True)
    
    # Foto Panorámica
    st.subheader("📸 Foto Panorámica / Banner")
    st.caption("Imagen panorámica que aparecerá en la parte superior de la PÁGINA 1")
    img_banner = st.file_uploader(
        "Sube la foto panorámica",
        type=['png', 'jpg', 'jpeg'],
        key="banner",
        help="Imagen panorámica del paisaje. Se añadirán etiquetas automáticamente."
    )
    if img_banner:
        st.image(img_banner, caption="Vista previa - Banner", use_container_width=True)
        imagenes['banner'] = img_banner
    
    st.divider()
    
    # Columnas para imágenes principales
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🗺️ Mapa Topográfico *")
        st.caption("Mapa con el trazado de la ruta (aparece en PÁGINA 2)")
        img_mapa = st.file_uploader(
            "Sube el mapa de la ruta",
            type=['png', 'jpg', 'jpeg'],
            key="mapa",
            help="Mapa topográfico con el recorrido marcado"
        )
        if img_mapa:
            st.image(img_mapa, caption="Vista previa - Mapa", use_container_width=True)
            imagenes['mapa'] = img_mapa
        else:
            st.warning("⚠️ Imagen obligatoria")
    
    with col2:
        st.subheader("📈 Perfil de Elevación *")
        st.caption("Gráfica del perfil altimétrico (aparece en PÁGINA 2)")
        img_perfil = st.file_uploader(
            "Sube el perfil de elevación",
            type=['png', 'jpg', 'jpeg'],
            key="perfil",
            help="Gráfico de área mostrando las variaciones de altitud"
        )
        if img_perfil:
            st.image(img_perfil, caption="Vista previa - Perfil", use_container_width=True)
            imagenes['perfil'] = img_perfil
        else:
            st.warning("⚠️ Imagen obligatoria")
    
    st.divider()
    
    # Tabla MIDE
    st.subheader("📊 Tabla MIDE *")
    st.caption("Imagen de la matriz MIDE con valores de dificultad")
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
    
    # Logo institucional
    st.subheader("🏛️ Logo Institucional (Opcional)")
    st.caption("Logo que aparecerá en la cabecera")
    img_logo = st.file_uploader(
        "Logo Castilla-La Mancha o del Parque",
        type=['png', 'jpg', 'jpeg'],
        key="logo"
    )
    if img_logo:
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.image(img_logo, caption="Vista previa - Logo", width=200)
        imagenes['logo'] = img_logo

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
        telefono_emergencias = st.text_input(
            "Teléfono Emergencias",
            value=st.session_state.plantilla['telefono_emergencias']
        )
    
    st.divider()
    st.subheader("🏛️ Datos Institucionales (Plantilla)")
    st.caption("Estos datos son comunes para todas las rutas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        entidad_promotora = st.text_input(
            "Entidad Promotora",
            value=st.session_state.plantilla['entidad_promotora']
        )
        
        parque_natural = st.text_input(
            "Parque Natural",
            value=st.session_state.plantilla['parque']
        )
    
    with col2:
        telefono_parque = st.text_input(
            "Teléfono del Parque",
            value=st.session_state.plantilla['telefono_parque']
        )
        
        red_senderos = st.text_input(
            "Red de Senderos",
            value=st.session_state.plantilla['red_senderos']
        )
    
    st.divider()
    
    st.subheader("📋 Consejos para 'Disfruta del Parque'")
    st.caption("Aparecerán en la sección inferior de la PÁGINA 2")
    
    consejos_predefinidos = st.text_area(
        "Consejos",
        value="• Lleva prismáticos para observar fauna\n• Respeta el silencio del entorno\n• No enciendas fuego\n• Llévate toda tu basura",
        height=120
    )
    
    if st.button("💾 Guardar Configuración de Plantilla", type="secondary"):
        st.session_state.plantilla = {
            'entidad_promotora': entidad_promotora,
            'parque': parque_natural,
            'telefono_parque': telefono_parque,
            'telefono_emergencias': telefono_emergencias,
            'red_senderos': red_senderos,
            'web_institucional': url_qr
        }
        st.success("✅ Configuración guardada correctamente")

# ==================== GENERACIÓN DEL PDF (LANDSCAPE - 2 PÁGINAS) ====================
class PDF_Landscape(FPDF):
    def __init__(self, datos):
        super().__init__(orientation='L', unit='mm', format='A4')  # Landscape
        self.datos = datos
        self.set_auto_page_break(False)
    
    def pagina_1_informativa(self, imgs):
        """PÁGINA 1: Cara informativa con descripción y foto panorámica"""
        self.add_page()
        
        # Color verde corporativo
        verde = (0, 122, 51)  # #007A33
        
        # 1. CABECERA CON LOGO (si existe)
        if imgs.get('logo'):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                tmp.write(imgs['logo'].getvalue())
                self.image(tmp.name, x=10, y=5, h=15)
                os.remove(tmp.name)
        
        # Texto institucional en cabecera
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(100, 100, 100)
        self.set_xy(200, 8)
        self.cell(0, 4, self.datos.get('entidad_promotora', ''), align='R')
        self.set_xy(200, 12)
        self.cell(0, 4, self.datos.get('parque_natural', ''), align='R')
        
        # 2. FOTO PANORÁMICA CON ETIQUETA VERTICAL
        y_banner = 25
        if imgs.get('banner'):
            # Etiqueta vertical izquierda
            mirador = self.datos.get('mirador_nombre', 'MIRADOR DEL PICO')
            if mirador:
                self.set_fill_color(*verde)
                self.rect(10, y_banner, 15, 80, 'F')
                self.set_font('Helvetica', 'B', 10)
                self.set_text_color(255, 255, 255)
                self.set_xy(10, y_banner + 40)
                self.rotate(90, 17.5, y_banner + 40)
                self.cell(0, 0, mirador, align='C')
                self.rotate(0)
            
            # Imagen panorámica
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                tmp.write(imgs['banner'].getvalue())
                self.image(tmp.name, x=28, y=y_banner, w=259, h=80)
                os.remove(tmp.name)
            
            # Etiquetas de lugares de interés (simuladas como texto sobre la imagen)
            self.set_font('Helvetica', 'B', 7)
            self.set_text_color(255, 255, 255)
            lugares = self.datos.get('lugares_interes', '').split(',')
            x_pos = 40
            for lugar in lugares[:3]:  # Máximo 3 etiquetas
                self.set_xy(x_pos, y_banner + 5)
                self.set_fill_color(0, 0, 0, 150)  # Fondo semi-transparente
                self.cell(0, 5, lugar.strip(), fill=False)
                x_pos += 80
        
        # 3. TÍTULO PRINCIPAL
        y_titulo = 110
        self.set_font('Helvetica', 'B', 28)
        self.set_text_color(*verde)
        self.set_xy(15, y_titulo)
        self.cell(0, 10, self.datos.get('codigo_ruta', ''))
        
        self.set_font('Helvetica', 'B', 14)
        self.set_xy(15, y_titulo + 12)
        self.cell(0, 7, f"SENDERO {self.datos.get('nombre_sendero', '')}")
        
        # 4. COLUMNA DE TEXTO - DESCRIPCIÓN (4 párrafos)
        y_texto = y_titulo + 25
        self.set_font('Helvetica', '', 9)
        self.set_text_color(0, 0, 0)
        
        ancho_columna = 180
        
        for i, parrafo in enumerate([
            self.datos.get('parrafo1', ''),
            self.datos.get('parrafo2', ''),
            self.datos.get('parrafo3', ''),
            self.datos.get('parrafo4', '')
        ]):
            self.set_xy(15, y_texto)
            self.multi_cell(ancho_columna, 4, parrafo, align='J')
            y_texto = self.get_y() + 2
        
        # 5. BLOQUE DE RECOMENDACIONES (Inferior)
        y_recom = 185
        self.set_fill_color(255, 243, 205)  # Fondo amarillo claro
        self.rect(15, y_recom, ancho_columna, 15, 'F')
        
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(*verde)
        self.set_xy(17, y_recom + 2)
        self.cell(0, 5, 'RECOMENDACIONES')
        
        self.set_font('Helvetica', '', 8)
        self.set_text_color(0, 0, 0)
        self.set_xy(17, y_recom + 7)
        self.multi_cell(ancho_columna - 4, 3.5, self.datos.get('recomendaciones', ''))
        
        # PIE DE PÁGINA
        self.set_y(-10)
        self.set_font('Helvetica', 'I', 7)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, f'Generado el {datetime.now().strftime("%d/%m/%Y")}', align='C')
    
    def pagina_2_tecnica(self, imgs):
        """PÁGINA 2: Mapa, perfil, ficha técnica y datos adicionales"""
        self.add_page()
        
        verde = (0, 122, 51)
        
        # 1. MAPA TOPOGRÁFICO (Superior Izquierdo - 60% del ancho)
        if imgs.get('mapa'):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                tmp.write(imgs['mapa'].getvalue())
                self.image(tmp.name, x=10, y=10, w=180, h=110)
                os.remove(tmp.name)
        
        # 2. PERFIL DE ELEVACIÓN (Centro - Debajo del mapa)
        y_perfil = 125
        if imgs.get('perfil'):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                tmp.write(imgs['perfil'].getvalue())
                self.image(tmp.name, x=10, y=y_perfil, w=180, h=45)
                os.remove(tmp.name)
        
        # 3. PANEL LATERAL DERECHO - FICHA TÉCNICA
        x_panel = 195
        y_panel = 10
        ancho_panel = 92
        
        # Título del panel
        self.set_fill_color(*verde)
        self.rect(x_panel, y_panel, ancho_panel, 8, 'F')
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(255, 255, 255)
        self.set_xy(x_panel, y_panel + 2)
        self.cell(ancho_panel, 5, 'FICHA TÉCNICA', align='C')
        
        # Datos técnicos en tabla
        y_datos = y_panel + 12
        self.set_fill_color(245, 245, 245)
        self.rect(x_panel, y_datos, ancho_panel, 35, 'F')
        
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(0, 0, 0)
        
        datos_lista = [
            ('Horario:', self.datos.get('tiempo', '')),
            ('Distancia:', self.datos.get('distancia', '')),
            ('Desnivel Subida:', self.datos.get('desnivel_subida', '')),
            ('Desnivel Bajada:', self.datos.get('desnivel_bajada', '')),
            ('Tipo:', self.datos.get('tipo_ruta', ''))
        ]
        
        y_item = y_datos + 3
        for etiqueta, valor in datos_lista:
            self.set_xy(x_panel + 3, y_item)
            self.set_font('Helvetica', 'B', 8)
            self.cell(35, 5, etiqueta, align='L')
            self.set_font('Helvetica', '', 8)
            self.cell(0, 5, valor, align='L')
            y_item += 6
        
        # 4. IMAGEN MIDE
        y_mide = y_datos + 40
        if imgs.get('mide'):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                tmp.write(imgs['mide'].getvalue())
                self.image(tmp.name, x=x_panel, y=y_mide, w=ancho_panel)
                os.remove(tmp.name)
            y_mide += 35
        
        # 5. SECCIÓN SEÑALIZACIÓN
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(*verde)
        self.set_xy(x_panel, y_mide + 5)
        self.cell(0, 5, 'SEÑALIZACIÓN')
        
        self.set_font('Helvetica', '', 7)
        self.set_text_color(0, 0, 0)
        self.set_xy(x_panel, y_mide + 11)
        self.multi_cell(ancho_panel, 3, 'Marcas blancas y amarillas:\n• Continuidad\n• Cambio de dirección\n• Dirección equivocada')
        
        # 6. SECCIÓN DISFRUTA DEL PARQUE
        y_consejos = y_mide + 28
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(*verde)
        self.set_xy(x_panel, y_consejos)
        self.cell(0, 5, 'DISFRUTA DEL PARQUE')
        
        self.set_font('Helvetica', '', 7)
        self.set_text_color(0, 0, 0)
        self.set_xy(x_panel, y_consejos + 6)
        self.multi_cell(ancho_panel, 3, self.datos.get('consejos_disfruta', ''))
        
        # 7. TELÉFONOS DE INTERÉS Y QR
        y_telefonos = y_consejos + 28
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(*verde)
        self.set_xy(x_panel, y_telefonos)
        self.cell(0, 5, 'TELÉFONOS DE INTERÉS')
        
        self.set_font('Helvetica', '', 8)
        self.set_text_color(0, 0, 0)
        self.set_xy(x_panel, y_telefonos + 6)
        self.cell(0, 4, f"Emergencias: {self.datos.get('telefono_emergencias', '112')}")
        self.set_xy(x_panel, y_telefonos + 11)
        self.cell(0, 4, f"Parque: {self.datos.get('telefono_parque', '')}")
        
        # Código QR
        if self.datos.get('url_qr'):
            qr = qrcode.QRCode(box_size=8, border=1)
            qr.add_data(self.datos['url_qr'])
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")
            
            qr_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            qr_img.save(qr_path.name)
            
            self.image(qr_path.name, x=x_panel + 30, y=y_telefonos + 18, w=25)
            os.remove(qr_path.name)
            
            self.set_font('Helvetica', 'I', 6)
            self.set_xy(x_panel, y_telefonos + 45)
            self.multi_cell(ancho_panel, 2.5, self.datos.get('url_qr', ''), align='C')

def crear_pdf_topoguia(datos, imgs):
    """Genera el PDF de la topoguía en formato landscape de 2 páginas"""
    pdf = PDF_Landscape(datos)
    
    # Página 1: Informativa
    pdf.pagina_1_informativa(imgs)
    
    # Página 2: Técnica
    pdf.pagina_2_tecnica(imgs)
    
    return pdf.output()

# ==================== BARRA LATERAL Y GENERACIÓN ====================
st.sidebar.header("🎯 Acciones")

# Resumen
st.sidebar.subheader("📊 Resumen")
st.sidebar.write(f"**Usuario:** {username}")
st.sidebar.write(f"**Ruta:** {codigo_ruta if 'codigo_ruta' in locals() else 'Sin definir'}")
st.sidebar.write(f"**Nombre:** {nombre_sendero[:25] if 'nombre_sendero' in locals() and nombre_sendero else 'Sin definir'}...")

# Validación
datos_formulario = {
    'codigo_ruta': codigo_ruta if 'codigo_ruta' in locals() else '',
    'nombre_sendero': nombre_sendero if 'nombre_sendero' in locals() else '',
    'distancia': distancia if 'distancia' in locals() else '',
    'tiempo': tiempo if 'tiempo' in locals() else '',
    'desnivel_subida': desnivel_subida if 'desnivel_subida' in locals() else '',
    'desnivel_bajada': desnivel_bajada if 'desnivel_bajada' in locals() else '',
    'tipo_ruta': tipo_ruta if 'tipo_ruta' in locals() else '',
    'lugares_interes': lugares_interes if 'lugares_interes' in locals() else '',
    'mirador_nombre': mirador_nombre if 'mirador_nombre' in locals() else '',
    'parrafo1': parrafo1 if 'parrafo1' in locals() else '',
    'parrafo2': parrafo2 if 'parrafo2' in locals() else '',
    'parrafo3': parrafo3 if 'parrafo3' in locals() else '',
    'parrafo4': parrafo4 if 'parrafo4' in locals() else '',
    'recomendaciones': recomendaciones if 'recomendaciones' in locals() else '',
    'consejos_disfruta': consejos_predefinidos if 'consejos_predefinidos' in locals() else '',
    'url_qr': url_qr if 'url_qr' in locals() else '',
    'telefono_emergencias': telefono_emergencias if 'telefono_emergencias' in locals() else '',
    'telefono_parque': telefono_parque if 'telefono_parque' in locals() else '',
    'entidad_promotora': entidad_promotora if 'entidad_promotora' in locals() else '',
    'parque_natural': parque_natural if 'parque_natural' in locals() else '',
}

errores = validar_campos(datos_formulario, imagenes)

if errores:
    st.sidebar.error(f"⚠️ Faltan {len(errores)} campo(s):")
    for error in errores[:5]:  # Mostrar máximo 5
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
            with st.spinner("Generando PDF en formato horizontal (2 páginas)..."):
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
                
                st.info("📄 El PDF tiene 2 páginas:\n- **Página 1**: Descripción y foto panorámica\n- **Página 2**: Mapa, perfil y ficha técnica")
        except Exception as e:
            st.error(f"❌ Error al generar el PDF: {str(e)}")
            st.exception(e)
