# Ejercicios Prácticos - Unidad 6, Sesión 1
## Introducción a MCP y Configuración de Servidores

---

## Ejercicio 1: Análisis de Arquitectura MCP

### Metadata
- **Duración estimada**: 20 minutos
- **Tipo**: Análisis
- **Modalidad**: Individual
- **Dificultad**: Básica
- **Prerequisitos**: Lectura de la sección 6.1 sobre el Model Context Protocol y su arquitectura cliente-servidor

### Contexto
El Model Context Protocol (MCP) propone una arquitectura estandarizada para conectar modelos de lenguaje con fuentes de datos y herramientas externas. Antes de MCP, cada integración requería un conector personalizado (N×M integraciones), lo que generaba un ecosistema fragmentado y difícil de mantener. MCP reduce esta complejidad a un modelo N+M: cada herramienta implementa un servidor MCP y cada cliente se conecta mediante un protocolo universal. Comprender esta arquitectura es el primer paso para diseñar sistemas de IA verdaderamente conectados.

### Objetivo de Aprendizaje
- Identificar los componentes clave de la arquitectura MCP: host, cliente, servidor y LLM
- Comprender el flujo de comunicación entre componentes
- Comparar el enfoque MCP con integraciones acopladas punto a punto
- Desarrollar la capacidad de diseñar arquitecturas MCP para escenarios reales

### Enunciado

Un equipo de producto quiere construir un **asistente de IA para gestión de proyectos** que pueda:
1. Leer y enviar correos electrónicos (Gmail)
2. Consultar y crear eventos en el calendario (Google Calendar)
3. Enviar mensajes y leer canales de Slack
4. Acceder a documentos en Google Drive

### Parte A: Diagrama de Arquitectura MCP (10 min)

Dibuja la arquitectura MCP completa para este escenario. Tu diagrama debe incluir:

| Componente | Qué debes identificar |
|------------|----------------------|
| **Host** | La aplicación que aloja al cliente MCP (ej: Claude Desktop) |
| **Cliente MCP** | El componente dentro del host que gestiona las conexiones |
| **Servidores MCP** | Un servidor por cada integración externa |
| **LLM** | El modelo de lenguaje que toma decisiones |
| **Recursos externos** | Las APIs/servicios finales (Gmail API, Calendar API, etc.) |
| **Flechas de comunicación** | Protocolo usado en cada conexión |

Esquema de referencia para tu diagrama:

```
┌─────────────────────────────────────────────┐
│                    HOST                     │
│  ┌─────────┐                                │
│  │   LLM   │                                │
│  └────┬────┘                                │
│       │                                     │
│  ┌────▼────────────────────────────────┐    │
│  │         CLIENTE MCP                 │    │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌─────┐ │    │
│  │  │Conn 1│ │Conn 2│ │Conn 3│ │ ..  │ │    │
│  └──┴───┬──┴─┴───┬──┴─┴───┬──┴─┴───┬─┘─┘    │
│         │        │        │        │        │
└─────────┼────────┼────────┼────────┼────────┘
          │JSON-RPC│        │        │
     ┌────▼───┐┌───▼────┐┌──▼─────┐┌─▼──────┐
     │Servidor││Servidor││Servidor││Servidor│
     │ Gmail  ││Calendar││ Slack  ││ Drive  │
     └───┬────┘└───┬────┘└──┬─────┘└─┬──────┘
         │         │        │        │
     ┌───▼───┐ ┌───▼────┐┌──▼───┐┌───▼───┐
     │Gmail  │ │Calendar││Slack ││Google │
     │ API   │ │  API   ││ API  ││Drive  │
     └───────┘ └────────┘└──────┘└───────┘
```

Completa los detalles de cada componente en la siguiente tabla:

| Componente | Nombre concreto | Responsabilidad |
|------------|----------------|-----------------|
| Host | __________________ | __________________ |
| LLM | __________________ | __________________ |
| Cliente MCP | __________________ | __________________ |
| Servidor MCP 1 | __________________ | __________________ |
| Servidor MCP 2 | __________________ | __________________ |
| Servidor MCP 3 | __________________ | __________________ |
| Servidor MCP 4 | __________________ | __________________ |

### Parte B: Comparación con Arquitectura Acoplada (10 min)

Ahora imagina que no existiera MCP. Dibuja cómo sería la integración directa (acoplada) donde el LLM necesita conectores específicos para cada servicio.

Responde las siguientes preguntas:

1. **Número de integraciones**: Si tienes 3 clientes de IA diferentes (Claude, ChatGPT, Gemini) y 4 servicios (Gmail, Calendar, Slack, Drive), ¿cuántas integraciones punto a punto necesitas? ¿Y con MCP?

2. **Coste de mantenimiento**: Si Gmail cambia su API, ¿cuántos componentes hay que actualizar en cada modelo?

3. **Escalabilidad**: Si añades un quinto servicio (ej: Notion), ¿cuántas integraciones nuevas requiere cada modelo?

Completa la tabla comparativa:

| Aspecto | Sin MCP (acoplado) | Con MCP |
|---------|-------------------|---------|
| Integraciones necesarias (3 clientes × 4 servicios) | __________________ | __________________ |
| Cambio en API de Gmail afecta a... | __________________ | __________________ |
| Añadir 1 servicio nuevo requiere... | __________________ | __________________ |
| Añadir 1 cliente nuevo requiere... | __________________ | __________________ |
| ¿Quién mantiene la integración? | __________________ | __________________ |


### Extensión (Opcional)
Investiga si existen servidores MCP reales para cada uno de los 4 servicios mencionados. Busca en [mcpservers.org](https://mcpservers.org) o en el [repositorio oficial de Anthropic](https://github.com/modelcontextprotocol/servers). Indica para cada uno: nombre del servidor, autor y si es oficial o comunitario.

---

## Ejercicio 2: Configuración del Servidor Filesystem en Claude Desktop

### Metadata
- **Duración estimada**: 30 minutos
- **Tipo**: Programación
- **Modalidad**: Individual
- **Dificultad**: Intermedia
- **Prerequisitos**: Tener Claude Desktop instalado, Node.js (v18+) instalado, lectura de la sección 6.2 sobre configuración de servidores locales

### Contexto
El servidor Filesystem es uno de los servidores MCP oficiales más utilizados. Permite que Claude acceda al sistema de archivos local para leer, escribir, buscar y organizar archivos. Configurar este servidor es el punto de partida ideal para entender cómo funciona MCP en la práctica: editarás el archivo de configuración JSON de Claude Desktop, arrancarás el servidor mediante STDIO y verificarás que las herramientas aparecen disponibles en la interfaz.

### Objetivo de Aprendizaje
- Localizar y editar el archivo de configuración `claude_desktop_config.json`
- Configurar un servidor MCP basado en STDIO con `npx`
- Comprender los parámetros de configuración: `command`, `args` y `env`
- Verificar que las herramientas del servidor aparecen en Claude Desktop
- Probar operaciones básicas de lectura y escritura de archivos

### Enunciado

### Paso 1: Localizar el Archivo de Configuración (3 min)

El archivo de configuración de Claude Desktop se encuentra en una ubicación específica según tu sistema operativo:

| Sistema Operativo | Ruta del archivo |
|-------------------|-----------------|
| **macOS** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Windows** | `%APPDATA%\Claude\claude_desktop_config.json` |

1. Abre una terminal y verifica que el archivo existe:

**macOS:**
```bash
ls -la ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows (PowerShell):**
```powershell
Test-Path "$env:APPDATA\Claude\claude_desktop_config.json"
```

2. Si el archivo no existe, créalo con un contenido JSON vacío:
```bash
echo '{}' > ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### Paso 2: Configurar el Servidor Filesystem (10 min)

1. Abre el archivo de configuración en tu editor favorito:

```bash
# macOS
code ~/Library/Application\ Support/Claude/claude_desktop_config.json

# O con cualquier editor de texto
open -a TextEdit ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

2. Escribe la siguiente configuración, sustituyendo las rutas por las de tu sistema:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/tu_usuario/Documents",
        "/Users/tu_usuario/Desktop"
      ]
    }
  }
}
```

> **Importante**: Las rutas que pasas como argumentos son los directorios a los que Claude tendrá acceso. Solo podrá leer y escribir dentro de estas carpetas. Esto es un mecanismo de seguridad fundamental.

3. Guarda el archivo.

### Paso 3: Reiniciar Claude Desktop y Verificar (5 min)

1. Cierra completamente Claude Desktop (no solo la ventana, sino la aplicación)
2. Vuelve a abrir Claude Desktop
3. En una nueva conversación, busca el icono de herramientas (martillo/llave) en la parte inferior del campo de texto
4. Haz clic en él: deberías ver las herramientas del servidor filesystem listadas:
   - `read_file` - Leer el contenido de un archivo
   - `write_file` - Escribir contenido en un archivo
   - `list_directory` - Listar el contenido de un directorio
   - `create_directory` - Crear un nuevo directorio
   - `move_file` - Mover o renombrar un archivo
   - `search_files` - Buscar archivos por nombre
   - `read_multiple_files` - Leer varios archivos a la vez
   - `get_file_info` - Obtener metadatos de un archivo
   - `list_allowed_directories` - Ver los directorios permitidos

### Paso 4: Probar Operaciones Básicas (12 min)

Escribe los siguientes prompts en Claude Desktop y verifica que funcionan correctamente:

**Prueba 1 - Listar archivos:**
```
Lista los archivos que hay en mi carpeta Documents
```
Resultado esperado: Claude invocará `list_directory` y mostrará el contenido.

**Prueba 2 - Crear un archivo:**
```
Crea un archivo llamado "prueba_mcp.txt" en mi escritorio con el texto:
"Este archivo fue creado por Claude usando MCP - Filesystem Server"
```
Resultado esperado: Claude invocará `write_file` y confirmará la creación. Verifica manualmente que el archivo existe en tu escritorio.

**Prueba 3 - Leer un archivo:**
```
Lee el contenido del archivo prueba_mcp.txt que acabamos de crear en el escritorio
```
Resultado esperado: Claude invocará `read_file` y mostrará el contenido.

**Prueba 4 - Buscar archivos:**
```
Busca todos los archivos con extensión .pdf en mi carpeta Documents
```
Resultado esperado: Claude invocará `search_files` y listará los PDFs encontrados.

Verificaciones:
- El icono de herramientas muestra 9 herramientas del servidor filesystem
- Las 4 pruebas se ejecutan correctamente, con Claude pidiendo permiso antes de cada operación
- El archivo `prueba_mcp.txt` existe físicamente en el escritorio

**Errores comunes y solución:**

| Error | Causa probable | Solución |
|-------|---------------|----------|
| No aparecen herramientas | JSON mal formado | Validar el JSON en [jsonlint.com](https://jsonlint.com) |
| `npx: command not found` | Node.js no instalado | Instalar Node.js desde [nodejs.org](https://nodejs.org) |
| `Error: Access denied` | Ruta no incluida en args | Añadir la ruta al array de `args` |
| Servidor no arranca | Puerto o proceso bloqueado | Reiniciar Claude Desktop completamente |

### Extensión (Opcional)
Añade variables de entorno al servidor para personalizar su comportamiento. Investiga qué ocurre si añades el campo `"env"` a la configuración:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/tu_usuario/Documents"],
      "env": {
        "NODE_ENV": "development"
      }
    }
  }
}
```
Además, intenta restringir el acceso a una sola subcarpeta y verifica que Claude no puede acceder fuera de ella.

---

## Ejercicio 3: Exploración de Servidores MCP Públicos

### Metadata
- **Duración estimada**: 25 minutos
- **Tipo**: Exploración
- **Modalidad**: Individual
- **Dificultad**: Básica
- **Prerequisitos**: Lectura de la sección 6.3 sobre el ecosistema de servidores MCP y criterios de seguridad

### Contexto
El ecosistema MCP ha crecido rápidamente y ya cuenta con cientos de servidores disponibles, tanto oficiales (mantenidos por Anthropic) como comunitarios. Saber navegar este ecosistema, evaluar la calidad y seguridad de un servidor, y elegir el adecuado para cada caso de uso es una competencia clave. No todos los servidores son iguales: algunos están bien mantenidos y auditados, mientras que otros pueden suponer riesgos de seguridad.

### Objetivo de Aprendizaje
- Navegar los principales directorios de servidores MCP
- Clasificar servidores por categoría funcional
- Aplicar criterios de seguridad para evaluar servidores de terceros
- Desarrollar criterio propio para seleccionar servidores fiables

### Enunciado

### Parte A: Exploración y Clasificación (12 min)

1. Visita los siguientes recursos:
   - [mcpservers.org](https://mcpservers.org) - Directorio comunitario de servidores MCP
   - [github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) - Repositorio oficial de Anthropic
   - [mcp.so](https://mcp.so) - Otro directorio popular

2. Selecciona **10 servidores** y clasifícalos en la siguiente tabla:

| # | Nombre del Servidor | Categoría | Oficial/Comunitario | Descripción breve |
|---|-------------------|-----------|--------------------|--------------------|
| 1 | __________________ | __________________ | __________________ | __________________ |
| 2 | __________________ | __________________ | __________________ | __________________ |
| 3 | __________________ | __________________ | __________________ | __________________ |
| 4 | __________________ | __________________ | __________________ | __________________ |
| 5 | __________________ | __________________ | __________________ | __________________ |
| 6 | __________________ | __________________ | __________________ | __________________ |
| 7 | __________________ | __________________ | __________________ | __________________ |
| 8 | __________________ | __________________ | __________________ | __________________ |
| 9 | __________________ | __________________ | __________________ | __________________ |
| 10 | __________________ | __________________ | __________________ | __________________ |

**Categorías sugeridas** (puedes crear las tuyas):
- Productividad (archivos, notas, calendario)
- Desarrollo (Git, bases de datos, CI/CD)
- Comunicación (email, mensajería, redes sociales)
- Datos (APIs, web scraping, análisis)
- Creatividad (imágenes, diseño, audio)
- Infraestructura (cloud, DevOps, monitorización)

### Parte B: Evaluación de Seguridad (13 min)

Selecciona **3 servidores comunitarios** de tu lista anterior y evalúalos según los siguientes criterios de seguridad. Puntúa cada criterio de 1 (muy bajo) a 5 (excelente):

| Criterio de Seguridad | Servidor 1: _______ | Servidor 2: _______ | Servidor 3: _______ |
|-----------------------|---------------------|---------------------|---------------------|
| **Código abierto** (¿se puede auditar el código?) | ___ | ___ | ___ |
| **Estrellas en GitHub** (popularidad como proxy de confianza) | ___ | ___ | ___ |
| **Frecuencia de actualizaciones** (¿se mantiene activo?) | ___ | ___ | ___ |
| **Documentación** (¿explica qué permisos necesita?) | ___ | ___ | ___ |
| **Principio de mínimo privilegio** (¿pide solo los permisos necesarios?) | ___ | ___ | ___ |
| **Autor/Organización** (¿es una entidad reconocida?) | ___ | ___ | ___ |
| **Issues y respuesta** (¿se atienden reportes de bugs/seguridad?) | ___ | ___ | ___ |
| **Total** | ___ /35 | ___ /35 | ___ /35 |

Para cada servidor evaluado, responde:

1. **¿Lo instalarías en tu equipo de trabajo?** ¿Por qué sí o por qué no?
2. **¿Qué riesgos identificas?** (ej: acceso a datos sensibles, ejecución de código, conexiones externas)
3. **¿Qué medidas de mitigación aplicarías?** (ej: restringir rutas, revisar el código, usar en sandbox)

### Solución Esperada

**Parte A - Ejemplo de clasificación:**

| # | Nombre del Servidor | Categoría | Oficial/Comunitario |
|---|-------------------|-----------|---------------------|
| 1 | filesystem | Productividad | Oficial |
| 2 | github | Desarrollo | Oficial |
| 3 | slack | Comunicación | Oficial |
| 4 | google-drive | Productividad | Oficial |
| 5 | postgresql | Desarrollo | Oficial |
| 6 | brave-search | Datos | Oficial |
| 7 | memory | Productividad | Oficial |
| 8 | puppeteer | Datos | Oficial |
| 9 | sqlite | Desarrollo | Oficial |
| 10 | fetch | Datos | Oficial |

**Parte B - Criterios clave de evaluación:**
- Un servidor con puntuación inferior a 20/35 debería usarse con precaución
- Los servidores oficiales de Anthropic parten con ventaja en autor y mantenimiento
- La presencia de documentación clara sobre permisos es un indicador fuerte de calidad
- Servidores que piden acceso a todo el sistema de archivos o a todas las APIs sin restricción son una señal de alarma

### Extensión (Opcional)
Encuentra un servidor MCP que consideres potencialmente peligroso o con malas prácticas de seguridad. Documenta qué señales de alarma identificas y cómo podría un atacante explotar ese servidor (ej: prompt injection a través de herramientas MCP, exfiltración de datos, ejecución arbitraria de código).

---

## Ejercicio 4: Análisis de Mensajes JSON-RPC en MCP

### Metadata
- **Duración estimada**: 20 minutos
- **Tipo**: Análisis
- **Modalidad**: Individual
- **Dificultad**: Básica
- **Prerequisitos**: Lectura de la sección 6.4 sobre el protocolo JSON-RPC 2.0 y las capas de transporte

### Contexto
MCP utiliza JSON-RPC 2.0 como formato de mensajes para la comunicación entre clientes y servidores. Entender este formato es esencial para depurar problemas, analizar logs y comprender qué sucede "bajo el capó" cuando Claude invoca una herramienta MCP. En este ejercicio analizarás un intercambio real de mensajes entre un cliente y un servidor MCP.

### Objetivo de Aprendizaje
- Identificar los tipos de mensajes JSON-RPC: petición, respuesta y notificación
- Comprender la estructura de cada tipo de mensaje (campos obligatorios y opcionales)
- Trazar el flujo completo de una invocación de herramienta MCP
- Detectar errores en mensajes JSON-RPC malformados

### Enunciado

### Parte A: Identificación de Mensajes (8 min)

A continuación se muestra un intercambio de mensajes entre un cliente MCP y un servidor Filesystem. Para cada mensaje, identifica:
- **Dirección**: ¿Cliente → Servidor o Servidor → Cliente?
- **Tipo**: ¿Petición (request), Respuesta (response) o Notificación (notification)?
- **Propósito**: ¿Qué está haciendo este mensaje?

**Mensaje 1:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "roots": {
        "listChanged": true
      }
    },
    "clientInfo": {
      "name": "Claude Desktop",
      "version": "1.2.0"
    }
  }
}
```

| Campo | Valor |
|-------|-------|
| Dirección | __________________ |
| Tipo | __________________ |
| Propósito | __________________ |

**Mensaje 2:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "tools": {}
    },
    "serverInfo": {
      "name": "filesystem",
      "version": "0.5.0"
    }
  }
}
```

| Campo | Valor |
|-------|-------|
| Dirección | __________________ |
| Tipo | __________________ |
| Propósito | __________________ |

**Mensaje 3:**
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/initialized"
}
```

| Campo | Valor |
|-------|-------|
| Dirección | __________________ |
| Tipo | __________________ |
| Propósito | __________________ |

**Mensaje 4:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list",
  "params": {}
}
```

| Campo | Valor |
|-------|-------|
| Dirección | __________________ |
| Tipo | __________________ |
| Propósito | __________________ |

**Mensaje 5:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "read_file",
        "description": "Read the complete contents of a file",
        "inputSchema": {
          "type": "object",
          "properties": {
            "path": {
              "type": "string",
              "description": "Path to the file to read"
            }
          },
          "required": ["path"]
        }
      },
      {
        "name": "write_file",
        "description": "Write content to a file",
        "inputSchema": {
          "type": "object",
          "properties": {
            "path": { "type": "string" },
            "content": { "type": "string" }
          },
          "required": ["path", "content"]
        }
      }
    ]
  }
}
```

| Campo | Valor |
|-------|-------|
| Dirección | __________________ |
| Tipo | __________________ |
| Propósito | __________________ |

**Mensaje 6:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "read_file",
    "arguments": {
      "path": "/Users/alumno/Documents/notas.txt"
    }
  }
}
```

| Campo | Valor |
|-------|-------|
| Dirección | __________________ |
| Tipo | __________________ |
| Propósito | __________________ |

**Mensaje 7:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Apuntes de la clase de MCP:\n- JSON-RPC 2.0\n- Transporte STDIO\n- Servidores locales"
      }
    ]
  }
}
```

| Campo | Valor |
|-------|-------|
| Dirección | __________________ |
| Tipo | __________________ |
| Propósito | __________________ |

**Mensaje 8:**
```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "tools/call",
  "params": {
    "name": "read_file",
    "arguments": {
      "path": "/etc/shadow"
    }
  }
}
```

| Campo | Valor |
|-------|-------|
| Dirección | __________________ |
| Tipo | __________________ |
| Propósito | __________________ |

**Mensaje 9:**
```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "error": {
    "code": -32602,
    "message": "Access denied: /etc/shadow is not within allowed directories"
  }
}
```

| Campo | Valor |
|-------|-------|
| Dirección | __________________ |
| Tipo | __________________ |
| Propósito | __________________ |

### Parte B: Flujo Completo (7 min)

Ordena los mensajes anteriores en un diagrama de secuencia. Dibuja las flechas indicando la dirección:

```
  CLIENTE                         SERVIDOR
    │                                │
    │──── Mensaje ?: ____________ ──▶│
    │◀─── Mensaje ?: ____________ ───│
    │──── Mensaje ?: ____________ ──▶│
    │──── Mensaje ?: ____________ ──▶│
    │◀─── Mensaje ?: ____________ ───│
    │──── Mensaje ?: ____________ ──▶│
    │◀─── Mensaje ?: ____________ ───│
    │──── Mensaje ?: ____________ ──▶│
    │◀─── Mensaje ?: ____________ ───│
    │                                │
```

### Parte C: Detección de Errores (5 min)

Los siguientes mensajes JSON-RPC contienen errores. Identifica qué está mal en cada uno:

**Mensaje erróneo A:**
```json
{
  "id": 5,
  "method": "tools/call",
  "params": {
    "name": "read_file",
    "arguments": { "path": "/tmp/test.txt" }
  }
}
```

Error: __________________

**Mensaje erróneo B:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "read_file",
    "arguments": { "path": "/tmp/test.txt" }
  }
}
```

Error: __________________

**Mensaje erróneo C:**
```json
{
  "jsonrpc": "2.0",
  "id": 6,
  "result": { "content": "texto" },
  "error": { "code": -32600, "message": "Invalid request" }
}
```

Error: __________________

**Parte C - Errores:**
- **Mensaje A**: Falta el campo `"jsonrpc": "2.0"` (obligatorio en JSON-RPC 2.0)
- **Mensaje B**: Falta el campo `"id"`. Sin `id` sería una notificación, pero `tools/call` es una petición que espera respuesta, por lo que necesita un identificador
- **Mensaje C**: Un mensaje no puede contener simultáneamente `result` y `error`. Debe tener uno u otro, nunca ambos

### Extensión (Opcional)
Escribe tú mismo la secuencia completa de mensajes JSON-RPC que se intercambiarían si Claude invocara la herramienta `write_file` para crear un archivo nuevo. Incluye: petición del cliente, respuesta exitosa del servidor, y cómo sería la respuesta si el disco estuviera lleno (código de error `-32603` para error interno).

---

## Ejercicio 5: Configuración Multi-Servidor en Claude Desktop

### Metadata
- **Duración estimada**: 35 minutos
- **Tipo**: Programación
- **Modalidad**: Individual
- **Dificultad**: Intermedia
- **Prerequisitos**: Haber completado el Ejercicio 2, lectura de las secciones 6.2 y 6.5 sobre configuración de servidores y transporte STDIO

### Contexto
El verdadero poder de MCP se manifiesta cuando un mismo cliente conecta con múltiples servidores simultáneamente. En este escenario, Claude Desktop actúa como host que mantiene múltiples conexiones 1:1, y el LLM puede combinar herramientas de distintos servidores para resolver tareas complejas. Por ejemplo, puede leer un archivo (servidor filesystem), guardar información relevante (servidor memory) y buscar contexto adicional en la web (servidor brave-search), todo dentro de la misma conversación.

### Objetivo de Aprendizaje
- Configurar múltiples servidores MCP en un solo archivo de configuración
- Comprender que cada servidor se ejecuta como un proceso independiente
- Verificar que Claude puede combinar herramientas de distintos servidores
- Documentar una configuración completa y funcional

### Enunciado

### Paso 1: Planificación de Servidores (5 min)

Vas a configurar Claude Desktop con **tres servidores MCP** que trabajarán en conjunto:

| Servidor | Paquete npm | Función |
|----------|-------------|---------|
| **Filesystem** | `@modelcontextprotocol/server-filesystem` | Acceso al sistema de archivos local |
| **Memory** | `@modelcontextprotocol/server-memory` | Grafo de conocimiento persistente (entidades y relaciones) |
| **Brave Search** | `@modelcontextprotocol/server-brave-search` | Búsqueda en internet vía API de Brave |

> **Nota**: Para Brave Search necesitarás una API key gratuita. Si no la tienes, puedes sustituirlo por otro servidor como `@modelcontextprotocol/server-fetch` (que obtiene contenido de URLs) y no requiere API key.

### Paso 2: Escribir la Configuración JSON (15 min)

Edita tu archivo `claude_desktop_config.json` para incluir los tres servidores. Utiliza la siguiente plantilla y complétala con tus rutas y credenciales:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/tu_usuario/Documents/mcp_workspace"
      ]
    },
    "memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ]
    },
    "brave-search": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-brave-search"
      ],
      "env": {
        "BRAVE_API_KEY": "TU_API_KEY_AQUI"
      }
    }
  }
}
```

**Alternativa sin API key** (sustituye `brave-search` por `fetch`):

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/tu_usuario/Documents/mcp_workspace"
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

Antes de guardar, verifica que tu JSON es válido:
1. Asegúrate de que no hay comas finales después del último elemento
2. Todas las llaves y corchetes están correctamente cerrados
3. Las cadenas de texto usan comillas dobles

### Paso 3: Crear el Directorio de Trabajo (2 min)

Crea un directorio dedicado para este ejercicio:

```bash
mkdir -p ~/Documents/mcp_workspace
echo "Archivo de prueba para MCP" > ~/Documents/mcp_workspace/readme.txt
```

### Paso 4: Reiniciar y Verificar (5 min)

1. Reinicia Claude Desktop completamente
2. Abre una nueva conversación
3. Haz clic en el icono de herramientas: deberías ver herramientas de los **tres servidores**
4. Verifica contando las herramientas disponibles:

| Servidor | Herramientas esperadas |
|----------|----------------------|
| Filesystem | `read_file`, `write_file`, `list_directory`, `create_directory`, `move_file`, `search_files`, `read_multiple_files`, `get_file_info`, `list_allowed_directories` |
| Memory | `create_entities`, `create_relations`, `add_observations`, `delete_entities`, `delete_observations`, `delete_relations`, `read_graph`, `search_nodes`, `open_nodes` |
| Brave Search / Fetch | `brave_web_search`, `brave_local_search` / `fetch` |

### Paso 5: Prueba de Integración Multi-Servidor (8 min)

Ejecuta el siguiente flujo de trabajo que combina herramientas de los tres servidores:

**Prompt 1** (Filesystem + Memory):
```
Lee el archivo readme.txt de mi carpeta mcp_workspace.
Luego, guarda en tu memoria que existe un proyecto llamado
"Ejercicio MCP" con la descripción que encontraste en el archivo.
```

Resultado esperado: Claude usará `read_file` (filesystem) y luego `create_entities` (memory).

**Prompt 2** (Brave Search / Fetch + Memory):
```
Busca en internet qué es el Model Context Protocol.
Guarda en tu memoria las 3 ideas principales que encuentres
como observaciones de una entidad llamada "MCP".
```

Resultado esperado: Claude usará `brave_web_search` o `fetch` y luego `create_entities` + `add_observations` (memory).

**Prompt 3** (Memory + Filesystem):
```
Recupera todo lo que tienes guardado en tu memoria sobre MCP.
Genera un resumen y guárdalo como un archivo "resumen_mcp.md"
en la carpeta mcp_workspace.
```

Resultado esperado: Claude usará `read_graph` (memory) y luego `write_file` (filesystem).

**Prompt 4** (Verificación):
```
Lee el archivo resumen_mcp.md que acabamos de crear.
```

## Resumen de Ejercicios

| Ejercicio | Duración | Tipo | Dificultad | Tema principal |
|-----------|----------|------|------------|----------------|
| 1. Análisis de Arquitectura MCP | 20 min | Análisis | Básica | Componentes y flujo N+M vs N×M |
| 2. Configuración Servidor Filesystem | 30 min | Programación | Intermedia | Primer servidor MCP en Claude Desktop |
| 3. Exploración de Servidores Públicos | 25 min | Exploración | Básica | Ecosistema y evaluación de seguridad |
| 4. Análisis de JSON-RPC | 20 min | Análisis | Básica | Protocolo de comunicación MCP |
| 5. Configuración Multi-Servidor | 35 min | Programación | Intermedia | Múltiples servidores trabajando juntos |
| **Total** | **130 min** | | | |
