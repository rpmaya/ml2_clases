# Unidad 4 - Sesión 1: Agentes de IA y Fundamentos de n8n

## Objetivos de la Sesión

Al finalizar esta sesión, el estudiante será capaz de:
- Comprender qué es un agente de IA, sus componentes y el paradigma Percepción-Decisión-Acción
- Entender la filosofía y ventajas de n8n como plataforma de automatización no-code con IA nativa
- Instalar y configurar n8n en entorno local y en la nube (Koyeb)
- Dominar la arquitectura de n8n: workflows, nodos, conexiones y credenciales
- Construir automatizaciones básicas con triggers, acciones y expresiones

## Duración Total: 4 horas

---

## Bloque 1: Introducción a los Agentes de IA (45 minutos)

### 1.1 ¿Qué es un Agente de IA?

Un **agente de IA** es un sistema que puede **percibir** su entorno, **tomar decisiones** y **ejecutar acciones** de forma autónoma para alcanzar un objetivo.

#### Analogía: El Robot Autónomo

Imagina un robot en una fábrica:
- **Percibe**: Sensores detectan piezas en la cinta transportadora (cámaras, sensores de proximidad)
- **Decide**: Analiza qué pieza es, dónde colocarla, si hay defectos
- **Actúa**: Mueve el brazo mecánico, coloca la pieza, alerta si hay problemas

Los agentes de IA funcionan exactamente igual, pero en el mundo digital.

#### Ejemplo Concreto: Chatbot de Atención al Cliente

```
┌────────────────────────────────────────────────────────────────┐
│              AGENTE: CHATBOT DE ATENCIÓN AL CLIENTE            │
│                                                                │
│   PERCEPCIÓN              DECISIÓN                ACCIÓN       │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │ Mensaje del  │───►│ LLM analiza  │───►│ Responder    │      │
│  │ cliente      │    │ intención    │    │ al cliente   │      │
│  │              │    │              │    │              │      │
│  │ Historial de │───►│ Consulta base│───►│ Crear ticket │      │
│  │ conversación │    │ de datos     │    │ de soporte   │      │
│  │              │    │              │    │              │      │
│  │ Datos del    │───►│ Decide acción│───►│ Escalar a    │      │
│  │ cliente      │    │ más adecuada │    │ humano       │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
└────────────────────────────────────────────────────────────────┘
```

#### Los Tres Componentes Fundamentales

| Componente | Descripción | Ejemplos |
|------------|-------------|----------|
| **Percepción** (Inputs) | Todo lo que el agente recibe del entorno | Mensajes de usuario, datos de APIs, eventos, sensores |
| **Decisión** (Procesamiento) | El "cerebro" del agente que analiza y planifica | LLM (GPT, Claude), reglas de negocio, lógica condicional |
| **Acción** (Outputs) | Lo que el agente ejecuta en el entorno | Enviar emails, actualizar BBDD, llamar APIs, generar respuestas |

### 1.2 ¿Por Qué Agentes de IA y Por Qué Ahora?

La convergencia de tres factores hace que este sea el momento ideal para los agentes de IA:

```
┌────────────────────────────────────────────────────────────────┐
│            ¿POR QUÉ AGENTES DE IA AHORA?                       │
│                                                                │
│   1. AUTOMATIZACIÓN INTELIGENTE                                │
│      │  Antes: reglas fijas ("si X, entonces Y")               │
│      │  Ahora: decisiones contextuales con LLMs                │
│      │                                                         │
│   2. PERSONALIZACIÓN A ESCALA                                  │
│      │  Antes: respuestas genéricas para todos                 │
│      │  Ahora: interacción adaptada a cada usuario             │
│      │                                                         │
│   3. DEMOCRATIZACIÓN (NO-CODE)                                 │
│      │  Antes: solo desarrolladores podían crear agentes       │
│      │  Ahora: cualquiera con herramientas como n8n            │
│                                                                │
│   LLMs potentes + APIs accesibles + Herramientas no-code       │
│                    = Agentes al alcance de todos               │
└────────────────────────────────────────────────────────────────┘
```

### 1.3 De Function Calling a Agentes Autónomos

En la Unidad 3 aprendimos **Function Calling**: la capacidad de un LLM para invocar funciones externas. Los agentes de IA llevan este concepto mucho más lejos.

#### Conexión con la Unidad 3

```
RECORRIDO DEL CURSO:

Unidad 1: Fundamentos de IA Generativa y LLMs
├── Qué son los LLMs, cómo funcionan
└── Capacidades y limitaciones

Unidad 2: Prompt Engineering
├── Diseño de prompts efectivos
└── Técnicas avanzadas (CoT, few-shot)

Unidad 3: Arquitectura Transformer y APIs
├── Self-Attention, arquitectura interna
├── APIs de OpenAI, Claude, Gemini
└── Function Calling ← BASE PARA AGENTES

Unidad 4: Agentes de IA y n8n  ← ESTAMOS AQUÍ
├── Agentes autónomos con múltiples herramientas
├── Plataforma n8n para automatización con IA
└── De la teoría a la práctica sin código
```

#### Function Calling vs. Agentes: Comparativa

| Aspecto | Function Calling (Unidad 3) | Agente de IA (Unidad 4) |
|---------|----------------------------|------------------------|
| **Herramientas** | Una función por llamada | Múltiples herramientas encadenadas |
| **Memoria** | Sin memoria entre llamadas | Memoria persistente de conversación |
| **Encadenamiento** | Manual (el desarrollador orquesta) | Automático (el agente decide el orden) |
| **Autonomía** | El usuario dirige cada paso | El agente planifica y ejecuta solo |
| **Ejemplo** | "Consulta el clima en Madrid" | "Planifica mi viaje a Madrid: consulta clima, busca vuelos, reserva hotel" |

#### Ejemplo Comparativo

```
FUNCTION CALLING (Unidad 3):
────────────────────────────
Usuario: "¿Qué tiempo hace en Madrid?"
LLM → llama a get_weather("Madrid")
API → {"temp": 22, "estado": "soleado"}
LLM → "En Madrid hace 22°C y está soleado"
                    FIN (una sola herramienta, una sola acción)


AGENTE DE IA (Unidad 4):
────────────────────────
Usuario: "Organiza mi viaje a Madrid la próxima semana"
Agente → PASO 1: get_weather("Madrid", "próxima semana")
       → PASO 2: search_flights("Barcelona", "Madrid", fechas)
       → PASO 3: search_hotels("Madrid", fechas, presupuesto)
       → PASO 4: create_calendar_event(vuelo, hotel)
       → PASO 5: send_email(usuario, resumen_viaje)
       → Respuesta: "He organizado tu viaje. Vuelo el lunes a las 10:00,
         hotel céntrico reservado, todo añadido a tu calendario."
                    (múltiples herramientas, planificación autónoma)
```

### 1.4 El Paradigma Percepción-Decisión-Acción (PDA)

Todo agente de IA se puede diseñar respondiendo a tres preguntas fundamentales:

```
┌────────────────────────────────────────────────────────────────┐
│              PARADIGMA PDA (PERCEPCIÓN-DECISIÓN-ACCIÓN)        │
│                                                                │
│   ┌─────────────┐      ┌─────────────┐      ┌─────────────┐    │
│   │  PERCEPCIÓN │─────►│  DECISIÓN   │─────►│   ACCIÓN    │    │
│   │             │      │             │      │             │    │
│   │ ¿Qué recibe │      │ ¿Cómo       │      │ ¿Qué hace   │    │
│   │  el agente? │      │  procesa?   │      │  el agente? │    │
│   └─────────────┘      └─────────────┘      └─────────────┘    │
│         │                     │                     │          │
│         ▼                     ▼                     ▼          │
│   - Mensajes texto      - LLM (GPT,          - Enviar emails   │
│   - Webhooks              Claude)             - Actualizar DB  │
│   - Formularios         - Reglas de           - Llamar APIs    │
│   - Eventos de apps       negocio             - Generar docs   │
│   - Datos de APIs       - Lógica              - Notificar      │
│   - Archivos             condicional          - Crear tickets  │
│                         - Memoria             - Publicar       │
│                           contextual                           │
└────────────────────────────────────────────────────────────────┘
```

#### Preguntas de Diseño para Cada Componente

Al diseñar un agente, hazte estas preguntas:

**Percepción:**
- ¿De dónde vienen los datos? (chat, email, webhook, formulario, evento)
- ¿Qué formato tienen? (texto, JSON, imagen, archivo)
- ¿Con qué frecuencia llegan? (tiempo real, programado, bajo demanda)

**Decisión:**
- ¿Qué modelo de IA utilizará? (GPT-4, Claude, Gemini, modelo local)
- ¿Necesita contexto o memoria? (historial de conversación, datos previos)
- ¿Qué herramientas tiene disponibles? (APIs, bases de datos, servicios)
- ¿Cuál es su objetivo? (responder preguntas, automatizar tareas, analizar datos)

**Acción:**
- ¿Qué acciones puede ejecutar? (enviar mensajes, crear documentos, actualizar sistemas)
- ¿Necesita confirmación humana? (human-in-the-loop)
- ¿Cómo se mide el éxito? (tiempo de respuesta, precisión, satisfacción)

---

## Bloque 2: Introducción a n8n - Automatización No-Code (50 minutos)

### 2.1 ¿Qué es n8n?

**n8n** (pronunciado "nodemation", de *node automation*) es una plataforma de automatización de workflows **open source** con una interfaz visual y soporte nativo para **agentes de IA**.

```
┌────────────────────────────────────────────────────────────────┐
│                       ¿QUÉ ES n8n?                             │
│                                                                │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                  INTERFAZ VISUAL (LIENZO)               │  │
│   │                                                         │  │
│   │   [Trigger] ──► [Nodo 1] ──► [Nodo 2] ──► [Nodo 3]      │  │
│   │    (Evento)    (Procesar)   (Decidir)    (Actuar)       │  │
│   │                                                         │  │
│   │   Arrastra, conecta, configura. Sin escribir código.    │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                │
│   CARACTERÍSTICAS CLAVE:                                       │
│   ✔ Open source (licencia fair-code)                           │
│   ✔ Self-hosted o cloud                                        │
│   ✔ +400 integraciones nativas                                 │
│   ✔ Nodo AI Agent nativo                                       │
│   ✔ Soporte para modelos de IA (OpenAI, Claude, Gemini, etc.)  │
│   ✔ Código personalizado cuando sea necesario (JavaScript/Python)│
└──────────────────────────────────────────────────────────────┘
```

#### Filosofía de n8n

- **Visual-first**: Todo se diseña arrastrando y conectando nodos en un lienzo
- **Open source**: Código disponible en GitHub, comunidad activa
- **Extensible**: Si no existe un nodo, puedes crear el tuyo o usar HTTP Request
- **IA nativa**: No es un add-on; los agentes de IA son ciudadanos de primera clase
- **Fair-code**: Gratuito para self-hosting; modelo de pago para la versión cloud

### 2.2 Comparativa: n8n vs Make vs Zapier

| Característica | n8n | Make (Integromat) | Zapier |
|---------------|-----|-------------------|--------|
| **Modelo** | Open source (fair-code) | SaaS propietario | SaaS propietario |
| **Despliegue** | Cloud, self-hosted, local | Solo cloud | Solo cloud |
| **Código personalizado** | JavaScript y Python nativos | Limitado | Muy limitado |
| **Agentes de IA** | Nodo AI Agent nativo | No nativo | No nativo |
| **Precio** | Gratis (self-hosted), desde 20€/mes (cloud) | Desde 9$/mes | Desde 19.99$/mes |
| **Integraciones** | +400 nativas + HTTP Request | +1000 | +5000 |
| **Complejidad de workflows** | Ilimitada (loops, branches, sub-workflows) | Alta | Media |
| **Comunidad** | Muy activa, templates compartidos | Activa | Muy grande |
| **Curva de aprendizaje** | Media | Media | Baja |

#### ¿Cuándo Elegir n8n?

```
ELIGE n8n CUANDO:
─────────────────
✔ Necesitas agentes de IA con herramientas
✔ Quieres control total (self-hosting, datos privados)
✔ Necesitas lógica compleja (loops, condiciones, sub-workflows)
✔ Quieres combinar no-code con código personalizado
✔ Tu presupuesto es limitado (self-hosted es gratuito)
✔ Necesitas integrar modelos de IA (OpenAI, Claude, Gemini, Ollama)

ELIGE ZAPIER/MAKE CUANDO:
─────────────────────────
✔ Necesitas integraciones rápidas y sencillas
✔ No quieres gestionar infraestructura
✔ Tus workflows son lineales y simples
✔ Necesitas una integración específica que solo ellos tienen
```

### 2.3 Ventajas de n8n para Agentes de IA

n8n destaca especialmente para la construcción de agentes de IA por cuatro razones:

| Ventaja | Descripción |
|---------|-------------|
| **Nodo AI Agent nativo** | Nodo dedicado que conecta un LLM con herramientas, memoria y lógica de agente |
| **Memoria persistente** | Almacenamiento de contexto entre conversaciones (buffer, ventana, resumen) |
| **Herramientas ilimitadas** | Cualquier nodo de n8n puede ser una herramienta del agente (Gmail, Sheets, HTTP, SQL...) |
| **Canales de entrada diversos** | Chat embebido, Webhook, Telegram, Slack, WhatsApp, formularios |

```
┌──────────────────────────────────────────────────────────────┐
│               AGENTE DE IA EN n8n                              │
│                                                                │
│   CANALES           AI AGENT              HERRAMIENTAS         │
│  ┌─────────┐    ┌──────────────┐    ┌──────────────────┐      │
│  │  Chat   │───►│              │───►│  Gmail           │      │
│  │  Web    │    │   LLM        │    │  Google Sheets   │      │
│  ├─────────┤    │  (GPT/Claude)│    │  HTTP Request    │      │
│  │ Telegram│───►│              │    │  Base de datos   │      │
│  ├─────────┤    │   Memoria    │    │  Calendario      │      │
│  │ Webhook │───►│   ┌──────┐  │    │  Slack           │      │
│  ├─────────┤    │   │Buffer│  │    │  Vector Store    │      │
│  │  Slack  │───►│   └──────┘  │    │  Código custom   │      │
│  └─────────┘    └──────────────┘    └──────────────────┘      │
└──────────────────────────────────────────────────────────────┘
```

### 2.4 Integraciones Disponibles: Apps, APIs y Modelos de IA

n8n ofrece más de 400 integraciones nativas organizadas por categorías:

| Categoría | Ejemplos de Integraciones |
|-----------|--------------------------|
| **Productividad** | Google Sheets, Google Docs, Notion, Airtable, Microsoft Excel |
| **CRM** | HubSpot, Salesforce, Pipedrive |
| **Comunicación** | Gmail, Outlook, Slack, Telegram, WhatsApp, Discord |
| **Bases de datos** | PostgreSQL, MySQL, MongoDB, Redis, Supabase |
| **Modelos de IA** | OpenAI (GPT), Anthropic (Claude), Google (Gemini), Ollama, Groq, Mistral |
| **Almacenamiento vectorial** | Pinecone, Qdrant, Supabase Vector, PostgreSQL pgvector |
| **Almacenamiento de archivos** | Google Drive, Dropbox, AWS S3 |
| **Desarrollo** | GitHub, GitLab, Jira, HTTP Request, Webhook |
| **Redes sociales** | X (Twitter), LinkedIn, Facebook, Instagram |
| **Finanzas** | Stripe, PayPal, QuickBooks |

> **Nota**: Si una integración no existe de forma nativa, el nodo **HTTP Request** permite conectar con cualquier API REST del mundo.

---

### --- DESCANSO (15 minutos) ---

---

## Bloque 3: Instalación y Configuración de n8n (45 minutos)

### 3.1 Opciones de Despliegue

n8n ofrece tres modalidades de despliegue según las necesidades:

| Opción | Descripción | Ideal para | Coste |
|--------|-------------|------------|-------|
| **n8n Cloud (SaaS)** | Alojado por n8n, sin gestión de infraestructura | Equipos, producción rápida | Desde 20€/mes |
| **Self-hosted** | Despliegue en tu propio servidor (Docker, Kubernetes) | Control total, datos privados | Gratuito + infra |
| **Local (desarrollo)** | Ejecución en tu máquina con npx o Docker | Aprendizaje, desarrollo, pruebas | Gratuito |

```
┌──────────────────────────────────────────────────────────────┐
│              OPCIONES DE DESPLIEGUE DE n8n                     │
│                                                                │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│   │  n8n CLOUD   │  │ SELF-HOSTED  │  │    LOCAL     │        │
│   │              │  │              │  │              │        │
│   │  ☁ SaaS      │  │  🖥 Tu server │  │  💻 Tu PC    │        │
│   │  Gestionado  │  │  Docker      │  │  npx n8n    │        │
│   │  HTTPS auto  │  │  Control     │  │  Desarrollo │        │
│   │  Backups     │  │  total       │  │  Pruebas    │        │
│   │              │  │              │  │              │        │
│   │  20€/mes+    │  │  Gratuito    │  │  Gratuito   │        │
│   └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                                │
│   Producción          Producción          Desarrollo           │
│   rápida              con control         y aprendizaje        │
└──────────────────────────────────────────────────────────────┘
```

### 3.2 Instalación Local con npx

La forma más rápida de empezar con n8n es la instalación local usando **npx** (incluido con Node.js).

#### Requisitos Previos

- **Node.js 18+** instalado (https://nodejs.org)
- Verificar instalación: `node --version` (debe mostrar v18.x o superior)

#### Pasos de Instalación

```bash
# Paso 1: Verificar Node.js
node --version
# v18.17.0 o superior

# Paso 2: Ejecutar n8n con npx (descarga e inicia automáticamente)
npx n8n

# Paso 3: Abrir en el navegador
# http://localhost:5678
```

#### Primera Ejecución

```
┌──────────────────────────────────────────────────────────────┐
│              PRIMERA EJECUCIÓN DE n8n                          │
│                                                                │
│   Terminal:                                                    │
│   $ npx n8n                                                    │
│   ┌─────────────────────────────────────────────────────┐      │
│   │  n8n ready on 0.0.0.0, port 5678                    │      │
│   │  Version: 1.x.x                                     │      │
│   │  Editor: http://localhost:5678                       │      │
│   └─────────────────────────────────────────────────────┘      │
│                                                                │
│   Navegador → http://localhost:5678                             │
│   ┌─────────────────────────────────────────────────────┐      │
│   │  1. Crear cuenta de propietario (email + contraseña)│      │
│   │  2. Acceder al lienzo de workflows                  │      │
│   │  3. ¡Listo para crear tu primer workflow!            │      │
│   └─────────────────────────────────────────────────────┘      │
└──────────────────────────────────────────────────────────────┘
```

> **Nota**: Los datos se guardan en `~/.n8n/` por defecto (base de datos SQLite).

### 3.3 Despliegue en Koyeb desde GitHub

Para tener n8n accesible desde cualquier lugar (útil para webhooks y agentes en producción), podemos desplegarlo en **Koyeb**, una plataforma cloud con tier gratuito.

#### Pasos para el Despliegue

```
PASO 1: Fork del repositorio
────────────────────────────
- Ir a https://github.com/nickvidal/n8n-koyeb (o repositorio similar)
- Hacer fork a tu cuenta de GitHub

PASO 2: Crear cuenta en Koyeb
──────────────────────────────
- Ir a https://www.koyeb.com
- Registrarse (tier gratuito disponible)

PASO 3: Crear nuevo servicio
─────────────────────────────
- "Create App" → "GitHub"
- Seleccionar el repositorio forkeado
- Configurar:
  · Instance type: Free tier (nano)
  · Port: 5678
  · Variables de entorno:
    - N8N_BASIC_AUTH_ACTIVE=true
    - N8N_BASIC_AUTH_USER=tu_usuario
    - N8N_BASIC_AUTH_PASSWORD=tu_contraseña

PASO 4: Desplegar
──────────────────
- Koyeb construye y despliega automáticamente
- URL pública: https://tu-app-n8n.koyeb.app
```

```
┌──────────────────────────────────────────────────────────────┐
│              DESPLIEGUE EN KOYEB                               │
│                                                                │
│   GitHub (Fork)          Koyeb                  URL Pública    │
│   ┌──────────┐     ┌──────────────┐     ┌──────────────────┐  │
│   │ Repo n8n │────►│ Build auto   │────►│ https://tu-app   │  │
│   │ forkeado │     │ Deploy auto  │     │ .koyeb.app       │  │
│   └──────────┘     │ Free tier    │     │                  │  │
│                    └──────────────┘     │ n8n accesible    │  │
│                                        │ desde cualquier   │  │
│                                        │ lugar             │  │
│                                        └──────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

> **Ventaja**: Al tener una URL pública, puedes recibir webhooks de servicios externos (GitHub, Stripe, Telegram, etc.), algo que no es posible con la instalación local sin herramientas adicionales.

---

## Bloque 4: Arquitectura y Funcionamiento de n8n (40 minutos)

### 4.1 Conceptos Fundamentales: Workflows, Nodos y Conexiones

#### Workflow: La Receta de Cocina

Un **workflow** en n8n es como una **receta de cocina**: una secuencia ordenada de pasos que transforma ingredientes (datos de entrada) en un plato final (resultado deseado).

```
┌──────────────────────────────────────────────────────────────┐
│              ANALOGÍA: WORKFLOW = RECETA                       │
│                                                                │
│   Receta de cocina:                                            │
│   [Ingredientes] → [Picar] → [Cocinar] → [Emplatar] → [Plato]│
│                                                                │
│   Workflow de n8n:                                              │
│   [Trigger]  → [Procesar] → [Decidir] → [Actuar] → [Resultado]│
│                                                                │
│   Ejemplo: Notificación de emails importantes                  │
│   [Gmail     → [Filtrar   → [Resumir  → [Enviar  → [Registro  │
│    Trigger]     emails]      con IA]     Slack]     en Sheets] │
└──────────────────────────────────────────────────────────────┘
```

#### Nodo: La Unidad de Trabajo

Un **nodo** es la unidad mínima de trabajo en n8n. Cada nodo realiza una acción específica: leer datos, transformarlos, enviarlos a un servicio, tomar una decisión, etc.

| Propiedad del Nodo | Descripción |
|--------------------|-------------|
| **Nombre** | Identificador único en el workflow |
| **Tipo** | Categoría (trigger, acción, control de flujo) |
| **Parámetros** | Configuración específica (credenciales, campos, opciones) |
| **Entrada** | Datos que recibe del nodo anterior |
| **Salida** | Datos que envía al nodo siguiente |

#### Conexiones: Flujo de Datos y Orden de Ejecución

Las **conexiones** son las líneas que unen los nodos. Definen:
1. **El flujo de datos**: Qué datos pasan de un nodo a otro
2. **El orden de ejecución**: Qué nodo se ejecuta después de cuál

```
┌──────────────────────────────────────────────────────────────┐
│              ANATOMÍA DE UN WORKFLOW                            │
│                                                                │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌────────┐  │
│   │ TRIGGER  │───►│  NODO 1  │───►│  NODO 2  │───►│ NODO 3 │  │
│   │          │    │          │    │          │    │        │  │
│   │ "¿Cuándo │    │ "Obtener │    │ "Procesar│    │"Enviar │  │
│   │  empezar?"│    │  datos"  │    │  datos"  │    │resultado"│ │
│   └──────────┘    └──────────┘    └──────────┘    └────────┘  │
│       │                │                │              │       │
│       ▼                ▼                ▼              ▼       │
│   Evento que       Datos JSON       Datos JSON     Acción     │
│   inicia el        de entrada       transformados  final      │
│   workflow                                                     │
└──────────────────────────────────────────────────────────────┘
```

### 4.2 Tipos de Nodos

n8n organiza sus nodos en cuatro categorías principales:

#### Nodos Trigger (¿Cuándo se ejecuta el workflow?)

| Trigger | Descripción | Caso de uso |
|---------|-------------|-------------|
| **Manual Trigger** | Se ejecuta al pulsar "Test workflow" | Desarrollo y pruebas |
| **Schedule Trigger** | Se ejecuta en un horario definido (cron) | Informes diarios, limpieza periódica |
| **Webhook** | Se ejecuta cuando recibe una petición HTTP | Integraciones externas, APIs |
| **On App Event** | Se ejecuta ante un evento en una app | Nuevo email, nuevo registro en CRM |
| **Chat Trigger** | Se ejecuta al recibir un mensaje de chat | Chatbots, asistentes de IA |
| **Form Trigger** | Se ejecuta al enviar un formulario web | Recogida de datos, encuestas |

#### Nodos de Acción (¿Qué hace el workflow?)

| Acción | Descripción |
|--------|-------------|
| **Gmail** | Leer, enviar, buscar emails |
| **Google Sheets** | Leer, escribir, actualizar hojas de cálculo |
| **HTTP Request** | Llamar a cualquier API REST |
| **Slack** | Enviar mensajes, crear canales |
| **OpenAI** | Generar texto, embeddings, imágenes |
| **Postgres/MySQL** | Consultar y modificar bases de datos |

#### Nodos de Control de Flujo (¿Cómo fluyen los datos?)

| Nodo | Descripción | Ejemplo |
|------|-------------|---------|
| **IF** | Bifurcación condicional (verdadero/falso) | Si el email es urgente → ruta A, si no → ruta B |
| **Switch** | Múltiples rutas según un valor | Según el departamento: ventas, soporte, RRHH |
| **Merge** | Combina datos de múltiples ramas | Unir resultados de dos APIs |
| **Loop Over Items** | Itera sobre una lista de elementos | Procesar cada fila de una hoja de cálculo |
| **Wait** | Pausa la ejecución un tiempo determinado | Esperar 5 segundos entre llamadas a API |
| **Filter** | Filtra elementos según condiciones | Mantener solo emails con adjuntos |

#### Nodos de Transformación (¿Cómo se procesan los datos?)

| Nodo | Descripción |
|------|-------------|
| **Set** | Crear o modificar campos de datos |
| **Code** | Ejecutar JavaScript o Python personalizado |
| **Split Out** | Dividir un array en elementos individuales |
| **Aggregate** | Combinar múltiples elementos en uno solo |

```
┌──────────────────────────────────────────────────────────────┐
│              TIPOS DE NODOS EN n8n                              │
│                                                                │
│   TRIGGERS           ACCIONES          CONTROL         TRANSF. │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌─────────┐  │
│  │ Manual   │    │ Gmail    │    │ IF       │    │ Set     │  │
│  │ Schedule │    │ Sheets   │    │ Switch   │    │ Code    │  │
│  │ Webhook  │    │ HTTP Req │    │ Merge    │    │ Split   │  │
│  │ App Event│    │ Slack    │    │ Loop     │    │ Aggr.   │  │
│  │ Chat     │    │ OpenAI   │    │ Wait     │    │         │  │
│  │ Form     │    │ Postgres │    │ Filter   │    │         │  │
│  └──────────┘    └──────────┘    └──────────┘    └─────────┘  │
│                                                                │
│  "¿Cuándo?"     "¿Qué hacer?"   "¿Cómo fluir?"  "¿Cómo       │
│                                                   transformar?"│
└──────────────────────────────────────────────────────────────┘
```

### 4.3 El Lienzo Visual: Navegación y Organización

El **lienzo** (canvas) es el espacio de trabajo donde se diseñan los workflows. Funciones principales:

- **Arrastrar y soltar**: Añadir nodos desde el panel lateral
- **Conectar**: Arrastrar desde la salida de un nodo hasta la entrada de otro
- **Zoom**: Acercar/alejar para ver el panorama completo
- **Notas**: Añadir notas adhesivas para documentar el workflow
- **Agrupar**: Organizar nodos relacionados visualmente
- **Minimap**: Vista en miniatura del workflow completo

#### Buenas Prácticas de Organización

1. **Flujo de izquierda a derecha**: Trigger a la izquierda, resultado a la derecha
2. **Nombres descriptivos**: Renombrar nodos con nombres claros ("Filtrar emails urgentes" en vez de "IF")
3. **Notas adhesivas**: Documentar bloques lógicos del workflow
4. **Colores**: Usar colores para distinguir secciones (disponible en notas)

### 4.4 Gestión de Credenciales y Conexiones Externas

Para conectar n8n con servicios externos, necesitamos configurar **credenciales**. n8n soporta tres tipos principales:

| Tipo de Autenticación | Descripción | Servicios Típicos |
|----------------------|-------------|-------------------|
| **API Key** | Clave secreta proporcionada por el servicio | OpenAI, Anthropic, Pinecone, Telegram |
| **OAuth2** | Flujo de autorización con consentimiento del usuario | Google (Gmail, Sheets, Drive), Microsoft |
| **Basic Auth** | Usuario y contraseña | APIs internas, servicios legacy |

#### Ejemplo: Configurar API Key de OpenAI

```
PASOS:
1. En n8n: Settings → Credentials → Add Credential
2. Buscar "OpenAI"
3. Pegar tu API Key (obtener en https://platform.openai.com/api-keys)
4. Guardar

La credencial queda disponible para todos los nodos de OpenAI.
```

#### Ejemplo: Configurar OAuth2 para Google (Gmail, Sheets, Drive)

```
PASO 1: Crear proyecto en Google Cloud Console
─────────────────────────────────────────────
- Ir a https://console.cloud.google.com
- Crear nuevo proyecto
- Habilitar APIs necesarias (Gmail API, Google Sheets API, Google Drive API)

PASO 2: Crear credenciales OAuth2
──────────────────────────────────
- APIs & Services → Credentials → Create Credentials → OAuth Client ID
- Application type: Web Application
- Authorized redirect URI: http://localhost:5678/rest/oauth2-credential/callback
  (o tu URL de n8n en producción)

PASO 3: Configurar en n8n
──────────────────────────
- Settings → Credentials → Add Credential → Google OAuth2
- Client ID: (del paso 2)
- Client Secret: (del paso 2)
- Pulsar "Connect" → Autorizar en ventana de Google

PASO 4: Usar en nodos
──────────────────────
- Al añadir un nodo de Google (Gmail, Sheets...), seleccionar la credencial creada
```

### 4.5 Importar y Exportar Workflows (JSON)

Los workflows de n8n se almacenan como **archivos JSON**, lo que permite:

- **Compartir** workflows con otros usuarios
- **Versionar** workflows en Git
- **Migrar** entre instancias de n8n
- **Usar templates** de la comunidad (https://n8n.io/workflows)

```
EXPORTAR:
─────────
- En el editor → menú "..." → "Download"
- Se descarga un archivo .json con toda la configuración

IMPORTAR:
─────────
- En el dashboard → "Add Workflow" → "Import from File"
- Seleccionar el archivo .json
- Configurar credenciales (no se exportan por seguridad)
```

```json
// Ejemplo simplificado de workflow JSON
{
  "name": "Mi Workflow de Ejemplo",
  "nodes": [
    {
      "name": "Manual Trigger",
      "type": "n8n-nodes-base.manualTrigger",
      "position": [250, 300]
    },
    {
      "name": "HTTP Request",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://api.ejemplo.com/datos",
        "method": "GET"
      },
      "position": [450, 300]
    }
  ],
  "connections": {
    "Manual Trigger": {
      "main": [
        [{ "node": "HTTP Request", "type": "main", "index": 0 }]
      ]
    }
  }
}
```

---

### --- DESCANSO (15 minutos) ---

---

## Bloque 5: Automatización de Procesos con n8n (45 minutos)

### 5.1 Triggers: Manual, Schedule, Webhook, Form Submission

Cada tipo de trigger tiene una configuración específica. Veamos los más importantes en detalle:

#### Manual Trigger

El más simple. Se ejecuta al pulsar "Test workflow" en el editor. Ideal para desarrollo y pruebas.

```
┌──────────────┐
│   Manual     │───► [resto del workflow]
│   Trigger    │
│              │
│ Botón "Test" │
└──────────────┘
```

#### Schedule Trigger

Ejecuta el workflow en un horario definido. Usa expresiones **cron** o configuración visual.

```
Ejemplos de Schedule:
─────────────────────
- Cada 5 minutos:    */5 * * * *
- Cada hora:         0 * * * *
- Cada día a las 9:  0 9 * * *
- Lunes a viernes:   0 9 * * 1-5
- Primer día del mes: 0 0 1 * *

En n8n (configuración visual):
┌──────────────────────────────────────┐
│ Trigger Rule:                         │
│ ├── Interval: Every 1 day            │
│ ├── At hour: 9                       │
│ └── At minute: 0                     │
│                                       │
│ → Se ejecuta cada día a las 09:00    │
└──────────────────────────────────────┘
```

#### Webhook Trigger

Crea un endpoint HTTP que activa el workflow cuando recibe una petición. Esencial para integraciones.

```
Configuración del Webhook:
──────────────────────────
- HTTP Method: GET, POST, PUT, DELETE
- Path: /mi-webhook (genera URL completa automáticamente)
- Authentication: None, Basic Auth, Header Auth
- Response: Immediately, When Last Node Finishes

URL generada (local):
  http://localhost:5678/webhook/mi-webhook

URL generada (producción):
  https://tu-app.koyeb.app/webhook/mi-webhook
```

```
┌──────────────────────────────────────────────────────────────┐
│              WEBHOOK TRIGGER                                    │
│                                                                │
│   Servicio externo                    n8n                      │
│   ┌──────────────┐              ┌──────────────┐               │
│   │  GitHub      │              │  Webhook     │               │
│   │  (push event)│──── POST ───►│  Trigger     │──►[workflow]  │
│   │              │   /webhook/  │              │               │
│   │  Stripe     │   github     │  Recibe JSON │               │
│   │  (payment)  │              │  del body    │               │
│   └──────────────┘              └──────────────┘               │
└──────────────────────────────────────────────────────────────┘
```

#### Form Trigger

Genera un formulario web automáticamente. Útil para recoger datos de usuarios sin crear una interfaz.

```
Configuración del Form:
───────────────────────
- Form Title: "Solicitud de soporte"
- Form Description: "Completa el formulario..."
- Form Fields:
  ├── Nombre (text, required)
  ├── Email (email, required)
  ├── Departamento (dropdown: Ventas, Soporte, RRHH)
  └── Descripción del problema (textarea)

→ n8n genera automáticamente una página web con el formulario
→ Al enviar, se activa el workflow con los datos del formulario
```

### 5.2 Ejemplos Prácticos de Automatización

#### Ejemplo 1: Workflow de Notificación de Emails

```
┌──────────────────────────────────────────────────────────────┐
│  WORKFLOW: NOTIFICACIÓN DE EMAILS IMPORTANTES                  │
│                                                                │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   │
│  │  Gmail   │──►│  Filter  │──►│  OpenAI  │──►│  Slack   │   │
│  │  Trigger │   │          │   │          │   │          │   │
│  │          │   │ Subject  │   │ "Resume  │   │ Enviar   │   │
│  │ Nuevos   │   │ contains │   │  este    │   │ resumen  │   │
│  │ emails   │   │ "urgente"│   │  email"  │   │ a #alerts│   │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘   │
│                                                                │
│  Trigger:  Cada nuevo email en la bandeja de entrada           │
│  Filtro:   Solo emails con "urgente" en el asunto              │
│  IA:       GPT-4 resume el contenido en 2-3 líneas            │
│  Acción:   Envía el resumen al canal #alertas de Slack        │
└──────────────────────────────────────────────────────────────┘
```

**Configuración paso a paso:**

1. **Gmail Trigger**: Evento = "Message Received", Label = "INBOX"
2. **Filter**: Condición = `{{ $json.subject }}` contiene "urgente"
3. **OpenAI**: Model = "gpt-4", Prompt = "Resume en 2-3 líneas este email: {{ $json.body }}"
4. **Slack**: Channel = "#alertas", Message = "Email urgente de {{ $json.from }}: {{ $node['OpenAI'].json.text }}"

#### Ejemplo 2: Automatización de Datos con Google Sheets

```
┌──────────────────────────────────────────────────────────────┐
│  WORKFLOW: REGISTRO AUTOMÁTICO EN GOOGLE SHEETS                │
│                                                                │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   │
│  │  Form    │──►│  Set     │──►│  Google  │──►│  Gmail   │   │
│  │  Trigger │   │          │   │  Sheets  │   │          │   │
│  │          │   │ Añadir   │   │          │   │ Enviar   │   │
│  │ Formulario│   │ fecha y  │   │ Append   │   │ confirm. │   │
│  │ de alta  │   │ ID único │   │ Row      │   │ al user  │   │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘   │
│                                                                │
│  Trigger:  Usuario envía formulario de alta                    │
│  Set:      Añade timestamp e ID único a los datos              │
│  Sheets:   Inserta nueva fila con todos los datos              │
│  Gmail:    Envía email de confirmación al usuario              │
└──────────────────────────────────────────────────────────────┘
```

### 5.3 Flujo de Datos entre Nodos: Expresiones y Variables

En n8n, los datos fluyen entre nodos como **objetos JSON**. Para acceder a los datos de nodos anteriores, se utilizan **expresiones**.

#### Sintaxis de Expresiones

| Expresión | Descripción | Ejemplo |
|-----------|-------------|---------|
| `{{ $json.campo }}` | Acceder a un campo del nodo anterior | `{{ $json.email }}` → "usuario@ejemplo.com" |
| `{{ $node["nombre"].json.campo }}` | Acceder a un campo de un nodo específico | `{{ $node["Gmail Trigger"].json.subject }}` |
| `{{ $input.first().json.campo }}` | Primer elemento de la entrada | `{{ $input.first().json.name }}` |
| `{{ $now }}` | Fecha y hora actual | "2026-02-21T10:30:00.000Z" |
| `{{ $workflow.name }}` | Nombre del workflow actual | "Mi Workflow" |

#### Variables Especiales

| Variable | Descripción |
|----------|-------------|
| `$input` | Datos de entrada del nodo actual |
| `$json` | Atajo para `$input.item.json` (elemento actual en procesamiento) |
| `$binary` | Datos binarios adjuntos (archivos, imágenes) |
| `$node["nombre"]` | Referencia a los datos de salida de un nodo específico |
| `$now` | Fecha/hora actual (ISO 8601) |
| `$today` | Fecha actual sin hora |
| `$runIndex` | Número de ejecución actual (útil en loops) |
| `$itemIndex` | Índice del elemento actual en un array |
| `$workflow.id` | ID único del workflow |
| `$execution.id` | ID único de la ejecución actual |

#### Ejemplo Práctico de Expresiones

```
Supongamos que el nodo anterior (Gmail Trigger) devuelve:
{
  "from": "cliente@empresa.com",
  "subject": "Urgente: Problema con factura #1234",
  "body": "Hola, tengo un problema con la factura...",
  "date": "2026-02-21T10:00:00Z"
}

En el nodo siguiente, podemos usar:
─────────────────────────────────────
{{ $json.from }}           → "cliente@empresa.com"
{{ $json.subject }}        → "Urgente: Problema con factura #1234"
{{ $json.body.length }}    → 45 (longitud del texto)
{{ $json.date }}           → "2026-02-21T10:00:00Z"

Expresiones combinadas:
───────────────────────
"Email de {{ $json.from }} recibido el {{ $json.date }}"
→ "Email de cliente@empresa.com recibido el 2026-02-21T10:00:00Z"
```

#### Nodo Code: Cuando las Expresiones No Son Suficientes

Para transformaciones complejas, el nodo **Code** permite escribir JavaScript o Python:

```javascript
// Ejemplo en JavaScript (nodo Code)
// Procesar cada email y extraer información

for (const item of $input.all()) {
  const email = item.json;

  // Extraer número de factura del asunto
  const match = email.subject.match(/#(\d+)/);
  const invoiceNumber = match ? match[1] : 'N/A';

  // Clasificar prioridad
  const priority = email.subject.toLowerCase().includes('urgente')
    ? 'alta'
    : 'normal';

  // Añadir campos calculados
  item.json.invoiceNumber = invoiceNumber;
  item.json.priority = priority;
  item.json.processedAt = new Date().toISOString();
}

return $input.all();
```

---

## Resumen de la Sesión

### Conceptos Clave

1. **Agente de IA** es un sistema que percibe su entorno, toma decisiones y ejecuta acciones de forma autónoma, evolucionando desde el Function Calling de la Unidad 3 hacia sistemas con múltiples herramientas, memoria y encadenamiento autónomo.

2. **El paradigma PDA (Percepción-Decisión-Acción)** proporciona un marco de diseño universal para cualquier agente: qué recibe, cómo procesa y qué hace.

3. **n8n** es una plataforma open source de automatización visual con soporte nativo para agentes de IA, que destaca frente a alternativas como Zapier y Make por su flexibilidad, capacidad de self-hosting y nodo AI Agent integrado.

4. **La arquitectura de n8n** se basa en workflows (secuencias de pasos), nodos (unidades de trabajo) y conexiones (flujo de datos), organizados en categorías de triggers, acciones, control de flujo y transformación.

5. **Las credenciales** en n8n (API Key, OAuth2, Basic Auth) permiten conectar con servicios externos de forma segura, y los workflows se almacenan como JSON para facilitar su portabilidad y versionado.

6. **Las expresiones y variables** (`{{ $json.campo }}`, `$node["nombre"]`, `$now`) permiten que los datos fluyan dinámicamente entre nodos, mientras que el nodo Code ofrece la potencia de JavaScript y Python para transformaciones complejas.

---

## Conexión con la Sesión 2

En la próxima sesión abordaremos la construcción de agentes de IA completos en n8n:

- **Nodo AI Agent**: Configuración del agente con LLM, herramientas y memoria
- **Herramientas del agente**: Conectar Gmail, Google Sheets, HTTP Request como tools
- **Memoria del agente**: Buffer, ventana y resumen para conversaciones persistentes
- **Agente RAG**: Integración con bases de datos vectoriales (conexión con Unidad 5)
- **Canales de entrada**: Chat embebido, Telegram, Slack, WhatsApp
- **Proyecto integrador**: Agente de IA funcional con múltiples herramientas

---

## Conexiones con Otras Unidades

```
┌──────────────────────────────────────────────────────────────┐
│              MAPA DE CONEXIONES DEL CURSO                      │
│                                                                │
│   Unidad 3: APIs y Function Calling                            │
│        │                                                       │
│        ▼  Function Calling es la BASE de los agentes           │
│                                                                │
│   Unidad 4: Agentes de IA y n8n  ← ESTAMOS AQUÍ               │
│        │                                                       │
│        ├──► Unidad 5: RAG (extensión de agentes con            │
│        │    conocimiento externo mediante vectores)             │
│        │                                                       │
│        └──► Unidad 6: MCP (estándar para definir               │
│             herramientas que usan los agentes)                  │
└──────────────────────────────────────────────────────────────┘
```

---

## Actividades

### Ejercicios de esta Sesión

Completa los ejercicios prácticos disponibles en [ejercicios.md](./ejercicios.md):

1. **Diseño de un agente con PDA** - Definir percepción, decisión y acción para un caso de uso
2. **Instalación de n8n** - Instalar y ejecutar n8n localmente con npx
3. **Primer workflow** - Crear un workflow con Manual Trigger + Set + resultado
4. **Workflow con webhook** - Configurar un webhook que reciba datos y los procese
5. **Expresiones y variables** - Practicar el uso de expresiones para transformar datos entre nodos

### Práctica Evaluable de la Unidad

Al finalizar ambas sesiones, completa la [práctica evaluable](../practica.md) de la Unidad 4.

---

## Referencias

- n8n Documentation. *Getting Started*. https://docs.n8n.io/
- n8n Documentation. *AI Agents*. https://docs.n8n.io/advanced-ai/
- n8n Workflow Templates. https://n8n.io/workflows
- Repositorio de código del curso. https://github.com/rpmaya/ml2_code/
- OpenAI. *Function Calling Guide*. https://platform.openai.com/docs/guides/function-calling
- Anthropic. *Tool Use (Claude)*. https://docs.anthropic.com/en/docs/build-with-claude/tool-use
- Koyeb Documentation. *Deploy n8n*. https://www.koyeb.com/docs
- Wang, L., Ma, C., Feng, X., et al. (2024). *A Survey on Large Language Model based Autonomous Agents*. Frontiers of Computer Science.
- Weng, L. (2023). *LLM Powered Autonomous Agents*. Lil'Log. https://lilianweng.github.io/posts/2023-06-23-agent/
