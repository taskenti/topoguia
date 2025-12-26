# 🚀 Quick Start - Inicio Rápido

Guía rápida para poner en marcha el Generador de Topoguías en 5 minutos.

## ⚡ Instalación Express

```bash
# 1. Clonar repositorio
git clone https://github.com/tu-usuario/generador-topoguias.git
cd generador-topoguias

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Ejecutar
streamlit run app.py
```

## 🔑 Credenciales por Defecto

```
Usuario: admin
Contraseña: admin123

Usuario: usuario1
Contraseña: demo123
```

## 📝 Flujo de Uso Rápido

1. **Login** con credenciales
2. **Datos Básicos**: Código PR-GU 08, nombre del sendero
3. **Ficha Técnica**: Distancia, tiempo, valores MIDE
4. **Descripción**: 4 párrafos sobre la ruta
5. **Imágenes**: Sube mapa, perfil y MIDE (obligatorios)
6. **Generar PDF** desde la barra lateral

## 📂 Archivos Necesarios

```
generador-topoguias/
├── app.py           ← Aplicación principal
├── config.yaml      ← Usuarios (crear si no existe)
├── requirements.txt ← Dependencias
└── .streamlit/
    └── config.toml  ← Configuración (crear carpeta)
```

## 🆕 Primera Configuración

### 1. Crear config.yaml

Crea un archivo `config.yaml` en la raíz con este contenido:

```yaml
credentials:
  usernames:
    admin:
      email: admin@topoguias.es
      name: Administrador
      password: $2b$12$KIXqvB5pJH8yGmK6pZ4aEOqN7xGx1tZ4y3rJ8c5d6f7g8h9i0j1k2

cookie:
  expiry_days: 30
  key: cambiar_esta_clave_en_produccion_12345
  name: topoguias_auth_cookie

preauthorized:
  emails: []
```

### 2. Crear carpeta .streamlit

```bash
mkdir .streamlit
```

Crea `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#007A33"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f9ff"

[server]
maxUploadSize = 10
```

## 🎯 Generar Tu Primera Topoguía

### Datos Mínimos Necesarios:

✅ Código de ruta (ej: PR-GU 08)
✅ Nombre del sendero
✅ Distancia y tiempo
✅ Imagen del mapa
✅ Imagen del perfil
✅ Imagen de tabla MIDE

### Flujo:

1. Login → admin / admin123
2. Pestaña "Datos Básicos":
   - Código: PR-GU 08
   - Nombre: MI PRIMERA RUTA
3. Pestaña "Ficha Técnica":
   - Distancia: 10 Km
   - Tiempo: 2h 30m
   - MIDE: Valores del 1 al 5
4. Pestaña "Descripción":
   - Escribe 3-4 párrafos
5. Pestaña "Imágenes":
   - Sube mapa, perfil y MIDE
6. Clic en "GENERAR PDF"

## 🔧 Solución Rápida de Problemas

### Error: "No module named 'streamlit_authenticator'"
```bash
pip install streamlit-authenticator
```

### Error: "config.yaml not found"
Crea el archivo `config.yaml` (ver arriba)

### Error: "Invalid binary data format"
Asegúrate de usar la última versión de fpdf2:
```bash
pip install --upgrade fpdf2
```

### El PDF no se ve bien
- Verifica que las imágenes sean JPG o PNG
- Comprueba que no sean mayores de 5MB
- Revisa que el mapa y perfil tengan buena resolución

## 📱 Acceso desde Otros Dispositivos

Una vez ejecutando en tu PC:

1. Mira la IP local:
```bash
# Windows
ipconfig
# Linux/Mac
ifconfig
```

2. Accede desde otro dispositivo en la misma red:
```
http://TU_IP_LOCAL:8501
```

## 🌐 Deploy Rápido en Internet

### Opción 1: Streamlit Cloud (GRATIS)

1. Sube tu código a GitHub
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Conecta tu repo
4. Deploy automático!

### Opción 2: Render

1. Crea cuenta en [render.com](https://render.com)
2. Conecta GitHub
3. Configura:
   - Build: `pip install -r requirements.txt`
   - Start: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

## 🔒 Seguridad Básica

Antes de poner en producción:

```bash
# 1. Generar nueva clave para cookies
python -c "import secrets; print(secrets.token_hex(32))"

# 2. Cambiar contraseñas
python generate_passwords.py

# 3. Actualizar config.yaml con nuevos datos
```

## 📚 Próximos Pasos

- Lee el [README.md](README.md) completo
- Revisa [USUARIOS.md](USUARIOS.md) para gestionar usuarios
- Consulta [DISEÑO_PDF.md](DISEÑO_PDF.md) para personalizar
- Mira [DEPLOYMENT.md](DEPLOYMENT.md) para opciones de hosting

## 💡 Consejos Útiles

1. **Guarda plantillas**: Configura los datos genéricos una vez en "Configuración"
2. **Prepara las imágenes**: Ten mapa, perfil y MIDE listos antes de empezar
3. **Usa buenos navegadores**: Chrome o Firefox funcionan mejor
4. **Prueba local primero**: Genera varios PDFs de prueba antes de compartir
5. **Documenta tus rutas**: Usa nombres descriptivos para los archivos PDF

## 🆘 ¿Necesitas Ayuda?

- 📖 [Documentación completa](README.md)
- 🐛 [Reportar bug](https://github.com/tu-usuario/generador-topoguias/issues)
- 💬 [Discusiones](https://github.com/tu-usuario/generador-topoguias/discussions)

---

**¡Listo!** Ya puedes generar topoguías profesionales. 🎉
