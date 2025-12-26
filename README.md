# 🏔️ Generador de Topoguías PR-GU

Aplicación web para generar folletos de topoguías de senderos en el estilo oficial de la Red de Senderos de Guadalajara (PR-GU).

## 📋 Características

- **Sistema de autenticación**: Login seguro con usuarios y contraseñas encriptadas
- **Interfaz intuitiva** con pestañas organizadas para facilitar la introducción de datos
- **Generación automática de PDF** con diseño profesional en formato horizontal (2 páginas)
- **Diseño fiel al original**: Replica exacta del estilo PR-GU oficial
- **Campos personalizables** para cada ruta
- **Plantilla institucional** con datos genéricos reutilizables
- **Soporte para múltiples imágenes**: mapa, perfil, MIDE, foto panorámica, logo
- **Código QR automático** para enlaces web
- **Validación de campos** obligatorios
- **Vista previa de imágenes** antes de generar el PDF
- **Multi-usuario**: Cada usuario puede acceder con su propia cuenta

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clona el repositorio**

```bash
git clone https://github.com/tu-usuario/generador-topoguias.git
cd generador-topoguias
```

2. **Crea un entorno virtual (recomendado)**

```bash
python -m venv venv

# En Windows
venv\Scripts\activate

# En Linux/Mac
source venv/bin/activate
```

3. **Instala las dependencias**

```bash
pip install -r requirements.txt
```

4. **Ejecuta la aplicación**

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

5. **Credenciales por defecto**

La aplicación viene con dos usuarios de prueba:
- **Admin**: Usuario: `admin` | Contraseña: `admin123`
- **Demo**: Usuario: `usuario1` | Contraseña: `demo123`

### Gestión de Usuarios

Para añadir o modificar usuarios:

1. **Genera un hash de contraseña**:
```bash
python generate_passwords.py
```

2. **Edita el archivo `config.yaml`** y añade el nuevo usuario:
```yaml
credentials:
  usernames:
    nuevo_usuario:
      email: nuevo@example.com
      name: Nombre Completo
      password: [hash generado]
```

3. Reinicia la aplicación

## 📖 Uso

### Login

1. Accede a la aplicación
2. Introduce tu usuario y contraseña
3. Click en "Login"

### 1. Datos Básicos
- Introduce el código de ruta (ej: PR-GU 08)
- Nombre del sendero
- Punto de inicio y coordenadas GPS
- Lugares de interés que aparecerán etiquetados
- Nombre del mirador principal

### 2. Ficha Técnica y MIDE
- Distancia total y tiempo estimado
- Desniveles de subida y bajada
- Tipo de ruta y rango de altitud
- **Valores MIDE**: Severidad, Orientación, Dificultad, Esfuerzo (1-5)

### 3. Descripción
- **4 párrafos personalizables**:
  - Párrafo 1: Introducción
  - Párrafo 2: Descripción del recorrido
  - Párrafo 3: Vegetación y vistas
  - Párrafo 4: Fauna
- Texto de recomendaciones
- Hitos del recorrido (para etiquetar el perfil)

### 4. Imágenes
Sube las siguientes imágenes (**obligatorias las marcadas con ***):
- Foto panorámica/banner (opcional) - Aparece en PÁGINA 1
- **Mapa de ruta*** - Aparece en PÁGINA 2, zona superior izquierda
- **Perfil de elevación*** - Aparece en PÁGINA 2, zona central
- **Tabla MIDE*** - Aparece en PÁGINA 2, panel lateral derecho
- Logo institucional (opcional) - Aparece en cabecera

### 5. Configuración
- URL para código QR
- Teléfonos de contacto y emergencias
- Datos institucionales (plantilla genérica)
- Consejos para "Disfruta del Parque"

### 6. Generar PDF
- Revisa el resumen en la barra lateral
- Verifica que todos los campos obligatorios estén completos
- Haz clic en "GENERAR PDF"
- Descarga el archivo generado

**El PDF generado tendrá 2 páginas en formato horizontal:**
- **PÁGINA 1**: Foto panorámica, descripción completa (4 párrafos) y recomendaciones
- **PÁGINA 2**: Mapa topográfico, perfil de elevación, ficha técnica, valores MIDE, señalización, teléfonos y QR

## 📁 Estructura del Proyecto

```
generador-topoguias/
│
├── app.py                    # Aplicación principal de Streamlit
├── config.yaml               # Configuración de usuarios
├── generate_passwords.py     # Script para generar contraseñas
├── requirements.txt          # Dependencias del proyecto
├── README.md                # Este archivo
├── .gitignore               # Archivos a ignorar por Git
│
├── .streamlit/              # Configuración de Streamlit
│   └── config.toml
│
└── ejemplos/                # Carpeta con ejemplos (opcional)
    ├── ejemplo_mapa.jpg
    ├── ejemplo_perfil.jpg
    ├── ejemplo_mide.png
    └── ejemplo_banner.jpg
```

## 🎨 Personalización

### Colores Institucionales

Los colores del diseño pueden personalizarse en la clase `PDF` dentro de `app.py`:

```python
# Franja verde superior
self.set_fill_color(45, 80, 22)  # RGB
```

### Plantilla de Datos Genéricos

Edita la función `cargar_plantilla()` en `app.py` para cambiar los valores por defecto:

```python
def cargar_plantilla():
    return {
        'entidad_promotora': 'Tu Entidad',
        'red_senderos': 'Tu Red de Senderos',
        'homologacion': 'Tu Organismo',
        'web_institucional': 'https://tu-web.com'
    }
```

## 🔒 Seguridad

### Gestión de Contraseñas

- Las contraseñas se almacenan hasheadas con bcrypt
- **IMPORTANTE**: Cambia las contraseñas por defecto antes de desplegar en producción
- El archivo `config.yaml` NO debe subirse a repositorios públicos
- Añade `config.yaml` a `.gitignore` si contiene datos sensibles

### Configuración de Cookies

Edita los parámetros de cookies en `config.yaml`:

```yaml
cookie:
  expiry_days: 30              # Días antes de expirar la sesión
  key: tu_clave_secreta_única  # Cambia esto por una clave única
  name: topoguias_auth_cookie
```

**¡IMPORTANTE!**: Genera una clave única para `key` en producción:

```python
import secrets
print(secrets.token_hex(32))
```

### Usuarios Preautorizados

Puedes definir emails que podrán registrarse automáticamente:

```yaml
preauthorized:
  emails:
  - usuario@permitido.com
  - otro@permitido.com
```

## 🔧 Tecnologías Utilizadas

- **Streamlit**: Framework para aplicaciones web interactivas
- **streamlit-authenticator**: Sistema de autenticación seguro
- **FPDF2**: Generación de documentos PDF
- **qrcode**: Creación de códigos QR
- **Pillow**: Procesamiento de imágenes
- **PyYAML**: Gestión de configuración de usuarios

## 📝 Formatos de Imagen Soportados

- JPG / JPEG
- PNG

**Tamaño recomendado**: Máximo 5MB por imagen

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 👥 Autores

- Tu Nombre - [@tu-usuario](https://github.com/tu-usuario)

## 🙏 Agradecimientos

- Junta de Comunidades de Castilla-La Mancha
- Federación de Montañismo
- Red de Senderos de Guadalajara

## 📞 Soporte

Si encuentras algún problema o tienes sugerencias:

- Abre un [Issue](https://github.com/tu-usuario/generador-topoguias/issues)
- Contacta: tuemail@ejemplo.com

## 🔄 Actualizaciones

### Versión 2.0.0 (Actual)
- ✨ Sistema de autenticación multi-usuario
- ✨ Diseño PDF horizontal (landscape) de 2 páginas
- ✨ Replica exacta del formato oficial PR-GU
- ✨ Página 1: Descripción completa con foto panorámica
- ✨ Página 2: Mapa, perfil, ficha técnica completa
- ✨ Etiquetado automático de lugares de interés
- ✨ Panel lateral con MIDE, señalización y contactos
- ✨ Código QR integrado

### Versión 1.0.0
- Lanzamiento inicial
- Sistema básico de generación de topoguías
- Interfaz con pestañas
- Validación de campos

---

**Nota**: Esta aplicación está diseñada específicamente para generar topoguías en el formato PR-GU de Guadalajara, pero puede adaptarse fácilmente para otras redes de senderos.
