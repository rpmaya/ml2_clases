"""
Ejemplo 4.1 - Chatbot con Memoria de Conversacion
ML2 - Unidad 3, Sesion 2: Acceso Programatico a LLMs

Un chatbot que mantiene el historial de la conversacion
para proporcionar respuestas contextualizadas.
Implementa gestion de ventana de contexto para evitar
exceder el limite de tokens.

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
# CLASE CHATBOT
# ============================================
class Chatbot:
    def __init__(self, system_prompt, modelo=MODEL, max_mensajes=20):
        self.modelo = modelo
        self.max_mensajes = max_mensajes
        self.mensajes = [
            {"role": "system", "content": system_prompt}
        ]

    def chat(self, mensaje_usuario):
        """Envia un mensaje y obtiene la respuesta manteniendo contexto."""
        # Anadir mensaje del usuario
        self.mensajes.append({"role": "user", "content": mensaje_usuario})

        # Gestionar ventana de contexto
        self._gestionar_contexto()

        # Llamar a la API
        response = client.chat.completions.create(
            model=self.modelo,
            messages=self.mensajes,
            temperature=0.7,
            max_tokens=500
        )

        # Extraer y almacenar la respuesta
        respuesta = response.choices[0].message.content
        self.mensajes.append({"role": "assistant", "content": respuesta})

        return respuesta

    def _gestionar_contexto(self):
        """Trunca el historial si excede el maximo de mensajes."""
        if len(self.mensajes) > self.max_mensajes:
            # Mantener el system prompt + los ultimos N mensajes
            self.mensajes = [self.mensajes[0]] + self.mensajes[-(self.max_mensajes - 1):]

    def ver_historial(self):
        """Muestra el historial de la conversacion."""
        for i, msg in enumerate(self.mensajes):
            role = msg["role"].upper()
            content = msg["content"][:80] + "..." if len(msg["content"]) > 80 else msg["content"]
            print(f"  [{i}] {role}: {content}")


# ============================================
# DEMOSTRACION
# ============================================
print("=" * 60)
print("DEMO: Chatbot con Memoria de Conversacion")
print("=" * 60)

bot = Chatbot(
    system_prompt="Eres un asistente de soporte tecnico para una empresa de software. "
                  "Respondes de forma amable y concisa.",
    max_mensajes=20
)

# Turno 1
print("\n  Usuario: Hola, tengo un problema con la instalacion")
respuesta = bot.chat("Hola, tengo un problema con la instalacion")
print(f"  Bot: {respuesta}")

# Turno 2
print(f"\n  Usuario: Me da un error de permisos")
respuesta = bot.chat("Me da un error de permisos")
print(f"  Bot: {respuesta}")

# Turno 3 - El bot deberia recordar el contexto
print(f"\n  Usuario: Que me recomendaste antes?")
respuesta = bot.chat("Que me recomendaste antes?")
print(f"  Bot: {respuesta}")

# Mostrar historial
print("\n" + "-" * 60)
print("HISTORIAL COMPLETO:")
print("-" * 60)
bot.ver_historial()

print(f"\n  Total mensajes en memoria: {len(bot.mensajes)}")
print("=" * 60)
