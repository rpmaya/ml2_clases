"""
Ejemplo 3.4 - Manteniendo Contexto en Conversaciones Multi-turno
ML2 - Unidad 2, Sesión 2: Desarrollo con LLMs

El modelo NO tiene memoria. Cada llamada a la API es independiente.
Para simular una conversación, debemos enviar TODO el historial
de mensajes en cada llamada.

Este script implementa un chatbot interactivo que mantiene contexto.
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

# ============================================
# HISTORIAL DE CONVERSACIÓN
# ============================================
# El system message define la personalidad del asistente.
# Se mantiene SIEMPRE como primer mensaje.
conversation = [
    {"role": "system", "content": "Eres un tutor de Python. Explicas conceptos de forma clara y con ejemplos cortos."}
]


def chat(user_message):
    """Envía un mensaje y mantiene el historial completo."""

    # 1. Añadir mensaje del usuario al historial
    conversation.append({"role": "user", "content": user_message})

    # 2. Llamar a la API con TODO el historial
    #    El modelo "ve" toda la conversación previa
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=conversation,
        temperature=0.7,
        max_tokens=500
    )

    # 3. Extraer la respuesta del asistente
    assistant_message = response.choices[0].message.content

    # 4. Añadir respuesta al historial (para la próxima llamada)
    conversation.append({"role": "assistant", "content": assistant_message})

    # 5. Mostrar uso de tokens (crece con cada turno)
    tokens = response.usage.total_tokens
    return assistant_message, tokens


# ============================================
# DEMOSTRACIÓN: Conversación multi-turno
# ============================================
print("=" * 60)
print("DEMO: Conversación multi-turno con contexto")
print("=" * 60)

# Turno 1: Pregunta inicial
pregunta1 = "¿Qué es una lista en Python?"
print(f"\n👤 Usuario: {pregunta1}")
respuesta1, tokens1 = chat(pregunta1)
print(f"🤖 Asistente: {respuesta1}")
print(f"   [Tokens usados: {tokens1}]")

# Turno 2: Pregunta de seguimiento (usa contexto previo)
pregunta2 = "¿Y cómo le agrego un elemento?"
print(f"\n👤 Usuario: {pregunta2}")
respuesta2, tokens2 = chat(pregunta2)
print(f"🤖 Asistente: {respuesta2}")
print(f"   [Tokens usados: {tokens2}]")

# Turno 3: Referencia implícita al contexto
pregunta3 = "Dame un ejemplo completo con lo que me explicaste."
print(f"\n👤 Usuario: {pregunta3}")
respuesta3, tokens3 = chat(pregunta3)
print(f"🤖 Asistente: {respuesta3}")
print(f"   [Tokens usados: {tokens3}]")

# ============================================
# MOSTRAR EL HISTORIAL COMPLETO
# ============================================
print("\n" + "=" * 60)
print("HISTORIAL COMPLETO ENVIADO EN LA ÚLTIMA LLAMADA")
print("=" * 60)
for i, msg in enumerate(conversation):
    role = msg["role"].upper()
    content = msg["content"][:80] + "..." if len(msg["content"]) > 80 else msg["content"]
    print(f"  [{i}] {role}: {content}")

print(f"\n📊 Mensajes en historial: {len(conversation)}")
print(f"📊 Tokens en última llamada: {tokens3}")
print(f"\n⚠️  Nota: Los tokens CRECEN con cada turno porque enviamos")
print(f"   todo el historial. Esto tiene implicaciones de costo y")
print(f"   límite de context window (ver sección 3.5).")
