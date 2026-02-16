"""
Ejemplo 3.2 - Anatomía de una Llamada API
ML2 - Unidad 2, Sesión 2: Desarrollo con LLMs

Este script muestra la estructura completa de una llamada
a la Chat Completion API de OpenAI.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# ============================================
# CONFIGURACIÓN - Carga API Key desde .env
# ============================================
# Busca el .env en la carpeta ejemplos
load_dotenv(Path(__file__).parent / ".env")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ============================================
# LLAMADA A LA API
# ============================================
response = client.chat.completions.create(
    # Modelo a usar
    model="gpt-4.1-nano",

    # Historial de mensajes (roles: system, user, assistant)
    messages=[
        {"role": "system", "content": "Eres un asistente útil."},
        {"role": "user", "content": "Hola, explica qué es una API en una frase."}
    ],

    # Parámetros de generación
    temperature=0.7,       # Creatividad (0=determinista, 2=muy aleatorio)
    max_tokens=500,        # Límite de tokens en la respuesta
    top_p=0.9,             # Nucleus sampling

    # Opcionales
    n=1,                   # Número de respuestas a generar
    stop=None,             # Tokens de parada
    presence_penalty=0,    # Penaliza repetición de temas (-2 a 2)
    frequency_penalty=0    # Penaliza repetición de palabras (-2 a 2)
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
