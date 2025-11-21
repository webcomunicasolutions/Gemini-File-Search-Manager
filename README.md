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
- **Enhanced File Upload**:
  - 60+ file extensions supported (PDF, DOCX, XLSX, CSV, code files, and more)
  - Smart MIME type detection with 70+ pre-mapped formats
  - Dual-method upload system (direct + fallback) for maximum reliability
  - Automatic handling of problematic file formats (CSV, large files)
- **AI-Powered Metadata** ⭐ NEW:
  - Automatic metadata extraction using Gemini models
  - **Bilingual metadata generation** - respects your interface language
  - **DOCX/XLSX analysis support** - extract metadata from Office documents
  - Smart text extraction for unsupported file types
  - Quality over quantity (5-12 metadata fields)

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
- **60+ file extensions supported** including:
  - 📄 Documents: PDF, DOC, DOCX, ODT, RTF
  - 📊 Spreadsheets: CSV, XLSX, XLS, XLSM, ODS
  - 📈 Presentations: PPTX, PPT, ODP
  - 💾 Data: JSON, XML, YAML, SQL
  - 💻 Code: 30+ programming languages (Python, JavaScript, Java, C++, Go, Rust, TypeScript, PHP, Ruby, Swift, Kotlin, Scala, and more)
  - 📝 Markup: HTML, Markdown, LaTeX, Jupyter Notebooks
- **Smart MIME type detection** with automatic fallback
- **Robust upload system**: Direct upload with Files API fallback for problematic files
- **See complete list**: [SUPPORTED_FORMATS.md](SUPPORTED_FORMATS.md) - 200+ MIME types officially supported by Gemini
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
│  │  - Smart MIME detection             │   │
│  │  - Upload fallback system           │   │
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

### 🔄 Enhanced File Upload System

The application implements a **robust dual-method upload system** to ensure maximum compatibility:

**Primary Method: Direct Upload**
- Uses `uploadToFileSearchStore` API
- Single-step process
- Automatic MIME type detection by API
- Fastest and most efficient

**Fallback Method: Files API + Import**
- Activates when direct upload fails
- Two-step process: upload to Files API → import to store
- Explicit MIME type specification
- Handles edge cases (CSV, large files, etc.)

**Smart MIME Type Detection**
- 70+ pre-mapped file extensions
- Fallback to Python `mimetypes` module
- Safe default for unknown types
- Optimized for Gemini File Search API

**Supported Extensions:**
```
Documents:    txt, pdf, doc, docx, odt, rtf, md
Spreadsheets: csv, tsv, xlsx, xls, xlsm, xlsb, ods
Presentations: pptx, ppt, odp
Data Formats: json, xml, yaml, yml, sql
Code Files:   py, js, jsx, ts, tsx, java, c, cpp, cs, go, rs, php, rb, swift, kt, scala, pl, r, hs, erl, lua, sh, dart
Web:          html, htm, css, scss, sass
Scientific:   ipynb, bib, tex
Archives:     zip
... and more (60+ total)
```

This dual-method approach ensures files are uploaded successfully even when encountering API-specific issues with certain formats.

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

**Last Updated**: November 21, 2025
**Version**: 1.2.0
**Status**: Production Ready ✅

### 🆕 Recent Updates (v1.2.0 - Nov 21, 2025)
- ✅ **Bilingual Metadata Generation**: AI now generates metadata in your interface language (Spanish/English)
- ✅ **DOCX/XLSX Metadata Analysis**: Extract metadata from Word and Excel documents with AI
- ✅ **Text Extraction**: Smart local text extraction for Office documents
- ✅ **Windows File Lock Fix**: Proper file handle management prevents locking issues

### Previous Updates (v1.1.0 - Nov 21, 2025)
- ✅ **Enhanced File Upload System**: Dual-method upload with automatic fallback
- ✅ **Smart MIME Detection**: Comprehensive MIME type mapping for 70+ formats
- ✅ **Extended Format Support**: 60+ file extensions supported
- ✅ **CSV/Excel Upload Fix**: Resolved upload issues with spreadsheet formats

---

## 🌍 Available Languages

- [English](README.md)
- [Español](README_ES.md)
