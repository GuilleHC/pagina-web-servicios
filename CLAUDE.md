# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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

- `GET /` — Formulario con 5 preguntas del negocio + selector de 4 paletas de color
- `POST /generar` — Llama a Claude API, genera el Hero y muestra la preview

Archivos principales:
- `app.py` — Servidor Flask, lógica de generación con Claude, construcción del HTML
- `templates/index.html` — Formulario de entrada con selector visual de paletas
- `templates/preview.html` — Vista previa full-screen del Hero + botón de descarga
- `hero_generator.py` — Script CLI original (referencia, no se usa en la app web)

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

## Key Details

- El prompt está en español y apunta a emprendedores/profesionales latinoamericanos.
- La llamada a Claude espera JSON puro (sin backticks); `json.loads` lo parsea directo.
- El link de WhatsApp se construye con `urllib.parse.quote` desde el número ingresado (requiere código de país, ej: `56912345678`).
- **API key:** Debe estar en la variable de entorno `ANTHROPIC_API_KEY`. La key empieza con `sk-ant-`, sin `#` al inicio.
