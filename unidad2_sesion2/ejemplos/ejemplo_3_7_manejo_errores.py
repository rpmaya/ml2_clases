"""
Ejemplo 3.7 - Manejo de Errores
ML2 - Unidad 2, Sesión 2: Desarrollo con LLMs

En producción, las llamadas a la API pueden fallar por:
  - Rate limiting (demasiadas peticiones)
  - Errores de autenticación (API key inválida)
  - Errores del servidor (timeout, sobrecarga)
  - Errores de uso (modelo inexistente, tokens excedidos)

Este script muestra cómo manejar cada caso con reintentos.
"""

import os
import time
from pathlib import Path
from dotenv import load_dotenv
from openai import (
    OpenAI,
    APIError,
    RateLimitError,
    AuthenticationError,
    BadRequestError,
)

# ============================================
# CONFIGURACIÓN
# ============================================
load_dotenv(Path(__file__).parent / ".env")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ============================================
# FUNCIÓN CON MANEJO ROBUSTO DE ERRORES
# ============================================
def safe_chat(messages, retries=3):
    """Llama a la API con reintentos y manejo de errores."""

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=messages,
                temperature=0.7,
                max_tokens=300
            )
            return response.choices[0].message.content

        except RateLimitError:
            # Demasiadas peticiones → esperar con backoff exponencial
            wait = 2 ** attempt
            print(f"⏳ Rate limit alcanzado. Reintentando en {wait}s... (intento {attempt + 1}/{retries})")
            time.sleep(wait)

        except AuthenticationError:
            # API key inválida → no tiene sentido reintentar
            print("🔑 Error de autenticación. Verifica tu OPENAI_API_KEY en .env")
            raise

        except BadRequestError as e:
            # Error en la petición (modelo no existe, tokens excedidos, etc.)
            print(f"❌ Error en la petición: {e}")
            raise

        except APIError as e:
            # Error genérico del servidor → reintentar
            wait = 2 ** attempt
            print(f"⚠️  Error del servidor: {e}. Reintentando en {wait}s... (intento {attempt + 1}/{retries})")
            time.sleep(wait)

    raise Exception(f"Falló después de {retries} reintentos")


# ============================================
# DEMO 1: Llamada exitosa
# ============================================
print("=" * 60)
print("DEMO 1: Llamada exitosa con manejo de errores")
print("=" * 60)

messages_ok = [
    {"role": "system", "content": "Eres un asistente útil."},
    {"role": "user", "content": "Di 'hola' en 3 idiomas."}
]

result = safe_chat(messages_ok)
print(f"\n✅ Respuesta: {result}")

# ============================================
# DEMO 2: Error por modelo inexistente
# ============================================
print("\n" + "=" * 60)
print("DEMO 2: Error controlado (modelo inexistente)")
print("=" * 60)

try:
    # Forzamos un error usando un modelo que no existe
    bad_response = client.chat.completions.create(
        model="gpt-99-turbo",  # No existe
        messages=messages_ok
    )
except BadRequestError as e:
    print(f"\n❌ BadRequestError capturado: {e.message}")
except Exception as e:
    print(f"\n❌ Error capturado: {type(e).__name__}: {e}")

# ============================================
# DEMO 3: Error por max_tokens insuficiente
# ============================================
print("\n" + "=" * 60)
print("DEMO 3: Respuesta cortada por max_tokens")
print("=" * 60)

response = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=[
        {"role": "user", "content": "Cuenta del 1 al 100."}
    ],
    max_tokens=20  # Muy poco para la respuesta completa
)

text = response.choices[0].message.content
reason = response.choices[0].finish_reason

print(f"\n📏 Respuesta: {text}")
print(f"📏 Finish reason: {reason}")

if reason == "length":
    print("⚠️  La respuesta fue cortada por alcanzar max_tokens.")
    print("   Solución: aumentar max_tokens o pedir respuestas más cortas.")

# ============================================
# RESUMEN
# ============================================
print("\n" + "=" * 60)
print("💡 Buenas prácticas:")
print("   1. Siempre envuelve las llamadas API en try/except")
print("   2. Usa backoff exponencial para rate limits")
print("   3. No reintentes errores de autenticación o bad request")
print("   4. Verifica finish_reason para detectar respuestas cortadas")
print("   5. Registra errores en logs para monitoreo")
print("=" * 60)
