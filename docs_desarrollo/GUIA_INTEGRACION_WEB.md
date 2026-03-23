# Guia de Integracion - Gemini File Search Manager en tu Web

Como integrar el RAG de Gemini File Search en cualquier aplicacion web existente.

## Que puedes ofrecer a tus clientes

Integrar el File Search Manager en la web de tu cliente le permite:

1. **Subir documentos** y construir su propio RAG (base de conocimiento)
2. **Chatear con sus datos** usando Gemini con busqueda semantica
3. **Hacer investigaciones** con multiples preguntas y obtener informes
4. **Exportar informes** en PDF, TXT o audio (TTS)
5. **Gestionar stores** (crear, borrar, ver documentos, metadata)

## Arquitectura recomendada

```
Tu Web (React/Vue/Angular)
    |
    ├── Frontend: Pagina /rag con 3-4 tabs
    |       ├── Upload (drag & drop + auto-enrich con IA)
    |       ├── Chat (selector de store + modelo + filtros)
    |       ├── Investigaciones (plantillas + informes guardados)
    |       └── Stores (gestion de File Search stores)
    |
    └── Backend: Endpoints /api/rag/*
            ├── POST /chat (File Search + Gemini)
            ├── POST /upload (Files API + import con metadata)
            ├── POST /auto-enrich (analisis IA → metadata)
            ├── POST /investigate (multi-pregunta + summary)
            ├── GET/POST/DELETE /stores (CRUD stores)
            └── POST /tts (Text-to-Speech)
```

## Modelos recomendados por funcionalidad

| Funcionalidad | Modelo | Precio input/MTok |
|---------------|--------|-------------------|
| Chat rapido | gemini-3-flash-preview | $0.50 |
| Auto-enrich metadata | gemini-3-flash-preview | $0.50 |
| Investigaciones profundas | gemini-3.1-pro-preview | $2.00 |
| TTS (audio) | gemini-2.5-flash-preview-tts | $0.50 |

## Metadata: basica vs enriquecida

Hemos comprobado experimentalmente (410 conversaciones, 10 tests comparativos) que:

- **Consultas generales**: ambos tipos de metadata dan resultados similares
- **Filtros avanzados**: solo la metadata enriquecida permite filtrar por categoria, marca, sentimiento, estado
- **Recomendacion**: siempre subir con metadata enriquecida (el coste es minimo, ~$1.30 por 410 docs)

### Campos recomendados de metadata (max 6-10)

Los campos dependen del tipo de documento. Ejemplo para conversaciones de WhatsApp:

```json
{
  "phone": "+34686515371",
  "categoria_principal": "reparacion_pantalla",
  "marca": "Apple",
  "estado_final": "reparado",
  "sentimiento_cliente": "positivo",
  "precio_mencionado": 180.0
}
```

### Limite de metadata

La API de Gemini File Search tiene un limite practico de ~10-13 campos de custom_metadata por documento (la documentacion dice 20 pero falla con mas). Recomendamos max 10 campos.

No incluir campos largos (como "resumen") - el RAG ya busca semanticamente en el texto completo.

## Codigo de referencia

### Chat con File Search (Python)

```python
from google import genai
from google.genai import types

client = genai.Client(api_key=API_KEY)

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="tu pregunta aqui",
    config=types.GenerateContentConfig(
        tools=[types.Tool(
            file_search=types.FileSearch(
                file_search_store_names=["fileSearchStores/tu-store"],
                metadata_filter='marca="Apple"'  # AIP-160 format
            )
        )]
    )
)

# Citations
citations = response.candidates[0].grounding_metadata.grounding_chunks
```

### Subir con metadata (Python)

```python
# Paso 1: subir a Files API
uploaded_file = client.files.upload(
    file='documento.pdf',
    config={'display_name': 'documento.pdf'}
)

# Paso 2: importar con metadata
operation = client.file_search_stores.import_file(
    file_search_store_name="fileSearchStores/tu-store",
    file_name=uploaded_file.name,
    config={
        'custom_metadata': [
            {'key': 'categoria', 'string_value': 'factura'},
            {'key': 'importe', 'numeric_value': 1500.0}
        ]
    }
)

# Esperar
while not operation.done:
    time.sleep(3)
    operation = client.operations.get(operation)
```

### Auto-enriquecimiento con IA (Python)

```python
# Subir archivo temporalmente
temp_file = client.files.upload(file='documento.pdf')

# Analizar con structured output
response = client.models.generate_content(
    model='gemini-3-flash-preview',
    contents=[temp_file, "Analiza este documento y extrae metadata"],
    config=types.GenerateContentConfig(
        response_mime_type='application/json',
        response_schema={
            "type": "object",
            "properties": {
                "categoria": {"type": "string"},
                "resumen": {"type": "string"}
            }
        }
    )
)

metadata = json.loads(response.text)
```

### Investigacion multi-pregunta (Python)

```python
questions = [
    "Cuales son los problemas mas frecuentes?",
    "Como es la atencion al cliente?",
    "Que precios se manejan?"
]

sections = []
for q in questions:
    response = client.models.generate_content(
        model="gemini-3.1-pro-preview",  # Pro para investigaciones
        contents=q,
        config=types.GenerateContentConfig(
            tools=[types.Tool(
                file_search=types.FileSearch(
                    file_search_store_names=[store_name]
                )
            )]
        )
    )
    sections.append({
        'question': q,
        'answer': response.text,
        'citations': extract_citations(response)
    })

# Summary ejecutivo
all_text = "\n".join([f"Q: {s['question']}\nA: {s['answer']}" for s in sections])
summary = client.models.generate_content(
    model="gemini-3.1-pro-preview",
    contents=f"Genera un resumen ejecutivo:\n\n{all_text}"
)
```

### TTS - Escuchar resumen (Python)

```python
response = client.models.generate_content(
    model='gemini-2.5-flash-preview-tts',
    contents=texto,
    config=types.GenerateContentConfig(
        response_modalities=['AUDIO'],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name='Aoede')
            )
        )
    )
)
# PCM audio en response.candidates[0].content.parts[0].inline_data.data
# Convertir a WAV para el browser
```

## Costes tipicos

| Concepto | Coste |
|----------|-------|
| Indexar 410 documentos (9 MB) | ~$0.34 |
| Enriquecer 410 docs con IA | ~$1.30 |
| Almacenamiento | GRATIS |
| Consultas | Solo tokens del modelo |
| Una investigacion (5 preguntas) | ~$0.05 con Pro |

## Proyecto de referencia

Este Manager es open source: https://github.com/webcomunicasolutions/Gemini-File-Search-Manager

Desarrollado por [Webcomunica Soluciones Informaticas](https://webcomunica.solutions/)
