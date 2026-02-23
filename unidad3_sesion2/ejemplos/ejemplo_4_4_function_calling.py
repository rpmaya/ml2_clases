"""
Ejemplo 4.4 - Function Calling / Tool Use
ML2 - Unidad 3, Sesion 2: Acceso Programatico a LLMs

Function Calling permite que el modelo decida cuando necesita
invocar una herramienta externa. El modelo NO ejecuta la funcion:
genera los argumentos y la aplicacion la ejecuta.

Flujo: Usuario -> Modelo -> Decide usar tool -> App ejecuta
       -> Resultado al modelo -> Respuesta final

Usa OpenRouter con modelo gratuito.
Nota: No todos los modelos gratuitos soportan function calling.
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
# FUNCIONES SIMULADAS (en produccion serian APIs reales)
# ============================================
def obtener_clima(ciudad, unidad="celsius"):
    """Simula una API de clima."""
    climas = {
        "madrid": {"temperatura": 22, "condicion": "soleado", "humedad": 45},
        "barcelona": {"temperatura": 19, "condicion": "nublado", "humedad": 65},
        "londres": {"temperatura": 12, "condicion": "lluvioso", "humedad": 80},
    }
    clima = climas.get(ciudad.lower(), {"temperatura": 20, "condicion": "desconocido", "humedad": 50})
    clima["ciudad"] = ciudad
    clima["unidad"] = unidad
    return clima


def buscar_restaurante(ciudad, tipo_cocina="cualquiera"):
    """Simula una API de busqueda de restaurantes."""
    restaurantes = {
        "madrid": {"nombre": "Casa Lucio", "tipo": "espanola", "puntuacion": 4.5},
        "barcelona": {"nombre": "Can Culleretes", "tipo": "catalana", "puntuacion": 4.3},
    }
    rest = restaurantes.get(ciudad.lower(), {"nombre": "Restaurante Local", "tipo": tipo_cocina, "puntuacion": 4.0})
    rest["ciudad"] = ciudad
    return rest


# ============================================
# DEFINIR HERRAMIENTAS PARA EL MODELO
# ============================================
tools = [
    {
        "type": "function",
        "function": {
            "name": "obtener_clima",
            "description": "Obtiene el clima actual de una ciudad",
            "parameters": {
                "type": "object",
                "properties": {
                    "ciudad": {
                        "type": "string",
                        "description": "Nombre de la ciudad"
                    },
                    "unidad": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Unidad de temperatura"
                    }
                },
                "required": ["ciudad"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "buscar_restaurante",
            "description": "Busca un restaurante recomendado en una ciudad",
            "parameters": {
                "type": "object",
                "properties": {
                    "ciudad": {
                        "type": "string",
                        "description": "Nombre de la ciudad"
                    },
                    "tipo_cocina": {
                        "type": "string",
                        "description": "Tipo de cocina preferida"
                    }
                },
                "required": ["ciudad"]
            }
        }
    }
]

# Mapa de funciones disponibles
funciones_disponibles = {
    "obtener_clima": obtener_clima,
    "buscar_restaurante": buscar_restaurante,
}


# ============================================
# FUNCION PARA PROCESAR FUNCTION CALLING
# ============================================
def chat_con_herramientas(pregunta):
    """Procesa una pregunta usando function calling."""
    print(f"\n  Usuario: {pregunta}")

    messages = [
        {"role": "system", "content": "Eres un asistente de viajes util. Usa las herramientas disponibles cuando necesites datos reales."},
        {"role": "user", "content": pregunta}
    ]

    # 1. Primera llamada: el modelo decide si usar herramientas
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    assistant_message = response.choices[0].message

    # 2. Si el modelo quiere usar herramientas
    if assistant_message.tool_calls:
        print(f"  Modelo quiere usar herramientas:")
        messages.append(assistant_message)

        for tool_call in assistant_message.tool_calls:
            func_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            print(f"    -> {func_name}({args})")

            # 3. Ejecutar la funcion real
            funcion = funciones_disponibles[func_name]
            resultado = funcion(**args)
            print(f"    <- Resultado: {resultado}")

            # 4. Enviar resultado al modelo
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(resultado)
            })

        # 5. Segunda llamada: el modelo genera respuesta final
        response_final = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )
        respuesta = response_final.choices[0].message.content
    else:
        # El modelo respondio sin usar herramientas
        respuesta = assistant_message.content

    print(f"  Asistente: {respuesta}")
    return respuesta


# ============================================
# DEMOSTRACION
# ============================================
print("=" * 60)
print("DEMO: Function Calling / Tool Use")
print("=" * 60)

# Pregunta que requiere la herramienta de clima
chat_con_herramientas("Que tiempo hace en Madrid?")

# Pregunta que requiere la herramienta de restaurantes
chat_con_herramientas("Recomiendame un restaurante en Barcelona")

# Pregunta que NO requiere herramientas
chat_con_herramientas("Que idioma se habla en Francia?")

print("\n" + "=" * 60)
print("Function Calling es la base de los AGENTES (Unidad 4).")
print("El modelo decide QUE herramienta usar y con que parametros.")
print("Tu aplicacion ejecuta la funcion y devuelve el resultado.")
print("=" * 60)
