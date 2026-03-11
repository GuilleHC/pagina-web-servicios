# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Script

**1. Configura la API key** (requiere créditos en console.anthropic.com):

Windows PowerShell:
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."
```

Bash:
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

**2. Corre el script** desde la carpeta del proyecto:

```bash
cd "C:/Users/guill/OneDrive/Documents/Proyectos Python/Pagina Web Servicios"
python hero_generator.py
```

El script pedirá 5 datos interactivamente: nombre de marca, valor entregado, diferenciación, cliente ideal, y número de WhatsApp (con código de país, ej: `56912345678`).

## Architecture

Single-script tool (`hero_generator.py`) with three responsibilities:

1. **CLI input** (`preguntar`, `main`) — collects brand info interactively from the user.
2. **AI generation** (`generar_hero`) — calls `claude-opus-4-5` via the Anthropic SDK to produce a JSON object with `slogan`, `subtitulo`, and `cta` fields.
3. **HTML output** (`generar_html_hero`) — assembles a self-contained HTML file with inline CSS for a Hero section, including a WhatsApp CTA button.

Output files are written to `/mnt/user-data/outputs/` as `hero_<brand_name>.html`.

> **Windows:** La ruta `/mnt/user-data/outputs/` no existe en Windows. Al ejecutar desde Claude Code o localmente, guardar directamente en la carpeta del proyecto (ej: `hero_terapia_con_pintura.html`).

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
- Cuerpo opcional con bullets explicando el qué y el por qué del cambio
- Siempre en español, claros y descriptivos para poder revertir cambios fácilmente

**Seguridad:** Nunca incluir API keys en el código. Usar variables de entorno. El `.gitignore` excluye `__pycache__/`, `.env`, y archivos `hero_*.html` generados.

## Key Details

- The prompt is Spanish-language and targets Latin American entrepreneurs.
- The Claude API call expects a raw JSON response (no markdown fences); `json.loads` parses it directly.
- WhatsApp link is built with `urllib.parse.quote` from the phone number the user provides (expects country code, e.g. `56912345678`).
- **Windows encoding:** Al ejecutar desde Claude Code en Windows, agregar `sys.stdout.reconfigure(encoding='utf-8')` al inicio para evitar `UnicodeEncodeError` con emojis.
- **API key:** Debe estar configurada como variable de entorno `ANTHROPIC_API_KEY` antes de ejecutar. No tiene valor por defecto en el código.
