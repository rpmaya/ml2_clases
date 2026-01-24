# Preparar Clase Completa

Flujo completo para preparar una clase: genera documento para alumnos, documento para NotebookLM, y opcionalmente publica en GitHub.

## Argumentos

- `$ARGUMENTS` - Formato: `unidad sesion` (ejemplo: `1 2` para Unidad 1 Sesion 2)

## Instrucciones

1. **Parsear argumentos**: Extrae el numero de unidad y sesion de `$ARGUMENTS`
   - Si no se proporcionan, mostrar sesiones disponibles con `/listar-sesiones`

2. **Leer materiales fuente** del repositorio ml2_online:
   ```
   /Users/rpalacios/Documents/GitHub/ml2_online/clases/unidad_[N]/sesion_[M]/
   ```

3. **PASO 1 - Documento para alumnos**:
   - Genera markdown integrado teoria + practica
   - Guarda en `/tmp/ml2_clases/unidad[N]_sesion[M]/`
   - Muestra resumen de bloques y practicas

4. **PASO 2 - Documento para NotebookLM**:
   - Genera markdown consolidado para presentacion
   - Guarda en `/tmp/`
   - Abre el archivo y directorio

5. **PASO 3 - Preguntar al usuario**:
   ```
   Documentos generados:
   1. Para alumnos: /tmp/ml2_clases/unidad[N]_sesion[M]/...
   2. Para NotebookLM: /tmp/sesion[M]_...

   ¿Deseas publicar en GitHub? (si/no)
   ```

6. **Si el usuario confirma**, ejecutar publicacion:
   - git add, commit, push
   - Mostrar URL del repositorio

## Resumen de archivos generados

| Archivo | Ubicacion | Proposito |
|---------|-----------|-----------|
| sesion_teoria_practica.md | /tmp/ml2_clases/... | Compartir con alumnos |
| sesion_notebooklm.md | /tmp/ | Subir a NotebookLM |

## Ejemplo de uso

```
/preparar-clase 2 1
```

Prepara todos los materiales para la Unidad 2, Sesion 1
