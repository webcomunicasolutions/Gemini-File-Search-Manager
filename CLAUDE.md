# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository is focused on implementing Retrieval Augmented Generation (RAG) using Google's Gemini File Search API. The File Search tool enables semantic search capabilities by chunking, embedding, and indexing documents to provide grounded responses from the Gemini model.

## Key Concepts

### File Search Architecture
The File Search system follows a three-step process:
1. **Create a File Search store**: A persistent container for document embeddings
2. **Upload and import files**: Files are chunked, embedded using `gemini-embedding-001`, and indexed
3. **Query with File Search**: The model performs semantic search on the store to ground responses

### Two Upload Approaches
- **Direct upload**: Use `uploadToFileSearchStore` to simultaneously upload and import files
- **Separate upload and import**: Use Files API to upload, then `importFile` to import into the store

### Important Implementation Details
- Raw files uploaded via Files API are deleted after 48 hours
- File Search store data persists indefinitely until manually deleted
- File Search store names are globally scoped
- Default model: `gemini-2.5-flash` or `gemini-2.5-pro`
- Embedding model: `gemini-embedding-001`

## API Patterns

### Python Client Pattern
```python
from google import genai
from google.genai import types
import time

client = genai.Client()

# Operations require polling until operation.done is True
while not operation.done:
    time.sleep(5)
    operation = client.operations.get(operation)
```

### JavaScript Client Pattern
```javascript
const { GoogleGenAI } = require('@google/genai');
const ai = new GoogleGenAI({});

// Operations require polling until operation.done is true
while (!operation.done) {
    await new Promise(resolve => setTimeout(resolve, 5000));
    operation = await ai.operations.get({ operation });
}
```

## Advanced Features

### Chunking Configuration
Use `chunking_config` with `white_space_config` to control:
- `max_tokens_per_chunk`: Maximum tokens per chunk
- `max_overlap_tokens`: Overlapping tokens between chunks

### Metadata Filtering
Add custom metadata (key-value pairs) to files for filtering:
- String values: `{ key: "author", string_value: "..." }`
- Numeric values: `{ key: "year", numeric_value: 1934 }`
- Filter syntax follows google.aip.dev/160

### Citations and Grounding
Access citation information through `response.candidates[0].grounding_metadata` to verify which document chunks were used.

## File Support

File Search supports specific file formats through MIME types. See [SUPPORTED_FORMATS.md](SUPPORTED_FORMATS.md) for the complete list.

### Summary

**Application File Types (30 MIME types):**
- Documents: PDF, Word (.doc, .docx), Excel, PowerPoint, ODT
- Code/Data: JSON, XML, SQL, Dart, TypeScript, Java, PHP
- Other: LaTeX, Jupyter notebooks, Shell scripts, ZIP archives

**Text File Types (170 MIME types):**
- Web: HTML, CSS, JavaScript, JSX, TypeScript, TSX
- Programming: Python, Java, C/C++, C#, Go, Rust, Swift, Kotlin, Scala, Ruby, Perl, R, Haskell, Erlang, Lisp, Lua
- Data: CSV, TSV, plain text, YAML
- Markup: Markdown, XML, RST, SGML, Turtle, N3
- Other: RTF, vCard, calendar formats

### Common File Extensions

- **Documents**: `.pdf`, `.doc`, `.docx`, `.odt`, `.rtf`
- **Spreadsheets**: `.xls`, `.xlsx`, `.ods`, `.csv`, `.tsv`
- **Presentations**: `.ppt`, `.pptx`, `.odp`
- **Code**: `.py`, `.js`, `.ts`, `.java`, `.c`, `.cpp`, `.cs`, `.go`, `.rs`, `.php`, `.rb`, `.swift`, `.kt`, `.scala`, `.pl`, `.r`, `.hs`, `.erl`, `.lisp`, `.lua`, `.sh`
- **Markup**: `.md`, `.html`, `.xml`, `.rst`, `.tex`
- **Data**: `.json`, `.yaml`, `.yml`, `.sql`, `.csv`, `.tsv`, `.txt`
- **Notebooks**: `.ipynb`
- **Archives**: `.zip`

### Limitations

- **Maximum file size**: 100 MB per document
- **Recommended**: Keep each File Search store under 20 GB for optimal latency
- **Total storage**: Varies by tier (Free: 1GB, Tier 1: 10GB, Tier 2: 100GB, Tier 3: 1TB)

## Rate Limits and Pricing

### Limits
- Max file size: 100 MB per document
- Total File Search store size varies by tier (Free: 1GB, Tier 1: 10GB, Tier 2: 100GB, Tier 3: 1TB)
- Recommended: Keep each store under 20GB for optimal latency
- Backend computed size ≈ 3x input data size (includes embeddings)

### Pricing
- Embeddings at indexing: $0.15 per 1M tokens
- Storage: Free
- Query-time embeddings: Free
- Retrieved document tokens: Charged as regular context tokens

## REST API Reference

### Base URL
`https://generativelanguage.googleapis.com/v1beta`

### FileSearchStore Endpoints

**Create Store**
- `POST /fileSearchStores`
- Request body: `{ "displayName": "optional-name" }`
- Response: FileSearchStore resource

**List Stores**
- `GET /fileSearchStores`
- Query params: `pageSize` (max 20), `pageToken`
- Response: Paginated list with `nextPageToken`

**Get Store**
- `GET /fileSearchStores/{filesearchstore}`
- Response: FileSearchStore with metrics

**Delete Store**
- `DELETE /fileSearchStores/{filesearchstore}?force=true`
- Query param `force=true` deletes all documents and related objects

**Upload to Store**
- `POST /fileSearchStores/{filesearchstore}:uploadToFileSearchStore`
- Upload URI: `https://generativelanguage.googleapis.com/upload/v1beta/{fileSearchStoreName}:uploadToFileSearchStore`
- Request body: `displayName`, `customMetadata`, `chunkingConfig`, `mimeType`
- Response: Long-running Operation

**Import File**
- `POST /fileSearchStores/{filesearchstore}:importFile`
- Request body: `fileName`, `customMetadata`, `chunkingConfig`
- Response: Long-running Operation

### Document Endpoints

**List Documents**
- `GET /fileSearchStores/{filesearchstore}/documents`
- Query params: `pageSize` (max 20), `pageToken`
- Response: Paginated list sorted by `createTime`

**Get Document**
- `GET /fileSearchStores/{filesearchstore}/documents/{document}`
- Response: Document resource with state

**Delete Document**
- `DELETE /fileSearchStores/{filesearchstore}/documents/{document}?force=true`
- Query param `force=true` deletes all chunks and related objects

**Query Document (Semantic Search)**
- `POST /fileSearchStores/{filesearchstore}/documents/{document}:query`
- Request body: `query` (string), `resultsCount` (max 100), `metadataFilters`
- Response: List of relevant chunks

### Operations (Long-Running)

**Get Operation Status**
- `GET /fileSearchStores/{filesearchstore}/operations/{operation}`
- `GET /fileSearchStores/{filesearchstore}/upload/operations/{operation}`
- Poll until `done: true`, then check `error` or `response`

## Resource Structures

### FileSearchStore Resource
```json
{
  "name": "fileSearchStores/my-store-123",
  "displayName": "My Store",
  "createTime": "2024-01-01T00:00:00Z",
  "updateTime": "2024-01-02T00:00:00Z",
  "activeDocumentsCount": "10",
  "pendingDocumentsCount": "2",
  "failedDocumentsCount": "0",
  "sizeBytes": "1048576"
}
```

Key fields:
- `name`: Globally unique, output-only (40 char max: lowercase alphanumeric or dashes)
- `displayName`: Optional, human-readable (512 char max)
- `activeDocumentsCount`: Documents ready for retrieval
- `pendingDocumentsCount`: Documents being processed
- `failedDocumentsCount`: Documents that failed processing
- `sizeBytes`: Total raw bytes ingested

### Document Resource
```json
{
  "name": "fileSearchStores/{store}/documents/{doc}",
  "displayName": "My Document",
  "customMetadata": [
    { "key": "author", "stringValue": "..." },
    { "key": "year", "numericValue": 2024 }
  ],
  "state": "STATE_ACTIVE",
  "sizeBytes": "102400",
  "mimeType": "application/pdf",
  "createTime": "2024-01-01T00:00:00Z",
  "updateTime": "2024-01-02T00:00:00Z"
}
```

Document states:
- `STATE_UNSPECIFIED`: Default/omitted value
- `STATE_PENDING`: Chunks being processed (embedding and storage)
- `STATE_ACTIVE`: All chunks processed and ready for querying
- `STATE_FAILED`: Some chunks failed processing

Document constraints:
- Maximum 20 CustomMetadata items per document
- `displayName` max 512 characters
- `name` ID max 40 characters (lowercase alphanumeric or dashes)

### Operation Resource
```json
{
  "name": "operations/{unique_id}",
  "done": false,
  "metadata": { "@type": "...", ... },
  "response": { "@type": "...", ... },
  "error": { "code": 0, "message": "..." }
}
```

Polling pattern:
- Check `done` field
- If `done == true`, check either `error` or `response` (exactly one will be set)
- Poll at recommended intervals (5 seconds typical)

## Advanced Query Features

### Metadata Filtering in Queries
Metadata filters use logical AND between different keys, OR for same key:

**Numeric ranges** (AND supported for same key):
```json
{
  "metadataFilters": [
    { "key": "chunk.custom_metadata.year", "conditions": [
      { "intValue": 2015, "operation": "GREATER" }
    ]},
    { "key": "chunk.custom_metadata.year", "conditions": [
      { "intValue": 2020, "operation": "LESS_EQUAL" }
    ]}
  ]
}
```

**String values** (only OR supported for same key):
```json
{
  "metadataFilters": [
    { "key": "chunk.custom_metadata.genre", "conditions": [
      { "stringValue": "drama", "operation": "EQUAL" },
      { "stringValue": "action", "operation": "EQUAL" }
    ]}
  ]
}
```

### Direct Document Query
Use `documents.query` for semantic search on a specific document:
- Returns relevant chunks without full generation
- Useful for retrieval-only use cases
- Max 100 results per query (default 10)
- Supports metadata filtering at chunk level

## Pagination Pattern

All list operations support pagination:
- Set `pageSize` (max 20 per page)
- Use `nextPageToken` from response in next request
- All other parameters must match between paginated requests
- Results sorted by `createTime` ascending

## File Search Store Management

### Important Notes
- File Search stores persist indefinitely until manually deleted
- Temporary `File` objects (from Files API) are deleted after 48 hours
- Use `force: true` when deleting stores/documents with children
- Store names are globally unique and output-only (auto-generated from displayName)
- Name format: `fileSearchStores/{id}` where {id} is derived from displayName + 12-char random suffix

---

## Implementation Notes - Gemini File Search Manager Flask Application

### Project Structure

This implementation consists of:
- **Backend**: Flask application (`web_app/app.py`) - 1013 lines
- **Frontend**: Single-page application (`web_app/templates/index.html`) - 1600+ lines
- **State**: JSON persistence (`web_app/store_state.json`)

### Key Features Implemented

#### 1. AI Metadata Suggestion System (lines 769-914 in app.py)

**Innovative Feature**: Gemini 2.0 Flash analyzes documents and automatically suggests metadata.

**Endpoint**: `POST /suggest-metadata`

**Implementation Details**:
```python
model='gemini-2.0-flash-exp'  # Experimental model for better analysis
temperature=0.1  # Low for consistency
system_instruction=expert_prompt  # Detailed prompt for metadata extraction
```

**System Prompt** (lines 794-832):
- Expert identity: Document analysis specialist for RAG systems
- Extraction rules: Max 20 fields, lowercase with underscores
- Universal metadata: titulo (from content, NOT filename), tipo, fecha, autor, etc.
- Document type detection: factura, contrato, informe, manual, email, etc.

**Key Feature**: "titulo" field extracted from document CONTENT, not filename

**Process**:
1. Upload file to Gemini Files API temporarily
2. Send to model with system instruction
3. Parse JSON response (handles markdown blocks)
4. Delete temporary file
5. Return metadata to client

**Error Handling**:
- JSON parsing errors caught
- Temporary file cleanup even on failure
- Detailed logging of responses

#### 2. Metadata Templates (lines 1166-1239 in index.html)

**8 Pre-configured Templates**:
1. factura - Invoice fields
2. contrato - Contract fields
3. informe - Report fields
4. manual - Manual fields
5. presentacion - Presentation fields
6. acta - Meeting minutes fields
7. certificado - Certificate fields
8. email - Email fields

**All templates include**: `titulo` as first field (extracted by AI from content)

**Format**:
```javascript
factura: [
    { key: 'titulo', value: '', type: 'string' },
    { key: 'tipo', value: 'factura', type: 'string' },
    { key: 'numero_factura', value: '', type: 'string' },
    // ... more fields
]
```

#### 3. Tab-Based Navigation Architecture

**4 Tabs Implemented**:
1. **Chat Tab**: Upload, AI metadata, chat, filtering
2. **Documentos Tab**: List, view, edit, delete documents
3. **File Stores Tab**: List, switch, manage stores
4. **API Docs Tab**: Auto-generated documentation with cURL examples

**Implementation**:
- Pure JavaScript event handlers
- No frameworks used
- Clean tab switching logic
- State preserved across tabs

#### 4. Hybrid Metadata Storage System

**Two Storage Locations**:

**Gemini Metadata** (with document in File Search Store):
- Stored at upload time
- Immutable without re-upload
- Queried via File Search API

**Local Metadata** (`store_state.json`):
- Editable anytime
- Persists across restarts
- Merged with Gemini metadata

**Merge Logic**:
```python
# Gemini metadata fetched from API
gemini_metadata = {...}

# Local metadata from store_state.json
local_metadata = uploaded_files[i]['custom_metadata']

# Local overrides Gemini
final_metadata = {**gemini_metadata, **local_metadata}
```

**Benefits**:
- Edit metadata without re-uploading
- Fast metadata updates
- Persistence across sessions

#### 5. Upload Timeout Configuration (line 182 in app.py)

**Increased Timeout**: 120 seconds (2 minutes)

**Reason**: Large files take time to:
- Upload to Files API
- Import to File Search Store
- Chunk documents
- Embed chunks
- Index in vector database

**Progress Logging** (lines 188-189):
```python
if wait_time % 15 == 0:
    logger.info(f"Still waiting... ({wait_time}s elapsed)")
```

**Configurable**:
```python
max_wait = 120  # Can be increased if needed
```

#### 6. Conversation History Management (lines 263-270, 362-364)

**Limit**: 7 message pairs (MAX_HISTORY = 7)

**Reason**:
- Balance context vs token usage
- Prevent context window overflow
- Maintain conversation flow

**Implementation**:
```python
# Add messages
conversation_history.append({'role': 'user', 'content': message})
conversation_history.append({'role': 'assistant', 'content': response})

# Trim to last 7 pairs
if len(conversation_history) > MAX_HISTORY:
    conversation_history = conversation_history[-MAX_HISTORY:]
```

**Context Building** (lines 269-288):
```python
context_messages = conversation_history[-MAX_HISTORY:]
for msg in context_messages[:-1]:
    if msg['role'] == 'user':
        prompt_parts.append(f"User: {msg['content']}")
    else:
        prompt_parts.append(f"Assistant: {msg['content']}")
```

#### 7. Metadata Filtering Implementation (lines 300-343 in app.py)

**Frontend Format**:
```javascript
[
    {key: 'tipo', value: 'contrato'},
    {key: 'estado', value: 'activo'}
]
```

**Backend Conversion to Gemini Format**:
```python
gemini_filters = []
for filter_item in metadata_filters:
    filter_condition = {
        'key': f'chunk.custom_metadata.{key}',
        'conditions': []
    }

    if is_numeric:
        filter_condition['conditions'].append({
            'numericValue': numeric_value,
            'operation': 'EQUAL'
        })
    else:
        filter_condition['conditions'].append({
            'stringValue': str(value),
            'operation': 'EQUAL'
        })

    gemini_filters.append(filter_condition)
```

**Logic**: AND between different keys (all must match)

#### 8. State Persistence System

**File**: `store_state.json`

**Structure**:
```json
{
    "store_name": "fileSearchStores/rag-app-store-xyz123",
    "uploaded_files": [
        {
            "filename": "contract.pdf",
            "size": 524288,
            "uploaded_at": "2024-11-19 14:30:00",
            "custom_metadata": {...},
            "document_id": "fileSearchStores/.../documents/doc1",
            "metadata_updated_at": "2024-11-19 15:00:00"
        }
    ]
}
```

**Functions**:
- `load_state()` (lines 51-72): Load on startup
- `save_state()` (lines 73-84): Save after changes

**Called After**:
- Document upload (line 213)
- Store deletion (line 568)
- Document deletion (line 712)
- Metadata update (line 755)
- Store switch (line 677)

#### 9. Citation Extraction (lines 366-392 in app.py)

**Source**: `response.candidates[0].grounding_metadata`

**Extraction**:
```python
citations = []
if hasattr(grounding, 'grounding_chunks'):
    for chunk in grounding.grounding_chunks:
        if hasattr(chunk, 'retrieved_context'):
            ctx = chunk.retrieved_context
            citation = {
                'title': ctx.title,
                'uri': ctx.uri,
                'text': ctx.text
            }
            citations.append(citation)
```

**Response Format**:
```json
{
    "response": "According to the documents...",
    "metadata": {
        "citations": [...],
        "citation_count": 3
    }
}
```

#### 10. Store Management Features

**Create Store** (lines 137-141):
```python
file_search_store = client.file_search_stores.create(
    config={'display_name': 'RAG-App-Store'}
)
```

**List All Stores** (lines 476-547):
- Fetches all stores
- Includes document counts
- Merges Gemini + local metadata
- Returns current store indicator

**Switch Stores** (lines 657-690):
- Validates store exists
- Updates global state
- Clears uploaded_files list
- Saves to persistence

**Delete Store** (lines 549-577):
- Uses `force=True` to delete all documents
- Resets global state
- Saves to persistence

### Technical Decisions

#### Why Flask?

- **Lightweight**: Minimal overhead
- **Flexible**: Easy to customize
- **Python**: Same language as Gemini SDK
- **Simple**: No complex framework magic

#### Why Vanilla JavaScript?

- **No dependencies**: Faster load times
- **Full control**: Custom implementation
- **Educational**: Easy to understand
- **Portable**: Works anywhere

#### Why JSON Persistence?

- **Simple**: No database required
- **Portable**: Easy to backup
- **Readable**: Human-readable format
- **Fast**: Small files, quick I/O

### Performance Optimizations

#### 1. Timeout Handling
- 120-second timeout for large files
- Progress logging every 15 seconds
- Graceful error messages

#### 2. Conversation Pruning
- Limit to 7 message pairs
- Prevents context overflow
- Maintains relevance

#### 3. Metadata Caching
- Local storage in JSON
- Reduces API calls
- Faster metadata retrieval

### Security Considerations

**Current Implementation** (Development):
- API key in `.env` file
- Single-user application
- No authentication

**Production Recommendations**:
- Move API key to environment variables
- Add user authentication
- Implement API rate limiting
- Add CORS restrictions
- Use HTTPS only
- Sanitize file uploads
- Validate metadata inputs

### Known Limitations

1. **Max metadata fields**: 20 (Gemini API limit)
2. **Max file size**: 100 MB
3. **Single API key**: No multi-user support
4. **No batch upload**: One file at a time
5. **No document versioning**: Overwrite only
6. **No undo**: Deletions permanent

### Future Enhancements

See [README.md](README.md) Roadmap section for planned features.

### Community Documentation

**Comprehensive Docs Created**:
- README.md - Project overview with features, quick start, examples
- INSTALLATION.md - Detailed setup guide with troubleshooting
- API_REFERENCE.md - Complete API documentation with examples
- FEATURES.md - In-depth feature explanations and use cases
- CONTRIBUTING.md - Contribution guidelines and code style
- LICENSE - MIT License for open source

**Documentation Philosophy**:
- Clear and comprehensive
- Code examples in multiple languages
- Real-world use cases
- Troubleshooting sections
- Professional formatting

### For Future Claude Sessions

When working on this project:

1. **Read app.py first**: Understand Flask endpoints and logic
2. **Check store_state.json**: See current state
3. **Review index.html**: Understand frontend implementation
4. **Test locally**: Always test changes before committing
5. **Update docs**: Keep documentation in sync with code
6. **Follow style**: Maintain existing code patterns
