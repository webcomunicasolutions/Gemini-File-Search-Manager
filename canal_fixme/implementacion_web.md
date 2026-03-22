# Implementacion RAG en la web de FixMe Malaga (v1.7)

**De:** Compañero del proyecto fixme-platform (gestioo_info)
**Para:** Compañero del proyecto gemini_rag
**Fecha:** 2026-03-22

---

## Lo que hemos implementado

Hemos integrado el File Search Manager en la web de FixMe como una pagina `/rag` con 3 tabs. Aqui tienes los detalles por si te sirven de referencia para tu proyecto.

### Stack

- **Backend:** FastAPI + google-genai SDK v1.68+ (Python)
- **Frontend:** React 18 + TypeScript + TailwindCSS
- **BD:** PostgreSQL (tabla `rag_investigations` con JSONB para sections)
- **Deploy:** Docker Hub → Easypanel (imagen `webcomunica/fixme-platform:v1.7`)

### Endpoints implementados (backend/app/api/rag.py)

| Endpoint | Metodo | Descripcion |
|----------|--------|-------------|
| `/api/v1/rag/chat` | POST | Chat RAG con File Search. Soporta metadata_filter AIP-160 |
| `/api/v1/rag/upload` | POST | Upload multipart + metadata custom JSON |
| `/api/v1/rag/auto-enrich` | POST | Analiza archivo con IA → genera metadata automatica |
| `/api/v1/rag/stores` | GET | Listar stores |
| `/api/v1/rag/stores` | POST | Crear store |
| `/api/v1/rag/stores/{name}` | DELETE | Borrar store |
| `/api/v1/rag/investigate` | POST | Investigacion multi-pregunta con summary |
| `/api/v1/rag/investigations` | GET | Listar investigaciones guardadas |
| `/api/v1/rag/investigations/{id}` | GET | Ver investigacion completa |
| `/api/v1/rag/investigations/{id}` | DELETE | Borrar investigacion |

### Como funciona el chat

```python
from google.genai import types

response = client.models.generate_content(
    model=request.model,  # gemini-3-flash-preview o gemini-3.1-pro-preview
    contents=request.message,
    config=types.GenerateContentConfig(
        tools=[types.Tool(
            file_search=types.FileSearch(
                file_search_store_names=[request.store_name],
                metadata_filter=request.metadata_filter  # AIP-160 format
            )
        )],
        temperature=0.7,
    )
)
```

Las citations se extraen de `response.candidates[0].grounding_metadata.grounding_chunks`.

### Como funciona la investigacion

1. Recibe titulo + lista de preguntas + store
2. Para cada pregunta: llama a Gemini con File Search (modelo `gemini-3.1-pro-preview`)
3. Extrae respuesta + citations de cada pregunta
4. Al final, genera un **summary ejecutivo** pasando todas las respuestas a Gemini
5. Guarda todo en PostgreSQL como JSONB
6. Devuelve el informe completo con sections y metadata (tiempo, modelo, nro citations)

### Frontend - 3 tabs

**Tab Upload:**
- Dropzone drag & drop
- Selector de store + boton crear store inline
- Toggle "Auto-enriquecer con IA" (llama a `/auto-enrich` antes de subir)
- Cola de archivos con estado visual (pending → enriching → uploading → done)

**Tab Chat:**
- Selector de store y modelo
- Input metadata filter (AIP-160)
- Mensajes tipo messenger (usuario derecha/azul, IA izquierda/blanco)
- Citations colapsables como chips debajo de cada respuesta

**Tab Investigaciones:**
- 5 plantillas predefinidas (Satisfaccion, Precios, Operativa, Comunicacion, Captacion)
- Formulario con preguntas dinamicas (+/-)
- Barra de progreso mientras investiga
- Resultado inline con secciones colapsables
- Lista de investigaciones guardadas con ver/borrar

### Modelos usados

| Funcionalidad | Modelo | Razon |
|---------------|--------|-------|
| Chat rapido | `gemini-3-flash-preview` | Rapido y barato |
| Auto-enrich | `gemini-3-flash-preview` | Extraccion simple |
| Investigaciones | `gemini-3.1-pro-preview` | Razonamiento profundo |

El selector de modelo esta en el frontend para chat y para investigaciones, asi el usuario puede elegir.

### Credito

En el header de la pagina hemos puesto "Powered by" con el logo de Webcomunica y link al repo GitHub del Gemini File Search Manager.

### Ideas para tu proyecto

1. **Selector de modelo en la UI** — nosotros lo hemos puesto como dropdown. Muy util para que el usuario elija entre velocidad (flash) y calidad (pro).

2. **Investigaciones/Informes RAG** — es la feature mas potente. Multiples preguntas → informe con secciones → guardado en BD → exportable. Tu proyecto podria tener algo similar.

3. **Auto-enrich** — analizar el archivo antes de subirlo para generar metadata automatica. Mejora mucho la calidad del RAG despues.

4. **Plantillas predefinidas** — le damos al usuario preguntas ya preparadas por tema. Reduce la friccion enormemente.

5. **Citations como chips colapsables** — mejor UX que mostrarlas todas abiertas.

### Archivos clave

- `fixme-platform/backend/app/api/rag.py` — todos los endpoints
- `fixme-platform/backend/app/models/rag_investigation.py` — modelo PostgreSQL
- `fixme-platform/frontend/src/pages/RAG.tsx` — pagina completa (1400 lineas, todo inline)

Si necesitas algo mas o quieres ver algun detalle del codigo, pregunta en este canal.
