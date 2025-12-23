# 🚀 Guía de Deployment

Esta guía te ayudará a desplegar la aplicación "Generador de Topoguías" en diferentes plataformas.

## 📦 Opciones de Deployment

### 1. Streamlit Community Cloud (Recomendado - GRATIS)

La forma más sencilla y gratuita de desplegar tu aplicación Streamlit.

#### Pasos:

1. **Sube tu código a GitHub** (si aún no lo has hecho)
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/tu-usuario/generador-topoguias.git
   git push -u origin main
   ```

2. **Regístrate en Streamlit Cloud**
   - Ve a [share.streamlit.io](https://share.streamlit.io)
   - Inicia sesión con tu cuenta de GitHub
   - Haz clic en "New app"

3. **Configura tu app**
   - Repository: `tu-usuario/generador-topoguias`
   - Branch: `main`
   - Main file path: `app.py`
   - Haz clic en "Deploy!"

4. **¡Listo!** Tu app estará disponible en una URL como:
   `https://tu-usuario-generador-topoguias.streamlit.app`

#### Ventajas:
- ✅ Completamente gratis
- ✅ Deployment automático desde GitHub
- ✅ HTTPS incluido
- ✅ Actualizaciones automáticas al hacer push

---

### 2. Render (Alternativa Gratuita)

#### Pasos:

1. Crea una cuenta en [render.com](https://render.com)

2. Crea un nuevo "Web Service"

3. Conecta tu repositorio de GitHub

4. Configura el servicio:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

5. Añade variables de entorno (si es necesario)

6. Haz clic en "Create Web Service"

#### Ventajas:
- ✅ Plan gratuito disponible
- ✅ Fácil configuración
- ✅ Soporte para múltiples frameworks

---

### 3. Heroku

#### Pasos:

1. Instala Heroku CLI
   ```bash
   # En Windows (con Chocolatey)
   choco install heroku-cli
   
   # En Mac
   brew tap heroku/brew && brew install heroku
   
   # En Linux
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. Crea archivos adicionales:

   **Procfile**:
   ```
   web: sh setup.sh && streamlit run app.py
   ```

   **setup.sh**:
   ```bash
   mkdir -p ~/.streamlit/
   
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

3. Despliega:
   ```bash
   heroku login
   heroku create nombre-de-tu-app
   git push heroku main
   heroku open
   ```

---

### 4. Docker (Para Despliegue en Servidor Propio)

#### Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Comandos:

```bash
# Construir imagen
docker build -t topoguias-generator .

# Ejecutar contenedor
docker run -p 8501:8501 topoguias-generator
```

#### docker-compose.yml:

```yaml
version: '3.8'

services:
  streamlit:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

---

### 5. VPS / Servidor Propio (Ubuntu/Debian)

#### Pasos:

1. **Conecta a tu servidor**
   ```bash
   ssh usuario@tu-servidor.com
   ```

2. **Instala dependencias**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv nginx -y
   ```

3. **Clona tu repositorio**
   ```bash
   git clone https://github.com/tu-usuario/generador-topoguias.git
   cd generador-topoguias
   ```

4. **Configura entorno virtual**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Crea servicio systemd**
   
   `/etc/systemd/system/topoguias.service`:
   ```ini
   [Unit]
   Description=Generador de Topoguías
   After=network.target

   [Service]
   User=tu-usuario
   WorkingDirectory=/home/tu-usuario/generador-topoguias
   Environment="PATH=/home/tu-usuario/generador-topoguias/venv/bin"
   ExecStart=/home/tu-usuario/generador-topoguias/venv/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0

   [Install]
   WantedBy=multi-user.target
   ```

6. **Inicia el servicio**
   ```bash
   sudo systemctl enable topoguias
   sudo systemctl start topoguias
   sudo systemctl status topoguias
   ```

7. **Configura Nginx como proxy reverso**
   
   `/etc/nginx/sites-available/topoguias`:
   ```nginx
   server {
       listen 80;
       server_name tu-dominio.com;

       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

8. **Activa el sitio**
   ```bash
   sudo ln -s /etc/nginx/sites-available/topoguias /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

9. **Configura SSL con Let's Encrypt (opcional pero recomendado)**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d tu-dominio.com
   ```

---

## 🔒 Seguridad

### Variables de Entorno

Si necesitas guardar información sensible, usa variables de entorno:

```python
import os

# En app.py
api_key = os.getenv('API_KEY', 'default_value')
```

En Streamlit Cloud: Settings → Secrets

En otros servicios: Variables de entorno en configuración

### Autenticación (Opcional)

Para añadir autenticación básica:

```python
import streamlit as st

def check_password():
    def password_entered():
        if st.session_state["password"] == "tu_contraseña_segura":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("😕 Password incorrect")
        return False
    else:
        return True

if check_password():
    # Tu aplicación aquí
    pass
```

---

## 📊 Monitoreo

### Logs en Streamlit Cloud
- Ve a tu app en Streamlit Cloud
- Haz clic en "Manage app"
- Ve a la pestaña "Logs"

### Logs en servidor propio
```bash
# Ver logs del servicio
sudo journalctl -u topoguias -f

# Ver logs de Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

---

## 🔄 Actualizaciones

### Streamlit Cloud
- Simplemente haz `git push` a tu repositorio
- La app se actualizará automáticamente

### Servidor Propio
```bash
cd /ruta/a/generador-topoguias
git pull
sudo systemctl restart topoguias
```

---

## ⚡ Optimización

### Caché de Streamlit
Usa el decorador `@st.cache_data` para funciones costosas:

```python
@st.cache_data
def cargar_plantilla():
    # código costoso
    return datos
```

### Compresión de Imágenes
Para mejorar el rendimiento con imágenes grandes:

```python
from PIL import Image

def comprimir_imagen(imagen, max_size=(1920, 1080)):
    img = Image.open(imagen)
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    return img
```

---

## 🆘 Troubleshooting

### Error: "ModuleNotFoundError"
```bash
pip install -r requirements.txt --upgrade
```

### Error: Puerto ya en uso
```bash
# Cambiar puerto
streamlit run app.py --server.port=8502
```

### Error de memoria en deployment
- Optimiza tamaño de imágenes
- Usa caché de Streamlit
- Considera upgrade del plan (si es servicio de pago)

---

## 📞 Soporte

Si tienes problemas con el deployment:
1. Revisa los logs de la plataforma
2. Verifica que `requirements.txt` esté actualizado
3. Asegúrate de que Python 3.8+ esté instalado
4. Abre un issue en GitHub con detalles del error

---

**¡Tu aplicación está lista para el mundo!** 🎉
