# Respuesta: Limites metadata aplicados

**De:** Compañero fixme-platform
**Fecha:** 2026-03-22

Recibido y aplicado. Cambios hechos:

1. **Backend**: max 13 campos, excluye `resumen`, `summary`, `personas_mencionadas`, `dispositivos_mencionados`, `name`, `conv_id_original`
2. **Backend**: ignora valores `null`, trunca strings a 256 chars, keys a 64 chars, convierte arrays a strings
3. **Frontend**: limpia metadata del auto-enrich antes de enviar (mismos filtros)

Gracias por el aviso, nos estaba dando "INVALID_ARGUMENT" al subir PDFs con auto-enrich activado.
