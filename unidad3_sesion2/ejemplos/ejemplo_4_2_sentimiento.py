"""
Ejemplo 4.2 - Analisis de Sentimiento Automatizado
ML2 - Unidad 3, Sesion 2: Acceso Programatico a LLMs

Procesamiento por lotes de textos para clasificar su
sentimiento de forma automatica. El modelo devuelve JSON
estructurado con sentimiento, confianza y razon.

Usa OpenRouter con modelo gratuito.
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
# FUNCION DE ANALISIS DE SENTIMIENTO
# ============================================
def analizar_sentimiento_lote(textos, modelo=MODEL):
    """
    Analiza el sentimiento de una lista de textos.

    Args:
        textos: Lista de strings a analizar
        modelo: Modelo a utilizar

    Returns:
        Lista de diccionarios con sentimiento y confianza
    """
    resultados = []

    for i, texto in enumerate(textos):
        response = client.chat.completions.create(
            model=modelo,
            messages=[
                {
                    "role": "system",
                    "content": "Analiza el sentimiento del texto. "
                               "Responde SOLO con JSON valido: "
                               '{"sentimiento": "positivo|negativo|neutral", '
                               '"confianza": 0.0-1.0, '
                               '"razon": "breve explicacion"}'
                },
                {
                    "role": "user",
                    "content": texto
                }
            ],
            temperature=0.0  # Determinista para clasificacion
        )

        try:
            resultado = json.loads(response.choices[0].message.content)
            resultado["texto_original"] = texto[:100]
            resultados.append(resultado)
        except json.JSONDecodeError:
            resultados.append({
                "texto_original": texto[:100],
                "sentimiento": "error",
                "confianza": 0.0,
                "razon": "Error al parsear respuesta"
            })

        # Progreso
        print(f"  Procesado {i+1}/{len(textos)}")

    return resultados


# ============================================
# DEMOSTRACION
# ============================================
print("=" * 60)
print("DEMO: Analisis de Sentimiento por Lotes")
print("=" * 60)

resenas = [
    "El producto es excelente, supero mis expectativas",
    "Pesimo servicio, llevo 3 dias esperando",
    "El envio llego a tiempo, producto correcto",
    "No funciona como esperaba, muy decepcionado",
    "Calidad precio imbatible, lo recomiendo al 100%",
]

print(f"\nAnalizando {len(resenas)} resenas...\n")

resultados = analizar_sentimiento_lote(resenas)

print("\n" + "-" * 60)
print("RESULTADOS:")
print("-" * 60)
for r in resultados:
    sentimiento = r.get("sentimiento", "?")
    confianza = r.get("confianza", 0)
    razon = r.get("razon", "")
    texto = r.get("texto_original", "")
    print(f"  {sentimiento:>10} ({confianza:.0%}) - {texto}")
    print(f"             Razon: {razon}")

# Resumen
positivos = sum(1 for r in resultados if r.get("sentimiento") == "positivo")
negativos = sum(1 for r in resultados if r.get("sentimiento") == "negativo")
neutrales = sum(1 for r in resultados if r.get("sentimiento") == "neutral")

print(f"\n  Resumen: {positivos} positivos, {negativos} negativos, {neutrales} neutrales")
print("=" * 60)
