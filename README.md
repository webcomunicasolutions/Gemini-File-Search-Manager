# 🔍 Gemini File Search Manager

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![Google Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-orange.svg)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> A powerful, full-featured web application for managing File Search Stores and performing Retrieval Augmented Generation (RAG) using Google's Gemini File Search API with bilingual support (Spanish/English).

<p align="center">
  <img src="web_app/static/images/webcomunica.png" alt="Webcomunica Solutions" height="60">
  <img src="web_app/static/images/optimizaconia.png" alt="Optimizaconia" height="60">
</p>

---

## ✨ Features

### 🎨 Modern Web Interface
- **Bilingual Support**: Complete Spanish/English translation system
- **3 Main Tabs**: Chat, File Stores Management, Documentation & HTTP Generator
- **Real-time Chat**: Interactive RAG queries with document citations
- **File Upload**: Support for 100+ file types (PDF, DOCX, TXT, Markdown, etc.)
- **AI-Powered Metadata**: Automatic metadata extraction using Gemini models

### 📦 File Store Management
- Create and manage multiple File Search Stores
- Upload documents with automatic chunking and embedding
- View documents with state tracking (PENDING, ACTIVE, FAILED)
- Edit metadata with visual tag system
- Delete stores and documents with safety confirmations

### 🔧 HTTP Request Generator
- **6 Output Formats**: cURL, Python, JavaScript, n8n, Make.com, Postman
- **8 Operations**: Create Store, List Stores, Upload Document, Chat RAG, List Documents, Delete Document, Delete Store, Get Operation Status
- Dynamic parameter forms for each operation
- Ready-to-copy code with explanations
- Fully translated interface

### 🌐 Multi-language Support
- Complete translation system (Spanish/English)
- Persistent language preference
- All UI elements translated including:
  - Forms and labels
  - Buttons and messages
  - Code explanations
  - Error messages

### 🎯 Advanced Features
- **Smart Citations**: Automatic grounding metadata extraction
- **Conversation History**: Full chat history with timestamps
- **Model Selection**: Support for multiple Gemini models
- **Metadata Editor**: Visual interface for custom metadata
- **Store Selector**: Easy switching between File Search Stores
- **Responsive Design**: Works on desktop and mobile devices

---

## 📸 Screenshots

### Main Interface
![Main Interface](screenshots/01-main-interface.jpg)
*Modern bilingual interface with upload, chat, file stores, and settings tabs*

### AI Metadata Suggestions
![AI Metadata](screenshots/05-metadata-ai-suggestions.jpg)
*Automatic metadata extraction powered by Gemini AI*

### Chat with Documents
![Chat Interface](screenshots/06-chat-interface.jpg)
*Interactive RAG chat with real-time responses*

### File Stores Management
![File Stores](screenshots/07-file-stores-management.jpg)
*Manage multiple file search stores with document tracking*

### Settings Configuration
![Settings](screenshots/08-settings-page.jpg)
*Configure API keys and model preferences*

### API Documentation & HTTP Generator
![API Docs](screenshots/09-api-docs-http-generator.jpg)
*Built-in HTTP request generator with 6 output formats*

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API Key ([Get one here](https://aistudio.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/webcomunicasolutions/gemini-rag.git
   cd gemini-rag
   ```

2. **Create and activate virtual environment**
   ```bash
   cd web_app
   python -m venv venv

   # On Windows:
   venv\Scripts\activate

   # On Linux/Mac:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key**
   - Copy `.env.example` to `.env`
   - Add your Gemini API key:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open in browser**
   ```
   http://localhost:5001
   ```

---

## 📖 Usage

### 1. Configure Your API Key
Go to **Settings** tab and enter your Gemini API Key. The app will remember it for future sessions.

### 2. Create or Select a Store
- Create a new File Search Store in the **File Stores** tab
- Or select an existing store from the dropdown

### 3. Upload Documents
- Click **Browse Files** or drag & drop
- Supported formats: PDF, DOCX, TXT, MD, CSV, and 100+ more
- Add custom metadata (optional)
- Select AI model for metadata generation (optional)

### 4. Chat with Your Documents
- Go to **Chat** tab
- Ask questions about your uploaded documents
- Get answers with citations and source references
- View full conversation history

### 5. Generate HTTP Requests
- Go to **Docs & Help** tab
- Select an operation
- Configure parameters
- Choose output format (cURL, Python, JavaScript, etc.)
- Copy ready-to-use code

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│           User (Browser)                    │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│      Flask Web Application                  │
│  ┌─────────────────────────────────────┐   │
│  │  Frontend (HTML/CSS/JS)             │   │
│  │  - Bilingual UI                     │   │
│  │  - Real-time chat                   │   │
│  │  - File upload                      │   │
│  │  - HTTP generator                   │   │
│  └─────────────────────────────────────┘   │
│  ┌─────────────────────────────────────┐   │
│  │  Backend (Python/Flask)             │   │
│  │  - API endpoints                    │   │
│  │  - State management                 │   │
│  │  - File processing                  │   │
│  └─────────────────────────────────────┘   │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│   Google Gemini File Search API            │
│  - Document vectorization                   │
│  - Semantic search                          │
│  - RAG responses                            │
│  - Citations & grounding                    │
└─────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

- **Backend**: Flask (Python 3.8+)
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **AI/ML**: Google Gemini 2.5 Flash API
- **Storage**: JSON-based state persistence
- **Dependencies**:
  - `google-genai`: Official Gemini SDK
  - `flask`: Web framework
  - `python-dotenv`: Environment management

---

## 📚 Documentation

- **[Installation Guide](INSTALLATION.md)**: Detailed setup instructions
- **[Features](FEATURES.md)**: Complete feature list
- **[API Reference](API_REFERENCE.md)**: Backend API documentation
- **[Contributing](CONTRIBUTING.md)**: How to contribute
- **[CLAUDE.md](CLAUDE.md)**: Gemini File Search API reference

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Original Inspiration**: This project was inspired by the YouTube video ["Gemini's File Search API Makes RAG Easy (and CHEAP!)"](https://www.youtube.com/watch?v=_wN2v8o-imo) by **Mark Kashef** - Thank you for showing the potential of Gemini's File Search API!
- **Google Gemini Team**: For the amazing File Search API
- **Flask Community**: For the excellent web framework
- Built with ❤️ by [Webcomunica Solutions](https://webcomunica.solutions/) & [Optimizaconia](https://www.optimizaconia.es/)

---

## 📞 Contact & Support

- **Website**: [webcomunica.solutions](https://webcomunica.solutions/)
- **GitHub**: [@webcomunicasolutions](https://github.com/webcomunicasolutions/)
- **LinkedIn**: [Juan José Sánchez Bernal](https://www.linkedin.com/in/juan-josé-sánchez-bernal-6292a925/)
- **Instagram**: [@webcomunica_soluciones](https://www.instagram.com/webcomunica_soluciones/)

---

## ⭐ Star History

If you find this project useful, please consider giving it a star on GitHub!

---

**Last Updated**: November 19, 2025
**Version**: 1.0.0
**Status**: Production Ready ✅

---

## 🌍 Available Languages

- [English](README.md)
- [Español](README_ES.md)
