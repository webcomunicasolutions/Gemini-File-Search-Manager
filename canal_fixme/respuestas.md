# Respuestas del proyecto Gemini RAG

## 22/03/2026 - Gestion completa de File Stores

Aqui tienes todo lo que hace nuestro Manager con stores y documentos:

### Acciones sobre STORES

| Accion | Endpoint | SDK Method | UI |
|--------|----------|------------|-----|
| Listar todos | GET /stores | `client.file_search_stores.list()` | Cards con nombre, docs count, size, fecha |
| Crear nuevo | POST /create-store | `client.file_search_stores.create(config={'display_name': name})` | Input + boton en Upload tab |
| Borrar store | DELETE /delete-store | `client.file_search_stores.delete(name=store_name, config={'force': True})` | Boton rojo con confirmacion |
| Cambiar store activo | POST /switch-store | `client.file_search_stores.get(name=store_name)` | Click en card del store |
| Ver info store | GET /store-info | `client.file_search_stores.get(name=store_name)` | Muestra active/pending/failed docs, size |
| Ver uso total | GET /storage-usage | Suma `size_bytes` de todos los stores | Barra progreso + tier selector |

### Acciones sobre DOCUMENTOS dentro de un store

| Accion | Endpoint | SDK Method | UI |
|--------|----------|------------|-----|
| Listar docs | GET /current-store-documents | `client.file_search_stores.documents.list(parent=store_name)` | Tabla con nombre, estado, size, mime, metadata |
| Ver metadata | (incluido en list) | `doc.custom_metadata` del listado | Expandible en cada doc |
| Editar metadata local | POST /update-document-metadata | Solo local (store_state.json) | Modal de edicion |
| Borrar documento | DELETE /delete-document | `client.file_search_stores.documents.delete(name=doc_name, config={'force': True})` | Boton rojo con confirmacion |
| Buscar en documento | POST /document-query | `client.file_search_stores.documents.query(...)` | (nuevo, aun sin UI dedicada) |

### Datos que mostramos por STORE

```json
{
  "name": "fileSearchStores/mi-store-abc123",
  "display_name": "Mi Store",
  "size_bytes": 1048576,
  "active_documents_count": 10,
  "pending_documents_count": 0,
  "failed_documents_count": 0,
  "create_time": "2026-03-22T..."
}
```

### Datos que mostramos por DOCUMENTO

```json
{
  "name": "fileSearchStores/.../documents/doc-id",
  "display_name": "archivo.txt",
  "state": "STATE_ACTIVE",
  "size_bytes": 52412,
  "mime_type": "text/plain",
  "create_time": "2026-03-22T...",
  "custom_metadata": {
    "phone": "+34686515371",
    "tipo": "whatsapp_history",
    "total_mensajes": 455
  }
}
```

### UI: Como lo mostramos

**Tab File Stores:**
- Grid de cards, una por store
- Cada card muestra: nombre, nro docs activos/pendientes/fallidos, tamaño, fecha
- Store actual resaltado en azul
- Boton "Cambiar" y "Borrar" por store
- Al expandir un store: tabla de documentos con columnas (nombre, estado, tamaño, tipo, metadata)
- Cada documento tiene boton borrar

**Notas importantes:**
- `force: True` es OBLIGATORIO al borrar stores y docs (si no, da error FAILED_PRECONDITION)
- Los nombres de stores son globalmente unicos y auto-generados (displayName + 12 chars random)
- `size_bytes` del store reporta bytes RAW, no el 3x del backend
- Renombrar store NO es posible via la API (hay que crear uno nuevo)
- Mover documentos entre stores NO es posible (hay que re-subir)

### Respuesta anterior sobre PDF

(ver mas abajo)

---

## 22/03/2026 - Respuesta a respuesta_pdf.md

Recibido. Perfecto, mismo enfoque que nosotros: reportlab en backend + blob download. Lo vamos a implementar igual.

Lo del TTS para el summary ejecutivo nos interesa mucho. Cuando lo tengais conectado a las investigaciones, pasadnos el patron. Seria una gran feature para nuestro Manager tambien.

Por ahora no necesitamos nada mas. Buen trabajo con la v1.7.

---

## 22/03/2026 - AVISO: Limites de metadata en File Search

Hemos encontrado un problema al subir metadata enriquecida: la API de Gemini File Search falla con `INVALID_ARGUMENT` cuando hay mas de ~13 campos de custom_metadata por documento (aunque la doc dice 20).

**Solucion:** Limitar a 8-10 campos max. Los campos utiles para filtrar son:
- phone, tipo, fecha_inicio, fecha_fin (basicos)
- categoria_principal, marca, estado_final, sentimiento_cliente (enriquecidos)

**Excluir:** resumen (largo y el RAG ya busca en el texto), categorias (array), dispositivo, es_recurrente, precio_mencionado.

Teneis el detalle completo en `integracion_rag/AVISO_METADATA_LIMITES.md`.

Tambien teneis `integracion_rag/UX_INVESTIGACIONES.md` con el flujo correcto de plantillas e investigaciones nuevas.

---

## 22/03/2026 - Respuesta a resumen_sesion_v17.md

Impresionante trabajo. El resumen es muy completo. Notas:

1. **TTS con descarga WAV**: gran feature, lo portaremos al Manager en una version futura.
2. **Export PDF/TXT/Audio**: nosotros de momento solo tenemos PDF via reportlab. El TXT y Audio los copiaremos.
3. **Los 5 modelos con optgroups**: nosotros hemos subido a 6 (añadimos gemini-2.5-flash-lite).
4. **Creditos con logos**: gracias por eso.

Sobre la **carga de los 410 archivos WhatsApp**: estamos a punto de terminar el experimento (383/410 subidos al store enriquecido). En cuanto acabe la comparativa, os pasamos las instrucciones definitivas con el script de carga listo para usar con vuestra API key.

Buen trabajo con la v1.7.
