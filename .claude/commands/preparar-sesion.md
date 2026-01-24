# Preparar Sesion para Alumnos

Genera un documento markdown integrado (teoria + practica) para una sesion del curso ML2.

## Argumentos

- `$ARGUMENTS` - Formato: `unidad sesion` (ejemplo: `1 2` para Unidad 1 Sesion 2)

## Instrucciones

1. **Parsear argumentos**: Extrae el numero de unidad y sesion de `$ARGUMENTS`
   - Si no se proporcionan, pregunta al usuario

2. **Leer materiales fuente** del repositorio ml2_online:
   ```
   /Users/rpalacios/Documents/GitHub/ml2_online/clases/unidad_[N]/sesion_[M]/
   ```
   Lee todos los archivos .md:
   - teoria.md
   - ejercicios.md
   - slides_guion.md
   - recursos.md

3. **Generar documento integrado** que:
   - Intercale teoria con ejercicios practicos relacionados
   - Cada bloque teorico debe tener una practica asociada cuando sea posible
   - Incluya objetivos de aprendizaje con checkboxes
   - Tenga preparacion previa con links a herramientas
   - Incluya un quiz de evaluacion al final
   - Tenga resumen y recursos adicionales
   - Use formato consistente con sesiones anteriores

4. **Estructura del documento**:
   ```
   # Titulo de la Sesion
   ## Informacion de la Sesion
   ## Objetivos de Aprendizaje
   ## Preparacion Previa

   # BLOQUE 1: [Tema]
   ## Teoria
   ## PRACTICA 1.1: [Ejercicio relacionado]

   # BLOQUE 2: [Tema]
   ...

   # EVALUACION: Quiz
   # Resumen
   # Proxima Sesion
   # Recursos Adicionales
   ```

5. **Guardar el documento** en:
   ```
   /tmp/ml2_clases/unidad[N]_sesion[M]/sesion[M]_[titulo].md
   ```

6. **Mostrar resumen** de lo generado:
   - Ruta del archivo
   - Numero de bloques
   - Numero de practicas integradas
   - Preguntar si quiere publicarlo en GitHub

## Ejemplo de uso

```
/preparar-sesion 1 2
```

Genera el documento para Unidad 1, Sesion 2 (LLMs en Profundidad)
