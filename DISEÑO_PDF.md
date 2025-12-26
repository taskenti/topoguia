# 📄 Guía de Diseño del PDF

Este documento explica cómo está estructurado el PDF generado y cómo replicar el diseño oficial PR-GU.

## 📐 Formato General

- **Orientación**: Horizontal (Landscape)
- **Tamaño**: A4 (297 x 210 mm)
- **Páginas**: 2
- **Color Principal**: Verde #007A33 (RGB: 0, 122, 51)
- **Fuentes**: Helvetica (Sans-serif)

## 📄 PÁGINA 1: Cara Informativa

### Estructura Visual

```
┌─────────────────────────────────────────────────────┐
│ [Logo]                    Entidad Promotora │
│                           Parque Natural    │
├─────────────────────────────────────────────────────┤
│ [M]│                                                │
│ [I]│         FOTO PANORÁMICA                       │
│ [R]│    [Etiqueta: Pico]  [Etiqueta: Castillo]    │
│ [A]│                                                │
│ [D]│                                                │
│ [O]│                                                │
│ [R]├────────────────────────────────────────────────┤
│    │ PR-GU 08                                       │
│    │ SENDERO MANDAYONA-MIRABUENO-ARAGOSA           │
│    │                                                │
│    │ [Párrafo 1: Introducción]                     │
│    │ [Párrafo 2: Recorrido]                        │
│    │ [Párrafo 3: Vegetación y vistas]              │
│    │ [Párrafo 4: Fauna]                            │
│    │                                                │
│    │ ┌────────────────────────────────────────┐    │
│    │ │ RECOMENDACIONES                        │    │
│    │ │ [Texto de advertencias]                │    │
│    │ └────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

### Elementos de la Página 1

#### 1. Cabecera (0-20mm desde arriba)
- **Logo institucional** (izquierda, si existe)
- **Texto institucional** (derecha):
  - Entidad promotora (8pt, gris)
  - Parque Natural (8pt, gris)

#### 2. Franja de Foto Panorámica (25-105mm)
- **Etiqueta vertical** (borde izquierdo):
  - Ancho: 15mm
  - Color de fondo: Verde #007A33
  - Texto: Nombre del mirador (rotado 90°, blanco, negrita)
  
- **Imagen panorámica**:
  - Posición: 28mm desde izquierda
  - Ancho: 259mm
  - Alto: 80mm
  
- **Etiquetas de lugares** (sobre la imagen):
  - Fuente: 7pt, negrita, blanco
  - Distribuidas horizontalmente

#### 3. Título Principal (110-130mm)
- **Código de ruta**: 
  - Fuente: Helvetica Bold, 28pt
  - Color: Verde #007A33
  
- **Nombre del sendero**:
  - Fuente: Helvetica Bold, 14pt
  - Color: Verde #007A33
  - Prefijo: "SENDERO "

#### 4. Columna de Texto (130-180mm)
- **Ancho**: 180mm
- **Fuente**: Helvetica Regular, 9pt
- **Alineación**: Justificado
- **Separación entre párrafos**: 2mm
- **Contenido**:
  1. Párrafo introducción
  2. Párrafo recorrido
  3. Párrafo vegetación
  4. Párrafo fauna

#### 5. Bloque de Recomendaciones (185-200mm)
- **Fondo**: Amarillo claro #FFF3CD
- **Borde**: Sin borde
- **Padding**: 2mm
- **Título**: "RECOMENDACIONES" (10pt, negrita, verde)
- **Texto**: 8pt, regular, negro

#### 6. Pie de Página (200-210mm)
- **Texto**: Fecha de generación
- **Fuente**: 7pt, cursiva, gris
- **Alineación**: Centro

---

## 📄 PÁGINA 2: Cara Técnica

### Estructura Visual

```
┌──────────────────────────────────┬──────────────────┐
│                                  │ FICHA TÉCNICA    │
│                                  ├──────────────────┤
│                                  │ Horario: 2h 35m  │
│        MAPA TOPOGRÁFICO          │ Distancia: 11 km │
│                                  │ Desnivel+: 167m  │
│         (Con trazado de          │ Desnivel-: 167m  │
│          ruta marcado)           │ Tipo: Circular   │
│                                  ├──────────────────┤
│                                  │                  │
│                                  │  [TABLA MIDE]    │
│                                  │                  │
├──────────────────────────────────┤                  │
│                                  ├──────────────────┤
│   PERFIL DE ELEVACIÓN            │ SEÑALIZACIÓN     │
│                                  │ • Continuidad    │
│   [Gráfico de área con          │ • Cambio dir.    │
│    hitos etiquetados]            │ • Dir. errónea   │
│                                  ├──────────────────┤
│                                  │ DISFRUTA PARQUE  │
└──────────────────────────────────┤ • Prismáticos    │
                                   │ • Silencio       │
                                   │ • No fuego       │
                                   │ • Basura         │
                                   ├──────────────────┤
                                   │ TELÉFONOS        │
                                   │ 112 - 949885300  │
                                   │    [QR CODE]     │
                                   │   [URL Web]      │
                                   └──────────────────┘
```

### Elementos de la Página 2

#### 1. Mapa Topográfico (10-120mm altura, izquierda)
- **Posición**: 10mm desde arriba, 10mm desde izquierda
- **Dimensiones**: 180mm ancho × 110mm alto
- **Contenido esperado en la imagen**:
  - Trazado de ruta (línea amarilla con borde negro)
  - Iconos: P (parking), punto de inicio
  - Topografía de fondo

#### 2. Perfil de Elevación (125-170mm)
- **Posición**: 10mm desde izquierda
- **Dimensiones**: 180mm ancho × 45mm alto
- **Contenido esperado en la imagen**:
  - Gráfico de área con degradado
  - Eje X: Distancia (0-11km)
  - Eje Y: Altitud (ej: 900-1100m)
  - Etiquetas de hitos del recorrido

#### 3. Panel Lateral Derecho (195mm desde izquierda)

##### 3.1 Cabecera del Panel (10-18mm)
- **Fondo**: Verde #007A33
- **Ancho**: 92mm
- **Título**: "FICHA TÉCNICA" (11pt, negrita, blanco, centrado)

##### 3.2 Datos Técnicos (22-57mm)
- **Fondo**: Gris claro #F5F5F5
- **Fuente**: 8pt
- **Estructura**:
  ```
  Horario:           2h 35m
  Distancia:         11,0 Km
  Desnivel Subida:   167 m
  Desnivel Bajada:   167 m
  Tipo:              Circular
  ```
- **Separación**: 6mm entre líneas

##### 3.3 Tabla MIDE (57-92mm)
- **Imagen precargada** con matriz 2×2
- **Dimensiones**: Ancho completo del panel
- **Contenido**: Valores del 1 al 5 para cada criterio

##### 3.4 Señalización (100-127mm)
- **Título**: "SEÑALIZACIÓN" (9pt, negrita, verde)
- **Contenido**: (7pt, regular, negro)
  ```
  Marcas blancas y amarillas:
  • Continuidad
  • Cambio de dirección
  • Dirección equivocada
  ```

##### 3.5 Disfruta del Parque (135-163mm)
- **Título**: "DISFRUTA DEL PARQUE" (9pt, negrita, verde)
- **Contenido**: Lista de consejos (7pt)
  ```
  • Lleva prismáticos para observar fauna
  • Respeta el silencio del entorno
  • No enciendas fuego
  • Llévate toda tu basura
  ```

##### 3.6 Teléfonos y QR (170-210mm)
- **Título**: "TELÉFONOS DE INTERÉS" (9pt, negrita, verde)
- **Teléfonos**: (8pt)
  ```
  Emergencias: 112
  Parque: 949 88 53 00
  ```
- **Código QR**:
  - Posición: Centrado
  - Dimensiones: 25mm × 25mm
  - Contenido: URL del parque
- **URL**: Debajo del QR (6pt, cursiva, centrado)

---

## 🎨 Paleta de Colores Exacta

```
Verde Corporativo Principal:
  - HEX: #007A33
  - RGB: (0, 122, 51)
  - Uso: Cabeceras, títulos, elementos destacados

Amarillo/Ocre (Recomendaciones):
  - HEX: #FFF3CD
  - RGB: (255, 243, 205)
  - Uso: Fondo del bloque de recomendaciones

Gris Claro (Ficha Técnica):
  - HEX: #F5F5F5
  - RGB: (245, 245, 245)
  - Uso: Fondo de datos técnicos

Gris Texto Secundario:
  - HEX: #646464
  - RGB: (100, 100, 100)
  - Uso: Texto institucional, pie de página

Negro:
  - HEX: #000000
  - RGB: (0, 0, 0)
  - Uso: Texto principal

Blanco:
  - HEX: #FFFFFF
  - RGB: (255, 255, 255)
  - Uso: Texto sobre fondos oscuros
```

---

## 📏 Medidas Exactas (en mm)

### Página 1
```
Cabecera Logo:      10, 5, altura=15
Banner Etiqueta:    10, 25, ancho=15, alto=80
Banner Imagen:      28, 25, ancho=259, alto=80
Título PR-GU:       15, 110, fuente=28pt
Subtítulo:          15, 122, fuente=14pt
Columna Texto:      15, 135, ancho=180
Recomendaciones:    15, 185, ancho=180, alto=15
```

### Página 2
```
Mapa:               10, 10, ancho=180, alto=110
Perfil:             10, 125, ancho=180, alto=45
Panel Derecho:      195, 10, ancho=92
  - Ficha:          195, 10, ancho=92, alto=47
  - MIDE:           195, 57, ancho=92, alto=35
  - Señal:          195, 100
  - Disfruta:       195, 135
  - Teléfonos:      195, 170
  - QR:             225, 188, tamaño=25×25
```

---

## 🔧 Personalización

### Cambiar Colores

En `app.py`, busca la clase `PDF_Landscape` y modifica:

```python
# Cambiar el verde corporativo
verde = (0, 122, 51)  # RGB

# O en hexadecimal (convertir primero):
# #007A33 → R=0, G=122, B=51
```

### Ajustar Tamaños de Fuente

```python
# Títulos principales
self.set_font('Helvetica', 'B', 28)  # Código de ruta

# Subtítulos
self.set_font('Helvetica', 'B', 14)  # Nombre sendero

# Texto normal
self.set_font('Helvetica', '', 9)   # Descripción

# Texto pequeño
self.set_font('Helvetica', '', 7)   # Consejos, pie
```

### Cambiar Dimensiones de Imágenes

```python
# Mapa
pdf.image(mapa, x=10, y=10, w=180, h=110)

# Perfil
pdf.image(perfil, x=10, y=125, w=180, h=45)

# Ajusta 'w' (ancho) y 'h' (alto) en mm
```

---

## 📸 Preparación de Imágenes

### Mapa Topográfico
- **Formato recomendado**: JPG o PNG
- **Resolución**: Mínimo 1800×1100 px (300 DPI)
- **Contenido**: Debe incluir el trazado de la ruta visible

### Perfil de Elevación
- **Formato recomendado**: PNG (para transparencias)
- **Resolución**: Mínimo 1800×450 px
- **Contenido**: Gráfico con ejes claros y etiquetas legibles

### Tabla MIDE
- **Formato recomendado**: PNG
- **Resolución**: Mínimo 920×350 px
- **Contenido**: Matriz 2×2 con valores claramente visibles

### Foto Panorámica
- **Formato recomendado**: JPG
- **Resolución**: Mínimo 2590×800 px
- **Aspecto**: 16:5 aproximadamente (muy horizontal)

### Logo
- **Formato recomendado**: PNG con transparencia
- **Resolución**: Altura 150px mínimo
- **Fondo**: Transparente preferiblemente

---

## ✅ Checklist de Diseño

Antes de generar el PDF, verifica:

- [ ] Logo institucional (opcional)
- [ ] Foto panorámica de alta calidad
- [ ] Etiquetas de lugares preparadas
- [ ] Nombre del mirador definido
- [ ] 4 párrafos de descripción completos
- [ ] Texto de recomendaciones claro
- [ ] Mapa con trazado visible
- [ ] Perfil con hitos etiquetados
- [ ] Tabla MIDE con valores correctos
- [ ] Consejos personalizados
- [ ] Teléfonos actualizados
- [ ] URL para QR funcional

---

## 🎯 Resultado Final

El PDF generado debe ser:

✅ Profesional y limpio
✅ Fiel al diseño oficial PR-GU
✅ Fácil de leer e imprimir
✅ Con toda la información técnica necesaria
✅ Atractivo visualmente
✅ Listo para distribuir

---

## 📞 Soporte

Si necesitas ayuda con el diseño:
- Revisa las medidas en esta guía
- Compara con el PDF de ejemplo
- Verifica las imágenes de entrada
- Ajusta los parámetros según necesites
