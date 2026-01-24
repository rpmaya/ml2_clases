# Unidad 1 - Sesion 1: Fundamentos de IA Generativa
## Aprendizaje Automatico II

---

## Informacion de la Sesion

| | |
|---|---|
| **Duracion** | 4 horas |
| **Modalidad** | Teoria + Practica integrada |
| **Materiales** | Laptop con navegador, cuenta gratuita en plataformas de IA |

---

## Objetivos de Aprendizaje

Al finalizar esta sesion, seras capaz de:

- [ ] Comprender las diferencias entre modelos generativos y discriminativos
- [ ] Explicar el funcionamiento basico de GANs, VAEs y Modelos de Difusion
- [ ] Experimentar con herramientas reales de generacion de imagenes
- [ ] Distinguir entre modelos autorregresivos y no autorregresivos
- [ ] Seleccionar la tecnica apropiada segun el caso de uso

---

## Preparacion Previa

Antes de comenzar, asegurate de tener acceso a:

| Herramienta | URL | Requiere Cuenta |
|-------------|-----|-----------------|
| This Person Does Not Exist | https://thispersondoesnotexist.com | No |
| Stable Diffusion Demo | https://huggingface.co/spaces/stabilityai/stable-diffusion | No |
| MNIST VAE Demo | https://transcranial.github.io/keras-js/#/mnist-vae | No |
| GAN Lab | https://poloclub.github.io/ganlab/ | No |

---

# BLOQUE 1: Introduccion a la IA Generativa
## Duracion: 45 minutos (30 teoria + 15 practica)

---

## 1.1 ¿Que es la IA Generativa?

La **Inteligencia Artificial Generativa** representa un cambio de paradigma en Machine Learning. Mientras los modelos tradicionales se centran en clasificar o predecir, la IA generativa tiene un objetivo mas ambicioso: **crear contenido nuevo**.

### Modelos Discriminativos vs Generativos

| Aspecto | Discriminativos | Generativos |
|---------|-----------------|-------------|
| **Objetivo matematico** | P(Y\|X) | P(X) o P(X,Y) |
| **Pregunta que responde** | "¿A que clase pertenece?" | "¿Como se genero este dato?" |
| **Puede generar datos nuevos?** | No | Si |
| **Ejemplos clasicos** | Regresion logistica, SVM | Naive Bayes, GMM |
| **Ejemplos Deep Learning** | CNN clasificacion | GANs, VAEs, Diffusion |

### Analogia Practica

Imagina un **detective**:
- **Discriminativo**: "Este documento es falso porque tiene estas caracteristicas..."
- **Generativo**: "Asi es como luciria un documento autentico" (y puede crear uno)

### Ejemplo Concreto

Un **clasificador de spam** (discriminativo):
- Puede decir si un correo es spam
- NO puede redactar un correo

Un **modelo generativo** entrenado con correos:
- Puede detectar patrones de spam
- Puede generar ejemplos sinteticos para entrenamiento
- Puede redactar respuestas automaticas
- Puede completar borradores incompletos

---

## 1.2 Contexto Historico

### Evolucion de los Modelos Generativos

```
1960s-80s          1980s-90s          2014            2017            2020+
    |                  |                |               |               |
   HMM               GMM              GANs         Transformers      Difusion
(Markov)          (Gaussian)       (Goodfellow)    (Attention)    (DALL-E, SD)
    |                  |                |               |               |
  Audio            Clusters          Imagenes         Texto          Multimodal
```

### Hitos Clave

| Año | Evento | Impacto |
|-----|--------|---------|
| 2014 | GANs (Goodfellow) | Primera generacion de imagenes realistas |
| 2017 | Transformers | Arquitectura base de LLMs |
| 2020 | GPT-3 | Capacidades emergentes en texto |
| 2022 | DALL-E 2, Stable Diffusion | Democratizacion de text-to-image |
| 2022 | ChatGPT | Adopcion masiva global |
| 2024-25 | GPT-4, Claude, Gemini | Competencia multimodal |

---

## 1.3 Impacto en la Industria del Software

### Transformacion del Desarrollo

| Fase | Herramientas IA | Impacto |
|------|-----------------|---------|
| Requisitos | Generacion de historias de usuario | Acelera documentacion |
| Implementacion | GitHub Copilot, Cursor | +30-55% productividad |
| Testing | Generacion de casos de prueba | Mayor cobertura |
| Mantenimiento | Documentacion de legacy | Reduce deuda tecnica |

### Consideraciones Eticas

| Aspecto | Pregunta Clave |
|---------|----------------|
| Propiedad intelectual | ¿Quien es autor del codigo generado? |
| Sesgos | ¿Los modelos heredan sesgos de sus datos? |
| Alucinaciones | ¿Como manejar informacion falsa generada con confianza? |
| Impacto laboral | ¿Transformacion o desplazamiento? |

---

## PRACTICA 1.1: Primera Exploracion de IA Generativa
### Duracion: 15 minutos | Individual

### Objetivo
Desarrollar intuicion sobre las capacidades de modelos generativos antes de estudiar su teoria.

### Parte A: Generacion de Rostros con GANs (5 min)

1. Visita [thispersondoesnotexist.com](https://thispersondoesnotexist.com)
2. Recarga la pagina 5-10 veces
3. Observa y anota:

| Pregunta | Tus Observaciones |
|----------|-------------------|
| ¿Los rostros parecen reales? | |
| ¿Detectas algun artefacto o error? | |
| ¿Que partes fallan mas? (orejas, dientes, fondos, manos) | |

### Parte B: Generacion con Difusion (10 min)

1. Accede a [Stable Diffusion Demo](https://huggingface.co/spaces/stabilityai/stable-diffusion)
2. Genera imagenes con estos prompts:

```
Prompt 1: "A cat sitting on a laptop, photorealistic"
Prompt 2: "A futuristic city at sunset, cyberpunk style"
Prompt 3: "A medieval knight riding a horse, oil painting"
```

3. Completa la tabla:

| Prompt | Tiempo generacion | Calidad (1-10) | Sigue instrucciones? |
|--------|-------------------|----------------|----------------------|
| Gato en laptop | | | |
| Ciudad futurista | | | |
| Caballero medieval | | | |

### Reflexion (compartir en clase)
- ¿Que modelo te parecio mas impresionante?
- ¿Notaste diferencias de velocidad?
- ¿Que limitaciones observaste?

---

# BLOQUE 2: GANs - Generative Adversarial Networks
## Duracion: 50 minutos (35 teoria + 15 practica)

---

## 2.1 La Idea Revolucionaria

Las GANs fueron propuestas por **Ian Goodfellow en 2014**. La leyenda dice que tuvo la idea en un bar discutiendo con amigos.

El concepto es elegante: **dos redes neuronales compitiendo en un juego**.

### Analogia del Falsificador y el Detective

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
- **Salida**: Imagen sintetica
- **Objetivo**: Engañar al discriminador

**Discriminador (D)**:
- **Entrada**: Imagenes (reales o generadas)
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
# Pseudocodigo simplificado
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
    # G aprende: hacer que D diga 1 para sus imagenes
```

### Funcion Objetivo

```
min_G max_D V(D,G) = E[log D(x)] + E[log(1 - D(G(z)))]
```

**Intuicion**:
- D quiere **maximizar**: dar 1 a reales, 0 a falsas
- G quiere **minimizar**: que D de 1 a sus falsas

### Convergencia Ideal

Cuando el entrenamiento funciona bien:
- El Generador produce imagenes indistinguibles de las reales
- El Discriminador tiene precision del 50% (no puede hacer mejor que adivinar)

---

## 2.4 Problemas Comunes

| Problema | Que Ocurre | Consecuencia |
|----------|------------|--------------|
| **Mode Collapse** | G produce solo unas pocas variantes | Poca diversidad |
| **Vanishing Gradients** | D es muy bueno muy rapido | G no recibe señal para mejorar |
| **Inestabilidad** | Oscilaciones en el entrenamiento | No converge |

### Mode Collapse Explicado

```
Lo esperado:                    Mode Collapse:

Genera: gatos, perros,          Genera: solo gatos negros
        pajaros, peces...       (encontro un "truco" que engaña a D)
```

---

## 2.5 Variantes de GANs

| Variante | Innovacion | Aplicacion |
|----------|------------|------------|
| **DCGAN** | Convoluciones profundas | Estabilizo el entrenamiento |
| **StyleGAN** | Control de estilo por capas | Rostros hiperrealistas |
| **CycleGAN** | Sin necesidad de pares | Caballo ↔ Cebra |
| **Pix2Pix** | Con pares de entrenamiento | Boceto → Imagen |

---

## 2.6 Aplicaciones Reales

| Aplicacion | Descripcion | Ejemplo Real |
|------------|-------------|--------------|
| Rostros | Personas que no existen | thispersondoesnotexist.com |
| Transferencia de estilo | Foto → Pintura | Prisma, DeepArt |
| Super-resolucion | Aumentar calidad | ESRGAN en videojuegos |
| Inpainting | Rellenar huecos | Adobe Firefly |
| Datos sinteticos | Entrenamiento con privacidad | Imagenes medicas |

---

## PRACTICA 2.1: Analisis de Arquitectura GAN
### Duracion: 15 minutos | Parejas

### Objetivo
Comprender la dinamica adversarial analizando el flujo de informacion.

### Parte A: Analisis del Diagrama (5 min)

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

1. ¿Cual es el input del Generador? ¿Por que ruido aleatorio?

   _Tu respuesta:_

2. ¿Por que el Discriminador recibe AMBOS tipos de imagenes?

   _Tu respuesta:_

3. Si el Discriminador se vuelve perfecto muy rapido, ¿que le pasa al Generador?

   _Tu respuesta:_

### Parte B: Visualizacion Interactiva (10 min)

1. Visita [GAN Lab](https://poloclub.github.io/ganlab/)
2. Observa el entrenamiento en tiempo real
3. Experimenta con diferentes configuraciones

**Completa**:

| Observacion | Lo que vi |
|-------------|-----------|
| ¿Como evolucionan los puntos generados? | |
| ¿Hubo algun momento de mode collapse? | |
| ¿Cuantas iteraciones hasta convergencia? | |

### Discusion en Clase
- ¿Que estrategias podrian evitar que D sea "demasiado bueno"?
- ¿Por que es dificil encontrar el equilibrio?

---

# DESCANSO: 15 minutos

---

# BLOQUE 3: VAEs - Variational Autoencoders
## Duracion: 45 minutos (30 teoria + 15 practica)

---

## 3.1 Del Autoencoder Clasico al VAE

### Autoencoder Clasico

```
Input x ──> [Encoder] ──> z (codigo) ──> [Decoder] ──> x' (reconstruccion)
```

- **Encoder**: Comprime la entrada
- **Decoder**: Reconstruye desde la compresion
- **Objetivo**: Minimizar diferencia entre x y x'

**Problema**: El espacio z no tiene estructura. Si muestreamos puntos aleatorios, el decoder produce basura.

---

## 3.2 La Innovacion del VAE

En lugar de mapear a un **punto fijo**, el encoder produce **parametros de una distribucion**:

```
Input x ──> [Encoder] ──> μ, σ ──> z ~ N(μ, σ²) ──> [Decoder] ──> x'
```

### Diferencia Visual

```
AUTOENCODER CLASICO:              VAE:

     Input                         Input
       |                             |
       v                             v
   [Encoder]                    [Encoder]
       |                             |
       v                             v
    Punto z                     μ y σ (distribucion)
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

## 3.3 Funcion de Perdida

```
L = Reconstruccion + Regularizacion KL

L = ||x - x'||² + KL(q(z|x) || N(0,1))
```

### Dos Componentes

| Termino | Que Hace | Intuicion |
|---------|----------|-----------|
| **Reconstruccion** | Mide diferencia input/output | "Que se parezca" |
| **KL Divergence** | Fuerza q(z\|x) hacia N(0,1) | "Espacio organizado" |

### ¿Por que KL hacia N(0,1)?

Si todas las distribuciones se parecen a una normal estandar:
- Podemos **muestrear de N(0,1)** para generar
- El espacio latente es **continuo y navegable**
- Puntos cercanos producen outputs similares

---

## 3.4 Propiedades del Espacio Latente

| Propiedad | Descripcion | Utilidad |
|-----------|-------------|----------|
| **Continuidad** | Puntos cercanos → datos similares | Interpolacion suave |
| **Completitud** | Todo punto produce dato realista | Generacion por muestreo |
| **Estructura semantica** | Dimensiones interpretables | Control de atributos |

### Interpolacion en el Espacio Latente

```python
# Si tenemos dos puntos en el espacio latente
z1 = encoder(imagen_gato)
z2 = encoder(imagen_perro)

# Podemos "caminar" entre ellos
for t in [0, 0.25, 0.5, 0.75, 1.0]:
    z_intermedio = z1 * (1-t) + z2 * t
    imagen_intermedia = decoder(z_intermedio)
    # Vemos transicion suave gato → perro
```

---

## 3.5 Comparativa GANs vs VAEs

| Aspecto | GANs | VAEs |
|---------|------|------|
| **Calidad de imagen** | Superior, nitidas | Mas borrosas |
| **Estabilidad** | Dificil de entrenar | Estable |
| **Espacio latente** | No estructurado | Estructurado, navegable |
| **Diversidad** | Propenso a mode collapse | Mejor cobertura |
| **Velocidad generacion** | Muy rapida | Muy rapida |

### ¿Por que VAEs dan imagenes borrosas?

La funcion de perdida MSE "promedia" sobre posibles outputs, suavizando detalles de alta frecuencia.

---

## PRACTICA 3.1: Explorando el Espacio Latente de VAEs
### Duracion: 15 minutos | Individual

### Objetivo
Visualizar y entender las propiedades del espacio latente estructurado.

### Parte A: Exploracion Visual (10 min)

1. Accede al [MNIST VAE Demo](https://transcranial.github.io/keras-js/#/mnist-vae)
2. Explora el espacio latente 2D moviendo el cursor

**Observa y responde**:

| Pregunta | Tu Observacion |
|----------|----------------|
| ¿Los digitos similares estan cerca? (ej: 3 y 8) | |
| ¿Hay zonas "vacias" sin significado? | |
| ¿Que pasa en las fronteras entre clusters? | |
| ¿Puedes encontrar un "4" que parece "9"? | |

### Parte B: Interpolacion Mental (5 min)

Imagina dos puntos en el espacio latente:
- Punto A: genera un "3"
- Punto B: genera un "8"

**Dibuja o describe**: ¿Que digitos esperarias ver en 5 puntos intermedios entre A y B?

```
Punto A (3) ──> ??? ──> ??? ──> ??? ──> ??? ──> ??? ──> Punto B (8)
```

**Verifica** moviendo el cursor en la demo.

### Reflexion
- ¿Por que la interpolacion produce digitos coherentes y no ruido?
- ¿Como podria usarse esto en aplicaciones reales? (pista: edicion de imagenes, animacion)

---

# BLOQUE 4: Modelos de Difusion
## Duracion: 45 minutos (35 teoria + 10 reflexion)

---

## 4.1 La Idea Contraintuitiva

La intuicion es sorprendente: **aprender a revertir la destruccion gradual de informacion**.

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

La red aprende a **predecir el ruido** que se añadio:

```python
# Pseudocodigo de entrenamiento
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

## 4.3 Generacion

```python
# Partir de ruido puro
x = sample_pure_noise()

# Iterar T pasos de "limpieza"
for t in range(T, 0, -1):
    ruido_predicho = modelo(x, t)
    x = quitar_ruido(x, ruido_predicho, t)

return x  # Imagen generada
```

**Nota**: Por eso es lento - necesita muchos pasos (tipicamente 20-1000).

---

## 4.4 Ventajas sobre GANs

| Aspecto | GANs | Difusion |
|---------|------|----------|
| **Estabilidad** | Dificil, inestable | Muy estable |
| **Diversidad** | Mode collapse posible | Excelente cobertura |
| **Calidad** | Alta | Muy alta (estado del arte) |
| **Control** | Limitado | Excelente (guiado por texto) |
| **Velocidad** | Muy rapida | Lenta (multiples pasos) |

---

## 4.5 Difusion en Espacio Latente (Stable Diffusion)

### El Problema
Operar en espacio de pixeles es muy costoso (512×512 = 262,144 valores).

### La Solucion
Comprimir primero con un VAE, hacer difusion en espacio pequeño:

```
Imagen (512×512) ──> [VAE Encoder] ──> Latente (64×64) ──> [Difusion] ──> Latente ──> [VAE Decoder] ──> Imagen
```

**Beneficios**:
- 64× menos computo
- Misma calidad
- Posible en GPUs consumer

---

## 4.6 Modelos Destacados

| Modelo | Organizacion | Caracteristica |
|--------|--------------|----------------|
| DALL-E 2/3 | OpenAI | Text-to-image alta calidad |
| Stable Diffusion | Stability AI | Open-source, comunidad activa |
| Midjourney | Midjourney | Estetica artistica |
| Imagen | Google | Alta fidelidad |
| Sora | OpenAI | Text-to-video |

---

## REFLEXION 4.1: Conectando Conceptos
### Duracion: 10 minutos | Grupos de 3

### Discusion

En grupos, discutan las siguientes preguntas:

1. **Difusion vs GANs**:
   - Ya experimentaste con ambos al inicio de la clase
   - ¿Notaste diferencia en tiempo de generacion?
   - ¿Cual produjo imagenes de mayor calidad?

2. **Trade-off velocidad/calidad**:
   - Para una app de filtros en tiempo real, ¿cual usarias?
   - Para generar arte de alta calidad, ¿cual usarias?

3. **Conexion con VAEs**:
   - Stable Diffusion usa un VAE internamente. ¿Para que?
   - ¿Que ventaja da esto sobre difusion "pura"?

**Preparen una respuesta de 1 minuto para compartir.**

---

# BLOQUE 5: Autorregresivo vs No Autorregresivo
## Duracion: 30 minutos (teoria)

---

## 5.1 Modelos Autorregresivos

Generan **secuencialmente**, un elemento a la vez:

```
P(x₁, x₂, ..., xₙ) = P(x₁) · P(x₂|x₁) · P(x₃|x₁,x₂) · ... · P(xₙ|x₁,...,xₙ₋₁)
```

### Ejemplo: Como Genera un LLM

```
Prompt: "El gato esta"

Paso 1: P("sentado" | "El gato esta") = 0.3 → genera "sentado"
Paso 2: P("en" | "El gato esta sentado") = 0.5 → genera "en"
Paso 3: P("el" | "El gato esta sentado en") = 0.4 → genera "el"
...
```

### Caracteristicas

| Propiedad | Descripcion |
|-----------|-------------|
| Generacion | Token por token, secuencial |
| Atencion | Solo mira hacia atras (causal) |
| Velocidad | Lenta para secuencias largas |
| Coherencia | Alta (cada token depende de todos los anteriores) |

### Ejemplos
**Todos los LLMs principales**: GPT, Claude, LLaMA, Gemini

---

## 5.2 Modelos No Autorregresivos

Generan **todo simultaneamente**:

```
P(x₁, x₂, ..., xₙ) ≈ P(x₁|ctx) · P(x₂|ctx) · ... · P(xₙ|ctx)
```

### Caracteristicas

| Propiedad | Descripcion |
|-----------|-------------|
| Generacion | Todo en paralelo |
| Velocidad | Muy rapida |
| Coherencia | Potencialmente menor |

### Ejemplos
- BERT (para comprension, no generacion)
- Algunos modelos de traduccion
- Modelos de difusion (generan imagen completa por paso)

---

## 5.3 Arquitecturas Transformer

| Tipo | Atencion | Uso | Ejemplos |
|------|----------|-----|----------|
| **Decoder-only** | Causal (masked) | Generacion | GPT, Claude, LLaMA |
| **Encoder-only** | Bidireccional | Comprension | BERT |
| **Encoder-Decoder** | Mixta | Traduccion | T5, BART |

---

## 5.4 Implicaciones Practicas

La naturaleza autorregresiva de los LLMs tiene consecuencias importantes:

| Implicacion | Descripcion |
|-------------|-------------|
| No planifica | Cada palabra se decide localmente |
| Sensible al inicio | Primeros tokens condicionan todo |
| Streaming | Tokens se muestran mientras se generan |
| "Piensa" linealmente | No puede "volver atras" y corregir |

---

# BLOQUE 6: Comparativa y Seleccion de Tecnicas
## Duracion: 20 minutos (10 teoria + 10 practica final)

---

## 6.1 Matriz de Decision

| Criterio | GANs | VAEs | Difusion | LLMs |
|----------|------|------|----------|------|
| **Tipo de dato** | Imagenes | Imagenes | Imagenes, audio, video | Texto, codigo |
| **Calidad** | Alta | Media | Muy alta | Muy alta |
| **Velocidad** | Muy rapida | Muy rapida | Lenta | Media |
| **Estabilidad** | Baja | Alta | Alta | Alta |
| **Control** | Limitado | Bueno | Muy bueno | Excelente |

---

## 6.2 Guia de Seleccion

### ¿Cuando usar cada tecnica?

| Caso de Uso | Tecnica Recomendada | Razon |
|-------------|---------------------|-------|
| Filtros en tiempo real | GANs | Velocidad |
| Deteccion de anomalias | VAEs | Espacio latente estructurado |
| Arte de alta calidad | Difusion | Maxima calidad |
| Generacion de texto | LLMs | Diseñados para lenguaje |
| Interpolacion controlada | VAEs | Navegacion del espacio latente |
| Datos sinteticos | GANs o VAEs | Privacidad + velocidad |

---

## PRACTICA 6.1: Ejercicio Integrador - Comparativa de Tecnicas
### Duracion: 10 minutos | Grupal (3-4 personas)

### Contexto
Eres consultor de IA y debes recomendar tecnologias para estos clientes.

### Casos de Uso

**Caso 1: App de Filtros de Belleza**
- Requisitos: Tiempo real (<100ms), movil, calidad aceptable

**Tu recomendacion**: ________________

**Justificacion** (velocidad, recursos, calidad):

---

**Caso 2: Plataforma de Arte Digital**
- Requisitos: Maxima calidad, control via texto, tiempo no critico

**Tu recomendacion**: ________________

**Justificacion**:

---

**Caso 3: Hospital - Datos Sinteticos de Rayos X**
- Requisitos: Realismo medico, control de patologias, privacidad

**Tu recomendacion**: ________________

**Justificacion**:

---

**Caso 4: Archivo de Biblioteca - Compresion de Imagenes**
- Requisitos: Compresion extrema, reconstruccion fiel, busqueda semantica

**Tu recomendacion**: ________________

**Justificacion**:

---

### Discusion Final (5 min)
- ¿Hubo consenso en las recomendaciones?
- ¿Que criterio fue mas dificil de evaluar?
- ¿Hay casos donde varias tecnicas serian validas?

---

# EVALUACION: Quiz de Conceptos
## Duracion: 10 minutos | Individual

Responde sin consultar material.

### Pregunta 1
¿Cual es la principal diferencia entre un modelo discriminativo y uno generativo?

- [ ] a) Los discriminativos son mas precisos
- [ ] b) Los generativos aprenden P(X,Y), los discriminativos P(Y|X)
- [ ] c) Los generativos solo funcionan con imagenes
- [ ] d) Los discriminativos son mas modernos

### Pregunta 2
En una GAN, ¿que ocurre si el Discriminador se vuelve demasiado bueno muy rapido?

- [ ] a) El entrenamiento se acelera
- [ ] b) El Generador recibe gradientes muy pequeños y deja de aprender
- [ ] c) Las imagenes generadas mejoran inmediatamente
- [ ] d) No tiene ningun efecto

### Pregunta 3
¿Por que los VAEs producen imagenes mas borrosas que las GANs?

- [ ] a) Usan redes mas pequeñas
- [ ] b) La funcion de perdida MSE promedia sobre variaciones
- [ ] c) El espacio latente es demasiado grande
- [ ] d) Solo funcionan con imagenes de baja resolucion

### Pregunta 4
¿Cual es el proposito del termino KL en la perdida del VAE?

- [ ] a) Mejorar la calidad de reconstruccion
- [ ] b) Regularizar el espacio latente para que siga N(0,1)
- [ ] c) Acelerar el entrenamiento
- [ ] d) Reducir el tamaño del modelo

### Pregunta 5
¿Por que los modelos de difusion son mas lentos que las GANs?

- [ ] a) Tienen mas parametros
- [ ] b) Requieren multiples pasos de denoising iterativo
- [ ] c) Usan imagenes de mayor resolucion
- [ ] d) Necesitan GPU mas potentes

---

<details>
<summary><strong>Ver Respuestas</strong></summary>

1. **b)** - Los generativos modelan la distribucion conjunta, los discriminativos la condicional
2. **b)** - Vanishing gradients impiden el aprendizaje del Generador
3. **b)** - El MSE promedia, perdiendo detalles de alta frecuencia
4. **b)** - Fuerza q(z|x) a aproximar N(0,1), estructurando el espacio latente
5. **b)** - Necesitan T pasos para revertir el proceso de ruido (20-1000 tipicamente)

</details>

---

# Resumen de la Sesion

## Las 5 Ideas Fundamentales

| Concepto | Resumen en una linea |
|----------|----------------------|
| **Generativo vs Discriminativo** | Discriminativo clasifica, Generativo crea |
| **GANs** | Dos redes compitiendo: falsificador vs detective |
| **VAEs** | Espacio latente estructurado con regularizacion KL |
| **Difusion** | Aprender a revertir proceso de destruccion por ruido |
| **Autorregresivo** | Genera secuencialmente, token a token |

## Para Recordar

- No hay tecnica "mejor" universal - depende del caso
- GANs para velocidad, Difusion para calidad, VAEs para espacio latente
- El campo evoluciona muy rapido
- Entender fundamentos permite evaluar nuevas tecnologias

---

# Proxima Sesion

## Sesion 2: Large Language Models en Profundidad

- Panorama actual: GPT, Claude, Gemini, LLaMA
- Ciclo de vida: Pre-entrenamiento → RLHF → Producto
- Funcionamiento interno: Tokenizacion, embeddings, context window
- Parametros de generacion

---

# Recursos Adicionales

## Papers Fundamentales
- Goodfellow et al. (2014) - "Generative Adversarial Networks"
- Kingma & Welling (2014) - "Auto-Encoding Variational Bayes"
- Ho et al. (2020) - "Denoising Diffusion Probabilistic Models"
- Vaswani et al. (2017) - "Attention Is All You Need"

## Demos para Seguir Explorando
- [thispersondoesnotexist.com](https://thispersondoesnotexist.com) - StyleGAN
- [Stable Diffusion](https://huggingface.co/spaces/stabilityai/stable-diffusion) - Difusion
- [GAN Lab](https://poloclub.github.io/ganlab/) - Visualizacion GAN
- [MNIST VAE](https://transcranial.github.io/keras-js/#/mnist-vae) - Espacio latente

## Videos Recomendados
- 3Blue1Brown - "But what is a neural network?"
- Computerphile - "Generative Adversarial Networks"
- Two Minute Papers - AI breakthroughs

---

# Ejercicio para Casa (Opcional)

## Investigacion: Modelo Generativo Reciente

Investiga uno de estos modelos y prepara una presentacion de 5 minutos:

1. **DALL-E 3** (OpenAI)
2. **Sora** (OpenAI) - Video
3. **Stable Diffusion 3**
4. **Flux**

### Puntos a Cubrir
- ¿Que tecnica(s) usa?
- ¿Que lo diferencia?
- ¿Cuales son sus limitaciones?
- ¿Esta disponible publicamente?

---

*Documento generado para el curso de Aprendizaje Automatico II*
