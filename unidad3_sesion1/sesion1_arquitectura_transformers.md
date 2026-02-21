# Unidad 3 - Sesión 1: Arquitectura Transformer en Profundidad

## Objetivos de la Sesión

Al finalizar esta sesión, el estudiante será capaz de:
- Comprender en profundidad el mecanismo de Self-Attention y Multi-Head Attention
- Integrar APIs de modelos de lenguaje modernos en aplicaciones prácticas
- Desarrollar aplicaciones prácticas basadas en arquitecturas Transformer
- Implementar un Transformer desde cero entendiendo cada componente

## Duración Total: 4 horas

---

## Bloque 1: Recapitulación y Contexto

### 1.1 Conexión con las Unidades Anteriores

A lo largo de las primeras dos unidades hemos construido una base sólida:

```
RECORRIDO DEL CURSO:

Unidad 1 (y Aprendizaje Automático I): Deep Learning e IA Generativa
├── Redes neuronales, backpropagation
├── CNNs, RNNs, LSTMs
└── Limitaciones de las arquitecturas secuenciales

Unidad 2: Prompt Engineering y Uso de LLMs
├── Diseño de prompts efectivos
├── Técnicas: zero-shot, few-shot, CoT
└── Interacción práctica con modelos de lenguaje

Unidad 3: Arquitectura Transformer en Profundidad  ← ESTAMOS AQUÍ
├── Self-Attention y Multi-Head Attention
├── Componentes internos del Transformer
├── Tipos de arquitectura (encoder, decoder, encoder-decoder)
└── Integración con APIs modernas
```

### 1.2 De los Modelos Generativos a los Transformers

Las arquitecturas previas (RNNs, LSTMs, ...) presentaban limitaciones fundamentales:

| Limitación | RNN/LSTM | Transformer |
|------------|----------|-------------|
| Procesamiento | Secuencial (token a token) | Paralelo (todos los tokens a la vez) |
| Dependencias largas | Se degradan con la distancia | Acceso directo a cualquier posición |
| Velocidad de entrenamiento | Lenta (no paralelizable) | Rápida (altamente paralelizable) |
| Escalabilidad | Limitada | Escala eficientemente con datos y parámetros |

En 2017, el paper **"Attention Is All You Need"** (Vaswani et al.) introdujo la arquitectura Transformer, eliminando por completo la recurrencia y las convoluciones, reemplazándolas por mecanismos de **atención**.

```
┌────────────────────────────────────────────────────────────┐
│                  EVOLUCIÓN DE ARQUITECTURAS                │
│                                                            │
│  RNN (1986) → LSTM (1997) → Attention (2014) → Transformer │
│       │            │              │                  │     │
│    Secuencial  Compuertas    Atención como      Solo       │
│    simple      de memoria    complemento        atención   │
└────────────────────────────────────────────────────────────┘
```

### 1.3 Objetivos de esta Unidad

Esta unidad tiene cuatro objetivos principales:

1. **Comprender Self-Attention y Multi-Head Attention**: Entender matemáticamente y de forma intuitiva cómo el modelo decide qué información es relevante en cada posición de la secuencia.

2. **Integrar APIs de modelos de lenguaje**: Aprender a usar las APIs de OpenAI, Gemini, Claude y herramientas como LangChain para construir aplicaciones reales.

3. **Desarrollar aplicaciones prácticas**: Pasar de la teoría a la implementación, creando sistemas que utilicen modelos Transformer para resolver problemas concretos.

4. **Implementar un Transformer desde cero**: Codificar cada componente (atención, feed-forward, normalización, positional encoding) para consolidar la comprensión profunda de la arquitectura.

### 1.4 Visión General de la Arquitectura Transformer

```
┌──────────────────────────────────────────────────────────────┐
│                   ARQUITECTURA TRANSFORMER                   │
│                                                              │
│    ENCODER                              DECODER              │
│  ┌──────────────┐                   ┌──────────────┐         │
│  │ Multi-Head   │                   │ Masked       │         │
│  │ Attention    │                   │ Multi-Head   │         │
│  │    + Add&Norm│                   │ Attention    │         │
│  ├──────────────┤                   │    + Add&Norm│         │
│  │ Feed-Forward │                   ├──────────────┤         │
│  │    + Add&Norm│                   │ Cross        │         │
│  └──────┬───────┘ × N               │ Attention    │         │
│         │                           │    + Add&Norm│         │
│  ┌──────┴───────┐                   ├──────────────┤         │
│  │ Positional   │                   │ Feed-Forward │         │
│  │ Encoding     │                   │    + Add&Norm│         │
│  ├──────────────┤                   └──────┬───────┘ × N     │
│  │ Input        │                   ┌──────┴───────┐         │
│  │ Embedding    │                   │ Positional   │         │
│  └──────────────┘                   │ Encoding     │         │
│                                     ├──────────────┤         │
│                                     │ Output       │         │
│                                     │ Embedding    │         │
│                                     └──────────────┘         │
└──────────────────────────────────────────────────────────────┘
```

---

## Bloque 2: Self-Attention y Multi-Head Attention

### 2.1 El Mecanismo de Self-Attention en Detalle

El **Self-Attention** (auto-atención) es el mecanismo central del Transformer. Permite que cada token de una secuencia "preste atención" a todos los demás tokens para construir una representación contextualizada.

#### ¿Por qué es necesaria la atención?

Consideremos la oración: *"El banco estaba lleno de peces"* vs *"El banco estaba lleno de clientes"*. La palabra "banco" tiene significados completamente diferentes según su contexto. Self-Attention permite capturar esta dependencia.

### 2.2 Matrices Q, K, V: Query, Key, Value

El mecanismo de Self-Attention se basa en tres matrices fundamentales:

| Matriz | Nombre | Analogía Intuitiva |
|--------|--------|-------------------|
| **Q** (Query) | Consulta | "Lo que estoy buscando" |
| **K** (Key) | Clave | "Lo que tengo para ofrecer" |
| **V** (Value) | Valor | "La información que proporciono" |

#### Analogía: Biblioteca

Imagina una biblioteca:
- **Query**: La pregunta que llevas al bibliotecario ("Busco un libro sobre redes neuronales")
- **Key**: Los temas de cada libro en el catálogo ("Redes neuronales", "Cocina italiana", "Historia de España")
- **Value**: El contenido real de cada libro

El mecanismo compara tu Query con cada Key para determinar qué Values son más relevantes.

#### Cálculo de Q, K, V

Cada token tiene un embedding (vector numérico). Las matrices Q, K y V se obtienen mediante transformaciones lineales aprendidas:

```
Q = embedding × W_Q    (Matriz de pesos para queries)
K = embedding × W_K    (Matriz de pesos para keys)
V = embedding × W_V    (Matriz de pesos para values)
```

Donde `W_Q`, `W_K`, `W_V` son matrices de parámetros que el modelo aprende durante el entrenamiento.

```
┌─────────────┐     ┌───────┐     ┌─────┐
│  Embedding  │────►│  W_Q  │────►│  Q  │
│  del token  │     └───────┘     └─────┘
│             │     ┌───────┐     ┌─────┐
│  (d_model)  │────►│  W_K  │────►│  K  │
│             │     └───────┘     └─────┘
│             │     ┌───────┐     ┌─────┐
│             │────►│  W_V  │────►│  V  │
└─────────────┘     └───────┘     └─────┘
```

### 2.3 Los 4 Pasos del Self-Attention

#### Paso 1: Calcular scores (puntuaciones de atención)

Se calcula el producto punto entre el Query de un token y los Keys de todos los tokens:

```
score(i, j) = Q_i · K_j^T
```

Un score alto indica que el token j es muy relevante para el token i.

#### Paso 2: Escalar los scores

Se dividen los scores por la raíz cuadrada de la dimensión de los keys (`d_k`) para evitar que los valores del producto punto sean demasiado grandes:

```
scaled_score(i, j) = (Q_i · K_j^T) / √d_k
```

Sin este escalado, los gradientes se volverían inestables (valores extremos en softmax).

#### Paso 3: Aplicar Softmax

Se convierte el vector de scores en una distribución de probabilidad:

```
attention_weights = softmax(scaled_scores)
```

Esto garantiza que los pesos sumen 1 y sean todos positivos.

#### Paso 4: Calcular la salida (suma ponderada de Values)

La salida es la suma ponderada de los Values según los pesos de atención:

```
output_i = Σ_j (attention_weight(i,j) × V_j)
```

#### Fórmula Completa

Todo se resume en una sola ecuación elegante:

```
Attention(Q, K, V) = softmax(QK^T / √d_k) × V
```

```
┌─────────────────────────────────────────────────────────────┐
│              FLUJO DE SELF-ATTENTION                        │
│                                                             │
│   Q ──┐                                                     │
│       ├──► Q × K^T ──► ÷ √d_k ──► softmax ──► × V ──► output│
│   K ──┘                                                     │
│                                                             │
│   V ─────────────────────────────────────────►┘             │
└─────────────────────────────────────────────────────────────┘
```

### 2.4 Ejemplo Numérico Completo

Trabajemos con una secuencia de 3 tokens y dimensión d=2.

**Datos iniciales:**

```
Tokens: ["Hola", "mundo", "feliz"]

Q (Queries):              K (Keys):                V (Values):
┌─────────┐              ┌─────────┐              ┌─────────┐
│  1   0  │  ← Hola      │  1   0  │  ← Hola      │  1   2  │  ← Hola
│  0   1  │  ← mundo     │  0   1  │  ← mundo     │  3   4  │  ← mundo
│  1   1  │  ← feliz     │ 0.5 0.5 │  ← feliz     │  5   6  │  ← feliz
└─────────┘              └─────────┘              └─────────┘
```

**Paso 1: Calcular scores (Q × K^T)**

```
             K_Hola  K_mundo  K_feliz
Q_Hola   [  1×1+0×0  1×0+0×1  1×0.5+0×0.5 ]   [ 1.0   0.0   0.5 ]
Q_mundo  [  0×1+1×0  0×0+1×1  0×0.5+1×0.5 ]  = [ 0.0   1.0   0.5 ]
Q_feliz  [  1×1+1×0  1×0+1×1  1×0.5+1×0.5 ]   [ 1.0   1.0   1.0 ]
```

**Paso 2: Escalar (÷ √d_k = √2 ≈ 1.414)**

```
Scores escalados:
[ 0.707   0.000   0.354 ]
[ 0.000   0.707   0.354 ]
[ 0.707   0.707   0.707 ]
```

**Paso 3: Aplicar Softmax (por filas)**

```
Pesos de atención:
[ 0.421   0.208   0.371 ]   ← "Hola" presta más atención a sí mismo
[ 0.208   0.421   0.371 ]   ← "mundo" presta más atención a sí mismo
[ 0.333   0.333   0.333 ]   ← "feliz" presta atención uniforme
```

**Paso 4: Salida (pesos × V)**

```
Output_Hola  = 0.421×[1,2] + 0.208×[3,4] + 0.371×[5,6]
             = [0.421, 0.842] + [0.624, 0.832] + [1.855, 2.226]
             = [2.900, 3.900]

Output_mundo = 0.208×[1,2] + 0.421×[3,4] + 0.371×[5,6]
             = [0.208, 0.416] + [1.263, 1.684] + [1.855, 2.226]
             = [3.326, 4.326]

Output_feliz = 0.333×[1,2] + 0.333×[3,4] + 0.333×[5,6]
             = [0.333, 0.666] + [0.999, 1.332] + [1.665, 1.998]
             = [2.997, 3.996]
```

### 2.5 Ejemplo Intuitivo: Resolución de Correferencia

Consideremos la oración:

> *"El gato se sentó en la alfombra porque estaba cansado"*

¿A qué se refiere "estaba"? Veamos cómo Self-Attention resuelve esto:

```
El  gato  se  sentó  en  la  alfombra  porque  estaba  cansado
                                                  │
                            ¿A quién presta atención "estaba"?
                                                  │
                         ┌────────────────────────┘
                         │
                    ┌────▼────┐
                    │  "gato" │ ← Score alto: sujeto de la oración
                    │  0.45   │
                    └─────────┘
                    ┌─────────┐
                    │"alfombra"│ ← Score bajo: no es un ser animado
                    │  0.10   │
                    └─────────┘
                    ┌─────────┐
                    │ "sentó" │ ← Score medio: verbo relacionado
                    │  0.25   │
                    └─────────┘
```

El mecanismo de atención aprende que "estaba" debe conectarse con "gato" (no con "alfombra") porque:
- "cansado" es un adjetivo que se aplica a seres animados
- "gato" es el sujeto de la cláusula principal
- Los patrones sintácticos aprendidos favorecen esta conexión

### 2.6 Mapas de Atención (Attention Maps)

Los mapas de atención son visualizaciones matriciales que muestran los pesos de atención entre todos los pares de tokens:

```
              El   gato  se  sentó  en   la  alfombra porque estaba cansado
El          [0.8  0.1  0.0  0.0   0.0  0.0   0.0    0.0    0.1    0.0  ]
gato        [0.1  0.6  0.0  0.2   0.0  0.0   0.0    0.0    0.0    0.1  ]
se          [0.0  0.3  0.2  0.4   0.0  0.0   0.0    0.0    0.1    0.0  ]
sentó       [0.0  0.3  0.1  0.3   0.1  0.0   0.1    0.0    0.0    0.1  ]
en          [0.0  0.0  0.0  0.2   0.3  0.1   0.3    0.0    0.0    0.1  ]
la          [0.0  0.0  0.0  0.0   0.1  0.3   0.5    0.0    0.0    0.1  ]
alfombra    [0.0  0.0  0.0  0.1   0.2  0.2   0.4    0.0    0.0    0.1  ]
porque      [0.0  0.1  0.0  0.3   0.0  0.0   0.0    0.3    0.2    0.1  ]
estaba      [0.0  0.4  0.0  0.1   0.0  0.0   0.1    0.1    0.1    0.2  ]
cansado     [0.0  0.5  0.0  0.0   0.0  0.0   0.0    0.0    0.2    0.3  ]
```

> **Nota**: Los valores más altos indican mayor atención. Observa cómo "estaba" presta mayor atención a "gato" (0.4) — el modelo ha resuelto la correferencia.

Herramientas como **BertViz** permiten visualizar estos mapas de atención de forma interactiva para modelos reales.

---

## Bloque 3: FFN, Conexiones Residuales y Layer Normalization

### 3.1 Multi-Head Attention

En lugar de ejecutar una sola función de atención, el Transformer utiliza **múltiples cabezas de atención** en paralelo. Cada cabeza puede capturar diferentes tipos de relaciones.

#### Fórmula

```
MultiHead(Q, K, V) = Concat(head_1, head_2, ..., head_h) × W_O

donde:
    head_i = Attention(Q × W_Q^i, K × W_K^i, V × W_V^i)
```

#### ¿Qué captura cada cabeza?

| Cabeza | Tipo de Relación | Ejemplo |
|--------|------------------|---------|
| Cabeza 1 | Relaciones sintácticas | sujeto ↔ verbo |
| Cabeza 2 | Correferencia | pronombre ↔ sustantivo |
| Cabeza 3 | Relaciones semánticas | sinónimos, antónimos |
| Cabeza 4 | Dependencias de largo alcance | inicio de párrafo ↔ conclusión |
| ... | ... | ... |

```
┌────────────────────────────────────────────────────────────────┐
│                  MULTI-HEAD ATTENTION                          │
│                                                                │
│   Input ──┬──► Cabeza 1 (sintáctica)    ───┐                   │
│           ├──► Cabeza 2 (correferencia)  ──┤                   │
│           ├──► Cabeza 3 (semántica)      ──┼──► Concat ──► W_O ──► Output│
│           ├──► Cabeza 4 (largo alcance)  ──┤                   │
│           └──► ...                       ──┘                   │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

#### Eficiencia: División de Dimensiones

No multiplicamos el costo computacional por el número de cabezas. En su lugar, dividimos la dimensionalidad:

```
d_head = d_model / num_heads

Ejemplo (GPT / BERT base):
    d_model   = 768
    num_heads = 12
    d_head    = 768 / 12 = 64

Cada cabeza trabaja con vectores de dimensión 64.
El costo total es equivalente a una sola cabeza de dimensión 768.
```

### 3.2 Feed-Forward Networks (FFN)

Después de la capa de atención, cada posición pasa por una red feed-forward idéntica e independiente.

#### Fórmula

```
FFN(x) = GELU(x × W_1 + b_1) × W_2 + b_2
```

#### Factor de Expansión 4x

La red feed-forward expande la dimensionalidad por un factor de 4 y luego la comprime de vuelta:

```
┌────────────────────────────────────────────────────────────────┐
│                    FEED-FORWARD NETWORK                        │
│                                                                │
│   Input (768) ──► Expansión (3072) ──► GELU ──► Compresión (768) ──► Output│
│                    W_1: 768×3072         │        W_2: 3072×768│
│                                     Activación                 │
│                                     no lineal                  │
└────────────────────────────────────────────────────────────────┘
```

| Componente | Dimensiones | Descripción |
|------------|-------------|-------------|
| Entrada | d_model = 768 | Vector del token |
| Capa oculta | d_ff = 3072 (4 × 768) | Expansión para mayor capacidad |
| Activación | GELU | Función de activación suave |
| Salida | d_model = 768 | De vuelta a la dimensión original |

#### ¿Para qué sirve la FFN?

Investigaciones recientes han mostrado que:

- **La atención captura relaciones contextuales** entre tokens (quién se relaciona con quién)
- **La FFN almacena conocimiento factual** (hechos del mundo aprendidos durante el entrenamiento)

```
Atención: "París" se relaciona con "Francia" en esta oración
FFN:      "París" → "capital", "Torre Eiffel", "río Sena" (conocimiento almacenado)
```

### 3.3 Conexiones Residuales (Skip Connections)

Las conexiones residuales son un componente crítico que permite entrenar redes profundas.

#### Fórmula

```
output = sublayer(input) + input
```

Es decir, la salida de cada subcapa se **suma** con su entrada original.

```
┌────────────────────────────────────────────────────────────────┐
│                  CONEXIÓN RESIDUAL                             │
│                                                                │
│   input ──────────────────────────────┐                        │
│     │                                 │                        │
│     ▼                                 │                        │
│  ┌─────────────┐                      │  (identidad)           │
│  │  Subcapa    │                      │                        │
│  │  (Atención  │                      │                        │
│  │   o FFN)    │                      │                        │
│  └──────┬──────┘                      │                        │
│         │                             │                        │
│         └──────────── + ◄─────────────┘                        │
│                       │                                        │
│                       ▼                                        │
│                    output                                      │
└────────────────────────────────────────────────────────────────┘
```

#### ¿Por qué son importantes?

1. **Flujo de gradientes**: Permiten que los gradientes fluyan directamente hacia las capas iniciales sin degradarse (resuelven el problema del vanishing gradient).
2. **Aprendizaje incremental**: Cada capa aprende una "corrección" o "refinamiento" sobre la entrada, no una transformación completa.
3. **Profundidad**: Hacen posible entrenar modelos con decenas o cientos de capas.

### 3.4 Layer Normalization

La normalización de capa estabiliza el entrenamiento al normalizar las activaciones dentro de cada ejemplo.

#### Fórmula

```
LayerNorm(x) = γ × (x - μ) / σ + β

donde:
    μ = media de x (a lo largo de la dimensión del modelo)
    σ = desviación estándar de x
    γ = parámetro de escala aprendido
    β = parámetro de desplazamiento aprendido
```

#### Diferencia con Batch Normalization

| Característica | Batch Norm | Layer Norm |
|---------------|------------|------------|
| Normaliza sobre | El batch (entre ejemplos) | Las features (dentro del ejemplo) |
| Dependencia del batch | Sí | No |
| Uso en secuencias | Problemático | Ideal |
| Entrenamiento vs inferencia | Diferente comportamiento | Mismo comportamiento |

### 3.5 El Bloque "Add & Norm"

Cada subcapa del Transformer está envuelta en un patrón "Add & Norm":

```
output = LayerNorm(x + sublayer(x))
```

Este patrón combina las conexiones residuales con la normalización:

```
┌────────────────────────────────────────────────────────────────┐
│                   BLOQUE ADD & NORM                            │
│                                                                │
│   input ──────────────────┐                                    │
│     │                     │                                    │
│     ▼                     │                                    │
│  ┌─────────────┐          │                                    │
│  │  Subcapa    │          │  (skip connection)                 │
│  └──────┬──────┘          │                                    │
│         │                 │                                    │
│         └──── ADD ◄───────┘                                    │
│               │                                                │
│               ▼                                                │
│        ┌──────────────┐                                        │
│        │  LayerNorm   │                                        │
│        └──────┬───────┘                                        │
│               │                                                │
│               ▼                                                │
│            output                                              │
└────────────────────────────────────────────────────────────────┘
```

### 3.6 Bloque Transformer Completo

Combinando todos los componentes, un bloque completo del Transformer tiene esta estructura:

```
┌────────────────────────────────────────────────────────────────┐
│              BLOQUE TRANSFORMER (ENCODER)                      │
│                                                                │
│   Input                                                        │
│     │                                                          │
│     ├─────────────────────────┐                                │
│     ▼                         │                                │
│  ┌──────────────────────┐     │                                │
│  │  Multi-Head Attention│     │  (residual)                    │
│  └──────────┬───────────┘     │                                │
│             │                 │                                │
│             └──── ADD ◄───────┘                                │
│                   │                                            │
│                   ▼                                            │
│            ┌──────────────┐                                    │
│            │  LayerNorm   │                                    │
│            └──────┬───────┘                                    │
│                   │                                            │
│                   ├─────────────────────────┐                  │
│                   ▼                         │                  │
│            ┌──────────────┐                 │                  │
│            │  Feed-Forward│                 │  (residual)      │
│            └──────┬───────┘                 │                  │
│                   │                         │                  │
│                   └──── ADD ◄───────────────┘                  │
│                         │                                      │
│                         ▼                                      │
│                  ┌──────────────┐                              │
│                  │  LayerNorm   │                              │
│                  └──────┬───────┘                              │
│                         │                                      │
│                         ▼                                      │
│                      Output                                    │
└────────────────────────────────────────────────────────────────┘
```

### 3.7 Pseudocódigo: Encoder Block y Decoder Block

#### Encoder Block

```python
def encoder_block(x):
    # Sub-capa 1: Multi-Head Self-Attention + Add & Norm
    attn_output = multi_head_attention(x, x, x)   # Q=x, K=x, V=x
    x = layer_norm(x + attn_output)                # Residual + Norm

    # Sub-capa 2: Feed-Forward Network + Add & Norm
    ffn_output = feed_forward(x)
    x = layer_norm(x + ffn_output)                 # Residual + Norm

    return x
```

#### Decoder Block

```python
def decoder_block(x, encoder_output):
    # Sub-capa 1: Masked Multi-Head Self-Attention + Add & Norm
    masked_attn_output = masked_multi_head_attention(x, x, x)
    x = layer_norm(x + masked_attn_output)

    # Sub-capa 2: Cross-Attention con el encoder + Add & Norm
    cross_attn_output = multi_head_attention(x, encoder_output, encoder_output)
    x = layer_norm(x + cross_attn_output)          # Q=x, K=enc, V=enc

    # Sub-capa 3: Feed-Forward Network + Add & Norm
    ffn_output = feed_forward(x)
    x = layer_norm(x + ffn_output)

    return x
```

**Diferencias clave entre encoder y decoder:**

| Aspecto | Encoder Block | Decoder Block |
|---------|---------------|---------------|
| Self-Attention | Bidireccional (ve todo) | Causal/enmascarada (solo pasado) |
| Cross-Attention | No tiene | Sí (atiende al encoder) |
| Subcapas | 2 | 3 |

---

## Bloque 4: Masked Attention y Tipos de Arquitectura

### 4.1 Masked Self-Attention (Atención Enmascarada)

En la generación de texto, el modelo debe predecir el siguiente token **sin ver los tokens futuros**. Para lograr esto, se aplica una **máscara causal** (triangular inferior).

#### ¿Cómo funciona?

```
Oración: "El gato come pescado"

Sin máscara (encoder - bidireccional):
        El  gato  come  pescado
El     [ ✓    ✓     ✓      ✓  ]    ← "El" ve todos los tokens
gato   [ ✓    ✓     ✓      ✓  ]
come   [ ✓    ✓     ✓      ✓  ]
pescado[ ✓    ✓     ✓      ✓  ]

Con máscara causal (decoder - unidireccional):
        El  gato  come  pescado
El     [ ✓    ✗     ✗      ✗  ]    ← "El" solo se ve a sí mismo
gato   [ ✓    ✓     ✗      ✗  ]    ← "gato" ve "El" y a sí mismo
come   [ ✓    ✓     ✓      ✗  ]    ← "come" ve los 3 anteriores
pescado[ ✓    ✓     ✓      ✓  ]    ← "pescado" ve todo lo anterior
```

La máscara funciona poniendo **-infinito** en las posiciones no permitidas antes del softmax, lo que resulta en pesos de atención de 0.

#### Implementación de la Máscara Causal

```python
import numpy as np

def create_causal_mask(seq_len):
    """
    Crea una máscara causal (triangular inferior).
    Posiciones futuras se enmascaran con -infinito.
    """
    # Crear matriz de unos (triangular inferior)
    mask = np.tril(np.ones((seq_len, seq_len)))

    # Convertir 0s a -infinito y 1s a 0
    mask = np.where(mask == 0, float('-inf'), 0.0)

    return mask

# Ejemplo para secuencia de 4 tokens
mask = create_causal_mask(4)
print(mask)
# [[ 0.   -inf  -inf  -inf]
#  [ 0.    0.   -inf  -inf]
#  [ 0.    0.    0.   -inf]
#  [ 0.    0.    0.    0. ]]
```

#### Aplicación de la máscara

```python
def masked_attention(Q, K, V, mask):
    d_k = Q.shape[-1]
    scores = (Q @ K.transpose(-2, -1)) / np.sqrt(d_k)

    # Aplicar la máscara ANTES del softmax
    scores = scores + mask    # -inf positions → 0 after softmax

    weights = softmax(scores, axis=-1)
    output = weights @ V
    return output
```

### 4.2 Tres Tipos de Arquitectura Transformer

A partir de la arquitectura Transformer original, se han desarrollado tres variantes principales:

```
┌─────────────────────────────────────────────────────────────┐
│               TIPOS DE ARQUITECTURA TRANSFORMER             │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │   ENCODER    │  │   DECODER    │  │ ENCODER-DECODER  │   │
│  │    ONLY      │  │    ONLY      │  │                  │   │
│  │              │  │              │  │  ┌─────┐ ┌─────┐ │   │
│  │  ┌────────┐  │  │  ┌────────┐  │  │  │ ENC │→│ DEC │ │   │
│  │  │ Encoder│  │  │  │Decoder │  │  │  └─────┘ └─────┘ │   │
│  │  │ Blocks │  │  │  │ Blocks │  │  │                  │   │
│  │  └────────┘  │  │  └────────┘  │  │                  │   │
│  │              │  │              │  │                  │   │
│  │ Bidireccional│  │  Causal      │  │  Seq-to-Seq      │   │
│  │              │  │  (izq→der)   │  │                  │   │
│  └──────────────┘  └──────────────┘  └──────────────────┘   │
│                                                             │
│  BERT, RoBERTa     GPT, Claude       T5, BART               │
│  ALBERT            LLaMA, Mistral    mT5                    │
│                    Gemini                                   │
└─────────────────────────────────────────────────────────────┘
```

#### Tabla Comparativa Completa

| Característica | Encoder-only | Decoder-only | Encoder-Decoder |
|---------------|-------------|-------------|-----------------|
| **Modelos** | BERT, RoBERTa, ALBERT | GPT, Claude, LLaMA, Mistral, Gemini | T5, BART, mT5 |
| **Atención** | Bidireccional | Causal (unidireccional) | Bidireccional (enc) + causal (dec) |
| **Entrenamiento** | MLM (Masked Language Modeling) | Next token prediction | Seq-to-seq con teacher forcing |
| **Casos de uso principales** | Clasificación, NER, búsqueda semántica | Generación de texto, chat, código | Traducción, resumen, paráfrasis |
| **Ventaja principal** | Comprensión profunda del contexto | Versatilidad en generación | Mapeo entrada→salida |
| **Limitación** | No genera texto fluido | No tiene representación bidireccional | Mayor complejidad arquitectónica |

### 4.3 Encoder-Only: Comprensión Bidireccional

Los modelos encoder-only ven **toda la secuencia a la vez**, lo que les da una comprensión profunda del contexto completo.

```
Ejemplo: Clasificación de sentimiento

Input:  "La película fue aburrida pero el final fue sorprendente"

Encoder bidireccional:
- "aburrida" atiende a "película" y a "pero" y a "sorprendente"
- Captura la estructura completa: sentimiento mixto

Output: [CLS] token → clasificación
```

**Modelos representativos:**
- **BERT** (Google, 2018): 110M / 340M parámetros
- **RoBERTa** (Facebook/Meta, 2019): Entrenamiento optimizado de BERT
- **ALBERT** (Google, 2019): Versión ligera con compartición de parámetros

### 4.4 Decoder-Only: Generación Causal

Los modelos decoder-only generan texto **de izquierda a derecha**, prediciendo el siguiente token basándose solo en los tokens anteriores.

```
Ejemplo: Generación de texto

Prompt:  "La inteligencia artificial"
Paso 1:  "La inteligencia artificial es"      (predice "es")
Paso 2:  "La inteligencia artificial es una"   (predice "una")
Paso 3:  "La inteligencia artificial es una rama" (predice "rama")
...

Cada paso solo ve lo que hay a la izquierda (máscara causal).
```

**Modelos representativos:**
- **GPT-4** (OpenAI): Modelo multimodal, razonamiento avanzado
- **Claude** (Anthropic): Enfoque en seguridad y utilidad
- **LLaMA** (Meta): Modelos abiertos de alto rendimiento
- **Mistral** (Mistral AI): Eficiencia con mecanismos de atención optimizados
- **Gemini** (Google): Modelo multimodal nativo

### 4.5 Encoder-Decoder: Transformación Secuencia a Secuencia

Los modelos encoder-decoder procesan una secuencia de entrada completa (encoder) y generan una secuencia de salida (decoder), con cross-attention conectando ambos.

```
Ejemplo: Traducción

Encoder input:  "The cat sat on the mat"
                    │
                    ▼ (cross-attention)
                    │
Decoder output: "El gato se sentó en la alfombra"
```

**Modelos representativos:**
- **T5** (Google): "Text-to-Text Transfer Transformer"
- **BART** (Facebook/Meta): Denoising autoencoder
- **mT5** (Google): Versión multilingüe de T5

### 4.6 ¿Por qué Dominan los Modelos Decoder-Only?

En la actualidad, la mayoría de los modelos de lenguaje más potentes son decoder-only. Las razones principales son:

| Razón | Explicación |
|-------|-------------|
| **Simplicidad** | Una sola pila de bloques, más fácil de escalar |
| **Versatilidad** | Un mismo modelo sirve para generación, clasificación, resumen, código, razonamiento |
| **Eficiencia de entrenamiento** | Next-token prediction es un objetivo simple y universal |
| **Capacidades emergentes** | Al escalar, surgen habilidades no programadas explícitamente (razonamiento, few-shot learning, CoT) |

```
┌──────────────────────────────────────────────────────────────┐
│            ¿POR QUÉ DECODER-ONLY DOMINA?                     │
│                                                              │
│   Escala                                                     │
│     ▲                                                        │
│     │           ★ GPT-4, Claude, Gemini                      │
│     │         ★ LLaMA 3                                      │
│     │       ★ Mistral                                        │
│     │                                                        │
│     │   Una arquitectura simple                              │
│     │   + Un objetivo simple (next token)                    │
│     │   + Datos masivos                                      │
│     │   = Capacidades emergentes extraordinarias             │
│     │                                                        │
│     └──────────────────────────────────────────────► Tiempo  │
│         2017   2018   2019   2020   2021   2022   2023+      │
└──────────────────────────────────────────────────────────────┘
```

---

## Bloque 5: Ejercicio Práctico Guiado

### 5.1 Referencia a Ejercicios

A continuación se presentan los ejercicios guiados que realizaremos en clase.

### 5.2 Ejercicio 1: Cálculo Manual de Self-Attention

**Objetivo**: Consolidar la comprensión del mecanismo de atención calculando paso a paso.

Dados los siguientes valores para una secuencia de 2 tokens con dimensión d_k = 2:

```
Q = [[1, 0],     K = [[0, 1],     V = [[1, 3],
     [0, 1]]          [1, 0]]          [2, 4]]
```

**Tareas:**

1. Calcular la matriz de scores: `Q × K^T`
2. Escalar por `√d_k`
3. Aplicar softmax a cada fila
4. Calcular la salida: pesos × V
5. Interpretar los resultados: ¿A quién presta más atención cada token?

```
Espacio de trabajo:

Paso 1: Scores = Q × K^T
┌─────────┐   ┌─────────┐   ┌─────────┐
│  1   0  │ × │  0   1  │ = │  ?   ?  │
│  0   1  │   │  1   0  │   │  ?   ?  │
└─────────┘   └─────────┘   └─────────┘

Paso 2: Escalar ÷ √2 ≈ 1.414
...

Paso 3: Softmax por filas
...

Paso 4: Pesos × V
...
```

### 5.3 Ejercicio 2: Análisis de Arquitecturas

**Objetivo**: Determinar qué tipo de arquitectura Transformer es más adecuada para diferentes tareas.

Para cada tarea, indica el tipo de arquitectura más adecuado y justifica tu elección:

| Tarea | Tipo de Arquitectura | Justificación |
|-------|---------------------|---------------|
| Clasificación de emails como spam/no spam | ¿? | ¿? |
| Chatbot de atención al cliente | ¿? | ¿? |
| Traducción automática español → inglés | ¿? | ¿? |
| Generación de código a partir de descripción | ¿? | ¿? |
| Búsqueda semántica en documentos | ¿? | ¿? |
| Resumen automático de artículos | ¿? | ¿? |

### 5.4 Herramientas de Visualización

Para una comprensión más profunda de los mecanismos de atención, se recomienda explorar:

- **BertViz**: Herramienta interactiva para visualizar patrones de atención en modelos Transformer. Permite inspeccionar cada cabeza de atención y cada capa.
  - Instalación: `pip install bertviz`
  - Documentación: https://github.com/jessevig/bertviz

- **Attention Pattern Explorer**: Visualización de mapas de atención en tiempo real.

- **TransformerLens**: Biblioteca para interpretabilidad mecanística de Transformers.

```python
# Ejemplo básico con BertViz
from bertviz import head_view
from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased", output_attentions=True)

inputs = tokenizer("The cat sat on the mat", return_tensors="pt")
outputs = model(**inputs)
attention = outputs.attentions  # Tuple de tensores de atención

head_view(attention, tokenizer.convert_ids_to_tokens(inputs["input_ids"][0]))
```

---

## Resumen de la Sesión

### Conceptos Clave

1. **Self-Attention** permite que cada token atienda a todos los demás tokens de la secuencia, creando representaciones contextualizadas mediante las matrices Q (Query), K (Key) y V (Value).

2. **Multi-Head Attention** ejecuta múltiples mecanismos de atención en paralelo, donde cada cabeza captura diferentes tipos de relaciones (sintácticas, semánticas, de correferencia, de largo alcance).

3. **Feed-Forward Networks (FFN)** procesan cada posición de forma independiente con una expansión 4x, almacenando conocimiento factual aprendido durante el entrenamiento.

4. **Conexiones residuales y Layer Normalization** estabilizan el entrenamiento de redes profundas, permitiendo el flujo de gradientes y el aprendizaje incremental.

5. **Masked Self-Attention** restringe la atención a posiciones anteriores mediante una máscara causal, siendo esencial para la generación autoregresiva de texto.

6. **Tres tipos de arquitectura** (encoder-only, decoder-only, encoder-decoder) se adaptan a diferentes tareas, con los modelos decoder-only dominando el panorama actual por su simplicidad, versatilidad y capacidades emergentes al escalar.

---

## Conexión con la Sesión 2

En la próxima sesión abordaremos la integración práctica con APIs de modelos de lenguaje modernos:

- **API de OpenAI**: Chat Completions, modelos GPT, parámetros de generación
- **API de Gemini (Google)**: Integración con el ecosistema de Google
- **API de Claude (Anthropic)**: Mensajes, system prompts, herramientas
- **LangChain**: Framework para orquestar llamadas a LLMs, cadenas y agentes
- **Comparativa práctica**: Diferencias de rendimiento, costo y capacidades entre proveedores
- **Proyecto integrador**: Construcción de una aplicación que utilice múltiples APIs

---

## Actividades

### Ejercicios de esta Sesión

Completa los ejercicios prácticos disponibles en [ejercicios.md](./ejercicios.md):

1. **Cálculo manual de Self-Attention** - Calcular paso a paso con valores numéricos
2. **Análisis de arquitecturas** - Seleccionar la arquitectura adecuada para cada tarea
3. **Interpretación de mapas de atención** - Analizar y explicar patrones de atención
4. **Implementación de componentes** - Codificar atención, FFN y normalización
5. **Comparación Multi-Head vs Single-Head** - Evaluar el impacto de múltiples cabezas

---

## Referencias

- Vaswani, A., Shazeer, N., Parmar, N., et al. (2017). *Attention Is All You Need*. Advances in Neural Information Processing Systems (NeurIPS).
- Alammar, J. (2018). *The Illustrated Transformer*. https://jalammar.github.io/illustrated-transformer/
- Devlin, J., Chang, M., Lee, K., & Toutanova, K. (2019). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. NAACL.
- Radford, A., et al. (2019). *Language Models are Unsupervised Multitask Learners*. OpenAI.
- Touvron, H., et al. (2023). *LLaMA: Open and Efficient Foundation Language Models*. Meta AI.
- Vig, J. (2019). *BertViz: A Tool for Visualizing Multi-Head Self-Attention in the BERT Model*. ICLR Workshop.
- Elhage, N., et al. (2021). *A Mathematical Framework for Transformer Circuits*. Anthropic.
