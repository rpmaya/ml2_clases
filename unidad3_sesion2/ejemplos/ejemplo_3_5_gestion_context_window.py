"""
Ejemplo 3.5 - Gestion del Context Window
ML2 - Unidad 3, Sesion 2: Acceso Programatico a LLMs

El historial crece con cada turno y puede exceder el limite
de tokens del modelo. Este script muestra dos estrategias:
  1. Truncar mensajes antiguos (mantener los ultimos N)
  2. Resumir el historial con el propio modelo

Ejecuta este ejemplo despues del 3.4 para entender el problema.
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


# ============================================
# ESTRATEGIA 1: Truncar mensajes antiguos
# ============================================
def truncate_conversation(messages, max_messages=10):
    """Mantiene el system message + los ultimos N mensajes."""
    if len(messages) <= max_messages + 1:
        return messages  # No hace falta truncar

    system = messages[0]              # Siempre conservar system
    recent = messages[-max_messages:]  # Ultimos N mensajes
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
        model=MODEL,
        messages=[
            {"role": "system", "content": "Resume esta conversacion en 2-3 frases. Captura los puntos clave."},
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
        {"role": "system", "content": f"Resumen de la conversacion previa: {summary}"},
    ] + recent


# ============================================
# DEMOSTRACION
# ============================================
print("=" * 60)
print("DEMO: Simulando una conversacion larga")
print("=" * 60)

# Simulamos un historial largo (como si ya hubieramos tenido muchos turnos)
conversation = [
    {"role": "system", "content": "Eres un tutor de Python."},
    {"role": "user", "content": "Que es una variable?"},
    {"role": "assistant", "content": "Una variable es un nombre que almacena un valor en memoria."},
    {"role": "user", "content": "Y que tipos de datos hay?"},
    {"role": "assistant", "content": "Los tipos basicos son: int, float, str, bool, list, dict, tuple."},
    {"role": "user", "content": "Explicame las listas."},
    {"role": "assistant", "content": "Una lista es una coleccion ordenada y mutable. Se crea con corchetes: mi_lista = [1, 2, 3]."},
    {"role": "user", "content": "Como recorro una lista?"},
    {"role": "assistant", "content": "Con un bucle for: for elemento in mi_lista: print(elemento)."},
    {"role": "user", "content": "Y los diccionarios?"},
    {"role": "assistant", "content": "Un diccionario almacena pares clave-valor: mi_dict = {'nombre': 'Ana', 'edad': 25}."},
    {"role": "user", "content": "Que son las funciones?"},
    {"role": "assistant", "content": "Son bloques de codigo reutilizable que se definen con def."},
    {"role": "user", "content": "Dame un ejemplo de funcion."},
    {"role": "assistant", "content": "def saludar(nombre): return f'Hola, {nombre}!'. Se llama con saludar('Ana')."},
]

print(f"\n  Mensajes en historial: {len(conversation)}")

# --- Estrategia 1: Truncar ---
print("\n" + "-" * 60)
print("ESTRATEGIA 1: Truncar (mantener ultimos 4 mensajes)")
print("-" * 60)

truncated = truncate_conversation(conversation, max_messages=4)
print(f"Mensajes antes: {len(conversation)} -> despues: {len(truncated)}")
for msg in truncated:
    role = msg["role"].upper()
    content = msg["content"][:70] + "..." if len(msg["content"]) > 70 else msg["content"]
    print(f"  {role}: {content}")

# Verificar que aun funciona
response = client.chat.completions.create(
    model=MODEL,
    messages=truncated + [{"role": "user", "content": "De que hemos hablado?"}],
    max_tokens=150
)
print(f"\n  Con truncado, el modelo recuerda: {response.choices[0].message.content}")

# --- Estrategia 2: Resumir + Truncar ---
print("\n" + "-" * 60)
print("ESTRATEGIA 2: Resumir historial antiguo + mantener recientes")
print("-" * 60)

smart = smart_truncate(conversation, max_messages=4)
print(f"Mensajes antes: {len(conversation)} -> despues: {len(smart)}")
for msg in smart:
    role = msg["role"].upper()
    content = msg["content"][:70] + "..." if len(msg["content"]) > 70 else msg["content"]
    print(f"  {role}: {content}")

# Verificar que conserva mas contexto
response = client.chat.completions.create(
    model=MODEL,
    messages=smart + [{"role": "user", "content": "De que hemos hablado?"}],
    max_tokens=150
)
print(f"\n  Con resumen, el modelo recuerda: {response.choices[0].message.content}")

# --- Comparacion ---
print("\n" + "=" * 60)
print("Comparacion:")
print("   Truncar  -> Rapido y barato, pero pierde contexto antiguo")
print("   Resumir  -> Conserva contexto, pero cuesta tokens extra")
print("   En produccion se suelen combinar ambas estrategias")
print("=" * 60)
