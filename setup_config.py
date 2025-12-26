"""
Script para crear el archivo config.yaml con contraseñas hasheadas correctamente.
Ejecuta este script ANTES de iniciar la aplicación por primera vez.
"""

import streamlit_authenticator as stauth
import yaml

print("=" * 60)
print("GENERADOR DE CONFIG.YAML PARA TOPOGUÍAS")
print("=" * 60)

# Generar hashes para las contraseñas por defecto
print("\n📝 Generando hashes para contraseñas por defecto...")
passwords = ['admin123', 'demo123']
hashed_passwords = stauth.Hasher(passwords).generate()

print(f"✅ Hash para 'admin123': {hashed_passwords[0][:50]}...")
print(f"✅ Hash para 'demo123': {hashed_passwords[1][:50]}...")

# Crear estructura del config
config = {
    'credentials': {
        'usernames': {
            'admin': {
                'email': 'admin@topoguias.es',
                'name': 'Administrador',
                'password': hashed_passwords[0]
            },
            'usuario1': {
                'email': 'usuario1@example.com',
                'name': 'Usuario Demo',
                'password': hashed_passwords[1]
            }
        }
    },
    'cookie': {
        'expiry_days': 30,
        'key': 'cambiar_esta_clave_en_produccion_por_una_unica_12345',
        'name': 'topoguias_auth_cookie'
    },
    'preauthorized': {
        'emails': []
    }
}

# Guardar a archivo
print("\n💾 Guardando config.yaml...")
with open('config.yaml', 'w', encoding='utf-8') as file:
    yaml.dump(config, file, default_flow_style=False, allow_unicode=True)

print("✅ Archivo config.yaml creado exitosamente!")
print("\n" + "=" * 60)
print("CREDENCIALES DE ACCESO:")
print("=" * 60)
print("\n👤 Usuario 1:")
print("   Usuario: admin")
print("   Contraseña: admin123")
print("\n👤 Usuario 2:")
print("   Usuario: usuario1")
print("   Contraseña: demo123")
print("\n" + "=" * 60)
print("\n⚠️  IMPORTANTE:")
print("   1. Cambia estas contraseñas en producción")
print("   2. Cambia la 'key' del cookie por una única")
print("   3. Ejecuta: python generate_passwords.py para nuevas contraseñas")
print("\n✅ Ya puedes ejecutar: streamlit run app.py")
print("=" * 60)
