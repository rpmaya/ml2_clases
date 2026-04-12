# Unidad 6 - Sesión 1: Introducción a MCP y Configuración de Servidores

## Objetivos de la Sesión

Al finalizar esta sesión, el estudiante será capaz de:
- Comprender qué es el Model Context Protocol (MCP), su origen y por qué estandariza la conexión entre LLMs y herramientas externas
- Conocer la arquitectura MCP: LLM, Cliente (Host) y Servidor, y el flujo completo de una petición
- Configurar servidores MCP locales en Claude Desktop (Filesystem, Memory) y depurar errores comunes
- Distinguir las capas de transporte STDIO y HTTP, sus ventajas e implicaciones de seguridad
- Conectar servidores MCP remotos desde ChatGPT, Claude.ai y n8n

## Duración Total: 4 horas

---

## Bloque 1: Introducción a MCP (50 minutos)

### 1.1 ¿Qué es MCP y por qué surge?

**MCP** (Model Context Protocol) es un **estándar abierto** creado por **Anthropic** a finales de **2024** que define cómo los modelos de lenguaje (LLMs) se conectan con herramientas, datos y servicios externos.

#### Analogía: MCP es el USB de la IA

Antes de USB, cada dispositivo (impresora, ratón, teclado, cámara) necesitaba un conector diferente. Si comprabas una impresora nueva, necesitabas un cable específico, un driver específico y esperabas que fuera compatible con tu ordenador. USB lo estandarizó todo: un solo conector, un solo protocolo, cualquier dispositivo funciona con cualquier ordenador.

```
ANTES DE USB (Antes de MCP):
---------------------------
Impresora ──[Puerto paralelo]──► PC
Ratón ──────[Puerto serie PS/2]──► PC
Cámara ─────[FireWire]──────────► PC
Teclado ────[DIN/PS2]───────────► PC

Cada dispositivo = conector diferente
Cada fabricante = protocolo propio


DESPUÉS DE USB (Con MCP):
-------------------------
Impresora ──[USB]──► PC
Ratón ──────[USB]──► PC
Cámara ─────[USB]──► PC
Teclado ────[USB]──► PC

Un estándar, cualquier dispositivo, cualquier ordenador
```

MCP hace exactamente lo mismo, pero para conectar **LLMs con herramientas externas**:

```
ANTES DE MCP:
─────────────
Gmail ──────[API propia + código custom]──────► Claude
Slack ──────[API propia + código custom]──────► ChatGPT
GitHub ─────[API propia + código custom]──────► Gemini
Calendar ───[API propia + código custom]──────► LLM local

Cada integración = implementación diferente
Cada app = repite el trabajo


CON MCP:
────────
Gmail ──────[Servidor MCP]──► Cualquier cliente MCP
Slack ──────[Servidor MCP]──► Cualquier cliente MCP
GitHub ─────[Servidor MCP]──► Cualquier cliente MCP
Calendar ───[Servidor MCP]──► Cualquier cliente MCP

Un protocolo, cualquier herramienta, cualquier cliente
```

#### El Problema que Resuelve: Acoplamiento

Sin MCP, las herramientas se implementaban **dentro** de cada aplicación (User App). Esto genera tres problemas críticos:

```
SIN MCP (ACOPLAMIENTO):
┌──────────────────────────────────────────┐
│              USER APP (Claude Desktop)    │
│                                           │
│   ┌──────────┐  ┌──────────┐             │
│   │ Tool:    │  │ Tool:    │             │
│   │ Gmail    │  │ Slack    │   ...más    │
│   │ (código  │  │ (código  │   tools     │
│   │  propio) │  │  propio) │   acopladas │
│   └──────────┘  └──────────┘             │
│                                           │
│   Problemas:                              │
│   - Complejidad creciente                 │
│   - Duplicación (cada app reimplementa)   │
│   - Difícil actualizar (cambio en API     │
│     = cambio en cada app)                 │
└──────────────────────────────────────────┘


CON MCP (DESACOPLAMIENTO):
┌──────────────────┐    ┌──────────────────┐
│   USER APP       │    │  Servidor MCP:   │
│                  │◄──►│  Gmail           │
│  Solo se conecta │    └──────────────────┘
│  a servidores    │    ┌──────────────────┐
│  MCP vía         │◄──►│  Servidor MCP:   │
│  protocolo       │    │  Slack           │
│  estándar        │    └──────────────────┘
│                  │    ┌──────────────────┐
│                  │◄──►│  Servidor MCP:   │
│                  │    │  GitHub          │
└──────────────────┘    └──────────────────┘

Ventajas:
- Cada servidor es independiente y reutilizable
- Cualquier cliente MCP puede usarlos
- Actualizar un servidor no afecta al resto
```

### 1.2 Evolución: De Prompts Simples a MCP

MCP no surge de la nada. Es el resultado de una evolución natural en cómo los LLMs interactúan con el mundo exterior:

```
EVOLUCIÓN DE LA INTERACCIÓN LLM-HERRAMIENTAS:
══════════════════════════════════════════════

FASE 1: PROMPTS SIMPLES (2022-2023)
────────────────────────────────────
Usuario: "Busca el clima en Madrid"
LLM: "No tengo acceso a internet, pero puedo decirte que
      Madrid tiene clima mediterráneo continental..."
      → SIN acceso a herramientas externas


FASE 2: PROMPT ENGINEERING PARA JSON (2023)
───────────────────────────────────────────
System: "Cuando necesites datos externos, responde en JSON:
         {\"tool\": \"weather\", \"city\": \"Madrid\"}"
LLM: {"tool": "weather", "city": "Madrid"}
App: (parsea JSON, llama API, devuelve resultado)
      → FRÁGIL: depende de que el LLM genere JSON correcto


FASE 3: FUNCTION CALLING (2023-2024)     ← Unidad 3
─────────────────────────────────────
tools = [{"type": "function", "function": {"name": "get_weather", ...}}]
LLM: tool_call → get_weather(city="Madrid")
App: (ejecuta función, devuelve resultado al LLM)
      → ROBUSTO pero ACOPLADO a cada aplicación


FASE 4: MCP (2024-presente)              ← Unidad 6
───────────────────────────────────
Servidor MCP expone herramientas vía protocolo estándar
Cualquier cliente MCP se conecta y las utiliza
      → ROBUSTO + DESACOPLADO + REUTILIZABLE
```

> **Conexión con la Unidad 3**: En la Unidad 3 aprendimos **Function Calling**, donde definimos funciones y el LLM decide cuándo invocarlas. MCP lleva este concepto al siguiente nivel: las funciones (ahora llamadas **Tools**) viven en servidores independientes, reutilizables por cualquier cliente, sin necesidad de reimplementarlas en cada aplicación.

> **Conexión con la Unidad 4**: En la Unidad 4, los agentes de n8n utilizaban herramientas (tools) integradas directamente en la plataforma. Con MCP, esas herramientas pueden estar en servidores externos y n8n se conecta a ellas a través de su nodo **MCP Client Tool**.

### 1.3 Arquitectura MCP: Los Tres Componentes

La arquitectura MCP se compone de tres actores que colaboran para ejecutar una petición del usuario:

```
┌──────────────────────────────────────────────────────────────────────────┐
│                      ARQUITECTURA MCP                                    │
│                                                                          │
│   ┌─────────────┐     ┌──────────────────┐     ┌─────────────────────┐  │
│   │             │     │                  │     │                     │  │
│   │     LLM     │◄───►│   CLIENTE MCP    │◄───►│   SERVIDOR MCP     │  │
│   │  (Cerebro)  │     │   (MCP Host)     │     │   (Herramientas)   │  │
│   │             │     │                  │     │                     │  │
│   └─────────────┘     └──────────────────┘     └─────────────────────┘  │
│                                                                          │
│   Determina qué       Orquesta la              Implementa las            │
│   herramienta usar    comunicación              integraciones             │
│   y genera la         entre LLM y               y ejecuta las            │
│   respuesta final     servidores                acciones                  │
│                                                                          │
│   Ejemplos:           Ejemplos:                 Ejemplos:                 │
│   - GPT-4             - Claude Desktop          - filesystem             │
│   - Claude            - Claude Code (CLI)       - memory                 │
│   - Gemini            - ChatGPT                 - gmail                  │
│   - Modelos locales   - n8n                     - slack                  │
│                       - Apps propias            - github                 │
└──────────────────────────────────────────────────────────────────────────┘
```

#### Componente 1: El LLM (Cerebro)

El modelo de lenguaje es el **cerebro** del sistema. Recibe la consulta del usuario, analiza las herramientas disponibles, decide cuál usar y genera la respuesta final con los datos obtenidos. El LLM **no ejecuta** las herramientas directamente; solo indica **qué** herramienta invocar y con **qué parámetros**.

#### Componente 2: El Cliente MCP (MCP Host)

El cliente MCP es el **orquestador**. Es la aplicación que:
- Conecta con uno o más servidores MCP
- Descubre las herramientas disponibles en cada servidor
- Envía la lista de herramientas al LLM para que decida
- Transforma las peticiones del LLM al formato JSON-RPC que entienden los servidores
- Recibe las respuestas de los servidores y se las pasa al LLM
- Gestiona el contexto de la conversación

Ejemplos de clientes MCP: **Claude Desktop**, **Claude Code** (CLI), **ChatGPT** (con conectores), **Claude.ai**, **n8n** (con nodo MCP Client Tool), aplicaciones personalizadas.

> **Claude Code y sus herramientas nativas**: Claude Code (el CLI de Anthropic) ya puede leer y escribir archivos, ejecutar comandos y buscar en la web **sin necesitar servidores MCP** — usa herramientas internas propias (`Read`, `Write`, `Edit`, `Bash`…). Esto es diferente del servidor MCP `@modelcontextprotocol/server-filesystem`. Para añadir servidores MCP a Claude Code se configura `~/.claude/settings.json` bajo `mcpServers`, con la misma estructura JSON que Claude Desktop.

#### Componente 3: El Servidor MCP (Herramientas)

El servidor MCP es quien **implementa** las integraciones reales. Cada servidor:
- Expone un conjunto de **Tools** (herramientas ejecutables)
- Puede exponer **Resources** (datos de solo lectura)
- Puede exponer **Prompts** (plantillas de prompts reutilizables)
- Se comunica mediante el protocolo JSON-RPC 2.0

Un servidor puede ser **local** (ejecutándose en tu máquina) o **remoto** (en la nube, accesible por HTTP).

#### Qué Expone un Servidor MCP

| Primitiva | Descripción | Ejemplo | Controlado por |
|-----------|-------------|---------|----------------|
| **Tools** | Acciones ejecutables que el LLM puede invocar | `read_file`, `send_email`, `search_web` | El modelo (LLM decide cuándo usarlas) |
| **Resources** | Datos de solo lectura, como archivos o registros | Contenido de un fichero, esquema de BD | La aplicación (el cliente las solicita) |
| **Prompts** | Plantillas de prompts reutilizables y parametrizables | "Analiza este código", "Resume este texto" | El usuario (elige qué prompt usar) |

### 1.4 Flujo Completo de una Petición MCP

Veamos paso a paso qué ocurre cuando un usuario hace una pregunta que requiere una herramienta externa:

```
FLUJO COMPLETO DE UNA PETICIÓN MCP (9 PASOS):
═══════════════════════════════════════════════

 USUARIO                CLIENTE MCP             SERVIDOR MCP           LLM
    │                   (Claude Desktop)        (filesystem)
    │                        │                       │                  │
    │  1. "¿Qué archivos     │                       │                  │
    │   hay en mi proyecto?" │                       │                  │
    │───────────────────────►│                       │                  │
    │                        │  2. Conecta con       │                  │
    │                        │     servidor y         │                  │
    │                        │     obtiene tools      │                  │
    │                        │──────────────────────►│                  │
    │                        │                       │                  │
    │                        │  3. Lista de tools:   │                  │
    │                        │     list_directory,   │                  │
    │                        │     read_file, ...    │                  │
    │                        │◄──────────────────────│                  │
    │                        │                       │                  │
    │                        │  4. Envía pregunta    │                  │
    │                        │     + tools al LLM    │                  │
    │                        │──────────────────────────────────────────►│
    │                        │                       │                  │
    │                        │  5. LLM decide:       │                  │
    │                        │     usar              │                  │
    │                        │     list_directory     │                  │
    │                        │◄──────────────────────────────────────────│
    │                        │                       │                  │
    │                        │  6. Transforma a      │                  │
    │                        │     JSON-RPC y        │                  │
    │                        │     envía al servidor │                  │
    │                        │──────────────────────►│                  │
    │                        │                       │  7. Ejecuta      │
    │                        │                       │     la acción    │
    │                        │  8. Resultado:        │     (lee disco)  │
    │                        │     [archivo1.py,     │                  │
    │                        │      archivo2.md]     │                  │
    │                        │◄──────────────────────│                  │
    │                        │                       │                  │
    │                        │  9. Envía resultado   │                  │
    │                        │     al LLM para       │                  │
    │                        │     formular respuesta│                  │
    │                        │──────────────────────────────────────────►│
    │                        │                       │                  │
    │                        │  Respuesta formateada │                  │
    │                        │◄──────────────────────────────────────────│
    │                        │                       │                  │
    │  "Tu proyecto tiene    │                       │                  │
    │   2 archivos:          │                       │                  │
    │   archivo1.py y        │                       │                  │
    │   archivo2.md"         │                       │                  │
    │◄───────────────────────│                       │                  │
```

**Resumen del flujo:**
1. El usuario hace una pregunta al cliente MCP
2. El cliente se conecta al servidor MCP y solicita la lista de herramientas disponibles
3. El servidor responde con sus Tools, Resources y Prompts
4. El cliente envía la pregunta del usuario junto con las herramientas disponibles al LLM
5. El LLM analiza y decide qué herramienta usar y con qué parámetros
6. El cliente transforma la petición del LLM al formato JSON-RPC y la envía al servidor
7. El servidor ejecuta la acción real (leer archivo, consultar API, etc.)
8. El servidor devuelve el resultado al cliente
9. El cliente envía el resultado al LLM, que formula la respuesta final para el usuario

### 1.5 Formato JSON-RPC 2.0

MCP utiliza **JSON-RPC 2.0** como formato de comunicación entre clientes y servidores. Es un protocolo estándar, ligero y bien definido.

#### Estructura de una Petición JSON-RPC

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "list_directory",
    "arguments": {
      "path": "/Users/alumno/proyecto"
    }
  }
}
```

| Campo | Descripción |
|-------|-------------|
| `jsonrpc` | Versión del protocolo (siempre `"2.0"`) |
| `id` | Identificador único de la petición (para correlacionar con la respuesta) |
| `method` | Método a invocar (`tools/call`, `tools/list`, `resources/read`, etc.) |
| `params` | Parámetros del método (nombre de la tool y sus argumentos) |

#### Estructura de una Respuesta JSON-RPC

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "archivo1.py\narchivo2.md\nREADME.txt"
      }
    ]
  }
}
```

#### Métodos Principales de MCP

| Método | Descripción |
|--------|-------------|
| `initialize` | Handshake inicial entre cliente y servidor |
| `tools/list` | Obtener la lista de herramientas disponibles |
| `tools/call` | Invocar una herramienta con argumentos |
| `resources/list` | Listar recursos disponibles |
| `resources/read` | Leer un recurso específico |
| `prompts/list` | Listar prompts disponibles |
| `prompts/get` | Obtener un prompt con sus argumentos |

#### Ventajas de JSON-RPC 2.0

- **Estándar**: protocolo ampliamente adoptado, no es propietario
- **Legible**: formato JSON, fácil de inspeccionar y depurar
- **Flexible**: soporta peticiones, respuestas, notificaciones y errores
- **Ligero**: overhead mínimo comparado con otros protocolos RPC

> **Vídeo recomendado**: *Introducción a MCP* (3:18 min) - Disponible en los recursos del curso.

---

## Bloque 2: Configuración de Servidores MCP Locales (50 minutos)

### 2.1 Claude Desktop como Cliente MCP

**Claude Desktop** es la aplicación de escritorio de Anthropic y el **primer cliente MCP** del ecosistema. Permite conectar servidores MCP locales que se ejecutan en tu máquina mediante el transporte STDIO.

Para configurar servidores MCP en Claude Desktop se utiliza un archivo de configuración JSON:

| Sistema Operativo | Ruta del archivo de configuración |
|-------------------|-----------------------------------|
| **macOS** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Windows** | `%APPDATA%\Claude\claude_desktop_config.json` |

### 2.2 Estructura del Archivo de Configuración

El archivo `claude_desktop_config.json` tiene la siguiente estructura:

```json
{
  "mcpServers": {
    "nombreServidor": {
      "command": "comando_ejecutable",
      "args": ["argumento1", "argumento2"],
      "env": {
        "VARIABLE": "valor"
      },
      "workingDirectory": "/ruta/opcional"
    },
    "otroServidor": {
      "command": "otro_comando",
      "args": ["..."]
    }
  }
}
```

| Campo | Obligatorio | Descripción |
|-------|:-----------:|-------------|
| `command` | Sí | Comando ejecutable que arranca el servidor MCP |
| `args` | No | Lista de argumentos que se pasan al comando |
| `env` | No | Variables de entorno que necesita el servidor |
| `workingDirectory` | No | Directorio de trabajo desde donde se ejecuta el comando |

**Puntos clave:**
- Se pueden configurar **múltiples servidores** simultáneamente
- Cada servidor se identifica por un **nombre único** dentro de `mcpServers`
- Claude Desktop arranca cada servidor como un **proceso hijo** al iniciarse
- Los servidores se comunican con Claude Desktop vía **STDIO** (stdin/stdout)

### 2.3 Primer Servidor: Filesystem

El servidor **Filesystem** (`@modelcontextprotocol/server-filesystem`) es uno de los servidores oficiales de Anthropic. Permite al LLM leer, escribir y navegar archivos en directorios específicos de tu máquina.

> **¿No hace esto ya Claude Code?** Claude Code tiene herramientas de ficheros nativas (`Read`, `Write`, `Edit`, `Glob`) que no son servidores MCP — son internas al CLI y no usan JSON-RPC. El servidor Filesystem MCP es para **Claude Desktop** y otros clientes que no tienen esas capacidades integradas. La distinción importante: las tools nativas de Claude Code no se configuran en `mcpServers`, no son reutilizables por otros clientes y no aparecen en MCP Inspector.

#### Configuración

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/alumno/Documents",
        "/Users/alumno/proyecto"
      ]
    }
  }
}
```

**Explicación:**
- `npx -y`: Ejecuta el paquete npm sin instalación previa (el flag `-y` acepta automáticamente)
- `@modelcontextprotocol/server-filesystem`: Paquete del servidor oficial
- Las rutas al final son los **directorios permitidos** (el servidor solo puede acceder a estos)

> **Alternativa con `uvx`**: Para servidores MCP escritos en Python, se usa `uvx` (del gestor `uv`) en lugar de `npx`. Verás esta sintaxis en muchos servidores de terceros y en la documentación oficial:
> ```json
> { "command": "uvx", "args": ["mcp-server-git"] }
> ```
> `uvx` descarga y ejecuta paquetes Python de PyPI de forma aislada, igual que `npx` hace con npm.

#### Herramientas que Expone

| Herramienta | Descripción |
|-------------|-------------|
| `read_file` | Lee el contenido de un archivo |
| `write_file` | Escribe contenido en un archivo |
| `list_directory` | Lista los archivos y carpetas de un directorio |
| `create_directory` | Crea un nuevo directorio |
| `move_file` | Mueve o renombra un archivo |
| `search_files` | Busca archivos por patrón (glob) |
| `get_file_info` | Obtiene metadatos de un archivo (tamaño, fecha, permisos) |

#### Ejemplo de Uso

Una vez configurado, puedes preguntarle a Claude Desktop:

```
Usuario: "Lista los archivos de mi proyecto y muestra el contenido de main.py"

Claude Desktop:
1. Conecta con el servidor filesystem
2. Invoca list_directory(path="/Users/alumno/proyecto")
3. Recibe: ["main.py", "utils.py", "README.md", "requirements.txt"]
4. Invoca read_file(path="/Users/alumno/proyecto/main.py")
5. Recibe el contenido del archivo
6. Muestra la respuesta formateada al usuario
```

#### Consideraciones de Seguridad

- El servidor **solo accede** a los directorios especificados en la configuración
- No puede salir de esos directorios (sandboxing)
- Claude Desktop solicita **confirmación del usuario** antes de ejecutar acciones de escritura
- Es responsabilidad del usuario revisar qué directorios expone

### 2.4 Servidor Memory: Persistencia entre Sesiones

El servidor **Memory** (`@modelcontextprotocol/server-memory`) permite que Claude Desktop **recuerde información** entre sesiones. En sus versiones actuales utiliza un **grafo de conocimiento** (entidades, observaciones y relaciones) para almacenar y recuperar datos de forma estructurada, sin necesidad de configurar ninguna base de datos externa.

#### Configuración

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/alumno/Documents"
      ]
    },
    "memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ]
    }
  }
}
```

**Notas:**
- No requiere configuración adicional; el grafo de conocimiento se almacena automáticamente
- La memoria persiste entre reinicios de Claude Desktop
- El servidor estructura la información como entidades (personas, proyectos, conceptos) con observaciones y relaciones entre ellas
- Se pueden almacenar preferencias del usuario, notas, hechos importantes, etc.

#### Ejemplo de Uso

```
Sesión 1:
Usuario: "Recuerda que mi proyecto se llama 'MiApp' y uso Python 3.11"
Claude: (almacena entidad 'MiApp' con observaciones en el grafo) "Entendido."

Sesión 2 (días después):
Usuario: "¿Qué sabes sobre mi proyecto?"
Claude: (consulta el grafo de conocimiento) "Tu proyecto se llama 'MiApp'
         y utilizas Python 3.11."
```

### 2.5 Configuración Completa: Múltiples Servidores

Un archivo de configuración típico con varios servidores:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/alumno/Documents",
        "/Users/alumno/proyecto"
      ]
    },
    "memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ]
    },
    "fetch": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-fetch"
      ]
    }
  }
}
```

Con esta configuración, Claude Desktop tiene acceso a:
- **filesystem**: Leer/escribir archivos en los directorios permitidos
- **memory**: Recordar información entre sesiones
- **fetch**: Hacer peticiones HTTP a URLs externas (obtener contenido web)

### 2.6 Logs y Debugging

Cuando un servidor MCP no funciona correctamente, los logs son la primera herramienta de diagnóstico.

#### Ubicación de Logs

| Sistema | Ruta de logs |
|---------|-------------|
| **macOS** | `~/Library/Application Support/Claude/logs/` |
| **Windows** | `%APPDATA%\Claude\logs\` |

#### Problemas Comunes y Soluciones

| Problema | Causa Típica | Solución |
|----------|-------------|----------|
| Servidor no aparece en Claude | Error en el JSON de configuración | Validar JSON (comas, llaves, comillas) |
| `command not found` | El comando no está en el PATH | Usar ruta absoluta al ejecutable (`/usr/local/bin/npx`) |
| Timeout al conectar | Servidor tarda en arrancar | Aumentar timeout o revisar dependencias |
| Herramientas no disponibles | Servidor arranca pero no expone tools | Revisar versión del paquete y logs del servidor |
| Permiso denegado | El servidor no tiene acceso al recurso | Verificar permisos de archivo/directorio |

#### Proceso de Depuración

```
DEBUGGING DE SERVIDORES MCP:
════════════════════════════

1. Verificar JSON válido
   └─► Usar un validador JSON online o jq

2. Reiniciar Claude Desktop
   └─► Los servidores se recargan al iniciar

3. Revisar logs
   └─► ~/Library/Application Support/Claude/logs/

4. Probar el comando manualmente
   └─► Ejecutar en terminal: npx -y @modelcontextprotocol/server-filesystem /ruta
   └─► Debe arrancar sin errores

5. Verificar dependencias
   └─► Node.js instalado? (node --version)
   └─► npx disponible? (npx --version)
```

> **Vídeo recomendado**: *Configuración de servidores MCP* (3:27 min) - Disponible en los recursos del curso.

### 2.7 Herramienta de Depuración: MCP Inspector

**MCP Inspector** es la herramienta oficial de Anthropic para inspeccionar y probar servidores MCP de forma interactiva, sin necesidad de un cliente LLM. Se cubre en detalle en la Sesión 2, pero conviene conocerla desde el primer servidor que configuréis.

```bash
# Lanzar Inspector contra el servidor filesystem
npx @modelcontextprotocol/inspector npx @modelcontextprotocol/server-filesystem /ruta/proyecto
```

Abre una interfaz web en `http://localhost:6274` donde podéis ver las tools disponibles, ejecutarlas con parámetros y revisar las respuestas JSON-RPC en tiempo real.

### 2.8 Instalación Simplificada: Desktop Extensions (.dxt)

Anthropic introdujo en 2025 los **Desktop Extensions** (archivos `.dxt`) para Claude Desktop. Son paquetes que instalan un servidor MCP con un **doble clic**, sin necesidad de editar el archivo JSON de configuración manualmente.

```
Instalación tradicional (JSON):          Instalación con .dxt:
──────────────────────────────           ────────────────────
1. Localizar el archivo config           1. Descargar archivo .dxt
2. Editar JSON manualmente               2. Doble clic → Claude Desktop
3. Reiniciar Claude Desktop                 instala y configura solo
4. Verificar que arranca                 3. Listo
```

Los servidores `.dxt` se pueden encontrar en el directorio oficial de Anthropic y en repositorios de la comunidad. Para desarrolladores, es posible empaquetar un servidor propio como `.dxt`.

---

--- DESCANSO (15 minutos) ---

---

## Bloque 3: Capas de Transporte: STDIO vs HTTP (40 minutos)

### 3.1 ¿Qué es una Capa de Transporte?

La **capa de transporte** define **cómo** viajan los mensajes JSON-RPC entre el cliente MCP y el servidor MCP. MCP soporta dos capas de transporte principales:

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    CAPAS DE TRANSPORTE EN MCP                             │
│                                                                          │
│   ┌─────────────────────────────┐   ┌─────────────────────────────────┐  │
│   │         STDIO               │   │       HTTP (Streamable)         │  │
│   │                             │   │                                 │  │
│   │   Cliente ◄──stdin──► Srv   │   │   Cliente ◄──HTTP──► Servidor  │  │
│   │           ◄─stdout──►       │   │            (red/internet)       │  │
│   │                             │   │                                 │  │
│   │   Local, proceso hijo       │   │   Local o remoto               │  │
│   │   Sin red                   │   │   Vía red/internet              │  │
│   │   Máximo aislamiento        │   │   Compartible                   │  │
│   └─────────────────────────────┘   └─────────────────────────────────┘  │
│                                                                          │
│   Mismos mensajes JSON-RPC, diferente medio de transporte                │
└──────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Transporte STDIO

**STDIO** (Standard Input/Output) es el transporte por defecto para servidores MCP locales. El cliente MCP arranca el servidor como un **proceso hijo** y se comunica con él a través de las tuberías estándar del sistema operativo: **stdin** (entrada) y **stdout** (salida).

```
TRANSPORTE STDIO:
═════════════════

┌───────────────────┐                    ┌───────────────────┐
│   CLIENTE MCP     │   stdin (entrada)  │   SERVIDOR MCP    │
│                   │───────────────────►│                   │
│   (Claude Desktop)│                    │   (filesystem)    │
│                   │   stdout (salida)  │                   │
│                   │◄───────────────────│   Proceso hijo    │
└───────────────────┘                    └───────────────────┘

- El cliente ARRANCA el servidor como proceso hijo
- Comunicación vía tuberías del SO (no hay red involucrada)
- Cuando el cliente se cierra, el servidor también se detiene
```

#### Ventajas de STDIO

| Ventaja | Descripción |
|---------|-------------|
| **Seguridad** | No hay comunicación por red; todo ocurre dentro de la máquina |
| **Simplicidad** | Sin configuración de puertos, certificados ni autenticación |
| **Aislamiento** | El servidor es un proceso hijo controlado por el cliente |
| **Rendimiento** | Comunicación directa vía tuberías del SO, latencia mínima |

#### Limitaciones de STDIO

| Limitación | Descripción |
|------------|-------------|
| **Solo local** | El servidor debe ejecutarse en la misma máquina que el cliente |
| **Proceso hijo** | El servidor se detiene cuando el cliente se cierra |
| **No compartible** | Un servidor STDIO sirve a un solo cliente a la vez |
| **No apto para cloud** | No se puede desplegar en un servidor remoto |

#### Configuración STDIO (lo que ya hemos visto)

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/ruta"]
    }
  }
}
```

El campo `command` + `args` le dice al cliente **cómo arrancar** el proceso hijo.

### 3.3 Transporte HTTP

El transporte **HTTP** permite que el servidor MCP se ejecute de forma independiente (como un servicio web) y que los clientes se conecten a él por red.

#### HTTP Streamable (Recomendado)

La especificación actual de MCP recomienda **HTTP Streamable** como transporte remoto. El servidor expone un endpoint HTTP y el cliente se conecta a él:

```python
# Ejemplo: Servidor MCP con transporte HTTP (Python con FastMCP)
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mi-servidor")

@mcp.tool()
def saludar(nombre: str) -> str:
    """Saluda a una persona por su nombre."""
    return f"Hola, {nombre}! Bienvenido."

# Arrancar con transporte HTTP
mcp.run(transport="http", host="0.0.0.0", port=8080, path="/mcp")
```

```
TRANSPORTE HTTP:
════════════════

┌───────────────────┐        HTTP         ┌───────────────────┐
│   CLIENTE MCP     │  ─────────────────► │   SERVIDOR MCP    │
│                   │  POST /mcp          │                   │
│   (cualquiera)    │  ◄───────────────── │   Puerto 8080     │
│                   │  Respuesta JSON     │                   │
└───────────────────┘                     └───────────────────┘

- El servidor se ejecuta INDEPENDIENTEMENTE
- Puede estar en la misma máquina o en la nube
- Múltiples clientes pueden conectarse al mismo servidor
```

#### SSE (Server-Sent Events) - Deprecado

El transporte **SSE** fue el método original para comunicación remota en MCP, pero está **deprecado** (obsoleto) en favor de HTTP Streamable:

```python
# SSE (DEPRECADO - no usar en nuevos desarrollos)
mcp.run(transport="sse")  # Expone endpoint /sse
```

> **Nota**: Si encuentras documentación o servidores que usen SSE, es probable que sean versiones antiguas. Para nuevos desarrollos, utiliza siempre HTTP Streamable.

### 3.4 Comparativa STDIO vs HTTP

| Aspecto | STDIO | HTTP |
|---------|-------|------|
| **Ubicación** | Solo local | Local o remoto |
| **Red** | No requiere | Requiere red/internet |
| **Arranque** | El cliente lo arranca | Se ejecuta independientemente |
| **Compartir** | Un cliente por servidor | Múltiples clientes simultáneos |
| **Configuración** | `command` + `args` | URL del endpoint |
| **Seguridad** | Inherentemente seguro (sin red) | Requiere HTTPS, autenticación |
| **Latencia** | Mínima (tuberías SO) | Dependiente de la red |
| **Caso de uso** | Desarrollo local, uso personal | Equipos, producción, cloud |

### 3.5 Seguridad según el Transporte

La elección de transporte tiene implicaciones directas en la seguridad:

```
MATRIZ DE SEGURIDAD POR TRANSPORTE:
════════════════════════════════════

                    STDIO                    HTTP
                 ┌───────────────┐     ┌───────────────────────┐
  Riesgo de      │  MUY BAJO     │     │  MEDIO-ALTO           │
  exposición     │  (sin red)    │     │  (expuesto a la red)  │
                 └───────────────┘     └───────────────────────┘

  Medidas         - Limitar           - HTTPS obligatorio
  necesarias        directorios       - Autenticación (JWT,
                  - Permisos SO         API keys)
                                      - Validación de entrada
                                      - Rate limiting
                                      - Logs de auditoría
                                      - CORS configurado
```

#### Buenas Prácticas de Seguridad para HTTP

1. **Siempre HTTPS**: Nunca exponer un servidor MCP por HTTP plano en producción
2. **Autenticación**: Implementar JWT tokens o API keys para controlar el acceso
3. **Validación**: Validar todos los parámetros de entrada en el servidor
4. **Logs de auditoría**: Registrar todas las invocaciones de herramientas
5. **Rate limiting**: Limitar el número de peticiones por cliente/minuto
6. **CORS**: Configurar correctamente los orígenes permitidos

### 3.6 Cuándo Usar Cada Transporte

```
ÁRBOL DE DECISIÓN: STDIO vs HTTP
═════════════════════════════════

¿El servidor es para uso personal/local?
├── SÍ ──► STDIO
│          Más simple, más seguro, sin configuración de red
│
└── NO ──► HTTP
           │
           ├── ¿Necesitas compartir entre equipos? ──► HTTP
           ├── ¿Va a desplegarse en la nube? ──► HTTP
           ├── ¿Múltiples clientes lo van a usar? ──► HTTP
           └── ¿Es un servicio de producción? ──► HTTP + HTTPS + Auth
```

---

## Bloque 4: Servidores MCP Remotos y Otros Clientes (40 minutos)

### 4.1 ChatGPT con Servidores MCP Remotos

Desde 2025, **ChatGPT** (cuentas Plus y superiores) soporta la conexión con servidores MCP remotos a través de su funcionalidad de **Conectores**.

#### Configuración de un Conector MCP en ChatGPT

```
PASOS PARA CONFIGURAR MCP EN CHATGPT:
══════════════════════════════════════

1. Abrir ChatGPT ──► Configuración (Settings)

2. Ir a "Aplicaciones y Conectores" (Apps & Connectors)

3. Activar "Modo desarrollador" (Developer Mode)

4. Clic en "Crear conector" (Create Connector)

5. Rellenar:
   ┌─────────────────────────────────────────────┐
   │  Nombre: Mi Servidor MCP                     │
   │  URL:    https://mi-servidor.com/mcp          │
   │  Auth:   API Key / OAuth / Sin auth           │
   └─────────────────────────────────────────────┘

6. Guardar y probar
```

#### Opciones de Autenticación

| Tipo | Descripción | Cuándo Usar |
|------|-------------|-------------|
| **Sin autenticación** | Acceso abierto | Solo desarrollo/pruebas locales |
| **API Key** | Clave secreta en cabecera HTTP | Servidores propios, uso personal |
| **OAuth 2.0** | Flujo de autorización completo | Integraciones con terceros (Google, GitHub, etc.) |

> **Importante**: ChatGPT solo soporta servidores MCP **remotos** (HTTP). No puede conectarse a servidores locales STDIO, ya que ChatGPT se ejecuta en los servidores de OpenAI, no en tu máquina.

### 4.2 Repositorios Públicos de Servidores MCP

Existe un ecosistema creciente de servidores MCP listos para usar. Los principales repositorios son:

#### Servidores Oficiales de Anthropic

Disponibles en el repositorio oficial de GitHub: `github.com/modelcontextprotocol/servers`

| Servidor | Descripción | Transporte |
|----------|-------------|------------|
| `filesystem` | Lectura/escritura de archivos locales | STDIO |
| `memory` | Persistencia entre sesiones (SQLite) | STDIO |
| `fetch` | Peticiones HTTP a URLs externas | STDIO |
| `sqlite` | Consultas a bases de datos SQLite | STDIO |
| `git` | Operaciones Git (status, diff, log, commit) | STDIO |

#### Directorio mcpservers.org

**mcpservers.org** es un directorio comunitario que cataloga servidores MCP por categoría:

| Categoría | Ejemplos de Servidores |
|-----------|----------------------|
| **Productividad** | Gmail, Google Calendar, Notion, Todoist |
| **Desarrollo** | GitHub, GitLab, Docker, Kubernetes |
| **Datos** | PostgreSQL, MongoDB, Elasticsearch |
| **Comunicación** | Slack, Discord, Telegram |
| **Análisis** | Google Analytics, Mixpanel |
| **Almacenamiento** | Google Drive, Dropbox, S3 |
| **Web** | Brave Search, Puppeteer, Playwright |

#### Criterios para Evaluar un Servidor MCP

Antes de usar un servidor MCP de terceros, evalúalo con estos criterios:

| Criterio | Qué Verificar |
|----------|---------------|
| **Reputación** | Estrellas en GitHub, autor conocido, comunidad activa |
| **Código abierto** | ¿El código es visible? ¿Puedes auditarlo? |
| **Mantenimiento** | ¿Última actualización reciente? ¿Issues resueltos? |
| **Documentación** | ¿Tiene documentación clara de instalación y uso? |
| **Política de datos** | ¿Qué datos recopila? ¿Los envía a terceros? |
| **Seguridad** | ¿Tiene vulnerabilidades conocidas? ¿Usa dependencias seguras? |

> **Precaución**: Un servidor MCP tiene acceso a las herramientas que expone. Un servidor malicioso podría exfiltrar datos o ejecutar acciones no deseadas. **Siempre revisa el código fuente** de servidores de terceros antes de instalarlos.

### 4.3 Claude.ai con Conectores Personalizados

**Claude.ai** (la versión web) también soporta servidores MCP, pero con diferencias respecto a Claude Desktop:

| Característica | Claude Desktop | Claude.ai |
|---------------|---------------|-----------|
| **STDIO** | Sí (servidores locales) | No (no ejecuta procesos locales) |
| **HTTP** | Sí | Sí |
| **Configuración** | Archivo JSON local | Panel web de conectores |
| **Servidores locales** | Sí | No (solo remotos vía HTTP) |
| **Autenticación** | Vía env en JSON | Vía panel web (API key, OAuth) |

```
DIFERENCIA CLAVE:
═════════════════

Claude Desktop (app escritorio)
├── Puede usar STDIO (local) ──► Arranca servidores en tu máquina
└── Puede usar HTTP (remoto) ──► Se conecta a servidores en la nube

Claude.ai (web)
└── Solo HTTP (remoto) ──► No puede arrancar procesos en tu máquina
                            (se ejecuta en los servidores de Anthropic)
```

### 4.4 MCP con n8n

> **Conexión con la Unidad 4**: En la Unidad 4 aprendimos a construir agentes de IA en n8n con herramientas nativas. Ahora, con el nodo **MCP Client Tool**, los agentes de n8n pueden conectarse a servidores MCP externos, ampliando enormemente sus capacidades.

n8n incluye un nodo **MCP Client Tool** que permite a los agentes de IA conectarse con servidores MCP:

```
AGENTE n8n CON MCP:
═══════════════════

┌──────────────────────────────────────────────────────────┐
│                    WORKFLOW n8n                            │
│                                                           │
│   [Chat Trigger] ──► [AI Agent] ──► [Respuesta]          │
│                          │                                │
│                    ┌─────┴─────┐                          │
│                    │  Tools:   │                          │
│                    ├───────────┤                          │
│                    │ MCP Client│──► Servidor MCP externo  │
│                    │ Tool      │   (filesystem, gmail...) │
│                    ├───────────┤                          │
│                    │ Calculator│   (tool nativa de n8n)   │
│                    └───────────┘                          │
└──────────────────────────────────────────────────────────┘
```

#### Configuración del Nodo MCP Client Tool

| Campo | Descripción |
|-------|-------------|
| **Tipo de transporte** | STDIO o HTTP (según el servidor) |
| **Command** (STDIO) | Comando para arrancar el servidor (ej: `npx`) |
| **Args** (STDIO) | Argumentos del comando |
| **URL** (HTTP) | URL del servidor MCP remoto |
| **Autenticación** | API Key, Bearer Token, o sin autenticación |

#### Ejemplo: Agente n8n con Servidor Filesystem vía MCP

```
Configuración del nodo MCP Client Tool:
─────────────────────────────────────────
Transporte: STDIO
Command: npx
Args: -y @modelcontextprotocol/server-filesystem /ruta/proyecto

El agente de n8n ahora puede:
- Leer archivos del proyecto
- Listar directorios
- Buscar archivos por patrón
...todo a través del protocolo MCP estándar
```

> La ventaja de usar MCP en n8n es que **cualquier servidor MCP** funciona sin necesidad de crear integraciones personalizadas. Si existe un servidor MCP para un servicio, el agente de n8n puede usarlo directamente.

---

--- DESCANSO (15 minutos) ---

---

## Bloque 5: Práctica Guiada (30 minutos)

### 5.1 Ejercicio Guiado: Configurar tu Primer Servidor MCP

En esta práctica guiada, configuraremos el servidor **Filesystem** en Claude Desktop paso a paso.

#### Requisitos Previos

- Claude Desktop instalado
- Node.js instalado (versión 18 o superior)
- npx disponible en el PATH

#### Pasos

**Paso 1: Verificar requisitos**

```bash
# Verificar Node.js
node --version
# Debe mostrar v18.x.x o superior

# Verificar npx
npx --version
```

**Paso 2: Crear/editar el archivo de configuración**

```bash
# macOS: Abrir el archivo de configuración
# (se crea si no existe)
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Paso 3: Añadir la configuración del servidor Filesystem**

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/alumno/Documents"
      ]
    }
  }
}
```

**Paso 4: Reiniciar Claude Desktop**

- Cerrar completamente Claude Desktop
- Volver a abrirlo
- Verificar que aparece el icono de herramientas (martillo) en la interfaz

**Paso 5: Probar el servidor**

Pregúntale a Claude Desktop:
- "Lista los archivos en mi carpeta Documents"
- "Lee el contenido del archivo X"
- "Crea un archivo llamado prueba.txt con el texto 'Hola MCP'"

### 5.2 Ejercicio Guiado: Añadir el Servidor Memory

**Paso 1: Ampliar la configuración**

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/alumno/Documents"
      ]
    },
    "memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ]
    }
  }
}
```

**Paso 2: Reiniciar Claude Desktop y probar**

- "Recuerda que mi lenguaje favorito es Python"
- (Cerrar y abrir Claude Desktop)
- "¿Qué recuerdas sobre mí?"

### 5.3 Verificación y Diagnóstico

Si algo no funciona, sigue la lista de verificación:

```
CHECKLIST DE VERIFICACIÓN:
══════════════════════════
[ ] El JSON del archivo de configuración es válido (sin errores de sintaxis)
[ ] Node.js está instalado (node --version funciona)
[ ] npx está disponible (npx --version funciona)
[ ] Claude Desktop se ha reiniciado completamente después del cambio
[ ] Aparece el icono de herramientas en la interfaz de Claude Desktop
[ ] Los logs no muestran errores: ~/Library/Application Support/Claude/logs/
```

---

## Resumen de la Sesión

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    RESUMEN - SESIÓN 1: MCP                                │
│                                                                          │
│   1. MCP = Model Context Protocol                                        │
│      - Estándar abierto de Anthropic (2024)                              │
│      - "El USB de la IA": estandariza la conexión LLM ↔ herramientas     │
│      - Resuelve el acoplamiento: servidores independientes y reutilizables│
│                                                                          │
│   2. ARQUITECTURA MCP (3 componentes)                                    │
│      - LLM: decide qué herramienta usar                                  │
│      - Cliente MCP: orquesta la comunicación                             │
│      - Servidor MCP: implementa las herramientas (Tools, Resources,      │
│        Prompts)                                                          │
│                                                                          │
│   3. CONFIGURACIÓN LOCAL (Claude Desktop)                                │
│      - Archivo claude_desktop_config.json                                │
│      - Servidores: filesystem, memory, fetch                             │
│      - Debugging: logs, validación JSON, prueba manual                   │
│                                                                          │
│   4. TRANSPORTE: STDIO vs HTTP                                           │
│      - STDIO: local, seguro, simple, un solo cliente                     │
│      - HTTP: remoto, compartible, requiere seguridad adicional           │
│                                                                          │
│   5. CLIENTES MCP                                                        │
│      - Claude Desktop: STDIO + HTTP                                      │
│      - ChatGPT: solo HTTP (conectores remotos)                           │
│      - Claude.ai: solo HTTP                                              │
│      - n8n: STDIO + HTTP (nodo MCP Client Tool)                          │
└──────────────────────────────────────────────────────────────────────────┘
```

**Conceptos clave aprendidos:**

1. **MCP** es un estándar abierto que desacopla las herramientas de los clientes, permitiendo que cualquier servidor MCP funcione con cualquier cliente MCP.

2. La **arquitectura MCP** tiene tres componentes: el LLM (decide), el cliente MCP (orquesta) y el servidor MCP (ejecuta), comunicándose mediante **JSON-RPC 2.0**.

3. Claude Desktop se configura con el archivo `claude_desktop_config.json`, donde se declaran servidores locales como **filesystem** y **memory** que se ejecutan vía **STDIO**.

4. El transporte **STDIO** es ideal para uso local (seguro, simple), mientras que **HTTP** es necesario para servidores remotos, compartidos o en la nube (requiere medidas de seguridad adicionales).

5. Además de Claude Desktop, otros clientes MCP como **ChatGPT**, **Claude.ai** y **n8n** pueden conectarse a servidores MCP, cada uno con sus particularidades de transporte y configuración.

---

## Conexión con la Sesión 2

En la próxima sesión abordaremos la **creación de servidores MCP personalizados** y temas avanzados:

- **Desarrollo de servidores MCP**: Crear servidores propios con Python (FastMCP) y TypeScript
- **Tools, Resources y Prompts**: Implementar las tres primitivas en detalle
- **Caso práctico Gmail**: Construir un servidor MCP que gestione correo electrónico
- **Clientes MCP programáticos**: Desarrollar clientes propios en Python
- **Seguridad avanzada**: Autenticación, autorización, sandboxing y buenas prácticas
- **Despliegue**: Publicar servidores MCP en la nube para uso en producción

---

## Conexiones con Otras Unidades

```
┌──────────────────────────────────────────────────────────────────────────┐
│              MAPA DE CONEXIONES DEL CURSO                                │
│                                                                          │
│   Unidad 3: APIs y Function Calling                                      │
│        │  Function Calling = herramientas DENTRO de la app               │
│        │  MCP = herramientas en SERVIDORES EXTERNOS                      │
│        ▼                                                                 │
│   Unidad 4: Agentes de IA y n8n                                          │
│        │  Agentes con tools nativas → Agentes con MCP Client Tool        │
│        │  n8n se conecta a servidores MCP vía nodo dedicado              │
│        ▼                                                                 │
│   Unidad 5: RAG                                                          │
│        │  Un servidor MCP puede exponer una base de datos vectorial       │
│        │  como herramienta, integrando RAG en cualquier cliente MCP       │
│        ▼                                                                 │
│   Unidad 6: MCP  ← ESTAMOS AQUÍ                                         │
│        Protocolo estándar que UNIFICA todo lo anterior                   │
│        Function Calling + Agentes + RAG = accesibles vía MCP             │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Actividades

### Ejercicios de esta Sesión

Completa los ejercicios prácticos disponibles en [ejercicios.md](./ejercicios.md):

1. **Configurar servidor Filesystem** - Instalar y probar el servidor MCP de sistema de archivos en Claude Desktop
2. **Configurar servidor Memory** - Añadir persistencia entre sesiones y verificar su funcionamiento
3. **Análisis de JSON-RPC** - Analizar y construir mensajes JSON-RPC 2.0 para diferentes operaciones MCP
4. **Comparativa de transportes** - Diseñar la arquitectura de transporte para diferentes escenarios (local, equipo, producción)
5. **Explorar el ecosistema** - Investigar servidores MCP disponibles en mcpservers.org y evaluar uno con los criterios aprendidos

### Práctica Evaluable de la Unidad

Al finalizar ambas sesiones, completa la [práctica evaluable](../practica.md) de la Unidad 6.

---

## Referencias

- Anthropic. *Model Context Protocol - Specification*. https://spec.modelcontextprotocol.io/
- Anthropic. *MCP Documentation*. https://modelcontextprotocol.io/
- GitHub. *MCP Servers (Official)*. https://github.com/modelcontextprotocol/servers
- MCP Servers Directory. https://mcpservers.org/
- Anthropic. *Introducing the Model Context Protocol* (Blog). https://www.anthropic.com/news/model-context-protocol
- JSON-RPC 2.0 Specification. https://www.jsonrpc.org/specification
- Claude Desktop Documentation. https://docs.anthropic.com/en/docs/claude-desktop
- n8n Documentation. *MCP Client Tool Node*. https://docs.n8n.io/
- Repositorio de código del curso. https://github.com/rpmaya/ml2_code/
