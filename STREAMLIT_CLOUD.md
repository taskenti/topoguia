# 🌐 Configuración para Streamlit Cloud

## 📋 Pasos para Desplegar en Streamlit Cloud

### 1. Preparar el Repositorio

Asegúrate de tener estos archivos en tu repositorio:

```
generador-topoguias/
├── app.py
├── requirements.txt
├── packages.txt (opcional)
├── .streamlit/
│   └── config.toml
└── config.yaml (se creará automáticamente si no existe)
```

### 2. Subir a GitHub

```bash
git add .
git commit -m "Deploy to Streamlit Cloud"
git push origin main
```

### 3. Desplegar en Streamlit Cloud

1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Haz login con tu cuenta de GitHub
3. Click en "New app"
4. Selecciona:
   - **Repository**: tu-usuario/generador-topoguias
   - **Branch**: main
   - **Main file path**: app.py
5. Click "Deploy!"

### 4. Configurar Secrets (Opcional pero Recomendado)

Para mayor seguridad, puedes usar Streamlit Secrets en lugar de `config.yaml`:

1. En tu app desplegada, haz click en **"Settings"** (esquina superior derecha)
2. Ve a **"Secrets"**
3. Añade el contenido de tu `config.yaml`:

```toml
# .streamlit/secrets.toml

[credentials.usernames.admin]
email = "admin@topoguias.es"
name = "Administrador"
password = "$2b$12$KIXqvB5pJH8yGmK6pZ4aEOqN7xGx1tZ4y3rJ8c5d6f7g8h9i0j1k2"

[credentials.usernames.usuario1]
email = "usuario1@example.com"
name = "Usuario Demo"
password = "$2b$12$KIXqvB5pJH8yGmK6pZ4aEOqN7xGx1tZ4y3rJ8c5d6f7g8h9i0j1k2"

[cookie]
expiry_days = 30
key = "TU_CLAVE_UNICA_AQUI_12345_CAMBIAR"
name = "topoguias_auth_cookie"
```

4. Modifica `app.py` para usar secrets (opcional):

```python
# Opción 1: Usar config.yaml (actual)
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Opción 2: Usar Streamlit Secrets (más seguro en cloud)
# config = dict(st.secrets)
```

## 🔑 Credenciales por Defecto

```
Usuario: admin
Password: admin123

Usuario: usuario1
Password: demo123
```

**⚠️ IMPORTANTE**: Cambia estas contraseñas antes de usar en producción.

## 🔒 Cambiar Contraseñas en Streamlit Cloud

1. **Genera nuevos hashes localmente**:
```bash
python generate_passwords.py
```

2. **Copia los hashes generados**

3. **Actualiza Secrets en Streamlit Cloud**:
   - Settings → Secrets
   - Reemplaza los valores de `password`

4. **Guarda y reinicia** la app

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError"

**Solución**: Verifica que `requirements.txt` esté en la raíz del repo.

### Error: "config.yaml not found"

**Solución**: La app creará uno automáticamente. Si no:
1. Crea el archivo manualmente en el repo
2. O usa Streamlit Secrets

### Error: "streamlit-authenticator" no funciona

**Solución**: Actualiza la versión en requirements.txt:
```
streamlit-authenticator>=0.3.0
```

### La app está muy lenta

**Solución**: 
- Optimiza las imágenes antes de subirlas
- Reduce el tamaño máximo de upload en config.toml
- Considera usar Streamlit Cloud Pro

### Error al generar PDF

**Solución**:
- Verifica que las imágenes sean JPG o PNG
- Comprueba que no excedan 5MB
- Asegúrate de que fpdf2 esté instalado correctamente

## 📊 Límites de Streamlit Cloud (Plan Gratuito)

- **CPU**: Compartida
- **RAM**: 1 GB
- **Storage**: 50 MB
- **Concurrent users**: 1 (otros esperan en cola)

Para más usuarios simultáneos, considera [Streamlit Cloud Pro](https://streamlit.io/cloud).

## 🔄 Actualizar la App

Cada vez que hagas `git push` a tu repo, la app se actualizará automáticamente en Streamlit Cloud.

```bash
# Hacer cambios en app.py
git add .
git commit -m "Actualización: descripción del cambio"
git push origin main

# La app se redesplegará automáticamente
```

## 📱 Compartir tu App

Tu app estará disponible en una URL como:

```
https://tu-usuario-generador-topoguias.streamlit.app
```

Puedes compartir esta URL con quien quieras. Los usuarios necesitarán:
- Usuario y contraseña que hayas configurado
- Navegador moderno (Chrome, Firefox, Safari)

## 🎨 Personalizar URL

1. Ve a Settings → General
2. Cambia "App URL" (sujeto a disponibilidad)
3. Guarda cambios

## 📈 Ver Logs y Estadísticas

1. Click en "Manage app" (esquina inferior derecha)
2. Pestaña **"Logs"**: Ver errores y mensajes
3. Pestaña **"Analytics"**: Uso y tráfico (solo Pro)

## 🔐 Seguridad en Producción

✅ **Hacer**:
- Cambiar todas las contraseñas por defecto
- Usar una clave de cookie única
- Actualizar usuarios y permisos regularmente
- Monitorear los logs

❌ **No hacer**:
- Compartir contraseñas en texto plano
- Dejar usuarios de prueba activos
- Usar la configuración por defecto en producción

## 💰 Upgrade a Pro (Opcional)

Si necesitas:
- Más usuarios concurrentes
- Más recursos (CPU/RAM)
- Dominios personalizados
- Analytics avanzado
- Soporte prioritario

Considera [Streamlit Cloud Pro](https://streamlit.io/cloud).

## 📞 Soporte

- 📖 [Docs oficiales Streamlit](https://docs.streamlit.io)
- 💬 [Foro de Streamlit](https://discuss.streamlit.io)
- 🐛 [Issues del proyecto](https://github.com/tu-usuario/generador-topoguias/issues)

---

**¡Tu app está lista para el mundo!** 🚀
