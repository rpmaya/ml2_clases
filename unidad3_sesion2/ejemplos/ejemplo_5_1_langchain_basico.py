"""
Ejemplo 5.1 - LangChain Basico: Modelos, Templates y Chains
ML2 - Unidad 3, Sesion 2: Acceso Programatico a LLMs

LangChain es un framework de orquestacion que proporciona:
  - Interfaz unificada para multiples proveedores
  - Prompt Templates parametrizados
  - Chains (composicion de operaciones con operador pipe |)

Usa OpenRouter como proveedor via ChatOpenAI.

Requiere: pip install langchain langchain-openai
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ============================================
# CONFIGURACION
# ============================================
load_dotenv(Path(__file__).parent / ".env")

# ============================================
# PARTE 1: Chat Model con OpenRouter
# ============================================
print("=" * 60)
print("PARTE 1: Chat Model unificado con LangChain + OpenRouter")
print("=" * 60)

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Crear modelo apuntando a OpenRouter
modelo = ChatOpenAI(
    model="arcee-ai/trinity-large-preview:free",
    temperature=0.7,
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
)

# Llamada simple
mensajes = [
    SystemMessage(content="Eres un asistente util. Responde en espanol."),
    HumanMessage(content="Que es Python en una frase?")
]

respuesta = modelo.invoke(mensajes)
print(f"\n  Respuesta: {respuesta.content}")

# ============================================
# PARTE 2: Prompt Templates
# ============================================
print("\n" + "=" * 60)
print("PARTE 2: Prompt Templates parametrizados")
print("=" * 60)

from langchain_core.prompts import ChatPromptTemplate

# Definir un template reutilizable
template = ChatPromptTemplate.from_messages([
    ("system", "Eres un traductor experto. Traduces de {idioma_origen} a {idioma_destino}."),
    ("human", "Traduce el siguiente texto:\n\n{texto}")
])

# Usar el template con diferentes parametros
prompt_1 = template.invoke({
    "idioma_origen": "espanol",
    "idioma_destino": "ingles",
    "texto": "La inteligencia artificial esta transformando el mundo."
})

prompt_2 = template.invoke({
    "idioma_origen": "espanol",
    "idioma_destino": "frances",
    "texto": "Buenos dias, como estas?"
})

respuesta_1 = modelo.invoke(prompt_1)
respuesta_2 = modelo.invoke(prompt_2)
print(f"\n  Espanol -> Ingles: {respuesta_1.content}")
print(f"  Espanol -> Frances: {respuesta_2.content}")

# ============================================
# PARTE 3: Chains con operador pipe |
# ============================================
print("\n" + "=" * 60)
print("PARTE 3: Chains (composicion con operador pipe |)")
print("=" * 60)

from langchain_core.output_parsers import StrOutputParser

# Definir componentes
prompt_experto = ChatPromptTemplate.from_messages([
    ("system", "Eres un experto en {tema}. Responde de forma concisa en 2-3 frases."),
    ("human", "{pregunta}")
])

parser = StrOutputParser()

# Componer la cadena con el operador pipe
cadena = prompt_experto | modelo | parser

# Ejecutar
resultado = cadena.invoke({
    "tema": "Python",
    "pregunta": "Cuales son las ventajas de usar type hints?"
})
print(f"\n  Resultado de la cadena: {resultado}")

# ============================================
# PARTE 4: Cadena secuencial (multi-paso)
# ============================================
print("\n" + "=" * 60)
print("PARTE 4: Cadena secuencial (resumen -> traduccion)")
print("=" * 60)

# Paso 1: Generar un resumen
prompt_resumen = ChatPromptTemplate.from_messages([
    ("human", "Resume el siguiente texto en 1-2 oraciones:\n\n{texto}")
])

# Paso 2: Traducir el resumen
prompt_traduccion = ChatPromptTemplate.from_messages([
    ("human", "Traduce al ingles:\n\n{resumen}")
])

# Cadenas individuales
cadena_resumen = prompt_resumen | modelo | parser
cadena_traduccion = prompt_traduccion | modelo | parser

# Ejecutar secuencialmente
texto_largo = (
    "La inteligencia artificial generativa ha experimentado un crecimiento "
    "exponencial en los ultimos anos. Los modelos de lenguaje grande como "
    "GPT-4, Claude y Gemini pueden generar texto, codigo y contenido "
    "creativo con una calidad que hace pocos anos parecia ciencia ficcion. "
    "Esto ha abierto nuevas posibilidades en educacion, medicina, "
    "programacion y muchos otros campos."
)

print(f"\n  Texto original: {texto_largo[:80]}...")

resumen = cadena_resumen.invoke({"texto": texto_largo})
print(f"\n  Resumen: {resumen}")

traduccion = cadena_traduccion.invoke({"resumen": resumen})
print(f"  Traduccion: {traduccion}")

print("\n" + "=" * 60)
print("LangChain simplifica:")
print("   - Cambiar de proveedor: solo cambia ChatOpenAI por ChatAnthropic")
print("   - Reutilizar prompts: templates con variables {variable}")
print("   - Componer operaciones: prompt | modelo | parser")
print("=" * 60)
