# Ejercicios Prácticos - Unidad 5, Sesión 2
## Implementación y Optimización de Sistemas RAG

---

## Ejercicio 1: Workflow de Ingesta de Documentos en n8n

### Metadata
- **Duración estimada**: 35 minutos
- **Tipo**: Hands-on
- **Modalidad**: Individual
- **Dificultad**: Intermedia
- **Prerequisitos**: n8n instalado y funcionando, cuenta de Pinecone con índice creado (dimensión 1536), API key de OpenAI, carpeta en Google Drive con al menos 3 documentos de texto (PDF, TXT o Google Docs)

### Contexto
El primer paso para construir un sistema RAG funcional es la ingesta de documentos: tomar los documentos fuente, dividirlos en fragmentos manejables, convertirlos en vectores (embeddings) y almacenarlos en una base de datos vectorial. En n8n, este proceso se construye como un workflow que conecta un origen de datos (Google Drive), un procesador de texto (chunking), un modelo de embeddings (OpenAI) y un destino vectorial (Pinecone). Una vez que los documentos están indexados, el agente RAG podrá buscar en ellos para responder preguntas.

### Objetivo de Aprendizaje
- Construir un workflow completo de ingesta de documentos en n8n
- Configurar la conexión entre Google Drive, OpenAI Embeddings y Pinecone
- Comprender el proceso de chunking y su impacto en la calidad de las búsquedas
- Verificar que los vectores se han creado correctamente en Pinecone

### Enunciado

### Paso 1: Preparar los documentos fuente (5 min)

1. En Google Drive, crea una carpeta llamada **"RAG_Documentos"**
2. Sube al menos 3 documentos de ejemplo. Se recomienda usar documentos sobre un tema concreto para poder verificar las búsquedas después. Por ejemplo, documentos sobre:
   - Normativa interna de una empresa ficticia (vacaciones, teletrabajo, horarios)
   - Manual de un producto o servicio
   - Preguntas frecuentes de un sitio web
3. Asegúrate de que los documentos contienen texto suficiente (al menos 1-2 páginas cada uno)

### Paso 2: Crear el workflow de ingesta (10 min)

1. Abre n8n y crea un nuevo workflow llamado **"RAG - Ingesta de Documentos"**
2. Añade un nodo **"Manual Trigger"** (usaremos ejecución manual para controlar cuándo se indexa)
3. Añade un nodo **"Google Drive"**:
   - Operation: **"List Files in Folder"**
   - Crea o selecciona la credencial de Google Drive (OAuth2)
   - Folder: Selecciona la carpeta **"RAG_Documentos"**
   - Filter: Filtra por tipos de archivo relevantes
4. Añade un nodo **"Google Drive"** (segundo nodo):
   - Operation: **"Download File"**
   - File ID: `{{ $json.id }}` (del nodo anterior)
5. Conecta: **Manual Trigger → List Files → Download File**

### Paso 3: Configurar el procesamiento y vectorización (10 min)

1. Añade un nodo **"Default Data Loader"**:
   - Este nodo convierte el contenido binario del archivo en texto procesable
   - Data Type: **"Binary"**

2. Añade un nodo **"Recursive Character Text Splitter"**:
   - Chunk Size: `1000` (caracteres por fragmento)
   - Chunk Overlap: `200` (solapamiento entre fragmentos para mantener contexto)

3. Añade un nodo **"Embeddings OpenAI"**:
   - Model: `text-embedding-ada-002` (o `text-embedding-3-small` si está disponible)
   - Usa tus credenciales de OpenAI

4. Añade un nodo **"Pinecone Vector Store"**:
   - Operation: **"Insert Documents"**
   - Crea una credencial de Pinecone con tu API key
   - Selecciona tu índice (debe tener dimensión 1536 para ada-002, o 1536 para text-embedding-3-small)

5. Conecta los subnodos al nodo de Pinecone:
   - El **Default Data Loader** se conecta como "Document Loader"
   - El **Text Splitter** se conecta como "Text Splitter" (subnodo del Data Loader)
   - El **Embeddings OpenAI** se conecta como "Embedding"

### Paso 4: Ejecutar y verificar (10 min)

1. Ejecuta el workflow con el botón **"Test Workflow"**
2. Revisa la ejecución nodo por nodo:

| Nodo | Verificación | Resultado |
|------|-------------|-----------|
| List Files | ¿Devuelve los 3+ archivos? | __________________ |
| Download File | ¿Descarga el contenido correctamente? | __________________ |
| Pinecone Vector Store | ¿Inserta documentos sin error? | __________________ |

3. Verifica en la **consola de Pinecone** (https://app.pinecone.io):
   - Accede a tu índice
   - Comprueba que el número de vectores ha aumentado
   - Revisa las estadísticas del índice: ¿cuántos vectores se crearon?

4. Documenta los resultados:
   - Número de documentos procesados: __________
   - Número total de vectores creados: __________
   - Relación documentos/vectores (¿cuántos chunks se generaron por documento en promedio?): __________

### Preguntas de Reflexión

1. Si cambias el Chunk Size de 1000 a 500 caracteres manteniendo el Overlap en 200, ¿cómo cambiará el número de vectores? ¿Qué implicaciones tiene esto en coste de almacenamiento y calidad de búsqueda?
2. ¿Qué pasaría si ejecutas el workflow de ingesta dos veces sin borrar los vectores previos? ¿Cómo podrías evitar duplicados?
3. ¿Qué estrategia seguirías para mantener los vectores actualizados cuando los documentos originales cambian? Diseña brevemente un mecanismo de sincronización.

---

## Ejercicio 2: Pipeline RAG Completo con LangChain y Chroma

### Metadata
- **Duración estimada**: 40 minutos
- **Tipo**: Hands-on
- **Modalidad**: Individual
- **Dificultad**: Intermedia
- **Prerequisitos**: Python 3.8+ instalado, conocimientos básicos de Python, API key de OpenAI, comprensión del concepto de embeddings y bases vectoriales (Sesión 1)

### Contexto
Mientras que n8n permite construir sistemas RAG de forma visual, LangChain ofrece un control programático completo sobre cada componente del pipeline. Esto es especialmente útil cuando necesitamos personalizar la lógica de chunking, aplicar filtros avanzados en la búsqueda, o integrar RAG en aplicaciones Python existentes. En este ejercicio implementaremos un pipeline RAG completo usando LangChain con Chroma como base de datos vectorial local (sin necesidad de servicios externos más allá de OpenAI para embeddings y generación).

### Objetivo de Aprendizaje
- Implementar un pipeline RAG funcional en Python usando LangChain
- Cargar, dividir e indexar documentos en una base vectorial Chroma
- Configurar la cadena de recuperación y generación (RetrievalQA)
- Comparar respuestas con y sin contexto RAG

### Enunciado

### Paso 1: Preparar el entorno (5 min)

Instala las dependencias necesarias:

```bash
pip install langchain langchain-openai langchain-community chromadb tiktoken
```

Configura la API key de OpenAI:

```python
import os
os.environ["OPENAI_API_KEY"] = "tu-api-key-aqui"
```

### Paso 2: Crear documentos de ejemplo (5 min)

Para este ejercicio, crearemos documentos en memoria que simulan una base de conocimiento corporativa. Copia el siguiente código:

```python
from langchain.schema import Document

# Simulamos documentos de una empresa ficticia "TechCorp"
documentos = [
    Document(
        page_content="""
        Política de Vacaciones de TechCorp:
        Todos los empleados a tiempo completo tienen derecho a 23 días laborables
        de vacaciones al año. Los empleados con más de 5 años de antigüedad
        reciben 2 días adicionales por cada año extra, hasta un máximo de 30 días.
        Las vacaciones deben solicitarse con al menos 15 días de antelación a través
        del portal de RRHH. El período de julio y agosto tiene restricciones:
        solo se puede tomar un máximo de 15 días consecutivos. Las vacaciones
        no disfrutadas no se acumulan al año siguiente, salvo autorización expresa
        del director de departamento.
        """,
        metadata={"fuente": "manual_rrhh.pdf", "seccion": "vacaciones"}
    ),
    Document(
        page_content="""
        Política de Teletrabajo de TechCorp:
        Los empleados pueden teletrabajar hasta 3 días por semana, siendo obligatoria
        la presencia en oficina los martes y jueves. Para teletrabajar es necesario
        tener una conexión a internet estable de al menos 50 Mbps y un espacio
        de trabajo adecuado. El horario de teletrabajo es flexible entre las 7:00
        y las 20:00, pero se debe mantener disponibilidad en el horario core de
        10:00 a 14:00. El responsable directo debe aprobar el plan de teletrabajo
        cada trimestre. Los gastos de internet y electricidad derivados del
        teletrabajo se compensan con 50 euros mensuales.
        """,
        metadata={"fuente": "manual_rrhh.pdf", "seccion": "teletrabajo"}
    ),
    Document(
        page_content="""
        Proceso de Evaluación del Desempeño en TechCorp:
        La evaluación se realiza semestralmente en junio y diciembre. Cada empleado
        debe completar una autoevaluación y recibir feedback de al menos 3 compañeros
        (evaluación 360). La puntuación va de 1 a 5, donde 1 es 'No cumple expectativas'
        y 5 es 'Excepcional'. Los empleados con puntuación 4 o superior son elegibles
        para bonus (hasta el 15% del salario anual) y promoción. Los empleados con
        puntuación inferior a 2 durante dos semestres consecutivos entran en un plan
        de mejora de 90 días. Los resultados de la evaluación son confidenciales
        y solo los conocen el empleado, su responsable directo y RRHH.
        """,
        metadata={"fuente": "manual_rrhh.pdf", "seccion": "evaluacion"}
    ),
    Document(
        page_content="""
        Beneficios Sociales de TechCorp:
        Seguro médico privado para el empleado y familiares directos (cónyuge e hijos).
        Ticket restaurante de 11 euros diarios para días presenciales. Retribución
        flexible: guardería, transporte y formación. Presupuesto de formación anual
        de 1500 euros por empleado. Gimnasio corporativo gratuito en la sede central.
        Descuentos en productos de la empresa (hasta 40%). Plan de pensiones con
        aportación de la empresa del 3% del salario bruto. Seguro de vida de
        2x el salario anual bruto.
        """,
        metadata={"fuente": "manual_rrhh.pdf", "seccion": "beneficios"}
    ),
]

print(f"Documentos creados: {len(documentos)}")
for doc in documentos:
    print(f"  - {doc.metadata['seccion']}: {len(doc.page_content)} caracteres")
```

### Paso 3: Dividir, indexar y crear la base vectorial (10 min)

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# 1. Configurar el text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    separators=["\n\n", "\n", ". ", " ", ""]
)

# 2. Dividir los documentos en chunks
chunks = text_splitter.split_documents(documentos)
print(f"\nDocumentos originales: {len(documentos)}")
print(f"Chunks generados: {len(chunks)}")
print(f"\nEjemplo de chunk:")
print(f"  Contenido: {chunks[0].page_content[:150]}...")
print(f"  Metadata: {chunks[0].metadata}")

# 3. Crear embeddings y base vectorial Chroma
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="techcorp_rrhh",
    persist_directory="./chroma_db"  # Persiste en disco
)

print(f"\nBase vectorial creada con {vectorstore._collection.count()} vectores")
```

**Verifica** que la base se creó correctamente haciendo una búsqueda de prueba:

```python
# Búsqueda por similitud (sin LLM, solo recuperación)
resultados = vectorstore.similarity_search("¿cuántos días de vacaciones tengo?", k=3)
print("\n--- Resultados de búsqueda ---")
for i, doc in enumerate(resultados):
    print(f"\nResultado {i+1} (sección: {doc.metadata.get('seccion', 'N/A')}):")
    print(f"  {doc.page_content[:200]}...")
```

### Paso 4: Construir la cadena RAG completa (10 min)

```python
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# 1. Configurar el LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.0  # Respuestas deterministas para RAG
)

# 2. Definir el prompt template para RAG
template = """Eres un asistente de recursos humanos de TechCorp. Responde la pregunta
del empleado basándote EXCLUSIVAMENTE en el contexto proporcionado.

Si la información no está en el contexto, di claramente: "No tengo información sobre
ese tema en la documentación disponible. Te recomiendo contactar con RRHH directamente."

No inventes ni extrapoles información que no esté explícitamente en el contexto.

Contexto:
{context}

Pregunta del empleado: {question}

Respuesta:"""

prompt = PromptTemplate(
    template=template,
    input_variables=["context", "question"]
)

# 3. Crear la cadena RAG
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # Inserta todo el contexto en un solo prompt
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    chain_type_kwargs={"prompt": prompt},
    return_source_documents=True
)

# 4. Probar con preguntas
preguntas = [
    "¿Cuántos días de vacaciones me corresponden si llevo 7 años en la empresa?",
    "¿Puedo teletrabajar los viernes?",
    "¿Cuánto es el bonus máximo por buen desempeño?",
    "¿Cómo solicito un aumento de sueldo?",  # No está en los documentos
]

for pregunta in preguntas:
    print(f"\n{'='*60}")
    print(f"PREGUNTA: {pregunta}")
    resultado = qa_chain.invoke({"query": pregunta})
    print(f"RESPUESTA: {resultado['result']}")
    print(f"FUENTES: {[doc.metadata.get('seccion') for doc in resultado['source_documents']]}")
```

### Paso 5: Documentar resultados (10 min)

Completa la siguiente tabla con los resultados obtenidos:

| Pregunta | Respuesta del sistema | Fuentes utilizadas | ¿Respuesta correcta? |
|----------|----------------------|--------------------|-----------------------|
| ¿Cuántos días de vacaciones con 7 años? | __________________ | __________________ | _______ |
| ¿Puedo teletrabajar los viernes? | __________________ | __________________ | _______ |
| ¿Cuánto es el bonus máximo? | __________________ | __________________ | _______ |
| ¿Cómo solicito un aumento de sueldo? | __________________ | __________________ | _______ |

**Referencia de código adicional:** Para ver un ejemplo más completo de un bot FAQ con LangChain, consulta el repositorio del curso: [faqBot.py](https://github.com/rpmaya/ml2_code/blob/main/LangChain/faqBot.py)

### Preguntas de Reflexión

1. La cuarta pregunta ("¿Cómo solicito un aumento de sueldo?") no tiene respuesta en los documentos. ¿El sistema respondió correctamente indicando que no tiene esa información, o inventó una respuesta? ¿Qué ajustes harías en el prompt para mejorar este comportamiento?
2. Observa las fuentes utilizadas para cada respuesta. ¿El retriever recuperó siempre los chunks más relevantes? ¿Hubo algún caso donde incluyó chunks irrelevantes?
3. ¿Qué ventajas e inconvenientes tiene usar Chroma (local) frente a Pinecone (cloud) para la base vectorial? ¿En qué escenarios elegirías cada uno?

---

## Ejercicio 3: Agente RAG en n8n con Vector Store

### Metadata
- **Duración estimada**: 30 minutos
- **Tipo**: Hands-on
- **Modalidad**: Individual
- **Dificultad**: Intermedia
- **Prerequisitos**: Ejercicio 1 completado (documentos indexados en Pinecone), n8n con credenciales de OpenAI y Pinecone configuradas, comprensión del nodo AI Agent (Unidad 4)

### Contexto
Una vez que los documentos están indexados en la base vectorial, necesitamos un agente que pueda consultarla para responder preguntas de los usuarios. En n8n, esto se logra creando un AI Agent que tiene como herramienta un Vector Store Tool: cuando el agente recibe una pregunta, decide si necesita buscar en la base vectorial, formula una consulta de búsqueda, recupera los fragmentos relevantes y genera una respuesta fundamentada en ellos. Este es el patrón completo de RAG aplicado a un agente conversacional.

### Objetivo de Aprendizaje
- Crear un agente RAG funcional en n8n usando el nodo AI Agent con Vector Store Tool
- Configurar la memoria del agente para conversaciones multi-turno
- Probar el sistema con preguntas positivas (con respuesta en los documentos) y negativas (sin respuesta)
- Analizar los logs de ejecución para entender el flujo de recuperación y generación

### Enunciado

### Paso 1: Crear el workflow del agente RAG (10 min)

1. Crea un nuevo workflow en n8n: **"RAG - Agente de Consulta"**

2. Añade un nodo **"When chat message received"** (Chat Trigger)

3. Añade un nodo **"AI Agent"** y configura:

   **Chat Model:**
   - Añade un nodo **"OpenAI Chat Model"**
   - Model: `gpt-4o-mini`
   - Temperature: `0.0` (queremos respuestas fieles al contexto)

   **System Message:**
   ```
   # Rol
   Eres un asistente experto que responde preguntas basándose en la documentación
   interna de la empresa. Tu nombre es DocBot.

   # Tareas
   - Analiza la pregunta del usuario: {{ $json.chatInput }}
   - Busca información relevante en la base de documentos usando la herramienta
     de búsqueda vectorial
   - Genera una respuesta precisa basada ÚNICAMENTE en los documentos recuperados
   - Si la información no está disponible en los documentos, indícalo claramente

   # Restricciones
   - NUNCA inventes información que no esté en los documentos
   - Si no encuentras la respuesta, di: "No he encontrado información sobre este
     tema en la documentación disponible"
   - Cita la fuente o sección del documento cuando sea posible
   - Responde siempre en español

   # Formato
   - Respuestas claras y concisas (máximo 200 palabras)
   - Usa viñetas para listas
   - Incluye la referencia al documento fuente al final de la respuesta
   ```

4. Conecta: **Chat Trigger → AI Agent**

### Paso 2: Añadir la herramienta Vector Store (10 min)

1. En el nodo AI Agent, haz clic en **"+ Tool"**
2. Selecciona **"Vector Store Tool"**
3. Configura el Vector Store Tool:
   - **Name**: `buscar_documentacion` (nombre descriptivo para que el agente entienda cuándo usarla)
   - **Description**: `Busca información en la documentación interna de la empresa. Úsala cuando el usuario pregunte sobre políticas, procedimientos, normativas o cualquier información corporativa.`
   - **Top K**: `3` (recuperar los 3 fragmentos más relevantes)

4. Conecta el **Vector Store** al Tool:
   - Añade un nodo **"Pinecone Vector Store"**
   - Operation: **"Retrieve Documents (As Tool for AI Agent)"**
   - Selecciona tus credenciales de Pinecone
   - Selecciona el mismo índice donde indexaste los documentos en el Ejercicio 1

5. Conecta el **Embeddings OpenAI** al nodo de Pinecone:
   - Model: `text-embedding-ada-002` (debe ser el mismo modelo usado en la ingesta)

### Paso 3: Añadir memoria conversacional (3 min)

1. En el nodo AI Agent, haz clic en **"+ Memory"**
2. Selecciona **"Window Buffer Memory"**
3. Configura:
   - **Session ID Source**: `Connected Chat Trigger`
   - **Context Window Length**: `10`

### Paso 4: Probar el agente (7 min)

Abre la interfaz de chat y prueba con las siguientes preguntas. Documenta las respuestas:

**Preguntas positivas** (deberían encontrar respuesta en los documentos):

| Pregunta | Respuesta del agente | ¿Usó Vector Store? | ¿Respuesta correcta? |
|----------|---------------------|---------------------|-----------------------|
| "¿Cuáles son los horarios de trabajo?" | __________________ | _______ | _______ |
| "¿Qué documentos necesito para [tema de tus docs]?" | __________________ | _______ | _______ |
| "Explícame el procedimiento de [tema de tus docs]" | __________________ | _______ | _______ |

**Preguntas negativas** (NO deberían encontrar respuesta en los documentos):

| Pregunta | Respuesta del agente | ¿Indicó que no tiene info? |
|----------|---------------------|---------------------------|
| "¿Cuál es la capital de Francia?" | __________________ | _______ |
| "¿Quién ganó el mundial de fútbol en 2022?" | __________________ | _______ |

**Preguntas de seguimiento** (verifican la memoria):

| Secuencia | Respuesta | ¿Usó contexto previo? |
|-----------|-----------|----------------------|
| 1. "¿Cuáles son los beneficios para empleados?" | __________________ | N/A |
| 2. "¿Y para los que llevan más de 5 años?" | __________________ | _______ |
| 3. "Resúmeme todo lo que me has contado" | __________________ | _______ |

**Verificación en logs:** Después de cada ejecución, haz clic en el nodo AI Agent y revisa el panel de output para confirmar:
- ¿El agente decidió usar la herramienta `buscar_documentacion`?
- ¿Qué consulta envió al vector store?
- ¿Qué fragmentos recuperó?

### Preguntas de Reflexión

1. Para las preguntas negativas, ¿el agente respondió usando su conocimiento general o indicó que no tenía información? ¿Cómo podrías reforzar el system prompt para que SIEMPRE se limite a la documentación?
2. ¿En qué se diferencia la experiencia de usuario de este agente RAG frente a un chatbot genérico como ChatGPT? ¿Cuáles son las ventajas y limitaciones de cada enfoque?
3. Si un usuario envía una pregunta ambigua como "¿Cuánto me toca?", ¿cómo debería responder el agente? ¿Qué mejora añadirías al system prompt para manejar la ambigüedad?

---

## Ejercicio 4: Evaluación de Calidad de un Sistema RAG

### Metadata
- **Duración estimada**: 25 minutos
- **Tipo**: Análisis
- **Modalidad**: Individual
- **Dificultad**: Avanzada
- **Prerequisitos**: Al menos uno de los ejercicios anteriores completado (sistema RAG funcionando), comprensión de los conceptos de relevancia, fidelidad y completitud

### Contexto
Construir un sistema RAG es solo la mitad del trabajo; la otra mitad es evaluar su calidad. Un sistema RAG puede fallar de múltiples formas: puede recuperar fragmentos irrelevantes (fallo de recuperación), puede ignorar la información recuperada e inventar respuestas (alucinación), o puede dar respuestas parciales omitiendo datos importantes (falta de completitud). La evaluación sistemática permite identificar estos problemas y guiar las mejoras del sistema.

### Objetivo de Aprendizaje
- Diseñar un conjunto de preguntas de evaluación (test set) para un sistema RAG
- Aplicar las métricas de calidad: relevancia de contexto, fidelidad y completitud
- Identificar patrones de fallo y clasificarlos por tipo
- Proponer mejoras concretas basadas en los resultados de la evaluación

### Enunciado

### Paso 1: Diseñar el conjunto de evaluación (8 min)

Crea un test set de al menos 8 preguntas que cubran los siguientes tipos:

| Tipo de pregunta | Descripción | Ejemplo |
|-----------------|-------------|---------|
| **Factual directa** | La respuesta está explícitamente en un documento | "¿Cuántos días de vacaciones tiene un empleado?" |
| **Factual con razonamiento** | Requiere combinar información de un fragmento | "Si llevo 7 años, ¿cuántos días extra de vacaciones tengo?" |
| **Multi-documento** | Requiere información de varios documentos | "¿Qué beneficios económicos tiene un empleado sumando ticket, compensación de teletrabajo y plan de pensiones?" |
| **Sin respuesta** | La información no existe en los documentos | "¿Cuál es la política de mascotas en la oficina?" |
| **Ambigua** | La pregunta es imprecisa o tiene múltiples interpretaciones | "¿Qué puedo pedir?" |
| **Paráfrasis** | Misma pregunta que una factual pero formulada de forma diferente | "¿Cuántas jornadas de descanso anual me corresponden?" |

Completa la tabla con tus preguntas:

| # | Tipo | Pregunta | Respuesta esperada |
|---|------|----------|--------------------|
| 1 | Factual directa | __________________ | __________________ |
| 2 | Factual directa | __________________ | __________________ |
| 3 | Factual con razonamiento | __________________ | __________________ |
| 4 | Multi-documento | __________________ | __________________ |
| 5 | Sin respuesta | __________________ | __________________ |
| 6 | Sin respuesta | __________________ | __________________ |
| 7 | Ambigua | __________________ | __________________ |
| 8 | Paráfrasis | __________________ | __________________ |

### Paso 2: Ejecutar las preguntas y recoger resultados (7 min)

Ejecuta cada pregunta en tu sistema RAG (ya sea el de n8n del Ejercicio 3 o el de LangChain del Ejercicio 2) y documenta los resultados:

| # | Respuesta del sistema | Fragmentos recuperados (resumen) |
|---|----------------------|----------------------------------|
| 1 | __________________ | __________________ |
| 2 | __________________ | __________________ |
| 3 | __________________ | __________________ |
| 4 | __________________ | __________________ |
| 5 | __________________ | __________________ |
| 6 | __________________ | __________________ |
| 7 | __________________ | __________________ |
| 8 | __________________ | __________________ |

### Paso 3: Evaluar con métricas de calidad (5 min)

Para cada pregunta, evalúa las tres métricas principales en una escala de 1 a 5:

| # | Relevancia del contexto | Fidelidad | Completitud | Puntuación global |
|---|------------------------|-----------|-------------|-------------------|
| 1 | ___ /5 | ___ /5 | ___ /5 | ___ /5 |
| 2 | ___ /5 | ___ /5 | ___ /5 | ___ /5 |
| 3 | ___ /5 | ___ /5 | ___ /5 | ___ /5 |
| 4 | ___ /5 | ___ /5 | ___ /5 | ___ /5 |
| 5 | ___ /5 | ___ /5 | ___ /5 | ___ /5 |
| 6 | ___ /5 | ___ /5 | ___ /5 | ___ /5 |
| 7 | ___ /5 | ___ /5 | ___ /5 | ___ /5 |
| 8 | ___ /5 | ___ /5 | ___ /5 | ___ /5 |
| **Promedio** | **___ /5** | **___ /5** | **___ /5** | **___ /5** |

**Guía de puntuación:**

- **Relevancia del contexto** (¿Los fragmentos recuperados son pertinentes para la pregunta?):
  - 5: Todos los fragmentos son directamente relevantes
  - 3: Algunos fragmentos son relevantes, otros no
  - 1: Ningún fragmento es relevante

- **Fidelidad** (¿La respuesta se basa en los fragmentos recuperados, sin inventar?):
  - 5: Toda la información de la respuesta proviene de los fragmentos
  - 3: Mezcla información de fragmentos con información inventada
  - 1: La respuesta es completamente inventada (alucinación)

- **Completitud** (¿La respuesta incluye toda la información relevante disponible?):
  - 5: Incluye toda la información disponible en los documentos
  - 3: Incluye parte de la información, omite detalles importantes
  - 1: Respuesta muy incompleta o vacía

### Paso 4: Analizar patrones de fallo y proponer mejoras (5 min)

Clasifica los problemas encontrados:

| Tipo de fallo | Preguntas afectadas | Causa probable | Mejora propuesta |
|---------------|--------------------|-----------------|--------------------|
| Recuperación irrelevante | #___, #___ | Chunks muy grandes / embeddings inadecuados | __________________ |
| Alucinación | #___, #___ | Prompt insuficiente / temperatura alta | __________________ |
| Respuesta incompleta | #___, #___ | Top K bajo / chunks que cortan información | __________________ |
| Fallo en pregunta sin respuesta | #___, #___ | No hay instrucción clara de "no sé" | __________________ |

**Resumen de la evaluación:**
- Puntuación global del sistema: ___ /5
- Principal fortaleza: __________________
- Principal debilidad: __________________
- Mejora prioritaria: __________________

### Preguntas de Reflexión

1. ¿Qué tipo de pregunta fue más difícil para tu sistema RAG? ¿Por qué crees que es así?
2. Si tuvieras que automatizar esta evaluación (sin revisión humana), ¿cómo lo harías? Investiga brevemente el concepto de "LLM-as-judge" donde un segundo modelo evalúa las respuestas del primero.
3. ¿Qué relación existe entre el parámetro Top K (número de fragmentos recuperados) y las métricas de relevancia y completitud? ¿Hay un trade-off? ¿Cuál sería el valor óptimo para tu caso?

---

## Ejercicio 5: Diseño de Arquitectura RAG para un Caso Práctico

### Metadata
- **Duración estimada**: 25 minutos
- **Tipo**: Diseño
- **Modalidad**: Grupal (2-3 personas)
- **Dificultad**: Intermedia
- **Prerequisitos**: Comprensión completa del pipeline RAG (ingesta, chunking, embeddings, búsqueda, generación), conocimiento de los casos prácticos vistos en la sesión teórica

### Contexto
El verdadero desafío de RAG no es técnico sino de diseño: elegir la arquitectura correcta para cada caso de uso. Las decisiones sobre qué documentos incluir, cómo dividirlos, qué modelo de embeddings usar, qué base vectorial elegir y cómo configurar los prompts del agente determinan la calidad final del sistema. En este ejercicio, cada grupo diseñará la arquitectura completa de un sistema RAG para un caso de uso real, justificando cada decisión técnica.

### Objetivo de Aprendizaje
- Diseñar una arquitectura RAG completa para un caso de uso específico
- Justificar las decisiones técnicas (chunking, embeddings, base vectorial, prompts)
- Identificar los retos y riesgos específicos de cada caso de uso
- Presentar y defender el diseño ante los compañeros

### Enunciado

### Paso 1: Elegir el caso práctico (3 min)

Cada grupo elige uno de los siguientes casos (no se pueden repetir):

| Caso | Descripción | Reto principal |
|------|-------------|----------------|
| **A. E-commerce** | Asistente de compras para una tienda online con 10.000 productos. Debe responder sobre características, precios, disponibilidad y comparativas. | Volumen de datos y actualización frecuente de precios/stock |
| **B. Documentación técnica** | Asistente para desarrolladores que consulta la documentación de una API con 500 endpoints, tutoriales y guías de troubleshooting. | Código en los documentos, relaciones entre endpoints, versionado |
| **C. Soporte con escalado** | Sistema de soporte nivel 1 que responde preguntas frecuentes y escala a humanos cuando no puede resolver. Maneja 200 artículos de FAQ y 50 procedimientos. | Saber cuándo escalar, evitar respuestas incorrectas en temas críticos |
| **D. Legal/Compliance** | Asistente que consulta contratos, regulaciones y políticas internas (100 documentos legales). Los abogados lo usan para encontrar cláusulas específicas. | Precisión extrema requerida, no puede inventar ni parafrasear mal |

### Paso 2: Diseñar la arquitectura (15 min)

Completa el siguiente documento de diseño:

**Caso elegido:** _______________

**1. Fuentes de datos**

| Fuente | Formato | Volumen estimado | Frecuencia de actualización |
|--------|---------|-----------------|----------------------------|
| __________________ | __________________ | __________________ | __________________ |
| __________________ | __________________ | __________________ | __________________ |
| __________________ | __________________ | __________________ | __________________ |

**2. Estrategia de chunking**

- Tamaño de chunk: ___ caracteres
- Solapamiento: ___ caracteres
- Justificación del tamaño elegido: __________________
- ¿Necesita chunking especial? (ej: por secciones, por producto, por endpoint): __________________
- Metadata a incluir en cada chunk: __________________

**3. Modelo de embeddings**

- Modelo elegido: __________________
- Dimensiones: ___
- Justificación: __________________
- Coste estimado para el volumen de datos: __________________

**4. Base de datos vectorial**

- Servicio elegido: __________________
- Justificación (¿por qué esta y no otra?): __________________
- Configuración del índice:
  - Tipo de índice: __________________
  - Métrica de similitud: __________________
  - ¿Necesita filtros por metadata?: __________________

**5. Pipeline de ingesta**

Describe el flujo de ingesta paso a paso:

```
Paso 1: _______________________________________________
Paso 2: _______________________________________________
Paso 3: _______________________________________________
Paso 4: _______________________________________________
Paso 5: _______________________________________________
```

¿Cómo se gestionan las actualizaciones? (¿re-indexado completo o incremental?): __________________

**6. Configuración del agente**

- System prompt (escribe un borrador completo):

```
# Rol
[...]

# Tareas
[...]

# Restricciones
[...]

# Formato
[...]
```

- Top K para la búsqueda: ___
- Temperatura del LLM: ___
- ¿Necesita herramientas adicionales además del vector store? __________________
- ¿Necesita memoria conversacional? ¿De qué tipo?: __________________

**7. Gestión de riesgos**

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|------------|
| Alucinación del modelo | __________________ | __________________ | __________________ |
| Documentos desactualizados | __________________ | __________________ | __________________ |
| Pregunta fuera de alcance | __________________ | __________________ | __________________ |
| __________________ | __________________ | __________________ | __________________ |

### Paso 3: Presentación y defensa (7 min)

Cada grupo presenta su diseño al resto de la clase (3-4 minutos) y responde preguntas (2-3 minutos).

**Guía para la presentación:**
1. Explica brevemente el caso elegido y su reto principal
2. Justifica las 2-3 decisiones de diseño más importantes
3. Menciona el principal riesgo identificado y su mitigación
4. Muestra el system prompt diseñado

**Guía para las preguntas:**
- ¿Por qué elegiste ese tamaño de chunk y no otro?
- ¿Cómo manejas las actualizaciones de datos?
- ¿Qué pasa si el usuario pregunta algo que no está en los documentos?
- ¿Cómo evaluarías la calidad del sistema una vez en producción?

### Preguntas de Reflexión

1. ¿Qué caso de los cuatro consideras más difícil de implementar con RAG? ¿Por qué?
2. ¿Hay algún caso donde RAG NO sería la mejor solución y sería preferible un fine-tuning del modelo o una base de datos tradicional? Justifica tu respuesta.
3. Si tuvieras que poner tu diseño en producción mañana, ¿cuál sería el primer paso que darías y cuál sería la mayor incertidumbre?

---

## Resumen de Tiempos

| Ejercicio | Duración | Tipo | Ubicación sugerida en la sesión |
|-----------|----------|------|--------------------------------|
| 1. Workflow de Ingesta en n8n | 35 min | Hands-on | Después del bloque de Pinecone + n8n |
| 2. RAG con LangChain y Chroma | 40 min | Hands-on | Después del bloque de LangChain |
| 3. Agente RAG en n8n | 30 min | Hands-on | Después del bloque de agentes RAG |
| 4. Evaluación de Calidad RAG | 25 min | Análisis | Después del bloque de optimización |
| 5. Diseño de Caso Práctico | 25 min | Diseño grupal | Bloque final de la sesión |
| **Total** | **155 min** | | |

**Nota:** Los ejercicios 1-3 son secuenciales (cada uno construye sobre el anterior en el contexto de n8n). El ejercicio 2 es independiente y puede realizarse en paralelo. Los ejercicios 4 y 5 pueden usar cualquiera de los sistemas construidos previamente.
