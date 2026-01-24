# Skill: Generar Practica Evaluable de Unidad

## Descripcion
Genera la actividad practica evaluable para cada unidad del curso de Aprendizaje Automatico II. Las practicas son tareas individuales que evaluan el aprendizaje de ambas sesiones de la unidad.

## Uso
```
Genera la practica de la unidad [X]
```

## Estructura del Repositorio
```
ml2_clases/
├── unidad1_sesion1/
├── unidad1_sesion2/
├── unidad1_practica/
│   └── practica.md          ← Actividad evaluable
├── unidad2_sesion1/
├── unidad2_sesion2/
├── unidad2_practica/
│   └── practica.md
└── ...
```

## Formato Estandar de Practica

```markdown
# Practica Evaluable - Unidad X
## [Titulo que engloba ambas sesiones]

---

## Informacion General

| Campo | Valor |
|-------|-------|
| **Nombre** | [Nombre descriptivo] |
| **Tipo** | Individual |
| **Duracion estimada** | 90-120 minutos |
| **Entregable** | Documento PDF (maximo 5 paginas) |
| **Peso en la nota** | XX% |

---

## Objetivos de Aprendizaje

Al completar esta practica, el estudiante sera capaz de:
- Objetivo 1 (relacionado con sesion 1)
- Objetivo 2 (relacionado con sesion 1)
- Objetivo 3 (relacionado con sesion 2)
- Objetivo 4 (relacionado con sesion 2)
- Objetivo 5 (integrador)

---

## Parte 1: [Tema de Sesion 1] (XX min)

### Ejercicio 1.1: [Nombre]
[Descripcion con tabla o formato para respuesta]

### Ejercicio 1.2: [Nombre]
[Descripcion]

---

## Parte 2: [Tema de Sesion 1 o transicion] (XX min)

### Ejercicio 2.1: [Nombre]
[Descripcion]

### Ejercicio 2.2: [Nombre]
[Descripcion]

---

## Parte 3: [Tema de Sesion 2] (XX min)

### Ejercicio 3.1: [Nombre]
[Descripcion]

### Ejercicio 3.2: [Nombre]
[Descripcion]

---

## Parte 4: Reflexion Critica (XX min)

### Ejercicio 4.1: [Analisis integrador]
[Pregunta que conecte ambas sesiones]

### Ejercicio 4.2: [Caso etico o practico]
[Escenario con preguntas]

---

## Recomendaciones para la Entrega
- Punto 1
- Punto 2
- Punto 3

---

## Rubrica de Evaluacion

| Criterio | Peso | Excelente (100%) | Satisfactorio (70%) | Insuficiente (40%) |
|----------|------|------------------|---------------------|-------------------|
| Criterio 1 | XX% | Descripcion | Descripcion | Descripcion |
| Criterio 2 | XX% | Descripcion | Descripcion | Descripcion |
| Criterio 3 | XX% | Descripcion | Descripcion | Descripcion |
| Criterio 4 | XX% | Descripcion | Descripcion | Descripcion |
| Presentacion | 10% | Descripcion | Descripcion | Descripcion |

---

## Formato de Entrega

### Especificaciones
- **Formato**: PDF
- **Extension maxima**: 5 paginas
- **Nombre del archivo**: `Apellido_Nombre_UX_Practica.pdf`

### Contenido Requerido
1. Portada
2. Respuestas organizadas por partes
3. Capturas de pantalla si aplica
4. Referencias si aplica

### Proceso de Entrega
1. Completar ejercicios
2. Revisar formato
3. Exportar a PDF
4. Subir al campus virtual

---

## Recursos Permitidos
[Lista de recursos]

---

*Practica correspondiente a la Unidad X del curso de Aprendizaje Automatico II*
```

## Tipos de Ejercicios Recomendados

| Tipo | Descripcion | Ejemplo |
|------|-------------|---------|
| **Seleccion/Clasificacion** | Elegir tecnica apropiada para casos | Tabla de casos de uso |
| **Ordenar procesos** | Secuenciar etapas de un pipeline | Ordenar ciclo de vida LLM |
| **Comparativa** | Completar tablas comparativas | Trade-offs entre tecnicas |
| **Analisis de escenario** | Responder preguntas sobre un caso | Analisis de alineamiento |
| **Uso de herramientas** | Experimentar y documentar | Tokenizador, APIs |
| **Reflexion critica** | Analisis etico o de limitaciones | Caso de uso medico |

## Contenido por Unidad

### Unidad 1: IA Generativa + LLMs
- Parte 1: Seleccion de tecnicas (GANs, VAEs, Difusion, LLMs)
- Parte 2: Ciclo de vida de LLMs (pre-training, RLHF)
- Parte 3: Tokenizacion y parametros
- Parte 4: Limitaciones y etica

### Unidad 2: Prompt Engineering + ChatGPT
- Parte 1: Diseno de prompts efectivos
- Parte 2: Tecnicas avanzadas (few-shot, CoT)
- Parte 3: Custom GPTs y casos de uso
- Parte 4: Evaluacion y mejora de prompts

### Unidad 3: Transformers + APIs
- Parte 1: Arquitectura y atencion
- Parte 2: Comparativa de APIs
- Parte 3: Implementacion practica
- Parte 4: Manejo de errores y optimizacion

### Unidad 4: n8n + Agentes
- Parte 1: Automatizacion con n8n
- Parte 2: Diseno de workflows
- Parte 3: Agentes y herramientas
- Parte 4: Caso integrador

### Unidad 5: RAG + Vectores
- Parte 1: Arquitectura RAG
- Parte 2: Chunking y embeddings
- Parte 3: Bases de datos vectoriales
- Parte 4: Evaluacion de sistemas RAG

### Unidad 6: MCP
- Parte 1: Protocolo MCP
- Parte 2: Servidores y clientes
- Parte 3: Integracion
- Parte 4: Caso practico

## Consideraciones

1. **Tiempo realista**: 90-120 minutos
2. **Extension limitada**: 5 paginas max (fomentar concision)
3. **Herramientas gratuitas**: Usar alternativas accesibles
4. **Balance**: 50% sesion 1, 50% sesion 2
5. **Reflexion critica**: Siempre incluir componente etico
6. **Rubrica clara**: Criterios objetivos y medibles
