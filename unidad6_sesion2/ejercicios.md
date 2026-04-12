# Ejercicios Prácticos - Unidad 6, Sesión 2
## Desarrollo de Servidores MCP y Producción

---

## Ejercicio 1: Servidor MCP Básico con FastMCP

### Metadata
- **Duración estimada**: 35 minutos
- **Tipo**: Programación
- **Modalidad**: Individual
- **Dificultad**: Intermedia
- **Prerequisitos**: Python 3.10+, pip instalado, conocimientos básicos de decoradores en Python, comprensión del protocolo MCP (Sesión 1)

### Contexto
FastMCP es el framework oficial de referencia para crear servidores MCP en Python. Proporciona una API de alto nivel basada en decoradores que simplifica enormemente la implementación: basta con anotar funciones Python con `@mcp.tool()` para exponerlas como herramientas invocables por cualquier cliente MCP. El servidor gestiona automáticamente la serialización JSON-RPC, la validación de parámetros mediante type hints y la documentación de las herramientas a partir de los docstrings. MCP Inspector es la herramienta oficial de depuración que permite probar servidores MCP sin necesidad de un cliente completo.

### Objetivo de Aprendizaje
- Instalar y configurar FastMCP para crear un servidor MCP funcional
- Implementar herramientas (tools) con validación de parámetros usando type hints
- Comprender cómo los docstrings se convierten en descripciones para el LLM
- Probar y depurar el servidor usando MCP Inspector

### Enunciado

Crea un servidor MCP que exponga tres herramientas útiles: una calculadora científica, un conversor de unidades y un generador de contraseñas. El servidor debe poder ejecutarse localmente y ser verificable con MCP Inspector.

### Pasos a Seguir

#### Paso 1: Preparar el entorno (5 min)

```bash
# Crear directorio del proyecto
mkdir mcp-server-basico && cd mcp-server-basico

# Crear entorno virtual con uv (recomendado) o venv
uv venv && source .venv/bin/activate   # Recomendado
# python -m venv venv && source venv/bin/activate  # Alternativa

# Instalar dependencias
pip install "fastmcp>=2.0.0" "mcp[cli]>=1.0.0"
```

#### Paso 2: Crear el servidor con herramientas (15 min)

Crea un archivo `server.py` con el siguiente esqueleto e implementa las tres herramientas:

```python
from fastmcp import FastMCP
import math
import string
import random

# Crear instancia del servidor
mcp = FastMCP(
    name="Herramientas Básicas",
    instructions="Servidor MCP con calculadora científica, conversor de unidades y generador de contraseñas."
)


@mcp.tool()
def calculadora(operacion: str, a: float, b: float = 0.0) -> str:
    """Realiza operaciones matemáticas.

    Args:
        operacion: Operación a realizar. Valores posibles: suma, resta,
                   multiplicacion, division, potencia, raiz, seno, coseno, logaritmo.
        a: Primer operando (o único operando para funciones como raíz, seno, etc.).
        b: Segundo operando (opcional, necesario para suma, resta, etc.).

    Returns:
        Resultado de la operación como texto descriptivo.
    """
    operaciones = {
        "suma": lambda: a + b,
        "resta": lambda: a - b,
        "multiplicacion": lambda: a * b,
        "division": lambda: a / b if b != 0 else "Error: división por cero",
        "potencia": lambda: a ** b,
        "raiz": lambda: math.sqrt(a) if a >= 0 else "Error: raíz de número negativo",
        "seno": lambda: math.sin(math.radians(a)),
        "coseno": lambda: math.cos(math.radians(a)),
        "logaritmo": lambda: math.log(a) if a > 0 else "Error: logaritmo de número no positivo",
    }

    if operacion not in operaciones:
        return f"Operación '{operacion}' no reconocida. Operaciones válidas: {', '.join(operaciones.keys())}"

    resultado = operaciones[operacion]()
    return f"{operacion}({a}, {b}) = {resultado}"


@mcp.tool()
def conversor_unidades(valor: float, de: str, a: str) -> str:
    """Convierte entre diferentes unidades de medida.

    Args:
        valor: Cantidad a convertir.
        de: Unidad de origen (ej: km, m, cm, kg, g, lb, celsius, fahrenheit).
        a: Unidad de destino.

    Returns:
        Resultado de la conversión con las unidades indicadas.
    """
    # Conversiones de longitud a metros
    longitud_a_metros = {
        "km": 1000, "m": 1, "cm": 0.01, "mm": 0.001,
        "mi": 1609.34, "ft": 0.3048, "in": 0.0254
    }

    # Conversiones de peso a gramos
    peso_a_gramos = {
        "kg": 1000, "g": 1, "mg": 0.001,
        "lb": 453.592, "oz": 28.3495
    }

    # Intentar conversión de longitud
    if de in longitud_a_metros and a in longitud_a_metros:
        resultado = valor * longitud_a_metros[de] / longitud_a_metros[a]
        return f"{valor} {de} = {resultado:.4f} {a}"

    # Intentar conversión de peso
    if de in peso_a_gramos and a in peso_a_gramos:
        resultado = valor * peso_a_gramos[de] / peso_a_gramos[a]
        return f"{valor} {de} = {resultado:.4f} {a}"

    # Conversión de temperatura
    if de == "celsius" and a == "fahrenheit":
        return f"{valor} °C = {valor * 9/5 + 32:.2f} °F"
    if de == "fahrenheit" and a == "celsius":
        return f"{valor} °F = {(valor - 32) * 5/9:.2f} °C"
    if de == "celsius" and a == "kelvin":
        return f"{valor} °C = {valor + 273.15:.2f} K"
    if de == "kelvin" and a == "celsius":
        return f"{valor} K = {valor - 273.15:.2f} °C"

    return f"No se puede convertir de '{de}' a '{a}'. Verifica las unidades."


@mcp.tool()
def generar_contrasena(longitud: int = 16, incluir_simbolos: bool = True) -> str:
    """Genera una contraseña aleatoria segura.

    Args:
        longitud: Longitud de la contraseña (entre 8 y 128 caracteres).
        incluir_simbolos: Si es True, incluye caracteres especiales (!@#$%...).

    Returns:
        Contraseña generada aleatoriamente.
    """
    if longitud < 8:
        return "Error: la longitud mínima es 8 caracteres."
    if longitud > 128:
        return "Error: la longitud máxima es 128 caracteres."

    caracteres = string.ascii_letters + string.digits
    if incluir_simbolos:
        caracteres += "!@#$%^&*()-_=+[]{}|;:,.<>?"

    contrasena = ''.join(random.choice(caracteres) for _ in range(longitud))

    # Evaluar fortaleza
    tiene_mayusculas = any(c.isupper() for c in contrasena)
    tiene_minusculas = any(c.islower() for c in contrasena)
    tiene_numeros = any(c.isdigit() for c in contrasena)
    tiene_especiales = any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?" for c in contrasena)

    fortaleza_score = sum([tiene_mayusculas, tiene_minusculas, tiene_numeros, tiene_especiales])
    fortaleza = {1: "Débil", 2: "Media", 3: "Fuerte", 4: "Muy fuerte"}.get(fortaleza_score, "Débil")

    return f"Contraseña: {contrasena}\nLongitud: {longitud}\nFortaleza: {fortaleza}"


if __name__ == "__main__":
    mcp.run()
```

#### Paso 3: Probar con MCP Inspector (10 min)

```bash
# Opción 1: Ejecutar el inspector directamente (requiere npx/node)
npx @modelcontextprotocol/inspector python server.py

# Opción 2: Si no tienes npx, ejecutar el servidor en modo stdio
# y probarlo con un script de pruebas manual
python server.py
```

En MCP Inspector:

1. Verifica que aparecen las tres herramientas en la pestaña **Tools**
2. Haz clic en cada herramienta y observa la descripción y los parámetros
3. Prueba cada herramienta con los siguientes valores:
   - `calculadora`: operacion="raiz", a=144
   - `conversor_unidades`: valor=100, de="km", a="mi"
   - `generar_contrasena`: longitud=20, incluir_simbolos=true

#### Paso 4: Verificar la documentación automática (5 min)

Observa en el Inspector cómo FastMCP ha generado automáticamente:
- La descripción de cada herramienta a partir del docstring
- El esquema JSON de parámetros a partir de los type hints
- Los valores por defecto cuando están definidos


### Extensión (Opcional)

- Añade una cuarta herramienta `consultar_hora` que devuelva la fecha y hora actual en una zona horaria especificada como parámetro (usa el módulo `zoneinfo` de Python 3.9+)
- Implementa manejo de errores robusto con try/except que devuelva mensajes descriptivos al LLM en caso de fallo

---

## Ejercicio 2: Implementar Resources y Prompts en el Servidor MCP

### Metadata
- **Duración estimada**: 30 minutos
- **Tipo**: Programación
- **Modalidad**: Individual
- **Dificultad**: Intermedia
- **Prerequisitos**: Ejercicio 1 completado, comprensión de los tres primitivos MCP (Tools, Resources, Prompts)

### Contexto
Un servidor MCP completo no solo expone herramientas (tools), sino también recursos (resources) y plantillas de prompts (prompts). Los **resources** proporcionan datos contextuales que el cliente puede leer (como ficheros de configuración, estado del sistema o datos de referencia), mientras que los **prompts** ofrecen plantillas reutilizables que guían al LLM en tareas específicas. La combinación de estos tres primitivos es lo que hace que un servidor MCP sea verdaderamente útil: las herramientas ejecutan acciones, los recursos aportan contexto y los prompts estructuran las interacciones.

### Objetivo de Aprendizaje
- Implementar resources estáticos y dinámicos con `@mcp.resource()`
- Crear prompt templates parametrizados con `@mcp.prompt()`
- Comprender la diferencia funcional entre tools, resources y prompts
- Verificar en MCP Inspector que los tres primitivos aparecen correctamente

### Enunciado

Amplía el servidor MCP del Ejercicio 1 añadiendo dos resources y dos prompt templates. Los resources proporcionarán información de contexto sobre el servidor, y los prompts guiarán al LLM en tareas específicas de análisis.

### Pasos a Seguir

#### Paso 1: Añadir Resources al servidor (10 min)

Añade los siguientes resources a tu archivo `server.py`:

```python
import json
from datetime import datetime


@mcp.resource("config://servidor")
def obtener_configuracion() -> str:
    """Configuración actual del servidor MCP y sus capacidades."""
    config = {
        "nombre": "Herramientas Básicas",
        "version": "1.0.0",
        "herramientas_disponibles": [
            "calculadora",
            "conversor_unidades",
            "generar_contrasena"
        ],
        "unidades_soportadas": {
            "longitud": ["km", "m", "cm", "mm", "mi", "ft", "in"],
            "peso": ["kg", "g", "mg", "lb", "oz"],
            "temperatura": ["celsius", "fahrenheit", "kelvin"]
        },
        "operaciones_calculadora": [
            "suma", "resta", "multiplicacion", "division",
            "potencia", "raiz", "seno", "coseno", "logaritmo"
        ]
    }
    return json.dumps(config, indent=2, ensure_ascii=False)


@mcp.resource("status://servidor")
def obtener_estado() -> str:
    """Estado actual del servidor incluyendo timestamp y métricas básicas."""
    estado = {
        "estado": "activo",
        "timestamp": datetime.now().isoformat(),
        "uptime_info": "Servidor funcionando correctamente",
        "version_python": f"{__import__('sys').version}",
        "modulos_cargados": ["math", "string", "random", "json", "datetime"]
    }
    return json.dumps(estado, indent=2, ensure_ascii=False)
```

#### Paso 2: Añadir Prompts al servidor (10 min)

Añade los siguientes prompt templates:

```python
@mcp.prompt()
def analizar_conversion(valor: float, unidad_origen: str, contexto: str = "general") -> str:
    """Prompt para analizar una conversión de unidades en contexto.

    Args:
        valor: Valor numérico a analizar.
        unidad_origen: Unidad del valor proporcionado.
        contexto: Contexto de uso (ej: cocina, ingeniería, ciencia, viaje).
    """
    return f"""Eres un experto en unidades de medida y conversiones.

Se te proporciona el siguiente valor: {valor} {unidad_origen}

Contexto de uso: {contexto}

Por favor:
1. Convierte este valor a las 3 unidades más relevantes para el contexto indicado.
   Usa la herramienta 'conversor_unidades' para cada conversión.
2. Explica en qué situaciones prácticas del contexto '{contexto}' se usaría cada unidad.
3. Indica si el valor proporcionado está dentro de rangos habituales para ese contexto.

Responde de forma clara y estructurada."""


@mcp.prompt()
def generar_informe_seguridad(
    longitud_minima: int = 12,
    num_contrasenas: int = 5
) -> str:
    """Prompt para generar un informe de seguridad de contraseñas.

    Args:
        longitud_minima: Longitud mínima de las contraseñas a evaluar.
        num_contrasenas: Número de contraseñas a generar para el análisis.
    """
    return f"""Eres un experto en ciberseguridad y gestión de contraseñas.

Realiza las siguientes tareas:

1. Genera {num_contrasenas} contraseñas usando la herramienta 'generar_contrasena':
   - 2 contraseñas de {longitud_minima} caracteres SIN símbolos
   - 2 contraseñas de {longitud_minima} caracteres CON símbolos
   - 1 contraseña de {longitud_minima + 8} caracteres CON símbolos

2. Para cada contraseña generada, analiza:
   - Fortaleza reportada por la herramienta
   - Tiempo estimado de cracking por fuerza bruta
   - Vulnerabilidades potenciales

3. Elabora un informe con:
   - Tabla comparativa de las contraseñas
   - Recomendaciones de mejores prácticas
   - Política de contraseñas sugerida para una organización

Presenta el informe de forma profesional y estructurada."""
```

#### Paso 3: Verificar en MCP Inspector (10 min)

1. Reinicia el servidor y abre MCP Inspector
2. Navega a la pestaña **Resources** y verifica:
   - Aparecen `config://servidor` y `status://servidor`
   - Al hacer clic en cada uno, se muestra el JSON correspondiente
   - El resource `status://servidor` muestra un timestamp actualizado
3. Navega a la pestaña **Prompts** y verifica:
   - Aparecen `analizar_conversion` y `generar_informe_seguridad`
   - Al seleccionar un prompt, se muestran sus parámetros
   - Rellena los parámetros de `analizar_conversion` (ej: valor=5, unidad_origen="km", contexto="viaje") y observa el texto generado

### Extensión (Opcional)

- Añade un resource dinámico con URI parametrizada: `@mcp.resource("conversion://{de}/{a}")` que devuelva la tabla de factores de conversión entre dos tipos de unidades
- Crea un prompt que combine el uso de las tres herramientas en una tarea de análisis completa

---

## Ejercicio 3: Análisis de Seguridad MCP

### Metadata
- **Duración estimada**: 20 minutos
- **Tipo**: Análisis
- **Modalidad**: Individual
- **Dificultad**: Básica
- **Prerequisitos**: Comprensión del modelo cliente-servidor MCP y conocimientos básicos de seguridad web (HTTPS, autenticación, tokens)

### Contexto
Cuando un servidor MCP se expone a través de HTTP (usando el transporte Streamable HTTP o el antiguo SSE), deja de ser una comunicación local entre procesos y pasa a ser un servicio de red accesible potencialmente por cualquier actor. Sin medidas de seguridad, un atacante podría invocar herramientas del servidor, acceder a recursos sensibles o inyectar prompts maliciosos. La especificación MCP delega la seguridad al implementador, por lo que es responsabilidad del desarrollador diseñar y aplicar las medidas adecuadas.

### Objetivo de Aprendizaje
- Identificar los vectores de ataque principales en un servidor MCP expuesto por HTTP
- Comprender los riesgos específicos de MCP: tool poisoning, prompt injection, exfiltración de datos
- Diseñar un esquema de autenticación y autorización basado en JWT
- Proponer un plan de mitigación completo y realista

### Enunciado

Se te presenta el siguiente escenario: una empresa ha desarrollado un servidor MCP que proporciona acceso a su base de datos de clientes, un sistema de envío de emails y una herramienta de generación de informes. El servidor está desplegado en un VPS con IP pública y accesible por HTTP en el puerto 8080, sin ninguna medida de seguridad implementada.

```
┌─────────────────────────────────────────────────────────────┐
│  SERVIDOR MCP (http://203.0.113.50:8080)                    │
│                                                             │
│  Tools:                                                     │
│    - consultar_cliente(id) → datos personales               │
│    - enviar_email(destinatario, asunto, cuerpo)             │
│    - generar_informe(tipo, fecha_inicio, fecha_fin)         │
│                                                             │
│  Resources:                                                 │
│    - db://clientes/esquema → esquema de la base de datos    │
│    - config://email → configuración SMTP con credenciales   │
│                                                             │
│  Sin autenticación | Sin HTTPS | Sin logs | Sin rate limit  │
└─────────────────────────────────────────────────────────────┘
```

### Parte A: Identificación de Riesgos (10 min)

Completa la siguiente tabla identificando al menos 6 riesgos de seguridad:

| # | Riesgo | Primitivo afectado | Severidad (Alta/Media/Baja) | Ejemplo de ataque |
|---|--------|-------------------|----------------------------|-------------------|
| 1 | __________________ | Tool / Resource / Prompt | _______ | __________________ |
| 2 | __________________ | Tool / Resource / Prompt | _______ | __________________ |
| 3 | __________________ | Tool / Resource / Prompt | _______ | __________________ |
| 4 | __________________ | Tool / Resource / Prompt | _______ | __________________ |
| 5 | __________________ | Tool / Resource / Prompt | _______ | __________________ |
| 6 | __________________ | Tool / Resource / Prompt | _______ | __________________ |

### Parte B: Diseño del Flujo de Autenticación JWT (10 min)

Diseña el flujo completo de autenticación JWT para proteger el servidor MCP. Completa el siguiente diagrama de secuencia con los pasos que faltan:

```
Cliente MCP                    Auth Server                    Servidor MCP
     │                              │                              │
     │  1. POST /auth/token         │                              │
     │     {client_id, secret}      │                              │
     │  ──────────────────────────► │                              │
     │                              │                              │
     │  2. ________________________ │                              │
     │  ◄────────────────────────── │                              │
     │                              │                              │
     │  3. ________________________________________________________________
     │     Header: ______________________________________________________ │
     │  ──────────────────────────────────────────────────────────────────►│
     │                              │                              │
     │                              │  4. ________________________ │
     │                              │  ◄──────────────────────────  │
     │                              │                              │
     │                              │  5. ________________________ │
     │                              │  ──────────────────────────► │
     │                              │                              │
     │  6. ________________________________________________________________
     │  ◄──────────────────────────────────────────────────────────────────│
```

Adicionalmente, define qué claims debe contener el JWT para este caso de uso:

```json
{
    "sub": "_______________",
    "iss": "_______________",
    "exp": "_______________",
    "iat": "_______________",
    "permissions": ["_______________", "_______________"],
    "allowed_tools": ["_______________"],
    "___": "_______________"
}
```

### Parte C: Plan de Mitigación

Propón al menos 5 medidas concretas que implementarías, ordenadas por prioridad:

| Prioridad | Medida | Implementación concreta |
|-----------|--------|------------------------|
| 1 (Crítica) | __________________ | __________________ |
| 2 (Crítica) | __________________ | __________________ |
| 3 (Alta) | __________________ | __________________ |
| 4 (Media) | __________________ | __________________ |
| 5 (Media) | __________________ | __________________ |


## Ejercicio 4: Cliente MCP con Streamlit

### Metadata
- **Duración estimada**: 40 minutos
- **Tipo**: Programación
- **Modalidad**: Individual
- **Dificultad**: Avanzada
- **Prerequisitos**: Ejercicios 1 y 2 completados (servidor MCP funcionando), conocimientos básicos de Streamlit, API key de OpenAI o Anthropic

### Contexto
Un servidor MCP solo es útil si existe un cliente que lo consuma. Mientras que herramientas como Claude Desktop o Cursor integran clientes MCP de forma nativa, en muchos escenarios empresariales se necesita un cliente personalizado con interfaz propia. Streamlit permite construir rápidamente interfaces web interactivas en Python, y combinado con el SDK de MCP, se puede crear un cliente completo que descubra herramientas, las presente al usuario y las invoque a través de un LLM. El código de referencia del curso (https://github.com/rpmaya/ml2_code/blob/main/MCP/client-mcp/app.py) proporciona la estructura base para este ejercicio.

### Objetivo de Aprendizaje
- Implementar un cliente MCP en Python usando el SDK oficial
- Integrar la conexión MCP con una interfaz Streamlit
- Comprender el flujo completo: usuario -> LLM -> tool call -> servidor MCP -> respuesta
- Gestionar la conexión y desconexión del cliente MCP con manejo de contextos asíncronos

### Enunciado

Crea un cliente MCP con interfaz web en Streamlit que se conecte al servidor del Ejercicio 1 (o a cualquier servidor MCP local) y permita al usuario interactuar mediante lenguaje natural. El LLM decidirá cuándo invocar las herramientas del servidor.

### Pasos a Seguir

#### Paso 1: Preparar el entorno (5 min)

```bash
# En el mismo directorio del proyecto o uno nuevo
pip install streamlit mcp anthropic python-dotenv

# Crear archivo .env con tu API key
echo "ANTHROPIC_API_KEY=tu-api-key-aqui" > .env
```

#### Paso 2: Crear el cliente MCP (20 min)

Crea un archivo `app.py` siguiendo esta estructura (basada en el código de referencia del curso):

```python
import streamlit as st
import asyncio
import json
import os
from dotenv import load_dotenv
from anthropic import Anthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

# Configuración de la página
st.set_page_config(
    page_title="Cliente MCP",
    page_icon="🔧",
    layout="wide"
)


class MCPClient:
    """Cliente MCP que gestiona la conexión con el servidor y las llamadas al LLM."""

    def __init__(self):
        self.session = None
        self.anthropic = Anthropic()
        self.available_tools = []

    async def connect(self, server_script_path: str):
        """Conecta con un servidor MCP local vía stdio."""
        server_params = StdioServerParameters(
            command="python",
            args=[server_script_path],
        )
        # Crear la conexión stdio
        self.stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        read_stream, write_stream = self.stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(read_stream, write_stream)
        )
        await self.session.initialize()

        # Descubrir herramientas disponibles
        response = await self.session.list_tools()
        self.available_tools = [
            {
                "name": tool.name,
                "description": tool.description or "",
                "input_schema": tool.inputSchema,
            }
            for tool in response.tools
        ]
        return self.available_tools

    async def process_message(self, user_message: str, message_history: list) -> str:
        """Procesa un mensaje del usuario, invocando tools si el LLM lo decide."""
        message_history.append({"role": "user", "content": user_message})

        # Primera llamada al LLM con las herramientas disponibles
        response = self.anthropic.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system="Eres un asistente útil con acceso a herramientas MCP. "
                   "Usa las herramientas disponibles cuando sea apropiado "
                   "para responder a las preguntas del usuario. "
                   "Responde siempre en español.",
            tools=self.available_tools,
            messages=message_history,
        )

        # Procesar la respuesta (puede incluir tool_use)
        result_text = ""
        while response.stop_reason == "tool_use":
            # Extraer bloques de texto y tool_use
            assistant_content = response.content
            message_history.append({"role": "assistant", "content": assistant_content})

            # Ejecutar cada tool call
            tool_results = []
            for block in assistant_content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_args = block.input

                    # Invocar la herramienta en el servidor MCP
                    tool_response = await self.session.call_tool(
                        tool_name, tool_args
                    )
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(tool_response.content),
                    })

            # Enviar resultados al LLM para que formule la respuesta final
            message_history.append({"role": "user", "content": tool_results})
            response = self.anthropic.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                system="Eres un asistente útil con acceso a herramientas MCP. "
                       "Usa las herramientas disponibles cuando sea apropiado. "
                       "Responde siempre en español.",
                tools=self.available_tools,
                messages=message_history,
            )

        # Extraer texto final
        for block in response.content:
            if hasattr(block, "text"):
                result_text += block.text

        message_history.append({"role": "assistant", "content": result_text})
        return result_text


# --- Interfaz Streamlit ---

st.title("Cliente MCP con Streamlit")
st.markdown("Conecta con un servidor MCP y chatea usando lenguaje natural.")

# Sidebar para configuración
with st.sidebar:
    st.header("Configuración")
    server_path = st.text_input(
        "Ruta al servidor MCP",
        value="server.py",
        help="Ruta al archivo Python del servidor MCP"
    )
    connect_button = st.button("Conectar al servidor")

# Estado de la sesión
if "messages" not in st.session_state:
    st.session_state.messages = []
if "connected" not in st.session_state:
    st.session_state.connected = False
if "tools" not in st.session_state:
    st.session_state.tools = []

# NOTA IMPORTANTE para el alumno:
# La integración completa de asyncio con Streamlit requiere
# gestión cuidadosa del event loop. En producción, se recomienda
# usar el patrón asyncio.run() o nest_asyncio para compatibilidad.
# Consulta el código de referencia del curso para la implementación
# completa: https://github.com/rpmaya/ml2_code/blob/main/MCP/client-mcp/app.py

# Mostrar herramientas disponibles si está conectado
if st.session_state.connected:
    with st.sidebar:
        st.success("Conectado al servidor MCP")
        st.subheader("Herramientas disponibles")
        for tool in st.session_state.tools:
            with st.expander(f"🔧 {tool['name']}"):
                st.write(tool["description"])

# Área de chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input del usuario
if prompt := st.chat_input("Escribe tu mensaje..."):
    if not st.session_state.connected:
        st.warning("Primero conecta con un servidor MCP usando el panel lateral.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Procesando..."):
                # Aquí se invoca process_message del cliente MCP
                # (requiere gestión del event loop async)
                st.write("Respuesta del asistente aparecería aquí")
```

#### Paso 3: Ejecutar y probar (10 min)

```bash
# Asegúrate de que el servidor MCP del Ejercicio 1 está disponible
# Ejecuta la aplicación Streamlit
streamlit run app.py
```

Prueba las siguientes interacciones en la interfaz:

1. Conecta con el servidor MCP indicando la ruta `server.py`
2. Envía: *"¿Cuánto es la raíz cuadrada de 256?"* (debe invocar la calculadora)
3. Envía: *"Convierte 72 grados Fahrenheit a Celsius"* (debe invocar el conversor)
4. Envía: *"Genera una contraseña segura de 24 caracteres"* (debe invocar el generador)
5. Envía: *"¿Cuál es la capital de Francia?"* (NO debe invocar ninguna herramienta)

#### Paso 4: Observar el flujo de tool calling (5 min)

Para cada interacción, añade logging que muestre:
- Si el LLM decidió usar una herramienta o no
- Qué herramienta eligió y con qué parámetros
- El resultado devuelto por el servidor MCP

```python
# Añadir al método process_message, dentro del bucle de tool_use:
st.sidebar.write(f"🔧 Tool call: {tool_name}")
st.sidebar.json(tool_args)
st.sidebar.write(f"📤 Resultado: {tool_response.content}")
```

### Solución Esperada

El alumno debe entregar:
- Un archivo `app.py` que ejecute una interfaz Streamlit funcional
- La aplicación debe conectarse al servidor MCP y mostrar las herramientas disponibles en el sidebar
- Al enviar mensajes en lenguaje natural, el LLM debe decidir correctamente cuándo usar herramientas y cuándo responder directamente
- El logging en el sidebar debe mostrar las tool calls realizadas
- El alumno debe comprender y poder explicar el flujo: usuario escribe -> LLM analiza -> LLM genera tool_use -> cliente invoca tool en servidor MCP -> resultado vuelve al LLM -> LLM formula respuesta final

### Extensión (Opcional)

- Añade soporte para conectarse a múltiples servidores MCP simultáneamente, mostrando todas las herramientas agregadas en el sidebar
- Implementa persistencia del historial de chat usando `st.session_state` para que sobreviva a recargas de página
- Añade un botón para listar y mostrar los Resources del servidor, mostrando su contenido en el sidebar

---

## Ejercicio 5: Diseño de Servidor MCP para Caso Real

### Metadata
- **Duración estimada**: 25 minutos
- **Tipo**: Diseño
- **Modalidad**: Grupal (equipos de 3-4 personas)
- **Dificultad**: Intermedia
- **Prerequisitos**: Comprensión de los tres primitivos MCP (tools, resources, prompts), conocimiento básico de APIs REST y bases de datos

### Contexto
El valor real de MCP se materializa cuando se aplica a casos de uso concretos que resuelven necesidades reales de una organización. Diseñar un servidor MCP requiere pensar de forma integral: qué herramientas exponer (sin dar acceso excesivo), qué recursos contextualizar, qué plantillas de prompts facilitarán el trabajo del usuario, cómo proteger el sistema y cómo desplegarlo de forma fiable. Este ejercicio simula el proceso de diseño que un equipo de desarrollo seguiría antes de implementar un servidor MCP en producción.

### Objetivo de Aprendizaje
- Aplicar los conceptos de MCP a un caso de uso empresarial real
- Diseñar una arquitectura MCP completa con los tres primitivos
- Considerar aspectos de seguridad, escalabilidad y despliegue desde el diseño
- Practicar la toma de decisiones técnicas en equipo y su justificación

### Enunciado

Cada equipo debe elegir uno de los siguientes casos de uso (o proponer uno propio aprobado por el profesor) y diseñar un servidor MCP completo. No se requiere implementación, pero el diseño debe ser suficientemente detallado para que un desarrollador pueda implementarlo.

### Casos de Uso Disponibles

**Caso A: Gestión de Base de Datos de Productos (e-commerce)**
Un marketplace online necesita que su equipo de soporte pueda consultar y gestionar el catálogo de productos mediante lenguaje natural: buscar productos, verificar stock, actualizar precios y generar informes de ventas.

**Caso B: Integración con API Meteorológica**
Una empresa de logística necesita que sus operadores consulten previsiones meteorológicas para planificar rutas de reparto: consultar el tiempo actual, previsión a 7 días, alertas meteorológicas y recomendaciones de ruta según condiciones.

**Caso C: Sistema de Gestión de Tickets de Soporte**
El departamento de IT de una empresa necesita gestionar tickets de soporte técnico mediante un asistente: crear tickets, asignarlos, cambiar estados, buscar tickets similares y generar estadísticas de resolución.

**Caso D: Propuesta Libre**
El equipo propone un caso de uso propio relevante para su ámbito profesional o académico.

### Pasos a Seguir

#### Paso 1: Selección y análisis del caso (5 min)

- Elegir uno de los casos de uso
- Identificar los actores principales (quién usará el sistema)
- Listar las acciones que necesitan realizar
- Identificar las fuentes de datos involucradas

#### Paso 2: Diseño de Tools (5 min)

Diseñar entre 4 y 6 herramientas. Para cada una, especificar:

| Herramienta | Descripción (para el LLM) | Parámetros | Retorno | Permisos necesarios |
|-------------|---------------------------|------------|---------|---------------------|
| `nombre_tool` | Qué hace y cuándo usarla | nombre: tipo (descripción) | Qué devuelve | lectura / escritura / admin |

**Ejemplo para Caso A:**

| Herramienta | Descripción | Parámetros | Retorno | Permisos |
|-------------|-------------|------------|---------|----------|
| `buscar_productos` | Busca productos en el catálogo por nombre, categoría o rango de precio | query: str, categoria: str (opcional), precio_min: float (opcional), precio_max: float (opcional) | Lista de productos con id, nombre, precio, stock | lectura |
| `actualizar_precio` | Actualiza el precio de un producto existente | producto_id: int, nuevo_precio: float, motivo: str | Confirmación con precio anterior y nuevo | escritura |

#### Paso 3: Diseño de Resources (5 min)

Diseñar entre 2 y 4 resources:

| URI del Resource | Descripción | Tipo de dato | Frecuencia de actualización |
|------------------|-------------|--------------|----------------------------|
| `esquema://...` | Qué información expone | JSON / texto / ... | estático / dinámico |

#### Paso 4: Diseño de Prompts (5 min)

Diseñar 2-3 prompt templates:

| Nombre del Prompt | Objetivo | Parámetros | Tools que utiliza |
|-------------------|----------|------------|-------------------|
| `nombre_prompt` | Para qué sirve | param1: tipo, param2: tipo | tool1, tool2 |

#### Paso 5: Seguridad y Despliegue (5 min)

Completar la ficha de seguridad y despliegue:

```
SEGURIDAD:
- Autenticación: __________________ (JWT / OAuth / API Key / otra)
- Autorización: __________________ (por roles / por herramienta / mixta)
- Datos sensibles: __________________ (qué datos requieren protección especial)
- Validación de inputs: __________________ (qué validaciones son críticas)
- Logging: __________________ (qué eventos registrar obligatoriamente)

DESPLIEGUE:
- Transporte: __________________ (stdio / Streamable HTTP)
- Infraestructura: __________________ (Docker / VPS / serverless / cloud)
- Escalabilidad: __________________ (cómo escalar si crece la demanda)
- Monitorización: __________________ (qué métricas rastrear)
- Backup y recuperación: __________________ (estrategia de continuidad)
```

### Entregable

Cada equipo presenta su diseño al resto de la clase (5 minutos de presentación) cubriendo:
1. Diagrama de arquitectura del servidor MCP y sus conexiones externas
2. Tabla de tools con sus parámetros y permisos
3. Tabla de resources y prompts
4. Decisiones de seguridad y justificación
5. Estrategia de despliegue elegida

### Extensión (Opcional)

- Implementar el esqueleto del servidor en Python con FastMCP: solo las definiciones de tools, resources y prompts con docstrings completos, sin la lógica interna (que puede devolver datos de ejemplo)
- Crear un diagrama de secuencia que muestre una interacción completa: desde que el usuario hace una pregunta hasta que recibe la respuesta, pasando por el LLM y las tool calls

---

## Resumen de Tiempos

| Ejercicio | Duración | Tipo | Dificultad |
|-----------|----------|------|------------|
| 1. Servidor MCP Básico con FastMCP | 35 min | Programación | Intermedia |
| 2. Resources y Prompts | 30 min | Programación | Intermedia |
| 3. Análisis de Seguridad MCP | 20 min | Análisis | Básica |
| 4. Cliente MCP con Streamlit | 40 min | Programación | Avanzada |
| 5. Diseño de Servidor MCP para Caso Real | 25 min | Diseño | Intermedia |
| **Total** | **150 min** | | |

