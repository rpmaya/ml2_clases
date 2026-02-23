"""
Ejemplo 3.2 - Anatomia de una Llamada API
ML2 - Unidad 3, Sesion 2: Acceso Programatico a LLMs

Este script muestra la estructura completa de una llamada
a la Chat Completion API usando OpenRouter como proxy.
Al usar la libreria openai con base_url de OpenRouter,
la sintaxis es identica a OpenAI directo.
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
    # Modelo a usar (gratuito via OpenRouter)
    model="arcee-ai/trinity-large-preview:free",

    # Historial de mensajes (roles: system, user, assistant)
    messages=[
        {"role": "system", "content": "Eres un asistente util."},
        {"role": "user", "content": "Hola, explica que es una API en una frase."}
    ],

    # Parametros de generacion
    temperature=0.7,       # Creatividad (0=determinista, 2=muy aleatorio)
    max_tokens=500,        # Limite de tokens en la respuesta
    top_p=0.9,             # Nucleus sampling

    # Opcionales
    n=1,                   # Numero de respuestas a generar
    stop=None,             # Tokens de parada
    presence_penalty=0,    # Penaliza repeticion de temas (-2 a 2)
    frequency_penalty=0    # Penaliza repeticion de palabras (-2 a 2)
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
print(f"Finish reason: {response.choices[0].finish_reason}")
