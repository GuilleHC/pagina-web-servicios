import json
import urllib.parse
from flask import Flask, render_template, request
import anthropic

app = Flask(__name__)

TIPOS_HERO = {
    "tipo_1": {
        "nombre": "Texto izquierda, Imagen derecha",
        "imagen": "hero_1.jpg",
    },
    "tipo_2": {
        "nombre": "Imagen izquierda, Texto derecha",
        "imagen": "hero_2.jpg",
    },
    "tipo_3": {
        "nombre": "Texto e Imagen Central",
        "imagen": "hero_3.jpg",
    },
}

PALETAS = {
    "profesional": {
        "nombre": "Profesional",
        "descripcion": "Coaches, consultores, abogados",
        "bg_gradient": "linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)",
        "acento": "#e94560",
        "texto": "#ffffff",
        "subtexto": "#a8b2c1",
        "preview": ["#1a1a2e", "#0f3460", "#e94560"],
    },
    "salud": {
        "nombre": "Salud & Nutrición",
        "descripcion": "Nutricionistas, médicos, dentistas",
        "bg_gradient": "linear-gradient(135deg, #1b4332 0%, #2d6a4f 50%, #40916c 100%)",
        "acento": "#95d5b2",
        "texto": "#ffffff",
        "subtexto": "#d8f3dc",
        "preview": ["#1b4332", "#40916c", "#95d5b2"],
    },
    "bienestar": {
        "nombre": "Bienestar & Mente",
        "descripcion": "Psicólogos, terapeutas, meditación",
        "bg_gradient": "linear-gradient(135deg, #2d1b69 0%, #553c9a 50%, #8b5cf6 100%)",
        "acento": "#e0aaff",
        "texto": "#ffffff",
        "subtexto": "#c8b1e4",
        "preview": ["#2d1b69", "#553c9a", "#e0aaff"],
    },
    "energia": {
        "nombre": "Energía & Movimiento",
        "descripcion": "Profesores, entrenadores, deportistas",
        "bg_gradient": "linear-gradient(135deg, #7c2d12 0%, #c2410c 50%, #f97316 100%)",
        "acento": "#fbbf24",
        "texto": "#ffffff",
        "subtexto": "#fed7aa",
        "preview": ["#7c2d12", "#c2410c", "#fbbf24"],
    },
}


def generar_hero_copy(profesion, marca, valor, diferenciacion, cliente_ideal):
    client = anthropic.Anthropic()
    prompt = f"""Eres un experto en marketing y copywriting para profesionales latinoamericanos que prestan servicios.
Con la siguiente información, genera el contenido para la sección Hero de una página web.

Información del profesional:
- Profesión: {profesion}
- Nombre de la marca o profesional: {marca}
- Valor que entrega / problema que resuelve: {valor}
- Diferenciación: {diferenciacion}
- Cliente ideal: {cliente_ideal}

Genera exactamente estos 4 elementos en formato JSON (solo el JSON, sin texto adicional ni backticks):
{{
  "etiqueta": "Profesión o especialidad en 2-4 palabras, ej: Nutricionista Certificada",
  "titulo": "Frase principal impactante de máximo 10 palabras, directa al dolor o deseo del cliente ideal",
  "subtitulo": "Propuesta de valor en 1-2 oraciones, máximo 25 palabras, clara y específica",
  "cta": "Texto del botón de WhatsApp, máximo 5 palabras, acción concreta"
}}

Reglas:
- La etiqueta debe reflejar la profesión con credibilidad
- El título debe hablarle directamente al cliente ideal usando "tú"
- El subtítulo debe mencionar el beneficio concreto
- El CTA debe facilitar el primer paso
- Usa español latinoamericano, tono cercano y profesional
"""
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(message.content[0].text.strip())


WA_ICON_SVG = """<svg style="width:24px;height:24px" viewBox="0 0 24 24" fill="white" xmlns="http://www.w3.org/2000/svg"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>"""

CTA_BTN_CSS = """
        .cta-btn {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            background: #25D366;
            color: white;
            text-decoration: none;
            padding: 16px 36px;
            border-radius: 50px;
            font-size: 1.1rem;
            font-weight: 700;
            transition: transform 0.2s, box-shadow 0.2s;
            box-shadow: 0 4px 20px rgba(37, 211, 102, 0.4);
        }
        .cta-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 28px rgba(37, 211, 102, 0.5);
        }"""

FOTO_PLACEHOLDER = """<div class="foto-placeholder">
                <span>📷 Tu foto aquí</span>
            </div>"""


def generar_html_hero(marca, hero, whatsapp, paleta_key, tipo_hero="tipo_1"):
    p = PALETAS[paleta_key]
    mensaje_wa = urllib.parse.quote(f"Hola {marca}, me interesa saber más sobre tus servicios.")
    wa_link = f"https://wa.me/{whatsapp}?text={mensaje_wa}"

    if tipo_hero == "tipo_2":
        return _html_split_imagen_izquierda(marca, hero, wa_link, p)
    elif tipo_hero == "tipo_3":
        return _html_central(marca, hero, wa_link, p)
    else:
        return _html_split_texto_izquierda(marca, hero, wa_link, p)


def _html_split_texto_izquierda(marca, hero, wa_link, p):
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{marca}</title>
    <meta name="description" content="{hero['subtitulo']}">
    <meta property="og:title" content="{hero['titulo']}">
    <meta property="og:description" content="{hero['subtitulo']}">
    <meta property="og:type" content="website">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', 'Segoe UI', sans-serif; }}
        .hero {{
            min-height: 100vh;
            background: {p['bg_gradient']};
            display: flex;
            align-items: center;
            padding: 60px 6%;
        }}
        .hero-inner {{
            width: 100%;
            max-width: 1100px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 60px;
            align-items: center;
        }}
        .hero-content {{ text-align: left; }}
        .etiqueta {{
            display: inline-block;
            font-size: 0.8rem;
            font-weight: 600;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: {p['acento']};
            border: 1px solid {p['acento']};
            padding: 6px 18px;
            border-radius: 50px;
            margin-bottom: 28px;
        }}
        .titulo {{
            font-size: 2.8rem;
            font-weight: 800;
            color: {p['texto']};
            line-height: 1.15;
            margin-bottom: 20px;
        }}
        .subtitulo {{
            font-size: 1.1rem;
            color: {p['subtexto']};
            line-height: 1.7;
            margin-bottom: 36px;
        }}
        {CTA_BTN_CSS}
        .foto-placeholder {{
            width: 100%;
            aspect-ratio: 4/5;
            border-radius: 20px;
            border: 2px dashed {p['acento']};
            display: flex;
            align-items: center;
            justify-content: center;
            color: {p['acento']};
            font-size: 1rem;
            font-weight: 600;
            opacity: 0.6;
        }}
        @media (max-width: 768px) {{
            .hero-inner {{ grid-template-columns: 1fr; gap: 40px; }}
            .titulo {{ font-size: 2rem; }}
        }}
    </style>
</head>
<body>
    <section class="hero">
        <div class="hero-inner">
            <div class="hero-content">
                <span class="etiqueta">{hero['etiqueta']}</span>
                <h1 class="titulo">{hero['titulo']}</h1>
                <p class="subtitulo">{hero['subtitulo']}</p>
                <a href="{wa_link}" target="_blank" class="cta-btn">
                    {WA_ICON_SVG}
                    {hero['cta']}
                </a>
            </div>
            {FOTO_PLACEHOLDER}
        </div>
    </section>
</body>
</html>"""


def _html_split_imagen_izquierda(marca, hero, wa_link, p):
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{marca}</title>
    <meta name="description" content="{hero['subtitulo']}">
    <meta property="og:title" content="{hero['titulo']}">
    <meta property="og:description" content="{hero['subtitulo']}">
    <meta property="og:type" content="website">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', 'Segoe UI', sans-serif; }}
        .hero {{
            min-height: 100vh;
            background: {p['bg_gradient']};
            display: flex;
            align-items: center;
            padding: 60px 6%;
        }}
        .hero-inner {{
            width: 100%;
            max-width: 1100px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 60px;
            align-items: center;
        }}
        .hero-content {{ text-align: left; }}
        .etiqueta {{
            display: inline-block;
            font-size: 0.8rem;
            font-weight: 600;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: {p['acento']};
            border: 1px solid {p['acento']};
            padding: 6px 18px;
            border-radius: 50px;
            margin-bottom: 28px;
        }}
        .titulo {{
            font-size: 2.8rem;
            font-weight: 800;
            color: {p['texto']};
            line-height: 1.15;
            margin-bottom: 20px;
        }}
        .subtitulo {{
            font-size: 1.1rem;
            color: {p['subtexto']};
            line-height: 1.7;
            margin-bottom: 36px;
        }}
        {CTA_BTN_CSS}
        .foto-placeholder {{
            width: 100%;
            aspect-ratio: 4/5;
            border-radius: 20px;
            border: 2px dashed {p['acento']};
            display: flex;
            align-items: center;
            justify-content: center;
            color: {p['acento']};
            font-size: 1rem;
            font-weight: 600;
            opacity: 0.6;
        }}
        @media (max-width: 768px) {{
            .hero-inner {{ grid-template-columns: 1fr; gap: 40px; }}
            .titulo {{ font-size: 2rem; }}
        }}
    </style>
</head>
<body>
    <section class="hero">
        <div class="hero-inner">
            {FOTO_PLACEHOLDER}
            <div class="hero-content">
                <span class="etiqueta">{hero['etiqueta']}</span>
                <h1 class="titulo">{hero['titulo']}</h1>
                <p class="subtitulo">{hero['subtitulo']}</p>
                <a href="{wa_link}" target="_blank" class="cta-btn">
                    {WA_ICON_SVG}
                    {hero['cta']}
                </a>
            </div>
        </div>
    </section>
</body>
</html>"""


def _html_central(marca, hero, wa_link, p):
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{marca}</title>
    <meta name="description" content="{hero['subtitulo']}">
    <meta property="og:title" content="{hero['titulo']}">
    <meta property="og:description" content="{hero['subtitulo']}">
    <meta property="og:type" content="website">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', 'Segoe UI', sans-serif; }}
        .hero {{
            min-height: 100vh;
            background: {p['bg_gradient']};
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 60px 20px;
        }}
        .hero-content {{ max-width: 720px; width: 100%; }}
        .etiqueta {{
            display: inline-block;
            font-size: 0.85rem;
            font-weight: 600;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: {p['acento']};
            border: 1px solid {p['acento']};
            padding: 6px 18px;
            border-radius: 50px;
            margin-bottom: 28px;
        }}
        .titulo {{
            font-size: 3rem;
            font-weight: 800;
            color: {p['texto']};
            line-height: 1.2;
            margin-bottom: 24px;
        }}
        .foto-placeholder {{
            width: 180px;
            height: 180px;
            border-radius: 50%;
            border: 2px dashed {p['acento']};
            display: flex;
            align-items: center;
            justify-content: center;
            color: {p['acento']};
            font-size: 0.9rem;
            font-weight: 600;
            opacity: 0.6;
            margin: 0 auto 28px;
        }}
        .subtitulo {{
            font-size: 1.2rem;
            color: {p['subtexto']};
            line-height: 1.7;
            margin-bottom: 40px;
            max-width: 580px;
            margin-left: auto;
            margin-right: auto;
        }}
        {CTA_BTN_CSS}
        @media (max-width: 600px) {{
            .titulo {{ font-size: 2rem; }}
            .subtitulo {{ font-size: 1rem; }}
        }}
    </style>
</head>
<body>
    <section class="hero">
        <div class="hero-content">
            <span class="etiqueta">{hero['etiqueta']}</span>
            <h1 class="titulo">{hero['titulo']}</h1>
            {FOTO_PLACEHOLDER}
            <p class="subtitulo">{hero['subtitulo']}</p>
            <a href="{wa_link}" target="_blank" class="cta-btn">
                {WA_ICON_SVG}
                {hero['cta']}
            </a>
        </div>
    </section>
</body>
</html>"""


@app.route("/")
def index():
    return render_template("index.html", paletas=PALETAS, tipos_hero=TIPOS_HERO)


@app.route("/generar", methods=["POST"])
def generar():
    profesion = request.form["profesion"]
    marca = request.form["marca"]
    valor = request.form["valor"]
    diferenciacion = request.form["diferenciacion"]
    cliente_ideal = request.form["cliente_ideal"]
    whatsapp = request.form["whatsapp"]
    paleta_key = request.form.get("paleta", "profesional")
    tipo_hero = request.form.get("tipo_hero", "tipo_1")

    hero = generar_hero_copy(profesion, marca, valor, diferenciacion, cliente_ideal)
    html_output = generar_html_hero(marca, hero, whatsapp, paleta_key, tipo_hero)

    return render_template(
        "preview.html",
        hero=hero,
        html_output=html_output,
        marca=marca,
        paleta=PALETAS[paleta_key],
    )


if __name__ == "__main__":
    app.run(debug=True)
