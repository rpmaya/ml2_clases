"""
Ejemplo 3.3 - Parámetros Clave: Temperature y Top-p
ML2 - Unidad 2, Sesión 2: Desarrollo con LLMs

Demuestra cómo temperature y top_p afectan la generación.
Ejecuta la misma pregunta con distintas configuraciones
para que puedas comparar los resultados.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# ============================================
# CONFIGURACIÓN
# ============================================
load_dotenv(Path(__file__).parent / ".env")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PROMPT = "Inventa un nombre creativo para una cafetería."

messages = [
    {"role": "system", "content": "Eres un experto en branding. Responde solo con el nombre, sin explicación."},
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
    print(f"\n🌡️  Temperature = {temp}")
    for i in range(3):
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
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
    print(f"\n🎯 Top-p = {top_p}")
    for i in range(3):
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
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
    {"role": "system", "content": "Eres un asistente útil."},
    {"role": "user", "content": "Explica qué es machine learning."}
]

for max_t in [10, 50, 200]:
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=messages_largo,
        temperature=0.7,
        max_tokens=max_t
    )
    texto = response.choices[0].message.content
    reason = response.choices[0].finish_reason
    print(f"\n📏 Max Tokens = {max_t} (finish_reason: {reason})")
    print(f"   {texto}")

print("\n" + "=" * 60)
print("💡 Observa:")
print("   - Temperature 0 = respuestas casi idénticas (determinista)")
print("   - Temperature alta = más variedad y creatividad")
print("   - Top-p bajo = vocabulario más conservador")
print("   - Max tokens bajo = respuesta cortada (finish_reason: 'length')")
print("=" * 60)
