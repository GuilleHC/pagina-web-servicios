import anthropic
import urllib.parse

def preguntar(pregunta: str) -> str:
    print(f"\n{pregunta}")
    return input("> ").strip()

def generar_hero(marca: str, valor: str, diferenciacion: str, cliente_ideal: str) -> dict:
    client = anthropic.Anthropic()

    prompt = f"""Eres un experto en marketing y copywriting para emprendedores latinoamericanos.
Con la siguiente información, genera el contenido para la sección Hero de una página web de servicios.

Información del negocio:
- Nombre de la marca: {marca}
- Valor que entrega: {valor}
- Diferenciación: {diferenciacion}
- Cliente ideal: {cliente_ideal}

Genera exactamente estos 3 elementos en formato JSON (solo el JSON, sin texto adicional ni backticks):
{{
  "slogan": "Frase principal impactante de máximo 10 palabras, directa al dolor o deseo del cliente ideal",
  "subtitulo": "Descripción de la propuesta de valor en 1-2 oraciones, máximo 25 palabras, clara y específica",
  "cta": "Texto del botón de WhatsApp, máximo 5 palabras, acción concreta"
}}

Reglas:
- El slogan debe hablarle directamente al cliente ideal
- El subtítulo debe mencionar el beneficio concreto y la diferenciación
- El CTA debe generar urgencia o facilitar el primer paso
- Usa español latinoamericano, tono cercano y profesional
"""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    import json
    contenido = message.content[0].text.strip()
    return json.loads(contenido)

def generar_html_hero(marca: str, hero: dict, whatsapp_numero: str) -> str:
    slogan = hero["slogan"]
    subtitulo = hero["subtitulo"]
    cta = hero["cta"]

    mensaje_wa = urllib.parse.quote(f"Hola {marca}, me interesa saber más sobre sus servicios.")
    wa_link = f"https://wa.me/{whatsapp_numero}?text={mensaje_wa}"

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{marca}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', sans-serif; }}

        .hero {{
            min-height: 100vh;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 40px 20px;
        }}

        .hero-content {{
            max-width: 750px;
        }}

        .marca {{
            font-size: 1rem;
            font-weight: 600;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: #e94560;
            margin-bottom: 24px;
        }}

        .slogan {{
            font-size: 3rem;
            font-weight: 800;
            color: #ffffff;
            line-height: 1.2;
            margin-bottom: 24px;
        }}

        .subtitulo {{
            font-size: 1.2rem;
            color: #a8b2c1;
            line-height: 1.7;
            margin-bottom: 40px;
            max-width: 600px;
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
            box-shadow: 0 4px 20px rgba(37, 211, 102, 0.4);
        }}

        .cta-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 28px rgba(37, 211, 102, 0.5);
        }}

        .wa-icon {{
            width: 24px;
            height: 24px;
        }}

        @media (max-width: 600px) {{
            .slogan {{ font-size: 2rem; }}
        }}
    </style>
</head>
<body>
    <section class="hero">
        <div class="hero-content">
            <p class="marca">{marca}</p>
            <h1 class="slogan">{slogan}</h1>
            <p class="subtitulo">{subtitulo}</p>
            <a href="{wa_link}" target="_blank" class="cta-btn">
                <svg class="wa-icon" viewBox="0 0 24 24" fill="white" xmlns="http://www.w3.org/2000/svg">
                    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
                </svg>
                {cta}
            </a>
        </div>
    </section>
</body>
</html>"""
    return html

def main():
    print("=" * 50)
    print("  🚀 GENERADOR DE PÁGINA WEB - SECCIÓN HERO")
    print("=" * 50)
    print("\nResponde estas preguntas para crear tu Hero:\n")

    marca = preguntar("1. ¿Cómo se llama tu marca o negocio?")
    valor = preguntar("2. ¿Cuál es el valor que entregas a tus clientes? (¿qué problema resuelves o qué beneficio das?)")
    diferenciacion = preguntar("3. ¿Cómo te diferencias de otros o de las alternativas que existen?")
    cliente_ideal = preguntar("4. Descríbeme tu perfil de cliente ideal (quién es, qué necesita, qué siente)")
    whatsapp = preguntar("5. ¿Cuál es tu número de WhatsApp? (con código de país, ej: 56912345678)")

    print("\n⏳ Generando tu Hero con IA...")

    try:
        hero = generar_hero(marca, valor, diferenciacion, cliente_ideal)

        print("\n✅ Hero generado:")
        print(f"\n  Slogan:    {hero['slogan']}")
        print(f"  Subtítulo: {hero['subtitulo']}")
        print(f"  CTA:       {hero['cta']}")

        html = generar_html_hero(marca, hero, whatsapp)

        archivo = f"hero_{marca.lower().replace(' ', '_')}.html"
        ruta = f"/mnt/user-data/outputs/{archivo}"
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"\n🎉 ¡Listo! Tu Hero fue guardado en: {archivo}")

    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
