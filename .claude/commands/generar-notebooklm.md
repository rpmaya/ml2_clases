# Generar Documento para NotebookLM

Genera un documento markdown consolidado optimizado para subir a NotebookLM y crear presentaciones.

## Argumentos

- `$ARGUMENTS` - Formato: `unidad sesion` (ejemplo: `1 2` para Unidad 1 Sesion 2)

## Instrucciones

1. **Parsear argumentos**: Extrae el numero de unidad y sesion de `$ARGUMENTS`

2. **Leer materiales fuente** del repositorio ml2_online:
   ```
   /Users/rpalacios/Documents/GitHub/ml2_online/clases/unidad_[N]/sesion_[M]/
   ```
   Lee todos los archivos .md

3. **Generar documento consolidado** que:
   - Combine toda la teoria de forma estructurada
   - Incluya tablas comparativas
   - Tenga secciones claras y jerarquizadas
   - Sea optimo para que NotebookLM extraiga conceptos clave
   - NO incluya ejercicios detallados (solo menciones)

4. **Estructura optimizada para NotebookLM**:
   ```
   # Titulo Principal
   ## Informacion General

   # BLOQUE 1: [Tema]
   ## Subtema 1.1
   ### Conceptos clave
   ### Tablas comparativas

   # BLOQUE 2: [Tema]
   ...

   # Resumen de Conceptos Clave
   # Recursos Adicionales
   ```

5. **Guardar el documento** en:
   ```
   /tmp/sesion[N]_[titulo]_notebooklm.md
   ```

6. **Abrir el archivo y el directorio** para que el usuario pueda subirlo facilmente

## Ejemplo de uso

```
/generar-notebooklm 2 1
```

Genera documento para NotebookLM de la Unidad 2, Sesion 1
