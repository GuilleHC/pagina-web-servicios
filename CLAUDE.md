# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Contexto del proyecto

Aplicación web que genera páginas web profesionales para **emprendedores y profesionales de servicios latinoamericanos** (coaches, nutricionistas, psicólogos, entrenadores, consultores, etc.) que no tienen conocimientos técnicos.

El usuario responde un formulario con información de su negocio, elige un estilo visual, y la app usa Claude AI para generar automáticamente una **página web completa y descargable** lista para subir a un hosting como Hostinger.

### Filosofía de desarrollo
- El proyecto crece **iterativamente**: se van agregando secciones a la página web de a una, validando el resultado antes de continuar
- Cada nueva sección requiere: (1) nuevas preguntas en el formulario si aplica, (2) extensión del prompt a Claude, (3) función HTML nueva en `app.py`, (4) link en el navbar
- Se prioriza **simplicidad y calidad visual** por sobre cantidad de opciones
- El output final debe funcionar como sitio estático sin dependencias externas (sin frameworks, sin servidor)

## Correr la app web

**1. Configura la API key** (solo la primera vez — guardarla permanentemente):

```powershell
[System.Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-...", "User")
```

> La key debe empezar con `sk-ant-`, sin `#` ni comillas extra. Después de guardarla, cerrar y volver a abrir PowerShell.

**2. Inicia el servidor Flask:**

```powershell
cd "C:\Users\guill\OneDrive\Documents\Proyectos Python\Pagina Web Servicios"
python app.py
```

**3. Abre el navegador en:** `http://127.0.0.1:5000`

## Architecture

Aplicación web Flask (`app.py`) con dos rutas:

- `GET /` — Formulario con 5 preguntas del negocio + selector de tipo de Hero + selector de paleta de color
- `POST /generar` — Llama a Claude API, genera el Hero y muestra la preview

Archivos principales:
- `app.py` — Servidor Flask, lógica de generación con Claude, construcción del HTML
- `templates/index.html` — Formulario de entrada (3 secciones: info, tipo de Hero, paleta)
- `templates/preview.html` — Vista previa full-screen del Hero + botón de descarga
- `static/hero-tipos/` — Imágenes de referencia de los 3 layouts (`hero_1.jpg`, `hero_2.jpg`, `hero_3.jpg`)

### Flujo del formulario (3 secciones):
1. **Info del negocio** — profesión, marca, valor, diferenciación, cliente ideal, pilares (razones para elegirte), WhatsApp
2. **Tipo de Hero** — el usuario elige uno de 3 layouts clicando en una imagen de referencia
3. **Paleta de color** — 4 opciones visuales

### Tipos de Hero disponibles (`TIPOS_HERO` en app.py):
- `tipo_1` — Texto izquierda, Imagen derecha → `_hero_texto_izquierda()`
- `tipo_2` — Imagen izquierda, Texto derecha → `_hero_imagen_izquierda()`
- `tipo_3` — Texto e Imagen Central → `_hero_central()`

Cada función genera HTML independiente con el layout correspondiente. Los layouts con foto incluyen un placeholder `"📷 Tu foto aquí"`.

### Hero section — 4 elementos generados por Claude:
1. **Etiqueta** — profesión/especialidad (ej: "Nutricionista Certificada")
2. **Título** — frase principal impactante (máx. 10 palabras)
3. **Subtítulo** — propuesta de valor (máx. 25 palabras)
4. **CTA** — texto del botón WhatsApp (máx. 5 palabras)

### Paletas de color disponibles:
- `profesional` — Azul oscuro (coaches, consultores)
- `salud` — Verde (nutricionistas, médicos)
- `bienestar` — Morado (psicólogos, terapeutas)
- `energia` — Naranja (profesores, entrenadores)

## Git & GitHub

- **Repositorio:** https://github.com/GuilleHC/pagina-web-servicios
- **Remote:** `origin` → `https://github.com/GuilleHC/pagina-web-servicios.git`
- **Rama principal:** `master`
- **gh CLI** instalado en `C:/Program Files/GitHub CLI`, autenticado como `GuilleHC`

Flujo de trabajo:
```bash
git add <archivos>
git commit -m "tipo: resumen corto

- Detalle del cambio 1
- Detalle del cambio 2"
git push
```

**Reglas para mensajes de commit:**
- Primera línea: `tipo: resumen en máximo 72 caracteres`
- Tipos: `feat` (nueva función), `fix` (corrección), `docs` (documentación), `refactor`, `style`
- Cuerpo con bullets explicando el qué y el por qué del cambio
- Siempre en español, claros y descriptivos para poder revertir cambios fácilmente

**Seguridad:** Nunca incluir API keys en el código. Usar variables de entorno. El `.gitignore` excluye `__pycache__/`, `.env`, y archivos `hero_*.html` generados.

## Estrategia de desarrollo de la página web

El output de la app es una **página web completa** (`index.html`) lista para subir a Hostinger u otro hosting estático. Se construye de forma incremental — por ahora solo tiene el Hero, y se van agregando secciones a medida que se desarrollan.

**Secciones planificadas (en orden de implementación):**
1. ✅ **Hero** — 3 layouts, contenido generado por Claude
2. ✅ **Propuesta de Valor** — etiqueta, título, subtítulo + cards con pilares del negocio
3. ⬜ Sobre mí
4. ⬜ Servicios
5. ⬜ CTA final / Contacto

Cada sección nueva se agrega como una función `_html_seccion_X(contenido, p)` en `app.py` y se concatena en `generar_html_pagina()`. El formulario se expande con nuevas preguntas según lo requiera cada sección.

### Arquitectura modular del HTML generado:
- `_html_head()` — `<head>` con meta tags, fuentes y `scroll-behavior: smooth`
- `_html_navbar()` — **sección fija separada** (`position: fixed`, `background: #0d0d1a`, `border-bottom` con color acento de la paleta), links dinámicos según secciones activas, hamburger mobile
- `_html_seccion_hero()` — despacha a `_hero_texto_izquierda / _hero_imagen_izquierda / _hero_central` según `tipo_hero`; el hero tiene `id="inicio"` y `padding-top: 68px` para compensar la navbar fija
- `_html_seccion_propuesta_valor()` — grid de cards con `id="propuesta-valor"`
- `generar_html_pagina()` — construye la lista `secciones` para el navbar, luego ensambla: head → navbar → hero → propuesta_valor → cierre

### Navbar — reglas de diseño:
- Es una sección **completamente separada** del hero, con su propio color oscuro fijo (`#0d0d1a`)
- El diseño visual (border-bottom con color acento) sigue la paleta elegida, no el tipo de hero
- Siempre tiene un CTA de WhatsApp a la derecha
- Mobile: hamburger menu que despliega los links en columna

### Navbar — cómo agregar links al crecer la página:
En `generar_html_pagina()`, la lista `secciones` controla los links:
```python
secciones = [
    {"id": "inicio",          "label": "Inicio"},
    {"id": "propuesta-valor", "label": pv["etiqueta"]},
    # Agregar aquí cada sección nueva con su id y etiqueta
]
```
Cada sección nueva debe tener `id="su-id"` en su tag `<section>`.

### Generación de contenido:
- Una sola llamada a Claude (`generar_contenido()`) genera el JSON de todas las secciones
- El prompt incluye todos los inputs del formulario y retorna `hero` + `propuesta_valor`
- Al agregar una nueva sección, se extiende el JSON del prompt y se crea la función HTML correspondiente

## Key Details

- El prompt está en español y apunta a emprendedores/profesionales latinoamericanos.
- La llamada a Claude espera JSON puro (sin backticks); `json.loads` lo parsea directo.
- El link de WhatsApp se construye con `urllib.parse.quote` desde el número ingresado (requiere código de país, ej: `56912345678`).
- **API key:** Debe estar en la variable de entorno `ANTHROPIC_API_KEY`. La key empieza con `sk-ant-`, sin `#` al inicio.
