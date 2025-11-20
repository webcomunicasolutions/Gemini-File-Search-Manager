# 🔍 Gemini File Search Manager

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![Google Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-orange.svg)](https://ai.google.dev/)
[![Licencia](https://img.shields.io/badge/licencia-MIT-blue.svg)](LICENSE)

> Una aplicación web completa y potente para gestionar File Search Stores y realizar Generación Aumentada por Recuperación (RAG) usando la API de File Search de Google Gemini con soporte bilingüe (Español/Inglés).

<p align="center">
  <img src="web_app/static/images/webcomunica.png" alt="Webcomunica Solutions" height="60">
  <img src="web_app/static/images/optimizaconia.png" alt="Optimizaconia" height="60">
</p>

---

## ✨ Características

### 🎨 Interfaz Web Moderna
- **Soporte Bilingüe**: Sistema completo de traducción Español/Inglés
- **3 Pestañas Principales**: Chat, Gestión de File Stores, Documentación y Generador HTTP
- **Chat en Tiempo Real**: Consultas RAG interactivas con citaciones de documentos
- **Carga de Archivos**: Soporte para múltiples formatos (PDF, DOCX, XLSX, PPTX, TXT, MD, HTML, CSV, y más)
- **Metadatos con IA**: Extracción automática de metadatos usando modelos Gemini

### 📦 Gestión de File Stores
- Crear y gestionar múltiples File Search Stores
- Cargar documentos con chunking y embedding automáticos
- Ver documentos con seguimiento de estado (PENDING, ACTIVE, FAILED)
- Editar metadatos con sistema visual de etiquetas
- Eliminar stores y documentos con confirmaciones de seguridad

### 🔧 Generador de Peticiones HTTP
- **6 Formatos de Salida**: cURL, Python, JavaScript, n8n, Make.com, Postman
- **8 Operaciones**: Crear Store, Listar Stores, Subir Documento, Chat RAG, Listar Documentos, Eliminar Documento, Eliminar Store, Obtener Estado de Operación
- Formularios dinámicos de parámetros para cada operación
- Código listo para copiar con explicaciones
- Interfaz completamente traducida

### 🌐 Soporte Multi-idioma
- Sistema completo de traducción (Español/Inglés)
- Preferencia de idioma persistente
- Todos los elementos de UI traducidos incluyendo:
  - Formularios y etiquetas
  - Botones y mensajes
  - Explicaciones de código
  - Mensajes de error

### 🎯 Características Avanzadas
- **Citaciones Inteligentes**: Extracción automática de metadatos de fundamentación
- **Historial de Conversación**: Historial completo de chat con marcas de tiempo
- **Selección de Modelo**: Soporte para múltiples modelos Gemini
- **Editor de Metadatos**: Interfaz visual para metadatos personalizados
- **Selector de Store**: Cambio fácil entre File Search Stores
- **Diseño Responsivo**: Funciona en dispositivos de escritorio y móviles

---

## 🚀 Inicio Rápido

### Requisitos Previos

- Python 3.8 o superior
- API Key de Google Gemini ([Consigue una aquí](https://aistudio.google.com/app/apikey))

### Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/webcomunicasolutions/gemini-rag.git
   cd gemini-rag
   ```

2. **Crear y activar entorno virtual**
   ```bash
   cd web_app
   python -m venv venv

   # En Windows:
   venv\Scripts\activate

   # En Linux/Mac:
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar tu API key**
   - Copiar `.env.example` a `.env`
   - Añadir tu API key de Gemini:
     ```
     GEMINI_API_KEY=tu_api_key_aqui
     ```

5. **Ejecutar la aplicación**
   ```bash
   python app.py
   ```

6. **Abrir en el navegador**
   ```
   http://localhost:5001
   ```

---

## 📖 Uso

### 1. Configurar tu API Key
Ve a la pestaña **Configuración** e introduce tu API Key de Gemini. La aplicación la recordará para futuras sesiones.

### 2. Crear o Seleccionar un Store
- Crea un nuevo File Search Store en la pestaña **File Stores**
- O selecciona un store existente del menú desplegable

### 3. Subir Documentos
- Haz clic en **Examinar Archivos** o arrastra y suelta
- Formatos soportados: PDF, DOCX, XLSX, PPTX, TXT, MD, HTML, CSV, JSON, XML y muchos archivos de código (Python, JavaScript, Java, C++, Go, Rust, etc.)
- **Ver lista completa**: [SUPPORTED_FORMATS.md](SUPPORTED_FORMATS.md) - 200 tipos MIME soportados
- Añade metadatos personalizados (opcional)
- Selecciona modelo de IA para generación de metadatos (opcional)

### 4. Conversar con tus Documentos
- Ve a la pestaña **Chat**
- Haz preguntas sobre tus documentos cargados
- Obtén respuestas con citaciones y referencias a las fuentes
- Ver historial completo de conversación

### 5. Generar Peticiones HTTP
- Ve a la pestaña **Docs y Ayuda**
- Selecciona una operación
- Configura los parámetros
- Elige el formato de salida (cURL, Python, JavaScript, etc.)
- Copia el código listo para usar

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────┐
│           Usuario (Navegador)               │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│      Aplicación Web Flask                   │
│  ┌─────────────────────────────────────┐   │
│  │  Frontend (HTML/CSS/JS)             │   │
│  │  - UI Bilingüe                      │   │
│  │  - Chat en tiempo real              │   │
│  │  - Carga de archivos                │   │
│  │  - Generador HTTP                   │   │
│  └─────────────────────────────────────┘   │
│  ┌─────────────────────────────────────┐   │
│  │  Backend (Python/Flask)             │   │
│  │  - Endpoints API                    │   │
│  │  - Gestión de estado                │   │
│  │  - Procesamiento de archivos        │   │
│  └─────────────────────────────────────┘   │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│   API de File Search de Google Gemini      │
│  - Vectorización de documentos             │
│  - Búsqueda semántica                      │
│  - Respuestas RAG                          │
│  - Citaciones y fundamentación             │
└─────────────────────────────────────────────┘
```

---

## 🛠️ Stack Tecnológico

- **Backend**: Flask (Python 3.8+)
- **Frontend**: JavaScript Vanilla, HTML5, CSS3
- **IA/ML**: API Google Gemini 2.5 Flash
- **Almacenamiento**: Persistencia de estado basada en JSON
- **Dependencias**:
  - `google-genai`: SDK oficial de Gemini
  - `flask`: Framework web
  - `python-dotenv`: Gestión de variables de entorno

---

## 📚 Documentación

- **[Guía de Instalación](INSTALLATION_ES.md)**: Instrucciones detalladas de configuración
- **[Características](FEATURES_ES.md)**: Lista completa de características
- **[Referencia API](API_REFERENCE_ES.md)**: Documentación de la API backend
- **[Contribuir](CONTRIBUTING_ES.md)**: Cómo contribuir
- **[CLAUDE.md](CLAUDE.md)**: Referencia de la API File Search de Gemini

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor consulta [CONTRIBUTING_ES.md](CONTRIBUTING_ES.md) para más detalles.

### Configuración de Desarrollo

1. Haz fork del repositorio
2. Crea una rama de características (`git checkout -b feature/caracteristica-increible`)
3. Haz commit de tus cambios (`git commit -m 'Añadir característica increíble'`)
4. Haz push a la rama (`git push origin feature/caracteristica-increible`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.

---

## 🙏 Agradecimientos

- **Inspiración Original**: Este proyecto fue inspirado por el video de YouTube ["Gemini's File Search API Makes RAG Easy (and CHEAP!)"](https://youtu.be/_wN2v8o-imo) de **Mark Kashef** - ¡Gracias por mostrar el potencial de la API File Search de Gemini!
- **Equipo de Google Gemini**: Por la increíble API de File Search
- **Comunidad Flask**: Por el excelente framework web
- Construido con ❤️ por [Webcomunica Solutions](https://webcomunica.solutions/) & [Optimizaconia](https://www.optimizaconia.es/)

---

## 📞 Contacto y Soporte

- **Website**: [webcomunica.solutions](https://webcomunica.solutions/)
- **GitHub**: [@webcomunicasolutions](https://github.com/webcomunicasolutions/)
- **LinkedIn**: [Juan José Sánchez Bernal](https://www.linkedin.com/in/juan-josé-sánchez-bernal-6292a925/)
- **Instagram**: [@webcomunica_soluciones](https://www.instagram.com/webcomunica_soluciones/)

---

## ⭐ Historial de Estrellas

¡Si encuentras este proyecto útil, por favor considera darle una estrella en GitHub!

---

**Última Actualización**: 19 de Noviembre de 2025
**Versión**: 1.0.0
**Estado**: Listo para Producción ✅

---

## 🌍 Idiomas Disponibles

- [English](README.md)
- [Español](README_ES.md)
