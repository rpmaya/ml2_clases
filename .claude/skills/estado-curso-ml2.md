# Skill: Estado del Curso ML2

## Descripcion
Muestra el estado actual del curso, listando sesiones y practicas completadas y pendientes.

## Uso
```
Muestra el estado del curso
```
o
```
Que sesiones faltan por crear?
```

## Estructura por Unidad
Cada unidad tiene:
- 2 sesiones de 4 horas cada una
- 1 practica evaluable (cubre ambas sesiones)

```
unidadX_sesion1/   → Sesion 1
unidadX_sesion2/   → Sesion 2
unidadX_practica/  → Practica evaluable
```

## Indice Completo del Curso

### Unidad 1: Fundamentos de IA Generativa y LLMs
| Elemento | Tema | Estado | Archivo |
|----------|------|--------|---------|
| Sesion 1 | Fundamentos de IA Generativa | Completada | `unidad1_sesion1/sesion1_fundamentos_ia_generativa.md` |
| Sesion 2 | LLMs en Profundidad | Completada | `unidad1_sesion2/sesion2_llms_en_profundidad.md` |
| Practica | Analisis Comparativo de Tecnicas | Completada | `unidad1_practica/practica.md` |

### Unidad 2: Prompt Engineering y ChatGPT
| Elemento | Tema | Estado | Archivo |
|----------|------|--------|---------|
| Sesion 1 | Prompt Engineering | Pendiente | `unidad2_sesion1/sesion1_prompt_engineering.md` |
| Sesion 2 | Uso Avanzado de ChatGPT | Pendiente | `unidad2_sesion2/sesion2_chatgpt_avanzado.md` |
| Practica | Diseno y Evaluacion de Prompts | Pendiente | `unidad2_practica/practica.md` |

### Unidad 3: Arquitectura y APIs
| Elemento | Tema | Estado | Archivo |
|----------|------|--------|---------|
| Sesion 1 | Arquitectura Transformers | Pendiente | `unidad3_sesion1/sesion1_arquitectura_transformers.md` |
| Sesion 2 | Acceso Programatico a LLMs | Pendiente | `unidad3_sesion2/sesion2_acceso_programatico_llms.md` |
| Practica | Implementacion con APIs | Pendiente | `unidad3_practica/practica.md` |

### Unidad 4: Automatizacion y Agentes
| Elemento | Tema | Estado | Archivo |
|----------|------|--------|---------|
| Sesion 1 | Automatizacion con n8n | Pendiente | `unidad4_sesion1/sesion1_automatizacion_n8n.md` |
| Sesion 2 | Agentes de IA | Pendiente | `unidad4_sesion2/sesion2_agentes_ia.md` |
| Practica | Workflow con Agentes | Pendiente | `unidad4_practica/practica.md` |

### Unidad 5: RAG y Bases de Datos
| Elemento | Tema | Estado | Archivo |
|----------|------|--------|---------|
| Sesion 1 | RAG (Retrieval Augmented Generation) | Pendiente | `unidad5_sesion1/sesion1_rag.md` |
| Sesion 2 | Bases de Datos Vectoriales | Pendiente | `unidad5_sesion2/sesion2_bases_datos_vectoriales.md` |
| Practica | Sistema RAG Completo | Pendiente | `unidad5_practica/practica.md` |

### Unidad 6: Integracion Avanzada
| Elemento | Tema | Estado | Archivo |
|----------|------|--------|---------|
| Sesion 1 | Model Context Protocol (MCP) | Pendiente | `unidad6_sesion1/sesion1_mcp.md` |
| Practica | Integracion MCP | Pendiente | `unidad6_practica/practica.md` |

## Como Verificar el Estado

Para actualizar este documento, ejecuta:
```bash
ls -la unidad*/
```

Y compara con la lista de sesiones esperadas.

## Contenido Sugerido por Sesion

### Unidad 2, Sesion 1: Prompt Engineering
- Principios basicos de prompting
- Tecnicas: zero-shot, few-shot, chain-of-thought
- Estructuras de prompts efectivos
- Errores comunes y como evitarlos

### Unidad 2, Sesion 2: ChatGPT Avanzado
- Custom Instructions
- GPTs personalizados
- Plugins y herramientas
- Casos de uso empresariales

### Unidad 3, Sesion 1: Arquitectura Transformers
- Atencion y self-attention
- Arquitectura encoder-decoder
- Positional encoding
- Multi-head attention

### Unidad 3, Sesion 2: Acceso Programatico
- APIs de OpenAI, Anthropic, Google
- SDKs y librerias
- Manejo de errores y rate limits
- Streaming y funciones

### Unidad 4, Sesion 1: n8n
- Introduccion a n8n
- Nodos de IA
- Workflows con LLMs
- Automatizaciones practicas

### Unidad 4, Sesion 2: Agentes
- Que son los agentes de IA
- Herramientas y funciones
- ReAct, planificacion
- Frameworks: LangChain, AutoGPT

### Unidad 5, Sesion 1: RAG
- Arquitectura RAG
- Chunking y embedding
- Retrieval strategies
- Evaluacion de RAG

### Unidad 5, Sesion 2: Bases de Datos Vectoriales
- Vectores y similitud
- Pinecone, Weaviate, Chroma
- Indices y busqueda
- Integracion con LLMs

### Unidad 6: MCP
- Model Context Protocol
- Servidores MCP
- Integracion con herramientas
- Casos de uso
