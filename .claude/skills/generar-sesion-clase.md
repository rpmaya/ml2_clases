# Skill: Generar Sesion de Clase ML2

## Descripcion
Genera material didactico completo para una sesion del curso de Aprendizaje Automatico II (IA Generativa y LLMs). Cada sesion es de **4 horas** y sigue un formato estandarizado con teoria, practicas interactivas y evaluacion.

## Uso
Cuando el usuario pida generar una sesion:
```
Genera la sesion [X] de la unidad [Y] sobre [TEMA]
```

## Estructura del Repositorio
```
ml2_clases/
├── unidad1_sesion1/
│   └── sesion1_fundamentos_ia_generativa.md
├── unidad1_sesion2/
│   └── sesion2_llms_en_profundidad.md
├── unidadX_sesionY/
│   └── sesionY_[titulo_snake_case].md
```

## Indice del Curso (Referencia)
1. Fundamentos de IA Generativa (Unidad 1, Sesion 1)
2. LLMs en Profundidad (Unidad 1, Sesion 2)
3. Prompt Engineering (Unidad 2, Sesion 1)
4. Uso Avanzado de ChatGPT (Unidad 2, Sesion 2)
5. Arquitectura Transformers (Unidad 3, Sesion 1)
6. Acceso programatico a los LLMs (Unidad 3, Sesion 2)
7. Automatizacion con n8n (Unidad 4, Sesion 1)
8. Agentes de IA (Unidad 4, Sesion 2)
9. RAG (Unidad 5, Sesion 1)
10. Bases de Datos Vectoriales (Unidad 5, Sesion 2)
11. Model Context Protocol - MCP (Unidad 6)

## Formato del Archivo Markdown

### Estructura General
```markdown
# Unidad X - Sesion Y: [Titulo de la Sesion]
## Aprendizaje Automatico II

---

## Objetivos de Aprendizaje
Al finalizar esta sesion, seras capaz de:
- [ ] Objetivo 1
- [ ] Objetivo 2
- [ ] Objetivo 3
- [ ] Objetivo 4
- [ ] Objetivo 5

---

## Preparacion Previa
Antes de comenzar, asegurate de tener acceso a:

| Herramienta | URL | Requiere Cuenta |
|-------------|-----|-----------------|
| Herramienta 1 | https://... | Si/No |
| Herramienta 2 | https://... | Si/No |

---

# BLOQUE 1: [Titulo del Bloque]
[Contenido teorico con subsecciones, tablas, diagramas ASCII]

---

## PRACTICA X.Y: [Titulo]
### [Individual/Parejas/Grupal]

### Objetivo
[Descripcion del objetivo]

### Instrucciones
[Pasos detallados]

### Tabla para completar
| ... | ... |
|-----|-----|

### Reflexion
[Preguntas de reflexion]

---

[Repetir BLOQUES y PRACTICAS]

---

# EVALUACION: Quiz de Conceptos
## Individual

### Pregunta 1
[Enunciado]
- [ ] a) Opcion
- [ ] b) Opcion
- [ ] c) Opcion
- [ ] d) Opcion

[5 preguntas minimo]

<details>
<summary><strong>Ver Respuestas</strong></summary>
[Respuestas con explicacion]
</details>

---

# Resumen de la Sesion

## Las 5 Ideas Fundamentales
| Concepto | Resumen en una linea |
|----------|----------------------|
| ... | ... |

## Para Recordar
[Lista de puntos clave]

---

# Conexion con Sesion Anterior/Siguiente
[Como se relaciona con el resto del curso]

---

# Proxima Sesion
## [Titulo]
[Lista de temas]

---

# Recursos Adicionales

## Papers Fundamentales
- Autor et al. (Ano) - "Titulo"

## Herramientas para Explorar
- [Nombre](URL) - Descripcion

## Videos Recomendados
- Canal - "Titulo del video"

---

# Ejercicio para Casa (Opcional)
[Descripcion de tarea opcional]

---

*Documento generado para el curso de Aprendizaje Automatico II*
```

## Reglas de Contenido

### Bloques (6 por sesion tipicamente)
- Cada bloque = 30-60 minutos
- Incluir: conceptos, tablas comparativas, diagramas ASCII, ejemplos
- Alternar teoria con practicas

### Practicas
- Minimo 3 practicas por sesion
- Tipos: Individual, Parejas, Grupal
- Incluir siempre: Objetivo, Instrucciones, Tabla/Espacio para respuestas, Reflexion
- Usar herramientas online gratuitas cuando sea posible

### Diagramas ASCII
```
Preferir diagramas ASCII para arquitecturas y flujos:

┌─────────┐      ┌─────────┐
│ Input   │─────>│ Output  │
└─────────┘      └─────────┘
```

### Quiz
- 5 preguntas minimo
- Formato multiple choice
- Incluir respuestas ocultas con <details>

### Estilo
- Sin acentos ni caracteres especiales (para compatibilidad)
- Usar "tu/seras" (informal)
- Explicaciones claras y concisas
- Ejemplos practicos del mundo real
- Referencias a papers cuando sea relevante

## Ejemplo de Uso

Usuario: "Genera la sesion 1 de la unidad 2 sobre Prompt Engineering"

Claude:
1. Crea directorio: `unidad2_sesion1/`
2. Genera archivo: `sesion1_prompt_engineering.md`
3. Sigue la estructura completa del formato
4. Incluye practicas con herramientas como ChatGPT, Claude, etc.
5. Conecta con sesiones anteriores (LLMs) y siguientes (ChatGPT avanzado)
