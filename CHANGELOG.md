# Changelog

## 🌍 Available Languages

- [English](CHANGELOG.md)
- [Español](CHANGELOG_ES.md)

---

All notable changes to Gemini File Search Manager will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v1.0.0.html).

---

## [1.2.0] - 2025-11-21

### Added

- **Bilingual Metadata Generation**: AI-powered metadata now respects interface language
  - Spanish prompts when using Spanish UI
  - English prompts when using English UI
  - All metadata values generated in the selected language
  - Comprehensive system instructions for both languages (180+ lines each)
- **DOCX/XLSX Metadata Analysis Support**: Extract metadata from Office documents
  - Text extraction from DOCX files using `python-docx`
  - Text extraction from XLSX files using `openpyxl`
  - Reads up to 100 rows per Excel sheet
  - Extracts text from Word paragraphs and tables
  - Proper file handle closing to prevent Windows locking issues
- **New Dependencies**:
  - `python-docx==1.1.2` - For DOCX text extraction
  - `openpyxl==3.1.5` - For XLSX text extraction

### Fixed

- **DOCX Metadata Analysis**: Fixed 400 INVALID_ARGUMENT error
  - Files API doesn't support DOCX for multimodal analysis
  - Implemented local text extraction as workaround
  - Text sent directly to Gemini for metadata generation
- **XLSX Metadata Analysis**: Fixed 400 INVALID_ARGUMENT error
  - Files API doesn't support XLSX for multimodal analysis
  - Implemented local text extraction with openpyxl
  - Added proper workbook closing to prevent file locks
- **Windows File Locking**: Fixed `[WinError 32]` file access errors
  - Added `finally` block to ensure workbook closure
  - Prevents "file being used by another process" errors
  - Files now properly released before upload attempts
- **Language-Specific Metadata**: Metadata values now match UI language
  - Previously all metadata was generated in English
  - Now respects user's language preference
  - Consistent user experience across the application

### Changed

- **Metadata Generation Logic**: Dual-path approach based on file type
  - PDF, images, text files: Use Files API (original method)
  - DOCX, XLSX, DOC, XLS: Use text extraction method
  - Automatic detection based on MIME type
  - Transparent to the user
- **suggest-metadata Endpoint**: Enhanced with language parameter
  - Accepts `language` parameter ('es' or 'en')
  - Frontend automatically sends current UI language
  - Generates appropriate prompts based on language
- **System Prompts**: Created comprehensive bilingual prompts
  - Spanish: 180+ lines with detailed instructions
  - English: 180+ lines with detailed instructions
  - Explicit instructions to generate values in target language
  - Quality over quantity philosophy (5-12 metadata fields)

### Technical Details

**New Functions (`app.py`)**:
- `extract_text_from_docx()` (lines 226-258): Extracts text from DOCX files
  - Reads all paragraphs
  - Extracts text from tables
  - Returns concatenated text
- `extract_text_from_xlsx()` (lines 260-302): Extracts text from XLSX files
  - Iterates through all sheets
  - Reads up to 100 rows per sheet
  - Formats data with pipe separators
  - **Critical**: Includes `finally` block with `wb.close()`

**Modified Functions (`app.py`)**:
- `suggest_metadata()` endpoint (lines 1073-1380):
  - Added `language` parameter extraction (line 1091)
  - Implemented text extraction logic (lines 1107-1142)
  - Bilingual system instructions (lines 1144-1232)
  - Bilingual analysis prompts (lines 1234-1287)
  - Dual-path content generation (lines 1289-1329)

**Frontend Changes (`index.html`)**:
- Line 2294: Added `formData.append('language', currentLang)` in queue upload
- Line 2530: Added `formData.append('language', currentLang)` in direct upload

**Implementation Pattern**:
```python
# Detect if text extraction is needed
use_text_extraction = mime_type in [
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # DOCX
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # XLSX
    'application/vnd.ms-excel',  # XLS
    'application/msword'  # DOC
]

if use_text_extraction:
    # Extract text locally
    if 'wordprocessingml' in mime_type:
        extracted_text = extract_text_from_docx(temp_path)
    elif 'spreadsheetml' in mime_type:
        extracted_text = extract_text_from_xlsx(temp_path)

    # Send text directly to Gemini
    response = client.models.generate_content(
        contents=[Part.from_text(f"{prompt}\n\nDocument content:\n{extracted_text[:10000]}")],
        config=GenerateContentConfig(system_instruction=system_instruction)
    )
else:
    # Use Files API for supported formats (PDF, images, etc.)
    uploaded_file = client.files.upload(file=temp_path, config={'mime_type': mime_type})
    response = client.models.generate_content(
        contents=[Part.from_uri(uploaded_file.uri), Part.from_text(prompt)],
        config=GenerateContentConfig(system_instruction=system_instruction)
    )
```

---

## [1.1.0] - 2025-11-21

### Added

- **Enhanced File Upload System**: Implemented dual-method upload mechanism
  - Primary method: Direct upload via `uploadToFileSearchStore`
  - Fallback method: Files API upload + `importFile` for problematic files
  - Automatic retry on upload failure with alternative method
- **Smart MIME Type Detection**: New `get_mime_type()` function with comprehensive mapping
  - 70+ pre-mapped file extensions to official MIME types
  - Fallback to Python `mimetypes` module
  - Safe default for unknown file types
- **Extended File Format Support**: Expanded from 12 to 60+ supported extensions
  - Documents: txt, pdf, doc, docx, odt, rtf, md, markdown
  - Spreadsheets: csv, tsv, xlsx, xls, xlsm, xlsb, ods
  - Presentations: pptx, ppt, odp
  - Data formats: json, xml, yaml, yml, sql
  - Code files: 30+ programming languages (Python, JavaScript, Java, C++, Go, Rust, TypeScript, PHP, Ruby, Swift, Kotlin, Scala, and more)
  - Web: html, htm, css, scss, sass
  - Scientific: ipynb, bib, bibtex, tex
  - Archives: zip

### Fixed

- **CSV Upload Issues**: Resolved 500 Internal Server Error with CSV files
  - Fallback mechanism handles CSV files that fail direct upload
  - Explicit MIME type specification in fallback method
- **XLSX/XLS Upload Issues**: Fixed spreadsheet upload failures
  - Proper MIME type detection for Excel formats
  - Automatic fallback for problematic spreadsheet files
- **DOC/DOCX Upload Issues**: Corrected Word document upload errors
  - Added comprehensive Microsoft Office MIME type mappings
  - Fallback handles edge cases with Office documents

### Changed

- **MIME Type Mapping**: Added comprehensive `MIME_TYPE_MAPPING` dictionary
  - Priority-based detection: Manual mapping → mimetypes module → safe default
  - Optimized for Gemini File Search API compatibility
- **Upload Configuration**: Different config schemas for upload methods
  - `uploadToFileSearchStore`: Excludes MIME type (auto-detected)
  - `importFile`: Excludes display_name (only accepts custom_metadata and chunking_config)
- **Error Handling**: Enhanced error messages and logging
  - Detailed logging of upload attempts
  - Clear indication when fallback method is activated
  - Progress logging every 15 seconds during long uploads

### Technical Details

**File Changes**:
- `web_app/app.py`:
  - Added `mimetypes` import (line 11)
  - Expanded `ALLOWED_EXTENSIONS` set (lines 26-45)
  - Added `MIME_TYPE_MAPPING` dictionary (lines 49-135)
  - Implemented `get_mime_type()` function (lines 198-222)
  - Implemented dual-upload mechanism with try-catch fallback (lines 316-359)

**Implementation Pattern**:
```python
# Detect MIME type
mime_type = get_mime_type(filename)

# Try direct upload first
try:
    operation = client.file_search_stores.upload_to_file_search_store(...)
except Exception:
    # Fallback: Files API + importFile
    uploaded_file = client.files.upload(config={'mime_type': mime_type, ...})
    operation = client.file_search_stores.import_file(
        file_name=uploaded_file.name,
        config={...}  # No display_name here
    )
```

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

- **1.1.0** (2025-11-21) - Enhanced file upload system with 60+ formats and smart fallback
- **1.0.0** (2024-12-XX) - Initial production release with bilingual UI and AI metadata

---

## Migration Guides

### Upgrading from 1.0.0 to 1.1.0

#### Breaking Changes

**None**. Version 1.1.0 is fully backward compatible with 1.0.0.

#### What's New

- Files that previously failed to upload (CSV, XLSX, XLS, DOC) now work automatically
- 50+ additional file extensions are now supported
- More robust upload process with automatic retry
- Enhanced MIME type detection

#### Action Required

**None**. The application automatically uses the new upload system:
- Existing uploaded files are not affected
- No database migrations or state changes required
- No configuration changes needed

#### Testing Recommended

After upgrading, test the following:
1. Upload a CSV file (previously would fail with 500 error)
2. Upload an XLSX/XLS spreadsheet
3. Upload a DOC/DOCX document
4. Verify existing files still load correctly
5. Test chat functionality with new uploads

---

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

**Last Updated**: November 21, 2025
