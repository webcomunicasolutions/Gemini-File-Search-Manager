# Notas de Actualización - Marzo 2026

Investigación realizada el 21/03/2026 sobre cambios en la Gemini API desde que se creó el proyecto.

---

## 1. Gemini Embedding 2 (Preview - 10 marzo 2026)

**Estado:** Public Preview (aún no GA)

Google ha sacado su primer modelo de embeddings **multimodal**. Ya no solo embebe texto, sino también imágenes, video, audio y documentos en un mismo espacio vectorial.

### Especificaciones
| Campo | Valor |
|-------|-------|
| Modelo | `gemini-embedding-2-preview` |
| Dimensiones | 3072 (default), reducible a 1536, 768 via MRL |
| Contexto texto | 8.192 tokens |
| Imágenes | Hasta 6 por request |
| Video | Hasta 120 segundos |
| Audio | Nativo (sin transcripción intermedia) |
| Precio | $0.20/MTok (batch: $0.10/MTok) |

### Cambio respecto a embedding-001
- **embedding-001** (el que usa el Manager): solo texto, $0.15/MTok
- **embedding-2**: multimodal, $0.20/MTok
- Embedding-001 sigue funcionando, no está deprecado

### Impacto en el Manager
- File Search usa internamente `gemini-embedding-001` para indexar
- Cuando Embedding 2 salga a GA, File Search probablemente lo adopte automáticamente
- **Posible mejora**: Ofrecer opción de seleccionar modelo de embedding al crear un store (si la API lo permite)
- **Caso de uso nuevo**: Subir imágenes al store y buscar por contenido visual (ej: "foto de pantalla rota" encontraría imágenes de pantallas rotas)

### Matryoshka Representation Learning (MRL)
- Permite reducir dimensiones dinámicamente: 3072 → 1536 → 768
- Menor dimensión = menos almacenamiento, más rápido, algo menos preciso
- **Posible mejora**: Si el Manager permite embeddings custom (fuera de File Search), ofrecer selector de dimensiones

### Fuentes
- https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-embedding-2/
- https://ai.google.dev/gemini-api/docs/embeddings

---

## 2. Límites de archivo ampliados (Enero 2026)

### Cambios
| Campo | Antes | Ahora |
|-------|-------|-------|
| Max file size (upload) | 20 MB | **100 MB** |
| Max inline data (base64) | 20 MB | **100 MB** |
| PDFs | Sin límite de páginas | **Max 1.000 páginas o 50 MB** |

### Impacto en el Manager
- El CLAUDE.md ya dice 100 MB, pero verificar que el frontend y el backend no tengan validaciones antiguas de 20 MB
- Revisar si hay mensajes de error o tooltips que mencionen el límite antiguo

### Fuente
- https://blog.google/innovation-and-ai/technology/developers-tools/gemini-api-new-file-limits/

---

## 3. Input desde Google Cloud Storage (Enero 2026)

### Nueva funcionalidad
- Se pueden registrar archivos desde **buckets de GCS** sin re-subir los bytes
- También desde cualquier **URL firmada (pre-signed URL)** o **URL HTTP pública**
- Registras el URI una vez y lo usas en múltiples requests

### Impacto en el Manager
- **Mejora importante**: Añadir opción de "Importar desde URL" o "Importar desde GCS bucket"
- Para cargas masivas (ej: 11.000+ documentos), en lugar de subir uno a uno:
  1. Subir todos los archivos a un bucket GCS
  2. Registrar los URIs en File Search
  3. Mucho más rápido y escalable
- **Endpoint relevante**: `importFile` ya existente, pero con `gcsUri` como source en vez de upload directo

### Fuente
- https://blog.google/innovation-and-ai/technology/developers-tools/gemini-api-new-file-limits/

---

## 4. Gemini 3 + Tool Combos (Marzo 2026)

### Nueva funcionalidad
- Se pueden combinar **File Search + Function Calling + Google Search** en una sola llamada
- Gemini decide automáticamente cuándo usar cada tool

### Ejemplo de caso de uso
Un bot que en una sola llamada:
1. Busca en el historial del cliente (File Search)
2. Busca en Google información actualizada (Google Search)
3. Llama a una API interna para verificar estado de pedido (Function Calling)

### Impacto en el Manager
- **Mejora posible**: Opción de habilitar "Google Search grounding" en el chat además del File Search
- **Mejora posible**: Soporte para function calling combinado (el usuario define funciones que Gemini puede llamar durante el chat)

### Pricing Google Search grounding
- Antes: $35/1.000 prompts (flat rate)
- Ahora: **$14/1.000 búsquedas** (solo cobra cuando Gemini decide buscar)

### Fuentes
- https://blog.google/innovation-and-ai/technology/developers-tools/gemini-api-tooling-updates/
- https://developers.googleblog.com/new-gemini-api-updates-for-gemini-3/

---

## 5. File Search Store - Límites actualizados

### Límites por tier
| Tier | Max store size total |
|------|---------------------|
| Free | 1 GB |
| Tier 1 | 10 GB |
| Tier 2 | 100 GB |
| Tier 3 | 1 TB |

### Otros límites
- **500 stores por proyecto** (si necesitas más, usar proyectos separados)
- **Tamaño real del store ≈ 3x input** (incluye embeddings almacenados)
- **Recomendado**: Mantener cada store bajo 20 GB para latencia óptima
- **pageSize máximo**: 20 (para list stores y list documents)

### Impacto en el Manager
- Mostrar el tier actual y el uso de almacenamiento en la UI
- Avisar cuando se acerque al límite del tier
- **Posible mejora**: Calculadora de coste estimado antes de subir documentos masivos

### Fuente
- https://discuss.ai.google.dev/t/clarification-on-total-size-of-project-file-search-stores-limit-calculation/119435

---

## 6. Pricing actualizado (Marzo 2026)

### File Search
| Concepto | Precio |
|----------|--------|
| Indexación (crear embeddings) | $0.15/MTok |
| Almacenamiento | **GRATIS** |
| Consultas (embeddings en query) | **GRATIS** |
| Tokens recuperados en respuesta | Precio normal de context tokens |

### Embeddings API (uso directo, fuera de File Search)
| Modelo | Precio | Free tier |
|--------|--------|-----------|
| gemini-embedding-001 | $0.15/MTok | 1.500 req/día gratis |
| gemini-embedding-2-preview | $0.20/MTok | Gratis en preview |

### Impacto en el Manager
- Actualizar la documentación de pricing
- **Posible mejora**: Estimador de coste en la UI antes de indexar un batch grande
  - Fórmula: tokens_totales × $0.15/1M = coste de indexación

### Fuente
- https://ai.google.dev/gemini-api/docs/pricing

---

## 7. Modelos Gemini actualizados

### Para generación (chat)
| Modelo | Estado | Notas |
|--------|--------|-------|
| gemini-2.5-flash | Disponible | El que probablemente usa el Manager |
| gemini-2.5-pro | Disponible | Más potente, más caro |
| gemini-3 | Nuevo (marzo 2026) | Tool combos, Maps grounding |

### Para metadata suggestions
| Modelo | Estado | Notas |
|--------|--------|-------|
| gemini-2.0-flash-exp | El Manager lo usa | Verificar si sigue disponible |
| gemini-2.5-flash | Recomendado | Más estable que exp |

### Impacto en el Manager
- Verificar que `gemini-2.0-flash-exp` (usado en suggest-metadata) no esté deprecado
- Considerar upgrade a `gemini-2.5-flash` o `gemini-3` para la generación
- **Posible mejora**: Selector de modelo en la UI (ya existe parcialmente)

---

## 8. Nodos n8n para File Search

### Integración disponible
- **Paquete npm**: `n8n-nodes-gemini-file-search` (community node, no oficial)
- **Alternativa**: 4 nodos HTTP Request estándar
- **Templates existentes**:
  - https://n8n.io/workflows/11197-build-a-rag-system-by-uploading-pdfs-to-the-google-gemini-file-search-store/
  - https://n8n.io/workflows/11269-build-enterprise-rag-system-with-google-gemini-file-search-and-retell-ai-voice/

### Impacto en el Manager
- El Manager ya genera código para n8n en el HTTP Generator
- Verificar que los snippets generados estén actualizados con los endpoints actuales
- **Posible mejora**: Exportar un workflow n8n completo (.json) desde la UI, no solo snippets individuales

---

## 9. Resumen de mejoras prioritarias para el Manager

### Alta prioridad (funcionalidad nueva)
1. **Import desde GCS bucket / URL** - Para cargas masivas sin subir uno a uno
2. **Batch upload** - Subir múltiples archivos en una operación (actualmente es uno a uno)
3. **Actualizar modelo suggest-metadata** - De `gemini-2.0-flash-exp` a `gemini-2.5-flash`

### Media prioridad (mejoras de UX)
4. **Estimador de coste** - Calcular coste de indexación antes de subir
5. **Info de tier y almacenamiento** - Mostrar uso actual vs límite del tier
6. **Selector de modelo de chat** - Añadir gemini-3 como opción

### Baja prioridad (futuro)
7. **Google Search grounding** - Combinar File Search + Google Search en el chat
8. **Soporte multimodal** - Cuando Embedding 2 sea GA, permitir buscar por imágenes
9. **Export workflow n8n completo** - Generar .json importable en n8n

---

## 10. Caso de uso real: FixMe Málaga (Webcomunica)

### Contexto
- 11.587 conversaciones WhatsApp exportadas (Tecnoshare)
- Chatwoot como plataforma de atención al cliente
- Bot en n8n que necesita contexto histórico de cada cliente

### Cómo usaría el Manager
1. Preparar cada conversación como archivo .txt con metadata: `{phone, name, tipo: "whatsapp_history"}`
2. Subir las 11.587 conversaciones al Manager (idealmente via batch o GCS)
3. Bot de n8n consulta `POST /chat` con `metadata_filters: [{key: "phone", value: "+34XXX"}]`
4. Gemini devuelve contexto relevante del cliente
5. Nuevas conversaciones se añaden incrementalmente via webhook Chatwoot → n8n → Manager

### Coste estimado
- ~6M tokens × $0.15/MTok = **$0.90 total** para indexar todo el historial
- Consultas y almacenamiento: $0/mes
