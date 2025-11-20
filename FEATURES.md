# Features Documentation

## 🌍 Available Languages

- [English](FEATURES.md)
- [Español](FEATURES_ES.md)

---

Comprehensive guide to all features in Gemini File Search Manager application.

## Table of Contents

- [AI Metadata Suggestion System](#ai-metadata-suggestion-system)
- [Document Upload & Management](#document-upload--management)
- [RAG Chat Interface](#rag-chat-interface)
- [Metadata Filtering](#metadata-filtering)
- [File Search Store Management](#file-search-store-management)
- [Tab-Based Navigation](#tab-based-navigation)
- [Citation & Grounding](#citation--grounding)
- [State Persistence](#state-persistence)

---

## AI Metadata Suggestion System

### Overview

The **AI Metadata Suggestion System** is the flagship feature of this application. It uses Gemini 2.0 Flash Exp to analyze document content and automatically extract structured metadata, eliminating manual data entry and ensuring consistency.

### How It Works

1. **Upload**: User selects a document (PDF, DOCX, TXT, etc.)
2. **Analyze**: Click "Sugerir con IA" button
3. **Process**: Document sent to Gemini 2.0 Flash with expert system instruction
4. **Extract**: AI analyzes content and returns structured JSON metadata
5. **Review**: User reviews suggested metadata in UI
6. **Edit**: User can modify any field before uploading
7. **Upload**: Document uploaded with finalized metadata

### System Prompt

The AI uses a carefully crafted system instruction (lines 794-832 in `app.py`):

```
You are an expert in document analysis and metadata management for RAG systems.

EXTRACTION RULES:
- Maximum 20 metadata fields (Gemini File Search API limit)
- Field names: lowercase, no spaces, use underscores
- Values: simple strings or numbers, no arrays or objects
- Only include metadata explicitly found in the document
- Prioritize metadata useful for search and filtering

UNIVERSAL METADATA (if applicable):
- titulo: descriptive title (extracted from CONTENT, NOT filename)
- tipo: document category
- fecha: main date (YYYY-MM-DD format)
- autor: creator or responsible party
- departamento: organizational area
- confidencialidad: public/internal/confidential/private
- estado: active/pending/archived/etc
- tags: keywords (max 5, comma-separated)
```

### Document Types Recognized

The AI automatically recognizes and extracts metadata for:

**Facturas (Invoices):**
- numero_factura
- proveedor (supplier)
- cliente (client)
- importe (amount)
- fecha (date)
- estado (status)

**Contratos (Contracts):**
- partes (parties involved)
- fecha_firma (signature date)
- vigencia_hasta (valid until)
- valor_contrato (contract value)
- area (department/area)
- estado (status)

**Informes (Reports):**
- autor (author)
- departamento (department)
- fecha (date)
- periodo (period covered)
- confidencial (confidentiality level)

**Manuales (Manuals):**
- producto (product)
- version
- idioma (language)
- autor (author)
- fecha_publicacion (publication date)

**Emails:**
- remitente (sender)
- destinatarios (recipients)
- asunto (subject)
- fecha (date)
- prioridad (priority)

**And more**: Presentaciones, Actas, Certificados, etc.

### Technical Implementation

**Endpoint**: `/suggest-metadata`

**Model**: `gemini-2.0-flash-exp`

**Configuration**:
```python
{
    'system_instruction': expert_prompt,
    'temperature': 0.1  # Low for consistency
}
```

**Processing Flow**:
```
File uploaded (multipart/form-data)
    ↓
Temporary upload to Gemini Files API
    ↓
Generate content with system instruction
    ↓
Parse JSON response (remove markdown blocks)
    ↓
Delete temporary file
    ↓
Return metadata to client
```

**Response Time**: 5-15 seconds depending on:
- File size
- Document complexity
- API latency

### Metadata Quality

**Accuracy**: ~90% for well-structured documents

**Factors affecting quality**:
- Document format (structured PDFs work best)
- Language (Spanish optimized, English supported)
- Content clarity (headers, labels help)
- Scanned documents (OCR quality matters)

**Best practices**:
- Use clear document structure
- Include headers and labels
- Ensure text is selectable (not images)
- Review suggestions before uploading

### Example Results

**Input**: Invoice PDF

**AI Suggestion**:
```json
{
  "titulo": "Factura de Servicios Cloud - Microsoft Azure 19 de Noviembre de 2025",
  "tipo": "factura",
  "numero_factura": "INV-2024-001234",
  "proveedor": "Microsoft Corporation",
  "cliente": "Tu Empresa SL",
  "importe": 1247.89,
  "fecha": "2024-11-15",
  "estado": "pendiente",
  "departamento": "IT",
  "confidencialidad": "interno",
  "tags": "cloud, azure, servicios, tecnologia"
}
```

### Limitations

- **Max fields**: 20 per document (Gemini API limit)
- **Field names**: Must be lowercase with underscores
- **Value types**: Strings and numbers only (no arrays/objects)
- **File types**: Text-extractable formats (no pure images without OCR)
- **Language**: Optimized for Spanish, works with English

### Future Enhancements

- [ ] Multi-language support
- [ ] Custom metadata templates
- [ ] Batch metadata extraction
- [ ] Metadata validation rules
- [ ] Confidence scores for each field

---

## Document Upload & Management

### Supported File Types

File Search supports a wide range of file formats (200+ MIME types):

**Documents**:
- PDF (`.pdf`)
- Microsoft Word (`.doc`, `.docx`)
- OpenDocument (`.odt`)
- Text files (`.txt`)
- Markdown (`.md`)
- Rich Text Format (`.rtf`)
- HTML (`.html`)

**Spreadsheets**:
- Excel (`.xlsx`, `.xls`)
- OpenDocument Spreadsheet (`.ods`)
- CSV (`.csv`)
- TSV (`.tsv`)

**Presentations**:
- PowerPoint (`.pptx`, `.ppt`)
- OpenDocument Presentation (`.odp`)

**Code Files**:
- Python, JavaScript, TypeScript, Java, C, C++, C#
- Go, Rust, PHP, Ruby, Swift, Kotlin, Scala
- Perl, Dart, R, Shell scripts
- And many more programming languages

**Data Formats**:
- JSON (`.json`)
- XML (`.xml`)
- YAML (`.yaml`, `.yml`)
- SQL (`.sql`)

**Other**:
- LaTeX (`.tex`)
- Jupyter Notebooks (`.ipynb`)
- ZIP archives (`.zip`)
- YAML (`.yaml`)
- HTML (`.html`)

### Upload Process

**Step 1: Select File**
```javascript
// User clicks "Elegir Archivo"
<input type="file" id="fileInput">
```

**Step 2: Optional AI Analysis**
```javascript
// Click "Sugerir con IA" for metadata extraction
POST /suggest-metadata
```

**Step 3: Review Metadata**
```javascript
// Display suggested metadata in form
// User can edit any field
```

**Step 4: Upload**
```javascript
// Upload with finalized metadata
POST /upload
```

**Step 5: Processing**
```
File saved temporarily
    ↓
Uploaded to Gemini Files API
    ↓
Imported to File Search Store
    ↓
Document chunked (white_space_config)
    ↓
Chunks embedded (gemini-embedding-001)
    ↓
Indexed in vector database
    ↓
Metadata saved to store_state.json
    ↓
Temporary file deleted
```

### Chunking Configuration

Documents are split into chunks for efficient retrieval:

**Default Configuration**:
```python
{
    'max_tokens_per_chunk': 200,
    'max_overlap_tokens': 20
}
```

**Custom Configuration** (per upload):
```python
{
    'enabled': True,
    'max_tokens_per_chunk': 500,  # Larger chunks
    'max_overlap_tokens': 50       # More context
}
```

**Recommended Settings**:

| Document Type | Tokens/Chunk | Overlap |
|---------------|--------------|---------|
| Short (< 10 pages) | 200 | 20 |
| Medium (10-50) | 500 | 50 |
| Long (> 50) | 1000 | 100 |

### Document States

Documents go through these states:

1. **PENDING**: Chunks being processed
2. **ACTIVE**: Ready for querying
3. **FAILED**: Processing error occurred

Check status in "Documentos" tab.

### File Size Limits

- **Max file size**: 100 MB per document
- **Total store size**: Varies by Gemini tier (Free: 1GB, Tier 1: 10GB)
- **Backend size**: ~3x input size (includes embeddings)

### Document Deletion

Delete documents via:
- **UI**: "Documentos" tab → Delete button
- **API**: `DELETE /delete-document`

**Effect**:
- Document removed from store
- Chunks deleted from vector database
- Metadata removed from local state
- Cannot be undone

---

## RAG Chat Interface

### Overview

Chat with your documents using semantic search powered by Gemini File Search API.

### How It Works

**User Query Flow**:
```
User types message
    ↓
Optional: Add metadata filters
    ↓
Query sent to backend
    ↓
Conversation context built (last 7 pairs)
    ↓
Semantic search on File Search Store
    ↓
Relevant chunks retrieved
    ↓
Gemini generates grounded response
    ↓
Citations extracted
    ↓
Response displayed with citations
```

### Conversation History

The system maintains context by storing the last 7 message pairs:

```python
conversation_history = [
    {'role': 'user', 'content': 'Question 1'},
    {'role': 'assistant', 'content': 'Answer 1'},
    {'role': 'user', 'content': 'Question 2'},
    {'role': 'assistant', 'content': 'Answer 2'},
    ...
]
```

**Benefits**:
- Follow-up questions work naturally
- Context preserved across messages
- Efficient memory usage
- Can be cleared via "Limpiar" button

### System Prompts

Add custom system instructions per query:

```javascript
{
    "message": "¿Cuál es el estado de los contratos?",
    "system_prompt": "Eres un asistente legal experto. Responde en formato de lista."
}
```

### Response Features

**Markdown Support**: Responses rendered with:
- **Bold text**
- *Italic text*
- Headers (H1, H2, H3)
- Lists (ordered and unordered)
- Code blocks
- Blockquotes
- Links

**Citations**: Each response includes:
- Source document titles
- Document URIs
- Relevant text chunks
- Citation count

**Loading Indicator**: Animated dots while generating response

---

## Metadata Filtering

### Overview

Filter RAG queries by document metadata for precise, targeted results.

### How to Use

**UI**:
1. Open "Filtros de Metadatos" section
2. Click "+ Agregar Filtro"
3. Enter key (e.g., "tipo")
4. Enter value (e.g., "contrato")
5. Click "Aplicar Filtros"

**API**:
```python
{
    "message": "¿Cuáles son los contratos activos?",
    "metadata_filters": [
        {"key": "tipo", "value": "contrato"},
        {"key": "estado", "value": "activo"}
    ]
}
```

### Filter Logic

**AND Logic**: All filters must match

Example:
```json
[
    {"key": "tipo", "value": "factura"},
    {"key": "departamento", "value": "IT"}
]
```

Only returns documents where:
- tipo = "factura" **AND**
- departamento = "IT"

### Filter Types

**String Filters**:
```json
{"key": "autor", "value": "Juan Perez"}
```

**Numeric Filters**:
```json
{"key": "importe", "value": 1500}
```

**Date Filters** (as strings):
```json
{"key": "fecha", "value": "2024-11-15"}
```

### Filter Format

Filters converted to Gemini format:

```python
# Input
{"key": "tipo", "value": "contrato"}

# Converted to
{
    "key": "chunk.custom_metadata.tipo",
    "conditions": [{
        "stringValue": "contrato",
        "operation": "EQUAL"
    }]
}
```

### Common Use Cases

**By Document Type**:
```json
[{"key": "tipo", "value": "informe"}]
```

**By Department**:
```json
[{"key": "departamento", "value": "Legal"}]
```

**By Date**:
```json
[{"key": "fecha", "value": "2024-11-15"}]
```

**By Status**:
```json
[{"key": "estado", "value": "activo"}]
```

**Combined**:
```json
[
    {"key": "tipo", "value": "contrato"},
    {"key": "departamento", "value": "Legal"},
    {"key": "estado", "value": "activo"}
]
```

### Benefits

- **Precision**: Only relevant documents retrieved
- **Performance**: Faster search on filtered subset
- **Control**: User decides scope of search
- **Flexibility**: Combine multiple filters

---

## File Search Store Management

### Overview

File Search Stores are persistent containers for document embeddings and metadata.

### Store Lifecycle

**Creation**:
- Automatic on first document upload
- Manual via `/create-store` endpoint

**Usage**:
- Upload documents
- Query with RAG
- Manage metadata

**Persistence**:
- Stores persist indefinitely
- Survive application restarts
- Saved to Gemini infrastructure

**Deletion**:
- Manual deletion only
- Removes all documents
- Cannot be undone

### Multiple Stores

Use multiple stores for different projects:

**Create**:
```python
POST /create-store
{
    "store_name": "Project-Alpha-Documents"
}
```

**Switch**:
```python
POST /switch-store
{
    "store_name": "fileSearchStores/project-alpha-xyz123"
}
```

**List**:
```python
GET /list-stores
```

### Store Information

Each store contains:
- **Name**: Unique identifier
- **Display Name**: Human-readable name
- **Create Time**: When created
- **Update Time**: Last modified
- **Document Counts**:
  - Active documents
  - Pending documents
  - Failed documents
- **Size**: Total bytes stored

### Best Practices

- **One store per project** for organization
- **Keep stores under 20GB** for optimal performance
- **Regular cleanup** of unused documents
- **Descriptive names** for easy identification

---

## Tab-Based Navigation

### Overview

Clean, intuitive interface with 4 tabs:

### 1. Chat Tab

**Features**:
- Document upload
- AI metadata suggestion
- RAG chat interface
- Metadata filtering
- Conversation history

**Use Cases**:
- Upload new documents
- Chat with documents
- Filter by metadata
- Review citations

### 2. Documentos Tab

**Features**:
- List all documents in current store
- View document metadata
- Edit metadata
- Delete documents

**Use Cases**:
- Audit uploaded documents
- Update metadata
- Remove outdated documents
- Check document states

### 3. File Stores Tab

**Features**:
- List all File Search stores
- View store statistics
- Switch between stores
- Delete stores

**Use Cases**:
- Manage multiple projects
- Monitor storage usage
- Switch contexts
- Clean up old stores

### 4. API Docs Tab

**Features**:
- API endpoint documentation
- Request/response examples
- cURL commands
- Interactive testing

**Use Cases**:
- Learn API usage
- Copy example code
- Test endpoints
- Integrate with other tools

---

## Citation & Grounding

### Overview

Every response includes citations showing which document chunks were used.

### How It Works

Gemini File Search returns `grounding_metadata`:

```python
{
    "grounding_chunks": [
        {
            "retrieved_context": {
                "title": "contract.pdf",
                "uri": "fileSearchStores/.../documents/doc1",
                "text": "This contract establishes..."
            }
        }
    ]
}
```

### Citation Display

**Response Format**:
```json
{
    "response": "According to the contract...",
    "metadata": {
        "citations": [
            {
                "title": "contract.pdf",
                "uri": "fileSearchStores/.../documents/doc1",
                "text": "This contract establishes..."
            }
        ],
        "citation_count": 1
    }
}
```

**UI Display**:
- Citation count shown
- Expandable citation details
- Document title as link
- Relevant text excerpt

### Benefits

- **Transparency**: See source of information
- **Verification**: Check accuracy
- **Trust**: Know response is grounded
- **Audit**: Track information sources

---

## State Persistence

### Overview

Application state persists across restarts using `store_state.json`.

### What's Persisted

**Store Information**:
- Current store name
- Store configuration

**Document Metadata**:
- Uploaded files list
- Custom metadata
- Upload timestamps
- Document IDs

**Metadata Edits**:
- Local metadata changes
- Metadata update timestamps

### File Format

```json
{
    "store_name": "fileSearchStores/rag-app-store-xyz123",
    "uploaded_files": [
        {
            "filename": "contract.pdf",
            "size": 524288,
            "uploaded_at": "2024-11-19 14:30:00",
            "custom_metadata": {
                "tipo": "contrato",
                "autor": "Juan Perez"
            },
            "document_id": "fileSearchStores/.../documents/doc1",
            "metadata_updated_at": "2024-11-19 15:00:00"
        }
    ]
}
```

### Hybrid Metadata Storage

**Gemini Metadata**: Stored with document in File Search Store

**Local Metadata**: Stored in `store_state.json`

**Merged View**: Local metadata overrides Gemini metadata

**Benefits**:
- Edit metadata without re-uploading
- Metadata edits persist locally
- Fast metadata updates
- Full metadata history

### Lifecycle

**On Upload**:
```python
save_state()  # Save after successful upload
```

**On Startup**:
```python
load_state()  # Restore previous state
```

**On Edit**:
```python
save_state()  # Save metadata changes
```

**On Delete**:
```python
save_state()  # Update state after deletion
```

---

## Future Features

### Planned Enhancements

**Version 1.1**:
- [ ] Multi-language UI (English)
- [ ] Batch document upload
- [ ] Export/import stores
- [ ] Advanced search operators

**Version 1.2**:
- [ ] User authentication
- [ ] Multi-user support
- [ ] Document versioning
- [ ] Audit logs

**Version 2.0**:
- [ ] Real-time collaboration
- [ ] Document comparison
- [ ] Analytics dashboard
- [ ] Webhook notifications

---

## Support

For feature requests:
- Check [GitHub Issues](https://github.com/yourusername/gemini-file-search-manager/issues)
- Create feature request with use case
- Vote on existing requests

For bugs:
- Report in [Issues](https://github.com/yourusername/gemini-file-search-manager/issues)
- Include steps to reproduce
- Provide environment details

---

**Features Documentation Complete**

See also:
- [README.md](README.md) - Project overview
- [API_REFERENCE.md](API_REFERENCE.md) - API documentation
- [INSTALLATION.md](INSTALLATION.md) - Setup guide
