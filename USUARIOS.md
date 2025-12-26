# 👥 Guía de Gestión de Usuarios

Esta guía te explica cómo gestionar el sistema de usuarios de la aplicación.

## 📝 Estructura del archivo config.yaml

```yaml
credentials:
  usernames:
    nombre_usuario:
      email: email@ejemplo.com
      name: Nombre Completo
      password: $2b$12$hash_de_la_contraseña

cookie:
  expiry_days: 30
  key: clave_secreta_única_cambiar_en_produccion
  name: topoguias_auth_cookie

preauthorized:
  emails:
  - usuario@permitido.com
```

## 🔐 Añadir un Nuevo Usuario

### Método 1: Usando el script (Recomendado)

1. **Ejecuta el script de generación**:
```bash
python generate_passwords.py
```

2. **Elige opción personalizada** cuando te lo pida

3. **Copia el hash generado**

4. **Edita `config.yaml`** y añade:
```yaml
nuevo_usuario:
  email: nuevo@ejemplo.com
  name: Nombre Usuario
  password: [pegar hash aquí]
```

5. **Reinicia la aplicación**

### Método 2: Manualmente con Python

```python
import streamlit_authenticator as stauth

# Generar hash
hashed = stauth.Hasher(['tu_contraseña']).generate()[0]
print(hashed)
```

Copia el hash y añádelo a `config.yaml`.

## 🗑️ Eliminar un Usuario

Simplemente elimina su entrada del archivo `config.yaml`:

```yaml
# Eliminar todo este bloque
usuario_a_eliminar:
  email: ...
  name: ...
  password: ...
```

## 🔄 Cambiar Contraseña de un Usuario

1. Genera un nuevo hash con `generate_passwords.py`
2. Reemplaza el campo `password` del usuario en `config.yaml`
3. Reinicia la aplicación

## 🔒 Mejores Prácticas de Seguridad

### ✅ Hacer

- ✅ Cambiar las contraseñas por defecto (`admin123`, `demo123`)
- ✅ Usar contraseñas fuertes (mínimo 12 caracteres)
- ✅ Cambiar la `key` del cookie por una única
- ✅ Revisar periódicamente los usuarios activos
- ✅ Eliminar usuarios que ya no necesiten acceso
- ✅ Mantener `config.yaml` fuera de control de versiones en producción

### ❌ No hacer

- ❌ NO subir `config.yaml` a GitHub si contiene datos reales
- ❌ NO compartir contraseñas en texto plano
- ❌ NO usar la misma contraseña para múltiples usuarios
- ❌ NO dejar usuarios de prueba en producción
- ❌ NO usar la clave de cookie por defecto en producción

## 🔑 Generar Clave Secreta para Cookies

```python
import secrets
print(secrets.token_hex(32))
```

Copia el resultado y úsalo como valor de `key` en el apartado `cookie` de `config.yaml`.

## 📧 Usuarios Preautorizados

Si quieres que ciertos emails puedan auto-registrarse (función avanzada):

```yaml
preauthorized:
  emails:
  - usuario1@permitido.com
  - usuario2@permitido.com
```

**Nota**: Esta función requiere implementar la página de registro (no incluida en la versión básica).

## 🛠️ Solución de Problemas

### "Error al cargar config.yaml"

**Causa**: Formato YAML incorrecto

**Solución**: Verifica la indentación (usar espacios, no tabs)

### "Usuario/contraseña incorrectos"

**Causa**: El hash no coincide o usuario no existe

**Solución**: 
1. Verifica que el usuario existe en `config.yaml`
2. Regenera el hash de contraseña
3. Asegúrate de no tener espacios extra

### "La sesión expira muy rápido"

**Causa**: `expiry_days` muy bajo

**Solución**: Aumenta el valor en `config.yaml`:
```yaml
cookie:
  expiry_days: 60  # 2 meses
```

## 📊 Ejemplo Completo de config.yaml

```yaml
credentials:
  usernames:
    admin:
      email: admin@topoguias.es
      name: Administrador General
      password: $2b$12$ejemplo_hash_muy_largo_aqui
    
    geologo1:
      email: geologo@guadalajara.es
      name: Juan Pérez
      password: $2b$12$otro_hash_diferente
    
    tecnico_parque:
      email: tecnico@parque.es
      name: María García
      password: $2b$12$un_hash_mas
    
cookie:
  expiry_days: 30
  key: e4a5c7d9b2f8e3a1c6d9b4f7e2a8c5d9b3f6e1a7c4d8b5f9e2a6c3d7b8f4e1a9
  name: topoguias_auth_cookie

preauthorized:
  emails:
  - nuevousuario@example.com
```

## 🔐 Configuración Recomendada para Producción

1. **Cambia TODAS las contraseñas por defecto**
2. **Genera una key única para cookies**:
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```
3. **Añade `config.yaml` al `.gitignore`**:
   ```bash
   echo "config.yaml" >> .gitignore
   ```
4. **Mantén un backup cifrado** de `config.yaml`
5. **Documenta los usuarios** en un lugar seguro separado

## 📞 Soporte

Si tienes problemas con la gestión de usuarios:
1. Revisa que `streamlit-authenticator` esté instalado
2. Verifica la sintaxis de `config.yaml`
3. Consulta los logs de la aplicación
4. Crea un issue en GitHub si el problema persiste

---

**Importante**: Trata el archivo `config.yaml` como información sensible. Nunca lo compartas públicamente ni lo subas a repositorios públicos con datos reales.
