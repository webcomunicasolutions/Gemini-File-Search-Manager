# Resumen sesion v1.7 - Todo lo implementado

**De:** Compañero fixme-platform
**Fecha:** 2026-03-22

---

## Estado actual: v1.7 en produccion

URL: https://automatizaciones-fixme-platform.ilssio.easypanel.host
Docker Hub: webcomunica/fixme-platform:v1.7 (latest)

## Lo que hemos construido hoy

### 1. RAG completo con 4 tabs

**Tab Upload:**
- Drag & drop multiple files
- Selector de store + crear store inline
- Auto-enrich con IA: analiza archivo → genera metadata → campos editables antes de subir
- Metadata manual: editor key/value por archivo (añadir/quitar campos)
- Upload por lotes con estado visual por archivo (pending → enriching → enriched → uploading → done)
- Limites metadata aplicados: max 13 campos, excluye resumen/null, trunca 256 chars, keys 64 chars

**Tab Stores:**
- Grid de cards por store con nombre, docs count (activos/pendientes/fallidos), tamaño, fecha
- Documentos expandibles con tabla (nombre, estado, tamaño, tipo)
- Metadata de documentos como chips de colores (sky, violet, amber, emerald, rose, indigo)
- Borrar store y documentos con confirmacion (force: True)
- Barra de uso total (stores, documentos, tamaño)

**Tab Chat:**
- Selector de store y modelo (5 modelos con optgroups)
- Mensajes tipo messenger (usuario/IA)
- Citations colapsables como chips
- Filtro metadata AIP-160

**Tab Investigaciones:**
- 5 plantillas predefinidas (Satisfaccion, Precios, Operativa, Comunicacion, Captacion)
- Plantillas custom: guardar/borrar en localStorage
- Formulario con preguntas dinamicas (+/-)
- Progreso animado sin porcentaje fake ("La IA esta investigando...")
- Al completar: abre modal directamente
- Lista de investigaciones con botones "Detalles" y "Informe"
- Modal informe completo con: copiar, escuchar TTS, descargar audio, PDF, TXT
- Vista detalle con secciones colapsables y citations

### 2. Modelos disponibles (5)

| Modelo | Uso |
|--------|-----|
| gemini-3.1-pro-preview | Investigaciones (recomendado) |
| gemini-3-flash-preview | Chat (default) |
| gemini-3.1-flash-lite-preview | Rapido y barato |
| gemini-2.5-pro | Pro estable |
| gemini-2.5-flash | Flash estable |

Organizados en optgroups: Serie 3 y Serie 2.5.

### 3. Export e informes

- **PDF**: reportlab en backend, endpoint POST /investigations/{id}/export-pdf
- **TXT**: generado en frontend, descarga directa
- **Audio TTS**: Gemini TTS con voz Aoede, con controles play/pause/stop y descarga WAV
- **Copiar**: todo el texto al portapapeles

### 4. Backend (10+ endpoints)

| Endpoint | Metodo |
|----------|--------|
| /rag/chat | POST |
| /rag/upload | POST (multipart) |
| /rag/auto-enrich | POST (multipart) |
| /rag/stores | GET, POST |
| /rag/stores/{name} | DELETE (force) |
| /rag/stores/{name}/documents | GET |
| /rag/documents/{name} | DELETE (force) |
| /rag/storage-usage | GET |
| /rag/investigate | POST |
| /rag/investigations | GET |
| /rag/investigations/{id} | GET, DELETE |
| /rag/investigations/{id}/export-pdf | POST |

### 5. Bugs arreglados

- Upload metadata > 256 chars → INVALID_ARGUMENT (truncado)
- Upload metadata null/arrays → limpieza frontend + backend
- Max 13 campos metadata (aviso vuestro aplicado)
- Modelos incorrectos (2.0/2.5 → 3/3.1)
- Pantalla blanca post-investigacion (metadata fields mismatch)
- Modal solo funcionaba en vista detail (ahora global)
- Sidebar desaparecia en desktop al scroll (sticky fix)
- Progreso fake 90% → indicador animado

### 6. Creditos

- "Inspirado en Gemini File Search Manager by Webcomunica" con logos (webcomunica + optimizaconia)
- Link a https://github.com/webcomunicasolutions/Gemini-File-Search-Manager
- Footer PDF: "Generado con Gemini File Search Manager by Webcomunica"

### 7. Responsive mobile (v1.6)

Todo lo de RAG tambien es responsive:
- Sidebar hamburguesa
- Tabs adaptativos
- Cards y tablas responsive
- Botones tactiles (active:scale-95)
- Modal full-screen en mobile

## Pendiente

- Cargar los 410 archivos WhatsApp cuando termineis el experimento metadata
- El script de carga por lotes lo ejecutamos nosotros cuando nos paseis las instrucciones

## Archivos clave

- `backend/app/api/rag.py` — todos los endpoints RAG
- `backend/app/models/rag_investigation.py` — modelo PostgreSQL
- `frontend/src/pages/RAG.tsx` — pagina completa (~2500 lineas)
- `backend/requirements.txt` — google-genai + reportlab

Cualquier cosa, escribid en el canal.
