# Unidad 5 - Sesión 2: Implementación y Optimización de Sistemas RAG

## Objetivos de la Sesión

Al finalizar esta sesión, el estudiante será capaz de:
- Comprender el pipeline RAG completo desde la ingesta de documentos hasta la generación de respuestas
- Implementar búsqueda híbrida combinando búsqueda vectorial y léxica (BM25)
- Configurar Pinecone como vector store en la nube y construir workflows RAG en n8n
- Desarrollar sistemas RAG completos con LangChain en Python usando diferentes vector stores
- Aplicar patrones avanzados: RAG conversacional, query expansion y HyDE
- Evaluar la calidad de un sistema RAG utilizando el framework RAGAS
- Diseñar soluciones RAG para casos de uso reales en producción

---

## Bloque 1: Pipeline RAG Completo

### 5.5 Uniendo Todas las Piezas

En la sesión anterior estudiamos cada componente de forma individual: documentos, chunking, embeddings y vector stores. Ahora es el momento de ensamblar todas las piezas en un pipeline funcional de extremo a extremo.

Un sistema RAG se compone de dos fases claramente diferenciadas: la **fase de indexación** (offline, se ejecuta una vez o periódicamente) y la **fase de consulta** (online, se ejecuta en cada pregunta del usuario).

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PIPELINE RAG COMPLETO                                │
│                                                                         │
│  ╔═══════════════════════════════════════════════════════════════════╗  │
│  ║  FASE 1: INDEXACIÓN (Offline)                                     ║  │
│  ║                                                                   ║  │
│  ║  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────────┐    ║  │
│  ║  │Documentos│──►│ Chunking │──►│Embeddings│──►│ Vector Store │    ║  │
│  ║  │ PDF, TXT │   │ Split en │   │ Texto →  │   │ Pinecone,    │    ║  │
│  ║  │ CSV, Web │   │ fragmentos│  │ Vector   │   │ Chroma, FAISS│    ║  │
│  ║  └──────────┘   └──────────┘   └──────────┘   └──────────────┘    ║  │
│  ╚═══════════════════════════════════════════════════════════════════╝  │
│                                                                         │
│  ╔═══════════════════════════════════════════════════════════════════╗  │
│  ║  FASE 2: CONSULTA (Online)                                        ║  │
│  ║                                                                   ║  │
│  ║  ┌────────┐  ┌─────────┐  ┌──────────┐  ┌─────────┐  ┌────────┐   ║  │
│  ║  │Pregunta│─►│Embedding│─►│ Búsqueda │─►│ Prompt  │─►│  LLM   │   ║  │
│  ║  │usuario │  │consulta │  │ vectorial│  │+contexto│  │responde│   ║  │
│  ║  └────────┘  └─────────┘  └──────────┘  └─────────┘  └────────┘.  ║  │
│  ║                               │                                   ║  │
│  ║                        Top-K chunks                               ║  │
│  ║                        relevantes                                 ║  │
│  ╚═══════════════════════════════════════════════════════════════════╝  │
└─────────────────────────────────────────────────────────────────────────┘
```

### Fase 1: Indexación

La fase de indexación prepara los documentos para que puedan ser consultados de forma eficiente. Se ejecuta cada vez que se añaden o actualizan documentos en la base de conocimiento.

```
PASO A PASO DE LA INDEXACIÓN:

1. CARGA DE DOCUMENTOS
   ┌──────────────────────────────────────────────┐
   │ Fuentes soportadas:                          │
   │  - Archivos locales: PDF, TXT, DOCX, CSV     │
   │  - APIs: Notion, Confluence, Google Drive    │
   │  - Web: URLs, sitemaps, crawlers             │
   │  - Bases de datos: SQL, MongoDB              │
   └──────────────────────────────────────────────┘

2. PREPROCESAMIENTO
   ┌──────────────────────────────────────────────┐
   │ - Limpieza de texto (HTML, caracteres raros) │
   │ - Extracción de metadatos (título, fecha,    │
   │   autor, sección)                            │
   │ - Normalización de formato                   │
   └──────────────────────────────────────────────┘

3. CHUNKING (División en fragmentos)
   ┌──────────────────────────────────────────────┐
   │ - Tamaño de chunk: 200-1000 tokens           │
   │ - Overlap: 10-20% del tamaño del chunk       │
   │ - Estrategia: RecursiveCharacterTextSplitter │
   │ - Cada chunk conserva sus metadatos          │
   └──────────────────────────────────────────────┘

4. GENERACIÓN DE EMBEDDINGS
   ┌──────────────────────────────────────────────┐
   │ - Modelo: text-embedding-3-small (1536 dims) │
   │ - Cada chunk → vector de 1536 dimensiones    │
   │ - Batch processing para eficiencia           │
   └──────────────────────────────────────────────┘

5. ALMACENAMIENTO EN VECTOR STORE
   ┌──────────────────────────────────────────────┐
   │ - Vector + texto original + metadatos        │
   │ - Indexación para búsqueda rápida            │
   │ - Namespaces/colecciones para organización   │
   └──────────────────────────────────────────────┘
```

### Fase 2: Consulta

La fase de consulta se ejecuta cada vez que un usuario hace una pregunta. El sistema busca los fragmentos más relevantes y los utiliza como contexto para generar la respuesta.

```
FLUJO DETALLADO DE CONSULTA:

Usuario: "¿Cuál es la política de devoluciones para productos electrónicos?"
                    │
                    ▼
            ┌───────────────┐
            │  1. Embedding │  Convertir pregunta a vector
            │  de consulta  │  [0.023, -0.041, 0.087, ...]
            └──────┬────────┘
                   │
                   ▼
            ┌───────────────┐
            │  2. Búsqueda  │  Similitud coseno con todos
            │  vectorial    │  los chunks indexados
            │  (Top-K = 4)  │
            └──────┬────────┘
                   │
                   ▼
        ┌───────────────────────┐
        │  3. Chunks relevantes │
        │                       │
        │  [0.92] "Las devoluciones de productos electrónicos    │
        │         deben realizarse en un plazo de 30 días..."    │
        │  [0.87] "Para iniciar una devolución, el cliente       │
        │         debe presentar el ticket de compra..."         │
        │  [0.81] "Los productos electrónicos defectuosos        │
        │         se reemplazan sin coste adicional..."          │
        │  [0.74] "Excepciones: software abierto, productos      │
        │         personalizados no son retornables..."          │
        └──────────┬────────────┘
                   │
                   ▼
        ┌───────────────────────┐
        │  4. Construcción      │
        │  del prompt           │
        │                       │
        │  Sistema: "Eres un asistente de atención al cliente.  │
        │  Responde basándote ÚNICAMENTE en el contexto."       │
        │                                                       │
        │  Contexto: [chunks recuperados]                       │
        │                                                       │
        │  Pregunta: "¿Cuál es la política de devoluciones      │
        │  para productos electrónicos?"                        │
        └──────────┬───────────┘
                   │
                   ▼
        ┌───────────────────────┐
        │  5. LLM genera        │
        │  respuesta            │
        │                       │
        │  "Los productos electrónicos pueden devolverse en     │
        │   un plazo de 30 días con el ticket de compra.        │
        │   Los productos defectuosos se reemplazan sin         │
        │   coste. Excepciones: software abierto y productos    │
        │   personalizados."                                    │
        └───────────────────────┘
```

### Búsqueda Híbrida: Vectorial + BM25

La búsqueda puramente vectorial (semántica) tiene una limitación importante: puede fallar con términos muy específicos como nombres propios, códigos de producto, IDs o siglas técnicas. La **búsqueda híbrida** combina lo mejor de ambos mundos.

```
┌─────────────────────────────────────────────────────────────────┐
│                    BÚSQUEDA HÍBRIDA                             │
│                                                                 │
│  Consulta: "Error ERR-4502 en módulo de facturación"            │
│                   │                                             │
│          ┌────────┴────────┐                                    │
│          │                 │                                    │
│          ▼                 ▼                                    │
│  ┌───────────────┐  ┌──────────────┐                            │
│  │  Búsqueda     │  │  Búsqueda    │                            │
│  │  VECTORIAL    │  │  LÉXICA      │                            │
│  │  (Semántica)  │  │  (BM25)      │                            │
│  │               │  │              │                            │
│  │  Encuentra    │  │  Encuentra   │                            │
│  │  documentos   │  │  documentos  │                            │
│  │  sobre errores│  │  con texto   │                            │
│  │  y facturación│  │  "ERR-4502"  │                            │
│  └──────┬────────┘  └──────┬───────┘                            │
│         │                  │                                    │
│         └────────┬─────────┘                                    │
│                  ▼                                              │
│         ┌───────────────┐                                       │
│         │  Reciprocal   │  Fusiona rankings de ambas            │
│         │  Rank Fusion  │  búsquedas con pesos                  │
│         │  (RRF)        │  configurables                        │
│         └──────┬────────┘                                       │
│                ▼                                                │
│         Resultados combinados                                   │
│         (lo mejor de ambos)                                     │
└─────────────────────────────────────────────────────────────────┘
```

**¿Cuándo usar búsqueda híbrida?**

| Escenario | Solo Vectorial | Híbrida | Recomendación |
|-----------|---------------|---------|---------------|
| Preguntas conceptuales generales | Excelente | Buena | Vectorial |
| Búsqueda por código/ID exacto | Mala | Excelente | **Híbrida** |
| Nombres propios y siglas | Regular | Excelente | **Híbrida** |
| Documentación técnica con jerga | Regular | Excelente | **Híbrida** |
| Consultas en lenguaje natural | Excelente | Buena | Vectorial |
| Base de conocimiento heterogénea | Buena | Excelente | **Híbrida** |

> **Nota**: Pinecone soporta búsqueda híbrida de forma nativa con sparse vectors (BM25) + dense vectors (embeddings semánticos). En LangChain se puede implementar con `EnsembleRetriever`.

### Evaluación de Calidad del Sistema RAG

Un sistema RAG en producción necesita métricas objetivas para medir su rendimiento. El framework **RAGAS** (Retrieval Augmented Generation Assessment) proporciona métricas estándar.

```
┌─────────────────────────────────────────────────────────────────┐
│                    MÉTRICAS RAGAS                               │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ 1. Context Precision (Precisión del contexto)             │  │
│  │    ¿Los chunks recuperados son relevantes para la         │  │
│  │    pregunta? ¿Hay ruido innecesario?                      │  │
│  │    Ideal: > 0.85                                          │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ 2. Context Recall (Cobertura del contexto)                │  │
│  │    ¿Se recuperaron TODOS los chunks necesarios para       │  │
│  │    responder correctamente?                               │  │
│  │    Ideal: > 0.80                                          │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ 3. Faithfulness (Fidelidad)                               │  │
│  │    ¿La respuesta se basa SOLO en el contexto              │  │
│  │    recuperado? ¿Hay alucinaciones?                        │  │
│  │    Ideal: > 0.90                                          │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ 4. Answer Relevancy (Relevancia de la respuesta)          │  │
│  │    ¿La respuesta es pertinente y directa respecto         │  │
│  │    a la pregunta formulada?                               │  │
│  │    Ideal: > 0.85                                          │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

Puntuación global = Media ponderada de las 4 métricas
```

#### Ejemplo de Evaluación con RAGAS

```python
from ragas import evaluate
from ragas.metrics import (
    context_precision,
    context_recall,
    faithfulness,
    answer_relevancy,
)
from datasets import Dataset

# Datos de evaluación: preguntas, respuestas generadas,
# contextos recuperados y respuestas de referencia (ground truth)
eval_data = {
    "question": [
        "¿Cuál es la política de devoluciones?",
        "¿Cómo contactar con soporte técnico?",
    ],
    "answer": [
        "Las devoluciones se aceptan en 30 días con ticket.",
        "Puede contactar al 900-123-456 o email soporte@empresa.com.",
    ],
    "contexts": [
        ["Política: devoluciones en 30 días con ticket de compra original."],
        ["Soporte: teléfono 900-123-456, email soporte@empresa.com, horario 9-18h."],
    ],
    "ground_truth": [
        "Las devoluciones deben realizarse en un plazo de 30 días presentando el ticket.",
        "Soporte técnico disponible en 900-123-456 y soporte@empresa.com de 9 a 18h.",
    ],
}

dataset = Dataset.from_dict(eval_data)

# Ejecutar evaluación
results = evaluate(
    dataset,
    metrics=[context_precision, context_recall, faithfulness, answer_relevancy],
)

print(results)
# {'context_precision': 0.95, 'context_recall': 0.88,
#  'faithfulness': 0.92, 'answer_relevancy': 0.90}
```

> **Buena práctica**: Crea un dataset de evaluación con al menos 50-100 preguntas representativas y sus respuestas esperadas. Ejecuta RAGAS periódicamente para detectar degradación del sistema.

---

## Bloque 2: Implementación con Pinecone y n8n

### 5.6 Pinecone como Vector Store en la Nube

Pinecone es un servicio de base de datos vectorial gestionada (managed) que elimina la complejidad de mantener infraestructura propia. Es ideal para producción por su escalabilidad, disponibilidad y rendimiento.

### Configuración Inicial de Pinecone

```
PASO A PASO: CREAR CUENTA Y PRIMER ÍNDICE EN PINECONE

1. CREAR CUENTA
   ┌────────────────────────────────────────────┐
   │ https://www.pinecone.io/                   │
   │ → Sign Up (plan gratuito: Starter)         │
   │ → Verificar email                          │
   │ → Dashboard disponible                     │
   └────────────────────────────────────────────┘

2. OBTENER API KEY
   ┌────────────────────────────────────────────┐
   │ Dashboard → API Keys                       │
   │ → Copiar la API Key generada               │
   │ → Ejemplo: pcsk_xxxxxx...                  │
   │                                            │
   │ ⚠ Guardarla de forma segura                │
   │   (no compartir, no subir a Git)           │
   └────────────────────────────────────────────┘

3. CREAR ÍNDICE
   ┌────────────────────────────────────────────┐
   │ Dashboard → Indexes → Create Index         │
   │                                            │
   │ Configuración:                             │
   │  - Name: "ml2-knowledge-base"              │
   │  - Dimensions: 1536                        │
   │  - Metric: cosine                          │
   │  - Type: Serverless                        │
   │  - Cloud: AWS                              │
   │  - Region: us-east-1                       │
   │                                            │
   │ → Create Index                             │
   └────────────────────────────────────────────┘
```

> **Importante**: Las dimensiones del índice (1536) deben coincidir exactamente con las dimensiones del modelo de embeddings que se va a utilizar. Para `text-embedding-3-small` de OpenAI, las dimensiones son 1536. Si se usa otro modelo, hay que ajustar este valor.

#### Conceptos Clave de Pinecone

```
┌─────────────────────────────────────────────────────────────────┐
│                ESTRUCTURA DE PINECONE                           │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ ÍNDICE: "ml2-knowledge-base"                              │  │
│  │ (Equivalente a una "base de datos")                       │  │
│  │                                                           │  │
│  │  ┌──────────────────┐  ┌──────────────────┐               │  │
│  │  │ Namespace:       │  │ Namespace:       │               │  │
│  │  │ "rrhh"           │  │ "ventas"         │               │  │
│  │  │                  │  │                  │               │  │
│  │  │ ┌──────────────┐ │  │ ┌──────────────┐ │               │  │
│  │  │ │ Vector 1     │ │  │ │ Vector 1     │ │               │  │
│  │  │ │ id: "doc1_c1"│ │  │ │ id: "cat_01" │ │               │  │
│  │  │ │ values: [...]│ │  │ │ values: [...]│ │               │  │
│  │  │ │ metadata: {  │ │  │ │ metadata: {  │ │               │  │
│  │  │ │  source: ... │ │  │ │  producto: ..│ │               │  │
│  │  │ │  page: 1     │ │  │ │  precio: ... │ │               │  │
│  │  │ │ }            │ │  │ │ }            │ │               │  │
│  │  │ └──────────────┘ │  │ └──────────────┘ │               │  │
│  │  │ ┌──────────────┐ │  │ ┌──────────────┐ │               │  │
│  │  │ │ Vector 2     │ │  │ │ Vector 2     │ │               │  │
│  │  │ │ ...          │ │  │ │ ...          │ │               │  │
│  │  │ └──────────────┘ │  │ └──────────────┘ │               │  │
│  │  └──────────────────┘  └──────────────────┘               │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

Cada vector almacena:
- id: identificador único del chunk
- values: vector de embeddings (1536 dimensiones)
- metadata: información adicional (fuente, página, fecha, etc.)
```

**Namespaces**: Permiten organizar los vectores dentro de un mismo índice. Útiles para:
- Separar documentos por departamento (RRHH, Ventas, Legal)
- Mantener versiones diferentes del mismo contenido
- Aislar datos de diferentes clientes (multi-tenancy)
- Separar entornos (desarrollo vs producción)

### Workflow de Ingesta en n8n

El workflow de ingesta se encarga de procesar documentos nuevos y almacenarlos en Pinecone de forma automática. Se activa cada vez que se sube un archivo nuevo a Google Drive.

```
WORKFLOW DE INGESTA: Google Drive → Pinecone

┌───────────────┐     ┌──────────────┐     ┌────────────────────────────┐
│ Google Drive  │────►│ Download     │────►│ Pinecone Vector Store      │
│ Trigger       │     │ File         │     │ (Operation: Add Documents) │
│               │     │              │     │                            │
│ Evento:       │     │ Descarga el  │     │ ┌────────────────────────┐ │
│ "File Created"│     │ archivo como │     │ │ Document Loader:       │ │
│ en carpeta    │     │ binario      │     │ │ Binary (Default)       │ │
│ específica    │     │              │     │ │ Metadata: {{ $json.    │ │
│               │     │              │     │ │   name }} (filename)   │ │
└───────────────┘     └──────────────┘     │ └────────────────────────┘ │
                                           │                            │
                                           │ ┌────────────────────────┐ │
                                           │ │ Text Splitter:         │ │
                                           │ │ Token Splitter         │ │
                                           │ │ - Chunk Size: 200      │ │
                                           │ │ - Chunk Overlap: 20    │ │
                                           │ └────────────────────────┘ │
                                           │                            │
                                           │ ┌────────────────────────┐ │
                                           │ │ Embeddings:            │ │
                                           │ │ OpenAI Embeddings      │ │
                                           │ │ - Model: text-         │ │
                                           │ │   embedding-3-small    │ │
                                           │ │ - Dimensions: 1536     │ │
                                           │ └────────────────────────┘ │
                                           └────────────────────────────┘
```

#### Configuración Paso a Paso del Workflow de Ingesta

**Nodo 1: Google Drive Trigger**
```
┌────────────────────────────────────────────────┐
│ Google Drive Trigger                           │
│                                                │
│ Trigger On:        Changes involving a         │
│                    specific folder             │
│ Folder:            (seleccionar carpeta de     │
│                    documentos)                 │
│ Event:             File Created                │
│ Poll Times:        Every 5 minutes             │
│                                                │
│ Credenciales: Google Drive OAuth2              │
│                                                │
│ Output: { id, name, mimeType, ... }            │
└────────────────────────────────────────────────┘
```

**Nodo 2: Google Drive (Download File)**
```
┌────────────────────────────────────────────────┐
│ Google Drive                                   │
│                                                │
│ Operation:         Download                    │
│ File ID:           {{ $json.id }}              │
│                                                │
│ Output: archivo binario (PDF, TXT, etc.)       │
└────────────────────────────────────────────────┘
```

**Nodo 3: Pinecone Vector Store**
```
┌─────────────────────────────────────────────────┐
│ Pinecone Vector Store                           │
│                                                 │
│ Operation:         Add Documents                │
│ Pinecone Index:    ml2-knowledge-base           │
│ Namespace:         (opcional, ej: "docs")       │
│ Clear Namespace:   No (añadir, no reemplazar)   │
│                                                 │
│ Credenciales: Pinecone API                      │
│                                                 │
│ Subnodos conectados:                            │
│  ├── Document Loader: Default (Binary)          │
│  │   └── Metadata: filename = {{ $json.name }}  │
│  ├── Text Splitter: Token Splitter              │
│  │   ├── Chunk Size: 200                        │
│  │   └── Chunk Overlap: 20                      │
│  └── Embeddings: OpenAI Embeddings              │
│      ├── Model: text-embedding-3-small          │
│      └── Dimensions: 1536                       │
└─────────────────────────────────────────────────┘
```

#### Configuración de Credenciales de Pinecone en n8n

```
CREDENCIALES PINECONE EN n8n:

1. Settings → Credentials → Add New
2. Buscar: "Pinecone"
3. Tipo: Pinecone API
4. API Key: pcsk_xxxxxx... (copiada del dashboard de Pinecone)
5. Save → Test: Connection successful!
```

### Workflow del Agente RAG en n8n

Una vez que los documentos están indexados en Pinecone, construimos el agente que responde preguntas consultando esa base de conocimiento.

```
WORKFLOW DEL AGENTE RAG

┌───────────────┐     ┌────────────────────────────────────────────────┐
│ Chat Trigger  │────►│ AI Agent                                       │
│               │     │                                                │
│ (Interfaz de  │     │ ┌────────────────────────────────────────────┐ │
│  chat o       │     │ │ Chat Model:                                │ │
│  webhook)     │     │ │ OpenAI Chat Model                          │ │
│               │     │ │ - Model: gpt-4o-mini                       │ │
│               │     │ │ - Temperature: 0.3                         │ │
│               │     │ └────────────────────────────────────────────┘ │
│               │     │                                                │
│               │     │ ┌────────────────────────────────────────────┐ │
│               │     │ │ Memory:                                    │ │
│               │     │ │ Window Buffer Memory                       │ │
│               │     │ │ - Context Window Length: 10                │ │
│               │     │ └────────────────────────────────────────────┘ │
│               │     │                                                │
│               │     │ ┌────────────────────────────────────────────┐ │
│               │     │ │ Tool: Vector Store (Answer Questions)      │ │
│               │     │ │                                            │ │
│               │     │ │ Name: "knowledge_base"                     │ │
│               │     │ │ Description: "Consulta la base de          │ │
│               │     │ │  conocimiento de la empresa para           │ │
│               │     │ │  responder preguntas sobre políticas,      │ │
│               │     │ │  procedimientos y productos."              │ │
│               │     │ │                                            │ │
│               │     │ │ ┌──────────────────────┐                   │ │
│               │     │ │ │ Vector Store:        │                   │ │
│               │     │ │ │ Pinecone             │                   │ │
│               │     │ │ │ Index: ml2-kb        │                   │ │
│               │     │ │ │ Namespace: "docs"    │                   │ │
│               │     │ │ └──────────────────────┘                   │ │
│               │     │ │ ┌──────────────────────┐                   │ │
│               │     │ │ │ Embeddings:          │                   │ │
│               │     │ │ │ OpenAI Embeddings    │                   │ │
│               │     │ │ │ text-embedding-      │                   │ │
│               │     │ │ │ 3-small (1536)       │                   │ │
│               │     │ │ └──────────────────────┘                   │ │
│               │     │ └────────────────────────────────────────────┘ │
└───────────────┘     └────────────────────────────────────────────────┘
```

#### System Prompt del Agente RAG

El system prompt es fundamental para que el agente responda correctamente usando la base de conocimiento. Debe seguir la estructura **RTRF** (Rol, Tareas, Restricciones, Formato).

```
SYSTEM PROMPT RECOMENDADO:

# ROL
Eres un asistente experto de la empresa XYZ. Tu función es ayudar
a los usuarios respondiendo preguntas sobre nuestros productos,
políticas y procedimientos internos.

# TAREAS
- Responde preguntas consultando la base de conocimiento disponible
- Proporciona información precisa y actualizada
- Si la información no está en la base de conocimiento, indícalo
  claramente al usuario
- Ofrece referencias cuando sea posible (nombre del documento fuente)

# NOTAS Y RESTRICCIONES
- SOLO responde basándote en la información de la base de conocimiento
- NO inventes ni supongas información que no esté en los documentos
- Si no encuentras la respuesta, di: "No he encontrado esa información
  en nuestra base de conocimiento. Te recomiendo contactar con [canal]."
- Mantén un tono profesional y amable
- Responde en el mismo idioma que el usuario

# FORMATO
- Usa viñetas para listas
- Incluye la fuente del documento cuando sea relevante
- Mantén las respuestas concisas pero completas
```

#### Pruebas y Debugging

Una vez construido el workflow, es esencial verificar que funciona correctamente.

```
CHECKLIST DE VERIFICACIÓN:

1. VERIFICAR VECTORES EN PINECONE
   ┌──────────────────────────────────────────┐
   │ Dashboard de Pinecone → Índice           │
   │ → Stats: número de vectores > 0          │
   │ → Namespace correcto                     │
   │ → Dimensiones: 1536                      │
   └──────────────────────────────────────────┘

2. PROBAR BÚSQUEDA MANUALMENTE
   ┌──────────────────────────────────────────┐
   │ En el chat de n8n:                       │
   │ → Hacer preguntas sobre contenido        │
   │   que SÍ está en los documentos          │
   │ → Verificar que las respuestas           │
   │   coinciden con los documentos           │
   └──────────────────────────────────────────┘

3. ANALIZAR EJECUCIONES EN n8n
   ┌──────────────────────────────────────────┐
   │ Executions → Ver ejecución reciente      │
   │ → Revisar output de cada nodo            │
   │ → Verificar chunks recuperados           │
   │ → Comprobar prompt enviado al LLM        │
   └──────────────────────────────────────────┘

4. AJUSTAR SI ES NECESARIO
   ┌───────────────────────────────────────────┐
   │ Problemas comunes:                        │
   │ - Chunks muy grandes → reducir chunk_size │
   │ - Respuestas vagas → mejorar system prompt│
   │ - No encuentra info → verificar ingesta   │
   │ - Alucinaciones → reforzar restricciones  │
   └───────────────────────────────────────────┘
```
---

## Bloque 3: Implementación con LangChain en Python

### 5.7 RAG con LangChain

LangChain es el framework de referencia para construir aplicaciones con LLMs en Python. Proporciona abstracciones de alto nivel para cada componente del pipeline RAG, permitiendo implementar sistemas complejos con pocas líneas de código.

### Instalación y Configuración

```bash
# Instalar dependencias necesarias
pip install langchain langchain-openai langchain-community
pip install chromadb          # Vector store local
pip install faiss-cpu         # Vector store de alto rendimiento
pip install pinecone-client   # Vector store en la nube
pip install pypdf             # Carga de PDFs

# Configurar API Key (variable de entorno)
export OPENAI_API_KEY="sk-proj-xxxxxxxxxxxxxxxx" # Podéis usar la de OpenRouter (free)
```

```python
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Verificar que la API Key está configurada
assert os.getenv("OPENAI_API_KEY"), "Falta OPENAI_API_KEY en las variables de entorno"
```

### Document Loaders: Carga de Documentos

LangChain proporciona loaders para prácticamente cualquier fuente de datos. Cada loader retorna una lista de objetos `Document` con atributos `page_content` (texto) y `metadata` (información adicional).

```python
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    DirectoryLoader,
    CSVLoader,
    WebBaseLoader,
)

# ── Cargar un PDF ──────────────────────────────────────────────
loader = PyPDFLoader("documentos/manual_empresa.pdf")
docs = loader.load()
print(f"Páginas cargadas: {len(docs)}")
print(f"Contenido página 1: {docs[0].page_content[:200]}...")
print(f"Metadatos: {docs[0].metadata}")
# {'source': 'documentos/manual_empresa.pdf', 'page': 0}

# ── Cargar un archivo de texto ─────────────────────────────────
loader = TextLoader("documentos/faq.txt", encoding="utf-8")
docs = loader.load()

# ── Cargar todos los PDFs de un directorio ─────────────────────
loader = DirectoryLoader(
    "documentos/",
    glob="**/*.pdf",        # Patrón de archivos
    loader_cls=PyPDFLoader,  # Loader a usar para cada archivo
    show_progress=True,      # Barra de progreso
)
docs = loader.load()
print(f"Total documentos cargados: {len(docs)}")

# ── Cargar un CSV ──────────────────────────────────────────────
loader = CSVLoader(
    "datos/productos.csv",
    csv_args={"delimiter": ","},
    encoding="utf-8",
)
docs = loader.load()
# Cada fila del CSV es un Document

# ── Cargar una página web ──────────────────────────────────────
loader = WebBaseLoader("https://docs.empresa.com/politicas")
docs = loader.load()
```

### Pipeline de Ingesta Completo

El pipeline de ingesta toma documentos, los divide en chunks, genera embeddings y los almacena en un vector store. Aquí se muestra con tres vector stores diferentes.

```
PIPELINE DE INGESTA EN LANGCHAIN:

┌──────────────┐   ┌──────────────────────┐   ┌──────────────┐   ┌──────────┐
│ Directory    │──►│ Recursive Character  │──►│ OpenAI       │──►│ Vector   │
│ Loader       │   │ Text Splitter        │   │ Embeddings   │   │ Store    │
│              │   │                      │   │              │   │          │
│ glob: *.pdf  │   │ chunk_size: 500      │   │ text-        │   │ Chroma / │
│ loader_cls:  │   │ chunk_overlap: 50    │   │ embedding-   │   │ FAISS /  │
│ PyPDFLoader  │   │ separators:          │   │ 3-small      │   │ Pinecone │
│              │   │ ["\n\n","\n"," ",""] │   │              │   │          │
└──────────────┘   └──────────────────────┘   └──────────────┘   └──────────┘
```

#### Opción A: Chroma (Local, ideal para desarrollo)

Chroma es un vector store open-source que se ejecuta localmente. Perfecto para prototipado y desarrollo.

```python
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# 1. Cargar documentos
loader = DirectoryLoader("documentos/", glob="**/*.pdf", loader_cls=PyPDFLoader)
documents = loader.load()
print(f"Documentos cargados: {len(documents)}")

# 2. Dividir en chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""],
    length_function=len,
)
chunks = text_splitter.split_documents(documents)
print(f"Chunks generados: {len(chunks)}")

# 3. Crear vector store con Chroma (genera embeddings automáticamente)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db",  # Persistir en disco
    collection_name="knowledge_base",
)
print(f"Vectores almacenados en ./chroma_db")

# ── Cargar un vector store existente ───────────────────────────
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings,
    collection_name="knowledge_base",
)
```

#### Opción B: FAISS (Alto rendimiento)

FAISS (Facebook AI Similarity Search) es una librería optimizada para búsqueda de similitud a gran escala. Más rápida que Chroma para datasets grandes.

```python
from langchain_community.vectorstores import FAISS

# Crear vector store con FAISS
vectorstore = FAISS.from_documents(
    documents=chunks,
    embedding=embeddings,
)

# Guardar en disco
vectorstore.save_local("./faiss_index")

# Cargar desde disco
vectorstore = FAISS.load_local(
    "./faiss_index",
    embeddings,
    allow_dangerous_deserialization=True,  # Necesario desde LangChain 0.2
)
```

#### Opción C: Pinecone (Producción en la nube)

```python
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore

# Inicializar cliente de Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Crear vector store con Pinecone
vectorstore = PineconeVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
    index_name="ml2-knowledge-base",
    namespace="documentos",
)

# Conectar a un índice existente
vectorstore = PineconeVectorStore(
    index_name="ml2-knowledge-base",
    embedding=embeddings,
    namespace="documentos",
)
```

#### Comparativa de Vector Stores

| Característica | Chroma | FAISS | Pinecone |
|----------------|--------|-------|----------|
| **Tipo** | Local, open-source | Local, open-source | Cloud, managed |
| **Persistencia** | Disco local | Disco local | Cloud (siempre disponible) |
| **Rendimiento** | Bueno (< 100K docs) | Excelente (millones) | Excelente (escalable) |
| **Configuración** | Mínima | Mínima | Cuenta + API Key |
| **Coste** | Gratuito | Gratuito | Freemium (plan starter gratuito) |
| **Producción** | No recomendado | Posible con infra | Recomendado |
| **Filtros metadata** | Sí | Limitado | Sí (avanzados) |
| **Caso de uso** | Desarrollo y pruebas | Aplicaciones locales | Producción cloud |

### Construyendo la Cadena RAG (RetrievalQA)

Una vez que los documentos están indexados, construimos la cadena que conecta el retriever con el LLM para generar respuestas.

#### Método 1: LCEL (LangChain Expression Language) - Recomendado

LCEL es el método moderno y recomendado para construir cadenas en LangChain. Usa el operador `|` (pipe) para componer componentes de forma declarativa.

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 1. Crear el retriever a partir del vector store
retriever = vectorstore.as_retriever(
    search_type="similarity",  # o "mmr" para diversidad
    search_kwargs={"k": 4},    # recuperar 4 chunks
)

# 2. Función para formatear los documentos recuperados
def format_docs(docs):
    return "\n\n---\n\n".join(
        f"[Fuente: {doc.metadata.get('source', 'Desconocida')}]\n{doc.page_content}"
        for doc in docs
    )

# 3. Definir el prompt template
prompt = ChatPromptTemplate.from_template("""
Eres un asistente experto. Responde la pregunta basándote ÚNICAMENTE
en el contexto proporcionado. Si no encuentras la información en el
contexto, di "No tengo información suficiente para responder esa pregunta."

Contexto:
{context}

Pregunta: {question}

Respuesta:
""")

# 4. Crear el modelo LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

# 5. Construir la cadena con LCEL
rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough(),
    }
    | prompt
    | llm
    | StrOutputParser()
)

# 6. Ejecutar consulta
respuesta = rag_chain.invoke("¿Cuál es la política de devoluciones?")
print(respuesta)
```

```
FLUJO DE DATOS EN LA CADENA LCEL:

"¿Cuál es la política de devoluciones?"
           │
           ├───────────────────────────────────┐
           │                                   │
           ▼                                   ▼
   RunnablePassthrough()              retriever | format_docs
   (pasa la pregunta tal cual)        (busca y formatea chunks)
           │                                   │
           │    question                       │    context
           └──────────────┬────────────────────┘
                          │
                          ▼
                 ┌───────────────────┐
                 │ ChatPromptTemplate│
                 │ (combina context  │
                 │  + question)      │
                 └────────┬──────────┘
                          │
                          ▼
                 ┌───────────────────┐
                 │ ChatOpenAI        │
                 │ (gpt-4o-mini)     │
                 └────────┬──────────┘
                          │
                          ▼
                 ┌───────────────────┐
                 │ StrOutputParser   │
                 │ (extrae texto)    │
                 └────────┬──────────┘
                          │
                          ▼
                 "Los productos pueden
                  devolverse en 30 días..."
```

#### Método 2: RetrievalQA Chain (Legacy, pero más sencillo)

```python
from langchain.chains import RetrievalQA

qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.3),
    chain_type="stuff",  # Inserta todos los chunks en el prompt
    retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
    return_source_documents=True,  # Devolver las fuentes
)

result = qa_chain.invoke({"query": "¿Cuál es la política de devoluciones?"})
print(result["result"])
print(f"Fuentes: {[doc.metadata['source'] for doc in result['source_documents']]}")
```

### RAG Conversacional con Memoria

Para que el sistema RAG mantenga el contexto de la conversación (el usuario puede hacer preguntas de seguimiento como "¿Y en ese caso qué pasa?"), necesitamos añadir memoria.

```python
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory

# Crear memoria con ventana de 10 intercambios
memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="answer",
    k=10,
)

# Crear cadena conversacional
conv_chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.3),
    retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
    memory=memory,
    return_source_documents=True,
    verbose=True,
)

# Conversación con seguimiento
r1 = conv_chain.invoke({"question": "¿Cuál es la política de devoluciones?"})
print(r1["answer"])

r2 = conv_chain.invoke({"question": "¿Y para productos electrónicos?"})
print(r2["answer"])
# El sistema entiende que se refiere a devoluciones de productos electrónicos

r3 = conv_chain.invoke({"question": "¿Cuántos días tengo?"})
print(r3["answer"])
# Mantiene el contexto: "30 días para productos electrónicos"
```

```
FLUJO DEL RAG CONVERSACIONAL:

Turno 1: "¿Cuál es la política de devoluciones?"
         │
         ├─► Retriever busca chunks sobre devoluciones
         ├─► LLM genera respuesta con contexto
         └─► Memory guarda: [user: "¿Cuál es...", assistant: "Las..."]

Turno 2: "¿Y para productos electrónicos?"
         │
         ├─► Memory aporta historial de chat
         ├─► LLM reformula: "política de devoluciones de
         │   productos electrónicos" (standalone question)
         ├─► Retriever busca con la pregunta reformulada
         └─► LLM genera respuesta con contexto + historial

Turno 3: "¿Cuántos días tengo?"
         │
         ├─► Memory aporta historial completo
         ├─► LLM reformula: "¿Cuántos días para devolver
         │   productos electrónicos?"
         ├─► Retriever busca con pregunta reformulada
         └─► LLM responde: "30 días para electrónicos"
```

### Ejemplo Completo: FAQ Bot

El repositorio del curso incluye un ejemplo completo de un FAQ Bot con RAG en:

> **Código de referencia**: [https://github.com/rpmaya/ml2_code/blob/main/LangChain/faqBot.py](https://github.com/rpmaya/ml2_code/blob/main/LangChain/faqBot.py)

Este ejemplo integra todos los componentes vistos: carga de documentos, chunking, embeddings, vector store y cadena RAG con interfaz conversacional.

```python
"""
FAQ Bot completo con RAG - Ejemplo del curso ML2
Referencia: https://github.com/rpmaya/ml2_code/blob/main/LangChain/faqBot.py
"""
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

# ── 1. Ingesta de documentos ──────────────────────────────────
def ingest_documents(docs_path: str, db_path: str = "./chroma_db"):
    """Carga documentos, los divide en chunks y los almacena en Chroma."""
    # Cargar PDFs del directorio
    loader = DirectoryLoader(docs_path, glob="**/*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    print(f"Documentos cargados: {len(documents)}")

    # Dividir en chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(documents)
    print(f"Chunks generados: {len(chunks)}")

    # Crear vector store
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=db_path,
        collection_name="faq_bot",
    )
    print(f"Vector store creado en {db_path}")
    return vectorstore


# ── 2. Construir cadena RAG ───────────────────────────────────
def create_rag_chain(vectorstore):
    """Crea la cadena RAG con LCEL."""
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    def format_docs(docs):
        return "\n\n---\n\n".join(
            f"[{doc.metadata.get('source', '?')}]\n{doc.page_content}"
            for doc in docs
        )

    prompt = ChatPromptTemplate.from_template("""
Eres un asistente de FAQ. Responde basándote ÚNICAMENTE en el contexto.
Si no encuentras la información, di "No tengo esa información."

Contexto:
{context}

Pregunta: {question}

Respuesta:""")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain


# ── 3. Ejecutar el bot ────────────────────────────────────────
if __name__ == "__main__":
    # Primera ejecución: ingestar documentos
    if not os.path.exists("./chroma_db"):
        vectorstore = ingest_documents("./documentos")
    else:
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        vectorstore = Chroma(
            persist_directory="./chroma_db",
            embedding_function=embeddings,
            collection_name="faq_bot",
        )

    chain = create_rag_chain(vectorstore)

    # Bucle de conversación
    print("\nFAQ Bot listo. Escribe 'salir' para terminar.\n")
    while True:
        question = input("Tú: ")
        if question.lower() in ("salir", "exit", "quit"):
            break
        answer = chain.invoke(question)
        print(f"\nBot: {answer}\n")
```

---

## Bloque 4: Casos Prácticos Completos

### 5.8 Casos de Uso Reales

Los siguientes casos prácticos muestran cómo aplicar RAG a escenarios empresariales reales, combinando los componentes estudiados.

### Caso 1: Agente de E-commerce

Un agente que responde preguntas sobre productos y políticas de una tienda online, consultando tanto documentos de políticas como un inventario en Google Sheets.

```
ARQUITECTURA: AGENTE E-COMMERCE CON RAG

┌────────────────────────────────────────────────────────────────┐
│                                                                │
│  ┌──────────┐     ┌────────────────────────────────────────┐   │
│  │ Cliente  │────►│ AI Agent (n8n)                         │   │
│  │ (Chat)   │     │                                        │   │
│  └──────────┘     │ System Prompt:                         │   │
│                   │ "Eres un asistente de atención al      │   │
│                   │  cliente de TiendaXYZ..."              │   │
│                   │                                        │   │
│                   │ ┌────────────┐  ┌───────────────────┐  │   │
│                   │ │ Tool 1:    │  │ Tool 2:           │  │   │
│                   │ │ Vector     │  │ Google Sheets     │  │   │
│                   │ │ Store      │  │ (Inventario)      │  │   │
│                   │ │            │  │                   │  │   │
│                   │ │ Políticas  │  │ Stock, precios,   │  │   │
│                   │ │ de compra, │  │ disponibilidad    │  │   │
│                   │ │ devolución,│  │ en tiempo real    │  │   │
│                   │ │ envío, FAQ │  │                   │  │   │
│                   │ └────────────┘  └───────────────────┘  │   │
│                   └────────────────────────────────────────┘   │
│                                                                │
│  Flujo:                                                        │
│  1. Cliente pregunta: "¿Tenéis el iPhone 15 en stock?"         │
│  2. Agente consulta Google Sheets → Stock: 12 unidades         │
│  3. Cliente: "¿Cuál es la política de devolución?"             │
│  4. Agente consulta Vector Store → Política en documentos      │
│  5. Agente combina información y responde                      │
└────────────────────────────────────────────────────────────────┘
```

**Implementación en n8n**:
- **Tool 1 (Vector Store)**: Pinecone con políticas de compra, devolución, envío y FAQ indexadas
- **Tool 2 (Google Sheets)**: Nodo Google Sheets que lee inventario en tiempo real
- **Memory**: Window Buffer Memory para mantener contexto de la conversación
- **Despliegue**: Chat embebido en la web de la tienda o Telegram

### Caso 2: Asistente de Documentación Técnica

Un sistema RAG especializado en documentación técnica (Confluence, Notion, wikis internas) con chunking adaptado a documentos técnicos.

```
ARQUITECTURA: ASISTENTE DE DOCUMENTACIÓN TÉCNICA

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Fuentes de datos:                                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │Confluence│ │ Notion   │ │ GitHub   │ │ PDFs     │            │
│  │ (APIs)   │ │ (APIs)   │ │ (Repos)  │ │ (Manuales│            │
│  └─────┬────┘ └─────┬────┘ └────┬─────┘ └────┬─────┘            │
│        │            │           │             │                 │
│        └────────────┴─────┬─────┴─────────────┘                 │
│                           │                                     │
│                           ▼                                     │
│              ┌───────────────────────────┐                      │
│              │ Chunking Especializado    │                      │
│              │                           │                      │
│              │ - MarkdownHeaderText      │                      │
│              │   Splitter (por secciones)│                      │
│              │ - Preservar bloques de    │                      │
│              │   código completos        │                      │
│              │ - Metadatos: título,      │                      │
│              │   sección, autor, fecha   │                      │
│              └────────────┬──────────────┘                      │
│                           │                                     │
│                           ▼                                     │
│              ┌─────────────────────────┐                        │
│              │ Pinecone                │                        │
│              │ Namespace por fuente:   │                        │
│              │ - "confluence"          │                        │
│              │ - "notion"              │                        │
│              │ - "github"              │                        │
│              └─────────────────────────┘                        │
│                                                                 │
│  Consulta con filtros de metadata:                              │
│  "Buscar solo en documentación de la API v2.3 del módulo auth"  │
└─────────────────────────────────────────────────────────────────┘
```

**Consideraciones especiales para documentación técnica**:

| Aspecto | Estrategia |
|---------|------------|
| **Código en documentos** | Usar `MarkdownHeaderTextSplitter` para no partir bloques de código |
| **Versionado** | Namespaces por versión: `v2.3`, `v3.0` |
| **Actualización** | Workflow de ingesta con trigger periódico (cada 6h) |
| **Filtros** | Metadata filtering por módulo, versión, tipo de documento |

### Caso 3: Chatbot de Soporte con Escalado

Un chatbot que clasifica la urgencia de las consultas y escala a un agente humano cuando es necesario.

```
ARQUITECTURA: SOPORTE CON ESCALADO

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ┌──────────┐      ┌────────────────────────────────────────┐   │
│  │ Usuario  │─────►│ AI Agent (RAG)                         │   │
│  └──────────┘      │                                        │   │
│                    │ 1. Busca respuesta en base de          │   │
│                    │    conocimiento (FAQ + manuales)       │   │
│                    │                                        │   │
│                    │ 2. Clasifica urgencia:                 │   │
│                    │    ┌───────────────────────────────┐   │   │
│                    │    │ BAJA: FAQ, info general       │   │   │
│                    │    │ → Responde directamente       │   │   │
│                    │    │                               │   │   │
│                    │    │ MEDIA: Problema técnico       │   │   │
│                    │    │ → Responde + crea ticket      │   │   │
│                    │    │                               │   │   │
│                    │    │ ALTA: Sistema caído, pérdida  │   │   │
│                    │    │ de datos, seguridad           │   │   │
│                    │    │ → Escala a humano + alerta    │   │   │
│                    │    └───────────────────────────────┘   │   │
│                    └────────────────────┬───────────────────┘   │
│                                         │                       │
│                    ┌────────────────────┼───────────────────┐   │
│                    │                    │                   │   │
│                    ▼                    ▼                   ▼   │
│              ┌───────────┐     ┌──────────────┐    ┌──────────┐ │
│              │ Respuesta │     │ Crear Ticket │    │ Slack    │ │
│              │ directa   │     │ (Jira/Linear)│    │ Alerta   │ │
│              │ al usuario│     │              │    │ @soporte │ │
│              └───────────┘     └──────────────┘    └──────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

**Implementación del clasificador de urgencia** (en el system prompt del agente):

```
SYSTEM PROMPT - CLASIFICACIÓN DE URGENCIA:

# TAREAS
1. Responde la pregunta usando la base de conocimiento
2. Clasifica la urgencia del mensaje:
   - "BAJA": preguntas generales, FAQ, información de productos
   - "MEDIA": problemas técnicos, errores no críticos, solicitudes
   - "ALTA": sistema caído, pérdida de datos, problemas de seguridad,
     cliente muy frustrado

3. Incluye siempre al final de tu respuesta:
   URGENCIA: [BAJA|MEDIA|ALTA]

# REGLAS DE ESCALADO
- Si URGENCIA es ALTA: añade "ESCALAR: SÍ" al final
- Si mencionan palabras como "caído", "no funciona nada",
  "perdí datos", "hackeado": SIEMPRE es ALTA
```

En n8n, después del AI Agent, se añade un nodo **IF** que analiza la respuesta y enruta según la urgencia detectada.

### Caso 4: Análisis de Contratos Legal

Un sistema RAG especializado en documentos legales que requiere consideraciones especiales de chunking y privacidad.

```
ARQUITECTURA: RAG LEGAL

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  CONSIDERACIONES ESPECIALES:                                    │
│                                                                 │
│  1. CHUNKING POR CLÁUSULAS                                      │
│     ┌─────────────────────────────────────────────┐             │
│     │ No usar RecursiveCharacterTextSplitter      │             │
│     │ → Usar separadores por cláusulas:           │             │
│     │   ["CLÁUSULA", "Artículo", "Sección"]       │             │
│     │ → Cada chunk = una cláusula completa        │             │
│     │ → Metadata: número de cláusula, tipo        │             │
│     └─────────────────────────────────────────────┘             │
│                                                                 │
│  2. PRIVACIDAD Y SEGURIDAD                                      │
│     ┌─────────────────────────────────────────────┐             │
│     │ - Datos sensibles: nombres, DNI, cuentas    │             │
│     │ - Opción: anonimizar antes de indexar       │             │
│     │ - Vector store on-premise (no cloud)        │             │
│     │ - Modelo local (Ollama) para evitar enviar  │             │
│     │   datos a APIs externas                     │             │
│     │ - Logs de acceso y auditoría                │             │
│     └─────────────────────────────────────────────┘             │
│                                                                 │
│  3. PROMPT ESPECIALIZADO                                        │
│     ┌─────────────────────────────────────────────┐             │
│     │ "Eres un asistente legal. Responde citando  │             │
│     │  siempre la cláusula exacta. NO proporciones│             │
│     │  asesoramiento legal. Indica que el usuario │             │
│     │  debe consultar con un abogado."            │             │
│     └─────────────────────────────────────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

```python
# Ejemplo: Chunking por cláusulas para documentos legales
from langchain.text_splitter import RecursiveCharacterTextSplitter

legal_splitter = RecursiveCharacterTextSplitter(
    separators=[
        "\nCLÁUSULA",      # Separar por cláusulas
        "\nArtículo",       # Separar por artículos
        "\nSección",        # Separar por secciones
        "\n\n",             # Párrafos como fallback
        "\n",
        ". ",
        " ",
    ],
    chunk_size=1000,         # Cláusulas pueden ser largas
    chunk_overlap=100,       # Overlap para no perder contexto
    keep_separator=True,     # Mantener el separador en el chunk
)

# Añadir metadatos por cláusula
for i, chunk in enumerate(chunks):
    chunk.metadata["clause_number"] = i + 1
    chunk.metadata["document_type"] = "contrato"
    chunk.metadata["confidentiality"] = "alta"
```

---

## Bloque 5: Optimización y Mejores Prácticas

### 5.9 Técnicas de Optimización del RAG

Un sistema RAG básico funciona, pero puede mejorarse significativamente con técnicas avanzadas de optimización en las fases de consulta, retrieval y generación.

### Query Expansion (Expansión de Consulta)

La idea es generar múltiples variaciones de la consulta del usuario para mejorar el recall del retriever. Una sola formulación puede no capturar todos los documentos relevantes.

```
QUERY EXPANSION:

Consulta original: "¿Cómo devuelvo un producto?"
                          │
                          ▼
               ┌──────────────────┐
               │  LLM genera      │
               │  variaciones     │
               └────────┬─────────┘
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
   "política de    "proceso de    "plazo para
    devolución"    retorno de      devolver
                   productos"     artículos"
          │             │             │
          └─────────────┼─────────────┘
                        │
                        ▼
               ┌──────────────────┐
               │  Retriever busca │
               │  con TODAS las   │  Más chunks
               │  variaciones     │  relevantes
               └──────────────────┘
```

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Prompt para generar variaciones de la consulta
expansion_prompt = ChatPromptTemplate.from_template("""
Genera 3 variaciones de la siguiente pregunta.
Cada variación debe expresar la misma intención pero con palabras diferentes.
Devuelve solo las preguntas, una por línea, sin numeración.

Pregunta original: {question}

Variaciones:
""")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

def expand_query(question: str) -> list[str]:
    """Genera variaciones de la consulta para mejorar el retrieval."""
    response = (expansion_prompt | llm | StrOutputParser()).invoke(
        {"question": question}
    )
    variations = [q.strip() for q in response.strip().split("\n") if q.strip()]
    return [question] + variations  # Original + variaciones


# Buscar con todas las variaciones y combinar resultados
def retrieve_with_expansion(question: str, retriever, k: int = 4):
    """Busca con múltiples variaciones y deduplica resultados."""
    queries = expand_query(question)
    all_docs = []
    seen_contents = set()

    for query in queries:
        docs = retriever.invoke(query)
        for doc in docs:
            if doc.page_content not in seen_contents:
                seen_contents.add(doc.page_content)
                all_docs.append(doc)

    return all_docs[:k]  # Limitar a k documentos
```

### HyDE (Hypothetical Document Embeddings)

HyDE es una técnica innovadora: en lugar de buscar con el embedding de la pregunta, se genera un **documento hipotético** que respondería a la pregunta y se busca con el embedding de ese documento. Esto mejora la búsqueda porque el documento hipotético es más similar a los documentos reales que la pregunta.

```
HyDE - HYPOTHETICAL DOCUMENT EMBEDDINGS:

Pregunta: "¿Cuál es la política de devoluciones?"
                          │
                          ▼
               ┌──────────────────┐
               │  LLM genera un   │
               │  documento       │
               │  hipotético      │
               └────────┬─────────┘
                        │
                        ▼
   "La política de devoluciones de nuestra empresa
    permite a los clientes devolver productos en un
    plazo de 30 días desde la fecha de compra. Es
    necesario presentar el ticket de compra original
    y el producto debe estar en su estado original..."
                        │
                        ▼
               ┌──────────────────┐
               │  Embedding del   │  Más similar a los
               │  documento       │  documentos reales
               │  hipotético      │  que el embedding
               └────────┬─────────┘  de la pregunta
                        │
                        ▼
               ┌──────────────────┐
               │  Búsqueda        │
               │  vectorial       │
               └──────────────────┘
```

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser

# Prompt para generar documento hipotético
hyde_prompt = ChatPromptTemplate.from_template("""
Escribe un párrafo que responda la siguiente pregunta de forma detallada,
como si fuera un extracto de un documento oficial de la empresa.
No incluyas "Según el documento..." ni referencias a fuentes.
Escribe directamente el contenido como si fuera el documento real.

Pregunta: {question}

Documento:
""")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

def hyde_retrieve(question: str, vectorstore, k: int = 4):
    """Busca usando HyDE: genera documento hipotético y busca con su embedding."""
    # 1. Generar documento hipotético
    hypothetical_doc = (hyde_prompt | llm | StrOutputParser()).invoke(
        {"question": question}
    )

    # 2. Generar embedding del documento hipotético
    hyde_embedding = embeddings.embed_query(hypothetical_doc)

    # 3. Buscar con el embedding del documento hipotético
    results = vectorstore.similarity_search_by_vector(hyde_embedding, k=k)

    return results
```

> **¿Cuándo usar HyDE?**: Es especialmente útil cuando las preguntas de los usuarios son muy diferentes en estilo y vocabulario a los documentos indexados. Por ejemplo, un usuario pregunta coloquialmente pero los documentos son formales y técnicos.

### Métricas RAGAS en Detalle

Para un sistema RAG en producción, es fundamental monitorizar la calidad continuamente. Veamos cada métrica RAGAS con más detalle.

```
┌──────────────────────────────────────────────────────────────────┐
│              MÉTRICAS RAGAS - DETALLE                            │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │ CONTEXT PRECISION                                        │    │
│  │                                                          │    │
│  │ Mide: ¿Los chunks recuperados son relevantes?            │    │
│  │                                                          │    │
│  │ Ejemplo BUENO (precisión alta):                          │    │
│  │ Pregunta: "Política de devoluciones"                     │    │
│  │ Chunks: [devoluciones, plazo 30 días, excepciones]       │    │
│  │ → Todos relevantes ✓                                     │    │
│  │                                                          │    │
│  │ Ejemplo MALO (precisión baja):                           │    │
│  │ Pregunta: "Política de devoluciones"                     │    │
│  │ Chunks: [devoluciones, horarios tienda, historia empresa]│    │
│  │ → 2 de 3 son ruido ✗                                     │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │ CONTEXT RECALL                                           │    │
│  │                                                          │    │
│  │ Mide: ¿Se recuperaron TODOS los chunks necesarios?       │    │
│  │                                                          │    │
│  │ Ejemplo BUENO (recall alto):                             │    │
│  │ Para responder se necesitan chunks A, B, C               │    │
│  │ Recuperados: A, B, C → Recall = 1.0 ✓                    │    │
│  │                                                          │    │
│  │ Ejemplo MALO (recall bajo):                              │    │
│  │ Para responder se necesitan chunks A, B, C               │    │
│  │ Recuperados: A, C → Recall = 0.67 ✗ (falta B)            │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │ FAITHFULNESS (FIDELIDAD)                                 │    │
│  │                                                          │    │
│  │ Mide: ¿La respuesta se basa SOLO en el contexto?         │    │
│  │                                                          │    │
│  │ Ejemplo BUENO (fidelidad alta):                          │    │
│  │ Contexto: "Plazo de 30 días"                             │    │
│  │ Respuesta: "Tiene 30 días para devolver" ✓               │    │
│  │                                                          │    │
│  │ Ejemplo MALO (alucinación):                              │    │
│  │ Contexto: "Plazo de 30 días"                             │    │
│  │ Respuesta: "Tiene 30 días y le devolvemos                │    │
│  │  el doble del dinero" ✗ (inventado)                      │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │ ANSWER RELEVANCY                                         │    │
│  │                                                          │    │
│  │ Mide: ¿La respuesta contesta la pregunta?                │    │
│  │                                                          │    │
│  │ Ejemplo BUENO:                                           │    │
│  │ Pregunta: "¿Cuántos días para devolver?"                 │    │
│  │ Respuesta: "El plazo de devolución es de 30 días" ✓      │    │
│  │                                                          │    │
│  │ Ejemplo MALO:                                            │    │
│  │ Pregunta: "¿Cuántos días para devolver?"                 │    │
│  │ Respuesta: "Nuestra empresa fue fundada en 1995          │    │
│  │  y tiene 500 empleados" ✗ (no responde)                  │    │
│  └──────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────┘
```

### Consideraciones de Producción

Un sistema RAG en producción requiere atención a varios aspectos operativos que van más allá de la funcionalidad básica.

#### 1. Caché de Respuestas

```python
import hashlib
import json
from functools import lru_cache

class RAGCache:
    """Caché simple para respuestas RAG frecuentes."""

    def __init__(self):
        self.cache = {}

    def _hash_query(self, query: str) -> str:
        return hashlib.md5(query.lower().strip().encode()).hexdigest()

    def get(self, query: str):
        key = self._hash_query(query)
        return self.cache.get(key)

    def set(self, query: str, response: str, sources: list):
        key = self._hash_query(query)
        self.cache[key] = {
            "response": response,
            "sources": sources,
            "hits": 0,
        }

    def query_with_cache(self, query: str, rag_chain):
        """Busca en caché primero; si no existe, ejecuta RAG."""
        cached = self.get(query)
        if cached:
            cached["hits"] += 1
            return cached["response"]

        response = rag_chain.invoke(query)
        self.set(query, response, [])
        return response
```

#### 2. Monitorización de Costes

```
ESTIMACIÓN DE COSTES POR CONSULTA RAG:

┌────────────────────────────────────────────────────────────┐
│ Componente          │ Coste aproximado    │ Por consulta   │
├─────────────────────┼─────────────────────┼────────────────│
│ Embedding consulta  │ $0.00002 / 1K tokens│ ~$0.000004     │
│ Búsqueda Pinecone   │ $0.00 (incluido)    │ $0.00          │
│ LLM (gpt-4o-mini)   │ $0.15 / 1M input    │ ~$0.0003       │
│                     │ $0.60 / 1M output   │ ~$0.0003       │
├─────────────────────┼─────────────────────┼────────────────│
│ TOTAL por consulta  │                     │ ~$0.0006       │
│ 10.000 consultas/mes│                     │ ~$6.00         │
└────────────────────────────────────────────────────────────┘

Ingesta (una vez):
- 1000 páginas PDF ≈ 500K tokens de embedding ≈ $0.01
- Almacenamiento Pinecone: gratuito hasta 100K vectores
```

#### 3. Actualización de Índices

```
ESTRATEGIAS DE ACTUALIZACIÓN:

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  1. INCREMENTAL (Recomendada)                               │
│     ┌─────────────────────────────────────────────────────┐ │
│     │ - Solo procesar documentos nuevos o modificados     │ │
│     │ - Detectar cambios por fecha de modificación        │ │
│     │ - Eliminar vectores de docs antiguos y reindexar    │ │
│     │ - Menor coste y tiempo de procesamiento             │ │
│     └─────────────────────────────────────────────────────┘ │
│                                                             │
│  2. COMPLETA (Para cambios masivos)                         │
│     ┌─────────────────────────────────────────────────────┐ │
│     │ - Borrar namespace completo en Pinecone             │ │
│     │ - Reindexar todos los documentos                    │ │
│     │ - Usar cuando cambia la estrategia de chunking      │ │
│     │   o el modelo de embeddings                         │ │
│     └─────────────────────────────────────────────────────┘ │
│                                                             │
│  3. PROGRAMADA (n8n Cron Trigger)                           │
│     ┌─────────────────────────────────────────────────────┐ │
│     │ - Cron Trigger cada 6h / 24h                        │ │
│     │ - Sincronizar con fuentes de datos                  │ │
│     │ - Ideal para contenido que cambia frecuentemente    │ │
│     └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

#### 4. Manejo de Errores y Fallbacks

```python
from langchain_openai import ChatOpenAI

def query_with_fallback(question: str, rag_chain, llm_fallback=None):
    """Consulta RAG con fallback si falla el retrieval."""
    try:
        # Intentar RAG normal
        response = rag_chain.invoke(question)

        # Si la respuesta indica que no encontró información
        if "no tengo información" in response.lower():
            if llm_fallback:
                # Fallback: responder con conocimiento general del LLM
                return llm_fallback.invoke(
                    f"Responde brevemente: {question}"
                ).content + "\n\n(Nota: esta respuesta no proviene de la base de conocimiento)"
        return response

    except Exception as e:
        # Error en el pipeline RAG
        print(f"Error en RAG: {e}")
        if llm_fallback:
            return llm_fallback.invoke(
                f"Responde brevemente: {question}"
            ).content + "\n\n(Nota: respuesta generada sin consultar la base de conocimiento)"
        return "Lo siento, ha ocurrido un error. Por favor, inténtalo de nuevo."


# Configurar fallback
llm_fallback = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
```

### Checklist de Producción

```
┌──────────────────────────────────────────────────────────────────┐
│           CHECKLIST RAG EN PRODUCCIÓN                            │
│                                                                  │
│  RETRIEVAL                                                       │
│  □ Chunk size optimizado (testar 200, 500, 1000)                 │
│  □ Overlap configurado (10-20% del chunk size)                   │
│  □ Número de chunks recuperados (k) ajustado                     │
│  □ Búsqueda híbrida si hay términos técnicos                     │
│  □ Filtros de metadata cuando aplique                            │
│                                                                  │
│  GENERACIÓN                                                      │
│  □ System prompt con instrucciones claras y restricciones        │
│  □ Temperature baja (0.1-0.3) para respuestas factuales          │
│  □ Instrucción explícita de no alucinar                          │
│  □ Formato de respuesta definido                                 │
│                                                                  │
│  OPERACIONES                                                     │
│  □ Caché de respuestas frecuentes                                │
│  □ Monitorización de costes (tokens consumidos)                  │
│  □ Logging de consultas y respuestas                             │
│  □ Estrategia de actualización de índices                        │
│  □ Manejo de errores con fallbacks                               │
│  □ Rate limiting para evitar abusos                              │
│                                                                  │
│  EVALUACIÓN                                                      │
│  □ Dataset de evaluación (50-100 preguntas con ground truth)     │
│  □ RAGAS ejecutado periódicamente                                │
│  □ Alertas si métricas bajan del umbral                          │
│  □ A/B testing de cambios en configuración                       │
│                                                                  │
│  SEGURIDAD                                                       │
│  □ API Keys en variables de entorno (nunca en código)            │
│  □ Datos sensibles anonimizados antes de indexar                 │
│  □ Control de acceso a namespaces                                │
│  □ Prompt injection protection en el system prompt               │
└──────────────────────────────────────────────────────────────────┘
```

---

## Resumen de la Sesión

### Conceptos Clave

1. **Pipeline RAG completo**: Dos fases diferenciadas (indexación offline y consulta online) que conectan documentos con respuestas generadas por LLMs usando contexto recuperado
2. **Búsqueda híbrida**: Combina búsqueda vectorial (semántica) con BM25 (léxica) para mejorar el retrieval de términos técnicos, IDs y nombres propios
3. **Pinecone + n8n**: Implementación no-code de RAG con workflows de ingesta (Google Drive → Pinecone) y agente RAG (Chat → AI Agent → Vector Store Tool)
4. **LangChain RAG**: Pipeline completo en Python con Document Loaders, Text Splitters, Embeddings, Vector Stores (Chroma/FAISS/Pinecone) y cadenas LCEL
5. **Evaluación con RAGAS**: Cuatro métricas estándar (Context Precision, Context Recall, Faithfulness, Answer Relevancy) para medir la calidad del sistema
6. **Optimización**: Query expansion y HyDE para mejorar el retrieval; caché, monitorización y fallbacks para producción

### Qué Deberías Saber Hacer

| Habilidad | Nivel Esperado |
|-----------|---------------|
| Describir el pipeline RAG completo | Ambas fases con todos los componentes |
| Configurar Pinecone | Crear cuenta, índice, namespaces |
| Construir workflow de ingesta en n8n | Google Drive → Pinecone con splitter y embeddings |
| Construir agente RAG en n8n | AI Agent con Vector Store Tool y system prompt |
| Implementar RAG con LangChain | Ingesta + cadena LCEL completa en Python |
| Usar diferentes vector stores | Chroma (dev), FAISS (rendimiento), Pinecone (prod) |
| Implementar RAG conversacional | ConversationalRetrievalChain con memoria |
| Evaluar calidad con RAGAS | Configurar dataset y ejecutar evaluación |
| Aplicar query expansion y HyDE | Mejorar retrieval con técnicas avanzadas |
| Preparar RAG para producción | Caché, monitorización, fallbacks, seguridad |

---

## Conexión con la Siguiente Unidad

```
ROADMAP DEL CURSO:

Unidad 4 (anterior):   n8n + Agentes + Memoria + Despliegue
                        └─ Base de automatización y agentes

Unidad 5 (actual):     RAG (Retrieval-Augmented Generation)
                        └─ Conectar LLMs con documentos estáticos
                        └─ Base de conocimiento vectorial

Unidad 6 (siguiente):  MCP (Model Context Protocol)
                        └─ RAG conecta LLMs con documentos estáticos
                        └─ MCP va un paso más allá: permite a los LLMs
                           interactuar con sistemas DINÁMICOS en
                           tiempo real (APIs, bases de datos, servicios)
                        └─ Protocolo estándar para conectar herramientas
                           de forma interoperable
```

> **De RAG a MCP**: RAG resuelve el problema de dar conocimiento estático al LLM (documentos, manuales, FAQs). Pero, ¿qué pasa cuando el LLM necesita interactuar con sistemas en tiempo real? ¿Consultar una API, modificar una base de datos, ejecutar código? Ahí es donde entra MCP (Model Context Protocol), que estudiaremos en la Unidad 6.

---

## Actividades

### Ejercicios de esta Sesión

Completa los ejercicios prácticos disponibles en [ejercicios.md](./ejercicios.md):

1. **Pipeline RAG con Chroma** - Implementar ingesta de PDFs y cadena RAG con Chroma en Python
2. **Workflow de ingesta en n8n** - Construir el workflow Google Drive → Pinecone con Token Splitter
3. **Agente RAG en n8n** - Crear un AI Agent con Vector Store Tool y system prompt RTRF
4. **RAG conversacional** - Añadir memoria a la cadena RAG para preguntas de seguimiento
5. **Evaluación con RAGAS** - Crear dataset de evaluación y ejecutar métricas
6. **Optimización** - Implementar query expansion o HyDE y comparar resultados

### Práctica Evaluable de la Unidad

Ahora que has completado ambas sesiones, realiza la [práctica evaluable](../unidad5_practica/practica.md) de la unidad.

---

## Referencias

- LangChain. (2024). RAG Documentation. https://python.langchain.com/docs/tutorials/rag/
- LangChain. (2024). Document Loaders. https://python.langchain.com/docs/integrations/document_loaders/
- LangChain. (2024). Vector Stores. https://python.langchain.com/docs/integrations/vectorstores/
- Pinecone. (2024). Documentation. https://docs.pinecone.io/
- RAGAS. (2024). Evaluation Framework. https://docs.ragas.io/
- n8n. (2024). AI Agent Node. https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/
- n8n. (2024). Vector Store Nodes. https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.vectorstoreagent/
- Gao et al. (2023). Precise Zero-Shot Dense Retrieval without Relevance Labels (HyDE). https://arxiv.org/abs/2212.10496
- Es et al. (2023). RAGAS: Automated Evaluation of Retrieval Augmented Generation. https://arxiv.org/abs/2309.15217
- Repositorio del curso: https://github.com/rpmaya/ml2_code/
