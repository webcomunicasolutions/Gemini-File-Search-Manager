# Changelog

## 🌍 Available Languages

- [English](CHANGELOG.md)
- [Español](CHANGELOG_ES.md)

---

All notable changes to Gemini File Search Manager will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v1.0.0.html).

---

## [1.0.0] - 2024-12-XX

### Added

- Complete bilingual UI (Spanish/English)
- AI-powered metadata suggestion system using Gemini 2.0 Flash
- HTTP Request Generator with 6 output formats (cURL, Python, JavaScript, n8n, Make.com, Postman)
- 8 operations supported in HTTP Generator
- Tab-based navigation (Chat, Documentos, File Stores, Docs)
- Document metadata editor with visual tag system
- Multiple File Search Store management
- Store switching functionality
- Document state tracking (PENDING, ACTIVE, FAILED)
- Conversation history with 7-message limit
- Metadata filtering in RAG queries
- Citation and grounding metadata extraction
- State persistence via store_state.json
- Responsive design for desktop and mobile
- Comprehensive documentation (English/Spanish)
- Language preference persistence

### Changed

- Increased file upload timeout from 60s to 120s
- Improved metadata management (hybrid Gemini + local storage)
- Enhanced error handling and logging
- Optimized chunking configuration UI
- Modernized UI with Webcomunica branding

### Fixed

- File upload timeout issues for large files
- Metadata not persisting across sessions
- Store not loading on application restart
- Citation extraction from grounding metadata
- Metadata filter conversion to Gemini format

### Security

- Added security documentation (SECURITY.md)
- Implemented secure filename handling
- Added file type validation
- Configured maximum file size limits

---

## [1.0.0] - 2024-11-XX

### Added

- Initial release
- Basic document upload functionality
- RAG chat interface
- File Search Store integration
- Simple metadata support
- Local file management

---

## [Unreleased]

### Planned Features

- English UI translation (full internationalization)
- Batch document upload
- Advanced search operators
- Document versioning
- Export/import stores
- User authentication system
- Multi-user support
- Analytics dashboard
- Webhook notifications
- Real-time collaboration

---

## Version History

- **1.0.0** - Current production release
- **1.0.0** - Initial release

---

## Migration Guides

### Migrating from 1.x to 2.0

#### Breaking Changes

None. Version 2.0 is fully backward compatible with 1.x stores and documents.

#### New Features to Adopt

1. **AI Metadata Suggestion**:
   ```python
   # Upload file with AI-generated metadata
   POST /suggest-metadata
   # Then upload with suggested metadata
   POST /upload
   ```

2. **Metadata Filtering**:
   ```python
   # Filter chat queries by metadata
   POST /chat
   {
       "message": "query",
       "metadata_filters": [{"key": "tipo", "value": "contrato"}]
   }
   ```

3. **HTTP Generator**:
   - Access via "Docs & Help" tab
   - Generate code in 6 formats
   - 8 operations available

#### Configuration Changes

Add to `.env` if using custom settings:
```env
MAX_HISTORY=7  # Conversation history limit
MAX_FILE_SIZE=104857600  # 100MB in bytes
```

---

## Support

For questions about specific versions:
- Check [GitHub Releases](https://github.com/webcomunicasolutions/gemini-file-search-manager/releases)
- Review [Installation Guide](INSTALLATION.md)
- Consult [API Reference](API_REFERENCE.md)

---

**Maintained by**: [Webcomunica Solutions](https://webcomunica.solutions/) & [Optimizaconia](https://www.optimizaconia.es/)

**Last Updated**: November 19, 2025
