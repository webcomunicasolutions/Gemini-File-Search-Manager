# API Reference

## 🌍 Available Languages

- [English](API_REFERENCE.md)
- [Español](API_REFERENCE_ES.md)

---

Complete API documentation for Gemini File Search Manager application endpoints.

## Table of Contents

- [Base URL](#base-url)
- [Authentication](#authentication)
- [Core Endpoints](#core-endpoints)
- [Store Management](#store-management)
- [Document Management](#document-management)
- [Utility Endpoints](#utility-endpoints)
- [Error Handling](#error-handling)
- [Rate Limits](#rate-limits)

---

## Base URL

```
http://localhost:5001
```

For production deployments, replace with your domain:
```
https://yourdomain.com
```

---

## Authentication

Currently, the application uses a single API key configured in `.env` or `app.py`. No per-request authentication is required for local deployments.

For production, consider adding:
- API key header validation
- JWT tokens
- OAuth 2.0

---

## Core Endpoints

### GET /

Serve main HTML interface.

**Request:**
```http
GET / HTTP/1.1
Host: localhost:5001
```

**Response:**
```html
<!DOCTYPE html>
<html lang="en">
...
</html>
```

---

### POST /upload

Upload document with optional metadata and chunking configuration.

**Request:**
```http
POST /upload HTTP/1.1
Host: localhost:5001
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="contract.pdf"
Content-Type: application/pdf

[binary data]
------WebKitFormBoundary
Content-Disposition: form-data; name="metadata"

{"tipo":"contrato","autor":"Juan Perez","fecha":"2024-11-15"}
------WebKitFormBoundary
Content-Disposition: form-data; name="chunking_config"

{"enabled":true,"max_tokens_per_chunk":500,"max_overlap_tokens":50}
------WebKitFormBoundary--
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | File | Yes | Document file (max 100MB) |
| `metadata` | JSON string | No | Custom metadata (max 20 fields) |
| `chunking_config` | JSON string | No | Chunking configuration |

**Metadata Format:**
```json
{
  "key1": "string_value",
  "key2": 123,
  "key3": "another_value"
}
```

**Chunking Config Format:**
```json
{
  "enabled": true,
  "max_tokens_per_chunk": 500,
  "max_overlap_tokens": 50
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "File 'contract.pdf' uploaded and processed successfully",
  "filename": "contract.pdf",
  "file_size": 524288,
  "store_name": "fileSearchStores/rag-app-store-xyz123",
  "document_id": "fileSearchStores/rag-app-store-xyz123/documents/doc-abc456",
  "uploaded_files": [
    {
      "filename": "contract.pdf",
      "size": 524288,
      "uploaded_at": "2024-11-19 14:30:00",
      "custom_metadata": {
        "tipo": "contrato",
        "autor": "Juan Perez",
        "fecha": "2024-11-15"
      },
      "chunking_config": {
        "enabled": true,
        "max_tokens_per_chunk": 500,
        "max_overlap_tokens": 50
      },
      "file_api_name": "files/temp-file-xyz",
      "document_id": "fileSearchStores/rag-app-store-xyz123/documents/doc-abc456"
    }
  ]
}
```

**Response (Error):**
```json
{
  "error": "File type not supported"
}
```

**Status Codes:**
- `200 OK` - Upload successful
- `400 Bad Request` - Invalid file or missing data
- `500 Internal Server Error` - Processing error

**Example (cURL):**
```bash
curl -X POST http://localhost:5001/upload \
  -F "file=@contract.pdf" \
  -F 'metadata={"tipo":"contrato","autor":"Juan Perez"}' \
  -F 'chunking_config={"enabled":true,"max_tokens_per_chunk":500}'
```

**Example (Python):**
```python
import requests
import json

files = {'file': open('contract.pdf', 'rb')}
data = {
    'metadata': json.dumps({
        'tipo': 'contrato',
        'autor': 'Juan Perez',
        'fecha': '2024-11-15'
    }),
    'chunking_config': json.dumps({
        'enabled': True,
        'max_tokens_per_chunk': 500,
        'max_overlap_tokens': 50
    })
}

response = requests.post('http://localhost:5001/upload', files=files, data=data)
print(response.json())
```

**Example (JavaScript):**
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('metadata', JSON.stringify({
    tipo: 'contrato',
    autor: 'Juan Perez',
    fecha: '2024-11-15'
}));

const response = await fetch('/upload', {
    method: 'POST',
    body: formData
});

const data = await response.json();
console.log(data);
```

---

### POST /suggest-metadata

AI-powered metadata extraction from document content.

**Request:**
```http
POST /suggest-metadata HTTP/1.1
Host: localhost:5001
Content-Type: multipart/form-data

[file binary data]
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | File | Yes | Document for analysis |

**Response (Success):**
```json
{
  "success": true,
  "metadata": {
    "titulo": "Contrato de Servicios Profesionales - Consultoría IT",
    "tipo": "contrato",
    "partes": "Empresa XYZ y Consultor ABC",
    "fecha_firma": "2024-11-15",
    "vigencia_hasta": "2025-11-14",
    "valor_contrato": 50000,
    "area": "Tecnología",
    "estado": "activo",
    "departamento": "IT",
    "confidencialidad": "confidencial",
    "tags": "it, consultoria, servicios, tecnologia"
  },
  "filename": "contract.pdf"
}
```

**Response (Error):**
```json
{
  "error": "Error analyzing document",
  "details": "Could not parse JSON: Expecting value: line 1 column 1 (char 0)"
}
```

**Status Codes:**
- `200 OK` - Analysis successful
- `400 Bad Request` - No file provided
- `500 Internal Server Error` - Analysis failed

**Example (cURL):**
```bash
curl -X POST http://localhost:5001/suggest-metadata \
  -F "file=@invoice.pdf"
```

**Example (Python):**
```python
import requests

files = {'file': open('invoice.pdf', 'rb')}
response = requests.post('http://localhost:5001/suggest-metadata', files=files)
metadata = response.json()['metadata']
print(metadata)
```

**Example (JavaScript):**
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const response = await fetch('/suggest-metadata', {
    method: 'POST',
    body: formData
});

const {metadata} = await response.json();
console.log(metadata);
```

**Notes:**
- Uses `gemini-2.0-flash-exp` model
- Temperature set to 0.1 for consistency
- Maximum 20 metadata fields returned (Gemini API limit)
- Temporary file deleted after analysis
- Processing time: 5-15 seconds depending on file size

---

### POST /chat

RAG-powered chat with optional metadata filtering.

**Request:**
```http
POST /chat HTTP/1.1
Host: localhost:5001
Content-Type: application/json

{
  "message": "¿Cuáles son los contratos activos?",
  "metadata_filters": [
    {"key": "tipo", "value": "contrato"},
    {"key": "estado", "value": "activo"}
  ],
  "system_prompt": "Eres un asistente legal experto."
}
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message` | string | Yes | User question or message |
| `metadata_filters` | array | No | Metadata filters (AND logic) |
| `system_prompt` | string | No | Custom system instruction |

**Metadata Filter Format:**
```json
[
  {"key": "field_name", "value": "string_or_number"}
]
```

**Response (Success):**
```json
{
  "success": true,
  "response": "Según los documentos indexados, existen 3 contratos activos:\n\n1. **Contrato de Servicios IT** - Empresa XYZ, vigente hasta 2025-11-14\n2. **Contrato de Consultoría** - Consultor ABC, vigente hasta 2025-06-30\n3. **Contrato Marco** - Proveedor Cloud, vigente hasta 2026-12-31",
  "metadata": {
    "citations": [
      {
        "title": "Contrato de Servicios IT",
        "uri": "fileSearchStores/.../documents/doc1",
        "text": "Este contrato establece..."
      },
      {
        "title": "Contrato de Consultoría",
        "uri": "fileSearchStores/.../documents/doc2",
        "text": "Las partes acuerdan..."
      }
    ],
    "citation_count": 2
  },
  "conversation_length": 2,
  "metadata_filters_applied": [
    {"key": "tipo", "value": "contrato"},
    {"key": "estado", "value": "activo"}
  ],
  "filters_count": 2
}
```

**Response (Error):**
```json
{
  "error": "Please upload a file first"
}
```

**Status Codes:**
- `200 OK` - Response generated
- `400 Bad Request` - No message provided or no store
- `500 Internal Server Error` - Generation error

**Example (cURL):**
```bash
curl -X POST http://localhost:5001/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Qué dice el informe?",
    "metadata_filters": [{"key": "tipo", "value": "informe"}]
  }'
```

**Example (Python):**
```python
import requests

payload = {
    'message': '¿Cuáles son los contratos activos?',
    'metadata_filters': [
        {'key': 'tipo', 'value': 'contrato'},
        {'key': 'estado', 'value': 'activo'}
    ]
}

response = requests.post('http://localhost:5001/chat', json=payload)
data = response.json()
print(data['response'])
print(f"Citations: {data['metadata']['citation_count']}")
```

**Example (JavaScript):**
```javascript
const response = await fetch('/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        message: '¿Qué dice el informe?',
        metadata_filters: [
            {key: 'tipo', value: 'informe'},
            {key: 'departamento', value: 'IT'}
        ]
    })
});

const data = await response.json();
console.log(data.response);
```

**Notes:**
- Maintains conversation history (last 7 message pairs)
- Uses `gemini-2.5-flash` model
- Metadata filters use AND logic (all must match)
- Numeric and string values supported
- Citations extracted from `grounding_metadata`

---

### POST /clear

Clear conversation history.

**Request:**
```http
POST /clear HTTP/1.1
Host: localhost:5001
```

**Response:**
```json
{
  "success": true,
  "message": "Conversation cleared"
}
```

**Example (cURL):**
```bash
curl -X POST http://localhost:5001/clear
```

---

## Store Management

### GET /list-stores

List all File Search stores with their documents.

**Request:**
```http
GET /list-stores HTTP/1.1
Host: localhost:5001
```

**Response:**
```json
{
  "success": true,
  "stores": [
    {
      "name": "fileSearchStores/rag-app-store-xyz123",
      "display_name": "RAG-App-Store",
      "displayName": "RAG-App-Store",
      "create_time": "2024-11-19T10:00:00.000Z",
      "createTime": "2024-11-19T10:00:00.000Z",
      "active_documents_count": 5,
      "activeDocumentsCount": 5,
      "pending_documents_count": 0,
      "pendingDocumentsCount": 0,
      "failed_documents_count": 0,
      "failedDocumentsCount": 0,
      "documents": [
        {
          "name": "fileSearchStores/.../documents/doc1",
          "display_name": "contract.pdf",
          "displayName": "contract.pdf",
          "state": "STATE_ACTIVE",
          "size_bytes": 524288,
          "sizeBytes": 524288,
          "mime_type": "application/pdf",
          "mimeType": "application/pdf",
          "create_time": "2024-11-19T10:05:00.000Z",
          "createTime": "2024-11-19T10:05:00.000Z",
          "custom_metadata": {
            "tipo": "contrato",
            "autor": "Juan Perez"
          },
          "customMetadata": {
            "tipo": "contrato",
            "autor": "Juan Perez"
          }
        }
      ]
    }
  ],
  "count": 1,
  "current_store": "fileSearchStores/rag-app-store-xyz123"
}
```

**Example (Python):**
```python
response = requests.get('http://localhost:5001/list-stores')
stores = response.json()['stores']

for store in stores:
    print(f"{store['displayName']}: {store['activeDocumentsCount']} documents")
```

---

### GET /store-info

Get current store information.

**Request:**
```http
GET /store-info HTTP/1.1
Host: localhost:5001
```

**Response (Store exists):**
```json
{
  "success": true,
  "store_exists": true,
  "name": "fileSearchStores/rag-app-store-xyz123",
  "display_name": "RAG-App-Store",
  "create_time": "2024-11-19T10:00:00.000Z",
  "update_time": "2024-11-19T14:30:00.000Z",
  "document_count": 5
}
```

**Response (No store):**
```json
{
  "success": true,
  "store_exists": false,
  "message": "No file search store created yet"
}
```

---

### POST /switch-store

Switch to a different File Search store.

**Request:**
```http
POST /switch-store HTTP/1.1
Host: localhost:5001
Content-Type: application/json

{
  "store_name": "fileSearchStores/project-alpha-xyz456"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Switched to store: fileSearchStores/project-alpha-xyz456",
  "store_name": "fileSearchStores/project-alpha-xyz456"
}
```

---

### DELETE /delete-store

Delete the current File Search store and all its documents.

**Request:**
```http
DELETE /delete-store HTTP/1.1
Host: localhost:5001
```

**Response:**
```json
{
  "success": true,
  "message": "File search store deleted successfully"
}
```

**Warning**: This permanently deletes the store and all documents. Cannot be undone.

---

## Document Management

### GET /current-store-documents

Get all documents from the current store with metadata.

**Request:**
```http
GET /current-store-documents HTTP/1.1
Host: localhost:5001
```

**Response:**
```json
{
  "success": true,
  "documents": [
    {
      "name": "fileSearchStores/.../documents/doc1",
      "display_name": "contract.pdf",
      "displayName": "contract.pdf",
      "state": "STATE_ACTIVE",
      "size_bytes": 524288,
      "sizeBytes": 524288,
      "mime_type": "application/pdf",
      "mimeType": "application/pdf",
      "create_time": "2024-11-19T10:05:00.000Z",
      "createTime": "2024-11-19T10:05:00.000Z",
      "custom_metadata": {
        "tipo": "contrato",
        "autor": "Juan Perez",
        "fecha": "2024-11-15"
      },
      "customMetadata": {
        "tipo": "contrato",
        "autor": "Juan Perez",
        "fecha": "2024-11-15"
      }
    }
  ],
  "store_name": "fileSearchStores/rag-app-store-xyz123",
  "store_display_name": "RAG-App-Store"
}
```

---

### GET /files

Get uploaded files list (from local state).

**Request:**
```http
GET /files HTTP/1.1
Host: localhost:5001
```

**Response:**
```json
{
  "success": true,
  "files": [
    {
      "filename": "contract.pdf",
      "size": 524288,
      "uploaded_at": "2024-11-19 14:30:00",
      "custom_metadata": {
        "tipo": "contrato",
        "autor": "Juan Perez"
      },
      "document_id": "fileSearchStores/.../documents/doc1"
    }
  ],
  "store_name": "fileSearchStores/rag-app-store-xyz123"
}
```

---

### DELETE /delete-document

Delete a specific document from a store.

**Request:**
```http
DELETE /delete-document HTTP/1.1
Host: localhost:5001
Content-Type: application/json

{
  "document_name": "fileSearchStores/rag-app-store-xyz123/documents/doc1"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Document deleted successfully",
  "document_name": "fileSearchStores/.../documents/doc1"
}
```

---

### POST /update-document-metadata

Update metadata for a specific document.

**Request:**
```http
POST /update-document-metadata HTTP/1.1
Host: localhost:5001
Content-Type: application/json

{
  "document_name": "fileSearchStores/rag-app-store-xyz123/documents/doc1",
  "metadata": {
    "tipo": "contrato",
    "autor": "Juan Perez Updated",
    "fecha": "2024-11-20",
    "estado": "revisado"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Metadata updated successfully",
  "document_name": "fileSearchStores/.../documents/doc1",
  "metadata": {
    "tipo": "contrato",
    "autor": "Juan Perez Updated",
    "fecha": "2024-11-20",
    "estado": "revisado"
  }
}
```

**Note**: Updates are saved to local `store_state.json` and merged with Gemini metadata.

---

## Utility Endpoints

### GET /status

Get application status.

**Response:**
```json
{
  "file_uploaded": true,
  "conversation_length": 4,
  "store_name": "fileSearchStores/rag-app-store-xyz123",
  "uploaded_files": [...]
}
```

---

### GET /api-info

Get API information for documentation tab.

**Response:**
```json
{
  "success": true,
  "api_key": "AIza...",
  "store_exists": true,
  "store_name": "fileSearchStores/rag-app-store-xyz123",
  "store_display_name": "RAG-App-Store",
  "file_count": 5,
  "files": [...],
  "model": "gemini-2.5-flash",
  "metadata_keys": ["tipo", "autor", "fecha", "estado"]
}
```

---

### POST /update-api-key

Update Gemini API key.

**Request:**
```json
{
  "api_key": "new_api_key_here"
}
```

**Response:**
```json
{
  "success": true,
  "message": "API key updated successfully. Please reload the page."
}
```

---

## Error Handling

### Error Response Format

All errors follow this format:

```json
{
  "error": "Error message description",
  "details": "Optional detailed error information"
}
```

### Common Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error - Processing failed |

### Example Error Responses

**File too large:**
```json
{
  "error": "File size exceeds maximum allowed (100MB)"
}
```

**Invalid metadata:**
```json
{
  "error": "Metadata must be valid JSON"
}
```

**Store not found:**
```json
{
  "error": "Store not found: fileSearchStores/invalid-store"
}
```

---

## Rate Limits

### Gemini API Limits

Limits depend on your Gemini API tier:

**Free Tier:**
- 60 requests per minute
- 1500 requests per day

**Paid Tiers:**
- Higher limits based on tier
- Contact Google for enterprise limits

### Application Limits

- **Max file size**: 100 MB
- **Max metadata fields**: 20 per document
- **Conversation history**: 7 message pairs
- **Max query results**: 100 chunks

### Best Practices

1. **Implement retry logic** for transient errors
2. **Cache responses** when possible
3. **Batch operations** to reduce API calls
4. **Monitor usage** to stay within limits

---

## WebSocket Support (Future)

WebSocket support is planned for real-time updates:

```javascript
const ws = new WebSocket('ws://localhost:5001/ws');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'upload_progress') {
        console.log(`Upload ${data.progress}% complete`);
    }
};
```

---

## Versioning

Current API version: **v1**

Future versions will be accessible via URL:
```
http://localhost:5001/api/v2/chat
```

---

## SDK Examples

### Python SDK Wrapper

```python
class GeminiRAGClient:
    def __init__(self, base_url='http://localhost:5001'):
        self.base_url = base_url

    def upload(self, file_path, metadata=None):
        files = {'file': open(file_path, 'rb')}
        data = {'metadata': json.dumps(metadata)} if metadata else {}
        response = requests.post(f'{self.base_url}/upload', files=files, data=data)
        return response.json()

    def chat(self, message, filters=None):
        payload = {'message': message}
        if filters:
            payload['metadata_filters'] = filters
        response = requests.post(f'{self.base_url}/chat', json=payload)
        return response.json()

# Usage
client = GeminiRAGClient()
result = client.upload('document.pdf', {'tipo': 'informe'})
response = client.chat('¿Qué dice el documento?')
print(response['response'])
```

---

## Support

For API questions:
- Review this documentation
- Check [GitHub Issues](https://github.com/yourusername/gemini-file-search-manager/issues)
- Create new issue with API endpoint details

---

**API Reference Complete**

For more information, see:
- [README.md](README.md) - Project overview
- [FEATURES.md](FEATURES.md) - Feature details
- [INSTALLATION.md](INSTALLATION.md) - Setup guide
