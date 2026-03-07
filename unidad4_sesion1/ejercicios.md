# Ejercicios Prácticos - Unidad 4, Sesión 1
## Agentes de IA y Fundamentos de n8n

---

## Ejercicio 1: Análisis del Paradigma PDA

### Metadata
- **Duración estimada**: 20 minutos
- **Tipo**: Análisis
- **Modalidad**: Individual
- **Dificultad**: Básica
- **Prerequisitos**: Lectura de la sección 4.1 sobre agentes de IA y el paradigma Percepción-Decisión-Acción

### Contexto
El paradigma Percepción-Decisión-Acción (PDA) es el marco conceptual fundamental para diseñar agentes de IA efectivos. Antes de construir un agente, necesitamos ser capaces de identificar claramente qué información percibe, cómo toma decisiones y qué acciones ejecuta. Este ejercicio te entrenará para analizar escenarios reales descomponiéndolos en sus componentes PDA, una habilidad esencial para el diseño de automatizaciones inteligentes.

### Objetivo de Aprendizaje
- Aplicar el paradigma PDA a escenarios empresariales reales
- Identificar los tres componentes fundamentales de un agente en diferentes contextos
- Distinguir entre percepción pasiva (espera inputs) y activa (monitoriza fuentes)
- Desarrollar el pensamiento estructurado necesario para diseñar agentes efectivos

### Enunciado

Para cada uno de los siguientes escenarios, identifica y describe los componentes del paradigma PDA. Completa la tabla indicando qué percibe el agente, cómo decide qué hacer y qué acciones concretas ejecuta.

### Escenario A: Agente de Soporte Técnico (eCommerce)

Una tienda online quiere un agente que atienda consultas de clientes sobre el estado de sus pedidos, gestione devoluciones sencillas y escale a un humano los casos complejos.

| Componente | Descripción |
|------------|-------------|
| **Percepción** (¿Qué información recibe?) | __________________ |
| Fuentes de datos | __________________ |
| Formato de entrada | __________________ |
| **Decisión** (¿Cómo procesa?) | __________________ |
| Modelo de IA utilizado | __________________ |
| Instrucciones clave del prompt | __________________ |
| Criterios para escalar a humano | __________________ |
| **Acción** (¿Qué ejecuta?) | __________________ |
| Acciones posibles | __________________ |
| Sistemas externos que necesita | __________________ |

### Escenario B: Agente de Recursos Humanos

Una empresa quiere automatizar la primera fase de selección de candidatos: recibir CVs, analizarlos según los requisitos del puesto y enviar respuestas personalizadas a los candidatos.

| Componente | Descripción |
|------------|-------------|
| **Percepción** | __________________ |
| **Decisión** | __________________ |
| **Acción** | __________________ |

### Escenario C: Agente de Marketing de Contenidos

Un equipo de marketing necesita un agente que monitorice menciones de su marca en redes sociales, analice el sentimiento y genere borradores de respuesta para el community manager.

| Componente | Descripción |
|------------|-------------|
| **Percepción** | __________________ |
| **Decisión** | __________________ |
| **Acción** | __________________ |

### Escenario D: Agente Educativo (Tutor IA)

Una universidad quiere un agente que ayude a estudiantes con dudas sobre una asignatura, proporcionando explicaciones personalizadas y recomendando recursos de estudio.

| Componente | Descripción |
|------------|-------------|
| **Percepción** | __________________ |
| **Decisión** | __________________ |
| **Acción** | __________________ |

### Preguntas de Reflexión

1. ¿Cuál de los cuatro escenarios tiene la percepción más compleja? ¿Por qué? ¿Cómo afecta la complejidad de la percepción al diseño del agente?
2. En el Escenario A, el agente debe decidir cuándo escalar a un humano. ¿Qué criterios usarías para esta decisión? ¿Es mejor pecar de cauteloso (escalar demasiado) o de autónomo (intentar resolver todo)?
3. Compara los Escenarios B y C: ambos analizan texto, pero uno analiza documentos estructurados (CVs) y otro texto libre (redes sociales). ¿Cómo cambia esto el componente de decisión?
4. Si tuvieras que elegir un escenario para implementar como tu primer agente en n8n, ¿cuál elegirías y por qué? Considera la complejidad técnica, el valor de negocio y los riesgos.

---

## Ejercicio 2: Comparativa de Plataformas de Automatización

### Metadata
- **Duración estimada**: 15 minutos
- **Tipo**: Investigación/Análisis
- **Modalidad**: Parejas
- **Dificultad**: Básica
- **Prerequisitos**: Lectura de la sección 4.2 sobre introducción a n8n y su comparativa con Make y Zapier

### Contexto
En el mercado existen múltiples plataformas de automatización, cada una con sus fortalezas y limitaciones. Elegir la plataforma correcta para un proyecto específico es una decisión estratégica que impacta en costes, escalabilidad, seguridad y capacidades de IA. Este ejercicio te ayudará a desarrollar criterios de evaluación para tomar esta decisión de forma informada.

### Objetivo de Aprendizaje
- Comparar las tres plataformas principales de automatización no-code (n8n, Make, Zapier)
- Aplicar criterios de decisión a un caso de uso concreto
- Comprender las ventajas competitivas de n8n para agentes de IA
- Desarrollar argumentación técnica para la selección de herramientas

### Enunciado

### Parte A: Tabla de Decisión (7 min)

Tu equipo debe evaluar qué plataforma es más adecuada para el siguiente caso de uso:

> **Caso**: Una clínica dental con 3 sedes quiere automatizar la gestión de citas. El sistema debe: (1) recibir solicitudes de cita por WhatsApp, (2) consultar la disponibilidad en Google Calendar, (3) confirmar la cita al paciente, y (4) enviar recordatorios 24h antes. Además, quieren que un agente de IA responda preguntas frecuentes sobre tratamientos. Los datos de pacientes son sensibles (normativa sanitaria) y el presupuesto es limitado.

Completa la siguiente tabla de evaluación (puntúa de 1 a 5 cada criterio):

| Criterio | n8n | Make | Zapier | Peso (importancia) |
|----------|-----|------|--------|---------------------|
| Coste (menor es mejor) | ___ | ___ | ___ | Alta |
| Facilidad de uso | ___ | ___ | ___ | Media |
| Integración con WhatsApp | ___ | ___ | ___ | Alta |
| Capacidades de IA nativas | ___ | ___ | ___ | Alta |
| Despliegue on-premise (datos sensibles) | ___ | ___ | ___ | Muy Alta |
| Número de integraciones disponibles | ___ | ___ | ___ | Media |
| Soporte de la comunidad | ___ | ___ | ___ | Baja |
| Escalabilidad | ___ | ___ | ___ | Media |
| **Total ponderado** | ___ | ___ | ___ | |

**Instrucciones para el total ponderado:**
- Muy Alta = x4, Alta = x3, Media = x2, Baja = x1

### Parte B: Justificación de la Decisión (5 min)

Basándoos en la tabla, responded las siguientes preguntas:

1. **Plataforma recomendada**: ¿Cuál elegís y por qué?
2. **Factor determinante**: ¿Cuál fue el criterio que más influyó en vuestra decisión? ¿Cambiaría la decisión si ese criterio no fuera importante?
3. **Trade-offs**: ¿Qué desventajas tiene la plataforma elegida frente a las otras? ¿Cómo las mitigaríais?

### Parte C: Escenario Alternativo (3 min)

Ahora imaginad que el caso de uso cambia: en lugar de una clínica dental con datos sensibles, se trata de una **tienda de ropa online** que solo necesita automatizar publicaciones en Instagram y responder mensajes directos. ¿Cambiaría vuestra recomendación? ¿Por qué?

### Preguntas de Reflexión

1. ¿En qué situaciones elegirías Zapier a pesar de su mayor coste? ¿Cuándo es la simplicidad más valiosa que la flexibilidad?
2. El hecho de que n8n sea open source, ¿es siempre una ventaja? ¿Qué desafíos implica mantener una instancia propia frente a usar un servicio gestionado?

---

## Ejercicio 3: Primer Workflow en n8n

### Metadata
- **Duración estimada**: 30 minutos
- **Tipo**: Hands-on / Práctico
- **Modalidad**: Individual
- **Dificultad**: Básica
- **Prerequisitos**: n8n instalado y funcionando (local con Docker o n8n Cloud), lectura de secciones 4.3 y 4.4 sobre instalación y arquitectura de n8n

### Contexto
La mejor manera de aprender n8n es construyendo. En este ejercicio crearás tu primer workflow funcional que incluye los tres tipos de nodos fundamentales: un trigger que inicia la ejecución, un nodo de procesamiento que transforma datos y un nodo condicional que bifurca el flujo según una condición. Este patrón básico (trigger → procesamiento → condicional) es la base de la mayoría de las automatizaciones.

### Objetivo de Aprendizaje
- Crear un workflow desde cero en n8n
- Comprender el flujo de datos entre nodos (concepto de items y JSON)
- Utilizar el Manual Trigger para ejecutar y depurar workflows
- Configurar un nodo Set para definir y transformar datos
- Implementar lógica condicional con el nodo IF

### Enunciado

### Paso 1: Crear un Nuevo Workflow (2 min)

1. Abre n8n en tu navegador (por defecto: `http://localhost:5678`)
2. Haz clic en **"Add workflow"** (o el botón **+** en la esquina superior)
3. Dale un nombre descriptivo al workflow: `Ejercicio 3 - Mi Primer Workflow`

### Paso 2: Añadir el Manual Trigger (3 min)

1. Haz clic en el botón **"+"** en el canvas para añadir un nodo
2. Busca **"Manual Trigger"** y selecciónalo (también llamado "When clicking 'Test workflow'")
3. Este nodo se ejecutará cada vez que hagas clic en **"Test workflow"**

> **Nota**: El Manual Trigger es ideal para desarrollo y pruebas. En producción, lo sustituirías por un Webhook Trigger, Schedule Trigger u otro tipo de trigger automático.

### Paso 3: Añadir un Nodo Set (10 min)

1. Haz clic en el **"+"** que aparece a la derecha del Manual Trigger
2. Busca **"Edit Fields (Set)"** y selecciónalo
3. Configura los siguientes campos haciendo clic en **"Add Field"**:

| Campo | Tipo | Valor |
|-------|------|-------|
| `nombre` | String | `María García` |
| `edad` | Number | `28` |
| `curso` | String | `Aprendizaje Automático II` |
| `nota_final` | Number | `7.5` |
| `asistencia_porcentaje` | Number | `85` |

4. Haz clic en **"Test step"** para verificar que el nodo produce datos
5. Observa la pestaña **Output** a la derecha: deberías ver un JSON con los 5 campos

**Resultado esperado en la salida (Output):**
```json
[
  {
    "nombre": "María García",
    "edad": 28,
    "curso": "Aprendizaje Automático II",
    "nota_final": 7.5,
    "asistencia_porcentaje": 85
  }
]
```

> **Concepto clave**: En n8n, los datos fluyen entre nodos como **items**. Cada item es un objeto JSON. Un nodo puede producir uno o varios items que pasan al siguiente nodo.

### Paso 4: Añadir un Nodo IF (10 min)

1. Haz clic en el **"+"** a la derecha del nodo Set
2. Busca **"IF"** y selecciónalo
3. Configura la condición:
   - **Value 1**: Selecciona `{{ $json.nota_final }}` (haz clic en el campo y usa el selector de expresiones, o escribe directamente arrastrando el campo desde el panel izquierdo)
   - **Operation**: `is greater than or equal` (mayor o igual que)
   - **Value 2**: `5`

4. El nodo IF tiene dos salidas:
   - **true**: Se ejecuta cuando la condición se cumple (nota >= 5, aprobado)
   - **false**: Se ejecuta cuando la condición NO se cumple (nota < 5, suspenso)

### Paso 5: Añadir Nodos de Resultado (5 min)

1. En la salida **true** del IF, añade un nodo **Edit Fields (Set)** con:
   - Campo `resultado`: String, valor `Aprobado`
   - Campo `mensaje`: String, valor `Enhorabuena, {{ $json.nombre }}. Has aprobado con un {{ $json.nota_final }}.`

2. En la salida **false** del IF, añade otro nodo **Edit Fields (Set)** con:
   - Campo `resultado`: String, valor `Suspenso`
   - Campo `mensaje`: String, valor `Lo sentimos, {{ $json.nombre }}. No has alcanzado la nota mínima.`

> **Nota sobre expresiones**: Las dobles llaves `{{ }}` permiten usar expresiones en n8n. `$json` hace referencia a los datos que llegan del nodo anterior.

### Paso 6: Ejecutar y Verificar (5 min)

1. Haz clic en **"Test workflow"** (botón en la parte superior)
2. Observa cómo los datos fluyen por los nodos: cada nodo mostrará un indicador verde con el número de items procesados
3. Haz clic en cada nodo para inspeccionar su salida (Output)

**Verificaciones:**
- [ ] El Manual Trigger se ejecuta sin errores
- [ ] El nodo Set produce un item con los 5 campos
- [ ] El nodo IF evalúa correctamente la condición (nota 7.5 >= 5 → true)
- [ ] El flujo sigue por la rama **true** (aprobado)
- [ ] El mensaje final incluye el nombre y la nota del estudiante

### Paso 7: Experimentar (tiempo extra)

Modifica el valor de `nota_final` a `3.5` y vuelve a ejecutar el workflow. Verifica que ahora el flujo sigue por la rama **false** (suspenso).

**Diagrama del workflow completo:**
```
[Manual Trigger] → [Set: Datos Estudiante] → [IF: nota >= 5?]
                                                  ├── true → [Set: Aprobado]
                                                  └── false → [Set: Suspenso]
```

### Preguntas de Reflexión

1. ¿Qué ocurre si añades una segunda condición al nodo IF (por ejemplo, `asistencia_porcentaje >= 80`)? ¿Cómo combinarías ambas condiciones (AND/OR)?
2. El nodo Set define datos estáticos. En un workflow real, ¿de dónde vendrían estos datos? Nombra al menos 3 fuentes posibles (ej: formulario web, base de datos, API...).
3. ¿Cómo modificarías este workflow para procesar una lista de 10 estudiantes en lugar de uno solo? (Pista: el nodo Set puede producir múltiples items)

---

## Ejercicio 4: Diseño de Automatización con Schedule Trigger

### Metadata
- **Duración estimada**: 25 minutos
- **Tipo**: Diseño
- **Modalidad**: Individual
- **Dificultad**: Intermedia
- **Prerequisitos**: Comprensión de los tipos de nodos en n8n (sección 4.4), conocimiento básico de APIs REST

### Contexto
Muchas automatizaciones empresariales necesitan ejecutarse de forma periódica: resúmenes diarios, informes semanales, monitorizaciones cada hora... El Schedule Trigger de n8n permite programar estas ejecuciones automáticas. En este ejercicio diseñarás un workflow completo para un caso de uso real, combinando múltiples tipos de nodos en un flujo coherente.

### Objetivo de Aprendizaje
- Comprender el funcionamiento del Schedule Trigger y sus opciones de configuración
- Diseñar workflows multi-paso con bifurcaciones condicionales
- Planificar la integración de servicios externos (APIs, email)
- Documentar un diseño de workflow antes de implementarlo

### Enunciado

### Escenario

Tu jefe te pide diseñar un workflow en n8n que genere y envíe un **resumen diario de noticias sobre IA** cada mañana a las 8:00. El workflow debe:

1. Ejecutarse automáticamente todos los días laborables (lunes a viernes)
2. Obtener las últimas noticias sobre IA de una API de noticias
3. Filtrar solo las noticias en español o inglés
4. Generar un resumen con un modelo de IA
5. Enviar el resumen por email al equipo

### Parte A: Diagrama de Nodos (10 min)

Dibuja (en papel o en una herramienta de diagramas) el workflow completo identificando cada nodo necesario. Para cada nodo, indica:
- **Tipo de nodo** en n8n (nombre exacto)
- **Propósito** (qué hace en el flujo)
- **Datos de entrada** (qué recibe del nodo anterior)
- **Datos de salida** (qué produce para el siguiente nodo)

**Plantilla de nodos a considerar:**

```
Nodo 1: [Schedule Trigger]
   ├── Tipo: Schedule Trigger
   ├── Configuración: _______________
   ├── Entrada: Ninguna (es el trigger)
   └── Salida: Timestamp de ejecución

Nodo 2: [________________]
   ├── Tipo: _______________
   ├── Configuración: _______________
   ├── Entrada: _______________
   └── Salida: _______________

Nodo 3: [________________]
   ├── Tipo: _______________
   ├── Configuración: _______________
   ├── Entrada: _______________
   └── Salida: _______________

Nodo 4: [________________]
   ├── Tipo: _______________
   ├── Configuración: _______________
   ├── Entrada: _______________
   └── Salida: _______________

Nodo 5: [________________]
   ├── Tipo: _______________
   ├── Configuración: _______________
   ├── Entrada: _______________
   └── Salida: _______________
```

**Diagrama visual sugerido:**
```
[Schedule Trigger] → [HTTP Request] → [IF: ¿Hay noticias?]
    (L-V 8:00)       (API noticias)        ├── true → [OpenAI] → [Gmail]
                                           └── false → [Stop]
```

### Parte B: Configuración Detallada del Schedule Trigger (5 min)

Especifica la configuración exacta del Schedule Trigger:

| Parámetro | Valor | Justificación |
|-----------|-------|---------------|
| Trigger Times → Rule | _______________ | _______________ |
| Hora | _______________ | _______________ |
| Minuto | _______________ | _______________ |
| Días de la semana | _______________ | _______________ |
| Zona horaria | _______________ | _______________ |

**Pregunta**: ¿Qué ocurre si el servidor de n8n está apagado a las 8:00? ¿Se ejecutará el workflow cuando el servidor vuelva a estar online? Investiga el comportamiento de n8n en este caso.

### Parte C: Diseño del Nodo HTTP Request (5 min)

Para obtener las noticias, usarás la API gratuita de NewsAPI (https://newsapi.org). Diseña la configuración del nodo HTTP Request:

| Parámetro | Valor |
|-----------|-------|
| Method | `GET` |
| URL | `https://newsapi.org/v2/everything` |
| Query Parameters | |
| → `q` | _______________ |
| → `language` | _______________ |
| → `sortBy` | _______________ |
| → `pageSize` | _______________ |
| Authentication | _______________ |
| → Header Name | `X-Api-Key` |
| → Header Value | `{{ $credentials.newsApiKey }}` |

**Pregunta**: ¿Por qué es importante usar `$credentials` en lugar de poner la API key directamente en el nodo? ¿Cómo se configuran las credenciales en n8n?

### Parte D: Diseño del Prompt para el Resumen (5 min)

Escribe el System Prompt que usarías en el nodo de OpenAI (o el modelo de IA que prefieras) para generar el resumen:

```
System Prompt:
_______________________________________________
_______________________________________________
_______________________________________________
```

**Consideraciones para el prompt:**
- Longitud deseada del resumen (ej: 3-5 párrafos)
- Formato (ej: con títulos, bullets, enlaces)
- Tono (ej: profesional, informativo)
- Idioma de salida
- Qué información incluir de cada noticia (título, fuente, resumen, enlace)

### Preguntas de Reflexión

1. ¿Cómo manejarías el caso en que la API de noticias devuelve un error (ej: límite de peticiones excedido)? ¿Qué nodo añadirías y dónde?
2. Si quisieras enviar el resumen también por Slack además de por email, ¿cómo modificarías el diagrama? ¿Los nodos de Gmail y Slack irían en paralelo o en serie?
3. ¿Qué ventaja tiene programar el workflow a las 8:00 en vez de ejecutarlo manualmente cada mañana? Más allá del ahorro de tiempo, ¿qué otros beneficios aporta la automatización?

---

## Ejercicio 5: Configuración de Credenciales y Primer Nodo de IA

### Metadata
- **Duración estimada**: 20 minutos
- **Tipo**: Hands-on / Práctico
- **Modalidad**: Individual
- **Dificultad**: Básica
- **Prerequisitos**: n8n instalado y funcionando, cuenta en OpenAI con API key disponible, lectura de secciones 4.3 y 4.5

### Contexto
Antes de construir agentes de IA en n8n, necesitamos configurar las credenciales que permiten a n8n comunicarse con los proveedores de modelos de lenguaje. La gestión segura de credenciales es un aspecto crítico de cualquier plataforma de automatización: las API keys deben almacenarse de forma cifrada y nunca exponerse en los workflows. En este ejercicio configurarás tus primeras credenciales y verificarás que la conexión funciona correctamente.

### Objetivo de Aprendizaje
- Configurar credenciales de OpenAI en n8n de forma segura
- Comprender el sistema de gestión de credenciales de n8n
- Realizar una primera llamada a un modelo de IA desde n8n
- Verificar la conexión y diagnosticar errores comunes

### Enunciado

### Paso 1: Obtener tu API Key de OpenAI (3 min)

1. Accede a [platform.openai.com](https://platform.openai.com)
2. Ve a **API Keys** en el menú lateral
3. Crea una nueva API key (si no tienes una): haz clic en **"Create new secret key"**
4. **Copia la key inmediatamente** (solo se muestra una vez)
5. Verifica que tienes créditos disponibles en **Usage** > **Billing**

> **Importante**: Tu API key es como una contraseña. Nunca la compartas, no la pongas en código fuente y no la pegues en chats o documentos compartidos. n8n la almacenará cifrada.

### Paso 2: Configurar Credenciales en n8n (5 min)

1. En n8n, ve a **Settings** (icono de engranaje) > **Credentials**
2. Haz clic en **"Add Credential"**
3. Busca **"OpenAI"** en la lista de tipos de credencial
4. Rellena los campos:

| Campo | Valor |
|-------|-------|
| Credential Name | `OpenAI - Mi cuenta` |
| API Key | `sk-...` (pega tu API key) |

5. Haz clic en **"Save"**
6. n8n mostrará un mensaje de confirmación indicando que las credenciales se han guardado

> **Nota sobre seguridad**: n8n almacena las credenciales cifradas en su base de datos. Cuando usas Docker, la clave de cifrado se define mediante la variable de entorno `N8N_ENCRYPTION_KEY`. Asegúrate de que esta variable está configurada y respaldada.

### Paso 3: Crear un Workflow de Prueba con IA (7 min)

1. Crea un nuevo workflow llamado `Ejercicio 5 - Test OpenAI`
2. Añade los siguientes nodos en orden:

**Nodo 1: Manual Trigger**
- Tipo: `Manual Trigger`

**Nodo 2: OpenAI (Chat Model)**
- Tipo: Busca **"OpenAI"** en los nodos (no en la sección de AI, sino como nodo regular)
- Si no lo encuentras directamente, busca **"AI Agent"** y luego configura el modelo; o bien usa el nodo **"HTTP Request"** con la configuración de la API de OpenAI:

**Alternativa recomendada para prueba rápida - Nodo HTTP Request:**

| Parámetro | Valor |
|-----------|-------|
| Method | `POST` |
| URL | `https://api.openai.com/v1/chat/completions` |
| Authentication | Header Auth |
| → Name | `Authorization` |
| → Value | `Bearer {{ $credentials.openAiApi.apiKey }}` |
| Body Content Type | JSON |
| Body | Ver abajo |

**Body del request:**
```json
{
  "model": "gpt-4o-mini",
  "messages": [
    {
      "role": "system",
      "content": "Eres un asistente útil que responde en español de forma concisa."
    },
    {
      "role": "user",
      "content": "Explica en 2 frases qué es un agente de IA."
    }
  ],
  "max_tokens": 150,
  "temperature": 0.7
}
```

3. Conecta los nodos: `Manual Trigger → OpenAI / HTTP Request`

### Paso 4: Ejecutar y Verificar (5 min)

1. Haz clic en **"Test workflow"**
2. Inspecciona la salida del nodo de OpenAI/HTTP Request
3. Verifica que la respuesta contiene texto generado por el modelo

**Verificaciones:**
- [ ] Las credenciales se configuraron sin errores
- [ ] El nodo se conecta exitosamente a la API de OpenAI
- [ ] La respuesta contiene un campo `choices` con el texto generado
- [ ] El texto está en español como se solicitó en el system prompt
- [ ] No hay errores de autenticación (código 401) ni de cuota (código 429)

### Diagnóstico de Errores Comunes

Si la ejecución falla, consulta esta tabla:

| Error | Código HTTP | Causa Probable | Solución |
|-------|-------------|----------------|----------|
| Invalid API key | 401 | API key incorrecta o expirada | Verifica la key en platform.openai.com |
| Rate limit exceeded | 429 | Demasiadas peticiones | Espera unos segundos y reintenta |
| Insufficient quota | 429 | Sin créditos | Añade saldo en Billing |
| Model not found | 404 | Nombre de modelo incorrecto | Verifica que el modelo existe (ej: `gpt-4o-mini`) |
| Connection refused | - | n8n no puede acceder a internet | Verifica la configuración de red/Docker |

### Preguntas de Reflexión

1. ¿Qué diferencia hay entre usar el nodo nativo de OpenAI en n8n y hacer una llamada HTTP Request manual? ¿Cuándo preferirías uno sobre el otro?
2. ¿Qué pasaría si compartes el workflow exportado (JSON) con un compañero? ¿Se incluyen las credenciales en la exportación? ¿Por qué es importante que no se incluyan?
3. Si quisieras usar Claude (Anthropic) en lugar de OpenAI, ¿qué cambiarías en la configuración? ¿n8n soporta múltiples proveedores de IA?

---

## Ejercicio 6: Exploración de Templates de n8n

### Metadata
- **Duración estimada**: 15 minutos
- **Tipo**: Exploración/Investigación
- **Modalidad**: Individual
- **Dificultad**: Básica
- **Prerequisitos**: Familiaridad básica con la interfaz de n8n, comprensión del concepto de workflow y nodos

### Contexto
n8n cuenta con una biblioteca pública de templates (plantillas) con cientos de workflows pre-construidos por la comunidad y el equipo de n8n. Explorar estos templates es una excelente forma de aprender patrones de diseño, descubrir nodos que no conocías y acelerar el desarrollo de tus propios workflows. En particular, los templates de agentes de IA muestran las mejores prácticas para combinar modelos de lenguaje con herramientas y memoria.

### Objetivo de Aprendizaje
- Navegar y filtrar la biblioteca de templates de n8n
- Identificar templates relevantes para agentes de IA
- Analizar la estructura de workflows existentes para aprender patrones de diseño
- Evaluar qué templates pueden servir como punto de partida para proyectos propios

### Enunciado

### Parte A: Exploración de la Biblioteca (5 min)

1. Accede a la biblioteca de templates de n8n: [https://n8n.io/workflows/](https://n8n.io/workflows/)
2. Familiarízate con los filtros disponibles:
   - **Categoría** (ej: AI, Marketing, Sales, IT...)
   - **Nodos utilizados** (ej: OpenAI, Slack, Gmail...)
   - **Popularidad** y **fecha de publicación**

3. Realiza las siguientes búsquedas y anota cuántos resultados obtienes:

| Búsqueda | Número de resultados |
|----------|---------------------|
| "AI Agent" | ___ |
| "OpenAI" | ___ |
| "chatbot" | ___ |
| "email automation" | ___ |

### Parte B: Selección y Análisis de Templates (7 min)

Busca y selecciona **3 templates** que sean relevantes para construir agentes de IA. Para cada template, documenta la siguiente información:

**Template 1:**

| Aspecto | Descripción |
|---------|-------------|
| Nombre del template | __________________ |
| URL | __________________ |
| Descripción breve | __________________ |
| Nodos que utiliza (listado) | __________________ |
| ¿Usa nodo AI Agent? | Sí / No |
| ¿Incluye memoria? | Sí / No |
| ¿Qué herramientas (tools) usa el agente? | __________________ |
| ¿Qué trigger lo inicia? | __________________ |
| Complejidad estimada (Baja/Media/Alta) | __________________ |
| ¿Podrías usarlo como base para un proyecto propio? | __________________ |

**Template 2:**

| Aspecto | Descripción |
|---------|-------------|
| Nombre del template | __________________ |
| URL | __________________ |
| Descripción breve | __________________ |
| Nodos que utiliza (listado) | __________________ |
| ¿Usa nodo AI Agent? | Sí / No |
| ¿Incluye memoria? | Sí / No |
| ¿Qué herramientas (tools) usa el agente? | __________________ |
| ¿Qué trigger lo inicia? | __________________ |
| Complejidad estimada (Baja/Media/Alta) | __________________ |
| ¿Podrías usarlo como base para un proyecto propio? | __________________ |

**Template 3:**

| Aspecto | Descripción |
|---------|-------------|
| Nombre del template | __________________ |
| URL | __________________ |
| Descripción breve | __________________ |
| Nodos que utiliza (listado) | __________________ |
| ¿Usa nodo AI Agent? | Sí / No |
| ¿Incluye memoria? | Sí / No |
| ¿Qué herramientas (tools) usa el agente? | __________________ |
| ¿Qué trigger lo inicia? | __________________ |
| Complejidad estimada (Baja/Media/Alta) | __________________ |
| ¿Podrías usarlo como base para un proyecto propio? | __________________ |

### Parte C: Comparación y Patrones (3 min)

Responde las siguientes preguntas basándote en los 3 templates seleccionados:

1. **Patrón común**: ¿Qué nodos aparecen en los 3 templates? ¿Hay un patrón de diseño recurrente?
2. **Trigger más frecuente**: ¿Qué tipo de trigger es el más utilizado en templates de agentes de IA? ¿Por qué crees que es así?
3. **Memoria**: De los templates que incluyen memoria, ¿qué tipo de memoria usan (Window Buffer, PostgreSQL, etc.)? ¿Cómo afecta el tipo de memoria al comportamiento del agente?

### Preguntas de Reflexión

1. ¿Es mejor crear un workflow desde cero o partir de un template existente? ¿En qué situaciones preferirías cada enfoque?
2. Los templates de la comunidad pueden estar desactualizados o usar versiones antiguas de nodos. ¿Cómo verificarías que un template sigue siendo funcional antes de usarlo en un proyecto real?
3. Si tuvieras que crear un template para compartir con la comunidad, ¿qué workflow diseñarías? ¿Qué problema resolvería?

---

## Soluciones de Referencia

<details>
<summary>Ver solución Ejercicio 1 - Análisis del Paradigma PDA</summary>

### Escenario A: Agente de Soporte Técnico (eCommerce)

| Componente | Descripción |
|------------|-------------|
| **Percepción** | Mensaje del cliente vía chat, email o WhatsApp |
| Fuentes de datos | Chat en vivo, base de datos de pedidos, historial de interacciones, política de devoluciones |
| Formato de entrada | Texto libre (lenguaje natural del cliente) |
| **Decisión** | Un LLM (ej: GPT-4o o Claude) analiza el mensaje, identifica la intención (consulta de pedido, devolución, queja) y determina la acción apropiada |
| Modelo de IA utilizado | GPT-4o-mini (suficiente para soporte, buen balance coste/rendimiento) |
| Instrucciones clave del prompt | "Eres un agente de soporte de [tienda]. Responde de forma amable y profesional. Consulta el estado del pedido antes de responder. Si el cliente menciona problemas legales, defectos de seguridad o solicita hablar con un humano, escala inmediatamente." |
| Criterios para escalar a humano | Solicitud explícita del cliente, temas legales, queja repetida (>2 interacciones sin resolución), devoluciones de alto valor (>200 EUR) |
| **Acción** | Responder al cliente con información del pedido, iniciar proceso de devolución en el ERP, escalar ticket a agente humano, enviar email de confirmación |
| Acciones posibles | Consultar API de tracking, crear ticket en Zendesk, enviar email, actualizar CRM |
| Sistemas externos que necesita | Base de datos de pedidos, sistema de tracking, Zendesk/Freshdesk, email (SMTP/Gmail) |

### Escenario B: Agente de Recursos Humanos

| Componente | Descripción |
|------------|-------------|
| **Percepción** | CVs recibidos por email o formulario web, descripción del puesto con requisitos, historial de candidatos previos |
| **Decisión** | El LLM analiza cada CV extrayendo información clave (experiencia, formación, habilidades), la compara con los requisitos del puesto y genera una puntuación de idoneidad. Decide si el candidato pasa a la siguiente fase, se descarta o requiere revisión humana |
| **Acción** | Enviar email personalizado al candidato (aceptación para entrevista, rechazo cortés o solicitud de información adicional), actualizar el ATS (Applicant Tracking System), notificar al reclutador sobre candidatos destacados |

### Escenario C: Agente de Marketing de Contenidos

| Componente | Descripción |
|------------|-------------|
| **Percepción** | Menciones de marca en Twitter/X, Instagram, LinkedIn (vía APIs de redes sociales o herramientas de social listening), notificaciones en tiempo real o monitorización periódica |
| **Decisión** | El LLM analiza el sentimiento de cada mención (positivo, negativo, neutro), clasifica la urgencia (mención casual vs. crisis potencial), determina si requiere respuesta y genera un borrador de respuesta adaptado al tono de la marca |
| **Acción** | Guardar la mención y su análisis en una base de datos, enviar borrador de respuesta al community manager vía Slack, alertar al equipo de crisis si el sentimiento es muy negativo, generar informe semanal de menciones |

### Escenario D: Agente Educativo (Tutor IA)

| Componente | Descripción |
|------------|-------------|
| **Percepción** | Pregunta del estudiante vía chat, historial de preguntas anteriores del mismo estudiante, materiales del curso (apuntes, presentaciones, ejercicios) |
| **Decisión** | El LLM interpreta la duda del estudiante, identifica el tema y el nivel de comprensión, busca en los materiales del curso la información relevante y genera una explicación adaptada al nivel del estudiante. Decide si recomendar recursos adicionales o sugerir tutoría presencial |
| **Acción** | Responder con una explicación personalizada, compartir enlaces a recursos específicos (vídeos, capítulos del libro, ejercicios), registrar la interacción para seguimiento del profesor, enviar alerta al profesor si detecta dificultades recurrentes |

### Respuestas a las preguntas de reflexión

1. El Escenario C (Marketing) tiene la percepción más compleja porque necesita monitorizar múltiples fuentes de datos en tiempo real (varias redes sociales), procesar diferentes formatos (texto, imágenes, vídeos) y gestionar un flujo continuo de información. Esto requiere múltiples integraciones y un sistema de filtrado para evitar sobrecarga.

2. Para el escalado a humano, es mejor pecar de cauteloso al principio e ir calibrando con el tiempo. Un agente que resuelve incorrectamente un caso daña la confianza del cliente y la marca. Criterios progresivos: empezar escalando todo lo que no sea consulta directa de pedido, y gradualmente ampliar la autonomía del agente conforme se valida su rendimiento.

3. Los CVs (Escenario B) tienen estructura semi-predecible (secciones de experiencia, formación, etc.), lo que facilita la extracción de información. Las redes sociales (Escenario C) son texto completamente libre, con jerga, ironía, emojis y contexto cultural que dificultan el análisis de sentimiento. El componente de decisión en C necesita mayor sofisticación lingüística.

4. Respuesta abierta. El Escenario A suele ser la mejor opción para empezar: la percepción es clara (mensajes de chat), las acciones son acotadas (consultar pedido, responder) y el valor de negocio es inmediato (reducción de carga del equipo de soporte). El riesgo es moderado si se implementa escalado a humano.

</details>

<details>
<summary>Ver solución Ejercicio 2 - Comparativa de Plataformas</summary>

### Parte A: Tabla de Evaluación

| Criterio | n8n | Make | Zapier | Peso |
|----------|-----|------|--------|------|
| Coste (menor es mejor) | 5 | 3 | 2 | Alta (x3) |
| Facilidad de uso | 3 | 4 | 5 | Media (x2) |
| Integración con WhatsApp | 4 | 4 | 4 | Alta (x3) |
| Capacidades de IA nativas | 5 | 3 | 3 | Alta (x3) |
| Despliegue on-premise | 5 | 1 | 1 | Muy Alta (x4) |
| Número de integraciones | 3 | 4 | 5 | Media (x2) |
| Soporte de la comunidad | 4 | 3 | 4 | Baja (x1) |
| Escalabilidad | 4 | 4 | 3 | Media (x2) |

**Total ponderado:**
- **n8n**: 5x3 + 3x2 + 4x3 + 5x3 + 5x4 + 3x2 + 4x1 + 4x2 = 15+6+12+15+20+6+4+8 = **86**
- **Make**: 3x3 + 4x2 + 4x3 + 3x3 + 1x4 + 4x2 + 3x1 + 4x2 = 9+8+12+9+4+8+3+8 = **61**
- **Zapier**: 2x3 + 5x2 + 4x3 + 3x3 + 1x4 + 5x2 + 4x1 + 3x2 = 6+10+12+9+4+10+4+6 = **61**

### Parte B: Justificación

1. **Plataforma recomendada**: n8n. Gana en los criterios más ponderados: despliegue on-premise (imprescindible para datos sanitarios), coste (clínica con presupuesto limitado) y capacidades de IA nativas (agente para FAQ).

2. **Factor determinante**: El despliegue on-premise. Si la normativa sanitaria no exigiera control de datos, Make o Zapier podrían ser opciones viables. Sin este criterio, el resultado sería más equilibrado.

3. **Trade-offs de n8n**: Menor número de integraciones predefinidas (pero se puede suplir con HTTP Request), curva de aprendizaje mayor que Zapier (mitigable con templates y documentación), y necesidad de mantener la infraestructura propia (mitigable con Docker y backups automatizados).

### Parte C: Escenario Alternativo

Para la tienda de ropa online, **Zapier** sería la mejor opción: no hay requisitos de privacidad de datos sensibles, la integración con Instagram es nativa y robusta, la facilidad de uso reduce el tiempo de implementación, y el equipo de marketing probablemente no tiene perfil técnico para mantener una instancia de n8n.

</details>

<details>
<summary>Ver solución Ejercicio 4 - Diseño de Automatización con Schedule Trigger</summary>

### Parte A: Diagrama de Nodos

```
Nodo 1: [Schedule Trigger]
   ├── Tipo: Schedule Trigger
   ├── Configuración: Lunes a Viernes, 8:00 AM, Europe/Madrid
   ├── Entrada: Ninguna
   └── Salida: { timestamp: "2026-02-21T08:00:00.000Z" }

Nodo 2: [HTTP Request - NewsAPI]
   ├── Tipo: HTTP Request
   ├── Configuración: GET https://newsapi.org/v2/everything?q=artificial+intelligence&language=es&sortBy=publishedAt&pageSize=10
   ├── Entrada: Timestamp del trigger
   └── Salida: Array de artículos con título, descripción, URL, fuente

Nodo 3: [IF - ¿Hay noticias?]
   ├── Tipo: IF
   ├── Configuración: {{ $json.totalResults }} is greater than 0
   ├── Entrada: Respuesta de NewsAPI
   └── Salida: true (hay noticias) / false (no hay noticias)

Nodo 4: [OpenAI - Generar Resumen]
   ├── Tipo: HTTP Request (POST a OpenAI API)
   ├── Configuración: Model gpt-4o-mini, System prompt con instrucciones de resumen
   ├── Entrada: Array de artículos filtrados
   └── Salida: Texto del resumen en formato HTML/Markdown

Nodo 5: [Gmail - Enviar Resumen]
   ├── Tipo: Gmail
   ├── Configuración: To: equipo@empresa.com, Subject: "Resumen IA - {{ $now.format('dd/MM/yyyy') }}"
   ├── Entrada: Texto del resumen generado
   └── Salida: Confirmación de envío
```

### Parte B: Configuración del Schedule Trigger

| Parámetro | Valor | Justificación |
|-----------|-------|---------------|
| Trigger Times → Rule | Cron Expression | Permite especificar días y hora exacta |
| Expresión Cron | `0 8 * * 1-5` | Minuto 0, hora 8, cualquier día del mes, cualquier mes, lunes(1) a viernes(5) |
| Zona horaria | Europe/Madrid | Para que las 8:00 sean hora local española |

Si el servidor está apagado a las 8:00, n8n NO ejecutará el workflow retroactivamente cuando vuelva a estar online (por defecto). Las ejecuciones perdidas se pierden. Para mitigar esto, es recomendable monitorizar la disponibilidad del servidor y/o configurar alertas.

### Parte C: HTTP Request

| Parámetro | Valor |
|-----------|-------|
| `q` | `"artificial intelligence" OR "inteligencia artificial" OR "AI agents"` |
| `language` | `es` |
| `sortBy` | `publishedAt` |
| `pageSize` | `10` |

Usar `$credentials` es fundamental porque: (1) la API key se almacena cifrada en n8n, (2) no se expone al exportar el workflow, (3) se puede revocar y actualizar sin modificar el workflow, y (4) se puede compartir entre múltiples workflows.

### Parte D: System Prompt

```
Eres un asistente especializado en resumir noticias de inteligencia artificial para un equipo técnico.

Genera un resumen diario con las siguientes características:
- Título: "Resumen de IA - [fecha de hoy]"
- Incluye entre 3 y 5 noticias destacadas
- Para cada noticia incluye: título, fuente, resumen de 2-3 frases y enlace original
- Organiza las noticias por relevancia (de mayor a menor impacto)
- Al final, incluye una sección "Tendencia del día" con una reflexión breve sobre el tema dominante
- Escribe en español, con tono profesional e informativo
- Usa formato HTML para que el email se vea bien formateado
- Longitud total: máximo 500 palabras
```

</details>

<details>
<summary>Ver solución Ejercicio 5 - Configuración de Credenciales</summary>

### Respuestas a las preguntas de reflexión

1. **Nodo nativo vs HTTP Request**: El nodo nativo de OpenAI abstrae la complejidad de la API (no necesitas recordar la URL, los headers ni el formato del body). Es más rápido de configurar y menos propenso a errores. Sin embargo, el HTTP Request ofrece más control: puedes acceder a endpoints que el nodo nativo no soporta, personalizar headers, usar modelos de otros proveedores con API compatible (ej: modelos locales con API OpenAI-compatible), y depurar más fácilmente viendo la petición y respuesta completas.

2. **Exportación de workflows**: Al exportar un workflow como JSON, las credenciales NO se incluyen (por seguridad). Solo se incluye una referencia al nombre de la credencial. El destinatario deberá configurar sus propias credenciales con el mismo nombre o remapearlas al importar. Esto es un diseño intencional para evitar fugas de API keys.

3. **Claude en lugar de OpenAI**: Para usar Claude (Anthropic), necesitarías: (a) crear credenciales de tipo "Anthropic" o "HTTP Header Auth" en n8n, (b) cambiar la URL del endpoint a `https://api.anthropic.com/v1/messages`, (c) ajustar el formato del body (Anthropic usa un formato diferente al de OpenAI), y (d) cambiar el header de autenticación a `x-api-key`. n8n soporta múltiples proveedores de IA de forma nativa: OpenAI, Anthropic, Google (Gemini), Ollama (modelos locales), Hugging Face, entre otros.

</details>

<details>
<summary>Ver solución Ejercicio 6 - Exploración de Templates</summary>

### Nota sobre los Templates

Los templates de n8n se actualizan frecuentemente, por lo que los resultados exactos de búsqueda pueden variar. A continuación se muestra un ejemplo representativo de lo que podrías encontrar:

### Ejemplos de Templates Relevantes para Agentes de IA

**Template 1: AI Agent Chat**

| Aspecto | Descripción |
|---------|-------------|
| Nombre del template | AI Agent Chat |
| Descripción breve | Un agente conversacional con memoria que puede mantener conversaciones multi-turno |
| Nodos que utiliza | Chat Trigger, AI Agent, OpenAI Chat Model, Window Buffer Memory |
| ¿Usa nodo AI Agent? | Sí |
| ¿Incluye memoria? | Sí (Window Buffer Memory) |
| ¿Qué herramientas usa? | Ninguna adicional (solo conversación) |
| ¿Qué trigger lo inicia? | Chat Trigger (interfaz de chat embebida) |
| Complejidad estimada | Baja |

**Template 2: AI Agent with Tools**

| Aspecto | Descripción |
|---------|-------------|
| Nombre del template | AI Agent with Custom Tools |
| Descripción breve | Agente que puede buscar en internet, hacer cálculos y consultar APIs externas |
| Nodos que utiliza | Chat Trigger, AI Agent, OpenAI Chat Model, SerpAPI Tool, Calculator Tool, HTTP Request Tool |
| ¿Usa nodo AI Agent? | Sí |
| ¿Incluye memoria? | Sí |
| ¿Qué herramientas usa? | SerpAPI (búsqueda web), Calculator, HTTP Request |
| ¿Qué trigger lo inicia? | Chat Trigger |
| Complejidad estimada | Media |

**Template 3: Customer Support Agent**

| Aspecto | Descripción |
|---------|-------------|
| Nombre del template | Customer Support AI Agent |
| Descripción breve | Agente de soporte al cliente que consulta una base de conocimiento y puede escalar tickets |
| Nodos que utiliza | Webhook Trigger, AI Agent, OpenAI Chat Model, Postgres (memoria), Vector Store Tool |
| ¿Usa nodo AI Agent? | Sí |
| ¿Incluye memoria? | Sí (PostgreSQL para persistencia) |
| ¿Qué herramientas usa? | Vector Store (búsqueda semántica en documentos), Webhook (para integraciones) |
| ¿Qué trigger lo inicia? | Webhook Trigger |
| Complejidad estimada | Alta |

### Parte C: Patrones Observados

1. **Patrón común**: Todos usan el nodo AI Agent + un modelo de chat (OpenAI Chat Model es el más frecuente) + alguna forma de trigger. El patrón recurrente es: `Trigger → AI Agent (con modelo + memoria + herramientas)`.

2. **Trigger más frecuente**: El Chat Trigger es el más utilizado en templates de agentes de IA, porque la mayoría de los agentes están diseñados para interacción conversacional. Para integraciones en producción, se usan Webhook Triggers.

3. **Tipos de memoria**: Window Buffer Memory es la opción más simple (almacena los últimos N mensajes en memoria del proceso). PostgreSQL o Supabase proporcionan persistencia entre ejecuciones. La elección depende de si el agente necesita recordar conversaciones entre sesiones (persistente) o solo dentro de una conversación activa (buffer).

</details>
