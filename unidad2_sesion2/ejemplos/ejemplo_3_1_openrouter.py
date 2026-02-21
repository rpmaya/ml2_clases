"""
Ejemplo 3.1 - Primera Llamada a un LLM via OpenRouter: https://openrouter.ai/ (obtener la Key)
ML2 - Unidad 2, Sesion 2: Desarrollo con LLMs

Usa la librería openai apuntando a OpenRouter como proxy.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# ============================================
# CONFIGURACION - Carga API Key desde .env
# ============================================
load_dotenv(Path(__file__).parent / ".env")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# ============================================
# LLAMADA A LA API
# ============================================
response = client.chat.completions.create(
    # Modelos free a usar: https://openrouter.ai/models?q=free&order=most-popular
    model="arcee-ai/trinity-large-preview:free",
    messages=[
        {"role": "system", "content": "Eres un asistente util."},
        {"role": "user", "content": "Hola, explica qué es un LLM en una frase."}
    ],
    temperature=0.7,
    max_tokens=500,
)

# ============================================
# ACCEDER A LA RESPUESTA
# ============================================
print("=== RESPUESTA ===")
print(response.choices[0].message.content)

print("\n=== METADATOS ===")
print(f"Modelo usado: {response.model}")
print(f"Tokens prompt: {response.usage.prompt_tokens}")
print(f"Tokens respuesta: {response.usage.completion_tokens}")
print(f"Tokens totales: {response.usage.total_tokens}")
