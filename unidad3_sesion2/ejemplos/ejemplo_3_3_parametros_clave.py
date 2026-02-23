"""
Ejemplo 3.3 - Parametros Clave: Temperature y Top-p
ML2 - Unidad 3, Sesion 2: Acceso Programatico a LLMs

Demuestra como temperature y top_p afectan la generacion.
Ejecuta la misma pregunta con distintas configuraciones
para que puedas comparar los resultados.

Usa OpenRouter con modelo gratuito.
"""

import os
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
PROMPT = "Inventa un nombre creativo para una cafeteria."

messages = [
    {"role": "system", "content": "Eres un experto en branding. Responde solo con el nombre, sin explicacion."},
    {"role": "user", "content": PROMPT}
]

# ============================================
# EXPERIMENTO 1: Variando Temperature
# ============================================
print("=" * 60)
print("EXPERIMENTO 1: Efecto de Temperature")
print("Mismo prompt, 3 respuestas por nivel de temperature")
print("=" * 60)

for temp in [0.0, 0.7, 1.5]:
    print(f"\n  Temperature = {temp}")
    for i in range(3):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=temp,
            max_tokens=50
        )
        nombre = response.choices[0].message.content.strip()
        print(f"   Intento {i+1}: {nombre}")

# ============================================
# EXPERIMENTO 2: Variando Top-p
# ============================================
print("\n" + "=" * 60)
print("EXPERIMENTO 2: Efecto de Top-p (Nucleus Sampling)")
print("Temperature fija en 1.0, variamos top_p")
print("=" * 60)

for top_p in [0.1, 0.5, 0.95]:
    print(f"\n  Top-p = {top_p}")
    for i in range(3):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=1.0,
            top_p=top_p,
            max_tokens=50
        )
        nombre = response.choices[0].message.content.strip()
        print(f"   Intento {i+1}: {nombre}")

# ============================================
# EXPERIMENTO 3: Max Tokens (respuesta cortada)
# ============================================
print("\n" + "=" * 60)
print("EXPERIMENTO 3: Efecto de Max Tokens")
print("=" * 60)

messages_largo = [
    {"role": "system", "content": "Eres un asistente util."},
    {"role": "user", "content": "Explica que es machine learning."}
]

for max_t in [10, 50, 200]:
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages_largo,
        temperature=0.7,
        max_tokens=max_t
    )
    texto = response.choices[0].message.content
    reason = response.choices[0].finish_reason
    print(f"\n  Max Tokens = {max_t} (finish_reason: {reason})")
    print(f"   {texto}")

print("\n" + "=" * 60)
print("Observa:")
print("   - Temperature 0 = respuestas casi identicas (determinista)")
print("   - Temperature alta = mas variedad y creatividad")
print("   - Top-p bajo = vocabulario mas conservador")
print("   - Max tokens bajo = respuesta cortada (finish_reason: 'length')")
print("=" * 60)
