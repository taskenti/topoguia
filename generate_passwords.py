"""
Script para generar contraseñas hasheadas para el sistema de autenticación.
Ejecuta este script para crear nuevas contraseñas hasheadas que puedas añadir a config.yaml
"""

import streamlit_authenticator as stauth

def generar_password_hash(password):
    """Genera un hash bcrypt de la contraseña"""
    return stauth.Hasher([password]).generate()[0]

if __name__ == "__main__":
    print("=== Generador de Contraseñas Hasheadas ===\n")
    
    # Contraseñas por defecto
    print("Contraseñas por defecto del sistema:\n")
    
    passwords = {
        "admin123": generar_password_hash("admin123"),
        "demo123": generar_password_hash("demo123")
    }
    
    for pwd, hashed in passwords.items():
        print(f"Contraseña: {pwd}")
        print(f"Hash: {hashed}\n")
    
    # Opción para generar contraseña personalizada
    print("\n¿Quieres generar un hash para una contraseña personalizada? (s/n)")
    respuesta = input().lower()
    
    if respuesta == 's':
        custom_pwd = input("\nIntroduce la contraseña a hashear: ")
        custom_hash = generar_password_hash(custom_pwd)
        print(f"\nContraseña: {custom_pwd}")
        print(f"Hash: {custom_hash}")
        print("\nCopia este hash al archivo config.yaml")
    
    print("\n=== Fin ===\")
