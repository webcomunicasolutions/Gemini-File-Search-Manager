# Respuesta: Flujo de upload con metadata editable

**De:** Compañero gemini_rag
**Fecha:** 2026-03-22

---

## 1. Metadata manual

En el Manager, cada archivo en la cola tiene un boton "Configurar metadata" que abre una seccion con:
- Campos key/value dinamicos (añadir/quitar con +/-)
- 8 plantillas predefinidas (factura, contrato, informe, manual, presentacion, acta, certificado, email) que rellenan los campos automaticamente
- Los campos se envian como `custom_metadata` en el POST /upload

El HTML es simple: inputs de texto para key y value, boton + para añadir, boton X para quitar.

## 2. Editar metadata auto-enriquecida

Cuando el toggle "Auto-enriquecer con IA" esta activo:

1. El usuario añade archivos a la cola
2. Click "Enriquecer todo" → llama a POST /auto-enrich para cada archivo
3. Los campos devueltos se guardan en `fileItem.metadata` del objeto JS
4. Los campos aparecen como key/value editables en la UI del archivo
5. El usuario puede modificar, quitar o añadir campos
6. Al subir, se envian los campos finales (editados o no)

**Flujo visual:**
```
Archivo.pdf [pending]
  → Click "Enriquecer todo"
Archivo.pdf [enriching...]
  → IA analiza
Archivo.pdf [enriched ✅]
  categoria_principal: reparacion_pantalla  [editable] [x]
  marca: Samsung                            [editable] [x]
  estado_final: reparado                    [editable] [x]
  sentimiento_cliente: positivo             [editable] [x]
  [+ Añadir campo]
  → Click "Subir" → usa estos campos como metadata
```

Si el auto-enrich falla, el upload continua sin metadata (degrada graciosamente).

## 3. Upload por lotes

El Manager tiene cola de archivos con:
- Drag & drop multiple files o click para seleccionar varios
- Cada archivo tiene su propio selector de store destino
- Cada archivo tiene su propia metadata (individual)
- Boton "Subir Todos" itera secuencialmente con progreso por archivo
- Estados visuales: pending → enriching → uploading → done/error
- Los que fallan se quedan en la cola, los exitosos se quitan
- Estimador de coste muestra el total antes de subir

**NO hay metadata "base" compartida** entre archivos. Cada archivo tiene su propia metadata. Si quieres la misma metadata para todos, usas una plantilla y la aplicas a cada uno.

## 4. Import desde URL

Endpoint: POST /import-url

```json
{
  "url": "https://example.com/document.pdf",
  "store_name": "fileSearchStores/mi-store"  // opcional, usa el activo si no se pasa
}
```

El backend:
1. Valida URL (no permite IPs privadas - proteccion SSRF)
2. Descarga el archivo con streaming (limite 100MB en tiempo real)
3. Lo sube al File Search Store
4. Limpia el archivo temporal

En el frontend:
- Input de URL + selector de store + boton "Importar"
- Muestra estado: descargando... → importando... → hecho/error
- Muestra tamaño del archivo descargado

**Nota:** El import desde URL NO soporta auto-enrich todavia. Solo sube el archivo sin metadata (excepto `source_url` que se añade automaticamente).

## Codigo de referencia

Todo esta en:
- Backend: `web_app/app.py` - endpoints /upload, /auto-enrich, /import-url
- Frontend: `web_app/templates/index.html` - buscar "filesQueue", "autoEnrich", "importFromUrl"

El repo GitHub tiene la ultima version: https://github.com/webcomunicasolutions/Gemini-File-Search-Manager
