# Unidad 2 - Sesión 1: Fundamentos de Prompt Engineering

## Objetivos de la Sesión

Al finalizar esta sesión, el estudiante será capaz de:
- Comprender qué es el Prompt Engineering y su importancia en el uso de LLMs
- Identificar los componentes fundamentales de un prompt efectivo
- Aplicar técnicas básicas: zero-shot, one-shot y few-shot prompting
- Desarrollar prompts de forma iterativa siguiendo un proceso sistemático
- Estructurar outputs para obtener respuestas en formatos específicos
- Reconocer patrones comunes y anti-patrones en el diseño de prompts

---

## Bloque 1: Introducción al Prompt Engineering

### 1.1 ¿Qué es el Prompt Engineering?

El **Prompt Engineering** es la disciplina de diseñar, optimizar y refinar las instrucciones (prompts) que se proporcionan a los modelos de lenguaje para obtener respuestas útiles, precisas y alineadas con nuestros objetivos.

#### Definición Formal

> El Prompt Engineering es el proceso sistemático de estructurar texto de entrada para guiar el comportamiento de un modelo de lenguaje hacia outputs deseados, maximizando la calidad, relevancia y utilidad de las respuestas.

#### ¿Por qué es Importante?

| Sin Prompt Engineering | Con Prompt Engineering |
|------------------------|------------------------|
| Respuestas genéricas y vagas | Respuestas específicas y útiles |
| Formato inconsistente | Formato estructurado y predecible |
| Información irrelevante incluida | Solo información solicitada |
| Necesidad de múltiples intentos | Resultados óptimos en menos iteraciones |
| Difícil integración en sistemas | Fácil parseo e integración |

#### El Prompt como Interfaz

Antes de los LLMs, interactuábamos con software mediante:
- **GUIs**: Botones, menús, formularios
- **CLIs**: Comandos estructurados con sintaxis estricta
- **APIs**: Parámetros definidos en documentación

Con los LLMs, el **lenguaje natural es la interfaz**. Pero "natural" no significa "sin estructura". El Prompt Engineering es el arte de encontrar la estructura óptima dentro del lenguaje natural.

### 1.2 El Modelo Mental: El LLM como Colaborador

Para diseñar buenos prompts, es útil pensar en el LLM como un colaborador muy capaz pero con características específicas:

```
CARACTERÍSTICAS DEL "COLABORADOR" LLM:

✓ Conocimiento amplio pero estático (fecha de corte)
✓ Sigue instrucciones literalmente
✓ No tiene contexto previo de tu proyecto
✓ No puede preguntar por clarificaciones
✓ Toma decisiones basadas SOLO en el prompt
✓ Puede "alucinar" si no tiene información suficiente
```

**Implicación práctica**: Todo lo que el LLM necesita saber debe estar en el prompt o en el contexto proporcionado.

### 1.3 Niveles de Prompt Engineering

| Nivel | Descripción | Ejemplo |
|-------|-------------|---------|
| **Básico** | Preguntas directas sin estructura | "¿Qué es Python?" |
| **Intermedio** | Rol + contexto + formato | "Actúa como experto. Explica X en formato Y" |
| **Avanzado** | Técnicas especializadas | Few-shot, CoT, self-consistency |
| **Programático** | Prompts dinámicos via API | Templates con variables, pipelines |

En esta sesión cubriremos los niveles básico e intermedio. La sesión 2 profundizará en técnicas avanzadas.

---

## Bloque 2: Anatomía de un Prompt Efectivo

### 2.1 Componentes Fundamentales

Un prompt bien estructurado puede incluir los siguientes componentes:

```
┌─────────────────────────────────────────────────────────────┐
│                        PROMPT                               │
├─────────────────────────────────────────────────────────────┤
│  1. ROL         → ¿Quién debe "ser" el modelo?              │
│  2. CONTEXTO    → ¿Qué información de fondo necesita?       │
│  3. TAREA       → ¿Qué debe hacer exactamente?              │
│  4. FORMATO     → ¿Cómo debe estructurar la respuesta?      │
│  5. RESTRICCIONES → ¿Qué NO debe hacer o incluir?           │
│  6. EJEMPLOS    → ¿Hay ejemplos de input/output esperado?   │
└─────────────────────────────────────────────────────────────┘
```

No todos los prompts necesitan todos los componentes. La clave es incluir lo necesario para eliminar ambigüedad.

### 2.2 Componente 1: ROL

Asignar un rol al modelo establece el "marco mental" desde el que debe responder.

#### Ejemplos de Roles

```
# Roles genéricos
"Actúa como un experto en..."
"Eres un profesor universitario de..."
"Responde como un ingeniero senior de software..."

# Roles específicos
"Eres un revisor de código con 10 años de experiencia en Python..."
"Actúa como un copywriter especializado en tecnología B2B..."
"Eres un médico explicando a un paciente sin conocimientos técnicos..."
```

#### Impacto del Rol

| Prompt sin rol | Prompt con rol |
|----------------|----------------|
| "Explica que es una API REST" | "Actúa como un instructor de bootcamp explicando a estudiantes sin experiencia. Explica que es una API REST" |
| Respuesta técnica genérica | Respuesta adaptada al nivel, con analogias |

#### Cuidado con los Roles

- **Evitar roles poco eticos**: "Actúa como un hacker malicioso..."
- **Evitar roles contradictorios**: "Eres un experto pero no sabes nada..."
- **Ser específico**: "Experto en Python" > "Programador"

### 2.3 Componente 2: CONTEXTO

El contexto proporciona la información de fondo necesaria para una respuesta adecuada.

#### Tipos de Contexto

```
1. CONTEXTO DE DOMINIO
   "Estoy desarrollando una aplicación de e-commerce en Django..."

2. CONTEXTO DE AUDIENCIA
   "Los usuarios son personas mayores con poca experiencia tecnológica..."

3. CONTEXTO DE RESTRICCIONES TECNICAS
   "El sistema debe funcionar offline y en dispositivos con poca memoria..."

4. CONTEXTO DE OBJETIVO
   "El objetivo final es reducir el tiempo de respuesta del servidor..."
```

#### Ejemplo Comparativo

**Sin contexto:**
```
Recomienda una base de datos
```

**Con contexto:**
```
Contexto: Estoy desarrollando una aplicación móvil de mensajería
que debe manejar millones de mensajes diarios, con requisitos de
baja latencia (<50ms) y alta disponibilidad. El equipo tiene
experiencia con PostgreSQL pero está abierto a otras opciones.

Recomienda una base de datos y justifica tu elección.
```

### 2.4 Componente 3: TAREA

La tarea define exactamente lo que debe hacer el modelo. Debe ser clara, específica y actionable.

#### Verbos de Acción Útiles

| Categoría | Verbos |
|-----------|--------|
| Generación | Escribe, crea, genera, redacta, diseña |
| Análisis | Analiza, evalúa, compara, identifica, clasifica |
| Transformación | Traduce, convierte, reformatea, resume, expande |
| Explicación | Explica, describe, define, clarifica |
| Revisión | Revisa, corrige, mejora, optimiza, refactoriza |

#### Tareas Vagas vs Específicas

| Vaga | Específica |
|------|------------|
| "Ayudame con mi código" | "Revisa este código Python e identifica errores de sintaxis" |
| "Haz algo con estos datos" | "Calcula el promedio y la desviación estándar de estos valores" |
| "Mejora mi texto" | "Reescribe este párrafo para un tono más formal, manteniendo la misma longitud" |

### 2.5 Componente 4: FORMATO

Especificar el formato de salida es crucial para obtener respuestas útiles y procesables.

#### Formatos Comunes

```
# Listas
"Responde en forma de lista numerada"
"Proporciona 5 bullet points"

# Tablas
"Presenta la información en una tabla con columnas: X, Y, Z"

# Estructurado
"Responde en formato JSON con los campos: nombre, descripción, ejemplo"
"Usa formato Markdown con headers ##"

# Longitud
"Responde en máximo 3 oraciones"
"Escribe un párrafo de 100-150 palabras"
"Proporciona una respuesta detallada de al menos 500 palabras"
```

#### Ejemplo con Formato JSON

```
Analiza el siguiente texto y extrae las entidades mencionadas.

Texto: "Apple anuncio ayer que Tim Cook presentara el nuevo iPhone
en Cupertino el próximo mes."

Responde SOLO con JSON válido en este formato:
{
  "organizaciones": ["..."],
  "personas": ["..."],
  "productos": ["..."],
  "lugares": ["..."],
  "fechas": ["..."]
}
```

### 2.6 Componente 5: RESTRICCIONES

Las restricciones establecen límites claros sobre lo que el modelo NO debe hacer.

#### Tipos de Restricciones

```
# De contenido
"No incluyas opiniones personales"
"Evita jerga técnica"
"No menciones competidores"

# De formato
"No uses emojis"
"No incluyas introducciones ni conclusiones"
"Responde solo con el código, sin explicaciones"

# De comportamiento
"Si no estas seguro, indica que no tienes suficiente información"
"No inventes datos estadisticos"
"No proporciones consejos medicos o legales"
```

### 2.7 Delimitadores y Estructura Visual

Los delimitadores ayudan a separar claramente las secciones del prompt.

#### Delimitadores Comunes

```
# Comillas triples
"""
Texto a analizar aquí
"""

# XML-like tags
<contexto>
Información de contexto
</contexto>

<tarea>
Lo qué debe hacer
</tarea>

# Markdown
### Contexto
...

### Tarea
...

# Separadores
---
Sección 1
---
Sección 2
---
```

#### Ejemplo con Delimitadores

```
Eres un revisor de código experto en Python.

<código>
def calcular_promedio(lista):
    total = 0
    for num in lista:
        total += num
    return total / len(lista)
</código>

<tarea>
Revisa el código anterior e identifica:
1. Errores potenciales
2. Mejoras de rendimiento
3. Mejoras de legibilidad
</tarea>

<formato>
Para cada punto, usa el formato:
- **Problema**: descripción
- **Solución**: código corregido
</formato>
```

---

## Bloque 3: Técnicas Básicas de Prompting 

### 3.1 Zero-Shot Prompting

El modelo responde sin ningún ejemplo previo, basandose solo en su entrenamiento.

```
# Zero-shot
Clasifica el siguiente texto como positivo, negativo o neutral:

"El producto llegó a tiempo pero la calidad es inferior a lo esperado"

Clasificación:
```

**Ventajas:**
- Simple y rápido
- No requiere preparar ejemplos
- Útil para tareas comunes

**Limitaciones:**
- Puede fallar en tareas específicas o ambiguas
- Menos control sobre el formato de salida
- Resultados variables

### 3.2 One-Shot Prompting

Se proporciona un único ejemplo para guiar al modelo.

```
# One-shot
Clasifica el sentimiento del texto.

Ejemplo:
Texto: "Me encanta este restaurante, la comida es deliciosa"
Sentimiento: Positivo

Ahora clasifica:
Texto: "El producto llegó a tiempo pero la calidad es inferior a lo esperado"
Sentimiento:
```

### 3.3 Few-Shot Prompting

Se proporcionan múltiples ejemplos (típicamente 2-5) para establecer un patrón claro.

```
# Few-shot
Clasifica los tickets de soporte según su tipo.

Ejemplos:
Ticket: "La aplicación se cierra cuando intento exportar a PDF"
Tipo: Bug

Ticket: "Seria genial poder integrar con Google Calendar"
Tipo: Feature Request

Ticket: "¿Cómo puedo cambiar mi contraseña?"
Tipo: Question

Ticket: "Llevo 3 días esperando respuesta y nadie me ayuda"
Tipo: Complaint

Ahora clasifica:
Ticket: "El botón de guardar no funciona en Safari"
Tipo:
```

#### Principios para Buenos Ejemplos Few-Shot

1. **Representatividad**: Cubrir casos tipicos de cada categoría
2. **Diversidad**: Variar la estructura y longitud de los ejemplos
3. **Claridad**: Ejemplos sin ambigüedad
4. **Balance**: Número similar de ejemplos por categoría
5. **Orden**: A veces el orden importa (recency bias)

#### ¿Cuántos Ejemplos?

| Ejemplos | Uso recomendado |
|----------|-----------------|
| 1-2 | Tareas simples, formato básico |
| 3-5 | Clasificación, extracción |
| 5-10 | Tareas complejas, múltiples categorías |
| 10+ | Raramente necesario, considerar fine-tuning |

### 3.4 Desarrollo Iterativo de Prompts

El Prompt Engineering es un proceso iterativo. Raramente el primer prompt es el óptimo.

#### Proceso de Desarrollo Iterativo

```
┌─────────────────────────────────────────────────────────────┐
│                    CICLO ITERATIVO                          │
│                                                             │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│   │  Prompt  │───►│ Probar   │───►│ Evaluar  │              │
│   │  Inicial │    │ con LLM  │    │ Output   │              │
│   └──────────┘    └──────────┘    └────┬─────┘              │
│        ▲                               │                    │
│        │         ┌──────────┐          │                    │
│        └─────────│ Refinar  │◄─────────┘                    │
│                  │ Prompt   │                               │
│                  └──────────┘                               │
└─────────────────────────────────────────────────────────────┘
```

#### Ejemplo de Iteración

**Iteración 1 - Prompt básico:**
```
Analiza este código y encuentra errores.
```
*Problema: Respuesta vaga, sin estructura*

**Iteración 2 - Añadiendo formato:**
```
Analiza este código Python y encuentra errores.
Para cada error indica: línea, tipo de error, solución.
```
*Mejora: Más estructurado, pero falta profundidad*

**Iteración 3 - Añadiendo rol y criterios:**
```
Actúa como un ingeniero senior de Python realizando code review.

Analiza el siguiente código e identifica:
1. Errores que causarían fallos en ejecución
2. Malas prácticas (code smells)
3. Problemas de rendimiento
4. Mejoras de legibilidad

Para cada issue encontrado:
- Severidad: Crítica/Alta/Media/Baja
- Línea: número
- Problema: descripción
- Solución: código corregido

Código:
[código aquí]
```
*Resultado: Respuesta completa, estructurada, actionable*

### 3.5 Patrones Comunes de Prompts

#### Patrón: Extracción de Información

```
Extrae la siguiente información del texto:
- Nombre completo
- Email
- Telefono
- Empresa

Si algún campo no esta presente, indica "No especificado".

Texto:
"""
[texto aquí]
"""

Responde en formato JSON.
```

#### Patrón: Transformación de Formato

```
Convierte la siguiente tabla CSV a formato Markdown:

'''csv
nombre,edad,ciudad
Ana,28,Madrid
Carlos,35,Barcelona
'''

Genera una tabla Markdown bien formateada.
```

#### Patrón: Generación con Restricciones

```
Genera 5 nombres para una startup de tecnología educativa.

Requisitos:
- Máximo 2 palabras
- Fácil de pronunciar en español e inglés
- Disponible como dominio .com (verifica que suene plausible)
- Evita números y guiones

Formato: Lista numerada con una breve justificación de cada nombre.
```

#### Patrón: Análisis Comparativo

```
Compara las siguientes tecnologías para [caso de uso]:

Tecnología A: [nombre]
Tecnología B: [nombre]

Criterios de comparación:
1. Rendimiento
2. Facilidad de uso
3. Ecosistema y comunidad
4. Coste
5. Curva de aprendizaje

Presenta la comparación en una tabla y concluye con una recomendación.
```

---

## Bloque 4: Anti-patrones y Errores Comunes

### 4.1 Anti-patrones a Evitar

#### Anti-patrón 1: Prompts Demasiado Vagos

```
❌ MAL:
"Ayudame con mi proyecto"

✓ BIEN:
"Necesito crear una función Python que valide direcciones de email.
Debe retornar True si el email es válido, False en caso contrario.
Incluye validación de formato y dominios comunes."
```

#### Anti-patrón 2: Sobrecarga de Instrucciones

```
❌ MAL:
"Escribe un artículo sobre IA que sea informativo pero también
entretenido y que tenga exactamente 500 palabras y que incluya
3 ejemplos y que use un tono profesional pero accesible y que
mencione las últimas tendencias y que sea original y que..."

✓ BIEN:
"Escribe un artículo sobre IA para un blog de tecnología.

Requisitos:
- Longitud: ~500 palabras
- Tono: Profesional pero accesible
- Incluir: 3 ejemplos prácticos
- Audiencia: Profesionales no técnicos"
```

#### Anti-patrón 3: Instrucciones Contradictorias

```
❌ MAL:
"Explica en detalle pero sé breve"
"Dame una respuesta completa en una oración"

✓ BIEN:
"Proporciona una explicación concisa (2-3 párrafos) cubriendo
los puntos esenciales"
```

#### Anti-patrón 4: Asumir Contexto

```
❌ MAL:
"Continúa con lo que estábamos haciendo"
"Arregla el error del que hablamos"

✓ BIEN:
"En el código de la función calcular_total() que te mostré,
corrige el error de división por cero en la línea 15"
```

#### Anti-patrón 5: No Especificar Formato

```
❌ MAL:
"Dame información sobre Python"

✓ BIEN:
"Lista las 5 características principales de Python.
Formato: Lista numerada, una oración por característica."
```

### 4.2 Manejo de Respuestas Inesperadas

Cuando el modelo no responde como esperas:

| Problema | Posible Solución |
|----------|------------------|
| Respuesta muy larga | Añadir límite explícito de longitud |
| Respuesta muy corta | Pedir elaboración o ejemplos |
| Formato incorrecto | Añadir ejemplo del formato deseado |
| Información inventada | Pedir citar fuentes o indicar incertidumbre |
| Off-topic | Reformular tarea más claramente |
| Negarse a responder | Reformular para evitar triggers de seguridad |

### 4.3 Sesgos y Limitaciones

#### Sesgos a Considerar

- **Recency bias**: Información reciente del prompt puede tener más peso
- **Verbosity bias**: Respuestas largas pueden parecer más completas
- **Sycophancy**: Tendencia a estar de acuerdo con el usuario
- **Position bias**: En listas, primeros/últimos items pueden favorecer

#### Mitigación

```
# Contra recency bias
Asegurar que información importante está al inicio Y al final

# Contra verbosity bias
"Evalúa la calidad, no la longitud. Una respuesta concisa correcta
es mejor que una larga incorrecta."

# Contra sycophancy
"Proporciona una evaluación objetiva. Incluye críticas si las hay."
```

---

## Bloque 5: Práctica Guiada

### 5.1 Ejercicio en Clase: Mejora Iterativa

Partiendo del siguiente prompt básico, mejoradlo iterativamente:

```
Prompt inicial:
"Escribe código para ordenar una lista"
```

**Tareas:**
1. Añadir especificidad (lenguaje, tipo de ordenación)
2. Añadir formato de respuesta
3. Añadir restricciones
4. Añadir rol si es apropiado

<details>
<summary><strong>Ver solución</strong></summary>

**Iteración 1 — Añadir especificidad:**
```
Escribe una función en Python que ordene una lista de números enteros
de menor a mayor usando el algoritmo de ordenación por inserción
(insertion sort).
```

**Iteración 2 — Añadir formato de respuesta:**
```
Escribe una función en Python que ordene una lista de números enteros
de menor a mayor usando el algoritmo de ordenación por inserción.

Estructura tu respuesta así:
1. Código de la función con type hints
2. Ejemplo de uso con input y output esperado
3. Complejidad temporal y espacial (una línea cada una)
```

**Iteración 3 — Añadir restricciones:**
```
Escribe una función en Python que ordene una lista de números enteros
de menor a mayor usando el algoritmo de ordenación por inserción.

Restricciones:
- No uses funciones built-in de ordenación (sorted, .sort())
- La función debe modificar la lista in-place y retornarla
- Incluye validación para lista vacía
- Usa type hints

Estructura tu respuesta así:
1. Código de la función
2. Ejemplo de uso con input y output esperado
3. Complejidad temporal y espacial (una línea cada una)
```

**Iteración 4 — Añadir rol (versión final):**
```
Actúa como un profesor de algoritmos explicando a estudiantes
de segundo año de ingeniería.

Escribe una función en Python que ordene una lista de números enteros
de menor a mayor usando el algoritmo de ordenación por inserción.

Restricciones:
- No uses funciones built-in de ordenación (sorted, .sort())
- La función debe modificar la lista in-place y retornarla
- Incluye validación para lista vacía
- Usa type hints
- Añade comentarios explicando cada paso del algoritmo

Estructura tu respuesta así:
1. Breve explicación de cómo funciona insertion sort (2-3 líneas)
2. Código de la función comentado
3. Ejemplo de uso con input y output esperado
4. Complejidad temporal y espacial (una línea cada una)
```

**Observación:** Cada iteración añade más precisión sin sobrecargar el prompt. El resultado final es un prompt que produce una respuesta educativa, estructurada y completa.

</details>

### 5.2 Ejercicio: Diseño de Prompt para Caso Real

Diseña un prompt para:
> "Un sistema que recibe descripciones de bugs de usuarios y genera
> tickets estructurados para el equipo de desarrollo"

Incluir:
- Rol
- Contexto del sistema
- Formato de salida (campos del ticket)
- Manejo de información faltante

<details>
<summary><strong>Ver solución</strong></summary>

```
Eres un ingeniero de QA senior con experiencia en gestión de incidencias
y triaje de bugs. Tu tarea es convertir descripciones informales de
usuarios en tickets estructurados para el equipo de desarrollo.

<contexto>
Trabajas para una empresa SaaS de gestión de proyectos. Los usuarios
reportan problemas a través de un chat de soporte y sus descripciones
suelen ser informales, incompletas y a veces confusas. Tu trabajo es
interpretar el reporte y generar un ticket claro y accionable.
</contexto>

<formato_salida>
Genera el ticket con EXACTAMENTE estos campos en formato Markdown:

## [TÍTULO BREVE Y DESCRIPTIVO]

- **ID**: BUG-[número aleatorio de 4 dígitos]
- **Severidad**: Crítica | Alta | Media | Baja
- **Componente**: [módulo o área de la aplicación afectada]
- **Entorno**: [navegador, SO, dispositivo si se menciona]
- **Descripción**: [resumen claro del problema en 2-3 oraciones]
- **Pasos para reproducir**:
  1. [paso 1]
  2. [paso 2]
  ...
- **Comportamiento esperado**: [qué debería ocurrir]
- **Comportamiento actual**: [qué ocurre realmente]
- **Información adicional**: [capturas, logs, frecuencia, etc.]
</formato_salida>

<reglas>
- Si el usuario no proporciona información para un campo, indica
  "[Pendiente - solicitar al usuario]" en lugar de inventar datos.
- Infiere la severidad según el impacto:
  · Crítica: la aplicación no funciona o hay pérdida de datos
  · Alta: funcionalidad principal bloqueada, sin workaround
  · Media: funcionalidad afectada pero con workaround disponible
  · Baja: problema cosmético o de menor impacto
- Si la descripción es ambigua, añade una sección "**Preguntas de
  clarificación**" al final con las preguntas necesarias.
- No inventes pasos de reproducción que el usuario no haya mencionado.
</reglas>

Descripción del usuario:
"""
[AQUÍ SE INSERTA LA DESCRIPCIÓN DEL USUARIO]
"""
```

**Ejemplo de uso** — Si el usuario escribe:

> "Oigan, cuando intento exportar mi informe a PDF se queda cargando
> para siempre y nunca termina. Uso Chrome. Ya intenté varias veces
> y nada."

El prompt generaría un ticket estructurado con severidad Alta, componente "Exportación/Informes", pasos de reproducción inferidos del relato, y marcaría como `[Pendiente - solicitar al usuario]` campos como el SO o la versión del navegador.

</details>

---

## Resumen de la Sesión

### Conceptos Clave

1. **Prompt Engineering** = diseño sistemático de instrucciones para LLMs
2. **Componentes del prompt**: Rol, Contexto, Tarea, Formato, Restricciones, Ejemplos
3. **Técnicas básicas**: Zero-shot, One-shot, Few-shot
4. **Desarrollo iterativo**: Probar → Evaluar → Refinar → Repetir
5. **Delimitadores**: Separan secciones para mayor claridad
6. **Anti-patrones**: Vaguedad, sobrecarga, contradicciones

### Checklist de un Buen Prompt

- [ ] ¿Es claro qué debe hacer el modelo?
- [ ] ¿Tiene el contexto necesario?
- [ ] ¿Está especificado el formato de salida?
- [ ] ¿Hay restricciones claras?
- [ ] ¿Se evitan ambigüedades?
- [ ] ¿Los delimitadores separan las secciones?

---

## Conexión con la Sesión 2

En la próxima sesión profundizaremos en:
- **Chain of Thought (CoT)**: Razonamiento paso a paso
- **System Prompts**: Instrucciones persistentes
- **Chat Completion API**: Estructura de mensajes
- **Diseño de asistentes especializados**
- **Comparativa entre modelos**

---

## Actividades

### Ejercicios de esta Sesión
Completa los ejercicios prácticos disponibles en [ejercicios.md](./ejercicios.md):

1. **Anatomía de un Prompt** - Identificar componentes en prompts existentes
2. **Zero-shot vs Few-shot** - Comparar resultados con diferentes técnicas
3. **Desarrollo Iterativo** - Mejorar un prompt paso a paso
4. **Diseño de Prompts** - Crear prompts para casos de uso específicos
5. **Identificación de Anti-patrones** - Detectar y corregir prompts problemáticos


---

## Referencias

- OpenAI. (2023). GPT Best Practices
- Anthropic. (2024). Prompt Engineering Guide
- Google. (2024). Introduction to Prompt Design
- White, J. et al. (2023). A Prompt Pattern Catalog to Enhance Prompt Engineering with ChatGPT
- Wei, J. et al. (2022). Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
