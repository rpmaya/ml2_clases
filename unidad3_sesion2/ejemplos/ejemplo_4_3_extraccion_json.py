"""
Ejemplo 4.3 - Extraccion Estructurada de Informacion (JSON)
ML2 - Unidad 3, Sesion 2: Acceso Programatico a LLMs

Convertir texto no estructurado en datos estructurados
que pueden procesarse programaticamente. El modelo
extrae informacion siguiendo un esquema JSON definido.

Usa OpenRouter con modelo gratuito.
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# ============================================
# CONFIGURACION
# ============================================
load_dotenv(Path(__file__).parent / ".env")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

MODEL = "arcee-ai/trinity-large-preview:free"


# ============================================
# FUNCION DE EXTRACCION ESTRUCTURADA
# ============================================
def extraer_informacion(texto, esquema_json):
    """
    Extrae informacion estructurada de texto libre.

    Args:
        texto: Texto del que extraer informacion
        esquema_json: Ejemplo del formato JSON esperado

    Returns:
        Diccionario con la informacion extraida
    """
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": f"Extrae la informacion del texto proporcionado. "
                           f"Responde SOLO con JSON valido siguiendo este "
                           f"esquema:\n{json.dumps(esquema_json, indent=2)}\n\n"
                           f"Si algun campo no se encuentra en el texto, "
                           f"usa null."
            },
            {
                "role": "user",
                "content": texto
            }
        ],
        temperature=0.0,
    )

    return json.loads(response.choices[0].message.content)


# ============================================
# DEMO 1: Extraer datos de un CV
# ============================================
print("=" * 60)
print("DEMO 1: Extraccion de datos de un CV")
print("=" * 60)

texto_cv = """
Me llamo Maria Garcia Lopez y tengo 28 anos. Soy ingeniera informatica
graduada de la Universidad Politecnica de Madrid en 2019. Actualmente
trabajo como desarrolladora senior en Acme Corp desde 2021. Domino
Python, JavaScript y Go. Mi email es maria.garcia@email.com y vivo
en Madrid. Hablo espanol nativo e ingles avanzado (C1).
"""

esquema_cv = {
    "nombre_completo": "string",
    "edad": "number",
    "email": "string",
    "ciudad": "string",
    "educacion": {
        "titulo": "string",
        "universidad": "string",
        "ano_graduacion": "number"
    },
    "experiencia_actual": {
        "puesto": "string",
        "empresa": "string",
        "desde": "number"
    },
    "habilidades_tecnicas": ["string"],
    "idiomas": [{"idioma": "string", "nivel": "string"}]
}

print("\nTexto original:")
print(f"  {texto_cv.strip()}")

print("\nJSON extraido:")
resultado_cv = extraer_informacion(texto_cv, esquema_cv)
print(json.dumps(resultado_cv, indent=2, ensure_ascii=False))


# ============================================
# DEMO 2: Extraer datos de un evento
# ============================================
print("\n" + "=" * 60)
print("DEMO 2: Extraccion de datos de un evento")
print("=" * 60)

texto_evento = """
El proximo viernes 15 de marzo a las 18:00 se celebrara la conferencia
'Inteligencia Artificial en la Empresa' en el Auditorio Principal del
Centro de Convenciones de Madrid. El ponente sera el Dr. Carlos Ruiz,
director de IA en TechCorp. La entrada es gratuita pero requiere
inscripcion previa en eventos@techcorp.com. Aforo limitado a 200 personas.
"""

esquema_evento = {
    "nombre_evento": "string",
    "fecha": "string",
    "hora": "string",
    "lugar": "string",
    "ponente": {
        "nombre": "string",
        "cargo": "string",
        "empresa": "string"
    },
    "precio": "string",
    "contacto": "string",
    "aforo": "number"
}

print("\nTexto original:")
print(f"  {texto_evento.strip()}")

print("\nJSON extraido:")
resultado_evento = extraer_informacion(texto_evento, esquema_evento)
print(json.dumps(resultado_evento, indent=2, ensure_ascii=False))

print("\n" + "=" * 60)
print("Este patron es muy util para:")
print("   - Parsear emails, facturas, CVs automaticamente")
print("   - Alimentar bases de datos desde texto libre")
print("   - ETL (Extract-Transform-Load) con lenguaje natural")
print("=" * 60)
