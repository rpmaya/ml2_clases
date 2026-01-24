# Listar Sesiones Disponibles

Muestra todas las sesiones disponibles del curso ML2 y su estado de preparacion.

## Instrucciones

1. **Escanear repositorio fuente** (ml2_online):
   ```
   /Users/rpalacios/Documents/GitHub/ml2_online/clases/
   ```
   Lista todas las carpetas unidad_*/sesion_*

2. **Escanear repositorio destino** (ml2_clases):
   ```
   /tmp/ml2_clases/
   ```
   Lista todas las carpetas unidad*_sesion*

3. **Mostrar tabla** con:
   - Unidad y Sesion
   - Titulo (extraido de teoria.md)
   - Estado: Pendiente / Preparada
   - Archivos fuente disponibles

4. **Formato de salida**:

   ```
   ## Sesiones del Curso ML2

   | Unidad | Sesion | Titulo | Estado | Archivos |
   |--------|--------|--------|--------|----------|
   | 1 | 1 | Fundamentos IA Generativa | ✅ Preparada | 4/4 |
   | 1 | 2 | LLMs en Profundidad | ⏳ Pendiente | 4/4 |
   | 2 | 1 | [Titulo] | ⏳ Pendiente | 4/4 |
   | 2 | 2 | [Titulo] | ⏳ Pendiente | 4/4 |

   Para preparar una sesion: /preparar-sesion [unidad] [sesion]
   ```

## Ejemplo de uso

```
/listar-sesiones
```
