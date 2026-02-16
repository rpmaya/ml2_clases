"""
Ejemplo 3.5 - Gestión del Context Window
ML2 - Unidad 2, Sesión 2: Desarrollo con LLMs

El historial crece con cada turno y puede exceder el límite
de tokens del modelo. Este script muestra dos estrategias:
  1. Truncar mensajes antiguos (mantener los últimos N)
  2. Resumir el historial con el propio modelo

Ejecuta este ejemplo después del 3.4 para entender el problema.
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
# ESTRATEGIA 1: Truncar mensajes antiguos
# ============================================
def truncate_conversation(messages, max_messages=10):
    """Mantiene el system message + los últimos N mensajes."""
    if len(messages) <= max_messages + 1:
        return messages  # No hace falta truncar

    system = messages[0]              # Siempre conservar system
    recent = messages[-max_messages:]  # Últimos N mensajes
    return [system] + recent


# ============================================
# ESTRATEGIA 2: Resumir historial antiguo
# ============================================
def summarize_history(messages):
    """Usa el modelo para resumir mensajes antiguos."""
    text = "\n".join(
        f"{m['role']}: {m['content']}" for m in messages
    )
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": "Resume esta conversación en 2-3 frases. Captura los puntos clave."},
            {"role": "user", "content": text}
        ],
        temperature=0.3,
        max_tokens=150
    )
    return response.choices[0].message.content


def smart_truncate(messages, max_messages=6):
    """Combina resumen + truncado para conservar contexto."""
    if len(messages) <= max_messages + 1:
        return messages

    system = messages[0]
    old = messages[1:-max_messages]      # Mensajes que se van a resumir
    recent = messages[-max_messages:]     # Mensajes recientes que se mantienen

    summary = summarize_history(old)

    return [
        system,
        {"role": "system", "content": f"Resumen de la conversación previa: {summary}"},
    ] + recent


# ============================================
# DEMOSTRACIÓN
# ============================================
print("=" * 60)
print("DEMO: Simulando una conversación larga")
print("=" * 60)

# Simulamos un historial largo (como si ya hubiéramos tenido muchos turnos)
conversation = [
    {"role": "system", "content": "Eres un tutor de Python."},
    {"role": "user", "content": "¿Qué es una variable?"},
    {"role": "assistant", "content": "Una variable es un nombre que almacena un valor en memoria."},
    {"role": "user", "content": "¿Y qué tipos de datos hay?"},
    {"role": "assistant", "content": "Los tipos básicos son: int, float, str, bool, list, dict, tuple."},
    {"role": "user", "content": "Explícame las listas."},
    {"role": "assistant", "content": "Una lista es una colección ordenada y mutable. Se crea con corchetes: mi_lista = [1, 2, 3]."},
    {"role": "user", "content": "¿Cómo recorro una lista?"},
    {"role": "assistant", "content": "Con un bucle for: for elemento in mi_lista: print(elemento)."},
    {"role": "user", "content": "¿Y los diccionarios?"},
    {"role": "assistant", "content": "Un diccionario almacena pares clave-valor: mi_dict = {'nombre': 'Ana', 'edad': 25}."},
    {"role": "user", "content": "¿Qué son las funciones?"},
    {"role": "assistant", "content": "Son bloques de código reutilizable que se definen con def."},
    {"role": "user", "content": "Dame un ejemplo de función."},
    {"role": "assistant", "content": "def saludar(nombre): return f'Hola, {nombre}!'. Se llama con saludar('Ana')."},
]

print(f"\n📊 Mensajes en historial: {len(conversation)}")

# --- Estrategia 1: Truncar ---
print("\n" + "-" * 60)
print("ESTRATEGIA 1: Truncar (mantener últimos 4 mensajes)")
print("-" * 60)

truncated = truncate_conversation(conversation, max_messages=4)
print(f"Mensajes antes: {len(conversation)} → después: {len(truncated)}")
for msg in truncated:
    role = msg["role"].upper()
    content = msg["content"][:70] + "..." if len(msg["content"]) > 70 else msg["content"]
    print(f"  {role}: {content}")

# Verificar que aún funciona
response = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=truncated + [{"role": "user", "content": "¿De qué hemos hablado?"}],
    max_tokens=150
)
print(f"\n🤖 Con truncado, el modelo recuerda: {response.choices[0].message.content}")

# --- Estrategia 2: Resumir + Truncar ---
print("\n" + "-" * 60)
print("ESTRATEGIA 2: Resumir historial antiguo + mantener recientes")
print("-" * 60)

smart = smart_truncate(conversation, max_messages=4)
print(f"Mensajes antes: {len(conversation)} → después: {len(smart)}")
for msg in smart:
    role = msg["role"].upper()
    content = msg["content"][:70] + "..." if len(msg["content"]) > 70 else msg["content"]
    print(f"  {role}: {content}")

# Verificar que conserva más contexto
response = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=smart + [{"role": "user", "content": "¿De qué hemos hablado?"}],
    max_tokens=150
)
print(f"\n🤖 Con resumen, el modelo recuerda: {response.choices[0].message.content}")

# --- Comparación ---
print("\n" + "=" * 60)
print("💡 Comparación:")
print("   Truncar  → Rápido y barato, pero pierde contexto antiguo")
print("   Resumir  → Conserva contexto, pero cuesta tokens extra")
print("   En producción se suelen combinar ambas estrategias")
print("=" * 60)
