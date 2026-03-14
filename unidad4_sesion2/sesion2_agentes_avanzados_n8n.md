# Unidad 4 - Sesión 2: IA en n8n y Agentes Avanzados

## Objetivos de la Sesión

Al finalizar esta sesión, el estudiante será capaz de:
- Comprender las categorías de nodos de IA disponibles en n8n y sus funcionalidades
- Integrar proveedores de LLMs (OpenAI, Gemini, Claude, Ollama) en workflows de n8n
- Construir agentes de IA completos con herramientas, memoria y system prompts estructurados
- Implementar memoria persistente y por sesión en agentes conversacionales
- Desplegar agentes en canales de comunicación reales: chat embebido, Telegram y webhooks
- Diseñar system prompts efectivos para agentes con estructura Rol-Tareas-Restricciones-Formato

---

## Bloque 1: Inteligencia Artificial en n8n (40 minutos)

### 1.1 Nodos de IA en n8n: Categorías y Funcionalidades

n8n incorpora un ecosistema completo de nodos de IA que permiten construir workflows inteligentes sin necesidad de programar. Estos nodos se organizan en categorías funcionales.

```
┌──────────────────────────────────────────────────────────────────┐
│              ECOSISTEMA DE NODOS DE IA EN n8n                    │
│                                                                  │
│  ┌─────────────────┐   ┌─────────────────┐  ┌──────────────────┐ │
│  │  Chat Models    │   │  Embeddings     │  │  Vector Stores   │ │
│  │  ─────────────  │   │  ─────────────  │  │  ──────────────  │ │
│  │  OpenAI         │   │  OpenAI         │  │  Pinecone        │ │
│  │  Anthropic      │   │  Google Gemini  │  │  Supabase        │ │
│  │  Google Gemini  │   │  Cohere         │  │  Qdrant          │ │
│  │  Ollama         │   │  Ollama         │  │  In-Memory       │ │
│  └─────────────────┘   └─────────────────┘  └──────────────────┘ │
│                                                                  │
│  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐ │
│  │  Document       │  │  Text            │  │  AI Agent        │ │
│  │  Loaders        │  │  Splitters       │  │  ──────────────  │ │
│  │  ─────────────  │  │  ─────────────   │  │  Agent node      │ │
│  │  PDF            │  │  Recursive       │  │  Tools           │ │
│  │  CSV            │  │  Character       │  │  Memory          │ │
│  │  Google Drive   │  │  Token           │  │  Output Parser   │ │
│  │  Notion         │  │  Markdown        │  │                  │ │
│  └─────────────────┘  └──────────────────┘  └──────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

#### Descripción de Cada Categoría

| Categoría | Función | Nodos Principales | Caso de Uso Típico |
|-----------|---------|-------------------|---------------------|
| **Chat Models** | Conectar con LLMs para generación de texto | OpenAI, Anthropic, Gemini, Ollama | Chatbots, generación de contenido |
| **Embeddings** | Vectorización de texto (texto a vectores numéricos) | OpenAI Embeddings, Google Embeddings | Búsqueda semántica, RAG |
| **Vector Stores** | Almacenamiento y búsqueda vectorial | Pinecone, Supabase, Qdrant, In-Memory | Base de conocimiento vectorial |
| **Document Loaders** | Carga de documentos de distintas fuentes | PDF, CSV, Google Drive, Notion | Ingestión de documentos para RAG |
| **Text Splitters** | División de textos largos en fragmentos | Recursive, Character, Token, Markdown | Preparación de documentos para vectorización |

> **Conexión con la Unidad 5**: Los nodos de Embeddings, Vector Stores, Document Loaders y Text Splitters son la base de RAG (Retrieval-Augmented Generation), que estudiaremos en profundidad en la Unidad 5.

### 1.2 Integración con Proveedores de LLMs

n8n soporta múltiples proveedores de LLMs a través de nodos específicos. Cada proveedor se configura como un subnodo del Chat Model que se conecta al nodo principal (AI Agent, Basic LLM Chain, etc.).

#### OpenAI Chat Model

El nodo más utilizado. Permite conectar con los modelos de OpenAI.

```
┌─────────────────────────────────────────────┐
│         OPENAI CHAT MODEL NODE              │
├─────────────────────────────────────────────┤
│                                             │
│  Model:        gpt-4o / gpt-4o-mini         │
│  Temperature:  0.0 - 2.0 (default: 0.7)     │
│  Max Tokens:   Límite de tokens de salida   │
│  Top P:        Nucleus sampling             │
│                                             │
│  Credenciales: OpenAI API Key               │
│  Conexión:     Se conecta como subnodo      │
│                del AI Agent o Chain         │
└─────────────────────────────────────────────┘
```

#### Comparativa de Proveedores en n8n

| Proveedor | Nodo en n8n | Modelos Disponibles | Ventaja Principal |
|-----------|-------------|---------------------|-------------------|
| **OpenAI** | OpenAI Chat Model | gpt-4o, gpt-4o-mini | Mayor ecosistema, más herramientas compatibles |
| **Google** | Google Gemini Chat Model | gemini-1.5-pro, gemini-1.5-flash | Contexto de 1M tokens, buen rendimiento |
| **Anthropic** | Anthropic Chat Model | claude-3-sonnet, claude-3-haiku | Excelente seguimiento de instrucciones |
| **Ollama** | Ollama Chat Model | llama3, mistral, codellama | Gratuito, privacidad total, sin API Key |
| **OpenRouter** | OpenAI Chat Model (URL personalizada) | 200+ modelos: Claude, Gemini, Llama, Mistral... | Acceso unificado a todos los proveedores con una sola API Key |

#### OpenRouter: Acceso Unificado a Múltiples Modelos

OpenRouter actúa como proxy unificado que expone una API compatible con OpenAI, permitiendo acceder a más de 200 modelos de distintos proveedores con una sola cuenta y API Key.

```
┌──────────────────────────────────────────────────────────────┐
│              OPENROUTER EN n8n                               │
│                                                              │
│  Configuración del nodo OpenAI Chat Model:                   │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  Base URL:  https://openrouter.ai/api/v1             │    │
│  │  API Key:   sk-or-v1-xxxxxxxxxxxxx                   │    │
│  │  Model:     anthropic/claude-3.5-sonnet              │    │
│  │             google/gemini-2.0-flash                  │    │
│  │             meta-llama/llama-3.3-70b-instruct        │    │
│  │             mistralai/mistral-large                  │    │
   │             arcee-ai/trinity-large-preview:free      │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                              │
│  Ventajas:                                                   │
│  - Una sola API Key para todos los modelos                   │
│  - Comparar modelos fácilmente cambiando solo el nombre      │
│  - Acceso a modelos gratuitos (muchos disponibles en free)   │
│  - Fallback automático si un modelo no está disponible       │
│                                                              │
│  Cómo obtener la API Key:                                    │
│  https://openrouter.ai/keys                                  │
└──────────────────────────────────────────────────────────────┘
```

> **Truco**: OpenRouter es especialmente útil en clase para probar distintos modelos sin necesidad de crear cuentas en cada proveedor.

#### Modelos Locales con Ollama

Ollama permite ejecutar LLMs en el propio servidor, sin enviar datos a terceros.

```
┌──────────────────────────────────────────────────────────────┐
│              MODELOS LOCALES CON OLLAMA                      │
│                                                              │
│  Instalación:  curl -fsSL https://ollama.ai/install.sh | sh  │
│                http://ollama.com/download/windows  (Windows) │    
│  Ejecutar:     ollama run llama3                             │
│                                                              │
│  En n8n:                                                     │
│  ┌──────────────┐     ┌───────────────────┐                  │
│  │  Ollama Chat │────►│  http://localhost │                  │
│  │  Model Node  │     │  :11434           │                  │
│  └──────────────┘     └───────────────────┘                  │
│                                                              │
│  Ventajas:                                                   │
│  - Sin coste por token                                       │
│  - Datos nunca salen de tu servidor                          │
│  - Ideal para pruebas y desarrollo                           │
│                                                              │
│  Limitaciones:                                               │
│  - Requiere GPU para buen rendimiento                        │
│  - Modelos más pequeños que los comerciales                  │
└──────────────────────────────────────────────────────────────┘
```

### 1.3 Configuración de Credenciales de IA

Para conectar n8n con proveedores de LLMs, es necesario configurar las credenciales de cada proveedor. El proceso sigue un patrón común.

#### Paso a Paso: Configurar API Key de OpenAI

```
CONFIGURACIÓN DE CREDENCIALES EN n8n:

1. Obtener la API Key
   ┌──────────────────────────────────────┐
   │ https://platform.openai.com/api-keys │
   │ → Create new secret key              │
   │ → Copiar: sk-proj-xxxxxxxxxxxxx      │
   └──────────────────────────────────────┘

2. Crear credencial en n8n
   ┌────────────────────────────────────┐
   │ Settings → Credentials → Add New   │
   │ → Buscar "OpenAI"                  │
   │ → Credential type: OpenAI API      │
   └────────────────────────────────────┘

3. Configurar la credencial
   ┌────────────────────────────────────┐
   │ API Key: sk-proj-xxxxxxxxxxxxx     │
   │ → Save                             │
   │ → Test: Connection successful!     │
   └────────────────────────────────────┘

4. Usar en un nodo
   ┌────────────────────────────────────┐
   │ Nodo OpenAI Chat Model             │
   │ → Credential: "Mi OpenAI API"      │
   │ → Model: gpt-4o-mini               │
   └────────────────────────────────────┘
```

#### Credenciales por Proveedor

| Proveedor | Tipo de Credencial | Dónde Obtenerla | Nombre en n8n |
|-----------|-------------------|-----------------|---------------|
| OpenAI | API Key | platform.openai.com/api-keys | OpenAI API |
| Google Gemini | API Key | aistudio.google.com/apikey | Google AI |
| Anthropic | API Key | console.anthropic.com/settings/keys | Anthropic API |
| Ollama | Sin credencial | Local (localhost:11434) | Ollama API |
| OpenRouter | API Key + Base URL | openrouter.ai/keys | OpenAI API (con Base URL personalizada) |

> **Nota de seguridad**: Las credenciales se almacenan cifradas en la base de datos de n8n. Nunca se exponen en los workflows exportados.

### 1.4 Primer Workflow con IA: Chat Básico

El workflow más sencillo con IA en n8n conecta un Chat Trigger con un modelo de lenguaje.

```
WORKFLOW: CHAT BÁSICO CON IA

┌───────────────┐     ┌──────────────────┐     ┌──────────────┐
│  Chat         │────►│  Basic LLM       │────►│  Respuesta   │
│  Trigger      │     │  Chain           │     │  al usuario  │
│               │     │                  │     │              │
│  (Interfaz    │     │  ┌────────────┐  │     │              │
│   de chat)    │     │  │ OpenAI     │  │     │              │
│               │     │  │ Chat Model │  │     │              │
│               │     │  │ (subnodo)  │  │     │              │
│               │     │  └────────────┘  │     │              │
└───────────────┘     └──────────────────┘     └──────────────┘
```

#### Configuración Paso a Paso

1. **Chat Trigger**: Nodo inicial que proporciona una interfaz de chat dentro de n8n
   - No requiere configuración adicional
   - Genera la variable `{{ $json.chatInput }}` con el mensaje del usuario

2. **Basic LLM Chain**: Nodo que procesa el mensaje con un modelo de IA
   - Prompt: `{{ $json.chatInput }}`
   - Subnodo: OpenAI Chat Model (gpt-4o-mini)

3. **Parámetros del modelo**:

| Parámetro | Valor Recomendado | Descripción |
|-----------|-------------------|-------------|
| Model | gpt-4o-mini | Económico y rápido para chat |
| Temperature | 0.7 | Balance entre creatividad y coherencia |
| Max Tokens | 1000 | Longitud máxima de respuesta |

> **Importante**: Este workflow básico NO tiene memoria. Cada mensaje se procesa de forma independiente. En los siguientes bloques aprenderemos a añadir memoria al agente.

---

## Bloque 2: Construcción de Agentes de IA en n8n (50 minutos)

### 2.1 El Nodo AI Agent: Anatomía y Configuración

El nodo **AI Agent** es el componente central para construir agentes inteligentes en n8n. A diferencia del Basic LLM Chain, el AI Agent puede usar herramientas, mantener memoria y tomar decisiones autónomas.

```
┌─────────────────────────────────────────────────────────────┐
│                  ANATOMÍA DEL NODO AI AGENT                 │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                    AI AGENT                           │  │
│  │                                                       │  │
│  │   ┌─────────────────┐  ┌───────────────────────────┐  │  │
│  │   │  Chat Model     │  │  System Prompt (Options)  │  │  │
│  │   │  (obligatorio)  │  │  (Rol + Tareas +          │  │  │
│  │   │  OpenAI/Gemini/ │  │   Restricciones + Formato)│  │  │
│  │   │  Claude/Ollama  │  │                           │  │  │
│  │   └─────────────────┘  └───────────────────────────┘  │  │
│  │                                                       │  │
│  │   ┌─────────────────┐  ┌──────────────────────────┐   │  │
│  │   │  Memory         │  │  Tools                   │   │  │
│  │   │  (opcional)     │  │  (opcionales)            │   │  │
│  │   │  Window Buffer  │  │  Wikipedia, Calculator,  │   │  │
│  │   │  PostgreSQL     │  │  Google Sheets, Custom...│   │  │
│  │   │  Redis          │  │                          │   │  │
│  │   └─────────────────┘  └──────────────────────────┘   │  │
│  │                                                       │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  Entrada:  {{ $json.chatInput }} del Chat Trigger           │
│  Salida:   Respuesta generada por el agente                 │
└─────────────────────────────────────────────────────────────┘
```

#### Componentes del AI Agent

| Componente | Obligatorio | Función | Subnodos Típicos |
|------------|-------------|---------|-------------------|
| **Chat Model** | Sí | Motor de razonamiento del agente | OpenAI, Gemini, Claude, Ollama |
| **System Prompt** | Recomendado | Define el comportamiento del agente | Texto configurado en el nodo |
| **Memory** | Opcional | Mantiene contexto entre mensajes | Window Buffer, PostgreSQL, Redis |
| **Tools** | Opcional | Herramientas que el agente puede invocar | Wikipedia, Calculator, HTTP Request |

#### Configuración del System Prompt

El nodo AI Agent permite configurar el prompt de sistema de dos formas en "Options - System Message:

| Opción | Cuándo Usarla | Ejemplo |
|--------|---------------|---------|
| **Fixed** | Prompt estático, siempre igual | "Eres un asistente de soporte técnico" |
| **Expression** | Prompt dinámico, depende del contexto | `{{ $json.promptPersonalizado }}` |

### 2.2 Herramientas (Tools) para Agentes

Las herramientas son la clave que diferencia a un agente de un simple chatbot. Permiten que el LLM interactúe con el mundo exterior: buscar información, hacer cálculos, leer/escribir datos, enviar correos, etc.

> **Conexión con la Unidad 3**: Las herramientas de los agentes se basan en el concepto de **Function Calling** que estudiamos en la Unidad 3 (Sección 4.4). El modelo decide cuándo y con qué argumentos invocar cada herramienta.

#### Herramientas Nativas de n8n

```
┌─────────────────────────────────────────────────────────────┐
│              HERRAMIENTAS NATIVAS DEL AI AGENT              │
│                                                             │
│  Información:        Productividad:        Comunicación:    │
│  ┌────────────────┐  ┌────────────────┐  ┌───────────────┐  │
│  │ Wikipedia      │  │ Google Sheets  │  │ Gmail         │  │
│  │ WolframAlpha   │  │ Google Calendar│  │ Slack         │  │
│  │ SerpAPI        │  │ Notion         │  │ Telegram      │  │
│  └────────────────┘  └────────────────┘  └───────────────┘  │
│                                                             │
│  Utilidades:         Código:              Datos:            │
│  ┌────────────────┐  ┌────────────────┐  ┌───────────────┐  │
│  │ Calculator     │  │ Code Tool      │  │ HTTP Request  │  │
│  │ Date/Time      │  │ Execute        │  │ Database      │  │
│  │ Text Formatter │  │ Workflow       │  │ Vector Store  │  │
│  └────────────────┘  └────────────────┘  └───────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

| Herramienta | Descripción | Ejemplo de Uso |
|-------------|-------------|----------------|
| **Wikipedia** | Busca información en Wikipedia | "¿Quién fue Alan Turing?" |
| **Calculator** | Realiza cálculos matemáticos | "¿Cuánto es 15% de 2300?" |
| **Google Sheets** | Lee y escribe en hojas de cálculo | "Añade este registro a la hoja de ventas" |
| **Gmail** | Envía y lee correos electrónicos | "Envía un resumen por email" |
| **HTTP Request** | Llama a APIs externas | "Consulta el estado del pedido #1234" |
| **Code Tool** | Ejecuta código JavaScript/Python | Lógica personalizada compleja |

#### Custom Tools con $fromAI()

La función `$fromAI()` permite que el agente genere dinámicamente los parámetros de una herramienta. Es la forma en que n8n implementa el paso de argumentos de Function Calling.

```
FLUJO DE $fromAI():

1. El usuario pregunta: "Busca el precio del iPhone 17 en Google Shopping"

2. El AI Agent decide usar la herramienta HTTP Request

3. $fromAI() genera los parámetros:
   ┌──────────────────────────────────────────────────────┐
   │  HTTP Request Tool                                   │
   │                                                      │
   │  URL: https://serpapi.com/search                     │
   │  Parámetros:                                         │
   │    engine: google_shopping                           │
   │    q: "Defined automatically by the model"           │
   │    api_key: <tu_api_key_de_serpapi>                  │
   │                                                      │
   │  → El agente rellena q: "iPhone 17 precio"           │
   └──────────────────────────────────────────────────────┘

4. n8n ejecuta la petición HTTP con el parámetro generado

5. El resultado se envía de vuelta al agente para la respuesta final
```

> **Nota**: SerpAPI es una API real que permite hacer búsquedas en Google (incluyendo Google Shopping) y devuelve resultados estructurados en JSON. Ofrece 100 búsquedas gratuitas al mes. Obtén tu API Key en [serpapi.com](https://serpapi.com).


### 2.3 System Prompts Efectivos para Agentes en n8n

Un buen system prompt es determinante para el comportamiento del agente. La estructura recomendada sigue el patrón **RTRF**: Rol, Tareas, Restricciones, Formato.

#### Estructura Recomendada

```
┌───────────────────────────────────────────────────────────────┐
│           ESTRUCTURA DE SYSTEM PROMPT PARA AGENTES            │
│                                                               │
│  1. ROL                                                       │
│     "Eres un asistente especializado en atención al cliente   │
│      de una tienda de electrónica online."                    │
│                                                               │
│  2. TAREAS                                                    │
│     "Tu función es:                                           │
│      - Responder consultas sobre productos y precios          │
│      - Gestionar reclamaciones y devoluciones                 │
│      - Derivar casos complejos al equipo humano"              │
│                                                               │
│  3. RESTRICCIONES                                             │
│     "Reglas que SIEMPRE debes cumplir:                        │
│      - Nunca inventes información sobre stock o precios       │
│      - Si no tienes la información, usa la herramienta        │
│      - No compartas datos internos de la empresa              │
│      - Responde siempre en español"                           │
│                                                               │
│  4. FORMATO                                                   │
│     "Formato de respuesta:                                    │
│      - Saluda al cliente por su nombre si lo conoces          │
│      - Respuestas concisas (máximo 3 párrafos)                │
│      - Si consultas una herramienta, indica lo que hiciste"   │
│                                                               │
│  5. HERRAMIENTAS (opcional)                                   │
│     "Tienes disponibles las siguientes herramientas:          │
│      - Wikipedia: para buscar información general             │
│      - Calculator: para cálculos de precios y descuentos"     │
└───────────────────────────────────────────────────────────────┘
```

#### Ejemplo Completo de System Prompt (Options / System Message)

```
Eres un asistente virtual de soporte técnico para la empresa TechStore.

## Tareas
- Responder preguntas sobre productos de electrónica
- Ayudar a resolver problemas técnicos básicos
- Calcular precios con descuentos cuando el cliente lo solicite
- Buscar información adicional en Wikipedia si es necesario

## Restricciones
- Responde SIEMPRE en español
- Si no conoces la respuesta, busca en Wikipedia antes de decir que no sabes
- NUNCA inventes especificaciones técnicas
- Si el problema requiere asistencia presencial, indica al cliente que contacte
  con soporte avanzado en el teléfono 900-123-456

## Formato de Respuesta
- Máximo 3 párrafos por respuesta
- Usa listas para comparativas de productos
- Incluye el cálculo detallado cuando uses la calculadora

## Herramientas Disponibles
- Wikipedia: Buscar información sobre productos y tecnologías
- Calculator: Realizar cálculos de precios, descuentos e IVA
```

#### Uso de Variables en System Prompts

n8n permite insertar variables dinámicas en los system prompts usando la sintaxis de expresiones:

| Variable | Descripción | Ejemplo de Uso |
|----------|-------------|----------------|
| `{{ $json.chatInput }}` | Mensaje actual del usuario | Prompt dinámico |
| `{{ $now.toISO() }}` | Fecha y hora actual | "Hoy es {{ $now.toISO() }}" |
| `{{ $vars.nombreEmpresa }}` | Variable de entorno de n8n | "Eres el asistente de {{ $vars.nombreEmpresa }}" |
| `{{ $execution.id }}` | ID de la ejecución actual | Logging y trazabilidad |

### 2.4 Ejemplo Completo: Agente Q&A con Herramientas

Construyamos paso a paso un agente que puede buscar información y hacer cálculos.

```
WORKFLOW: AGENTE Q&A CON HERRAMIENTAS

┌───────────────┐     ┌──────────────────────────────────────┐
│  Chat         │────►│  AI Agent                            │
│  Trigger      │     │                                      │
│               │     │  System Prompt:                      │
│               │     │  "Eres un asistente de investigación │
│               │     │   que busca en Wikipedia y calcula"  │
│               │     │                                      │
│               │     │  ┌────────────┐  ┌────────────────┐  │
│               │     │  │ OpenRouter │  │ Window Buffer  │  │
│               │     │  │ Chat Model │  │ Memory (10)    │  │
│               │     │  │ trinity    │  │                │  │
│               │     │  └────────────┘  └────────────────┘  │
│               │     │                                      │
│               │     │  ┌────────────┐  ┌────────────────┐  │
│               │     │  │ Wikipedia  │  │ Calculator     │  │
│               │     │  │ Tool       │  │ Tool           │  │
│               │     │  └────────────┘  └────────────────┘  │
└───────────────┘     └──────────────────────────────────────┘
```

#### Paso a Paso de Construcción

| Paso | Acción | Detalle |
|------|--------|---------|
| 1 | Crear nuevo workflow | Nombre: "Agente Q&A" |
| 2 | Añadir **Chat Trigger** | Arrastrarlo al canvas |
| 3 | Añadir **AI Agent** | Conectar salida del Chat Trigger a la entrada del AI Agent |
| 4 | Configurar **System Prompt** | Add Optin: "System Message". Escribir el prompt con estructura RTRF |
| 5 | Añadir **OpenAI Chat Model** | Subnodo del AI Agent. Seleccionar gpt-4o-mini. Configurar credenciales |
| 6 | Añadir **Wikipedia** | Subnodo Tool del AI Agent. Sin configuración adicional |
| 7 | Añadir **Calculator** | Subnodo Tool del AI Agent. Sin configuración adicional |
| 8 | Activar y probar | Clic en "Chat" para abrir la interfaz de prueba |

#### Pruebas del Agente

```
Prueba 1: Información
Usuario: "¿Quién inventó la World Wide Web?"
Agente: [Usa Wikipedia] → "Tim Berners-Lee inventó la World Wide Web en 1989..."

Prueba 2: Cálculo
Usuario: "Si un producto cuesta 150€ y tiene 21% de IVA, ¿cuál es el precio final?"
Agente: [Usa Calculator] → "El precio final es 150 × 1.21 = 181.50€"

Prueba 3: Combinación
Usuario: "¿Cuál es la población de Japón y cuánto es el 10% de esa cifra?"
Agente: [Usa Wikipedia + Calculator] → "Japón tiene ~125 millones...
         El 10% es 12.5 millones"
```

---

## Bloque 3: Memoria en Agentes de IA (45 minutos)

### 3.1 ¿Por Qué Necesitan Memoria los Agentes?

Los LLMs son **stateless** por naturaleza: cada llamada a la API es independiente. El modelo no recuerda nada de conversaciones anteriores. La memoria es el mecanismo que permite a los agentes mantener contexto entre turnos de conversación.

```
┌──────────────────────────────────────────────────────────────┐
│              PROBLEMA: LLMs SON STATELESS                    │
│                                                              │
│  Sin memoria:                                                │
│  ┌─────────────────────────────────────────────────┐         │
│  │ Usuario: "Me llamo Carlos"                      │         │
│  │ Agente:  "¡Hola Carlos! ¿En qué puedo ayudarte?"│         │
│  │                                                 │         │
│  │ Usuario: "¿Cómo me llamo?"                      │         │
│  │ Agente:  "No tengo esa información."   ← ERROR  │         │
│  └─────────────────────────────────────────────────┘         │
│                                                              │
│  Con memoria:                                                │
│  ┌─────────────────────────────────────────────────┐         │
│  │ Usuario: "Me llamo Carlos"                      │         │
│  │ Agente:  "¡Hola Carlos! ¿En qué puedo ayudarte?"│         │
│  │ [Memoria guarda: user="Me llamo Carlos",        │         │
│  │  assistant="¡Hola Carlos!..."]                  │         │
│  │                                                 │         │
│  │ Usuario: "¿Cómo me llamo?"                      │         │
│  │ [Memoria inyecta historial en el prompt]        │         │
│  │ Agente:  "Te llamas Carlos."           ← OK     │         │
│  └─────────────────────────────────────────────────┘         │
└──────────────────────────────────────────────────────────────┘
```

#### Tipos de Memoria

| Tipo | Duración | Almacenamiento | Caso de Uso |
|------|----------|----------------|-------------|
| **Corto plazo** | Durante la sesión | RAM / Buffer temporal | Conversación activa |
| **Largo plazo** | Persistente | Base de datos | Recordar usuario entre sesiones |

### 3.2 Window Buffer Memory

La **Window Buffer Memory** es el tipo de memoria más común en n8n. Almacena los últimos N turnos de conversación en un buffer temporal.

```
┌───────────────────────────────────────────────────────────────┐
│              WINDOW BUFFER MEMORY                             │
│                                                               │
│  Context Window Length = 5 (guarda 5 pares user/assistant)    │
│                                                               │
│  Buffer:                                                      │
│  ┌───────────────────────────────────────────────────┐        │
│  │ [1] User: "Hola, me llamo Ana"                    │        │
│  │     Assistant: "¡Hola Ana!"                       │        │
│  │ [2] User: "Quiero saber sobre Python"             │        │
│  │     Assistant: "Python es un lenguaje..."         │        │
│  │ [3] User: "¿Y sus bibliotecas de datos?"          │        │
│  │     Assistant: "Las principales son pandas..."    │        │
│  │ [4] User: "¿Cómo instalo pandas?"                 │        │
│  │     Assistant: "Ejecuta: pip install pandas"      │        │
│  │ [5] User: "¿Cómo me llamo?"    ← ¡Todavía         │        │
│  │     Assistant: "Te llamas Ana"     en el buffer!  │        │
│  └───────────────────────────────────────────────────┘        │
│                                                               │
│  Si llega el turno [6], se elimina el turno [1]               │
│  (ventana deslizante)                                         │
└───────────────────────────────────────────────────────────────┘
```

#### Configuración en n8n

| Parámetro | Descripción | Valor Recomendado |
|-----------|-------------|-------------------|
| **Context Window Length** | Número de turnos que se guardan | 5-10 (según complejidad) |
| **Session ID** | Identificador de la sesión | Automático o personalizado |

#### Pasos para Añadir Window Buffer Memory

1. En el nodo AI Agent, hacer clic en el conector **Memory**
2. Seleccionar **Window Buffer Memory**
3. Configurar **Context Window Length** (por ejemplo, 10)
4. No requiere credenciales adicionales (se almacena en RAM de n8n)

#### Prueba de Memoria

```
Secuencia de prueba para verificar que la memoria funciona:

Mensaje 1: "Hola, me llamo Roberto y trabajo en Google"
→ Respuesta: "¡Hola Roberto! ¿En qué puedo ayudarte?"

Mensaje 2: "¿Dónde trabajo?"
→ Respuesta: "Trabajas en Google."  ← Funciona: recuerda el contexto

Mensaje 3: "¿Cómo me llamo?"
→ Respuesta: "Te llamas Roberto."  ← Funciona: recuerda el nombre
```

> **Limitación**: La Window Buffer Memory se pierde al reiniciar n8n o al reiniciar el workflow. Para memoria persistente, necesitamos una base de datos.

### 3.3 Memoria Persistente

Para mantener el historial de conversaciones entre reinicios del servidor, n8n ofrece opciones de memoria persistente que almacenan los datos en bases de datos externas.

#### Opciones de Memoria Persistente

```
┌──────────────────────────────────────────────────────────────┐
│           OPCIONES DE MEMORIA PERSISTENTE EN n8n             │
│                                                              │
│  ┌────────────────────┐  ┌──────────────────────┐            │
│  │  PostgreSQL        │  │  Supabase            │            │
│  │  Chat Memory       │  │  Chat Memory         │            │
│  │  ──────────────────│  │  ──────────────────  │            │
│  │  Base de datos SQL │  │  PostgreSQL en la    │            │
│  │  Auto-hosted       │  │  nube (gratuito)     │            │
│  │  Mayor control     │  │  Fácil de configurar │            │
│  └────────────────────┘  └──────────────────────┘            │
│                                                              │
│  ┌────────────────────┐  ┌──────────────────────┐            │
│  │  Redis             │  │  Motorhead           │            │
│  │  Chat Memory       │  │  Chat Memory         │            │
│  │  ──────────────────│  │  ──────────────────  │            │
│  │  Base de datos     │  │  Servicio            │            │
│  │  en memoria,       │  │  especializado en    │            │
│  │  muy rápida        │  │  memoria de chat     │            │
│  └────────────────────┘  └──────────────────────┘            │
└──────────────────────────────────────────────────────────────┘
```

| Opción | Tipo | Ventaja | Complejidad |
|--------|------|---------|-------------|
| **PostgreSQL** | SQL relacional | Robusto, maduro, buen ecosistema | Media |
| **Supabase** | PostgreSQL cloud | Gratis (tier inicial), API REST incluida | Baja |
| **Redis** | Key-value en memoria | Muy rápido, ideal para alta concurrencia | Media |
| **Motorhead** | Servicio de memoria | Diseñado específicamente para chat (deprecated) | Baja |

#### Configuración de PostgreSQL Chat Memory

```
CONFIGURACIÓN: POSTGRESQL CHAT MEMORY

1. Requisito: tener una instancia de PostgreSQL accesible

2. En n8n:
   AI Agent → Memory → PostgreSQL Chat Memory

3. Credenciales:
   ┌────────────────────────────────┐
   │ Host:     localhost            │
   │ Port:     5432                 │
   │ Database: n8n_memory           │
   │ User:     postgres             │
   │ Password: ********             │
   │ Table:    chat_histories       │
   └────────────────────────────────┘
   Nota: Para Supabase, "Connect to your project" con Method: Session pooler

4. n8n crea automáticamente la tabla si no existe

5. Estructura de la tabla:
   ┌────────────┬──────────┬─────────────────────┐
   │ session_id │ role     │ content             │
   ├────────────┼──────────┼─────────────────────┤
   │ user_123   │ user     │ "Me llamo Carlos"   │
   │ user_123   │ assistant│ "¡Hola Carlos!"     │
   │ user_456   │ user     │ "Hola, soy Ana"     │
   └────────────┴──────────┴─────────────────────┘
```

### 3.4 Session Key y Múltiples Conversaciones

Cuando un agente atiende a múltiples usuarios, es fundamental que cada uno tenga su propio contexto de conversación. Esto se gestiona mediante el **Session ID**.

```
┌──────────────────────────────────────────────────────────────┐
│        SESIONES: SEPARAR CONTEXTO POR USUARIO                │
│                                                              │
│  Usuario A (session_id: "user_A")                            │
│  ┌─────────────────────────────────────────┐                 │
│  │ "Me llamo Ana, trabajo en Microsoft"    │                 │
│  │ "¿Dónde trabajo?" → "En Microsoft"      │                 │
│  └─────────────────────────────────────────┘                 │
│                                                              │
│  Usuario B (session_id: "user_B")                            │
│  ┌─────────────────────────────────────────┐                 │
│  │ "Soy Pedro, estudio en la UNAM"         │                 │
│  │ "¿Cómo me llamo?" → "Pedro"             │                 │
│  └─────────────────────────────────────────┘                 │
│                                                              │
│  Las conversaciones están COMPLETAMENTE aisladas.            │
│  Ana no puede ver la conversación de Pedro y viceversa.      │
└──────────────────────────────────────────────────────────────┘
```

#### Configuración del Session ID

El Session ID puede obtenerse de diferentes fuentes según el canal de comunicación:

| Canal | Fuente del Session ID | Expresión en n8n |
|-------|----------------------|-------------------|
| **Chat embebido** | Automático (n8n lo genera) | (configuración por defecto) |
| **Telegram** | ID del chat de Telegram | `{{ $json.message.chat.id }}` |
| **Webhook** | Header o parámetro del request | `{{ $json.headers.x-session-id }}` |
| **WhatsApp** | Número de teléfono | `{{ $json.from }}` |

#### Configuración en el Nodo de Memoria

```
Window Buffer Memory / PostgreSQL Chat Memory:

Session ID:
  ┌──────────────────────────────────────────┐
  │  Opción 1: "Connected Chat Trigger"      │  ← Automático
  │  Opción 2: "Define Below"                │  ← Manual
  │             {{ $json.message.chat.id }}  │
  └──────────────────────────────────────────┘
```

> **Buena práctica**: Usar siempre un Session ID que identifique unívocamente al usuario o conversación. Esto es crítico cuando el agente se despliega en canales con múltiples usuarios concurrentes.

---

## Bloque 4: Despliegue de Agentes en Canales de Comunicación (45 minutos)

### 4.1 Chat Embebido en n8n

n8n proporciona dos formas de interactuar con el agente a través de chat: una interfaz interna para pruebas y un widget embebible en páginas web.

#### Chat Interno (Pruebas)

```
┌──────────────────────────────────────────────────────────────┐
│              CHAT INTERNO DE n8n                             │
│                                                              │
│  Acceso: Botón "Chat" en la barra superior del workflow      │
│                                                              │
│  ┌──────────────────────────────────────────────────┐        │
│  │  n8n Chat (Test Mode)                            │        │
│  ├──────────────────────────────────────────────────┤        │
│  │                                                  │        │
│  │  Agente: ¡Hola! ¿En qué puedo ayudarte?          │        │
│  │                                                  │        │
│  │  Tú: ¿Quién fue Marie Curie?                     │        │
│  │                                                  │        │
│  │  Agente: [Consultando Wikipedia...]              │        │
│  │  Marie Curie fue una científica polaca...        │        │
│  │                                                  │        │
│  ├──────────────────────────────────────────────────┤        │
│  │  [Escribe tu mensaje...]              [Enviar]   │        │
│  └──────────────────────────────────────────────────┘        │
│                                                              │
│  Uso: Pruebas rápidas durante el desarrollo                  │
│  Limitación: Solo accesible dentro de n8n                    │
└──────────────────────────────────────────────────────────────┘
```

#### Widget Embebible en Páginas Web

n8n genera un snippet HTML/JavaScript que se puede insertar en cualquier página web para que los usuarios finales interactúen con el agente.

```html
<!-- Widget de chat de n8n embebido en una página web -->
<link href="https://tu-n8n.com/webhook/chat/style.css" rel="stylesheet" />
<script type="module">
  import { createChat } from 'https://tu-n8n.com/webhook/chat/chat.js';

  createChat({
    webhookUrl: 'https://tu-n8n.com/webhook/mi-agente/chat',
    title: 'Asistente TechStore',
    subtitle: '¿En qué puedo ayudarte?',
    initialMessages: [
      '¡Hola! Soy el asistente virtual de TechStore.'
    ],
  });
</script>
```

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `webhookUrl` | URL del webhook del chat | `https://tu-n8n.com/webhook/.../chat` |
| `title` | Título del widget | "Asistente TechStore" |
| `subtitle` | Subtítulo | "¿En qué puedo ayudarte?" |
| `initialMessages` | Mensajes iniciales del agente | ["¡Hola! Soy el asistente..."] |

### 4.2 Integración con Telegram

Telegram es uno de los canales más populares para desplegar agentes de IA. El proceso implica crear un bot con BotFather y conectarlo a n8n.

#### Paso 1: Crear Bot con BotFather

```
CREACIÓN DE BOT EN TELEGRAM:

1. Abrir Telegram y buscar @BotFather

2. Enviar: /newbot

3. BotFather pregunta:
   "What's the name for your bot?"
   → Responder: "Mi Agente IA"

4. BotFather pregunta:
   "Choose a username for your bot"
   → Responder: "mi_agente_ia_bot"
   (debe terminar en "bot")

5. BotFather responde:
   "Done! Your bot is ready."
   Token: 7123456789:AAH_tu_token_secreto_aquí

   ← GUARDAR ESTE TOKEN
```

#### Paso 2: Configurar en n8n

```
WORKFLOW: AGENTE EN TELEGRAM

┌──────────────────┐     ┌───────────────────────────────────┐
│  Telegram        │────►│  AI Agent                         │
│  Trigger         │     │                                   │
│                  │     │  Chat Model: trinity-large-preview│
│  Evento:         │     │  Memory: Postgres Chat Memory     │
│  "Message"       │     │  Session ID:                      │
│                  │     │  {{ $json.message.chat.id }}      │
│  Credenciales:   │     │                                   │
│  Bot Token       │     │  Tools: Wikipedia, Calculator     │
│                  │     │                                   │
└──────────────────┘     └─────────────┬─────────────────────┘
                                       │
                                       ▼
                         ┌───────────────────────────────────┐
                         │  Telegram                         │
                         │  Send Message                     │
                         │                                   │
                         │  Chat ID:                         │
                         │  {{ $json.message.chat.id }}      │
                         │                                   │
                         │  Text:                            │
                         │  {{ $json.output }}               │
                         └───────────────────────────────────┘
```

#### Paso a Paso de Configuración

| Paso | Nodo | Configuración |
|------|------|---------------|
| 1 | **Telegram Trigger** | Credencial: Bot Token de BotFather. Evento: "message" |
| 2 | **AI Agent** | Prompt: `{{ $json.message.text }}`. System prompt con estructura RTRF |
| 3 | **Chat Model** | OpenAI Chat Model con gpt-4o-mini |
| 4 | **Memory** | Window Buffer. Session ID: `{{ $json.message.chat.id }}` |
| 5 | **Telegram Send** | Chat ID: `{{ $json.message.chat.id }}`. Texto: `{{ $json.output }}` |

#### Gestión de Sesiones por chat_id

Cada chat de Telegram tiene un `chat_id` único. Al usarlo como Session ID en la memoria, garantizamos que:

- Cada usuario tiene su propio historial de conversación
- Los grupos tienen un historial compartido
- Un mismo usuario que escriba desde otro chat tendrá un historial separado

```
Ejemplo de Session IDs de Telegram:

Chat privado con Ana:    chat_id = 123456789
Chat privado con Pedro:  chat_id = 987654321
Grupo "Equipo Dev":      chat_id = -100123456

Cada uno tiene su propio historial en la memoria del agente.
```

### 4.3 Webhook para Integraciones Personalizadas

El nodo Webhook permite que cualquier aplicación externa interactúe con el agente mediante peticiones HTTP.

```
WORKFLOW: AGENTE VÍA WEBHOOK

┌──────────────────┐     ┌──────────────────┐     ┌──────────────┐
│  Webhook         │────►│  AI Agent        │────►│  Respond to  │
│  Trigger         │     │                  │     │  Webhook     │
│                  │     │  Chat Model      │     │              │
│  Method: POST    │     │  Memory          │     │  Respuesta   │
│  Path: /mi-agente│     │  Tools           │     │  JSON        │
│                  │     │                  │     │              │
└──────────────────┘     └──────────────────┘     └──────────────┘
```

#### Ejemplo de Llamada al Webhook

```bash
# Petición HTTP al agente
curl -X POST https://tu-n8n.com/webhook/mi-agente \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Cuál es la capital de Francia?",
    "session_id": "user_001"
  }'

# Respuesta del agente
{
  "output": "La capital de Francia es París.",
  "session_id": "user_001"
}
```

#### Casos de Uso del Webhook

| Caso de Uso | Aplicación Cliente | Beneficio |
|-------------|-------------------|-----------|
| App móvil personalizada | React Native, Flutter | Control total de la UI |
| Integración CRM | Salesforce, HubSpot | Asistente dentro del CRM |
| Slack / Discord bot | Aplicación custom | Canales de equipo |
| Página web SPA | React, Vue, Angular | Chat personalizado |

### 4.4 WhatsApp Business (Conceptual)

La integración con WhatsApp es posible pero requiere pasos adicionales debido a las restricciones de Meta.

```
┌──────────────────────────────────────────────────────────────┐
│           INTEGRACIÓN CON WHATSAPP BUSINESS                  │
│                                                              │
│  Requisitos:                                                 │
│  ┌──────────────────────────────────────────────────┐        │
│  │ 1. Cuenta de Meta Business verificada            │        │
│  │ 2. Aplicación creada en Meta for Developers      │        │
│  │ 3. Número de teléfono dedicado para WhatsApp     │        │
│  │ 4. Acceso a la WhatsApp Business API             │        │
│  │ 5. Webhook configurado para recibir mensajes     │        │
│  └──────────────────────────────────────────────────┘        │
│                                                              │
│  Flujo:                                                      │
│  ┌────────┐    ┌──────────┐    ┌────────┐    ┌────────────┐  │
│  │WhatsApp│───►│ Meta API │───►│Webhook │───►│ AI Agent   │  │
│  │Usuario │    │          │    │ n8n    │    │            │  │
│  │        │◄───│          │◄───│        │◄───│            │  │
│  └────────┘    └──────────┘    └────────┘    └────────────┘  │
│                                                              │
│  Alternativa más sencilla: servicios intermediarios          │
│  como Twilio o 360dialog que simplifican la integración.     │
└──────────────────────────────────────────────────────────────┘
```

| Aspecto | Detalle |
|---------|---------|
| **Coste** | WhatsApp Business API es de pago por conversación |
| **Verificación** | Requiere cuenta de empresa verificada por Meta |
| **Alternativas** | Twilio, 360dialog, MessageBird simplifican el proceso |
| **Session ID** | Número de teléfono del usuario (`{{ $json.from }}`) |
| **Limitaciones** | Templates aprobados para mensajes proactivos, ventana de 24h |

> **Nota**: Para el ejercicio práctico de esta sesión, usaremos Telegram por su simplicidad. La integración con WhatsApp es conceptualmente similar pero requiere pasos administrativos adicionales.

---

## Bloque 5: Ejercicio Práctico Guiado (40 minutos)

### 5.1 Objetivo del Ejercicio

Construir un agente completo de investigación que:
- Responda preguntas usando Wikipedia
- Realice cálculos matemáticos
- Recuerde el contexto de la conversación
- Tenga un system prompt bien estructurado
- (Opcional) Se despliegue en Telegram

### 5.2 Construcción Paso a Paso

#### Paso 1: Chat Trigger

```
┌─────────────────────────────────────────────┐
│  Nodo: Chat Trigger                         │
│                                             │
│  Configuración: Ninguna necesaria           │
│  Salida: {{ $json.chatInput }}              │
│                                             │
│  Este nodo proporciona la interfaz de chat  │
│  interna de n8n para pruebas.               │
└─────────────────────────────────────────────┘
```

#### Paso 2: AI Agent con Modelo OpenAI/Gemini

```
┌─────────────────────────────────────────────┐
│  Nodo: AI Agent                             │
│                                             │
│  Prompt: {{ $json.chatInput }}              │
│                                             │
│  Subnodo Chat Model:                        │
│  ┌─────────────────────────────────────┐    │
│  │  Tipo: OpenAI Chat Model            │    │
│  │  Modelo: gpt-4o-mini                │    │
│  │  Temperature: 0.7                   │    │
│  │  Credencial: Tu API Key de OpenAI   │    │
│  │                                     │    │
│  │  Alternativa: Google Gemini         │    │
│  │  Modelo: gemini-1.5-flash           │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

#### Paso 3: System Prompt con Estructura PDA (Persona-Directrices-Acción)

```
System Prompt para el agente:

---
Eres un asistente de investigación y cálculo llamado "InvestigaBot".

## Tareas
- Responder preguntas de cultura general buscando en Wikipedia
- Realizar cálculos matemáticos cuando sea necesario
- Combinar información de múltiples fuentes para dar respuestas completas

## Restricciones
- Responde SIEMPRE en español
- Si no encuentras información en Wikipedia, dilo honestamente
- NUNCA inventes datos: usa las herramientas disponibles
- Si la pregunta requiere un cálculo, usa la calculadora (no calcules mentalmente)

## Formato
- Respuestas concisas: máximo 3 párrafos
- Si usaste una herramienta, menciona brevemente que consultaste la fuente
- Usa listas para enumerar datos
---
```

#### Paso 4: Window Buffer Memory

```
┌─────────────────────────────────────────────┐
│  Subnodo: Window Buffer Memory              │
│                                             │
│  Context Window Length: 10                  │
│  Session ID: Connected Chat Trigger         │
│                                             │
│  Esto permite que el agente recuerde los    │
│  últimos 10 turnos de conversación.         │
└─────────────────────────────────────────────┘
```

#### Paso 5: Herramienta Wikipedia

```
┌─────────────────────────────────────────────┐
│  Subnodo Tool: Wikipedia                    │
│                                             │
│  Configuración: Ninguna necesaria           │
│                                             │
│  El agente decidirá autónomamente cuándo    │
│  buscar en Wikipedia según la pregunta.     │
└─────────────────────────────────────────────┘
```

#### Paso 6: Herramienta Calculator

```
┌─────────────────────────────────────────────┐
│  Subnodo Tool: Calculator                   │
│                                             │
│  Configuración: Ninguna necesaria           │
│                                             │
│  El agente decidirá cuándo necesita         │
│  realizar un cálculo matemático.            │
└─────────────────────────────────────────────┘
```

### 5.3 Pruebas de Verificación

Una vez construido el agente, ejecutar la siguiente secuencia de pruebas para verificar que todo funciona correctamente:

| Prueba | Mensaje | Resultado Esperado | Verifica |
|--------|---------|---------------------|----------|
| 1 | "Hola, me llamo Lucía" | Saludo personalizado | Interacción básica |
| 2 | "¿Quién fue Ada Lovelace?" | Información de Wikipedia | Uso de herramienta Wikipedia |
| 3 | "¿En qué año nació? ¿Cuántos años habrían pasado hasta hoy?" | Año de Wikipedia + cálculo | Wikipedia + Calculator |
| 4 | "¿Cómo me llamo?" | "Te llamas Lucía" | Memoria funcional |
| 5 | "Si un libro cuesta 24.99€ y compro 3, ¿cuánto pago con 21% de IVA?" | Cálculo detallado | Calculator con cálculo complejo |
| 6 | "¿De quién estábamos hablando antes?" | "De Ada Lovelace" | Memoria de contexto |

### 5.4 (Opcional) Despliegue en Telegram

Para los estudiantes que quieran ir un paso más allá:

| Paso | Acción |
|------|--------|
| 1 | Crear bot con @BotFather en Telegram |
| 2 | Copiar el token del bot |
| 3 | En n8n, reemplazar Chat Trigger por Telegram Trigger |
| 4 | Configurar credencial de Telegram con el token |
| 5 | Añadir nodo Telegram Send Message al final |
| 6 | Cambiar Session ID de la memoria a `{{ $json.message.chat.id }}` |
| 7 | Activar el workflow y probar enviando mensajes al bot desde Telegram |

### 5.5 Diagrama del Workflow Completo

```
┌──────────────────────────────────────────────────────────────────┐
│              WORKFLOW COMPLETO: INVESTIGA-BOT                    │
│                                                                  │
│  ┌──────────────┐     ┌──────────────────────────────────────┐   │
│  │  Chat Trigger│────►│  AI Agent                            │   │
│  │  (o Telegram │     │                                      │   │
│  │   Trigger)   │     │  System Prompt: "InvestigaBot"       │   │
│  └──────────────┘     │                                      │   │
│                       │  ┌──────────────┐ ┌───────────────┐  │   │
│                       │  │ OpenAI Chat  │ │ Window Buffer │  │   │
│                       │  │ Model        │ │ Memory        │  │   │
│                       │  │ gpt-4o-mini  │ │ Length: 10    │  │   │
│                       │  └──────────────┘ └───────────────┘  │   │
│                       │                                      │   │
│                       │  ┌──────────────┐ ┌───────────────┐  │   │
│                       │  │ Wikipedia    │ │ Calculator    │  │   │
│                       │  │ Tool         │ │ Tool          │  │   │
│                       │  └──────────────┘ └───────────────┘  │   │
│                       │                                      │   │
│                       └──────────────────────────────────────┘   │
│                                                                  │
│  Si Telegram: añadir nodo Telegram Send Message al final         │
└──────────────────────────────────────────────────────────────────┘
```

---

## Resumen de la Sesión

### Conceptos Clave

1. **Nodos de IA en n8n**: Ecosistema completo con Chat Models, Embeddings, Vector Stores, Document Loaders y Text Splitters que permiten construir workflows inteligentes
2. **Proveedores de LLMs**: Integración nativa con OpenAI, Google Gemini, Anthropic Claude y modelos locales vía Ollama, todos configurables como subnodos
3. **AI Agent**: Nodo central que combina un Chat Model, Memory, Tools y System Prompt para crear agentes autónomos que razonan y usan herramientas
4. **Memoria**: Window Buffer Memory para sesiones temporales y PostgreSQL/Supabase/Redis para memoria persistente, con Session ID para separar conversaciones
5. **Despliegue**: Agentes desplegables en chat embebido, Telegram (via BotFather), webhooks personalizados y WhatsApp Business

### Qué Deberías Saber Hacer

| Habilidad | Nivel Esperado |
|-----------|---------------|
| Configurar credenciales de IA en n8n | API Keys de OpenAI, Gemini y Anthropic |
| Crear un workflow básico con IA | Chat Trigger + Basic LLM Chain + modelo |
| Construir un AI Agent completo | Con modelo, herramientas y system prompt |
| Escribir system prompts para agentes | Estructura RTRF: Rol, Tareas, Restricciones, Formato |
| Añadir memoria a un agente | Window Buffer Memory con Session ID |
| Configurar memoria persistente | PostgreSQL o Supabase Chat Memory |
| Desplegar agente en Telegram | Bot con BotFather + Telegram Trigger en n8n |
| Usar webhooks para integraciones | Webhook Trigger + AI Agent + Respond to Webhook |

---

## Conexión con la Práctica

La práctica evaluable de esta unidad está disponible en [practica.md](../practica.md).

**Proyecto**: Construcción de un agente de IA completo desplegado en un canal de comunicación real, aplicando todos los conceptos de automatización con n8n, herramientas, memoria y despliegue estudiados en esta sesión.

---

## Conexión con Otras Unidades

```
ROADMAP DEL CURSO:

Unidad 3 (anterior):   APIs + Function Calling + LangChain
                        └─ Base teórica de Tools y Agents

Unidad 4 (actual):     n8n + Agentes + Memoria + Despliegue
                        └─ Implementación visual y práctica de agentes

Unidad 5 (siguiente):  RAG (Retrieval-Augmented Generation)
                        └─ Embeddings, Vector Stores, Document Loaders
                        └─ Los nodos de IA de n8n que vimos en 1.1

Unidad 6 (futuro):     MCP (Model Context Protocol)
                        └─ Protocolo estándar para conectar herramientas
                        └─ Evolución del concepto de Tools de agentes
```

---

## Actividades

### Ejercicios de esta Sesión

Completa los ejercicios prácticos disponibles en [ejercicios.md](./ejercicios.md):

1. **Chat básico con IA** - Crear workflow con Chat Trigger + Basic LLM Chain + OpenAI
2. **Agente con herramientas** - Construir AI Agent con Wikipedia y Calculator
3. **System prompt estructurado** - Diseñar prompt con estructura RTRF para un caso de uso específico
4. **Memoria en agentes** - Añadir Window Buffer Memory y verificar retención de contexto
5. **Despliegue en Telegram** - Crear bot y conectar con el agente de n8n
6. **Webhook personalizado** - Exponer el agente como API REST vía webhook

### Práctica Evaluable de la Unidad

Al finalizar ambas sesiones, completa la [práctica evaluable](../practica.md) de la Unidad 4.

---

## Referencias

- n8n. (2024). AI Nodes Documentation. https://docs.n8n.io/integrations/builtin/cluster-nodes/
- n8n. (2024). AI Agent Node. https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/
- n8n. (2024). Memory Nodes. https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.memorybufferwindow/
- OpenAI. (2024). API Reference. https://platform.openai.com/docs/api-reference
- Anthropic. (2024). Claude API Documentation. https://docs.anthropic.com/en/api
- Google. (2024). Gemini API Documentation. https://ai.google.dev/docs
- Telegram. (2024). Bot API. https://core.telegram.org/bots/api
- Ollama. (2024). Documentation. https://ollama.ai/docs
- Repositorio del curso: https://github.com/rpmaya/ml2_code
