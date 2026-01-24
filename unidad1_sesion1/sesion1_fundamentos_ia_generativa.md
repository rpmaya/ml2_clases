# Unidad 1 - Sesión 1: Fundamentos de IA Generativa
## Aprendizaje Automático II

---

## Objetivos de Aprendizaje

Al finalizar esta sesión, serás capaz de:

- [ ] Comprender las diferencias entre modelos generativos y discriminativos
- [ ] Explicar el funcionamiento básico de GANs, VAEs y Modelos de Difusión
- [ ] Experimentar con herramientas reales de generación de imágenes
- [ ] Distinguir entre modelos autorregresivos y no autorregresivos
- [ ] Seleccionar la técnica apropiada según el caso de uso

---

## Preparación Previa

Antes de comenzar, asegúrate de tener acceso a:

| Herramienta | URL | Requiere Cuenta |
|-------------|-----|-----------------|
| This Person Does Not Exist | https://thispersondoesnotexist.com | No |
| Stable Diffusion Demo | https://huggingface.co/spaces/stabilityai/stable-diffusion-3-medium | No |
| MNIST VAE Demo | https://transcranial.github.io/keras-js/#/mnist-vae | No |
| GAN Lab | https://poloclub.github.io/ganlab/ | No |

---

# BLOQUE 1: Introducción a la IA Generativa

---

## 1.1 ¿Qué es la IA Generativa?

La **Inteligencia Artificial Generativa** representa un cambio de paradigma en Machine Learning. Mientras los modelos tradicionales se centran en clasificar o predecir, la IA generativa tiene un objetivo más ambicioso: **crear contenido nuevo**.

### Modelos Discriminativos vs Generativos

| Aspecto | Discriminativos | Generativos |
|---------|-----------------|-------------|
| **Objetivo matemático** | P(Y\|X) | P(X) o P(X,Y) |
| **Pregunta que responde** | "¿A qué clase pertenece?" | "¿Cómo se generó este dato?" |
| **¿Puede generar datos nuevos?** | No | Sí |
| **Ejemplos clásicos** | Regresión logística, SVM | Naive Bayes, GMM |
| **Ejemplos Deep Learning** | CNN clasificación | GANs, VAEs, Diffusion |

### Analogía Práctica

Imagina un **detective**:
- **Discriminativo**: "Este documento es falso porque tiene estas características..."
- **Generativo**: "Así es como se vería un documento auténtico" (y puede crear uno)

### Ejemplo Concreto

Un **clasificador de spam** (discriminativo):
- Puede decir si un correo es spam
- NO puede redactar un correo

Un **modelo generativo** entrenado con correos:
- Puede detectar patrones de spam
- Puede generar ejemplos sintéticos para entrenamiento
- Puede redactar respuestas automáticas
- Puede completar borradores incompletos

---

## 1.2 Contexto Histórico

### Evolución de los Modelos Generativos

```
1960s-80s          1980s-90s          2014            2017            2020+
    |                  |                |               |               |
   HMM               GMM              GANs         Transformers      Difusión
(Markov)          (Gaussian)       (Goodfellow)    (Attention)    (DALL-E, SD)
    |                  |                |               |               |
  Audio            Clusters          Imágenes         Texto          Multimodal
```

### Hitos Clave

| Año | Evento | Impacto |
|-----|--------|---------|
| 2014 | GANs (Goodfellow) | Primera generación de imágenes realistas |
| 2017 | Transformers | Arquitectura base de LLMs |
| 2020 | GPT-3 | Capacidades emergentes en texto |
| 2022 | DALL-E 2, Stable Diffusion | Democratización de text-to-image |
| 2022 | ChatGPT | Adopción masiva global |
| 2024-25 | GPT-4, Claude, Gemini | Competencia multimodal |

---

## 1.3 Impacto en la Industria del Software

### Transformación del Desarrollo

| Fase | Herramientas IA | Impacto |
|------|-----------------|---------|
| Requisitos | Generación de historias de usuario | Acelera documentación |
| Implementación | GitHub Copilot, Cursor | +30-55% productividad |
| Testing | Generación de casos de prueba | Mayor cobertura |
| Mantenimiento | Documentación de legacy | Reduce deuda técnica |

### Consideraciones Éticas

| Aspecto | Pregunta Clave |
|---------|----------------|
| Propiedad intelectual | ¿Quién es autor del código generado? |
| Sesgos | ¿Los modelos heredan sesgos de sus datos? |
| Alucinaciones | ¿Cómo manejar información falsa generada con confianza? |
| Impacto laboral | ¿Transformación o desplazamiento? |

---

## PRÁCTICA 1.1: Primera Exploración de IA Generativa
### Individual

### Objetivo
Desarrollar intuición sobre las capacidades de modelos generativos antes de estudiar su teoría.

### Parte A: Generación de Rostros con GANs (5 min)

1. Visita [thispersondoesnotexist.com](https://thispersondoesnotexist.com)
2. Recarga la página 5-10 veces
3. Observa y anota:

| Pregunta | Tus Observaciones |
|----------|-------------------|
| ¿Los rostros parecen reales? | |
| ¿Detectas algún artefacto o error? | |
| ¿Qué partes fallan más? (orejas, dientes, fondos, manos) | |

### Parte B: Generación con Difusión (10 min)

1. Accede a [Stable Diffusion Demo](https://huggingface.co/spaces/stabilityai/stable-diffusion-3-medium)
2. Genera imágenes con estos prompts:

```
Prompt 1: "A cat sitting on a laptop, photorealistic"
Prompt 2: "A futuristic city at sunset, cyberpunk style"
Prompt 3: "A medieval knight riding a horse, oil painting"
```

3. Completa la tabla:

| Prompt | Tiempo generación | Calidad (1-10) | ¿Sigue instrucciones? |
|--------|-------------------|----------------|----------------------|
| Gato en laptop | | | |
| Ciudad futurista | | | |
| Caballero medieval | | | |

### Reflexión (compartir en clase)
- ¿Qué modelo te pareció más impresionante?
- ¿Notaste diferencias de velocidad?
- ¿Qué limitaciones observaste?

---

# BLOQUE 2: GANs - Generative Adversarial Networks

---

## 2.1 La Idea Revolucionaria

Las GANs fueron propuestas por **Ian Goodfellow en 2014**. La leyenda dice que tuvo la idea en un bar discutiendo con amigos.

El concepto es elegante: **dos redes neuronales compitiendo en un juego**.

### Analogía del Falsificador y el Detective

```
FALSIFICADOR (Generador)         vs         DETECTIVE (Discriminador)
        |                                            |
Crea billetes falsos                        Detecta billetes falsos
        |                                            |
Mejora cuando lo atrapan                    Mejora cuando lo engañan
        |                                            |
        └──────────── COMPETENCIA ───────────────────┘
                            |
                   Ambos mejoran hasta que
                 los billetes son indistinguibles
```

---

## 2.2 Arquitectura

### Componentes

**Generador (G)**:
- **Entrada**: Vector de ruido aleatorio z ~ N(0, I)
- **Salida**: Imagen sintética
- **Objetivo**: Engañar al discriminador

**Discriminador (D)**:
- **Entrada**: Imágenes (reales o generadas)
- **Salida**: Probabilidad de ser real (0 a 1)
- **Objetivo**: Distinguir reales de falsas

### Diagrama de Flujo

```
      z (ruido aleatorio)
             |
             v
      +--------------+
      |  GENERADOR   |
      +--------------+
             |
             v
       Imagen Falsa ─────────┐
                             |
                             v
                     +---------------+
   Imagen Real ────> | DISCRIMINADOR | ───> Real (1) / Falso (0)
                     +---------------+
```

---

## 2.3 Entrenamiento

### Ciclo de Entrenamiento

```python
# Pseudocódigo simplificado
for epoca in range(num_epocas):

    # FASE 1: Entrenar Discriminador
    imagenes_reales = obtener_batch_real()
    z = generar_ruido()
    imagenes_falsas = Generador(z)

    loss_D = entrenar_discriminador(imagenes_reales, imagenes_falsas)
    # D aprende: reales → 1, falsas → 0

    # FASE 2: Entrenar Generador (D congelado)
    z = generar_ruido()
    imagenes_falsas = Generador(z)

    loss_G = entrenar_generador(imagenes_falsas)
    # G aprende: hacer que D diga 1 para sus imágenes
```

### Función Objetivo

```
min_G max_D V(D,G) = E[log D(x)] + E[log(1 - D(G(z)))]
```

**Intuición**:
- D quiere **maximizar**: dar 1 a reales, 0 a falsas
- G quiere **minimizar**: que D dé 1 a sus falsas

### Convergencia Ideal

Cuando el entrenamiento funciona bien:
- El Generador produce imágenes indistinguibles de las reales
- El Discriminador tiene precisión del 50% (no puede hacer mejor que adivinar)

---

## 2.4 Problemas Comunes

| Problema | Qué Ocurre | Consecuencia |
|----------|------------|--------------|
| **Mode Collapse** | G produce solo unas pocas variantes | Poca diversidad |
| **Vanishing Gradients** | D es muy bueno muy rápido | G no recibe señal para mejorar |
| **Inestabilidad** | Oscilaciones en el entrenamiento | No converge |

### Mode Collapse Explicado

```
Lo esperado:                    Mode Collapse:

Genera: gatos, perros,          Genera: solo gatos negros
        pájaros, peces...       (encontró un "truco" que engaña a D)
```

---

## 2.5 Variantes de GANs

| Variante | Innovación | Aplicación |
|----------|------------|------------|
| **DCGAN** | Convoluciones profundas | Estabilizó el entrenamiento |
| **StyleGAN** | Control de estilo por capas | Rostros hiperrealistas |
| **CycleGAN** | Sin necesidad de pares | Caballo ↔ Cebra |
| **Pix2Pix** | Con pares de entrenamiento | Boceto → Imagen |

---

## 2.6 Aplicaciones Reales

| Aplicación | Descripción | Ejemplo Real |
|------------|-------------|--------------|
| Rostros | Personas que no existen | thispersondoesnotexist.com |
| Transferencia de estilo | Foto → Pintura | Prisma, DeepArt |
| Super-resolución | Aumentar calidad | ESRGAN en videojuegos |
| Inpainting | Rellenar huecos | Adobe Firefly |
| Datos sintéticos | Entrenamiento con privacidad | Imágenes médicas |

---

## PRÁCTICA 2.1: Análisis de Arquitectura GAN
### Parejas

### Objetivo
Comprender la dinámica adversarial analizando el flujo de información.

### Parte A: Análisis del Diagrama (5 min)

Observa el siguiente diagrama y responde:

```
                ┌─────────────────────────────────────────┐
                │           ENTRENAMIENTO GAN            │
                └─────────────────────────────────────────┘

    ┌──────────┐         ┌──────────────┐
    │  Ruido   │────────>│  GENERADOR   │────────┐
    │  z~N(0,1)│         │     G(z)     │        │
    └──────────┘         └──────────────┘        │
                                                 │
                                                 v
                                        ┌──────────────┐
    ┌──────────┐                        │   Imagen     │
    │ Dataset  │                        │   Falsa      │
    │  Real    │──────────┐             └──────┬───────┘
    └──────────┘          │                    │
                          v                    v
                    ┌──────────────────────────────┐
                    │       DISCRIMINADOR          │
                    │          D(x)                │
                    └──────────────┬───────────────┘
                                   │
                                   v
                            ┌──────────────┐
                            │ Real: 1      │
                            │ Falso: 0     │
                            └──────────────┘
```

**Preguntas**:

1. ¿Cuál es el input del Generador? ¿Por qué ruido aleatorio?

   _Tu respuesta:_

2. ¿Por qué el Discriminador recibe AMBOS tipos de imágenes?

   _Tu respuesta:_

3. Si el Discriminador se vuelve perfecto muy rápido, ¿qué le pasa al Generador?

   _Tu respuesta:_

### Parte B: Visualización Interactiva (10 min)

1. Visita [GAN Lab](https://poloclub.github.io/ganlab/)
2. Observa el entrenamiento en tiempo real
3. Experimenta con diferentes configuraciones

**Completa**:

| Observación | Lo que vi |
|-------------|-----------|
| ¿Cómo evolucionan los puntos generados? | |
| ¿Hubo algún momento de mode collapse? | |
| ¿Cuántas iteraciones hasta convergencia? | |

### Discusión en Clase
- ¿Qué estrategias podrían evitar que D sea "demasiado bueno"?
- ¿Por qué es difícil encontrar el equilibrio?

---

# DESCANSO: 15 minutos

---

# BLOQUE 3: VAEs - Variational Autoencoders

---

## 3.1 Del Autoencoder Clásico al VAE

### Autoencoder Clásico

```
Input x ──> [Encoder] ──> z (código) ──> [Decoder] ──> x' (reconstrucción)
```

- **Encoder**: Comprime la entrada
- **Decoder**: Reconstruye desde la compresión
- **Objetivo**: Minimizar diferencia entre x y x'

**Problema**: El espacio z no tiene estructura. Si muestreamos puntos aleatorios, el decoder produce basura.

---

## 3.2 La Innovación del VAE

En lugar de mapear a un **punto fijo**, el encoder produce **parámetros de una distribución**:

```
Input x ──> [Encoder] ──> μ, σ ──> z ~ N(μ, σ²) ──> [Decoder] ──> x'
```

### Diferencia Visual

```
AUTOENCODER CLÁSICO:              VAE:

     Input                         Input
       |                             |
       v                             v
   [Encoder]                    [Encoder]
       |                             |
       v                             v
    Punto z                     μ y σ (distribución)
       |                             |
       |                             v
       |                      Muestrear z ~ N(μ,σ)
       |                             |
       v                             v
   [Decoder]                    [Decoder]
       |                             |
       v                             v
    Output                        Output
```

---

## 3.3 Función de Pérdida

```
L = Reconstrucción + Regularización KL

L = ||x - x'||² + KL(q(z|x) || N(0,1))
```

### Dos Componentes

| Término | Qué Hace | Intuición |
|---------|----------|-----------|
| **Reconstrucción** | Mide diferencia input/output | "Que se parezca" |
| **KL Divergence** | Fuerza q(z\|x) hacia N(0,1) | "Espacio organizado" |

### ¿Por qué KL hacia N(0,1)?

Si todas las distribuciones se parecen a una normal estándar:
- Podemos **muestrear de N(0,1)** para generar
- El espacio latente es **continuo y navegable**
- Puntos cercanos producen outputs similares

---

## 3.4 Propiedades del Espacio Latente

| Propiedad | Descripción | Utilidad |
|-----------|-------------|----------|
| **Continuidad** | Puntos cercanos → datos similares | Interpolación suave |
| **Completitud** | Todo punto produce dato realista | Generación por muestreo |
| **Estructura semántica** | Dimensiones interpretables | Control de atributos |

### Interpolación en el Espacio Latente

```python
# Si tenemos dos puntos en el espacio latente
z1 = encoder(imagen_gato)
z2 = encoder(imagen_perro)

# Podemos "caminar" entre ellos
for t in [0, 0.25, 0.5, 0.75, 1.0]:
    z_intermedio = z1 * (1-t) + z2 * t
    imagen_intermedia = decoder(z_intermedio)
    # Vemos transición suave gato → perro
```

---

## 3.5 Comparativa GANs vs VAEs

| Aspecto | GANs | VAEs |
|---------|------|------|
| **Calidad de imagen** | Superior, nítidas | Más borrosas |
| **Estabilidad** | Difícil de entrenar | Estable |
| **Espacio latente** | No estructurado | Estructurado, navegable |
| **Diversidad** | Propenso a mode collapse | Mejor cobertura |
| **Velocidad generación** | Muy rápida | Muy rápida |

### ¿Por qué VAEs dan imágenes borrosas?

La función de pérdida MSE "promedia" sobre posibles outputs, suavizando detalles de alta frecuencia.

---

## PRÁCTICA 3.1: Explorando el Espacio Latente de VAEs
### Individual

### Objetivo
Visualizar y entender las propiedades del espacio latente estructurado.

### Parte A: Exploración Visual (10 min)

1. Accede al [MNIST VAE Demo](https://transcranial.github.io/keras-js/#/mnist-vae)
2. Explora el espacio latente 2D moviendo el cursor

**Observa y responde**:

| Pregunta | Tu Observación |
|----------|----------------|
| ¿Los dígitos similares están cerca? (ej: 3 y 8) | |
| ¿Hay zonas "vacías" sin significado? | |
| ¿Qué pasa en las fronteras entre clusters? | |
| ¿Puedes encontrar un "4" que parece "9"? | |

### Parte B: Interpolación Mental (5 min)

Imagina dos puntos en el espacio latente:
- Punto A: genera un "3"
- Punto B: genera un "8"

**Dibuja o describe**: ¿Qué dígitos esperarías ver en 5 puntos intermedios entre A y B?

```
Punto A (3) ──> ??? ──> ??? ──> ??? ──> ??? ──> ??? ──> Punto B (8)
```

**Verifica** moviendo el cursor en la demo.

### Reflexión
- ¿Por qué la interpolación produce dígitos coherentes y no ruido?
- ¿Cómo podría usarse esto en aplicaciones reales? (pista: edición de imágenes, animación)

---

# BLOQUE 4: Modelos de Difusión

---

## 4.1 La Idea Contraintuitiva

La intuición es sorprendente: **aprender a revertir la destrucción gradual de información**.

### El Proceso

1. Tomar una imagen clara
2. Añadir ruido progresivamente hasta tener ruido puro
3. **Entrenar una red para revertir cada paso**
4. Para generar: partir de ruido y aplicar el proceso inverso

```
PROCESO FORWARD (destruir - NO se aprende):
Imagen Clara ──[+ruido]──> ... ──[+ruido]──> Ruido Puro
     x₀                                         xₜ

PROCESO REVERSE (reconstruir - SE APRENDE):
Ruido Puro ──[-ruido]──> ... ──[-ruido]──> Imagen Clara
     xₜ                                         x₀
```

---

## 4.2 Entrenamiento

### Objetivo Simple

La red aprende a **predecir el ruido** que se añadió:

```python
# Pseudocódigo de entrenamiento
for imagen in dataset:
    t = random_step()           # Paso aleatorio (1 a 1000)
    ruido = sample_noise()       # Ruido gaussiano
    imagen_ruidosa = add_noise(imagen, ruido, t)

    ruido_predicho = modelo(imagen_ruidosa, t)

    loss = MSE(ruido, ruido_predicho)
    loss.backward()
```

**Elegante**: Cada paso es independiente, entrenamiento estable.

---

## 4.3 Generación

```python
# Partir de ruido puro
x = sample_pure_noise()

# Iterar T pasos de "limpieza"
for t in range(T, 0, -1):
    ruido_predicho = modelo(x, t)
    x = quitar_ruido(x, ruido_predicho, t)

return x  # Imagen generada
```

**Nota**: Por eso es lento - necesita muchos pasos (típicamente 20-1000).

---

## 4.4 Ventajas sobre GANs

| Aspecto | GANs | Difusión |
|---------|------|----------|
| **Estabilidad** | Difícil, inestable | Muy estable |
| **Diversidad** | Mode collapse posible | Excelente cobertura |
| **Calidad** | Alta | Muy alta (estado del arte) |
| **Control** | Limitado | Excelente (guiado por texto) |
| **Velocidad** | Muy rápida | Lenta (múltiples pasos) |

---

## 4.5 Difusión en Espacio Latente (Stable Diffusion)

### El Problema
Operar en espacio de píxeles es muy costoso (512×512 = 262,144 valores).

### La Solución
Comprimir primero con un VAE, hacer difusión en espacio pequeño:

```
Imagen (512×512) ──> [VAE Encoder] ──> Latente (64×64) ──> [Difusión] ──> Latente ──> [VAE Decoder] ──> Imagen
```

**Beneficios**:
- 64× menos cómputo
- Misma calidad
- Posible en GPUs consumer

---

## 4.6 Modelos Destacados

| Modelo | Organización | Característica |
|--------|--------------|----------------|
| DALL-E 2/3 | OpenAI | Text-to-image alta calidad |
| Stable Diffusion | Stability AI | Open-source, comunidad activa |
| Midjourney | Midjourney | Estética artística |
| Imagen | Google | Alta fidelidad |
| Sora | OpenAI | Text-to-video |

---

## REFLEXIÓN 4.1: Conectando Conceptos
### Grupos de 3

### Discusión

En grupos, discutan las siguientes preguntas:

1. **Difusión vs GANs**:
   - Ya experimentaste con ambos al inicio de la clase
   - ¿Notaste diferencia en tiempo de generación?
   - ¿Cuál produjo imágenes de mayor calidad?

2. **Trade-off velocidad/calidad**:
   - Para una app de filtros en tiempo real, ¿cuál usarías?
   - Para generar arte de alta calidad, ¿cuál usarías?

3. **Conexión con VAEs**:
   - Stable Diffusion usa un VAE internamente. ¿Para qué?
   - ¿Qué ventaja da esto sobre difusión "pura"?

**Preparen una respuesta de 1 minuto para compartir.**

---

# BLOQUE 5: Autorregresivo vs No Autorregresivo

---

## 5.1 Modelos Autorregresivos

Generan **secuencialmente**, un elemento a la vez:

```
P(x₁, x₂, ..., xₙ) = P(x₁) · P(x₂|x₁) · P(x₃|x₁,x₂) · ... · P(xₙ|x₁,...,xₙ₋₁)
```

### Ejemplo: Cómo Genera un LLM

```
Prompt: "El gato está"

Paso 1: P("sentado" | "El gato está") = 0.3 → genera "sentado"
Paso 2: P("en" | "El gato está sentado") = 0.5 → genera "en"
Paso 3: P("el" | "El gato está sentado en") = 0.4 → genera "el"
...
```

### Características

| Propiedad | Descripción |
|-----------|-------------|
| Generación | Token por token, secuencial |
| Atención | Solo mira hacia atrás (causal) |
| Velocidad | Lenta para secuencias largas |
| Coherencia | Alta (cada token depende de todos los anteriores) |

### Ejemplos
**Todos los LLMs principales**: GPT, Claude, LLaMA, Gemini

---

## 5.2 Modelos No Autorregresivos

Generan **todo simultáneamente**:

```
P(x₁, x₂, ..., xₙ) ≈ P(x₁|ctx) · P(x₂|ctx) · ... · P(xₙ|ctx)
```

### Características

| Propiedad | Descripción |
|-----------|-------------|
| Generación | Todo en paralelo |
| Velocidad | Muy rápida |
| Coherencia | Potencialmente menor |

### Ejemplos
- BERT (para comprensión, no generación)
- Algunos modelos de traducción
- Modelos de difusión (generan imagen completa por paso)

---

## 5.3 Arquitecturas Transformer

| Tipo | Atención | Uso | Ejemplos |
|------|----------|-----|----------|
| **Decoder-only** | Causal (masked) | Generación | GPT, Claude, LLaMA |
| **Encoder-only** | Bidireccional | Comprensión | BERT |
| **Encoder-Decoder** | Mixta | Traducción | T5, BART |

---

## 5.4 Implicaciones Prácticas

La naturaleza autorregresiva de los LLMs tiene consecuencias importantes:

| Implicación | Descripción |
|-------------|-------------|
| No planifica | Cada palabra se decide localmente |
| Sensible al inicio | Primeros tokens condicionan todo |
| Streaming | Tokens se muestran mientras se generan |
| "Piensa" linealmente | No puede "volver atrás" y corregir |

---

# BLOQUE 6: Comparativa y Selección de Técnicas

---

## 6.1 Matriz de Decisión

| Criterio | GANs | VAEs | Difusión | LLMs |
|----------|------|------|----------|------|
| **Tipo de dato** | Imágenes | Imágenes | Imágenes, audio, video | Texto, código |
| **Calidad** | Alta | Media | Muy alta | Muy alta |
| **Velocidad** | Muy rápida | Muy rápida | Lenta | Media |
| **Estabilidad** | Baja | Alta | Alta | Alta |
| **Control** | Limitado | Bueno | Muy bueno | Excelente |

---

## 6.2 Guía de Selección

### ¿Cuándo usar cada técnica?

| Caso de Uso | Técnica Recomendada | Razón |
|-------------|---------------------|-------|
| Filtros en tiempo real | GANs | Velocidad |
| Detección de anomalías | VAEs | Espacio latente estructurado |
| Arte de alta calidad | Difusión | Máxima calidad |
| Generación de texto | LLMs | Diseñados para lenguaje |
| Interpolación controlada | VAEs | Navegación del espacio latente |
| Datos sintéticos | GANs o VAEs | Privacidad + velocidad |

---

## PRÁCTICA 6.1: Ejercicio Integrador - Comparativa de Técnicas
### Grupal (3-4 personas)

### Contexto
Eres consultor de IA y debes recomendar tecnologías para estos clientes.

### Casos de Uso

**Caso 1: App de Filtros de Belleza**
- Requisitos: Tiempo real (<100ms), móvil, calidad aceptable

**Tu recomendación**: ________________

**Justificación** (velocidad, recursos, calidad):

---

**Caso 2: Plataforma de Arte Digital**
- Requisitos: Máxima calidad, control vía texto, tiempo no crítico

**Tu recomendación**: ________________

**Justificación**:

---

**Caso 3: Hospital - Datos Sintéticos de Rayos X**
- Requisitos: Realismo médico, control de patologías, privacidad

**Tu recomendación**: ________________

**Justificación**:

---

**Caso 4: Archivo de Biblioteca - Compresión de Imágenes**
- Requisitos: Compresión extrema, reconstrucción fiel, búsqueda semántica

**Tu recomendación**: ________________

**Justificación**:

---

### Discusión Final (5 min)
- ¿Hubo consenso en las recomendaciones?
- ¿Qué criterio fue más difícil de evaluar?
- ¿Hay casos donde varias técnicas serían válidas?

---

# EVALUACIÓN: Quiz de Conceptos
## Individual

Responde sin consultar material.

### Pregunta 1
¿Cuál es la principal diferencia entre un modelo discriminativo y uno generativo?

- [ ] a) Los discriminativos son más precisos
- [ ] b) Los generativos aprenden P(X,Y), los discriminativos P(Y|X)
- [ ] c) Los generativos solo funcionan con imágenes
- [ ] d) Los discriminativos son más modernos

### Pregunta 2
En una GAN, ¿qué ocurre si el Discriminador se vuelve demasiado bueno muy rápido?

- [ ] a) El entrenamiento se acelera
- [ ] b) El Generador recibe gradientes muy pequeños y deja de aprender
- [ ] c) Las imágenes generadas mejoran inmediatamente
- [ ] d) No tiene ningún efecto

### Pregunta 3
¿Por qué los VAEs producen imágenes más borrosas que las GANs?

- [ ] a) Usan redes más pequeñas
- [ ] b) La función de pérdida MSE promedia sobre variaciones
- [ ] c) El espacio latente es demasiado grande
- [ ] d) Solo funcionan con imágenes de baja resolución

### Pregunta 4
¿Cuál es el propósito del término KL en la pérdida del VAE?

- [ ] a) Mejorar la calidad de reconstrucción
- [ ] b) Regularizar el espacio latente para que siga N(0,1)
- [ ] c) Acelerar el entrenamiento
- [ ] d) Reducir el tamaño del modelo

### Pregunta 5
¿Por qué los modelos de difusión son más lentos que las GANs?

- [ ] a) Tienen más parámetros
- [ ] b) Requieren múltiples pasos de denoising iterativo
- [ ] c) Usan imágenes de mayor resolución
- [ ] d) Necesitan GPU más potentes

---

<details>
<summary><strong>Ver Respuestas</strong></summary>

1. **b)** - Los generativos modelan la distribución conjunta, los discriminativos la condicional
2. **b)** - Vanishing gradients impiden el aprendizaje del Generador
3. **b)** - El MSE promedia, perdiendo detalles de alta frecuencia
4. **b)** - Fuerza q(z|x) a aproximar N(0,1), estructurando el espacio latente
5. **b)** - Necesitan T pasos para revertir el proceso de ruido (20-1000 típicamente)

</details>

---

# Resumen de la Sesión

## Las 5 Ideas Fundamentales

| Concepto | Resumen en una línea |
|----------|----------------------|
| **Generativo vs Discriminativo** | Discriminativo clasifica, Generativo crea |
| **GANs** | Dos redes compitiendo: falsificador vs detective |
| **VAEs** | Espacio latente estructurado con regularización KL |
| **Difusión** | Aprender a revertir proceso de destrucción por ruido |
| **Autorregresivo** | Genera secuencialmente, token a token |

## Para Recordar

- No hay técnica "mejor" universal - depende del caso
- GANs para velocidad, Difusión para calidad, VAEs para espacio latente
- El campo evoluciona muy rápido
- Entender fundamentos permite evaluar nuevas tecnologías

---

# Próxima Sesión

## Sesión 2: Large Language Models en Profundidad

- Panorama actual: GPT, Claude, Gemini, LLaMA
- Ciclo de vida: Pre-entrenamiento → RLHF → Producto
- Funcionamiento interno: Tokenización, embeddings, context window
- Parámetros de generación

---

# Recursos Adicionales

## Papers Fundamentales
- Goodfellow et al. (2014) - "Generative Adversarial Networks"
- Kingma & Welling (2014) - "Auto-Encoding Variational Bayes"
- Ho et al. (2020) - "Denoising Diffusion Probabilistic Models"
- Vaswani et al. (2017) - "Attention Is All You Need"

## Demos para Seguir Explorando
- [thispersondoesnotexist.com](https://thispersondoesnotexist.com) - StyleGAN
- [Stable Diffusion](https://huggingface.co/spaces/stabilityai/stable-diffusion) - Difusión
- [GAN Lab](https://poloclub.github.io/ganlab/) - Visualización GAN
- [MNIST VAE](https://transcranial.github.io/keras-js/#/mnist-vae) - Espacio latente

## Videos Recomendados
- 3Blue1Brown - "But what is a neural network?"
- Computerphile - "Generative Adversarial Networks"
- Two Minute Papers - AI breakthroughs

---

# Ejercicio para Casa (Opcional)

## Investigación: Modelo Generativo Reciente

Investiga uno de estos modelos y prepara una presentación de 5 minutos:

1. **DALL-E 3** (OpenAI)
2. **Sora** (OpenAI) - Video
3. **Stable Diffusion 3**
4. **Flux**

### Puntos a Cubrir
- ¿Qué técnica(s) usa?
- ¿Qué lo diferencia?
- ¿Cuáles son sus limitaciones?
- ¿Está disponible públicamente?

---

*Documento generado para el curso de Aprendizaje Automático II*
