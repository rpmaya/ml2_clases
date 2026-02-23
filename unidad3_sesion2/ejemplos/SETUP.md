# Setup - Ejemplos Unidad 3, Sesion 2

## 1. Activar el entorno virtual

```bash
source ~/Documents/GitHub/ml2_code/llm_env/bin/activate
```

> Si no tienes el entorno creado, crealo primero:
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

Abre `.env` y reemplaza con tu API key de OpenRouter:

```
OPENROUTER_API_KEY=sk-or-v1-...tu-api-key-aqui
```

> Puedes obtener tu API key en https://openrouter.ai/settings/keys

## 3. Ejecutar ejemplos

```bash
python ejemplo_3_1_openrouter.py                # Primera llamada via OpenRouter
python ejemplo_3_2_anatomia_llamada_api.py       # Anatomia de la llamada API
python ejemplo_3_3_parametros_clave.py           # Efecto de temperature y top_p
python ejemplo_3_4_manteniendo_contexto.py       # Conversacion multi-turno
python ejemplo_3_5_gestion_context_window.py     # Truncar y resumir historial
python ejemplo_3_6_streaming.py                  # Respuesta token a token
python ejemplo_3_7_manejo_errores.py             # Reintentos y errores
python ejemplo_4_1_chatbot_memoria.py            # Chatbot con memoria (clase)
python ejemplo_4_2_sentimiento.py                # Analisis de sentimiento por lotes
python ejemplo_4_3_extraccion_json.py            # Extraccion estructurada (JSON)
python ejemplo_4_4_function_calling.py           # Function Calling / Tool Use
python ejemplo_5_1_langchain_basico.py           # LangChain: modelos, templates y chains
```

## Notas

- Todos los ejemplos usan **OpenRouter** como API Gateway con el modelo gratuito `arcee-ai/trinity-large-preview:free`.
- El archivo `.env` esta en `.gitignore` y **no se sube a GitHub**. Nunca compartas tu API key.
- Todos los ejemplos de esta carpeta comparten el mismo `.env`.
