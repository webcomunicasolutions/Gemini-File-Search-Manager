# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Gemini File Search Manager v2.1.0 - Flask application for Retrieval Augmented Generation (RAG) using Google's Gemini File Search API. Enables semantic search by chunking, embedding, and indexing documents to provide grounded responses from Gemini models.

**Active deployment**: Store `fixmemalagawhatsapp-b3jrkfmmcj58` contains 408 WhatsApp conversations loaded for FixMe Malaga.

## Project Structure

- **Backend**: `web_app/app.py` - Flask application
- **Frontend**: `web_app/templates/index.html` - Single-page application (vanilla JS, no frameworks)
- **State**: `web_app/store_state.json` - JSON persistence for store name and file metadata

## Key Concepts

### File Search Architecture
1. **Create a File Search store**: A persistent container for document embeddings
2. **Upload and import files**: Files are chunked, embedded using `gemini-embedding-001`, and indexed
3. **Query with File Search**: The model performs semantic search on the store to ground responses

### Important Implementation Details
- Raw files uploaded via Files API are deleted after 48 hours
- File Search store data persists indefinitely until manually deleted
- File Search store names are globally scoped (auto-generated: displayName + 12-char suffix)
- Default chat model: `gemini-3-flash-preview`
- Metadata suggestion model: `gemini-3-flash-preview` (was `gemini-2.0-flash-exp`)
- Embedding model: `gemini-embedding-001`
- Upload timeout: 120 seconds with progress logging every 15 seconds
- Conversation history limit: 7 message pairs (MAX_HISTORY = 7)

## Supported Models (Chat Whitelist)

```python
ALLOWED_MODELS = [
    'gemini-3-flash-preview',
    'gemini-3.1-flash-lite-preview',
    'gemini-2.5-pro',
    'gemini-2.5-flash-lite',
]
```

## Flask Application Endpoints

### Core Chat & Upload
- `POST /chat` - Chat with RAG. Params: `message`, `model`, `top_k` (1-100), `thinking_level` (high/low), `media_resolution` (low/medium/high), `metadata_filters`, `output_schema` (JSON schema for structured output)
- `POST /upload` - Upload single file to active store with metadata
- `POST /batch-upload` - Upload multiple files with per-file progress tracking and cost estimation
- `POST /import-url` - Import file from public URL (SSRF-protected)

### Metadata
- `POST /suggest-metadata` - AI-powered metadata suggestion from document content
- `POST /auto-enrich` - AI-powered metadata enrichment with structured output (runs before upload)
- `PUT /update-metadata/<document_id>` - Update local metadata (no re-upload needed)

### Documents & Stores
- `GET /documents` - List documents in active store
- `DELETE /documents/<document_id>` - Delete a document
- `POST /document-query` - Semantic search on a specific document (retrieval only, no generation)
- `GET /stores` - List all File Search stores
- `POST /stores` - Create a new store
- `DELETE /stores/<store_name>` - Delete store with `force=True`
- `POST /switch-store` - Switch active store (resets uploaded_files in state)

### System & Monitoring
- `GET /api-info` - App info including active store (API key masked)
- `GET /storage-usage` - Storage usage and tier info
- `POST /update-tier` - Update current tier setting (Free/Tier1/Tier2/Tier3)

## Metadata Filtering

Filters use AIP-160 string format. The frontend sends a simple array and the backend converts it:

**Frontend format**:
```javascript
[
    { key: 'tipo', value: 'contrato' },
    { key: 'year', value: 2024 }
]
```

**Converted to AIP-160 filter string** (AND between different keys):
```
chunk.custom_metadata.tipo = "contrato" AND chunk.custom_metadata.year = 2024
```

Note: The old `conditions` objects format is deprecated. Use AIP-160 string format.

## Key Features

### AI Metadata System
- `POST /suggest-metadata`: Uploads file temporarily to Files API, sends to model with expert system prompt, extracts structured metadata (max 20 fields), deletes temp file
- `POST /auto-enrich`: Runs enrichment before upload using structured output / JSON schema response
- Key rule: `titulo` field is extracted from document CONTENT, not from the filename
- 8 pre-configured templates: factura, contrato, informe, manual, presentacion, acta, certificado, email

### Chat Features (v2.1.0)
- **Model selector**: Choose from whitelisted models per request
- **top_k control**: 1-100 results retrieved from store (sent in retrieval config)
- **thinking_level**: `high` or `low` - applies to Gemini 3 models only
- **media_resolution**: `low`, `medium`, or `high` for multimodal content
- **Structured output**: Pass a JSON schema via `output_schema`; backend uses `response_mime_type: application/json`
- **Citations**: Extracted from `response.candidates[0].grounding_metadata.grounding_chunks`

### Upload Features (v2.1.0)
- **Batch upload**: Multiple files with per-file progress SSE stream
- **Cost estimator**: Estimates embedding cost before upload based on estimated token count
- **Import from URL**: Downloads file from public URL and imports; SSRF protection blocks private IPs

### Hybrid Metadata Storage
Gemini metadata (stored at upload, immutable) is merged with local metadata (`store_state.json`, editable anytime). Local overrides Gemini:
```python
final_metadata = {**gemini_metadata, **local_metadata}
```

### Store Management
- List/switch/create/delete stores from the File Stores tab
- `force=True` required to delete stores or documents that have children
- `store_state.json` updated after every mutation (upload, delete, switch, metadata update)

## Security Measures (v2.1.0)

- API key masked in `/api-info` response (shows only last 4 chars)
- SSRF protection in `/import-url`: blocks 10.x, 192.168.x, 172.16-31.x, 127.x ranges
- Real-time file size check during URL download (enforces 100 MB limit)
- CORS restricted to `localhost` origins only
- Debug mode controlled via `FLASK_DEBUG` env var (not hardcoded)

## Tier & Storage

| Tier | Storage |
|------|---------|
| Free | 1 GB    |
| Tier 1 | 10 GB |
| Tier 2 | 100 GB |
| Tier 3 | 1 TB   |

- Backend computed size is approximately 3x raw input (includes embeddings)
- Recommended: keep each store under 20 GB for optimal query latency
- Use `GET /storage-usage` to monitor current usage

## Rate Limits and Pricing

- Max file size: 100 MB per document
- Embeddings at indexing: $0.15 per 1M tokens
- Storage: Free
- Query-time embeddings: Free
- Retrieved document tokens: Charged as regular context tokens

## REST API Reference (Gemini)

Base URL: `https://generativelanguage.googleapis.com/v1beta`

| Operation | Method | Path |
|-----------|--------|------|
| Create store | POST | `/fileSearchStores` |
| List stores | GET | `/fileSearchStores` |
| Get store | GET | `/fileSearchStores/{store}` |
| Delete store | DELETE | `/fileSearchStores/{store}?force=true` |
| Upload to store | POST | `/fileSearchStores/{store}:uploadToFileSearchStore` |
| Import file | POST | `/fileSearchStores/{store}:importFile` |
| List documents | GET | `/fileSearchStores/{store}/documents` |
| Get document | GET | `/fileSearchStores/{store}/documents/{doc}` |
| Delete document | DELETE | `/fileSearchStores/{store}/documents/{doc}?force=true` |
| Query document | POST | `/fileSearchStores/{store}/documents/{doc}:query` |
| Get operation | GET | `/fileSearchStores/{store}/operations/{op}` |

All list operations are paginated (`pageSize` max 20, `nextPageToken`). Long-running operations require polling until `done: true`.

## Document States

- `STATE_PENDING`: Chunks being processed
- `STATE_ACTIVE`: Ready for querying
- `STATE_FAILED`: Processing failed

## File Format Support

Supports 100+ MIME types. Key categories:
- Documents: PDF, DOCX, ODT, RTF
- Spreadsheets: XLSX, CSV, TSV
- Code: Python, JS, TS, Java, C/C++, Go, Rust, and many more
- Markup: MD, HTML, XML, YAML, JSON
- Notebooks: `.ipynb`
- Archives: `.zip`

See `SUPPORTED_FORMATS.md` for the complete list.

## For Future Claude Sessions

1. Read `web_app/app.py` first to understand current endpoint implementations
2. Check `web_app/store_state.json` for current active store and indexed documents
3. Metadata filtering uses AIP-160 string format - do not use the old `conditions` object format
4. The model whitelist is enforced server-side; do not add models outside it without testing
5. SSRF and CORS protections are active - test URL import features against localhost carefully
6. Always test changes locally before committing; the FixMe Malaga store is production data
