import json
import urllib.parse
from flask import Flask, render_template, request
import anthropic

app = Flask(__name__)

TIPOS_HERO = {
    "tipo_1": {
        "nombre": "Clásico",
        "imagen": "hero_1.jpg",
    },
    "tipo_2": {
        "nombre": "Moderno",
        "imagen": "hero_2.jpg",
    },
    "tipo_3": {
        "nombre": "Centrado",
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
        "acento": "#40916c",
        "texto": "#ffffff",
        "subtexto": "#d8f3dc",
        "preview": ["#1b4332", "#40916c", "#95d5b2"],
    },
    "bienestar": {
        "nombre": "Bienestar & Mente",
        "descripcion": "Psicólogos, terapeutas, meditación",
        "bg_gradient": "linear-gradient(135deg, #2d1b69 0%, #553c9a 50%, #8b5cf6 100%)",
        "acento": "#8b5cf6",
        "texto": "#ffffff",
        "subtexto": "#c8b1e4",
        "preview": ["#2d1b69", "#553c9a", "#e0aaff"],
    },
    "energia": {
        "nombre": "Energía & Movimiento",
        "descripcion": "Profesores, entrenadores, deportistas",
        "bg_gradient": "linear-gradient(135deg, #7c2d12 0%, #c2410c 50%, #f97316 100%)",
        "acento": "#f97316",
        "texto": "#ffffff",
        "subtexto": "#fed7aa",
        "preview": ["#7c2d12", "#c2410c", "#fbbf24"],
    },
}

# ── Constantes HTML reutilizables ─────────────────────────────────────────────

WA_ICON_SVG = """<svg style="width:24px;height:24px;flex-shrink:0" viewBox="0 0 24 24" fill="white" xmlns="http://www.w3.org/2000/svg"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>"""


# ── Generación de contenido con Claude ───────────────────────────────────────

def generar_contenido(profesion, marca, valor, diferenciacion, cliente_ideal, pilares):
    client = anthropic.Anthropic()
    prompt = f"""Eres un experto en marketing y copywriting para profesionales latinoamericanos que prestan servicios.
Con la siguiente información, genera el contenido para dos secciones de una página web.

Información del profesional:
- Profesión: {profesion}
- Nombre de la marca o profesional: {marca}
- Valor que entrega / problema que resuelve: {valor}
- Diferenciación: {diferenciacion}
- Cliente ideal: {cliente_ideal}
- Pilares del negocio / razones para elegirlo: {pilares}

Genera exactamente este JSON (solo el JSON, sin texto adicional ni backticks):
{{
  "hero": {{
    "etiqueta": "Profesión o especialidad en 2-4 palabras",
    "titulo": "Frase principal impactante de máximo 10 palabras, directa al dolor o deseo del cliente ideal",
    "subtitulo": "Propuesta de valor en 1-2 oraciones, máximo 25 palabras, clara y específica",
    "cta": "Texto del botón WhatsApp, máximo 5 palabras, acción concreta"
  }},
  "propuesta_valor": {{
    "etiqueta": "Etiqueta de sección en 2-4 palabras, ej: Por qué elegirnos",
    "titulo": "Título de sección impactante, máximo 10 palabras, enfocado en el valor entregado",
    "subtitulo": "Descripción breve de la propuesta de valor, máximo 25 palabras",
    "cards": [
      {{"titulo": "Nombre del pilar en 3-6 palabras", "descripcion": "Descripción del pilar en 1-2 oraciones, máximo 20 palabras"}},
      {{"titulo": "Nombre del pilar en 3-6 palabras", "descripcion": "Descripción del pilar en 1-2 oraciones, máximo 20 palabras"}},
      {{"titulo": "Nombre del pilar en 3-6 palabras", "descripcion": "Descripción del pilar en 1-2 oraciones, máximo 20 palabras"}}
    ]
  }}
}}

Reglas:
- El hero debe hablarle directamente al cliente ideal usando "tú"
- Las cards de propuesta_valor deben basarse en los pilares indicados, uno por card
- Si hay más de 3 pilares, incluye todos como cards adicionales
- Usa español latinoamericano, tono cercano y profesional
"""
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(message.content[0].text.strip())


# ── Ensamblado de la página web ───────────────────────────────────────────────

def generar_html_pagina(marca, contenido, whatsapp, paleta_key, tipo_hero="tipo_1"):
    p = PALETAS[paleta_key]
    mensaje_wa = urllib.parse.quote(f"Hola {marca}, me interesa saber más sobre tus servicios.")
    wa_link = f"https://wa.me/{whatsapp}?text={mensaje_wa}"

    hero = contenido["hero"]
    pv   = contenido["propuesta_valor"]

    # Lista de secciones para los links del navbar — agregar aquí cada sección nueva
    secciones = [
        {"id": "inicio",          "label": "Inicio"},
        {"id": "propuesta-valor", "label": pv["etiqueta"]},
    ]

    navbar_html = _html_navbar(marca, wa_link, hero["cta"], p, secciones)

    return (
        _html_head(marca, hero) +
        navbar_html +
        _html_seccion_hero(hero, wa_link, p, tipo_hero) +
        _html_seccion_propuesta_valor(pv, p) +
        "\n</body>\n</html>"
    )


# ── Head ──────────────────────────────────────────────────────────────────────

def _html_head(marca, hero):
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
        html {{ scroll-behavior: smooth; }}
        body {{ font-family: 'Inter', 'Segoe UI', sans-serif; }}
    </style>
</head>
<body>
"""


# ── Navbar ────────────────────────────────────────────────────────────────────

def _html_navbar(marca, wa_link, cta_text, p, secciones):
    links_html = "\n".join(
        f'            <a href="#{s["id"]}" class="nav-link">{s["label"]}</a>'
        for s in secciones
    )
    return f"""    <style>
        .navbar {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            height: 68px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 6%;
            background: #0d0d1a;
            border-bottom: 2px solid {p['acento']};
            box-shadow: 0 2px 20px rgba(0,0,0,0.3);
        }}
        .nav-brand {{
            font-size: 1rem;
            font-weight: 800;
            color: #ffffff;
            text-decoration: none;
            letter-spacing: 0.5px;
            flex-shrink: 0;
        }}
        .nav-links {{
            display: flex;
            align-items: center;
            gap: 32px;
        }}
        .nav-link {{
            font-size: 0.88rem;
            font-weight: 600;
            color: rgba(255,255,255,0.65);
            text-decoration: none;
            transition: color 0.2s;
            white-space: nowrap;
        }}
        .nav-link:hover {{ color: #ffffff; }}
        .nav-cta {{
            display: inline-flex;
            align-items: center;
            gap: 7px;
            background: #25D366;
            color: white;
            text-decoration: none;
            padding: 9px 20px;
            border-radius: 50px;
            font-size: 0.85rem;
            font-weight: 700;
            transition: opacity 0.2s, transform 0.15s;
            white-space: nowrap;
            flex-shrink: 0;
        }}
        .nav-cta:hover {{ opacity: 0.88; transform: translateY(-1px); }}
        .nav-hamburger {{
            display: none;
            flex-direction: column;
            gap: 5px;
            background: none;
            border: none;
            cursor: pointer;
            padding: 4px;
        }}
        .nav-hamburger span {{
            display: block;
            width: 22px;
            height: 2px;
            background: white;
            border-radius: 2px;
        }}
        @media (max-width: 768px) {{
            .nav-links {{
                display: none;
                position: fixed;
                top: 68px;
                left: 0;
                right: 0;
                flex-direction: column;
                gap: 0;
                background: #0d0d1a;
                border-bottom: 2px solid {p['acento']};
                padding: 8px 0;
            }}
            .nav-links.open {{ display: flex; }}
            .nav-link {{
                padding: 14px 6%;
                border-bottom: 1px solid rgba(255,255,255,0.08);
                color: rgba(255,255,255,0.85);
            }}
            .nav-hamburger {{ display: flex; }}
        }}
    </style>
    <nav class="navbar">
        <a href="#inicio" class="nav-brand">{marca}</a>
        <div class="nav-links" id="nav-links">
{links_html}
        </div>
        <div style="display:flex;align-items:center;gap:12px">
            <a href="{wa_link}" target="_blank" class="nav-cta">
                <svg style="width:15px;height:15px;flex-shrink:0" viewBox="0 0 24 24" fill="white"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
                {cta_text}
            </a>
            <button class="nav-hamburger" onclick="toggleNavMenu()" aria-label="Menú">
                <span></span><span></span><span></span>
            </button>
        </div>
    </nav>
    <script>
        function toggleNavMenu() {{
            document.getElementById('nav-links').classList.toggle('open');
        }}
    </script>"""


# ── Sección Hero ──────────────────────────────────────────────────────────────

def _html_seccion_hero(hero, wa_link, p, tipo_hero):
    if tipo_hero == "tipo_2":
        return _hero_imagen_izquierda(hero, wa_link, p)
    elif tipo_hero == "tipo_3":
        return _hero_central(hero, wa_link, p)
    else:
        return _hero_texto_izquierda(hero, wa_link, p)


def _cta_btn(wa_link, cta_text):
    return f"""<a href="{wa_link}" target="_blank" class="cta-btn">
                    {WA_ICON_SVG}
                    {cta_text}
                </a>"""


def _hero_texto_izquierda(hero, wa_link, p):
    return f"""
    <style>
        .hero {{
            min-height: 100vh;
            background: {p['bg_gradient']};
            display: flex;
            align-items: center;
            padding-top: 68px;
        }}
        .hero-inner {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 60px;
            align-items: center;
            width: 100%;
            max-width: 1100px;
            margin: 0 auto;
            padding: 60px 6%;
        }}
        .hero-content {{ text-align: left; }}
        .hero-etiqueta {{
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
        .hero-titulo {{
            font-size: 2.8rem;
            font-weight: 800;
            color: {p['texto']};
            line-height: 1.15;
            margin-bottom: 20px;
        }}
        .hero-subtitulo {{
            font-size: 1.1rem;
            color: {p['subtexto']};
            line-height: 1.7;
            margin-bottom: 36px;
        }}
        .cta-btn {{
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
            box-shadow: 0 4px 20px rgba(37,211,102,0.4);
        }}
        .cta-btn:hover {{ transform: translateY(-2px); box-shadow: 0 6px 28px rgba(37,211,102,0.5); }}
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
            .hero-inner {{ grid-template-columns: 1fr; gap: 40px; padding: 40px 5%; }}
            .hero-titulo {{ font-size: 2rem; }}
        }}
    </style>
    <section class="hero" id="inicio">
        <div class="hero-inner">
            <div class="hero-content">
                <span class="hero-etiqueta">{hero['etiqueta']}</span>
                <h1 class="hero-titulo">{hero['titulo']}</h1>
                <p class="hero-subtitulo">{hero['subtitulo']}</p>
                {_cta_btn(wa_link, hero['cta'])}
            </div>
            <div class="foto-placeholder"><span>📷 Tu foto aquí</span></div>
        </div>
    </section>"""


def _hero_imagen_izquierda(hero, wa_link, p):
    return f"""
    <style>
        .hero {{
            min-height: 100vh;
            background: {p['bg_gradient']};
            display: flex;
            align-items: center;
            padding-top: 68px;
        }}
        .hero-inner {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 60px;
            align-items: center;
            width: 100%;
            max-width: 1100px;
            margin: 0 auto;
            padding: 60px 6%;
        }}
        .hero-content {{ text-align: left; }}
        .hero-etiqueta {{
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
        .hero-titulo {{
            font-size: 2.8rem;
            font-weight: 800;
            color: {p['texto']};
            line-height: 1.15;
            margin-bottom: 20px;
        }}
        .hero-subtitulo {{
            font-size: 1.1rem;
            color: {p['subtexto']};
            line-height: 1.7;
            margin-bottom: 36px;
        }}
        .cta-btn {{
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
            box-shadow: 0 4px 20px rgba(37,211,102,0.4);
        }}
        .cta-btn:hover {{ transform: translateY(-2px); box-shadow: 0 6px 28px rgba(37,211,102,0.5); }}
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
            .hero-inner {{ grid-template-columns: 1fr; gap: 40px; padding: 40px 5%; }}
            .hero-titulo {{ font-size: 2rem; }}
        }}
    </style>
    <section class="hero" id="inicio">
        <div class="hero-inner">
            <div class="foto-placeholder"><span>📷 Tu foto aquí</span></div>
            <div class="hero-content">
                <span class="hero-etiqueta">{hero['etiqueta']}</span>
                <h1 class="hero-titulo">{hero['titulo']}</h1>
                <p class="hero-subtitulo">{hero['subtitulo']}</p>
                {_cta_btn(wa_link, hero['cta'])}
            </div>
        </div>
    </section>"""


def _hero_central(hero, wa_link, p):
    return f"""
    <style>
        .hero {{
            min-height: 100vh;
            background: {p['bg_gradient']};
            display: flex;
            align-items: center;
            padding-top: 68px;
        }}
        .hero-inner {{
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 60px 20px;
            width: 100%;
        }}
        .hero-content {{ max-width: 720px; width: 100%; }}
        .hero-etiqueta {{
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
        .hero-titulo {{
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
        .hero-subtitulo {{
            font-size: 1.2rem;
            color: {p['subtexto']};
            line-height: 1.7;
            margin-bottom: 40px;
            max-width: 580px;
            margin-left: auto;
            margin-right: auto;
        }}
        .cta-btn {{
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
            box-shadow: 0 4px 20px rgba(37,211,102,0.4);
        }}
        .cta-btn:hover {{ transform: translateY(-2px); box-shadow: 0 6px 28px rgba(37,211,102,0.5); }}
        @media (max-width: 600px) {{
            .hero-titulo {{ font-size: 2rem; }}
            .hero-subtitulo {{ font-size: 1rem; }}
        }}
    </style>
    <section class="hero" id="inicio">
        <div class="hero-inner">
            <div class="hero-content">
                <span class="hero-etiqueta">{hero['etiqueta']}</span>
                <h1 class="hero-titulo">{hero['titulo']}</h1>
                <div class="foto-placeholder"><span>📷 Tu foto aquí</span></div>
                <p class="hero-subtitulo">{hero['subtitulo']}</p>
                {_cta_btn(wa_link, hero['cta'])}
            </div>
        </div>
    </section>"""


# ── Sección Propuesta de Valor ────────────────────────────────────────────────

def _html_seccion_propuesta_valor(pv, p):
    cards_html = ""
    for i, card in enumerate(pv["cards"]):
        numero = str(i + 1).zfill(2)
        cards_html += f"""
            <div class="pv-card">
                <div class="pv-card-numero">{numero}</div>
                <h3 class="pv-card-titulo">{card['titulo']}</h3>
                <p class="pv-card-desc">{card['descripcion']}</p>
            </div>"""

    return f"""
    <style>
        .pv {{
            background: #ffffff;
            padding: 100px 6%;
        }}
        .pv-container {{
            max-width: 1100px;
            margin: 0 auto;
        }}
        .pv-header {{
            text-align: center;
            margin-bottom: 64px;
        }}
        .pv-etiqueta {{
            display: inline-block;
            font-size: 0.8rem;
            font-weight: 600;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: {p['acento']};
            border: 1px solid {p['acento']};
            padding: 6px 18px;
            border-radius: 50px;
            margin-bottom: 20px;
        }}
        .pv-titulo {{
            font-size: 2.4rem;
            font-weight: 800;
            color: #1a1a2e;
            line-height: 1.2;
            margin-bottom: 16px;
        }}
        .pv-subtitulo {{
            font-size: 1.1rem;
            color: #6b7280;
            line-height: 1.7;
            max-width: 580px;
            margin: 0 auto;
        }}
        .pv-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 28px;
        }}
        .pv-card {{
            background: #f9fafb;
            border-radius: 16px;
            padding: 36px 28px;
            border-top: 4px solid {p['acento']};
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .pv-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 32px rgba(0,0,0,0.08);
        }}
        .pv-card-numero {{
            font-size: 2rem;
            font-weight: 800;
            color: {p['acento']};
            opacity: 0.4;
            margin-bottom: 16px;
            line-height: 1;
        }}
        .pv-card-titulo {{
            font-size: 1.1rem;
            font-weight: 700;
            color: #1a1a2e;
            margin-bottom: 12px;
            line-height: 1.3;
        }}
        .pv-card-desc {{
            font-size: 0.95rem;
            color: #6b7280;
            line-height: 1.65;
        }}
        @media (max-width: 900px) {{
            .pv-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .pv-titulo {{ font-size: 1.9rem; }}
        }}
        @media (max-width: 560px) {{
            .pv-grid {{ grid-template-columns: 1fr; }}
            .pv {{ padding: 60px 5%; }}
        }}
    </style>
    <section class="pv" id="propuesta-valor">
        <div class="pv-container">
            <div class="pv-header">
                <span class="pv-etiqueta">{pv['etiqueta']}</span>
                <h2 class="pv-titulo">{pv['titulo']}</h2>
                <p class="pv-subtitulo">{pv['subtitulo']}</p>
            </div>
            <div class="pv-grid">{cards_html}
            </div>
        </div>
    </section>"""


# ── Rutas Flask ───────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html", paletas=PALETAS, tipos_hero=TIPOS_HERO)


def _contenido_desde_form(form):
    cards = []
    card_count = int(form.get("card_count", 0))
    for i in range(card_count):
        cards.append({
            "titulo":      form.get(f"card_{i}_titulo", ""),
            "descripcion": form.get(f"card_{i}_descripcion", ""),
        })
    return {
        "hero": {
            "etiqueta":  form["hero_etiqueta"],
            "titulo":    form["hero_titulo"],
            "subtitulo": form["hero_subtitulo"],
            "cta":       form["hero_cta"],
        },
        "propuesta_valor": {
            "etiqueta":  form["pv_etiqueta"],
            "titulo":    form["pv_titulo"],
            "subtitulo": form["pv_subtitulo"],
            "cards":     cards,
        },
    }


@app.route("/generar", methods=["POST"])
def generar():
    profesion      = request.form["profesion"]
    marca          = request.form["marca"]
    valor          = request.form["valor"]
    diferenciacion = request.form["diferenciacion"]
    cliente_ideal  = request.form["cliente_ideal"]
    pilares        = request.form["pilares"]
    whatsapp       = request.form["whatsapp"]
    paleta_key     = request.form.get("paleta", "profesional")
    tipo_hero      = request.form.get("tipo_hero", "tipo_1")

    contenido   = generar_contenido(profesion, marca, valor, diferenciacion, cliente_ideal, pilares)
    html_output = generar_html_pagina(marca, contenido, whatsapp, paleta_key, tipo_hero)

    return render_template(
        "editar.html",
        contenido=contenido,
        html_output=html_output,
        marca=marca,
        whatsapp=whatsapp,
        paleta=paleta_key,
        tipo_hero=tipo_hero,
    )


@app.route("/actualizar-preview", methods=["POST"])
def actualizar_preview():
    marca      = request.form["marca"]
    whatsapp   = request.form["whatsapp"]
    paleta_key = request.form["paleta"]
    tipo_hero  = request.form["tipo_hero"]
    contenido  = _contenido_desde_form(request.form)
    html_output = generar_html_pagina(marca, contenido, whatsapp, paleta_key, tipo_hero)
    return html_output, 200, {"Content-Type": "text/plain; charset=utf-8"}


@app.route("/preview", methods=["POST"])
def preview():
    marca      = request.form["marca"]
    whatsapp   = request.form["whatsapp"]
    paleta_key = request.form["paleta"]
    tipo_hero  = request.form["tipo_hero"]
    contenido  = _contenido_desde_form(request.form)
    html_output = generar_html_pagina(marca, contenido, whatsapp, paleta_key, tipo_hero)
    return render_template("preview.html", html_output=html_output, marca=marca)


if __name__ == "__main__":
    app.run(debug=True)
