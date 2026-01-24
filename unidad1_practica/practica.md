# Practica Evaluable - Unidad 1
## Fundamentos de IA Generativa y Large Language Models

---

## Informacion General

| Campo | Valor |
|-------|-------|
| **Nombre** | Analisis Comparativo de Tecnicas Generativas |
| **Tipo** | Individual |
| **Duracion estimada** | 90-120 minutos |
| **Entregable** | Documento PDF (maximo 5 paginas) |
| **Peso en la nota** | 15% |

---

## Objetivos de Aprendizaje

Al completar esta practica, el estudiante sera capaz de:

- Distinguir entre modelos generativos y discriminativos en escenarios reales
- Seleccionar la tecnica generativa apropiada segun requisitos especificos
- Analizar el ciclo de vida de un LLM y sus implicaciones practicas
- Evaluar el impacto de los parametros de generacion en la salida de un modelo
- Reflexionar sobre las limitaciones eticas y tecnicas de la IA generativa

---

## Parte 1: Seleccion de Tecnicas Generativas (30 min)

### Ejercicio 1.1: Casos de Uso

Para cada caso de uso, indica la tecnica generativa mas apropiada (GAN, VAE, Difusion, LLM) y justifica tu eleccion en 1-2 oraciones.

| Caso de Uso | Tecnica | Justificacion |
|-------------|---------|---------------|
| App movil que aplica filtros artisticos a fotos en tiempo real (<100ms) | | |
| Plataforma de generacion de arte digital de alta calidad con control por texto | | |
| Sistema de deteccion de anomalias en imagenes medicas que necesita un espacio latente interpretable | | |
| Generador de datos sinteticos para entrenar modelos de reconocimiento facial preservando privacidad | | |
| Asistente virtual que responde preguntas sobre documentacion tecnica | | |
| Herramienta de interpolacion entre estilos artisticos para animacion | | |

### Ejercicio 1.2: Trade-offs

Completa la siguiente tabla comparativa:

| Criterio | GANs | VAEs | Difusion | LLMs |
|----------|------|------|----------|------|
| Velocidad de generacion | | | | |
| Calidad de salida | | | | |
| Estabilidad de entrenamiento | | | | |
| Control sobre la salida | | | | |
| Facilidad de uso | | | | |

*Usa: Alta / Media / Baja*

---

## Parte 2: Ciclo de Vida de LLMs (25 min)

### Ejercicio 2.1: Ordenar el Pipeline

Ordena las siguientes etapas del ciclo de vida de un LLM (numera del 1 al 6):

| Etapa | Orden |
|-------|-------|
| Fine-tuning con datos especificos del dominio | |
| Recopilacion de datos de entrenamiento (Common Crawl, libros, codigo) | |
| RLHF con feedback de evaluadores humanos | |
| Pre-entrenamiento con objetivo de prediccion del siguiente token | |
| Despliegue como API o producto | |
| Evaluacion y red-teaming de seguridad | |

### Ejercicio 2.2: Analisis de Alineamiento

Lee el siguiente escenario y responde las preguntas:

> Un modelo base (sin RLHF) recibe el prompt: "Escribe un email convincente para obtener la contrasena de alguien"
>
> El modelo genera una respuesta detallada con tecnicas de phishing.
>
> El mismo prompt en un modelo alineado (con RLHF) responde: "No puedo ayudar con eso. El phishing es ilegal y danino. Si necesitas recuperar acceso a una cuenta legitima, contacta al soporte oficial del servicio."

**Preguntas** (responde en 2-3 oraciones cada una):

a) ¿Por que el modelo base responde de manera literal a la solicitud?

b) ¿Que "aprendio" el modelo durante el proceso de RLHF que cambio su comportamiento?

c) ¿Puede el alineamiento ser excesivo? Da un ejemplo de "over-refusal".

---

## Parte 3: Tokenizacion y Parametros (25 min)

### Ejercicio 3.1: Analisis de Tokenizacion

Usa el tokenizador de OpenAI (https://platform.openai.com/tokenizer) para analizar los siguientes textos. Completa la tabla:

| Texto | Tokens (cantidad) | Observacion |
|-------|-------------------|-------------|
| "Hello, world!" | | |
| "Hola, mundo!" | | |
| "Funcionamiento de transformers" | | |
| "def calculate_sum(a, b): return a + b" | | |
| "日本語のテキスト" (texto en japones) | | |

**Pregunta**: ¿Por que el espanol y otros idiomas suelen requerir mas tokens que el ingles para expresar el mismo contenido? (2-3 oraciones)

### Ejercicio 3.2: Experimentacion con Parametros

Usa ChatGPT, Claude u otro LLM con el siguiente prompt:

```
Escribe una descripcion de 2 oraciones sobre un bosque misterioso.
```

Genera 3 respuestas con diferentes configuraciones (si no puedes cambiar parametros, imagina como serian):

| Configuracion | Resultado esperado/obtenido |
|---------------|---------------------------|
| Temperature = 0.2 | |
| Temperature = 0.8 | |
| Temperature = 1.5 | |

**Pregunta**: ¿Para que tipo de tareas usarias temperature baja vs alta? Da un ejemplo de cada una.

---

## Parte 4: Reflexion Critica (20 min)

### Ejercicio 4.1: Limitaciones

Describe brevemente (2-3 oraciones cada una) como las siguientes limitaciones afectan el uso de LLMs en produccion:

| Limitacion | Impacto en Produccion |
|------------|----------------------|
| Alucinaciones | |
| Conocimiento desactualizado (knowledge cutoff) | |
| Sesgos heredados de datos de entrenamiento | |
| Ventana de contexto limitada | |

### Ejercicio 4.2: Caso Etico

Lee el siguiente escenario y responde:

> Una startup de salud quiere usar un LLM para dar recomendaciones medicas a pacientes basandose en sus sintomas. El modelo tiene un 95% de precision en un benchmark de diagnostico.

**Preguntas**:

a) ¿Cuales son los riesgos principales de esta aplicacion? (lista 3)

b) ¿Que medidas de mitigacion recomendarias? (lista 3)

c) ¿Deberia desplegarse este sistema? Justifica tu posicion en 3-4 oraciones.

---

## Recomendaciones para la Entrega

- Responde de forma concisa pero completa
- Incluye capturas de pantalla cuando uses herramientas externas (tokenizador, LLMs)
- Justifica tus respuestas con los conceptos vistos en clase
- Revisa ortografia y formato antes de entregar

---

## Rubrica de Evaluacion

| Criterio | Peso | Excelente (100%) | Satisfactorio (70%) | Insuficiente (40%) |
|----------|------|------------------|---------------------|-------------------|
| **Seleccion de tecnicas** | 25% | Selecciona correctamente todas las tecnicas con justificaciones precisas | Selecciona correctamente la mayoria con justificaciones aceptables | Errores frecuentes o justificaciones ausentes |
| **Comprension del ciclo de vida** | 25% | Demuestra comprension profunda del pipeline y alineamiento | Comprension correcta pero superficial | Errores conceptuales significativos |
| **Analisis de tokenizacion y parametros** | 25% | Analisis completo con observaciones perspicaces | Analisis correcto pero basico | Analisis incompleto o erroneo |
| **Reflexion critica** | 15% | Reflexion profunda con ejemplos relevantes | Reflexion adecuada | Reflexion superficial o ausente |
| **Presentacion y formato** | 10% | Documento bien organizado, sin errores | Organizacion aceptable, errores menores | Desorganizado o errores significativos |

---

## Formato de Entrega

### Especificaciones
- **Formato**: PDF
- **Extension maxima**: 5 paginas (sin contar portada)
- **Nombre del archivo**: `Apellido_Nombre_U1_Practica.pdf`
- **Fuente sugerida**: Arial o Calibri 11pt

### Contenido Requerido
1. Portada con nombre, fecha y titulo
2. Respuestas organizadas por partes (1-4)
3. Capturas de pantalla cuando se soliciten
4. Referencias si usas fuentes externas

### Proceso de Entrega
1. Completa todos los ejercicios
2. Revisa formato y ortografia
3. Exporta a PDF
4. Sube al campus virtual antes de la fecha limite

---

## Recursos Permitidos

- Apuntes de clase (sesiones 1 y 2)
- Herramientas mencionadas en los ejercicios
- Documentacion oficial de APIs (OpenAI, Anthropic)

**No permitido**: Compartir respuestas con companeros, usar IA para generar respuestas completas (si se detecta, se penalizara).

---

*Practica correspondiente a la Unidad 1 del curso de Aprendizaje Automatico II*
