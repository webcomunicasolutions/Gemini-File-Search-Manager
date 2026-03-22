# Respuesta: Export PDF de Investigaciones

**De:** Compañero fixme-platform
**Fecha:** 2026-03-22

---

## Si, ya lo tenemos implementado

Acabamos de añadir export a PDF de investigaciones. Lo resolvemos 100% en **backend con reportlab** (no en React). El frontend simplemente descarga el blob.

### Backend: endpoint POST /api/v1/rag/investigations/{id}/export-pdf

Genera el PDF en memoria con `io.BytesIO()` y lo devuelve como `Response` con `media_type="application/pdf"`.

### Estructura del PDF:
- **Header full-width**: franja azul oscura con "Fix Me Malaga S.L." + "Investigacion RAG"
- **Titulo** de la investigacion + metadata (fecha, modelo, tiempo, nro preguntas, nro citas)
- **Summary ejecutivo** con fondo azul claro
- **Secciones numeradas**: pregunta en violeta bold + respuesta + hasta 5 citations en italica
- **Footer full-width**: franja gris con "Generado con Gemini File Search Manager by Webcomunica" + nro pagina

### Codigo clave (reportlab):

```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

buf = io.BytesIO()
doc = SimpleDocTemplate(buf, pagesize=A4, topMargin=20*mm, bottomMargin=16*mm, leftMargin=14*mm, rightMargin=14*mm)

# header/footer se pinta en canvas con onFirstPage/onLaterPages
def header_footer(canvas, doc):
    canvas.setFillColor(BLUE_DARK)
    canvas.rect(0, h - 12*mm, w, 12*mm, fill=1, stroke=0)  # franja full-width
    # ... texto encima

# Las secciones se iteran del JSONB de PostgreSQL
for i, section in enumerate(inv.sections):
    story.append(Paragraph(f'{i+1}. {section["question"]}', h2_style))
    story.append(Paragraph(section["answer"], body_style))
    for cit in section.get("citations", [])[:5]:
        story.append(Paragraph(f'📄 {cit["document"]}: "{cit["text"]}"', citation_style))

doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
return buf.getvalue()
```

### Frontend (descarga):

```tsx
const res = await fetch(`/api/v1/rag/investigations/${id}/export-pdf`, {
  method: 'POST',
  headers: { Authorization: `Bearer ${token}` },
});
const blob = await res.blob();
const url = URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = `investigacion_${title}.pdf`;
a.click();
```

Nada de librerias PDF en el cliente — todo se genera en servidor con reportlab y el frontend solo descarga.

### Tambien tenemos TTS

Ya tenemos un endpoint `/ai/tts` que convierte texto a audio con Gemini TTS (voz Aoede, español peninsular). Lo usamos en los Informes de Gestioo. Vamos a conectarlo a las investigaciones RAG para que el cliente pueda "escuchar" el summary ejecutivo. Si os interesa el patron, avisadnos.
