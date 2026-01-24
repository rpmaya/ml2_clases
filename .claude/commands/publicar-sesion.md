# Publicar Sesion en GitHub

Sube los cambios de una sesion preparada al repositorio de GitHub.

## Argumentos

- `$ARGUMENTS` - (Opcional) Formato: `unidad sesion` (ejemplo: `1 2`)
  - Si no se proporciona, publica todos los cambios pendientes

## Instrucciones

1. **Verificar repositorio**:
   ```bash
   cd /tmp/ml2_clases
   git status
   ```

2. **Si hay argumentos**, verificar que existe la sesion:
   ```
   /tmp/ml2_clases/unidad[N]_sesion[M]/
   ```

3. **Mostrar cambios pendientes**:
   - Archivos nuevos
   - Archivos modificados
   - Pedir confirmacion al usuario

4. **Crear commit** con mensaje descriptivo:
   ```
   Add/Update Unidad [N] Sesion [M]: [Titulo]

   Documento integrado teoria + practica para alumnos:
   - [Lista de bloques incluidos]
   - [Numero de practicas]
   - Quiz de evaluacion

   Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
   ```

5. **Push a GitHub**:
   ```bash
   git push origin main
   ```

6. **Mostrar resultado**:
   - URL del repositorio: https://github.com/rpmaya/ml2_clases
   - Archivos subidos
   - Confirmar exito

## Ejemplo de uso

```
/publicar-sesion 1 2
```

Publica solo la sesion 2 de la unidad 1.

```
/publicar-sesion
```

Publica todos los cambios pendientes.
