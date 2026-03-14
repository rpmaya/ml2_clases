# Práctica Evaluable - Unidad 4
## Agente de IA con n8n

---

## Información General

| Campo | Valor |
|-------|-------|
| **Unidad** | 4 - Automatización con n8n y Agentes de IA |
| **Tipo** | Práctica individual |
| **Duración estimada** | 120-150 minutos |
| **Entrega** | En GitHub con workflow (JSON), documentación y reflexión |
| **Fecha límite** | Según calendario del curso |

---

## Objetivo

Diseñar e implementar un **agente de IA funcional** en n8n que utilice un modelo de lenguaje, memoria conversacional y herramientas externas para resolver un caso práctico real. La práctica se divide en un ejercicio guiado inicial y un caso práctico a elegir entre tres opciones.

### Objetivos de Aprendizaje

1. Configurar un agente de IA completo en n8n con modelo de lenguaje, memoria y herramientas
2. Diseñar instrucciones (system prompt) efectivas con Rol, Tareas, Restricciones y Formato
3. Integrar herramientas externas que amplíen las capacidades del agente
4. Documentar y probar un sistema de IA conversacional

---

## Ejercicio 0: Agente Q&A con n8n (Guiado) - 30-45 min

### Contexto

Este ejercicio guiado te permitirá construir paso a paso tu primer agente de IA en n8n. Al completarlo, tendrás una base sólida para abordar el caso práctico elegido. **Este ejercicio no se entrega**, pero es fundamental realizarlo antes de continuar.

### Paso 1: Configurar el Proyecto

1. Crea un nuevo workflow en n8n con el nombre **"Mi Agente Q&A"**
2. Añade el nodo **"When chat message received"** como trigger

### Paso 2: Añadir el Modelo de IA

1. Añade un nodo **"AI Agent"** y conéctalo al Chat Trigger
2. Haz clic en **"+ Chat Model"** dentro del nodo AI Agent
3. Selecciona uno de los siguientes modelos:
   - **OpenAI:** `gpt-4o-mini`
   - **Google Gemini:** `gemini-1.5-flash`
4. Configura las credenciales del proveedor elegido

### Paso 3: Configurar las Instrucciones Básicas

En el campo **System Prompt** del nodo AI Agent, escribe las instrucciones siguiendo esta estructura:

```
# Rol
Eres un asistente experto en [TU TEMA ELEGIDO].

# Tareas
- Responder a: {{ $json.chatInput }}
- Ser claro y conciso
- Si no sabes algo, admítelo honestamente

# Formato
- Respuestas de máximo 200 palabras
- Usa ejemplos cuando sea útil
```

> **Nota:** Elige un tema que conozcas bien (cocina, deportes, tecnología, historia...) para que puedas evaluar la calidad de las respuestas del agente.

### Paso 4: Añadir Memoria

1. Dentro del nodo AI Agent, haz clic en **"+ Memory"**
2. Selecciona **"Window Buffer Memory"**
3. Configura **Context Window Length: 10** (el agente recordará los últimos 10 mensajes)
4. Prueba la memoria con esta secuencia:
   - Escribe: *"Me llamo [tu nombre]"*
   - Luego pregunta: *"¿Cómo me llamo?"*
   - El agente debería recordar tu nombre

### Paso 5: Añadir una Herramienta

1. Dentro del nodo AI Agent, haz clic en **"+ Tool"**
2. Selecciona **"Wikipedia"**
3. Actualiza el System Prompt añadiendo una sección de herramientas:

```
# Rol
Eres un asistente experto en [TU TEMA ELEGIDO].

# Tareas
- Responder a: {{ $json.chatInput }}
- Ser claro y conciso
- Si no sabes algo, admítelo honestamente

# Herramientas
- Usa Wikipedia para verificar datos o ampliar información
- Siempre cita la fuente cuando uses Wikipedia

# Formato
- Respuestas de máximo 200 palabras
- Usa ejemplos cuando sea útil
```

4. Prueba haciendo preguntas que requieran consultar Wikipedia

> **Conexión con la teoría:** El patrón que acabas de construir (LLM + Memoria + Herramientas) es la arquitectura fundamental de un agente de IA, tal como se estudió en la sesión teórica. El agente decide de forma autónoma cuándo y cómo usar las herramientas disponibles.

---

## Casos Prácticos (Elegir UNO)

Una vez completado el Ejercicio 0, elige **uno** de los siguientes casos prácticos para desarrollar tu agente completo. Este es el trabajo que deberás entregar.

---

### Caso 1: Agente de Atención al Cliente para eCommerce (Intermedia)

#### Contexto

Construirás un agente que actúe como asistente de atención al cliente para una tienda online, capaz de consultar el inventario real desde una hoja de cálculo de Google Sheets.

#### Requisitos Previos

- Credenciales **Google OAuth2** configuradas en n8n
- Una hoja de **Google Sheets** con un inventario de 5-10 productos (nombre, precio, stock, descripción)

#### Instrucciones

1. Crea un nuevo workflow basándote en lo aprendido en el Ejercicio 0
2. Configura el nodo **AI Agent** con un modelo de lenguaje
3. Añade la herramienta **Google Sheets** con la operación **"Get Rows"** para que el agente pueda consultar el inventario
4. Diseña un System Prompt completo que incluya:
   - **Rol:** Asistente de atención al cliente de la tienda
   - **Tareas:** Consultar inventario, responder sobre productos, informar sobre políticas
   - **Restricciones:** No inventar productos que no estén en el inventario, no dar información falsa sobre stock
   - **Formato:** Respuestas amables y profesionales
5. Configura la **memoria** para mantener el contexto de la conversación
6. Realiza al menos **5 conversaciones de prueba** que demuestren:
   - Consulta de productos disponibles
   - Pregunta sobre un producto fuera de stock
   - Consulta sobre políticas (envíos, devoluciones)
   - Intento de preguntar por un producto inexistente
   - Conversación con contexto (preguntas encadenadas)

#### El agente debe:

- Consultar el inventario real desde Google Sheets
- Responder correctamente sobre disponibilidad y precios
- Informar sobre políticas de la tienda (envíos, devoluciones, etc.)
- **No inventar productos** que no estén en el inventario

---

### Caso 2: Agente de Envío de Emails Inteligente (Intermedia)

#### Contexto

Construirás un agente conversacional que ayude al usuario a componer y enviar emails de forma guiada, asegurándose de que el usuario confirme antes de enviar.

#### Requisitos Previos

- Credenciales **Google OAuth2** configuradas en n8n para Gmail
- Acceso a una cuenta de Gmail para pruebas

#### Instrucciones

1. Crea un nuevo workflow basándote en lo aprendido en el Ejercicio 0
2. Configura el nodo **AI Agent** con un modelo de lenguaje
3. Añade la herramienta **Gmail** utilizando la función `$fromAI()` para los campos dinámicos (destinatario, asunto, cuerpo)
4. Diseña un System Prompt completo que incluya:
   - **Rol:** Asistente de redacción y envío de emails
   - **Tareas:** Preguntar destinatario y propósito, proponer borrador, enviar tras confirmación
   - **Restricciones:** SOLO enviar cuando el usuario confirme explícitamente, siempre mostrar borrador antes
   - **Formato:** Presentar el borrador de forma clara antes de solicitar confirmación
5. Configura la **memoria** para mantener el contexto de la conversación
6. Realiza al menos **5 conversaciones de prueba** que demuestren:
   - Flujo completo de composición y envío
   - Modificación del borrador antes de enviar
   - Cancelación de un envío
   - Diferentes tipos de email (formal, informal)
   - Uso correcto de la confirmación antes del envío

#### El agente debe:

- Preguntar al usuario el destinatario y el propósito del email
- Proponer un borrador del email antes de enviar
- **SOLO enviar cuando el usuario confirme** explícitamente
- Permitir modificaciones al borrador

---

### Caso 3: Asistente Personal con Búsqueda y Cálculo (Básica-Intermedia)

#### Contexto

Construirás un asistente personal versátil que combine búsqueda de información y capacidad de cálculo matemático, utilizando herramientas integradas en n8n.

#### Requisitos Previos

- No requiere credenciales externas adicionales (usa herramientas integradas en n8n)

#### Instrucciones

1. Crea un nuevo workflow basándote en lo aprendido en el Ejercicio 0
2. Configura el nodo **AI Agent** con un modelo de lenguaje
3. Añade dos herramientas:
   - **Wikipedia:** Para búsqueda de conocimiento general
   - **Calculator:** Para operaciones matemáticas
4. Diseña un System Prompt completo que incluya:
   - **Rol:** Asistente personal inteligente
   - **Tareas:** Responder preguntas generales usando Wikipedia, resolver cálculos matemáticos, combinar ambas capacidades
   - **Restricciones:** Usar Wikipedia para datos factuales, Calculator para matemáticas, citar fuentes
   - **Formato:** Respuestas claras y estructuradas
5. Configura la **memoria** para mantener el contexto de la conversación
6. Realiza al menos **5 conversaciones de prueba** que demuestren:
   - Pregunta que requiera buscar en Wikipedia
   - Cálculo matemático
   - Pregunta que combine búsqueda y cálculo (ej: "¿Cuál es la población de España y cuánto es el 15% de esa cifra?")
   - Conversación con contexto mantenido
   - Pregunta compleja que requiera razonamiento

#### El agente debe:

- Usar **Wikipedia** para responder preguntas de conocimiento general
- Usar **Calculator** para resolver operaciones matemáticas
- Mantener el contexto de la conversación con la memoria

---

## Recomendaciones

- **Completa primero el Ejercicio 0** guiado antes de abordar el caso práctico
- **Documenta cada paso** con capturas de pantalla del workflow y de las conversaciones
- Realiza **al menos 5 conversaciones de prueba** variadas y significativas
- Asegúrate de que el **workflow funciona sin errores** antes de exportar
- Las **instrucciones del agente** (System Prompt) deben ser completas e incluir Rol, Tareas, Restricciones y Formato
- La **reflexión personal** debe ser específica sobre tu experiencia, no genérica

---

## Rúbrica de Evaluación

| Criterio | Descripción | Puntos |
|----------|-------------|--------|
| **Funcionalidad** | El workflow se ejecuta sin errores y el agente responde correctamente | **3** |
| **Instrucciones del agente** | System Prompt bien estructurado con Rol, Tareas, Restricciones y Formato | **2** |
| **Memoria** | Memoria configurada y demostrada funcionando correctamente | **1.5** |
| **Herramientas** | Al menos una herramienta integrada y utilizada correctamente | **1.5** |
| **Documentación** | Capturas de pantalla, pruebas de conversación y reflexión completas | **2** |
| **TOTAL** | | **10** |

### Bonificaciones (hasta +1 punto adicional)

| Bonificación | Descripción | Puntos extra |
|--------------|-------------|--------------|
| Canal externo | Agente desplegado en **Telegram** u otro canal de mensajería | **+0.5** |
| Memoria persistente | Uso de memoria persistente con **PostgreSQL** o **Supabase** | **+0.5** |

---

## Formato y Proceso de Entrega

### Nombre del Archivo

```
en tu repo de github en la carpeta practicas/unidad4
```

### Contenido del directorio en tu repo

1. **Workflow JSON:** Archivo `.json` exportado desde n8n (Menú > Descargar > Export Workflow)
2. **Documento de pruebas:** Archivo PDF o Word con capturas de pantalla de:
   - El workflow completo en n8n
   - Las conversaciones de prueba (mínimo 5)
   - El System Prompt utilizado
3. **Reflexión:** Texto de máximo 400 palabras (puede ir dentro del documento de pruebas o como archivo separado) respondiendo:
   - ¿Qué caso práctico elegiste y por qué?
   - ¿Qué dificultades encontraste durante el desarrollo?
   - ¿Qué mejoras añadirías al agente si tuvieras más tiempo?
   - ¿Cómo aplicarías este tipo de agentes en un contexto profesional real?
4. **Datos auxiliares** (si aplica): Hojas de cálculo u otros archivos necesarios para reproducir el workflow

> **Nota:** El Ejercicio 0 (Agente Q&A guiado) **no se entrega**. Solo se evalúa el caso práctico elegido (Caso 1, 2 ó 3).

### Proceso de Entrega

1. Exporta el workflow desde n8n en formato JSON
2. Prepara el documento de pruebas con capturas y reflexión
3. Sube el contenido a un directorio de tu repo github
4. Copia la url en Blackboard: https://github.com/tunombre/practica_unidad4/

---

## Recursos Útiles

### Herramientas

- [n8n - Documentación oficial](https://docs.n8n.io/)
- [n8n - AI Agent node](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/)
- [n8n - Community](https://community.n8n.io/)

### Referencias

- [Sesión 1 - Teoría](./sesion_1/teoria.md)
- [Sesión 2 - Teoría](./sesion_2/teoria.md)
- [n8n - Templates de AI Agents](https://n8n.io/workflows/?categories=AI)
- [OpenAI - API Keys](https://platform.openai.com/api-keys)
- [Google AI Studio - API Keys](https://aistudio.google.com/app/apikey)

---

## Notas Finales

- Esta práctica es **individual**
- Puedes consultar la documentación oficial de n8n y los materiales del curso
- Se valora la originalidad en el diseño de las instrucciones del agente y en la reflexión personal
- Asegúrate de que el workflow exportado funciona correctamente al importarlo
- Si usas credenciales, **no las incluyas en la entrega** (se configurarán en el entorno del evaluador)

