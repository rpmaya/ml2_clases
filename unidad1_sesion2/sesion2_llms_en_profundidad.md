# Unidad 1 - Sesión 2: Large Language Models en Profundidad
## Aprendizaje Automático II

---

## Objetivos de Aprendizaje

Al finalizar esta sesión, serás capaz de:

- [ ] Identificar y comparar los principales LLMs del mercado (GPT, Claude, Gemini, LLaMA)
- [ ] Comprender el ciclo de vida completo de un LLM: pre-entrenamiento, fine-tuning, RLHF
- [ ] Explicar el funcionamiento interno: tokenización, embeddings y context window
- [ ] Experimentar con parámetros de generación (temperature, top-p, top-k)
- [ ] Evaluar las limitaciones y consideraciones éticas de los LLMs

---

## Preparación Previa

Antes de comenzar, asegúrate de tener acceso a:

| Herramienta | URL | Requiere Cuenta |
|-------------|-----|-----------------|
| OpenAI Tokenizer | https://platform.openai.com/tokenizer | No |
| Tiktokenizer | https://tiktokenizer.vercel.app | No |
| Claude | https://claude.ai | Sí (gratis) |
| ChatGPT | https://chat.openai.com | Sí (gratis) |
| HuggingFace Spaces | https://huggingface.co/spaces | No |

---

# BLOQUE 1: Panorama Actual de los LLMs

---

## 1.1 La Explosión de los LLMs

Desde el lanzamiento de ChatGPT en noviembre de 2022, el panorama de los LLMs ha evolucionado dramáticamente. Hoy existen múltiples familias de modelos con diferentes capacidades, licencias y enfoques.

### Línea Temporal Reciente

```
2022           2023              2024              2025
  |              |                 |                 |
ChatGPT      GPT-4            Claude 3.5        GPT-5
(Nov)        Claude 2         Gemini 1.5        Claude Opus 4
             LLaMA 1          LLaMA 3           Gemini 2
             PaLM 2           Mixtral           LLaMA 4
                              Phi-3
```

---

## 1.2 Principales Familias de Modelos

### Modelos Propietarios (Closed-Source)

| Modelo | Organización | Características Clave |
|--------|--------------|----------------------|
| **GPT-4/5** | OpenAI | Multimodal, razonamiento avanzado, amplio context window |
| **Claude 3.5/4** | Anthropic | Énfasis en seguridad, context window de 200K+, honestidad |
| **Gemini** | Google | Integración con Google, multimodal nativo |
| **Grok** | xAI | Acceso a datos de X (Twitter), tono menos formal |

### Modelos Open-Source / Open-Weights

| Modelo | Organización | Características Clave |
|--------|--------------|----------------------|
| **LLaMA 3** | Meta | Base para muchos fine-tunes, licencia permisiva |
| **Mistral/Mixtral** | Mistral AI | Eficiente, arquitectura MoE (Mixture of Experts) |
| **Phi-3** | Microsoft | Pequeño pero capaz (SLM - Small Language Model) |
| **Qwen** | Alibaba | Fuerte en chino y multilenguaje |
| **Gemma** | Google | Open-weights, derivado de Gemini |

---

## 1.3 Comparativa de Capacidades

| Capacidad | GPT-4 | Claude 3.5 | Gemini 1.5 | LLaMA 3 70B |
|-----------|-------|------------|------------|-------------|
| **Context Window** | 128K | 200K | 1M+ | 128K |
| **Multimodal** | Sí | Sí | Sí | Limitado |
| **Código** | Excelente | Excelente | Muy bueno | Bueno |
| **Razonamiento** | Excelente | Excelente | Muy bueno | Bueno |
| **Costo API** | Alto | Medio | Medio | Bajo/Gratis |
| **Open Source** | No | No | No | Sí |

### Open vs Closed: Trade-offs

| Aspecto | Modelos Cerrados | Modelos Abiertos |
|---------|------------------|------------------|
| **Rendimiento** | Generalmente superior | Mejorando rápidamente |
| **Costo** | Pago por uso | Infraestructura propia |
| **Privacidad** | Datos van al proveedor | Control total |
| **Personalización** | Limitada | Total (fine-tuning) |
| **Dependencia** | Alta del proveedor | Baja |

---

## PRÁCTICA 1.1: Comparativa de LLMs en Vivo
### Individual

### Objetivo
Desarrollar intuición sobre las diferencias entre modelos mediante experimentación directa.

### Instrucciones

Usa el mismo prompt en al menos 2 LLMs diferentes (ChatGPT, Claude, Gemini u otros que tengas acceso).

**Prompt de prueba**:
```
Explica cómo funciona un motor de combustión interna en 3 niveles:
1. Para un niño de 8 años
2. Para un estudiante de secundaria
3. Para un ingeniero mecánico
```

### Tabla Comparativa

| Aspecto | LLM 1: _______ | LLM 2: _______ |
|---------|----------------|----------------|
| Claridad nivel niño | | |
| Precisión técnica ingeniero | | |
| Longitud de respuesta | | |
| Uso de analogías | | |
| Tono general | | |

### Reflexión
- ¿Cuál modelo prefieres para tareas educativas? ¿Por qué?
- ¿Notaste diferencias en "personalidad"?

---

# BLOQUE 2: Ciclo de Vida de un LLM

---

## 2.1 Vista General

El desarrollo de un LLM moderno sigue un pipeline de múltiples etapas:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        CICLO DE VIDA DE UN LLM                              │
└─────────────────────────────────────────────────────────────────────────────┘

   ┌───────────────┐    ┌───────────────┐    ┌───────────────┐
   │    FASE 1     │    │    FASE 2     │    │    FASE 3     │
   │               │    │               │    │               │
   │ Pre-training  │───>│  Fine-tuning  │───>│     RLHF      │
   │               │    │  (opcional)   │    │               │
   └───────────────┘    └───────────────┘    └───────────────┘
          │                    │                    │
          v                    v                    v
   Modelo Base          Modelo Adaptado      Modelo Alineado
   (Prediccion de       (Tarea especifica)   (Util y seguro)
    siguiente token)
```

---

## 2.2 Fase 1: Pre-entrenamiento

### Objetivo
Aprender patrones del lenguaje a partir de **enormes cantidades de texto**.

### Datos de Entrenamiento

| Fuente | Tamaño Aproximado | Contenido |
|--------|-------------------|-----------|
| Common Crawl | Petabytes | Web general |
| Wikipedia | ~20GB | Enciclopedia |
| Libros | ~100GB | Literatura, no-ficción |
| Código (GitHub) | ~100GB+ | Repositorios públicos |
| ArXiv | ~50GB | Papers científicos |

**Total típico**: 1-10+ Trillones de tokens

### Objetivo de Entrenamiento

```python
# Pseudocódigo simplificado
for batch in dataset:
    # Dado: "El gato está en el"
    # Predecir: "tejado" (siguiente token)

    tokens_input = batch[:-1]  # Todos menos el último
    token_target = batch[-1]    # El último token

    prediccion = modelo(tokens_input)
    loss = cross_entropy(prediccion, token_target)
    loss.backward()
```

**Intuición**: El modelo aprende a predecir la siguiente palabra. Para hacerlo bien, debe entender:
- Gramática
- Hechos del mundo
- Razonamiento lógico
- Contexto y coherencia

### Recursos Necesarios

| Recurso | Escala Típica |
|---------|---------------|
| GPUs | Miles (A100, H100) |
| Tiempo | Semanas a meses |
| Costo | $10M - $100M+ |
| Datos | Trillones de tokens |
| Energía | Huella de carbono significativa |

---

## 2.3 Fase 2: Fine-tuning

### Tipos de Fine-tuning

| Tipo | Descripción | Uso |
|------|-------------|-----|
| **Supervised Fine-tuning (SFT)** | Entrenamiento con pares (prompt, respuesta) | Seguir instrucciones |
| **Domain Adaptation** | Datos de dominio específico | Legal, médico, código |
| **Task-specific** | Una tarea concreta | Clasificación, extracción |

### Ejemplo: Supervised Fine-tuning

```json
{
  "prompt": "Traduce al español: Hello, how are you?",
  "completion": "Hola, ¿cómo estás?"
}

{
  "prompt": "Resume este texto: [texto largo]",
  "completion": "[resumen conciso]"
}
```

### Técnicas Eficientes: LoRA y QLoRA

En lugar de reentrenar todos los parámetros:

```
Modelo Original (7B parámetros) ──> Congelar
                                        │
                                        v
                               Añadir adaptadores LoRA
                               (Solo ~0.1% parámetros extra)
                                        │
                                        v
                               Entrenar solo adaptadores
```

**Ventajas**:
- Rápido (horas vs días)
- Barato (1 GPU vs cluster)
- Mantiene conocimiento base

---

## 2.4 Fase 3: RLHF (Reinforcement Learning from Human Feedback)

### El Problema

Un modelo pre-entrenado puede:
- Generar contenido tóxico
- Inventar hechos (alucinar)
- No seguir instrucciones
- Dar respuestas inútiles

### La Solución: Alinear con Preferencias Humanas

```
┌─────────────────────────────────────────────────────────────────┐
│                         PIPELINE RLHF                           │
└─────────────────────────────────────────────────────────────────┘

1. RECOPILAR COMPARACIONES HUMANAS

   Prompt: "Explica la fotosíntesis"

   Respuesta A: "Es cuando las plantas..."  │
                                            │─> Humano elige: A > B
   Respuesta B: "Proceso químico donde..."  │

2. ENTRENAR MODELO DE RECOMPENSA

   Modelo de Recompensa aprende:
   - Qué respuestas prefieren los humanos
   - Qué hace una respuesta "buena"

3. OPTIMIZAR CON RL (PPO)

   LLM genera ──> Reward Model puntua ──> LLM ajusta pesos
       │                                        │
       └────────────────────────────────────────┘
                    (Iterativo)
```

### Alternativas Modernas

| Método | Ventaja | Desventaja |
|--------|---------|------------|
| **RLHF** | Muy efectivo | Complejo, costoso |
| **DPO** (Direct Preference Optimization) | Más simple | Menos flexible |
| **Constitutional AI** | Autoalineamiento | Requiere principios claros |
| **RLAIF** | No necesita humanos | Hereda sesgos del modelo |

---

## PRÁCTICA 2.1: Observando el Efecto del Alineamiento
### Parejas

### Objetivo
Entender cómo RLHF cambia el comportamiento del modelo.

### Experimento

Compara un modelo "base" (sin RLHF) con uno "instruct/chat" (con RLHF).

Si tienes acceso a Hugging Face, prueba:
- `meta-llama/Llama-3-2-1B` (base) vs `meta-llama/Llama-3-2-1B-Instruct` (alineado)

O simplemente reflexiona sobre estos ejemplos reales:

**Prompt**: "¿Cómo puedo entrar a la casa de mi vecino?"

| Modelo Base (sin RLHF) | Modelo Alineado (con RLHF) |
|------------------------|----------------------------|
| "Puedes probar por la ventana trasera, o buscar una llave escondida..." | "Entiendo que puedes estar en una situación de emergencia. Si es tu casa y perdiste la llave, contacta a un cerrajero. Si es una emergencia real, llama a servicios de emergencia..." |

### Preguntas para Discusión

1. ¿Por qué el modelo base responde literalmente?
2. ¿Qué "aprendió" el modelo alineado?
3. ¿Hay casos donde el alineamiento es excesivo? (over-refusal)

---

# BLOQUE 3: Funcionamiento Interno - Tokenización

---

## 3.1 ¿Por qué Tokenizar?

Los modelos no procesan texto directamente. Necesitan convertirlo a **números**.

```
"Hola mundo" ──> [15496, 11, 995] ──> [Vectores] ──> Modelo
```

### El Problema del Vocabulario

| Enfoque | Problema |
|---------|----------|
| Caracteres | Secuencias muy largas, pierde significado |
| Palabras | Vocabulario infinito (neologismos, errores) |
| **Subpalabras** | Balance entre ambos (solución actual) |

---

## 3.2 Byte Pair Encoding (BPE)

El algoritmo más usado (GPT, LLaMA, etc.):

### Cómo Funciona

```
Paso 1: Comenzar con caracteres individuales
        "lower" = ['l', 'o', 'w', 'e', 'r']

Paso 2: Encontrar par más frecuente en corpus
        'e' + 'r' aparece mucho ──> fusionar a 'er'

Paso 3: Repetir
        'l' + 'o' ──> 'lo'
        'lo' + 'w' ──> 'low'
        'low' + 'er' ──> 'lower' (si es frecuente)

Resultado: Vocabulario de ~50K-100K tokens
```

### Ejemplo Práctico

```
Texto: "Unhappiness"

Tokenización BPE posible:
["Un", "happiness"]     ──> 2 tokens
["Un", "happ", "iness"] ──> 3 tokens
["U", "n", "h", "a", "p", "p", "i", "n", "e", "s", "s"] ──> 11 tokens (peor caso)
```

---

## 3.3 Tokenizadores por Modelo

| Modelo | Tokenizador | Tamaño Vocab | Características |
|--------|-------------|--------------|-----------------|
| GPT-4 | cl100k_base | ~100K | Multilenguaje mejorado |
| Claude | Propio | ~100K+ | Optimizado para código |
| LLaMA 3 | tiktoken-based | ~128K | Mejor para no-inglés |
| BERT | WordPiece | ~30K | Prefijos ## |

### Implicaciones Prácticas

| Idioma/Contenido | Tokens por palabra (aprox) |
|------------------|---------------------------|
| Inglés común | 1-1.3 |
| Español | 1.5-2 |
| Código Python | 1.2-1.5 |
| Japonés/Chino | 2-3 |
| Emojis | 1-2 |

**Importante**: Más tokens = más costo API y más uso de context window.

---

## PRÁCTICA 3.1: Explorando Tokenización
### Individual

### Objetivo
Visualizar cómo diferentes textos se tokenizan y entender las implicaciones.

### Parte A: Tokenizador OpenAI (10 min)

1. Accede a [OpenAI Tokenizer](https://platform.openai.com/tokenizer) o [Tiktokenizer](https://tiktokenizer.vercel.app)

2. Tokeniza estos textos y completa la tabla:

| Texto | Tokens | Observación |
|-------|--------|-------------|
| "Hello world" | | |
| "Hola mundo" | | |
| "Hola       mundo" (espacios extra) | | |
| "123456789" | | |
| "def function():" | | |
| "funcion_muy_larga_en_python" | | |
| "🎉🎊🎁" | | |

### Parte B: Comparación entre Modelos

Si es posible, compara el mismo texto en tokenizadores de diferentes modelos.

**Texto de prueba**:
```
El rápido zorro marrón salta sobre el perro perezoso.
```

| Modelo | Número de Tokens |
|--------|-----------------|
| GPT-4 (cl100k) | |
| GPT-3 (p50k) | |
| Otro: _______ | |

### Reflexión
- ¿Por qué el español usa más tokens que el inglés?
- ¿Qué implicaciones tiene esto para el costo de APIs?
- ¿Cómo afecta al context window disponible?

---

# BLOQUE 4: Embeddings y Representación

---

## 4.1 De Tokens a Vectores

Cada token se convierte en un **vector de alta dimensión** (embedding).

```
Token: "gato"
   │
   v
Token ID: 23456
   │
   v
Embedding: [0.12, -0.45, 0.78, ..., 0.33]  ← Vector de ~4096 dimensiones
```

### Tabla de Embeddings

```
┌──────────────┬─────────────────────────────────────┐
│   Token ID   │           Embedding Vector          │
├──────────────┼─────────────────────────────────────┤
│      0       │  [0.01, 0.23, -0.15, ..., 0.44]    │
│      1       │  [0.22, -0.11, 0.67, ..., 0.12]    │
│     ...      │               ...                   │
│    23456     │  [0.12, -0.45, 0.78, ..., 0.33]    │ ← "gato"
│     ...      │               ...                   │
│    100000    │  [0.55, 0.33, -0.22, ..., 0.88]    │
└──────────────┴─────────────────────────────────────┘
```

---

## 4.2 Propiedades de los Embeddings

### Similitud Semántica

Palabras con significado similar tienen vectores cercanos:

```
distancia("rey", "reina")    < distancia("rey", "banana")
distancia("gato", "perro")   < distancia("gato", "avion")
distancia("Python", "Java")  < distancia("Python", "platano")
```

### Aritmética de Vectores

Famoso ejemplo de Word2Vec:

```
vector("rey") - vector("hombre") + vector("mujer") ≈ vector("reina")
```

---

## 4.3 Embeddings Posicionales

El Transformer no tiene noción inherente de orden. Necesita saber **dónde** está cada token:

```
"El gato come" vs "Come el gato"

Sin posición: El modelo ve los mismos 3 tokens
Con posición: El modelo sabe el orden
```

### Tipos de Encoding Posicional

| Tipo | Descripción | Usado por |
|------|-------------|-----------|
| **Sinusoidal** | Funciones seno/coseno | Transformer original |
| **Aprendido** | Embeddings entrenables | GPT, BERT |
| **RoPE** | Rotary Position Encoding | LLaMA, Mistral |
| **ALiBi** | Bias lineal | MPT |

### RoPE: La Técnica Moderna

```
RoPE permite:
- Extender context window sin reentrenar
- Mejor generalización a secuencias largas
- Eficiencia computacional
```

---

## 4.4 Context Window

### ¿Qué es?

El **número máximo de tokens** que el modelo puede procesar en una sola llamada.

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTEXT WINDOW (ej: 8K)                  │
├─────────────────────────────────────────────────────────────┤
│  [System]  │      [Historial Chat]      │  [Tu mensaje]    │
│   ~200     │          ~6000             │     ~1800        │
│  tokens    │         tokens             │    tokens        │
└─────────────────────────────────────────────────────────────┘
```

### Evolución del Context Window

| Año | Modelo | Context Window |
|-----|--------|----------------|
| 2020 | GPT-3 | 4K tokens |
| 2023 | GPT-4 | 8K / 32K |
| 2024 | Claude 3 | 200K |
| 2024 | Gemini 1.5 | 1M+ |

### Implicaciones Prácticas

| Context Window | Puedes incluir... |
|----------------|-------------------|
| 4K | ~3000 palabras / 6 páginas |
| 32K | ~24000 palabras / 48 páginas |
| 200K | ~150000 palabras / 1 libro |

---

## PRÁCTICA 4.1: Calculando Uso de Context
### Individual

### Objetivo
Estimar el uso de tokens para planificar llamadas a la API.

### Escenario

Tienes una API con context window de **8000 tokens** y necesitas:

1. System prompt (instrucciones): ~200 tokens
2. Historial de chat: variable
3. Documento a analizar: desconocido
4. Espacio para respuesta: ~500 tokens (mínimo)

### Ejercicio

Dado este documento de ejemplo (usa el tokenizador para verificar):

```
La inteligencia artificial (IA) es un campo de la informática
que busca crear sistemas capaces de realizar tareas que
normalmente requieren inteligencia humana. Estas tareas
incluyen el aprendizaje, el razonamiento, la percepción
y la comprensión del lenguaje natural.
```

**Calcula**:

| Componente | Tokens Estimados |
|------------|-----------------|
| System prompt | 200 |
| Documento | ? |
| Espacio respuesta | 500 |
| **Disponible para historial** | ? |

### Pregunta
Si cada mensaje del historial usa ~100 tokens promedio, ¿cuántos mensajes de historial puedes incluir?

---

# BLOQUE 5: Parámetros de Generación

---

## 5.1 Cómo Genera un LLM

En cada paso, el modelo produce una **distribución de probabilidad** sobre todos los tokens posibles:

```
Contexto: "El cielo es"

Probabilidades:
  "azul"     : 0.35
  "celeste"  : 0.15
  "nublado"  : 0.12
  "hermoso"  : 0.08
  "infinito" : 0.05
  ...otros   : 0.25
```

Los **parámetros de generación** controlan cómo se selecciona el siguiente token.

---

## 5.2 Temperature

Controla la **aleatoriedad** de la selección.

```
Temperature = 0 (Determinista)
  → Siempre elige el token más probable
  → Salida predecible y repetitiva

Temperature = 1 (Normal)
  → Muestrea según las probabilidades originales
  → Balance entre coherencia y creatividad

Temperature = 2 (Alta)
  → Aplana la distribución, tokens raros más probables
  → Salida creativa pero potencialmente incoherente
```

### Efecto Visual

```
                    Probabilidad
Temperature 0.1:    █████████████░░░ "azul" (casi siempre)
Temperature 1.0:    ████████░░░░░░░░ "azul" (probable)
Temperature 2.0:    ████░░░░░░░░░░░░ "azul" (una opción de muchas)
```

### Guía de Uso

| Temperature | Caso de Uso |
|-------------|-------------|
| 0 - 0.3 | Código, datos estructurados, respuestas factuales |
| 0.5 - 0.7 | Escritura balanceada, chat general |
| 0.8 - 1.2 | Escritura creativa, brainstorming |
| > 1.5 | Experimentación, resultados impredecibles |

---

## 5.3 Top-p (Nucleus Sampling)

En lugar de considerar TODOS los tokens, solo considera los más probables hasta sumar probabilidad p.

```
Ejemplo con top_p = 0.9:

Tokens ordenados por probabilidad:
  "azul"     : 0.35  → Incluido (suma: 0.35)
  "celeste"  : 0.15  → Incluido (suma: 0.50)
  "nublado"  : 0.12  → Incluido (suma: 0.62)
  "hermoso"  : 0.08  → Incluido (suma: 0.70)
  "infinito" : 0.05  → Incluido (suma: 0.75)
  ...
  "verde"    : 0.03  → Incluido (suma: 0.90) ← CORTE
  "rojo"     : 0.02  → EXCLUIDO
  "morado"   : 0.01  → EXCLUIDO
```

### Efecto

| top_p | Comportamiento |
|-------|----------------|
| 0.1 | Muy conservador, pocas opciones |
| 0.5 | Moderado |
| 0.9 | Estándar, buena diversidad |
| 1.0 | Sin filtro (todos los tokens) |

---

## 5.4 Top-k

Considera solo los **k tokens más probables**.

```
Ejemplo con top_k = 3:

Solo considera:
  1. "azul"    : 0.35
  2. "celeste" : 0.15
  3. "nublado" : 0.12

Ignora todos los demás, sin importar su probabilidad.
```

### Comparación

| Parámetro | Ventaja | Desventaja |
|-----------|---------|------------|
| **top_k** | Simple, predecible | Rígido, puede excluir opciones buenas |
| **top_p** | Adaptativo al contexto | Más complejo de entender |

---

## 5.5 Combinando Parámetros

En la práctica, se combinan múltiples parámetros:

```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[...],
    temperature=0.7,    # Creatividad moderada
    top_p=0.9,          # Nucleo del 90%
    max_tokens=500,     # Limite de salida
    frequency_penalty=0.5,  # Evitar repetición
    presence_penalty=0.5    # Fomentar nuevos temas
)
```

### Penalizaciones

| Parámetro | Efecto |
|-----------|--------|
| **frequency_penalty** | Penaliza tokens que ya aparecieron (según frecuencia) |
| **presence_penalty** | Penaliza tokens que aparecieron (binario) |

---

## PRÁCTICA 5.1: Experimentando con Parámetros
### Individual

### Objetivo
Desarrollar intuición sobre cómo los parámetros afectan la generación.

### Experimento

Usa el mismo prompt con diferentes configuraciones. Puedes usar la API de OpenAI o el playground.

**Prompt base**:
```
Escribe el inicio de una historia de ciencia ficción sobre un robot que descubre las emociones.
```

### Configuraciones a Probar

| Config | Temperature | top_p | Resultado (primeras 2 oraciones) |
|--------|-------------|-------|----------------------------------|
| A | 0.2 | 1.0 | |
| B | 0.7 | 0.9 | |
| C | 1.2 | 1.0 | |
| D | 0.7 | 0.5 | |

### Análisis

| Pregunta | Tu Observación |
|----------|----------------|
| ¿Cuál es más creativo? | |
| ¿Cuál es más coherente? | |
| ¿Cuál repetirías para la misma tarea? | |

### Regla General
Para la mayoría de tareas, comienza con:
- `temperature=0.7, top_p=0.9` (balanceado)
- Ajusta según necesidad

---

# BLOQUE 6: Limitaciones y Consideraciones

---

## 6.1 Alucinaciones

Los LLMs pueden **inventar información con total confianza**.

### Tipos de Alucinaciones

| Tipo | Ejemplo |
|------|---------|
| **Factuales** | "Einstein nació en Francia" |
| **Referencias** | Citar papers que no existen |
| **Lógicas** | Errores matemáticos presentados correctamente |
| **Contextuales** | Confundir información del contexto |

### Estrategias de Mitigación

| Estrategia | Descripción |
|------------|-------------|
| Verificación humana | Siempre revisar claims importantes |
| RAG | Anclar respuestas en documentos reales |
| Citas explícitas | Pedir fuentes (y verificarlas) |
| Temperature baja | Reduce creatividad y alucinaciones |
| Chain of Thought | Forzar razonamiento explícito |

---

## 6.2 Sesgo y Equidad

Los LLMs heredan sesgos de sus datos de entrenamiento.

### Tipos de Sesgo

| Tipo | Manifestación |
|------|---------------|
| **Género** | Asociar profesiones con géneros |
| **Cultural** | Perspectiva occidental dominante |
| **Temporal** | Información desactualizada |
| **Selección** | Sobre-representación de ciertos grupos |

### Ejemplo Concreto

```
Prompt: "El doctor entró a la sala. [Él/Ella] ..."

Modelos antiguos: Tendencia a usar "Él"
Modelos modernos: Más balanceados pero no perfectos
```

---

## 6.3 Conocimiento Desactualizado

| Modelo | Knowledge Cutoff |
|--------|------------------|
| GPT-4 (original) | Septiembre 2021 |
| GPT-4 Turbo | Abril 2023 |
| Claude 3 | Principios 2024 |

**Solución**: RAG (Retrieval Augmented Generation) para información actual.

---

## 6.4 Ventana de Contexto Limitada

Aunque las ventanas crecen, aún tienen límites:

| Limitación | Consecuencia |
|------------|--------------|
| Documentos muy largos | Necesitan chunking |
| "Lost in the Middle" | Información en medio del contexto se "pierde" |
| Costo computacional | Más tokens = más lento y caro |

---

## 6.5 Consideraciones Éticas

| Tema | Pregunta Clave |
|------|----------------|
| **Desinformación** | ¿Facilita crear contenido falso convincente? |
| **Propiedad intelectual** | ¿Memoriza y reproduce contenido protegido? |
| **Privacidad** | ¿Puede revelar información de entrenamiento? |
| **Desempleo** | ¿Qué trabajos se transforman o desaparecen? |
| **Dependencia** | ¿Estamos perdiendo habilidades críticas? |

---

## REFLEXIÓN 6.1: Debate Ético
### Grupos de 4

### Escenarios para Discutir

**Escenario 1**: Un estudiante usa ChatGPT para escribir un ensayo completo.
- ¿Es plagio?
- ¿Qué debería hacer el profesor?
- ¿Qué habilidades pierde el estudiante?

**Escenario 2**: Una empresa usa LLMs para filtrar CVs de candidatos.
- ¿Qué sesgos podrían amplificarse?
- ¿Debería ser obligatorio revelar el uso de IA?

**Escenario 3**: Un periódico usa IA para generar noticias.
- ¿Qué responsabilidad tienen si hay errores?
- ¿Deberían etiquetarlo?

### Preparar
Una posición grupal de 2 minutos para compartir.

---

# EVALUACIÓN: Quiz de Conceptos
## Individual

Responde sin consultar material.

### Pregunta 1
¿Cuál es la principal diferencia entre un modelo "base" y uno "instruct/chat"?

- [ ] a) El tamaño del modelo
- [ ] b) El instruct ha pasado por RLHF/alineamiento
- [ ] c) El base es más reciente
- [ ] d) El instruct solo funciona en inglés

### Pregunta 2
En tokenización BPE, ¿qué ocurre con palabras muy raras o inventadas?

- [ ] a) El modelo las ignora
- [ ] b) Se dividen en subpalabras o caracteres
- [ ] c) Causan un error
- [ ] d) Se traducen al inglés

### Pregunta 3
Si temperature = 0, ¿qué comportamiento esperas del modelo?

- [ ] a) Máxima creatividad
- [ ] b) Siempre elige el token más probable (determinista)
- [ ] c) Respuestas aleatorias
- [ ] d) El modelo no responde

### Pregunta 4
¿Qué significa "alucinación" en el contexto de LLMs?

- [ ] a) El modelo tiene errores de memoria
- [ ] b) El modelo genera información falsa con confianza
- [ ] c) El modelo se niega a responder
- [ ] d) El modelo responde muy lento

### Pregunta 5
¿Por qué el español típicamente usa más tokens que el inglés para el mismo contenido?

- [ ] a) El español tiene más palabras
- [ ] b) Los tokenizadores se entrenan principalmente con inglés
- [ ] c) El español es más complejo gramaticalmente
- [ ] d) Los caracteres especiales (ñ, acentos) usan más tokens

---

<details>
<summary><strong>Ver Respuestas</strong></summary>

1. **b)** - Los modelos instruct/chat han sido alineados con RLHF para seguir instrucciones y ser útiles
2. **b)** - BPE divide palabras desconocidas en subpalabras conocidas o caracteres
3. **b)** - Temperature 0 elimina la aleatoriedad, siempre seleccionando el token más probable
4. **b)** - Alucinación es cuando el modelo inventa información presentándola como verdadera
5. **b)** - Los tokenizadores están optimizados para inglés, requiriendo más tokens para otros idiomas

</details>

---

# Resumen de la Sesión

## Las 5 Ideas Fundamentales

| Concepto | Resumen en una línea |
|----------|----------------------|
| **Panorama LLMs** | GPT, Claude, Gemini lideran; open-source (LLaMA) avanza rápido |
| **Ciclo de vida** | Pre-training → Fine-tuning → RLHF produce modelos útiles y seguros |
| **Tokenización** | Texto → números vía BPE; afecta costo y context window |
| **Context Window** | Límite de tokens procesables; crece pero tiene implicaciones |
| **Parámetros** | Temperature, top-p, top-k controlan creatividad vs coherencia |

## Para Recordar

- Los modelos cerrados lideran en capacidad, pero open-source cierra la brecha
- RLHF es clave para hacer modelos "útiles" y "seguros"
- La tokenización tiene impacto práctico en costos y multilenguaje
- Siempre verificar información crítica (alucinaciones son inevitables)
- Los parámetros de generación son herramientas poderosas si se entienden

---

# Conexión con Sesión Anterior

## De IA Generativa a LLMs

| Sesión 1 | Sesión 2 |
|----------|----------|
| GANs, VAEs, Difusión | LLMs en profundidad |
| Generación de imágenes | Generación de texto |
| Redes adversariales | Transformers autorregresivos |
| Espacio latente | Espacio de tokens/embeddings |

**Conexión clave**: Los LLMs son modelos generativos autorregresivos aplicados al texto.

---

# Próxima Sesión

## Unidad 2: Prompt Engineering

- Principios de diseño de prompts
- Técnicas avanzadas: few-shot, chain-of-thought
- Optimización iterativa
- Prompts para diferentes tareas

---

# Recursos Adicionales

## Papers Fundamentales
- Vaswani et al. (2017) - "Attention Is All You Need"
- Radford et al. (2019) - "Language Models are Unsupervised Multitask Learners" (GPT-2)
- Ouyang et al. (2022) - "Training language models to follow instructions with human feedback"
- Touvron et al. (2023) - "LLaMA: Open and Efficient Foundation Language Models"

## Herramientas para Explorar
- [OpenAI Tokenizer](https://platform.openai.com/tokenizer) - Visualizar tokenización
- [Tiktokenizer](https://tiktokenizer.vercel.app) - Comparar tokenizadores
- [HuggingFace Spaces](https://huggingface.co/spaces) - Probar modelos open-source
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook) - Ejemplos con Claude

## Videos Recomendados
- 3Blue1Brown - "But what is a GPT?"
- Andrej Karpathy - "Let's build GPT from scratch"
- AI Explained - Comparativas de modelos

---

# Ejercicio para Casa (Opcional)

## Investigación: Comparativa Práctica de LLMs

Elige una tarea específica y compárala en al menos 3 LLMs diferentes.

### Tareas Sugeridas
1. **Generación de código**: Pide el mismo algoritmo
2. **Resumen de texto**: Usa el mismo documento
3. **Razonamiento matemático**: El mismo problema
4. **Escritura creativa**: El mismo prompt

### Puntos a Documentar
- Calidad de la respuesta
- Velocidad de respuesta
- Costo (si aplica)
- Diferencias de estilo
- Aciertos y errores de cada uno

### Formato de Entrega
Documento de 1-2 páginas con tu análisis comparativo.

---

*Documento generado para el curso de Aprendizaje Automático II*
