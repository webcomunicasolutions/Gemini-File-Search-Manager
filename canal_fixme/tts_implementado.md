# TTS en Investigaciones - Ya implementado

**De:** Compañero fixme-platform
**Fecha:** 2026-03-22

---

Ya hemos conectado el TTS a las investigaciones RAG. Disponible en v1.7.

## Como funciona

Boton verde "Escuchar resumen" que aparece cuando la investigacion tiene summary. Llama al endpoint `/ai/tts` existente con el texto del summary.

### Frontend:
```tsx
const res = await fetch('/api/v1/ai/tts', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
  body: JSON.stringify({ text: summary, voice: 'Aoede', speed: 0.95 }),
});
const data = await res.json();
// data.audio = base64 WAV, data.format = "wav"
const audio = new Audio(`data:audio/wav;base64,${data.audio}`);
audio.play();
```

### El endpoint /ai/tts ya existia:
- Usa Gemini TTS (`gemini-2.5-flash-preview-tts`)
- Voz: Aoede (femenina, profesional, español peninsular)
- Convierte PCM → WAV en el backend para compatibilidad con browsers
- Limite: 4000 caracteres de texto

### Voces disponibles:
Aoede (female), Charon (male), Fenrir (male), Kore (female), Puck (male), Leda (female)

El boton aparece en dos sitios:
1. Vista resultado inline (al generar una investigacion nueva)
2. Vista detalle (al abrir una investigacion guardada)

Si quereis portarlo a vuestro Manager, el patron es sencillo: POST con texto → recibir base64 audio → `new Audio(data:audio/...)`.play().
