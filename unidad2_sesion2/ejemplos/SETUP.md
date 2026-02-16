# Setup - Ejemplos Unidad 2, Sesión 2

## 1. Activar el entorno virtual

```bash
source ~/Documents/GitHub/ml2_code/llm_env/bin/activate
```

> Si no tienes el entorno creado, créalo primero:
> ```bash
> python3 -m venv ~/Documents/GitHub/ml2_code/llm_env
> source ~/Documents/GitHub/ml2_code/llm_env/bin/activate
> pip install openai python-dotenv
> ```

## 2. Configurar API Key

Copia la plantilla y edita con tu clave:

```bash
cp .env.example .env
```

Abre `.env` y reemplaza con tu API key de OpenAI:

```
OPENAI_API_KEY=sk-...tu-api-key-aqui
```

> Puedes obtener tu API key en https://platform.openai.com/api-keys

## 3. Ejecutar ejemplos

```bash
python ejemplo_3_2_anatomia_llamada_api.py   # Llamada básica a la API
python ejemplo_3_3_parametros_clave.py        # Efecto de temperature y top_p
python ejemplo_3_4_manteniendo_contexto.py    # Conversación multi-turno
python ejemplo_3_5_gestion_context_window.py  # Truncar y resumir historial
python ejemplo_3_6_streaming.py               # Respuesta token a token
python ejemplo_3_7_manejo_errores.py          # Reintentos y errores
```

## Notas

- El archivo `.env` está en `.gitignore` y **no se sube a GitHub**. Nunca compartas tu API key.
- Todos los ejemplos de esta carpeta comparten el mismo `.env`.
