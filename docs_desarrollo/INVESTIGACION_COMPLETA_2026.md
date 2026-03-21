# Investigacion Completa - Gemini File Search API (Marzo 2026)

Scraping exhaustivo de 10 fuentes oficiales realizado el 21/03/2026.
Archivos raw en `/tmp/claude-1000/gemini_*.md`

---

## RESUMEN EJECUTIVO

### Lo que CAMBIA y nos afecta directamente

| Hallazgo | Impacto | Urgencia |
|----------|---------|----------|
| `gemini-2.0-flash-exp` DEPRECADO, shutdown 1 junio 2026 | El Manager lo usa para suggest-metadata | **CRITICA** |
| Metadata filter cambia de objetos a string AIP-160 | Nuestro backend usa formato viejo | **ALTA** |
| Modelo default en docs es `gemini-3-flash-preview` | Nuestro Manager usa 2.5-flash | MEDIA |
| File Search NO combinable con Google Search | Descarta feature de "dual search" | INFO |
| Structured output nuevo (Pydantic/Zod + File Search) | Oportunidad de mejora en chat | MEDIA |
| Limits de archivo: 100 MB confirmado | Ya documentado, verificar validaciones | BAJA |

### Lo que NO cambia (confirmado estable)

- SDK Python: mismos metodos `file_search_stores.create()`, `.get()`, `.delete()`
- Documents API: `.list()`, `.get()`, `.delete()` sin cambios
- Polling de operations: mismo patron `while not operation.done`
- Pricing File Search: $0.15/MTok indexacion, storage gratis, queries gratis
- `gemini-embedding-001` sigue funcionando dentro de File Search
- REST endpoints: misma base URL y paths

---

## 1. MODELOS - Estado actual completo

### Para generacion (chat del Manager)

| Modelo | Estado | Soporta File Search | Precio input/MTok |
|--------|--------|--------------------|--------------------|
| `gemini-3.1-pro-preview` | Activo | Si | $2.00 |
| `gemini-3.1-flash-lite-preview` | Activo | Si | $0.25 |
| `gemini-3-flash-preview` | Activo (default en docs) | Si | $0.50 |
| `gemini-2.5-pro` | Estable | Si | $1.25 |
| `gemini-2.5-flash` | Estable | NO listado en File Search | $0.30 |
| `gemini-2.5-flash-lite` | Estable | Si | $0.10 |
| `gemini-2.0-flash` | **DEPRECADO** (shutdown jun 2026) | N/A | $0.10 |
| `gemini-2.0-flash-exp` | **YA APAGADO** (nov 2025) | N/A | N/A |

**ALERTA**: `gemini-2.0-flash-exp` fue apagado en la deprecacion de noviembre 2025. El Manager lo usa en suggest-metadata. Puede que siga funcionando por redirect pero NO es fiable.

**NOTA IMPORTANTE**: `gemini-2.5-flash` NO aparece en la tabla oficial de modelos que soportan File Search. Los que si aparecen son: Gemini 3.1 Pro, 3.1 Flash-Lite, 3 Flash, 2.5 Pro, y 2.5 Flash-Lite.

### Para embeddings

| Modelo | Estado | Tipo | Dimensiones | Precio |
|--------|--------|------|-------------|--------|
| `gemini-embedding-001` | Estable (usado por File Search) | Solo texto | 768/1536/3072 | $0.15/MTok |
| `gemini-embedding-2-preview` | Preview (marzo 2026) | Multimodal | 128-3072 | $0.20/MTok |
| `text-embedding-004` | **APAGADO** (14 ene 2026) | N/A | N/A | N/A |
| `embedding-001` | **APAGADO** (oct 2025) | N/A | N/A | N/A |

### Aliases actuales (enero 2026)

- `gemini-pro-latest` -> `gemini-3-pro-preview`
- `gemini-flash-latest` -> `gemini-3-flash-preview`

---

## 2. METADATA FILTERING - CAMBIO DE SINTAXIS

### ANTES (formato que usa nuestro Manager)

```python
# Formato viejo con objetos conditions
tools=[types.Tool(
    file_search=types.FileSearch(
        file_search_store_names=[store.name],
        # NO HAY metadata_filter aqui
    )
)]
# Los filtros se pasaban en el body del REST como metadataFilters con conditions
```

### AHORA (formato actual en docs oficiales)

```python
# Python SDK - string AIP-160
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Tell me about...",
    config=types.GenerateContentConfig(
        tools=[
            types.Tool(
                file_search=types.FileSearch(
                    file_search_store_names=[store.name],
                    metadata_filter="author=Robert Graves",  # STRING, no objeto
                )
            )
        ]
    )
)
```

```javascript
// JavaScript SDK
config: {
    tools: [{
        fileSearch: {
            fileSearchStoreNames: [store.name],
            metadataFilter: 'author="Robert Graves"',  // STRING
        }
    }]
}
```

```bash
# REST
"file_search": {
    "file_search_store_names": ["store_name"],
    "metadata_filter": "author = \"Robert Graves\""
}
```

### Sintaxis AIP-160

- Guia: https://google.aip.dev/160
- Igualdad: `key=value`
- Numericos: `year > 2020`
- Combinacion AND implicito entre keys distintos
- OR para mismo key

**IMPACTO**: Nuestro backend construye filtros con el formato viejo de objetos `metadataFilters` con `conditions`. Hay que migrar al formato string.

---

## 3. CUSTOM METADATA EN IMPORT - Cambio de firma

### ANTES

```python
# custom_metadata dentro de config (como lo tiene nuestro Manager)
operation = client.file_search_stores.import_file(
    file_search_store_name=store.name,
    file_name=file.name,
    config={
        'custom_metadata': [...]
    }
)
```

### AHORA (docs actuales)

```python
# custom_metadata como parametro directo
operation = client.file_search_stores.import_file(
    file_search_store_name=store.name,
    file_name=file.name,
    custom_metadata=[
        {"key": "author", "string_value": "Robert Graves"},
        {"key": "year", "numeric_value": 1934}
    ]
)
```

**NOTA**: En JavaScript, `customMetadata` SI sigue dentro de `config`:
```javascript
await ai.fileSearchStores.importFile({
    fileSearchStoreName: store.name,
    fileName: file.name,
    config: {
        customMetadata: [
            { key: "author", stringValue: "Robert Graves" }
        ]
    }
});
```

---

## 4. STRUCTURED OUTPUT + FILE SEARCH (NUEVO - Gemini 3)

A partir de Gemini 3, se puede combinar File Search con respuestas estructuradas:

```python
from pydantic import BaseModel, Field

class Money(BaseModel):
    amount: str = Field(description="The numerical part of the amount.")
    currency: str = Field(description="The currency of amount.")

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="What is the minimum hourly wage?",
    config=types.GenerateContentConfig(
        tools=[
            types.Tool(
                file_search=types.FileSearch(
                    file_search_store_names=[store.name]
                )
            )
        ],
        response_mime_type="application/json",
        response_schema=Money.model_json_schema()
    )
)
result = Money.model_validate_json(response.text)
```

**IMPACTO**: Esto es una mejora potente para el Manager. En lugar de texto libre, podemos forzar que las respuestas del chat vengan en JSON estructurado cuando el usuario lo necesite.

---

## 5. TOOL COMBINATIONS (NUEVO - Gemini 3)

### Lo que SI se puede combinar

- **File Search + Function Calling** (custom tools) -> SI, desde Gemini 3
- **File Search + Google Maps** -> indirectamente, pero con limitaciones
- Cross-tool context circulation: el output de una tool se preserva como input de la siguiente

### Lo que NO se puede combinar

- **File Search + Google Search Grounding** -> NO, explicitamente documentado como incompatible
- **File Search + URL Context** -> NO
- **File Search + Live API** -> NO

### Interactions API (nueva)

Google recomienda la nueva **Interactions API** en vez de `generateContent` para workflows complejos con tools. Tiene server-side state y session resumption.

**IMPACTO**: La idea de "buscar en documentos Y en Google a la vez" NO es viable con File Search. Habria que hacer 2 llamadas separadas y combinar resultados manualmente.

---

## 6. GEMINI EMBEDDING 2 - Detalles completos

### Especificaciones

| Campo | Valor |
|-------|-------|
| Modelo | `gemini-embedding-2-preview` |
| Estado | Public Preview (10 marzo 2026) |
| Dimensiones | 128-3072 (default 3072, recomendado 768/1536/3072) |
| Texto | Hasta 8.192 tokens |
| Imagenes | Max 6 por request (PNG, JPEG) |
| Video | Max 120s (MP4, MOV, codecs H264/H265/AV1/VP9, max 32 frames) |
| Audio | Max 80 segundos (MP3, WAV) - nativo, sin transcripcion |
| PDFs | Max 6 paginas |
| Idiomas | 100+ |
| Precio texto | $0.20/MTok |
| Precio imagen | $0.45/MTok ($0.00012/imagen) |
| Precio audio | $6.50/MTok ($0.00016/segundo) |
| Precio video | $12.00/MTok ($0.00079/frame) |
| Batch | 50% descuento |
| MRL | Si (Matryoshka Representation Learning) |

### Migracion de embedding-001 a embedding-2

**CRITICO**: Los espacios vectoriales son INCOMPATIBLES. No se pueden comparar embeddings de modelos distintos. Migrar requiere re-embeddear TODO.

### Impacto en File Search

- File Search usa `gemini-embedding-001` internamente para indexar
- Cuando embedding-2 salga a GA, File Search probablemente lo adopte
- NO hay forma de elegir el modelo de embedding en File Search (es automatico)
- La migracion seria transparente (Google re-indexaria internamente)

### Integraciones disponibles

LangChain, LlamaIndex, Haystack, Weaviate, QDrant, ChromaDB, Vertex AI Vector Search

---

## 7. LIMITES Y ALMACENAMIENTO

### Limites de archivo

| Campo | Valor |
|-------|-------|
| Max file size (upload) | 100 MB |
| Max inline data (base64) | 100 MB |
| PDFs | Max 1.000 paginas o 50 MB |
| Max metadata items/doc | 20 |
| displayName max | 512 caracteres |
| name ID max | 40 caracteres (lowercase alfanumerico o guiones) |
| pageSize max (list) | 20 |

### Limites de stores

| Tier | Limite total proyecto |
|------|----------------------|
| Free | 1 GB |
| Tier 1 | 10 GB |
| Tier 2 | 100 GB |
| Tier 3 | 1 TB |

- Max 500 stores por proyecto
- Recomendado: cada store < 20 GB para latencia optima
- Tamano backend ≈ 3x input (incluye embeddings + indices)
- `sizeBytes` en API reporta bytes RAW, no el 3x

### Ambiguedad no resuelta

El foro de Google no ha respondido si el limite del tier se mide en bytes raw o bytes backend (3x). Planificar conservadoramente con el 3x:

| Tier | Capacidad conservadora (raw) | Capacidad optimista (raw) |
|------|------------------------------|--------------------------|
| Free | ~333 MB | 1 GB |
| Tier 1 | ~3.3 GB | 10 GB |
| Tier 2 | ~33 GB | 100 GB |
| Tier 3 | ~333 GB | 1 TB |

### Input desde GCS y URLs (enero 2026)

- **GCS buckets**: `client.files.register_files(uris=["gs://bucket/file.pdf"], auth=gcs_creds)`
- **URLs publicas HTTPS**: `types.Part.from_uri(file_uri="https://...")`
- **Pre-signed URLs**: AWS S3, Azure Blob, etc.
- Requiere OAuth con scopes `cloud-platform` y `devstorage.read_only`

**ADVERTENCIA**: Esta funcionalidad es para `generate_content` directo. NO esta confirmado que `uploadToFileSearchStore` o `importFile` soporten GCS URIs directamente. Hay que verificar con la API.

---

## 8. PRICING COMPLETO ACTUALIZADO

### File Search

| Concepto | Precio |
|----------|--------|
| Embeddings al indexar | $0.15/MTok (usando gemini-embedding-001) |
| Almacenamiento | GRATIS |
| Queries (embeddings en busqueda) | GRATIS |
| Tokens recuperados en respuesta | Precio normal del modelo usado |

### Google Search Grounding (comparativa)

| Serie | Free | Paid |
|-------|------|------|
| Gemini 2.5 | 500-1500 RPD gratis | $35/1.000 prompts |
| Gemini 3 | Varia | $14/1.000 search queries + 5.000/mes gratis |

### Coste estimado para FixMe Malaga

- 11.587 conversaciones WhatsApp
- ~6M tokens estimados
- Indexacion: 6M x $0.15/1M = **$0.90 total**
- Almacenamiento: $0/mes
- Consultas: solo el coste del modelo de chat

---

## 9. CHANGELOG COMPLETO - Hitos clave

| Fecha | Evento |
|-------|--------|
| Mar 7, 2025 | Primer modelo embeddings experimental (`gemini-embedding-exp-03-07`) |
| Jul 14, 2025 | `gemini-embedding-001` estable, deprecan exp |
| Sep 16, 2025 | Deprecan `embedding-001`, `embedding-gecko-001` |
| Sep 29, 2025 | Apagan modelos Gemini 1.5 |
| Nov 4, 2025 | Anuncian deprecacion de `gemini-2.0-flash-exp` (shutdown dic 2025) |
| Nov 6, 2025 | **File Search API lanza a public preview** |
| Nov 18, 2025 | Lanzan Gemini 3 Pro Preview |
| Dic 17, 2025 | Lanzan Gemini 3 Flash Preview |
| Ene 8, 2026 | GCS buckets + URLs como input, limite sube a 100 MB |
| Ene 14, 2026 | Apagan `text-embedding-004` |
| Ene 21, 2026 | `gemini-flash-latest` -> `gemini-3-flash-preview` |
| Feb 18, 2026 | Deprecan `gemini-2.0-flash` (shutdown jun 2026) |
| Mar 3, 2026 | Lanzan Gemini 3.1 Flash-Lite Preview |
| Mar 10, 2026 | `gemini-embedding-2-preview` (multimodal) |
| Mar 18, 2026 | Built-in Tools + Function Calling combo |

---

## 10. IMPACTO DIRECTO EN NUESTRO MANAGER - Plan de accion

### URGENTE (rompe o va a romper)

1. **Cambiar modelo suggest-metadata**: `gemini-2.0-flash-exp` -> `gemini-2.5-flash` o `gemini-3-flash-preview`
   - Linea ~794 en app.py: `model='gemini-2.0-flash-exp'`
   - El modelo exp fue apagado en nov/dic 2025, puede funcionar por redirect pero es inestable

2. **Migrar metadata filtering**: de objetos `metadataFilters` con `conditions` a string AIP-160
   - Lineas ~300-343 en app.py
   - Formato nuevo: `metadata_filter="tipo=contrato"`

### ALTA PRIORIDAD (mejoras significativas)

3. **Verificar que `gemini-2.5-flash` soporta File Search**: la tabla oficial de docs solo lista 2.5 Pro y 2.5 Flash-Lite, NO 2.5 Flash regular. Puede que funcione pero no esta en la tabla.

4. **Actualizar modelo de chat**: considerar `gemini-3-flash-preview` como opcion (es el default en docs)

5. **Structured output**: anadir opcion de respuesta JSON estructurada en el chat

### MEDIA PRIORIDAD (mejoras de UX)

6. **Estimador de costes**: calcular coste de indexacion antes de subir batches grandes
7. **Info de tier y almacenamiento**: mostrar uso actual vs limite
8. **Selector de modelo en UI**: ofrecer gemini-3-flash-preview, gemini-2.5-pro, etc.

### BAJA PRIORIDAD (futuro)

9. **Import desde GCS/URL**: verificar primero si File Search lo soporta nativamente
10. **Batch upload**: multiples archivos en una operacion
11. **Export workflow n8n completo**: generar .json importable

### DESCARTADO

- ~~Google Search + File Search combo~~: confirmado INCOMPATIBLE oficialmente
- ~~Seleccion de modelo de embedding en File Search~~: no es configurable, lo decide Google

---

## FUENTES SCRAPEADAS

| # | URL | Archivo local |
|---|-----|---------------|
| 1 | https://ai.google.dev/gemini-api/docs/file-search | gemini_file_search_docs.md |
| 2 | https://ai.google.dev/gemini-api/docs/embeddings | gemini_embeddings_docs.md |
| 3 | https://ai.google.dev/gemini-api/docs/changelog | gemini_changelog.md |
| 4 | https://ai.google.dev/gemini-api/docs/pricing | gemini_pricing.md |
| 5 | Blog Gemini Embedding 2 | gemini_embedding2_blog.md |
| 6 | Blog File Limits | gemini_file_limits.md |
| 7 | Blog Gemini 3 Tooling | gemini3_tooling.md |
| 8 | Forum Store Limits | gemini_store_limits.md |
| 9 | Context7 SDK docs | gemini_sdk_context7.md |
| 10 | Python SDK reference | gemini_python_sdk.md |
