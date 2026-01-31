# Práctica Evaluable - Unidad 1
## Fundamentos de IA Generativa y Large Language Models

---

## Información General

| Campo | Valor |
|-------|-------|
| **Nombre** | Análisis Comparativo de Técnicas Generativas |
| **Tipo** | Individual |
| **Duración estimada** | 90-120 minutos |
| **Entregable** | Documento PDF (máximo 5 páginas) |
| **Peso en la nota** | 15% |

---

## Objetivos de Aprendizaje

Al completar esta práctica, el estudiante será capaz de:

- Distinguir entre modelos generativos y discriminativos en escenarios reales
- Seleccionar la técnica generativa apropiada según requisitos específicos
- Analizar el ciclo de vida de un LLM y sus implicaciones prácticas
- Evaluar el impacto de los parámetros de generación en la salida de un modelo
- Reflexionar sobre las limitaciones éticas y técnicas de la IA generativa

---

## Parte 1: Selección de Técnicas Generativas

### Ejercicio 1.1: Casos de Uso

Para cada caso de uso, indica la técnica generativa más apropiada (GAN, VAE, Difusión, LLM) y justifica tu elección en 1-2 oraciones.

| Caso de Uso | Técnica | Justificación |
|-------------|---------|---------------|
| App móvil que aplica filtros artísticos a fotos en tiempo real (<100ms) | | |
| Plataforma de generación de arte digital de alta calidad con control por texto | | |
| Sistema de detección de anomalías en imágenes médicas que necesita un espacio latente interpretable | | |
| Generador de datos sintéticos para entrenar modelos de reconocimiento facial preservando privacidad | | |
| Asistente virtual que responde preguntas sobre documentación técnica | | |
| Herramienta de interpolación entre estilos artísticos para animación | | |

### Ejercicio 1.2: Trade-offs

Completa la siguiente tabla comparativa:

| Criterio | GANs | VAEs | Difusión | LLMs |
|----------|------|------|----------|------|
| Velocidad de generación | | | | |
| Calidad de salida | | | | |
| Estabilidad de entrenamiento | | | | |
| Control sobre la salida | | | | |
| Facilidad de uso | | | | |

*Usa: Alta / Media / Baja*

---

## Parte 2: Ciclo de Vida de LLMs

### Ejercicio 2.1: Ordenar el Pipeline

Ordena las siguientes etapas del ciclo de vida de un LLM (numera del 1 al 6):

| Etapa | Orden |
|-------|-------|
| Fine-tuning con datos específicos del dominio | |
| Recopilación de datos de entrenamiento (Common Crawl, libros, código) | |
| RLHF con feedback de evaluadores humanos | |
| Pre-entrenamiento con objetivo de predicción del siguiente token | |
| Despliegue como API o producto | |
| Evaluación y red-teaming de seguridad | |

### Ejercicio 2.2: Análisis de Alineamiento

Lee el siguiente escenario y responde las preguntas:

> Un modelo base (sin RLHF) recibe el prompt: "Escribe un email convincente para obtener la contraseña de alguien"
>
> El modelo genera una respuesta detallada con técnicas de phishing.
>
> El mismo prompt en un modelo alineado (con RLHF) responde: "No puedo ayudar con eso. El phishing es ilegal y dañino. Si necesitas recuperar acceso a una cuenta legítima, contacta al soporte oficial del servicio."

**Preguntas** (responde en 2-3 oraciones cada una):

a) ¿Por qué el modelo base responde de manera literal a la solicitud?

b) ¿Qué "aprendió" el modelo durante el proceso de RLHF que cambió su comportamiento?

c) ¿Puede el alineamiento ser excesivo? Da un ejemplo de "over-refusal".

---

## Parte 3: Tokenización y Parámetros

### Ejercicio 3.1: Análisis de Tokenización

Usa el tokenizador de OpenAI (https://platform.openai.com/tokenizer) para analizar los siguientes textos. Completa la tabla:

| Texto | Tokens (cantidad) | Observación |
|-------|-------------------|-------------|
| "Hello, world!" | | |
| "Hola, mundo!" | | |
| "Funcionamiento de transformers" | | |
| "def calculate_sum(a, b): return a + b" | | |
| "日本語のテキスト" (texto en japonés) | | |

**Pregunta**: ¿Por qué el español y otros idiomas suelen requerir más tokens que el inglés para expresar el mismo contenido? (2-3 oraciones)

### Ejercicio 3.2: Experimentación con Parámetros

Usa ChatGPT, Claude u otro LLM con el siguiente prompt:

```
Escribe una descripción de 2 oraciones sobre un bosque misterioso.
```

Genera 3 respuestas con diferentes configuraciones (si no puedes cambiar parámetros, imagina cómo serían):

| Configuración | Resultado esperado/obtenido |
|---------------|---------------------------|
| Temperature = 0.2 | |
| Temperature = 0.8 | |
| Temperature = 1.5 | |

**Pregunta**: ¿Para qué tipo de tareas usarías temperature baja vs alta? Da un ejemplo de cada una.

---

## Parte 4: Reflexión Crítica

### Ejercicio 4.1: Limitaciones

Describe brevemente (2-3 oraciones cada una) cómo las siguientes limitaciones afectan el uso de LLMs en producción:

| Limitación | Impacto en Producción |
|------------|----------------------|
| Alucinaciones | |
| Conocimiento desactualizado (knowledge cutoff) | |
| Sesgos heredados de datos de entrenamiento | |
| Ventana de contexto limitada | |

### Ejercicio 4.2: Caso Ético

Lee el siguiente escenario y responde:

> Una startup de salud quiere usar un LLM para dar recomendaciones médicas a pacientes basándose en sus síntomas. El modelo tiene un 95% de precisión en un benchmark de diagnóstico.

**Preguntas**:

a) ¿Cuáles son los riesgos principales de esta aplicación? (lista 3)

b) ¿Qué medidas de mitigación recomendarías? (lista 3)

c) ¿Debería desplegarse este sistema? Justifica tu posición en 3-4 oraciones.

---

## Recomendaciones para la Entrega

- Responde de forma concisa pero completa
- Incluye capturas de pantalla cuando uses herramientas externas (tokenizador, LLMs)
- Justifica tus respuestas con los conceptos vistos en clase
- Revisa ortografía y formato antes de entregar

---

## Rúbrica de Evaluación

| Criterio | Peso | Excelente (100%) | Satisfactorio (70%) | Insuficiente (40%) |
|----------|------|------------------|---------------------|-------------------|
| **Selección de técnicas** | 25% | Selecciona correctamente todas las técnicas con justificaciones precisas | Selecciona correctamente la mayoría con justificaciones aceptables | Errores frecuentes o justificaciones ausentes |
| **Comprensión del ciclo de vida** | 25% | Demuestra comprensión profunda del pipeline y alineamiento | Comprensión correcta pero superficial | Errores conceptuales significativos |
| **Análisis de tokenización y parámetros** | 25% | Análisis completo con observaciones perspicaces | Análisis correcto pero básico | Análisis incompleto o erróneo |
| **Reflexión crítica** | 15% | Reflexión profunda con ejemplos relevantes | Reflexión adecuada | Reflexión superficial o ausente |
| **Presentación y formato** | 10% | Documento bien organizado, sin errores | Organización aceptable, errores menores | Desorganizado o errores significativos |

---

## Formato de Entrega

### Especificaciones
- **Formato**: PDF
- **Extensión máxima**: 5 páginas (sin contar portada)
- **Nombre del archivo**: `Apellido_Nombre_U1_Practica.pdf`
- **Fuente sugerida**: Arial o Calibri 11pt

### Contenido Requerido
1. Portada con nombre, fecha y título
2. Respuestas organizadas por partes (1-4)
3. Capturas de pantalla cuando se soliciten
4. Referencias si usas fuentes externas

### Proceso de Entrega
1. Completa todos los ejercicios
2. Revisa formato y ortografía
3. Exporta a PDF
4. Sube al campus virtual antes de la fecha límite

---

## Recursos Permitidos

- Apuntes de clase (sesiones 1 y 2)
- Herramientas mencionadas en los ejercicios
- Documentación oficial de APIs (OpenAI, Anthropic)

**No permitido**: Compartir respuestas con compañeros, usar IA para generar respuestas completas (si se detecta, se penalizará).

---

*Práctica correspondiente a la Unidad 1 del curso de Aprendizaje Automático II*
