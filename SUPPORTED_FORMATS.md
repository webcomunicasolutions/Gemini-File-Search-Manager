# Supported File Formats

This document lists all file formats supported by Google Gemini File Search API.

**Source**: [Official Gemini API Documentation](https://ai.google.dev/gemini-api/docs/file-search)

---

## Application File Types

The File Search API supports **30 application MIME types**:

```
application/dart
application/ecmascript
application/json
application/ms-java
application/msword
application/pdf
application/sql
application/typescript
application/vnd.curl
application/vnd.dart
application/vnd.ibm.secure-container
application/vnd.jupyter
application/vnd.ms-excel
application/vnd.oasis.opendocument.text
application/vnd.openxmlformats-officedocument.presentationml.presentation
application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
application/vnd.openxmlformats-officedocument.wordprocessingml.document
application/vnd.openxmlformats-officedocument.wordprocessingml.template
application/x-csh
application/x-hwp
application/x-hwp-v5
application/x-latex
application/x-php
application/x-powershell
application/x-sh
application/x-shellscript
application/x-tex
application/x-zsh
application/xml
application/zip
```

### Common Application Formats by Category

**Documents:**
- `.pdf` - PDF (Portable Document Format)
- `.doc`, `.docx` - Microsoft Word
- `.odt` - OpenDocument Text

**Spreadsheets:**
- `.xls`, `.xlsx` - Microsoft Excel
- `.ods` - OpenDocument Spreadsheet

**Presentations:**
- `.ppt`, `.pptx` - Microsoft PowerPoint
- `.odp` - OpenDocument Presentation

**Code & Scripts:**
- `.dart` - Dart source code
- `.ts` - TypeScript
- `.java` - Java source code
- `.php` - PHP scripts
- `.sh`, `.csh`, `.zsh` - Shell scripts
- `.ps1` - PowerShell scripts

**Data & Markup:**
- `.json` - JSON data
- `.xml` - XML data
- `.sql` - SQL scripts

**Scientific & Academic:**
- `.tex` - LaTeX documents
- `.ipynb` - Jupyter Notebooks

**Archives:**
- `.zip` - ZIP compressed archives

---

## Text File Types

The File Search API supports **170 text MIME types**:

```
text/1d-interleaved-parityfec
text/RED
text/SGML
text/cache-manifest
text/calendar
text/cql
text/cql-extension
text/cql-identifier
text/css
text/csv
text/csv-schema
text/dns
text/encaprtp
text/enriched
text/example
text/fhirpath
text/flexfec
text/fwdred
text/gff3
text/grammar-ref-list
text/hl7v2
text/html
text/javascript
text/jcr-cnd
text/jsx
text/markdown
text/mizar
text/n3
text/parameters
text/parityfec
text/php
text/plain
text/provenance-notation
text/prs.fallenstein.rst
text/prs.lines.tag
text/prs.prop.logic
text/raptorfec
text/rfc822-headers
text/rtf
text/rtp-enc-aescm128
text/rtploopback
text/rtx
text/sgml
text/shaclc
text/shex
text/spdx
text/strings
text/t140
text/tab-separated-values
text/texmacs
text/troff
text/tsv
text/tsx
text/turtle
text/ulpfec
text/uri-list
text/vcard
text/vnd.DMClientScript
text/vnd.IPTC.NITF
text/vnd.IPTC.NewsML
text/vnd.a
text/vnd.abc
text/vnd.ascii-art
text/vnd.curl
text/vnd.debian.copyright
text/vnd.dvb.subtitle
text/vnd.esmertec.theme-descriptor
text/vnd.exchangeable
text/vnd.familysearch.gedcom
text/vnd.ficlab.flt
text/vnd.fly
text/vnd.fmi.flexstor
text/vnd.gml
text/vnd.graphviz
text/vnd.hans
text/vnd.hgl
text/vnd.in3d.3dml
text/vnd.in3d.spot
text/vnd.latex-z
text/vnd.motorola.reflex
text/vnd.ms-mediapackage
text/vnd.net2phone.commcenter.command
text/vnd.radisys.msml-basic-layout
text/vnd.senx.warpscript
text/vnd.sosi
text/vnd.sun.j2me.app-descriptor
text/vnd.trolltech.linguist
text/vnd.wap.si
text/vnd.wap.sl
text/vnd.wap.wml
text/vnd.wap.wmlscript
text/vtt
text/wgsl
text/x-asm
text/x-bibtex
text/x-boo
text/x-c
text/x-c++hdr
text/x-c++src
text/x-cassandra
text/x-chdr
text/x-coffeescript
text/x-component
text/x-csh
text/x-csharp
text/x-csrc
text/x-cuda
text/x-d
text/x-diff
text/x-dsrc
text/x-emacs-lisp
text/x-erlang
text/x-gff3
text/x-go
text/x-haskell
text/x-java
text/x-java-properties
text/x-java-source
text/x-kotlin
text/x-lilypond
text/x-lisp
text/x-literate-haskell
text/x-lua
text/x-moc
text/x-objcsrc
text/x-pascal
text/x-pcs-gcd
text/x-perl
text/x-perl-script
text/x-python
text/x-python-script
text/x-r-markdown
text/x-rsrc
text/x-rst
text/x-ruby-script
text/x-rust
text/x-sass
text/x-scala
text/x-scheme
text/x-script.python
text/x-scss
text/x-setext
text/x-sfv
text/x-sh
text/x-siesta
text/x-sos
text/x-sql
text/x-swift
text/x-tcl
text/x-tex
text/x-vbasic
text/x-vcalendar
text/xml
text/xml-dtd
text/xml-external-parsed-entity
text/yaml
```

### Common Text Formats by Category

**Web Development:**
- `.html` - HTML documents
- `.css`, `.scss`, `.sass` - Stylesheets
- `.js`, `.jsx` - JavaScript
- `.ts`, `.tsx` - TypeScript

**Programming Languages:**
- `.py` - Python
- `.java` - Java
- `.c`, `.cpp`, `.h`, `.hpp` - C/C++
- `.cs` - C#
- `.go` - Go
- `.rs` - Rust
- `.php` - PHP
- `.rb` - Ruby
- `.swift` - Swift
- `.kt` - Kotlin
- `.scala` - Scala
- `.pl` - Perl
- `.r` - R
- `.hs` - Haskell
- `.erl` - Erlang
- `.lisp` - Lisp
- `.lua` - Lua
- `.tcl` - Tcl
- `.asm` - Assembly
- `.d` - D
- `.pas` - Pascal
- `.vb` - Visual Basic

**Data Formats:**
- `.txt` - Plain text
- `.csv` - Comma-separated values
- `.tsv` - Tab-separated values
- `.yaml`, `.yml` - YAML
- `.json` (also under application/)
- `.xml` (also under application/)
- `.sql` (also under application/)

**Markup & Documentation:**
- `.md`, `.markdown` - Markdown
- `.rst` - reStructuredText
- `.tex` - LaTeX
- `.rtf` - Rich Text Format
- `.sgml` - SGML

**Configuration & Scripts:**
- `.sh` - Shell scripts
- `.csh` - C Shell scripts
- `.properties` - Java properties
- `.conf` - Configuration files

**Semantic Web & RDF:**
- `.n3` - Notation3
- `.ttl` - Turtle
- `.shaclc` - SHACL Compact
- `.shex` - ShEx

**Other:**
- `.vcard`, `.vcf` - vCard (contact cards)
- `.ics` - iCalendar
- `.vtt` - WebVTT (video subtitles)
- `.wgsl` - WebGPU Shading Language
- `.bib`, `.bibtex` - BibTeX

---

## File Size Limitations

- **Maximum file size**: 100 MB per document
- **Recommended**: Keep each File Search store under 20 GB for optimal retrieval latencies
- **Storage limits by tier**:
  - Free: 1 GB
  - Tier 1: 10 GB
  - Tier 2: 100 GB
  - Tier 3: 1 TB

---

## Notes

1. **MIME Type Detection**: The API identifies files by their MIME type, not just file extension
2. **Text Extraction**: Files must contain extractable text content for indexing
3. **Binary Files**: Pure binary files without text content (e.g., images, audio, video) are not supported
4. **Encoding**: Files should use standard text encodings (UTF-8, ASCII, etc.)

---

## Quick Reference: Most Common Formats

For quick reference, here are the most commonly used formats:

| Category | Formats |
|----------|---------|
| **Documents** | PDF, DOCX, DOC, ODT, TXT, RTF |
| **Spreadsheets** | XLSX, XLS, ODS, CSV, TSV |
| **Presentations** | PPTX, PPT, ODP |
| **Web** | HTML, CSS, JS, TS |
| **Code** | PY, JAVA, C, CPP, GO, RS, PHP, RB |
| **Data** | JSON, XML, YAML, SQL |
| **Markup** | MD, RST, TEX |
| **Notebooks** | IPYNB |

---

**Total Supported Formats**: 200 MIME types (30 application + 170 text)

**Last Updated**: November 2024
**Source**: https://ai.google.dev/gemini-api/docs/file-search
