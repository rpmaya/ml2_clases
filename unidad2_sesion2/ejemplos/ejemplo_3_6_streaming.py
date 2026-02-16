"""
Ejemplo 3.6 - Streaming de Respuestas
ML2 - Unidad 2, Sesión 2: Desarrollo con LLMs

Sin streaming: esperas a que se genere toda la respuesta → llega de golpe.
Con streaming: recibes la respuesta token a token → aparece progresivamente.

Esto mejora la experiencia de usuario en respuestas largas
(es lo que hacen ChatGPT, Claude, etc. en sus interfaces).
"""

import os
import time
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# ============================================
# CONFIGURACIÓN
# ============================================
load_dotenv(Path(__file__).parent / ".env")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

messages = [
    {"role": "system", "content": "Eres un asistente útil. Responde en español."},
    {"role": "user", "content": "Explica qué es el aprendizaje por refuerzo en 3-4 frases."}
]

# ============================================
# SIN STREAMING (comportamiento normal)
# ============================================
print("=" * 60)
print("SIN STREAMING: Esperar respuesta completa")
print("=" * 60)

start = time.time()
response = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=messages,
    temperature=0.7,
    max_tokens=300
)
elapsed = time.time() - start

print(f"\n(Respuesta recibida tras {elapsed:.2f}s de espera)")
print(response.choices[0].message.content)
print(f"\nTokens: {response.usage.total_tokens}")

# ============================================
# CON STREAMING (token a token)
# ============================================
print("\n" + "=" * 60)
print("CON STREAMING: Respuesta progresiva (token a token)")
print("=" * 60)
print()

start = time.time()
first_token_time = None

stream = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=messages,
    temperature=0.7,
    max_tokens=300,
    stream=True  # ← Esto activa el streaming
)

# Cada 'chunk' contiene un fragmento pequeño de la respuesta
for chunk in stream:
    # El contenido viene en chunk.choices[0].delta.content
    content = chunk.choices[0].delta.content
    if content:
        if first_token_time is None:
            first_token_time = time.time() - start
        print(content, end="", flush=True)  # flush=True fuerza la impresión inmediata

elapsed = time.time() - start
print(f"\n\n⏱️  Primer token en: {first_token_time:.2f}s")
print(f"⏱️  Respuesta completa en: {elapsed:.2f}s")

# ============================================
# RESUMEN
# ============================================
print("\n" + "=" * 60)
print("💡 Diferencias clave:")
print("   Sin streaming → El usuario espera sin ver nada")
print("   Con streaming  → El texto aparece mientras se genera")
print()
print("   Útil para: chatbots, interfaces web, respuestas largas")
print("   Nota: Con stream=True NO recibes usage (conteo de tokens)")
print("=" * 60)
