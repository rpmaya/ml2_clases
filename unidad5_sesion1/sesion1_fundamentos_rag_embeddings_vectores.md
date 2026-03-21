# Unidad 5 - Sesión 1: RAG, Embeddings y Bases de Datos Vectoriales

## Objetivos de la Sesión

Al finalizar esta sesión, el estudiante será capaz de:
- Comprender qué es RAG (Retrieval-Augmented Generation) y por qué resuelve las principales limitaciones de los LLMs
- Entender qué son los embeddings, cómo capturan significado semántico y cómo se utilizan para búsqueda por similitud
- Conocer las principales bases de datos vectoriales y sus casos de uso
- Dominar las estrategias de chunking para dividir documentos de forma efectiva
- Implementar un pipeline RAG básico desde la indexación hasta la generación de respuestas

---

## Bloque 1: Introducción a RAG

### 1.1 ¿Qué es RAG y Por Qué lo Necesitamos?

**RAG (Retrieval-Augmented Generation)** es un patrón arquitectónico que combina la potencia generativa de los LLMs con sistemas de recuperación de información externa. En lugar de depender únicamente del conocimiento almacenado durante el entrenamiento del modelo, RAG permite al LLM **consultar fuentes de datos externas** antes de generar una respuesta.

#### Analogía: El Estudiante con Apuntes vs. El Estudiante sin Apuntes

Imagina dos estudiantes en un examen:

- **Estudiante sin apuntes (LLM solo)**: Responde únicamente con lo que memorizó durante el curso. Si la pregunta es sobre un tema que no estudió bien, inventa una respuesta que "suena" correcta.
- **Estudiante con apuntes (LLM + RAG)**: Puede consultar sus apuntes antes de responder. Busca la información relevante, la lee y formula una respuesta fundamentada. Si no encuentra la información, lo dice.

RAG convierte al LLM en ese "estudiante con apuntes".

#### Las Tres Limitaciones Fundamentales de los LLMs que RAG Resuelve

| Limitación | Descripción | Cómo RAG lo Resuelve |
|------------|-------------|---------------------|
| **Fecha de corte del conocimiento** | El modelo solo conoce información hasta su fecha de entrenamiento | RAG permite acceder a documentos actualizados en tiempo real |
| **Falta de información privada** | El LLM no tiene acceso a documentación interna, bases de datos corporativas o datos propietarios | RAG indexa y consulta datos privados sin necesidad de reentrenar |
| **Alucinaciones** | El modelo genera respuestas plausibles pero incorrectas cuando no tiene información suficiente | RAG fundamenta las respuestas en documentos reales, reduciendo la invención |

#### Ejemplo Práctico: Chatbot Corporativo

Sin RAG:
```
Usuario: "¿Cuál es la política de vacaciones de nuestra empresa?"
LLM: "Normalmente las empresas ofrecen 22 días laborables..." ← INVENTA
```

Con RAG:
```
Usuario: "¿Cuál es la política de vacaciones de nuestra empresa?"
Sistema RAG:
  1. Busca en el manual de RRHH indexado
  2. Encuentra: "Artículo 14.2 - Vacaciones: 23 días laborables..."
  3. Envía el fragmento relevante al LLM junto con la pregunta
LLM: "Según el manual de RRHH (Art. 14.2), la política de vacaciones
      establece 23 días laborables al año..." ← FUNDAMENTADO
```

### 1.2 Arquitectura General de RAG

El patrón RAG tiene **dos fases principales**: la fase de **indexación** (offline, se hace una vez) y la fase de **consulta** (online, en cada pregunta del usuario).

```
┌──────────────────────────────────────────────────────────────────┐
│                    ARQUITECTURA RAG COMPLETA                     │
│                                                                  │
│   FASE 1: INDEXACIÓN (Offline)                                   │
│   ─────────────────────────────                                  │
│                                                                  │
│   ┌───────────┐    ┌───────────┐    ┌───────────┐    ┌────────┐  │
│   │Documentos │───►│ Chunking  │───►│Embeddings │───►│  Base  │  │
│   │ (PDF, TXT,│    │(División  │    │(Vectores  │    │Vectori-│  │
│   │  HTML...) │    │ en trozos)│    │numéricos) │    │  al    │  │
│   └───────────┘    └───────────┘    └───────────┘    └────────┘  │
│                                                                  │
│   FASE 2: CONSULTA (Online)                                      │
│   ─────────────────────────                                      │
│                                                                  │
│   ┌───────────┐    ┌───────────┐    ┌───────────┐    ┌────────┐  │
│   │ Pregunta  │───►│ Embedding │───►│ Búsqueda  │───►│Top-K   │  │
│   │del usuario│    │de la      │    │ vectorial │    │chunks  │  │
│   └───────────┘    │pregunta   │    │(similitud)│    │relevan-│  │
│                    └───────────┘    └───────────┘    │tes     │  │
│                                                      └───┬────┘  │
│                                                          │       │
│                    ┌───────────┐    ┌───────────┐        │       │
│                    │ Respuesta │◄───│   LLM     │◄───────┘       │
│                    │fundamenta-│    │(genera    │  Contexto +    │
│                    │da         │    │respuesta) │  Pregunta      │
│                    └───────────┘    └───────────┘                │
└──────────────────────────────────────────────────────────────────┘
```

#### Desglose de Cada Fase

**Fase 1 - Indexación** (se ejecuta una vez o cuando se actualizan los documentos):

1. **Carga de documentos**: Se recopilan todos los documentos relevantes (PDFs, páginas web, archivos de texto, bases de datos, etc.)
2. **Chunking**: Se dividen los documentos en fragmentos más pequeños y manejables (chunks)
3. **Generación de embeddings**: Cada chunk se convierte en un vector numérico que captura su significado semántico
4. **Almacenamiento**: Los vectores se guardan en una base de datos vectorial junto con el texto original y metadatos

**Fase 2 - Consulta** (se ejecuta en cada pregunta del usuario):

1. **Embedding de la pregunta**: La pregunta del usuario se convierte en un vector usando el mismo modelo de embeddings
2. **Búsqueda por similitud**: Se buscan los K chunks más similares a la pregunta en la base de datos vectorial
3. **Construcción del prompt**: Se crea un prompt que incluye los chunks recuperados como contexto junto con la pregunta
4. **Generación**: El LLM genera una respuesta fundamentada en los documentos recuperados

### 1.3 RAG en el Contexto del Curso

```
RECORRIDO DEL CURSO:

Unidad 1: Fundamentos de IA Generativa y LLMs
├── Qué son los LLMs, cómo se entrenan
└── Capacidades y limitaciones ← RAG RESUELVE estas limitaciones

Unidad 2: Prompt Engineering
├── Diseño de prompts efectivos
└── Técnicas avanzadas (CoT, few-shot) ← El prompt de RAG usa estas técnicas

Unidad 3: Arquitectura Transformer y APIs
├── Self-Attention, arquitectura interna
├── APIs de OpenAI, Claude, Gemini ← RAG usa estas APIs para generar
└── Function Calling ← RAG puede integrarse como herramienta

Unidad 4: Agentes de IA y n8n
├── Agentes autónomos con múltiples herramientas
└── Automatización con n8n ← Los agentes usan RAG para acceder a conocimiento

Unidad 5: RAG y Bases Vectoriales  ← ESTAMOS AQUÍ
├── Embeddings y similitud semántica
├── Bases de datos vectoriales
├── Estrategias de chunking
└── Pipeline RAG completo
```

RAG conecta directamente con lo aprendido en unidades anteriores:

- **Unidad 1**: Conocimos las limitaciones de los LLMs; RAG es la solución más práctica para superarlas.
- **Unidad 2**: Las técnicas de Prompt Engineering se aplican al diseño del prompt de RAG (instrucciones al LLM para que use el contexto recuperado).
- **Unidad 3**: Usamos las APIs que aprendimos (OpenAI, etc.) tanto para generar embeddings como para la fase de generación.
- **Unidad 4**: Los agentes de n8n pueden incorporar RAG como herramienta para acceder a documentación específica.

### 1.4 Ventajas Clave de RAG

```
┌──────────────────────────────────────────────────────────────────┐
│                     VENTAJAS DE RAG                              │
│                                                                  │
│  1. INFORMACIÓN ACTUALIZADA                                      │
│     │  Actualiza documentos → Respuestas al día                  │
│     │  Sin reentrenar el modelo (coste cero)                     │
│                                                                  │
│  2. DATOS PRIVADOS Y CORPORATIVOS                                │
│     │  Manuales internos, políticas, documentación técnica       │
│     │  Los datos nunca salen de tu infraestructura               │
│                                                                  │
│  3. REDUCCIÓN DE ALUCINACIONES                                   │
│     │  Respuestas basadas en documentos reales                   │
│     │  El LLM puede decir "no encontré información"              │
│                                                                  │
│  4. VERIFICABILIDAD Y TRAZABILIDAD                               │
│     │  Cada respuesta puede citar su fuente                      │
│     │  El usuario puede verificar la información original        │
│                                                                  │
│  5. COSTE-EFICIENCIA                                             │
│     │  Mucho más barato que hacer fine-tuning del modelo         │
│     │  Actualizar datos = reindexar documentos                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## Bloque 2: Embeddings - La Base de la Búsqueda Semántica

### 2.1 ¿Qué Son los Embeddings?

Un **embedding** es una representación numérica (un vector) que captura el **significado semántico** de un texto. Es la forma en que las máquinas "entienden" el lenguaje: convirtiendo palabras, frases o documentos en secuencias de números donde la **proximidad geométrica refleja proximidad de significado**.

#### Analogía: Coordenadas GPS del Significado

Piensa en los embeddings como **coordenadas GPS del significado**:

- Madrid y Barcelona están geográficamente cerca → sus coordenadas GPS son similares
- Madrid y Tokio están lejos → sus coordenadas GPS son muy diferentes

De la misma forma:

- "perro" y "gato" son conceptos cercanos → sus embeddings son vectores similares
- "perro" y "economía" son conceptos lejanos → sus embeddings son vectores distantes

```
┌──────────────────────────────────────────────────────────────────┐
│           ESPACIO VECTORIAL DE EMBEDDINGS (Simplificado)         │
│                                                                  │
│  Dimensión 2 ▲                                                   │
│              │           "gato" •  • "perro"                     │
│              │                  • "mascota"                      │
│              │                                                   │
│              │                                                   │
│              │    "coche" •  • "vehículo"                        │
│              │          • "automóvil"                            │
│              │                                                   │
│              │                         • "python"                │
│              │                    • "programación"               │
│              │               • "código"                          │
│              │                                                   │
│              └─────────────────────────────────────► Dimensión 1 │
│                                                                  │
│  Nota: Los embeddings reales tienen 768-3072 dimensiones,        │
│  aquí se muestra una simplificación en 2D.                       │
└──────────────────────────────────────────────────────────────────┘
```

#### La Propiedad Clave: Similitud Semántica

Lo verdaderamente poderoso de los embeddings es que capturan relaciones semánticas, no simplemente coincidencia de palabras:

| Búsqueda Tradicional (palabras clave) | Búsqueda Semántica (embeddings) |
|---------------------------------------|--------------------------------|
| "cómo instalar Python" solo encuentra documentos con esas palabras exactas | "cómo instalar Python" también encuentra "guía de configuración del entorno de desarrollo Python" |
| "dolor de cabeza" no encuentra "cefalea" | "dolor de cabeza" sí encuentra "cefalea", "migraña", "jaqueca" |
| Sensible a sinónimos, idiomas, reformulaciones | Robusto ante variaciones lingüísticas |

### 2.2 Cómo Funcionan los Embeddings

Un modelo de embeddings convierte texto en un vector de números de punto flotante. Cada dimensión del vector captura un aspecto del significado:

```python
# Ejemplo conceptual de un embedding
texto = "El aprendizaje automático es fascinante"

embedding = [0.0231, -0.0145, 0.0892, ..., 0.0341]  # Vector de N dimensiones
#            dim_1    dim_2    dim_3        dim_N

# Cada dimensión captura un aspecto del significado:
# dim_1: ¿Es técnico o cotidiano?
# dim_2: ¿Es positivo o negativo?
# dim_3: ¿Está relacionado con tecnología?
# ...
# (En la práctica, las dimensiones no tienen interpretación humana directa)
```

#### Proceso de Generación 

```
┌──────────────────────────────────────────────────────────────┐
│              GENERACIÓN DE EMBEDDINGS                        │
│                                                              │
│  Texto de entrada           Modelo de              Vector    │
│  ┌──────────────┐          Embeddings           de salida    │
│  │"El gato duerme│   ┌──────────────────┐    ┌────────────┐  │
│  │ en el sofá"  │───►│  Tokenización    │───►│[0.023,     │  │
│  └──────────────┘    │  Procesamiento   │    │ -0.014,    │  │
│                      │  Pooling         │    │  0.089,    │  │
│                      └──────────────────┘    │  ...       │  │
│                                              │  0.034]    │  │
│                                              │            │  │
│                                              │ N dims     │  │
│                                              └────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

### 2.3 Modelos de Embeddings

#### Modelos Comerciales (OpenAI)

| Modelo | Dimensiones | Precio (por 1M tokens) | Uso Recomendado |
|--------|-------------|----------------------|-----------------|
| `text-embedding-3-small` | 1536 | ~$0.02 | Uso general, mejor relación coste/rendimiento |
| `text-embedding-3-large` | 3072 | ~$0.13 | Máxima precisión, aplicaciones críticas |
| `text-embedding-ada-002` | 1536 | ~$0.10 | Modelo anterior, aún funcional |

#### Modelos Open Source (Sentence Transformers)

| Modelo | Dimensiones | Idiomas | Uso Recomendado |
|--------|-------------|---------|-----------------|
| `all-MiniLM-L6-v2` | 384 | Inglés | Rápido, ideal para prototipado |
| `multilingual-e5-large` | 1024 | 100+ | Aplicaciones multilingües |
| `all-mpnet-base-v2` | 768 | Inglés | Balance calidad/velocidad |

#### Código: Generación de Embeddings con OpenAI

```python
from openai import OpenAI

client = OpenAI()  # Usa OPENAI_API_KEY del entorno

# Generar embedding para un texto
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="El aprendizaje automático transforma industrias"
)

embedding = response.data[0].embedding
print(f"Dimensiones: {len(embedding)}")  # 1536
print(f"Primeros 5 valores: {embedding[:5]}")
# [0.0231, -0.0145, 0.0892, 0.0134, -0.0567]
```

#### Código: Generación de Embeddings con Sentence Transformers (Open Source)

```python
from sentence_transformers import SentenceTransformer

# Cargar modelo (se descarga automáticamente la primera vez)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generar embeddings para múltiples textos
textos = [
    "El gato duerme en el sofá",
    "Un felino descansa sobre el sillón",
    "La economía mundial crece un 3%"
]

embeddings = model.encode(textos)

print(f"Forma: {embeddings.shape}")  # (3, 384)
# Cada texto → vector de 384 dimensiones
```

### 2.4 Métricas de Similitud

Una vez que tenemos los embeddings, necesitamos una forma de **medir cuán parecidos son dos vectores**. Existen tres métricas principales:

#### Similitud del Coseno (la más utilizada para texto)

Mide el **ángulo** entre dos vectores. Un coseno de 1 significa vectores idénticos en dirección; 0 significa ortogonales (sin relación); -1 significa opuestos.

```
┌────────────────────────────────────────────────────────────────┐
│              SIMILITUD DEL COSENO                              │
│                                                                │
│        ▲                                                       │
│        │   A • ─ ─ ─ ─ ─ → (ángulo pequeño = alta similitud)   │
│        │  / θ                                                  │
│        │ /                                                     │
│        │/ B • ─ ─ ─ ─ ─ →                                      │
│        └──────────────────►                                    │
│                                                                │
│   cos(θ) = (A · B) / (||A|| × ||B||)                           │
│                                                                │
│   Si θ ≈ 0°  →  cos(θ) ≈ 1.0  →  MUY similares                 │
│   Si θ ≈ 90° →  cos(θ) ≈ 0.0  →  Sin relación                  │
│   Si θ ≈ 180°→  cos(θ) ≈ -1.0 →  Opuestos                      │
└────────────────────────────────────────────────────────────────┘
```

#### Comparativa de Métricas

| Métrica | Fórmula | Rango | Mejor Para |
|---------|---------|-------|-----------|
| **Similitud del coseno** | cos(θ) = A·B / (‖A‖·‖B‖) | [-1, 1] | Texto (ignora magnitud, solo dirección) |
| **Distancia euclidiana** | √(Σ(aᵢ - bᵢ)²) | [0, ∞) | Datos numéricos donde la magnitud importa |
| **Producto punto** | Σ(aᵢ × bᵢ) | (-∞, +∞) | Embeddings normalizados (equivale a coseno) |

> **¿Cuál elegir?** Para búsqueda semántica con texto, la **similitud del coseno** es la opción estándar porque compara la dirección de los vectores independientemente de su magnitud. Es la métrica que usaremos en nuestros ejemplos de RAG.

#### Código: Calcular Similitud entre Textos

```python
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

# Tres textos para comparar
texto_a = "El gato duerme en el sofá"
texto_b = "Un felino descansa sobre el sillón"
texto_c = "La economía mundial crece un 3%"

# Generar embeddings
emb_a = model.encode(texto_a)
emb_b = model.encode(texto_b)
emb_c = model.encode(texto_c)

# Función de similitud del coseno
def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# Comparar
print(f"Gato vs Felino:    {cosine_similarity(emb_a, emb_b):.4f}")  # ~0.85
print(f"Gato vs Economía:  {cosine_similarity(emb_a, emb_c):.4f}")  # ~0.10
print(f"Felino vs Economía:{cosine_similarity(emb_b, emb_c):.4f}")  # ~0.08
```

La similitud entre "gato duerme en el sofá" y "felino descansa sobre el sillón" será alta (~0.85) a pesar de no compartir casi ninguna palabra, porque los embeddings capturan el significado semántico.

### 2.5 Criterios de Selección del Modelo de Embeddings

A la hora de elegir un modelo de embeddings para tu proyecto RAG, considera estos factores:

```
┌─────────────────────────────────────────────────────────────────┐
│           CRITERIOS DE SELECCIÓN DE MODELO DE EMBEDDINGS        │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │   IDIOMA    │  │DIMENSIONES  │  │   COSTE     │              │
│  │             │  │             │  │             │              │
│  │ ¿Español?   │  │ 384: rápido │  │ OpenAI:     │              │
│  │ ¿Multilin-  │  │ 768: balance│  │  pago por   │              │
│  │  güe?       │  │1536: preciso│  │  uso        │              │
│  │ ¿Solo       │  │3072: máximo │  │ Open source:│              │
│  │  inglés?    │  │             │  │  gratuito   │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │RENDIMIENTO  │  │ PRIVACIDAD  │  │ VOLUMEN     │              │
│  │             │  │             │  │             │              │
│  │ Velocidad   │  │ ¿Datos en   │  │ ¿Miles o    │              │
│  │ de          │  │  la nube?   │  │  millones   │              │
│  │ inferencia  │  │ ¿Self-host? │  │  de docs?   │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
│                                                                 │
│  RECOMENDACIÓN GENERAL:                                         │
│  • Prototipado rápido → all-MiniLM-L6-v2 (local, gratuito)      │
│  • Producción en español → text-embedding-3-small (OpenAI)      │
│  • Máxima privacidad → multilingual-e5-large (self-hosted)      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Bloque 3: Bases de Datos Vectoriales

### 3.1 ¿Por Qué Necesitamos Bases de Datos Vectoriales?

Una vez que hemos convertido nuestros documentos en embeddings (vectores numéricos), necesitamos un lugar donde **almacenarlos y buscar eficientemente** entre ellos. Las bases de datos relacionales tradicionales (MySQL, PostgreSQL) están diseñadas para buscar por valores exactos o rangos, no para encontrar los vectores más cercanos en un espacio de miles de dimensiones.

#### El Problema de la Búsqueda por Fuerza Bruta

Si tienes 1 millón de documentos y quieres encontrar los 5 más similares a una consulta, la búsqueda por fuerza bruta requeriría:
- Calcular la similitud con **cada uno** de los 1.000.000 de vectores
- Ordenar los resultados
- Con vectores de 1536 dimensiones, esto implica ~1.5 mil millones de operaciones de multiplicación

Las bases de datos vectoriales resuelven esto con **índices especializados** (como HNSW o IVF) que permiten encontrar los vectores más cercanos sin comparar con todos.

```
┌──────────────────────────────────────────────────────────────────┐
│         BBDD RELACIONAL vs. BBDD VECTORIAL                       │
│                                                                  │
│  BBDD RELACIONAL (SQL)              BBDD VECTORIAL               │
│  ┌──────────────────────┐          ┌──────────────────────┐      │
│  │ SELECT * FROM docs   │          │ query = embed("¿Cómo │      │
│  │ WHERE title LIKE     │          │   instalar Python?") │      │
│  │ '%Python%'           │          │                      │      │
│  │                      │          │ results = db.query(  │      │
│  │ → Coincidencia       │          │   vector=query,      │      │
│  │   EXACTA de texto    │          │   top_k=5            │      │
│  │                      │          │ )                    │      │
│  │ → No encuentra       │          │                      │      │
│  │   "configurar entorno│          │ → Encuentra docs con │      │
│  │   de desarrollo"     │          │   SIGNIFICADO similar│      │
│  └──────────────────────┘          └──────────────────────┘      │
└──────────────────────────────────────────────────────────────────┘
```

### 3.2 Principales Bases de Datos Vectoriales

#### Comparativa Detallada

| Característica | **Pinecone** | **Chroma** | **FAISS** | **Weaviate** |
|---------------|-------------|-----------|----------|-------------|
| **Tipo** | Cloud (SaaS) | Local / Embebida | Librería | Self-hosted / Cloud |
| **Lenguaje** | API REST/Python | Python | C++ (bindings Python) | Go |
| **Open Source** | No (tier gratuito) | Sí | Sí (Meta) | Sí |
| **Persistencia** | Gestionada en la nube | Archivo local | En memoria (+ disco) | Integrada |
| **Filtrado por metadatos** | Sí | Sí | Básico | Sí (avanzado) |
| **Escalabilidad** | Alta (serverless) | Limitada (local) | Alta (optimizado) | Alta |
| **Caso de uso ideal** | Producción en la nube | Desarrollo / prototipado | Alto rendimiento | Búsqueda híbrida |
| **Curva de aprendizaje** | Baja | Muy baja | Media | Media |

#### Pinecone: La Opción Cloud

**Pinecone** es una base de datos vectorial totalmente gestionada en la nube. Destaca por su facilidad de uso y su plan gratuito (Starter) que permite hasta 100.000 vectores.

```python
from pinecone import Pinecone

# Inicializar cliente
pc = Pinecone(api_key="tu-api-key")

# Crear un índice
pc.create_index(
    name="mi-indice-rag",
    dimension=1536,              # Debe coincidir con el modelo de embeddings
    metric="cosine",             # Similitud del coseno
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)

# Conectar al índice
index = pc.Index("mi-indice-rag")

# Insertar vectores (upsert = insert + update)
index.upsert(vectors=[
    {
        "id": "doc_001",
        "values": [0.023, -0.014, ...],  # Vector de 1536 dims
        "metadata": {
            "fuente": "manual_rrhh.pdf",
            "pagina": 14,
            "seccion": "Vacaciones"
        }
    }
])

# Buscar los 5 vectores más similares
results = index.query(
    vector=[0.018, -0.022, ...],  # Embedding de la pregunta
    top_k=5,
    include_metadata=True
)
```

**Concepto clave - Namespaces**: Pinecone permite organizar vectores en **namespaces** dentro de un mismo índice. Es como tener carpetas dentro de una base de datos:

```
┌──────────────────────────────────────────────┐
│            ÍNDICE: "mi-empresa"              │
│                                              │
│  ┌──────────────┐  ┌──────────────┐          │
│  │ Namespace:   │  │ Namespace:   │          │
│  │ "rrhh"       │  │ "tecnico"    │          │
│  │              │  │              │          │
│  │ Manual RRHH  │  │ Docs técnicos│          │
│  │ Políticas    │  │ APIs         │          │
│  │ Contratos    │  │ Tutoriales   │          │
│  └──────────────┘  └──────────────┘          │
│                                              │
│  ┌──────────────┐                            │
│  │ Namespace:   │                            │
│  │ "legal"      │                            │
│  │              │                            │
│  │ Normativa    │                            │
│  │ Compliance   │                            │
│  └──────────────┘                            │
└──────────────────────────────────────────────┘
```

#### Chroma: La Opción Local para Desarrollo

**Chroma** es una base de datos vectorial open source, embebida, que se ejecuta localmente. Es ideal para **prototipado rápido** y desarrollo por su extrema sencillez.

```python
import chromadb

# Crear cliente (persiste datos localmente)
client = chromadb.PersistentClient(path="./mi_base_vectorial")

# Crear una colección
collection = client.create_collection(
    name="documentos",
    metadata={"hnsw:space": "cosine"}  # Métrica de similitud
)

# Añadir documentos (Chroma genera embeddings automáticamente)
collection.add(
    documents=[
        "Las vacaciones son de 23 días laborables al año",
        "El horario de oficina es de 9:00 a 18:00",
        "El período de prueba es de 6 meses"
    ],
    ids=["doc_1", "doc_2", "doc_3"],
    metadatas=[
        {"fuente": "manual_rrhh", "seccion": "vacaciones"},
        {"fuente": "manual_rrhh", "seccion": "horario"},
        {"fuente": "manual_rrhh", "seccion": "contratacion"}
    ]
)

# Buscar documentos similares
results = collection.query(
    query_texts=["¿Cuántos días de vacaciones tengo?"],
    n_results=2
)

print(results["documents"])
# [['Las vacaciones son de 23 días laborables al año',
#   'El período de prueba es de 6 meses']]
```

> **Nota**: Chroma puede generar embeddings automáticamente usando un modelo por defecto (all-MiniLM-L6-v2), o puedes proporcionar tus propios embeddings.

#### FAISS: Alto Rendimiento de Meta (Facebook)

**FAISS** (Facebook AI Similarity Search) es una librería de búsqueda de similitud desarrollada por Meta. No es una base de datos completa, sino una librería optimizada para búsqueda vectorial de alto rendimiento.

```python
import faiss
import numpy as np

# Dimensión de los vectores
dimension = 1536
n_vectores = 100000

# Crear vectores aleatorios (en producción serían embeddings reales)
vectores = np.random.random((n_vectores, dimension)).astype('float32')

# Crear índice FAISS
index = faiss.IndexFlatL2(dimension)  # Búsqueda exacta (L2)
index.add(vectores)                   # Añadir vectores

print(f"Vectores indexados: {index.ntotal}")  # 100000

# Buscar los 5 más cercanos
consulta = np.random.random((1, dimension)).astype('float32')
distancias, indices = index.search(consulta, k=5)

print(f"Índices encontrados: {indices}")
print(f"Distancias: {distancias}")
```

#### Weaviate: Búsqueda Híbrida

**Weaviate** combina búsqueda vectorial con búsqueda por palabras clave (BM25), ofreciendo lo mejor de ambos mundos: búsqueda **híbrida**.

```
┌──────────────────────────────────────────────────────────────────┐
│                BÚSQUEDA HÍBRIDA (Weaviate)                       │
│                                                                  │
│  Consulta: "política de vacaciones empresa"                      │
│                                                                  │
│  ┌──────────────────┐     ┌──────────────────┐                   │
│  │ Búsqueda         │     │ Búsqueda         │                   │
│  │ VECTORIAL        │     │ POR KEYWORDS     │                   │
│  │                  │     │ (BM25)           │                   │
│  │ Semántica:       │     │ Lexicográfica:   │                   │
│  │ "días libres     │     │ "vacaciones" ✓   │                   │
│  │  remunerados"    │     │ "política" ✓     │                   │
│  │  → Score: 0.89   │     │ → Score: 0.75    │                   │
│  └────────┬─────────┘     └────────┬─────────┘                   │
│           │                        │                             │
│           └─────────┬──────────────┘                             │
│                     ▼                                            │
│           ┌──────────────────┐                                   │
│           │ FUSIÓN DE        │                                   │
│           │ RESULTADOS       │                                   │
│           │ (Reciprocal Rank │                                   │
│           │  Fusion)         │                                   │
│           └────────┬─────────┘                                   │
│                    ▼                                             │
│           Resultados ordenados                                   │
│           por relevancia combinada                               │
└──────────────────────────────────────────────────────────────────┘
```

### 3.3 Operaciones Fundamentales en una Base de Datos Vectorial

Independientemente de la base de datos que elijas, las operaciones fundamentales son tres:

| Operación | Descripción | Ejemplo |
|-----------|-------------|---------|
| **Indexar (Upsert)** | Almacenar vectores con sus metadatos | Insertar embeddings de 1000 documentos |
| **Buscar (Query)** | Encontrar los K vectores más cercanos a una consulta | Dado un embedding de pregunta, encontrar los 5 chunks más relevantes |
| **Filtrar** | Combinar búsqueda vectorial con filtros por metadatos | Buscar solo en documentos del departamento de RRHH |

#### Ejemplo de Filtrado por Metadatos

```python
# En Pinecone: buscar solo en documentos del departamento de RRHH
results = index.query(
    vector=query_embedding,
    top_k=5,
    filter={"departamento": {"$eq": "rrhh"}}
)

# En Chroma: buscar solo en documentos creados después de 2024
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5,
    where={"año": {"$gte": 2024}}
)
```

### 3.4 ¿Cuál Elegir para tu Proyecto?

```
┌──────────────────────────────────────────────────────────────────┐
│              ÁRBOL DE DECISIÓN                                   │
│                                                                  │
│  ¿Estás prototipando o aprendiendo?                              │
│  │                                                               │
│  ├── SÍ → Chroma (instalación pip, cero configuración)           │
│  │                                                               │
│  └── NO → ¿Necesitas búsqueda híbrida (vectorial + keywords)?    │
│           │                                                      │
│           ├── SÍ → Weaviate                                      │
│           │                                                      │
│           └── NO → ¿Puedes usar la nube?                         │
│                    │                                             │
│                    ├── SÍ → Pinecone (mínima ops, serverless)    │
│                    │                                             │
│                    └── NO → ¿Rendimiento extremo?                │
│                             │                                    │
│                             ├── SÍ → FAISS                       │
│                             │                                    │
│                             └── NO → Chroma con persistencia     │
└──────────────────────────────────────────────────────────────────┘
```

> **Recomendación para este curso**: Usaremos **Chroma** para los ejercicios y prototipos por su sencillez, y opcionalmente **Pinecone** para entender despliegues en producción.

---

## Bloque 4: Chunking - Estrategias de División de Documentos

### 4.1 ¿Por Qué es Necesario el Chunking?

Los documentos suelen ser demasiado largos para procesarlos como una sola unidad en un sistema RAG. Un PDF de 100 páginas no puede convertirse en un solo embedding porque:

1. **Límite de tokens**: Los modelos de embeddings tienen un límite de tokens de entrada (generalmente 512-8192 tokens).
2. **Pérdida de precisión**: Un embedding de un documento completo es demasiado genérico; pierde los detalles específicos.
3. **Contexto del LLM**: El contexto que enviamos al LLM con los resultados de la búsqueda también tiene un límite.
4. **Relevancia**: Solo una pequeña parte del documento es relevante para cada pregunta.

```
┌─────────────────────────────────────────────────────────────────┐
│                   ¿POR QUÉ CHUNKING?                            │
│                                                                 │
│  Documento completo (100 páginas):                              │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■   │   │
│  │ ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■   │   │
│  │ ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■   │   │
│  └──────────────────────────────────────────────────────────┘   │
│  → Un solo embedding genérico, poca utilidad para búsqueda      │
│                                                                 │
│  Chunks (fragmentos manejables):                                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │ Chunk 1  │ │ Chunk 2  │ │ Chunk 3  │ │ Chunk 4  │  ...       │
│  │ Intro    │ │ Cap. 1   │ │ Cap. 1   │ │ Cap. 2   │            │
│  │          │ │ (parte 1)│ │ (parte 2)│ │          │            │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘            │
│  → Cada chunk tiene un embedding específico y buscable          │
│  → La pregunta del usuario se compara con cada chunk            │
│  → Solo se recuperan los chunks realmente relevantes            │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Estrategias de Chunking

#### Estrategia 1: Tamaño Fijo (Fixed-Size Chunking)

La estrategia más simple: dividir el texto en fragmentos de tamaño fijo (por número de caracteres o tokens).

```python
def fixed_size_chunking(text, chunk_size=500, overlap=50):
    """Divide texto en chunks de tamaño fijo con solapamiento."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap  # Retroceder para crear solapamiento
    return chunks

# Ejemplo
texto = "Lorem ipsum dolor sit amet..." * 100  # Texto largo
chunks = fixed_size_chunking(texto, chunk_size=500, overlap=50)
print(f"Chunks generados: {len(chunks)}")
```

**Ventajas**: Simple de implementar, predecible.
**Desventajas**: Puede cortar frases a la mitad, no respeta la estructura del documento.

```
Ejemplo de corte inadecuado:

Chunk 1: "...el contrato se rescindirá automáticamente si el"
Chunk 2: "empleado no cumple con las condiciones establecidas..."

→ La idea se parte en dos chunks, perdiendo coherencia en ambos.
```

#### Estrategia 2: Recursive Character Text Splitting (la más usada)

Esta estrategia, implementada en **LangChain**, intenta respetar la estructura natural del texto utilizando una jerarquía de separadores:

```
┌──────────────────────────────────────────────────────────────────┐
│           RECURSIVE CHARACTER TEXT SPLITTING                     │
│                                                                  │
│  Jerarquía de separadores (de mayor a menor prioridad):          │
│                                                                  │
│  1. "\n\n"  →  Primero intenta dividir por párrafos              │
│  2. "\n"    →  Si no cabe, divide por líneas                     │
│  3. ". "    →  Si no cabe, divide por oraciones                  │
│  4. ", "    →  Si no cabe, divide por cláusulas                  │
│  5. " "     →  Si no cabe, divide por palabras                   │
│  6. ""      →  Último recurso: divide por caracteres             │
│                                                                  │
│  El algoritmo INTENTA mantener el chunk dentro del tamaño        │
│  deseado mientras respeta las fronteras naturales del texto.     │
└──────────────────────────────────────────────────────────────────┘
```

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Crear el splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,          # Tamaño máximo por chunk (en caracteres)
    chunk_overlap=50,        # Solapamiento entre chunks consecutivos
    separators=["\n\n", "\n", ". ", ", ", " ", ""],
    length_function=len      # Función para medir el tamaño
)

# Texto de ejemplo
documento = """
Capítulo 1: Introducción

El aprendizaje automático es una rama de la inteligencia artificial
que se centra en el desarrollo de algoritmos que permiten a las
computadoras aprender patrones a partir de datos.

Existen tres tipos principales de aprendizaje:
- Aprendizaje supervisado
- Aprendizaje no supervisado
- Aprendizaje por refuerzo

Capítulo 2: Aprendizaje Supervisado

El aprendizaje supervisado utiliza datos etiquetados para entrenar
modelos. Los ejemplos más comunes incluyen clasificación y regresión.
"""

# Dividir el documento
chunks = text_splitter.split_text(documento)

for i, chunk in enumerate(chunks):
    print(f"--- Chunk {i+1} ({len(chunk)} chars) ---")
    print(chunk)
    print()
```

#### Estrategia 3: Semantic Chunking (por significado)

La estrategia más avanzada: usa embeddings para detectar **cambios de tema** dentro del documento y dividir en esos puntos.

```
┌─────────────────────────────────────────────────────────────────┐
│                  SEMANTIC CHUNKING                              │
│                                                                 │
│  Texto original:                                                │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ "El gato es un mamífero doméstico. Los gatos duermen     │   │
│  │  mucho. Los felinos son cazadores nocturnos.             │   │
│  │                                                          │   │
│  │  La economía española creció un 2.5% en 2024. El PIB     │   │
│  │  superó los 1.4 billones de euros. El desempleo bajó."   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Embeddings de cada oración:                                    │
│  Oración 1 (gato):      [0.82, 0.15, ...]                       │
│  Oración 2 (gatos):     [0.85, 0.12, ...]  ← Similar a la 1     │
│  Oración 3 (felinos):   [0.79, 0.18, ...]  ← Similar a la 1     │
│  Oración 4 (economía):  [0.12, 0.91, ...]  ← MUY diferente! ⚡   │
│  Oración 5 (PIB):       [0.15, 0.88, ...]  ← Similar a la 4     │
│  Oración 6 (desempleo): [0.18, 0.85, ...]  ← Similar a la 4     │
│                                                                 │
│  Resultado:                                                     │
│  Chunk 1: Oraciones 1-3 (tema: animales/gatos)                  │
│  Chunk 2: Oraciones 4-6 (tema: economía española)               │
└─────────────────────────────────────────────────────────────────┘
```

```python
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

# Crear el chunker semántico
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
semantic_chunker = SemanticChunker(
    embeddings,
    breakpoint_threshold_type="percentile",
    breakpoint_threshold_amount=95  # Umbral para detectar cambio de tema
)

# Dividir texto
chunks = semantic_chunker.split_text(documento)
```

#### Comparativa de Estrategias

| Estrategia | Complejidad | Calidad | Velocidad | Mejor Para |
|-----------|------------|---------|-----------|-----------|
| **Tamaño fijo** | Muy baja | Baja | Muy rápida | Prototipado rápido |
| **Recursive Character** | Baja | Alta | Rápida | Uso general (recomendada) |
| **Semantic Chunking** | Alta | Muy alta | Lenta (requiere embeddings) | Documentos con temas mixtos |

### 4.3 Parámetros Clave del Chunking

Los dos parámetros más importantes que debes ajustar son:

#### Chunk Size (Tamaño del chunk)

| Tamaño | Rango Típico | Ventajas | Desventajas |
|--------|-------------|----------|-------------|
| **Pequeño** | 200-400 tokens | Alta precisión en búsqueda, resultados específicos | Pierde contexto, puede fragmentar ideas |
| **Mediano** | 400-800 tokens | Buen balance precisión/contexto | El estándar para la mayoría de casos |
| **Grande** | 800-1500 tokens | Mucho contexto, ideas completas | Menos preciso en búsqueda, más ruido |

#### Chunk Overlap (Solapamiento)

El solapamiento asegura que la información en las fronteras entre chunks no se pierda:

```
┌─────────────────────────────────────────────────────────────────┐
│                 CHUNK OVERLAP (Solapamiento)                    │
│                                                                 │
│  Sin overlap:                                                   │
│  ┌──────────────┐┌──────────────┐┌──────────────┐               │
│  │   Chunk 1    ││   Chunk 2    ││   Chunk 3    │               │
│  │              ││              ││              │               │
│  └──────────────┘└──────────────┘└──────────────┘               │
│                  ↑              ↑                               │
│           Información en la frontera puede perderse             │
│                                                                 │
│  Con overlap (10-20%):                                          │
│  ┌───────────────────┐                                          │
│  │     Chunk 1       │                                          │
│  │              ┌────┤───────────────┐                          │
│  └──────────────│ OV │   Chunk 2     │                          │
│                 └────┤          ┌────┤──────────────┐           │
│                      └──────────│ OV │   Chunk 3    │           │
│                                 └────┤              │           │
│                                      └──────────────┘           │
│                                                                 │
│  OV = Overlap: texto compartido entre chunks consecutivos       │
│  Regla general: overlap = 10-20% del chunk_size                 │
└─────────────────────────────────────────────────────────────────┘
```

**Regla práctica**: Un overlap del 10-20% del `chunk_size` suele funcionar bien. Si `chunk_size = 500`, entonces `chunk_overlap = 50-100`.

### 4.4 Impacto del Chunking en la Calidad del RAG

> **El chunking inadecuado es la causa más común de respuestas pobres en un sistema RAG.**

```
┌──────────────────────────────────────────────────────────────────┐
│        IMPACTO DEL CHUNKING EN LA CALIDAD                        │
│                                                                  │
│  Chunks MUY GRANDES (>1500 tokens):                              │
│  ┌──────────────────────────────────────────┐                    │
│  │ ■ Mucho texto irrelevante mezclado       │                    │
│  │ ■ El embedding es demasiado genérico     │  → Baja precisión  │
│  │ ■ Ocupa mucho del contexto del LLM       │    en búsqueda     │
│  └──────────────────────────────────────────┘                    │
│                                                                  │
│  Chunks MUY PEQUEÑOS (<100 tokens):                              │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐                              │
│  │frag│ │frag│ │frag│ │frag│ │frag│                              │
│  └────┘ └────┘ └────┘ └────┘ └────┘                              │
│  → Pierde contexto, ideas fragmentadas                           │
│  → El LLM no tiene suficiente información                        │
│                                                                  │
│  Chunks BIEN CALIBRADOS (300-800 tokens):                        │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐              │
│  │ Idea completa│ │ Idea completa│ │ Idea completa│              │
│  │ con contexto │ │ con contexto │ │ con contexto │              │
│  └──────────────┘ └──────────────┘ └──────────────┘              │
│  → Precisión alta + contexto suficiente ✓                        │
└──────────────────────────────────────────────────────────────────┘
```

### 4.5 Ejemplo Completo: De Documento a Chunks Indexados

Veamos un flujo completo que integra chunking, embeddings y almacenamiento en una base vectorial:

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb

# 1. CARGAR DOCUMENTO
with open("manual_rrhh.txt", "r", encoding="utf-8") as f:
    documento = f.read()

print(f"Documento original: {len(documento)} caracteres")

# 2. CHUNKING
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", ", ", " ", ""]
)
chunks = text_splitter.split_text(documento)
print(f"Chunks generados: {len(chunks)}")

# 3. GENERAR EMBEDDINGS
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(chunks)
print(f"Embeddings generados: {embeddings.shape}")

# 4. ALMACENAR EN CHROMA
client = chromadb.PersistentClient(path="./vectordb")
collection = client.get_or_create_collection("manual_rrhh")

collection.add(
    documents=chunks,
    embeddings=embeddings.tolist(),
    ids=[f"chunk_{i}" for i in range(len(chunks))],
    metadatas=[{"fuente": "manual_rrhh.txt", "chunk_index": i}
               for i in range(len(chunks))]
)

print(f"Chunks almacenados en base vectorial: {collection.count()}")

# 5. CONSULTAR
pregunta = "¿Cuántos días de vacaciones tengo?"
query_embedding = model.encode([pregunta])

results = collection.query(
    query_embeddings=query_embedding.tolist(),
    n_results=3
)

print("\n--- Resultados de la búsqueda ---")
for i, doc in enumerate(results["documents"][0]):
    print(f"\nChunk {i+1} (distancia: {results['distances'][0][i]:.4f}):")
    print(doc[:200] + "...")
```

---

## Bloque 5: Integración - Construyendo un Mini Pipeline RAG 

### 5.1 Juntando Todas las Piezas

Ahora que entendemos cada componente (RAG, embeddings, bases vectoriales, chunking), vamos a ver cómo se integran en un pipeline funcional completo.

```
┌────────────────────────────────────────────────────────────────┐
│              PIPELINE RAG COMPLETO                             │
│                                                                │
│  ┌─────────┐   ┌──────────┐   ┌──────────┐   ┌──────────────┐  │
│  │ Docs    │──►│ Chunking │──►│Embedding │──►│   Chroma DB  │  │
│  │ (PDFs)  │   │ Recursive│   │ model    │   │   (vectores) │  │
│  └─────────┘   └──────────┘   └──────────┘   └──────┬───────┘  │
│                                                     │          │
│  ═══════════════════════════════════════════════════════       │
│                                                     │          │
│  ┌─────────┐   ┌──────────┐   ┌──────────┐          │          │
│  │Pregunta │──►│Embedding │──►│ Búsqueda │──────────┘          │
│  │ usuario │   │ pregunta │   │ top-k    │                     │
│  └─────────┘   └──────────┘   └────┬─────┘                     │
│                                    │                           │
│                               ┌────▼──────────────────────┐    │
│                               │ Prompt:                   │    │
│                               │ "Dado el siguiente        │    │
│                               │  contexto: {chunks}       │    │
│                               │  Responde: {pregunta}"    │    │
│                               └────┬──────────────────────┘    │
│                                    │                           │
│                               ┌────▼─────┐                     │
│                               │   LLM    │                     │
│                               │ (OpenAI) │                     │
│                               └────┬─────┘                     │
│                                    │                           │
│                               ┌────▼──────────────────────┐    │
│                               │ Respuesta fundamentada    │    │
│                               │ con citas a las fuentes   │    │
│                               └───────────────────────────┘    │
└────────────────────────────────────────────────────────────────┘
```

### 5.2 Ejemplo Conceptual: El Prompt de RAG

El prompt que se envía al LLM en la fase de generación es crucial. Aquí es donde aplicamos lo aprendido en la **Unidad 2 (Prompt Engineering)**:

```python
def construir_prompt_rag(pregunta, chunks_recuperados):
    """Construye el prompt para el LLM con el contexto recuperado."""

    contexto = "\n\n---\n\n".join(chunks_recuperados)

    prompt = f"""Eres un asistente experto que responde preguntas basándose
ÚNICAMENTE en el contexto proporcionado. Si la información no está en el
contexto, responde: "No tengo información suficiente para responder."

CONTEXTO:
{contexto}

PREGUNTA: {pregunta}

INSTRUCCIONES:
- Responde basándote SOLO en el contexto proporcionado
- Cita las fuentes cuando sea posible
- Si no encuentras la respuesta en el contexto, dilo explícitamente
- Sé conciso y directo

RESPUESTA:"""

    return prompt
```

Observa cómo aplicamos técnicas de Prompt Engineering:
- **Rol claro**: "Eres un asistente experto..."
- **Restricción explícita**: "basándose ÚNICAMENTE en el contexto"
- **Instrucciones específicas**: Citar fuentes, admitir desconocimiento
- **Formato estructurado**: Secciones claras de contexto, pregunta e instrucciones

### 5.3 RAG vs. Fine-Tuning: ¿Cuándo Usar Cada Uno?

Una pregunta frecuente es: ¿no sería mejor hacer fine-tuning del modelo con nuestros datos? La respuesta depende del caso de uso:

| Aspecto | RAG | Fine-Tuning |
|---------|-----|-------------|
| **Datos que cambian frecuentemente** | Ideal (reindexar = minutos) | No viable (reentrenar = horas/días) |
| **Coste** | Bajo (solo embeddings + búsqueda) | Alto (GPU, tiempo de entrenamiento) |
| **Tiempo de implementación** | Horas/días | Semanas |
| **Trazabilidad** | Alta (cita fuentes concretas) | Baja (el conocimiento se "mezcla" en el modelo) |
| **Estilo de respuesta** | Controlas con el prompt | El modelo "aprende" el estilo |
| **Conocimiento especializado profundo** | Bueno | Excelente |
| **Tareas muy específicas** | Bueno | Excelente |

**Regla general**: Si necesitas que el modelo **acceda a información específica**, usa RAG. Si necesitas que el modelo **se comporte de una forma específica**, considera fine-tuning. En la práctica, RAG es la opción correcta en el 80-90% de los casos empresariales.

### 5.4 Patrones Avanzados de RAG (Vista Previa)

En la Sesión 2 profundizaremos en estos patrones, pero es útil conocer que existen:

```
┌──────────────────────────────────────────────────────────────────┐
│            EVOLUCIÓN DE PATRONES RAG                             │
│                                                                  │
│  Naive RAG (lo que hemos visto hoy)                              │
│  ├── Pregunta → Búsqueda → LLM → Respuesta                       │
│  │   Simple pero efectivo para la mayoría de casos               │
│  │                                                               │
│  Advanced RAG (Sesión 2)                                         │
│  ├── Pre-retrieval: reformulación de queries, HyDE               │
│  ├── Retrieval: reranking, búsqueda híbrida                      │
│  └── Post-retrieval: compresión de contexto, verificación        │
│                                                                  │
│  Modular RAG (más allá del curso)                                │
│  ├── Componentes intercambiables                                 │
│  ├── Routing entre múltiples fuentes                             │
│  └── Agentes RAG con herramientas                                │
└──────────────────────────────────────────────────────────────────┘
```

---

## Resumen de la Sesión

### Conceptos Clave

1. **RAG (Retrieval-Augmented Generation)** es un patrón que combina la capacidad generativa de los LLMs con la recuperación de información externa, resolviendo las tres principales limitaciones de los LLMs: fecha de corte del conocimiento, falta de datos privados y alucinaciones.

2. **Los embeddings** son representaciones vectoriales que capturan el significado semántico del texto. Textos con significado similar tienen vectores cercanos en el espacio multidimensional, lo que permite búsqueda por similitud semántica en lugar de por coincidencia de palabras.

3. **Las bases de datos vectoriales** (Pinecone, Chroma, FAISS, Weaviate) almacenan y buscan eficientemente entre millones de vectores usando índices especializados, habilitando la recuperación de información en milisegundos.

4. **El chunking** es el proceso de dividir documentos en fragmentos manejables. La estrategia RecursiveCharacterTextSplitter es la más recomendada por respetar la estructura natural del texto, y los parámetros `chunk_size` (300-800 tokens) y `chunk_overlap` (10-20%) son críticos para la calidad del sistema.

5. **El pipeline RAG** integra cuatro componentes: carga de documentos, chunking, generación de embeddings y almacenamiento vectorial (indexación), seguido de búsqueda por similitud y generación de respuestas fundamentadas (consulta).

---

## Conexión con la Sesión 2

En la próxima sesión completaremos la implementación práctica de RAG y exploraremos técnicas avanzadas:

- **LangChain para RAG**: Uso del framework LangChain para construir pipelines RAG completos con pocas líneas de código
- **Técnicas avanzadas de RAG**: Query rewriting, HyDE, reranking y self-query retrieval
- **RAG con múltiples fuentes**: Integrar PDFs, páginas web, bases de datos y APIs
- **Evaluación de sistemas RAG**: Métricas de calidad (faithfulness, relevance, answer correctness)
- **RAG en producción**: Optimización, monitorización y buenas prácticas
- **Conexión con n8n**: Integrar RAG como herramienta de un agente en n8n (Unidad 4)

---

## Conexiones con Otras Unidades

```
┌──────────────────────────────────────────────────────────────────┐
│              MAPA DE CONEXIONES DEL CURSO                        │
│                                                                  │
│   Unidad 1: IA Generativa y LLMs                                 │
│        │  Conocemos las limitaciones de los LLMs                 │
│        ▼                                                         │
│   Unidad 2: Prompt Engineering                                   │
│        │  Técnicas para diseñar el prompt de RAG                 │
│        ▼                                                         │
│   Unidad 3: APIs y Function Calling                              │
│        │  APIs de OpenAI para embeddings y generación            │
│        ▼                                                         │
│   Unidad 4: Agentes de IA y n8n                                  │
│        │  Los agentes usan RAG como herramienta                  │
│        ▼                                                         │
│   Unidad 5: RAG y Bases Vectoriales  ← ESTAMOS AQUÍ              │
│        │  Pipeline completo de recuperación y generación         │
│        ▼                                                         │
│   Unidad 6: MCP (Model Context Protocol)                         │
│        └  Estándar para conectar modelos con fuentes de datos    │
└──────────────────────────────────────────────────────────────────┘
```

---

## Actividades

### Ejercicios de esta Sesión

Completa los ejercicios prácticos disponibles en [ejercicios.md](./ejercicios.md):

1. **Generar y comparar embeddings** - Crear embeddings con OpenAI y Sentence Transformers, calcular similitudes entre textos
2. **Explorar bases de datos vectoriales** - Crear una colección en Chroma, insertar documentos y realizar búsquedas
3. **Experimentar con estrategias de chunking** - Aplicar diferentes estrategias a un documento y comparar resultados
4. **Mini pipeline RAG** - Construir un pipeline RAG básico de extremo a extremo con Chroma y un LLM
5. **Análisis del impacto del chunk_size** - Variar el tamaño de chunks y observar cómo afecta a la calidad de las respuestas

---

## Referencias

- Lewis, P., Perez, E., Piktus, A., et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. NeurIPS. https://arxiv.org/abs/2005.11401
- Gao, Y., Xiong, Y., Gao, X., et al. (2024). *Retrieval-Augmented Generation for Large Language Models: A Survey*. https://arxiv.org/abs/2312.10997
- OpenAI. *Embeddings Guide*. https://platform.openai.com/docs/guides/embeddings
- Pinecone. *Documentation*. https://docs.pinecone.io/
- Chroma. *Documentation*. https://docs.trychroma.com/
- LangChain. *Text Splitters*. https://python.langchain.com/docs/modules/data_connection/document_transformers/
- Sentence Transformers. *Documentation*. https://www.sbert.net/
- FAISS. *Facebook AI Similarity Search*. https://github.com/facebookresearch/faiss
- Weaviate. *Documentation*. https://weaviate.io/developers/weaviate
- Repositorio de código del curso. https://github.com/rpmaya/ml2_code/
