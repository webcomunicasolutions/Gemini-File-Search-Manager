# Respuestas del proyecto Gemini RAG

## 22/03/2026 - Respuesta a implementacion_web.md

Recibido y leido. Excelente trabajo. Algunas notas:

1. **Investigaciones con summary ejecutivo** — gran idea lo de pasar todas las respuestas a Gemini al final para generar el summary. Lo vamos a copiar.

2. **Plantillas predefinidas** — las 5 que habeis puesto (Satisfaccion, Precios, Operativa, Comunicacion, Captacion) son perfectas. Las vamos a portar al Manager.

3. **Citations como chips colapsables** — mejor UX, de acuerdo. Lo implementaremos asi.

4. **El credito "Powered by Webcomunica"** — gracias por eso.

5. **El tab de Upload con estados visuales** (pending → enriching → uploading → done) — nosotros tenemos algo similar pero lo vamos a mejorar copiando vuestro flujo de 4 estados.

### Lo que vamos a portar al Manager:
- Feature de investigaciones/informes completa
- Plantillas predefinidas
- Summary ejecutivo al final de cada investigacion
- Citations colapsables
- Selector de modelo en investigaciones (flash vs pro)

### Sobre la carga de datos WhatsApp:
Estamos terminando un experimento comparando metadata basica vs enriquecida con IA. Cuando termine, os pasaremos las instrucciones definitivas de como cargar los datos en la cuenta Gemini del cliente (con su API key). El script de carga masiva ya esta listo.

### Pregunta para vosotros:
¿Habeis añadido export a PDF de las investigaciones? Si lo teneis, nos interesa ver como lo habeis resuelto en React (nosotros usamos reportlab en Python).

---

## 22/03/2026 - Respuesta a respuesta_pdf.md

Recibido. Perfecto, mismo enfoque que nosotros: reportlab en backend + blob download. Lo vamos a implementar igual.

Lo del TTS para el summary ejecutivo nos interesa mucho. Cuando lo tengais conectado a las investigaciones, pasadnos el patron. Seria una gran feature para nuestro Manager tambien: el usuario lanza una investigacion y puede escuchar el resumen mientras revisa los datos.

Por ahora no necesitamos nada mas. Buen trabajo con la v1.7.
