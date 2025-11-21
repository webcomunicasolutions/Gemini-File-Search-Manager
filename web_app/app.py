from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from google import genai
from google.genai import types
import os
import time
import json
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import logging
import mimetypes
from docx import Document as DocxDocument
from openpyxl import load_workbook

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure logging - Configuración de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration constants - Constantes de configuración
UPLOAD_FOLDER = 'uploads'
# Expanded allowed extensions to match all File Search supported formats
ALLOWED_EXTENSIONS = {
    # Documents
    'txt', 'pdf', 'doc', 'docx', 'odt', 'rtf', 'md', 'markdown',
    # Spreadsheets
    'csv', 'tsv', 'xlsx', 'xls', 'xlsm', 'xlsb', 'ods',
    # Presentations
    'pptx', 'ppt', 'odp',
    # Data formats
    'json', 'xml', 'yaml', 'yml', 'sql',
    # Code files
    'py', 'js', 'jsx', 'ts', 'tsx', 'java', 'c', 'cpp', 'h', 'hpp',
    'cs', 'go', 'rs', 'php', 'rb', 'swift', 'kt', 'scala', 'pl',
    'r', 'hs', 'erl', 'lisp', 'lua', 'sh', 'bash', 'zsh', 'dart',
    # Web
    'html', 'htm', 'css', 'scss', 'sass',
    # Scientific
    'ipynb', 'bib', 'bibtex', 'tex',
    # Archives
    'zip'
}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
MAX_HISTORY = 7  # Conversation history limit - Límite de historial de conversación

# Complete MIME type mapping for Gemini File Search API
# Based on official documentation: https://ai.google.dev/gemini-api/docs/file-search
MIME_TYPE_MAPPING = {
    # Documents
    'pdf': 'application/pdf',
    'doc': 'application/msword',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'odt': 'application/vnd.oasis.opendocument.text',
    'rtf': 'text/rtf',
    'txt': 'text/plain',
    'md': 'text/markdown',
    'markdown': 'text/markdown',

    # Spreadsheets (CRITICAL - These were failing without explicit MIME types)
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'xls': 'application/vnd.ms-excel',
    'xlsm': 'application/vnd.ms-excel.sheet.macroEnabled.12',
    'xlsb': 'application/vnd.ms-excel.sheet.binary.macroEnabled.12',
    'csv': 'text/csv',
    'tsv': 'text/tab-separated-values',
    'ods': 'application/vnd.oasis.opendocument.spreadsheet',

    # Presentations
    'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'ppt': 'application/vnd.ms-powerpoint',
    'odp': 'application/vnd.oasis.opendocument.presentation',

    # Data formats
    'json': 'application/json',
    'xml': 'application/xml',
    'yaml': 'text/yaml',
    'yml': 'text/yaml',
    'sql': 'application/sql',

    # Programming Languages
    'py': 'text/x-python',
    'js': 'text/javascript',
    'jsx': 'text/jsx',
    'ts': 'application/typescript',
    'tsx': 'text/tsx',
    'java': 'text/x-java',
    'c': 'text/x-c',
    'cpp': 'text/x-c++src',
    'cc': 'text/x-c++src',
    'cxx': 'text/x-c++src',
    'h': 'text/x-chdr',
    'hpp': 'text/x-c++hdr',
    'cs': 'text/x-csharp',
    'go': 'text/x-go',
    'rs': 'text/x-rust',
    'php': 'application/x-php',
    'rb': 'text/x-ruby-script',
    'swift': 'text/x-swift',
    'kt': 'text/x-kotlin',
    'scala': 'text/x-scala',
    'pl': 'text/x-perl',
    'r': 'text/x-rsrc',
    'hs': 'text/x-haskell',
    'erl': 'text/x-erlang',
    'lisp': 'text/x-lisp',
    'lua': 'text/x-lua',
    'sh': 'application/x-sh',
    'bash': 'application/x-sh',
    'zsh': 'application/x-zsh',
    'dart': 'application/vnd.dart',

    # Web Technologies
    'html': 'text/html',
    'htm': 'text/html',
    'css': 'text/css',
    'scss': 'text/x-scss',
    'sass': 'text/x-sass',

    # Scientific & Academic
    'ipynb': 'application/vnd.jupyter',
    'bib': 'text/x-bibtex',
    'bibtex': 'text/x-bibtex',
    'tex': 'application/x-tex',

    # Archives
    'zip': 'application/zip',

    # Other
    'ics': 'text/calendar',
    'vcard': 'text/vcard',
    'vcf': 'text/vcard'
}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize Gemini client - API key del usuario
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set GEMINI_API_KEY in your .env file")

client = genai.Client(api_key=api_key)

# Global state management - Gestión de estado global
conversation_history = []
file_search_store = None
uploaded_files = []  # Track uploaded files with metadata
PERSISTENCE_FILE = 'store_state.json'

# ============================================
# STATE PERSISTENCE FUNCTIONS - Funciones de persistencia de estado
# ============================================

def load_state():
    """Load persisted state from JSON file on startup - Cargar estado persistido desde archivo JSON"""
    global file_search_store, uploaded_files
    try:
        if os.path.exists(PERSISTENCE_FILE):
            with open(PERSISTENCE_FILE, 'r') as f:
                state = json.load(f)
                store_name = state.get('store_name')
                uploaded_files = state.get('uploaded_files', [])

                if store_name:
                    # Verify the store still exists
                    try:
                        file_search_store = client.file_search_stores.get(name=store_name)
                        logger.info(f"Restored file search store: {store_name} with {len(uploaded_files)} files")
                    except Exception as e:
                        logger.warning(f"Stored file search store not found: {e}")
                        file_search_store = None
                        uploaded_files = []
    except Exception as e:
        logger.error(f"Error loading state: {e}")

def save_state():
    """Save current state to JSON file - Guardar estado actual a archivo JSON"""
    try:
        state = {
            'store_name': file_search_store.name if file_search_store else None,
            'uploaded_files': uploaded_files
        }
        with open(PERSISTENCE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
        logger.info("State saved successfully")
    except Exception as e:
        logger.error(f"Error saving state: {e}")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_mime_type(filename):
    """
    Detect MIME type from file extension with fallback.

    Args:
        filename (str): Name of the file

    Returns:
        str: MIME type string
    """
    # Get file extension
    file_ext = filename.lower().rsplit('.', 1)[-1] if '.' in filename else ''

    # Priority 1: Check manual mapping (most reliable for File Search API)
    if file_ext in MIME_TYPE_MAPPING:
        return MIME_TYPE_MAPPING[file_ext]

    # Priority 2: Fallback to mimetypes module
    mime_type, _ = mimetypes.guess_type(filename)
    if mime_type:
        return mime_type

    # Priority 3: Safe default
    logger.warning(f"Could not determine MIME type for {filename}, using default")
    return 'application/octet-stream'

def extract_text_from_docx(file_path):
    """
    Extract text content from a DOCX file.

    Args:
        file_path (str): Path to the DOCX file

    Returns:
        str: Extracted text content
    """
    try:
        doc = DocxDocument(file_path)
        paragraphs = []

        # Extract all paragraphs
        for para in doc.paragraphs:
            if para.text.strip():
                paragraphs.append(para.text)

        # Extract text from tables
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    if cell.text.strip():
                        paragraphs.append(cell.text)

        text = '\n'.join(paragraphs)
        logger.info(f"Extracted {len(text)} characters from DOCX")
        return text

    except Exception as e:
        logger.error(f"Error extracting text from DOCX: {str(e)}")
        return ""

def extract_text_from_xlsx(file_path):
    """
    Extract text content from an XLSX file.

    Args:
        file_path (str): Path to the XLSX file

    Returns:
        str: Extracted text content
    """
    wb = None
    try:
        wb = load_workbook(filename=file_path, read_only=True, data_only=True)
        text_parts = []

        for sheet_name in wb.sheetnames:
            sheet = wb[sheet_name]
            text_parts.append(f"=== Sheet: {sheet_name} ===")

            # Read up to 100 rows to avoid overwhelming the model
            max_rows = min(sheet.max_row, 100) if sheet.max_row else 100

            for row in sheet.iter_rows(min_row=1, max_row=max_rows, values_only=True):
                # Convert row values to strings, skip empty rows
                row_text = ' | '.join([str(cell) if cell is not None else '' for cell in row])
                if row_text.strip():
                    text_parts.append(row_text)

        text = '\n'.join(text_parts)
        logger.info(f"Extracted {len(text)} characters from XLSX ({len(wb.sheetnames)} sheets)")
        return text

    except Exception as e:
        logger.error(f"Error extracting text from XLSX: {str(e)}")
        return ""
    finally:
        # IMPORTANT: Always close the workbook to release file handle
        if wb is not None:
            try:
                wb.close()
                logger.info("XLSX workbook closed successfully")
            except Exception as close_error:
                logger.warning(f"Error closing workbook: {close_error}")

# ============================================
# MAIN ROUTES - Rutas principales
# ============================================

@app.route('/')
def index():
    return render_template('index.html')

# ============================================
# FILE UPLOAD WITH PERSISTENCE - Carga de archivos con persistencia
# Timeout de 120 segundos configurado
# ============================================

@app.route('/upload', methods=['POST'])
def upload_file():
    global file_search_store, uploaded_files

    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not supported'}), 400

    filepath = None

    try:
        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Get file size
        file_size = os.path.getsize(filepath)
        logger.info(f"File saved: {filename}, size: {file_size} bytes")

        # Get custom metadata and chunking config from request
        metadata_json = request.form.get('metadata', '{}')
        chunking_json = request.form.get('chunking_config', '{}')
        store_name_param = request.form.get('store_name', '')
        custom_metadata = json.loads(metadata_json)
        chunking_config = json.loads(chunking_json)

        # Determine which store to use
        target_store = None
        if store_name_param:
            # Use the specified store
            logger.info(f"Using specified store: {store_name_param}")
            target_store_name = store_name_param
        elif file_search_store is None:
            # Create new default store if none exists
            logger.info("Creating new file search store")
            file_search_store = client.file_search_stores.create(
                config={'display_name': 'RAG-App-Store'}
            )
            target_store_name = file_search_store.name
        else:
            # Use existing default store
            target_store_name = file_search_store.name

        # Detect MIME type explicitly (CRITICAL for CSV, XLSX, etc.)
        mime_type = get_mime_type(filename)
        logger.info(f"Detected MIME type: {mime_type} for {filename}")

        # Build upload config WITHOUT MIME type (will be auto-detected)
        upload_config = {
            'display_name': filename
        }

        # Add custom metadata if provided
        if custom_metadata:
            metadata_list = []
            for key, value in custom_metadata.items():
                if isinstance(value, (int, float)):
                    metadata_list.append({"key": key, "numeric_value": value})
                else:
                    metadata_list.append({"key": key, "string_value": str(value)})
            upload_config['custom_metadata'] = metadata_list

        # Add chunking config if provided
        if chunking_config and chunking_config.get('enabled'):
            upload_config['chunking_config'] = {
                'white_space_config': {
                    'max_tokens_per_chunk': chunking_config.get('max_tokens_per_chunk', 200),
                    'max_overlap_tokens': chunking_config.get('max_overlap_tokens', 20)
                }
            }

        # TRY DIRECT UPLOAD FIRST (upload_to_file_search_store)
        uploaded_api_file = None
        try:
            logger.info(f"Attempting direct upload for {filename} (MIME type will be auto-detected)")
            operation = client.file_search_stores.upload_to_file_search_store(
                file=filepath,
                file_search_store_name=target_store_name,
                config=upload_config
            )
        except Exception as upload_error:
            # FALLBACK: Use Files API + importFile for problematic files (CSV, large files, etc.)
            logger.warning(f"Direct upload failed: {upload_error}")
            logger.info(f"Falling back to Files API + importFile method for {filename}")

            try:
                # Upload to Files API with explicit MIME type
                uploaded_api_file = client.files.upload(
                    file=filepath,
                    config={
                        'mime_type': mime_type,  # Files API DOES accept mime_type
                        'display_name': filename
                    }
                )
                logger.info(f"File uploaded to Files API: {uploaded_api_file.name}")

                # Import to File Search Store (importFile has different config schema)
                import_config_fallback = {}

                # importFile accepts custom_metadata and chunking_config, but NOT display_name
                if upload_config.get('custom_metadata'):
                    import_config_fallback['custom_metadata'] = upload_config['custom_metadata']
                if upload_config.get('chunking_config'):
                    import_config_fallback['chunking_config'] = upload_config['chunking_config']

                operation = client.file_search_stores.import_file(
                    file_search_store_name=target_store_name,
                    file_name=uploaded_api_file.name,
                    config=import_config_fallback if import_config_fallback else None
                )
                logger.info(f"Importing {filename} into File Search Store via importFile")

            except Exception as fallback_error:
                logger.error(f"Fallback method also failed: {fallback_error}")
                raise fallback_error

        # Wait for operation to complete with INCREASED TIMEOUT - 120 segundos
        logger.info("Waiting for file import to complete")
        max_wait = 120  # 2 minutes timeout - Timeout de 120 segundos
        wait_time = 0
        while not operation.done and wait_time < max_wait:
            time.sleep(3)
            operation = client.operations.get(operation)
            wait_time += 3
            if wait_time % 15 == 0:  # Log progress every 15 seconds
                logger.info(f"Still waiting... ({wait_time}s elapsed)")

        if not operation.done:
            logger.error(f"File processing timeout after {max_wait}s")
            return jsonify({'error': f'File processing timeout after {max_wait} seconds. The file may still be processing in the background.'}), 500

        # Extract document ID from operation response
        document_id = None
        if hasattr(operation, 'response') and operation.response:
            document_id = getattr(operation.response, 'name', None)

        # Check for operation errors
        if hasattr(operation, 'error') and operation.error:
            logger.error(f"Upload operation failed: {operation.error.message}")
            return jsonify({'error': f'Upload failed: {operation.error.message}'}), 500

        # Track uploaded file
        file_info = {
            'filename': filename,
            'size': file_size,
            'mime_type': mime_type,  # Store MIME type for debugging
            'uploaded_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'custom_metadata': custom_metadata,
            'chunking_config': chunking_config if chunking_config.get('enabled') else None,
            'document_id': document_id
        }
        uploaded_files.append(file_info)

        # IMPORTANT: Save state to persistence - Guardar estado
        save_state()

        # Clean up local file
        os.remove(filepath)
        logger.info(f"File {filename} successfully uploaded and imported")

        return jsonify({
            'success': True,
            'message': f'File "{filename}" uploaded and processed successfully',
            'filename': filename,
            'file_size': file_size,
            'mime_type': mime_type,
            'store_name': target_store_name,
            'document_id': document_id,
            'uploaded_files': uploaded_files
        })

    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        # Clean up file if it exists
        if filepath and os.path.exists(filepath):
            os.remove(filepath)
        # Clean up API file if uploaded in fallback
        if uploaded_api_file:
            try:
                client.files.delete(uploaded_api_file.name)
                logger.info(f"Cleaned up temporary file: {uploaded_api_file.name}")
            except:
                pass
        return jsonify({'error': f'Error uploading file: {str(e)}'}), 500

# ============================================
# CHAT WITH RAG & CITATIONS - Chat con RAG y citaciones
# Incluye MAX_HISTORY = 7 para límite de conversación
# ============================================

@app.route('/chat', methods=['POST'])
def chat():
    global conversation_history

    data = request.json
    user_message = data.get('message', '')
    metadata_filters = data.get('metadata_filters', [])  # Array de filtros del frontend
    system_prompt = data.get('system_prompt', '')

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    if file_search_store is None:
        return jsonify({'error': 'Please upload a file first'}), 400

    try:
        # Add user message to history
        conversation_history.append({
            'role': 'user',
            'content': user_message
        })

        # Build conversation context (last MAX_HISTORY messages) - Contexto de conversación
        context_messages = conversation_history[-MAX_HISTORY:]

        # Create prompt with conversation history
        prompt_parts = []

        # Add system prompt at the beginning if provided
        if system_prompt:
            prompt_parts.append(f"System Instructions: {system_prompt}\n")

        for msg in context_messages[:-1]:  # All except current message
            if msg['role'] == 'user':
                prompt_parts.append(f"User: {msg['content']}")
            else:
                prompt_parts.append(f"Assistant: {msg['content']}")

        # Add current question
        prompt_parts.append(f"User: {user_message}")
        prompt_parts.append("Assistant:")

        full_prompt = "\n\n".join(prompt_parts)

        logger.info(f"Querying with message: {user_message}")
        if metadata_filters:
            logger.info(f"Using metadata filters: {metadata_filters}")

        # Build file search config
        file_search_config = types.FileSearch(
            file_search_store_names=[file_search_store.name]
        )

        # Add metadata filters if provided - Convertir al formato de Gemini API
        if metadata_filters and len(metadata_filters) > 0:
            # Construir metadata filters según formato de Gemini
            # Formato: metadataFilters=[{key: "chunk.custom_metadata.X", conditions: [{stringValue: "Y", operation: "EQUAL"}]}]
            gemini_filters = []

            for filter_item in metadata_filters:
                key = filter_item.get('key', '')
                value = filter_item.get('value', '')

                if not key or not value:
                    continue

                # Determinar si el valor es numérico o string
                is_numeric = False
                numeric_value = None
                try:
                    numeric_value = float(value)
                    is_numeric = True
                except (ValueError, TypeError):
                    pass

                # Construir el filtro en formato Gemini
                filter_condition = {
                    'key': f'chunk.custom_metadata.{key}',
                    'conditions': []
                }

                if is_numeric:
                    filter_condition['conditions'].append({
                        'numericValue': numeric_value,
                        'operation': 'EQUAL'
                    })
                else:
                    filter_condition['conditions'].append({
                        'stringValue': str(value),
                        'operation': 'EQUAL'
                    })

                gemini_filters.append(filter_condition)

            if gemini_filters:
                file_search_config.metadata_filters = gemini_filters
                logger.info(f"Applied {len(gemini_filters)} metadata filter(s) to search")

        # Query with File Search
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(file_search=file_search_config)]
            )
        )

        assistant_message = response.text

        # Add assistant response to history
        conversation_history.append({
            'role': 'assistant',
            'content': assistant_message
        })

        # Keep only last MAX_HISTORY messages
        if len(conversation_history) > MAX_HISTORY:
            conversation_history = conversation_history[-MAX_HISTORY:]

        # Extract grounding metadata (citations) - Extracción de citaciones
        metadata = None
        if response.candidates and len(response.candidates) > 0:
            candidate = response.candidates[0]
            if hasattr(candidate, 'grounding_metadata') and candidate.grounding_metadata:
                grounding = candidate.grounding_metadata

                # Extract citation information
                citations = []
                if hasattr(grounding, 'grounding_chunks') and grounding.grounding_chunks:
                    for chunk in grounding.grounding_chunks:
                        if hasattr(chunk, 'retrieved_context'):
                            ctx = chunk.retrieved_context
                            citation = {}
                            if hasattr(ctx, 'title'):
                                citation['title'] = ctx.title
                            if hasattr(ctx, 'uri'):
                                citation['uri'] = ctx.uri
                            if hasattr(ctx, 'text'):
                                citation['text'] = ctx.text
                            citations.append(citation)

                metadata = {
                    'citations': citations,
                    'citation_count': len(citations)
                }

        logger.info(f"Response generated successfully with {len(metadata['citations']) if metadata else 0} citations")

        return jsonify({
            'success': True,
            'response': assistant_message,
            'metadata': metadata,
            'conversation_length': len(conversation_history),
            'metadata_filters_applied': metadata_filters if metadata_filters else None,
            'filters_count': len(metadata_filters) if metadata_filters else 0
        })

    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        return jsonify({'error': f'Error processing message: {str(e)}'}), 500

# ============================================
# FILE MANAGEMENT ENDPOINTS - Endpoints de gestión de archivos
# ============================================

@app.route('/delete-file/<int:file_index>', methods=['DELETE'])
def delete_file(file_index):
    global uploaded_files

    try:
        if file_index < 0 or file_index >= len(uploaded_files):
            return jsonify({'error': 'Invalid file index'}), 400

        file_info = uploaded_files[file_index]

        # Delete from Files API
        if file_info.get('file_api_name'):
            try:
                client.files.delete(file_info['file_api_name'])
                logger.info(f"Deleted file from Files API: {file_info['file_api_name']}")
            except Exception as e:
                logger.warning(f"Could not delete from Files API: {str(e)}")

        # Remove from tracking
        deleted_file = uploaded_files.pop(file_index)
        logger.info(f"Removed file from tracking: {deleted_file['filename']}")

        # Save state to persistence
        save_state()

        return jsonify({
            'success': True,
            'message': f"File '{deleted_file['filename']}' deleted successfully",
            'uploaded_files': uploaded_files
        })

    except Exception as e:
        logger.error(f"Error deleting file: {str(e)}")
        return jsonify({'error': f'Error deleting file: {str(e)}'}), 500

@app.route('/store-info', methods=['GET'])
def get_store_info():
    try:
        if file_search_store is None:
            return jsonify({
                'success': True,
                'store_exists': False,
                'message': 'No file search store created yet'
            })

        # Get store details
        store_details = client.file_search_stores.get(name=file_search_store.name)

        store_info = {
            'success': True,
            'store_exists': True,
            'name': store_details.name,
            'display_name': getattr(store_details, 'display_name', 'N/A'),
            'create_time': getattr(store_details, 'create_time', 'N/A'),
            'update_time': getattr(store_details, 'update_time', 'N/A'),
            'document_count': len(uploaded_files)
        }

        return jsonify(store_info)

    except Exception as e:
        logger.error(f"Error getting store info: {str(e)}")
        return jsonify({'error': f'Error getting store info: {str(e)}'}), 500

@app.route('/stores', methods=['GET'])
def list_stores():
    """List all File Search stores with their documents - Listar todos los stores con sus documentos"""
    try:
        stores = []
        for store in client.file_search_stores.list():
            # Get documents for this store
            documents = []
            try:
                for doc in client.file_search_stores.documents.list(parent=store.name):
                    # Extract custom metadata from Gemini
                    custom_metadata = {}
                    if hasattr(doc, 'custom_metadata') and doc.custom_metadata:
                        for metadata in doc.custom_metadata:
                            key = getattr(metadata, 'key', '')
                            if hasattr(metadata, 'string_value'):
                                custom_metadata[key] = getattr(metadata, 'string_value', '')
                            elif hasattr(metadata, 'numeric_value'):
                                custom_metadata[key] = getattr(metadata, 'numeric_value', 0)

                    # Merge with local metadata edits (local metadata takes precedence)
                    for file_info in uploaded_files:
                        if file_info.get('document_id') == doc.name:
                            local_metadata = file_info.get('custom_metadata', {})
                            custom_metadata.update(local_metadata)  # Local overrides Gemini
                            break

                    documents.append({
                        'name': doc.name,
                        'display_name': getattr(doc, 'display_name', 'N/A'),
                        'displayName': getattr(doc, 'display_name', 'N/A'),
                        'state': getattr(doc, 'state', 'UNKNOWN'),
                        'size_bytes': getattr(doc, 'size_bytes', 0),
                        'sizeBytes': getattr(doc, 'size_bytes', 0),
                        'mime_type': getattr(doc, 'mime_type', 'N/A'),
                        'mimeType': getattr(doc, 'mime_type', 'N/A'),
                        'create_time': str(getattr(doc, 'create_time', 'N/A')),
                        'createTime': str(getattr(doc, 'create_time', 'N/A')),
                        'custom_metadata': custom_metadata,
                        'customMetadata': custom_metadata
                    })
            except Exception as doc_error:
                logger.warning(f"Error listing documents for store {store.name}: {str(doc_error)}")

            stores.append({
                'name': store.name,
                'display_name': getattr(store, 'display_name', 'N/A'),
                'displayName': getattr(store, 'display_name', 'N/A'),
                'create_time': str(getattr(store, 'create_time', 'N/A')),
                'createTime': str(getattr(store, 'create_time', 'N/A')),
                'active_documents_count': getattr(store, 'active_documents_count', 0),
                'activeDocumentsCount': getattr(store, 'active_documents_count', 0),
                'pending_documents_count': getattr(store, 'pending_documents_count', 0),
                'pendingDocumentsCount': getattr(store, 'pending_documents_count', 0),
                'failed_documents_count': getattr(store, 'failed_documents_count', 0),
                'failedDocumentsCount': getattr(store, 'failed_documents_count', 0),
                'documents': documents
            })

        # Get current store name
        current_store_name = file_search_store.name if file_search_store else None

        return jsonify({
            'success': True,
            'stores': stores,
            'count': len(stores),
            'current_store': current_store_name
        })

    except Exception as e:
        logger.error(f"Error listing stores: {str(e)}")
        return jsonify({'error': f'Error listing stores: {str(e)}'}), 500

@app.route('/delete-store', methods=['DELETE'])
def delete_store():
    """Delete a File Search store (with all documents) - Eliminar store con todos los documentos"""
    global file_search_store, uploaded_files

    try:
        # Get store name from request body or use current store
        data = request.get_json() or {}
        store_name = data.get('store_name')

        # If no store name provided, use current store
        if not store_name:
            if file_search_store is None:
                return jsonify({'error': 'No store specified and no current store'}), 400
            store_name = file_search_store.name

        # Delete the store with force=True (deletes all documents automatically)
        client.file_search_stores.delete(name=store_name, config={'force': True})
        logger.info(f"Deleted file search store: {store_name}")

        # Reset state if we deleted the current store
        if file_search_store and file_search_store.name == store_name:
            file_search_store = None
            uploaded_files = []
            save_state()

        return jsonify({
            'success': True,
            'message': f'File search store deleted successfully: {store_name}'
        })

    except Exception as e:
        logger.error(f"Error deleting store: {str(e)}")
        return jsonify({'error': f'Error deleting store: {str(e)}'}), 500

# ============================================
# API DOCUMENTATION & INFO ENDPOINTS - Endpoints de documentación API
# ============================================

@app.route('/api-info', methods=['GET'])
def get_api_info():
    """Return API information for documentation tab - Devolver información API para pestaña de documentación"""
    try:
        api_info = {
            'success': True,
            'api_key': api_key,
            'store_exists': file_search_store is not None,
            'store_name': file_search_store.name if file_search_store else None,
            'store_display_name': getattr(file_search_store, 'display_name', 'RAG-App-Store') if file_search_store else 'RAG-App-Store',
            'file_count': len(uploaded_files),
            'files': uploaded_files,
            'model': 'gemini-2.5-flash',
            'example_metadata_filters': []
        }

        # Collect example metadata keys from uploaded files
        metadata_keys = set()
        for file_info in uploaded_files:
            if file_info.get('custom_metadata'):
                for key in file_info['custom_metadata'].keys():
                    metadata_keys.add(key)

        api_info['metadata_keys'] = list(metadata_keys)

        return jsonify(api_info)

    except Exception as e:
        logger.error(f"Error getting API info: {str(e)}")
        return jsonify({'error': f'Error getting API info: {str(e)}'}), 500

@app.route('/update-api-key', methods=['POST'])
def update_api_key():
    """Update API key in .env file and reinitialize client - Actualizar API key"""
    global api_key, client
    try:
        data = request.json
        new_api_key = data.get('api_key', '').strip()

        if not new_api_key:
            return jsonify({'error': 'API key cannot be empty'}), 400

        # Update .env file
        env_path = '.env'
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                lines = f.readlines()

            with open(env_path, 'w') as f:
                found = False
                for line in lines:
                    if line.startswith('GEMINI_API_KEY='):
                        f.write(f'GEMINI_API_KEY={new_api_key}\n')
                        found = True
                    else:
                        f.write(line)

                if not found:
                    f.write(f'\nGEMINI_API_KEY={new_api_key}\n')
        else:
            with open(env_path, 'w') as f:
                f.write(f'GEMINI_API_KEY={new_api_key}\n')

        # Update runtime variable and reinitialize client
        api_key = new_api_key
        client = genai.Client(api_key=api_key)

        logger.info("API key updated successfully")
        return jsonify({'success': True, 'message': 'API key updated successfully. Please reload the page.'})

    except Exception as e:
        logger.error(f"Error updating API key: {str(e)}")
        return jsonify({'error': f'Error updating API key: {str(e)}'}), 500

@app.route('/create-store', methods=['POST'])
def create_store():
    """Create a new File Search Store - Crear un nuevo File Search Store"""
    global file_search_store, uploaded_files
    try:
        data = request.json
        display_name = data.get('display_name', '').strip()

        if not display_name:
            return jsonify({'error': 'Display name is required'}), 400

        logger.info(f"Creating new File Search Store: {display_name}")

        # Create new store
        new_store = client.file_search_stores.create(
            config={'display_name': display_name}
        )

        logger.info(f"Created File Search Store: {new_store.name}")

        # Switch to the new store
        file_search_store = new_store
        uploaded_files = []

        # Save state
        save_state()

        return jsonify({
            'success': True,
            'store_name': new_store.name,
            'display_name': new_store.display_name,
            'message': f'Store "{display_name}" created successfully'
        })

    except Exception as e:
        logger.error(f"Error creating store: {str(e)}")
        return jsonify({'error': f'Error creating store: {str(e)}'}), 500

@app.route('/switch-store', methods=['POST'])
def switch_store():
    """Switch to a different File Search Store - Cambiar a otro store"""
    global file_search_store, uploaded_files
    try:
        data = request.json
        store_name = data.get('store_name', '').strip()

        if not store_name:
            return jsonify({'error': 'Store name is required'}), 400

        # Verify the store exists
        try:
            new_store = client.file_search_stores.get(name=store_name)
            file_search_store = new_store

            # Reset uploaded files list (will be loaded from store if needed)
            uploaded_files = []

            # Save new state
            save_state()

            logger.info(f"Switched to store: {store_name}")
            return jsonify({
                'success': True,
                'message': f'Switched to store: {store_name}',
                'store': {
                    'name': new_store.name,
                    'display_name': new_store.display_name or new_store.name.split('/')[-1],
                    'active_documents_count': new_store.active_documents_count or 0
                }
            })
        except Exception as e:
            return jsonify({'error': f'Store not found: {str(e)}'}), 404

    except Exception as e:
        logger.error(f"Error switching store: {str(e)}")
        return jsonify({'error': f'Error switching store: {str(e)}'}), 500

@app.route('/delete-document', methods=['DELETE'])
def delete_document():
    """Delete a specific document from a store - Eliminar un documento específico de un store"""
    global uploaded_files
    try:
        data = request.json
        document_name = data.get('document_name', '').strip()

        if not document_name:
            return jsonify({'error': 'Document name is required'}), 400

        # Delete the document with force=True
        try:
            client.file_search_stores.documents.delete(name=document_name, config={'force': True})
            logger.info(f"Deleted document: {document_name}")

            # If this document belongs to the current store, update uploaded_files
            if file_search_store and document_name.startswith(file_search_store.name):
                # Remove from uploaded_files if exists
                uploaded_files = [f for f in uploaded_files if f.get('document_id') != document_name]
                save_state()

            return jsonify({
                'success': True,
                'message': f'Document deleted successfully',
                'document_name': document_name
            })
        except Exception as e:
            return jsonify({'error': f'Document not found or could not be deleted: {str(e)}'}), 404

    except Exception as e:
        logger.error(f"Error deleting document: {str(e)}")
        return jsonify({'error': f'Error deleting document: {str(e)}'}), 500

@app.route('/update-document-metadata', methods=['POST'])
def update_document_metadata():
    """Update metadata for a document - Actualizar metadatos de un documento"""
    global uploaded_files
    try:
        data = request.json
        document_name = data.get('document_name', '').strip()
        new_metadata = data.get('metadata', {})

        if not document_name:
            return jsonify({'error': 'Document name is required'}), 400

        # Update metadata in local storage
        updated = False
        for file_info in uploaded_files:
            if file_info.get('document_id') == document_name:
                file_info['custom_metadata'] = new_metadata
                file_info['metadata_updated_at'] = time.strftime('%Y-%m-%d %H:%M:%S')
                updated = True
                break

        # If not found in uploaded_files, add new entry
        if not updated:
            uploaded_files.append({
                'document_id': document_name,
                'custom_metadata': new_metadata,
                'metadata_updated_at': time.strftime('%Y-%m-%d %H:%M:%S')
            })

        save_state()
        logger.info(f"Updated metadata for document: {document_name}")

        return jsonify({
            'success': True,
            'message': 'Metadata updated successfully',
            'document_name': document_name,
            'metadata': new_metadata
        })

    except Exception as e:
        logger.error(f"Error updating document metadata: {str(e)}")
        return jsonify({'error': f'Error updating metadata: {str(e)}'}), 500

@app.route('/suggest-metadata', methods=['POST'])
def suggest_metadata():
    """Analyze document with Gemini and suggest metadata - Sugerir metadatos con IA"""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Get model preference (default to gemini-2.5-flash)
        model = request.form.get('model', 'gemini-2.5-flash')

        # Get language preference (default to 'en')
        language = request.form.get('language', 'en')
        logger.info(f"Using model for metadata generation: {model}, language: {language}")

        # Read file content
        file_content = file.read()
        file.seek(0)  # Reset file pointer for potential reuse

        # Determine mime type using our smart detection function
        mime_type = get_mime_type(file.filename)

        logger.info(f"Analyzing document: {file.filename} ({mime_type})")

        # Save file temporarily
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        file.save(temp_path)

        # Determine if we need to extract text or use Files API
        use_text_extraction = mime_type in [
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # DOCX
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # XLSX
            'application/vnd.ms-excel',  # XLS
            'application/msword'  # DOC (old format)
        ]

        if use_text_extraction:
            # Extract text for unsupported formats (DOCX, XLSX)
            logger.info(f"Extracting text from {mime_type} file")

            if 'wordprocessingml' in mime_type or mime_type == 'application/msword':
                # DOCX or DOC
                extracted_text = extract_text_from_docx(temp_path)
            elif 'spreadsheetml' in mime_type or mime_type == 'application/vnd.ms-excel':
                # XLSX or XLS
                extracted_text = extract_text_from_xlsx(temp_path)
            else:
                extracted_text = ""

            if not extracted_text:
                raise Exception("Could not extract text from document")

            logger.info(f"Extracted {len(extracted_text)} characters")
            uploaded_file = None  # No uploaded file for text extraction
        else:
            # Upload file to Gemini Files API for supported formats (PDF, images, etc.)
            logger.info(f"Uploading to Files API: {mime_type}")
            uploaded_file = client.files.upload(
                file=temp_path,
                config={
                    'mime_type': mime_type,
                    'display_name': file.filename
                }
            )

        # System prompt with best practices - BILINGUAL VERSION
        if language == 'es':
            system_instruction = """Eres un asistente experto en análisis de documentos y gestión de metadatos para sistemas RAG (Retrieval Augmented Generation).

Tu trabajo es analizar documentos y extraer metadatos útiles que permitan:
1. Búsquedas eficientes por tipo, categoría, fecha, autor, etc.
2. Filtrado preciso en consultas RAG
3. Organización inteligente de información

FILOSOFÍA: CALIDAD sobre CANTIDAD
- Sugiere entre 5-12 campos de metadatos (máximo 20 solo si es absolutamente necesario)
- Cada campo de metadatos debe tener un propósito claro para búsqueda o filtrado
- Evita redundancias y campos triviales
- Si un campo no añade valor real para encontrar el documento, NO lo incluyas

REGLAS DE EXTRACCIÓN:
- Nombres de campos: minúsculas, sin espacios, usa guiones bajos
- Valores: strings simples o números, no arrays ni objetos
- Solo incluye metadatos que aparezcan explícitamente en el documento
- Prioriza metadatos que realmente diferencien este documento de otros
- IMPORTANTE: Todos los valores de metadatos deben estar EN ESPAÑOL

TIPOS DE DOCUMENTOS COMUNES:
- Facturas: numero_factura, proveedor, cliente, importe, fecha, estado
- Contratos: partes, fecha_firma, vigencia, valor, area, estado
- Informes: autor, departamento, periodo, tipo, confidencialidad
- Manuales: producto, version, idioma, categoria
- Emails: remitente, destinatario, asunto, fecha, prioridad

METADATOS UNIVERSALES (si aplican):
- titulo: título descriptivo del documento (extraído del contenido, NO del nombre de archivo)
- tipo: categoría del documento
- fecha: fecha principal (formato YYYY-MM-DD)
- autor: creador o responsable
- departamento: área organizacional
- confidencialidad: publico/interno/confidencial/privado
- estado: activo/pendiente/archivado/etc
- etiquetas: palabras clave (máximo 5, separadas por comas)

IMPORTANTE SOBRE EL TÍTULO:
- Debe extraerse del CONTENIDO del documento (encabezado, primera página, asunto)
- NO uses el nombre de archivo como título
- Debe ser descriptivo y profesional
- Formato: "Tipo de Documento - Descripción Breve"
- Ejemplo: "Factura de Servicios - Microsoft Azure Noviembre 2024"

Responde SOLO con JSON válido, sin markdown ni explicaciones."""
        else:
            system_instruction = """You are an expert assistant in document analysis and metadata management for RAG (Retrieval Augmented Generation) systems.

Your job is to analyze documents and extract useful metadata that enables:
1. Efficient searches by type, category, date, author, etc.
2. Precise filtering in RAG queries
3. Intelligent information organization

PHILOSOPHY: QUALITY over QUANTITY
- Suggest between 5-12 metadata fields (maximum 20 only if absolutely necessary)
- Each metadata field must have a clear purpose for search or filtering
- Avoid redundancies and trivial fields
- If a field doesn't add real value for finding the document, DON'T include it

EXTRACTION RULES:
- Field names: lowercase, no spaces, use underscores
- Values: simple strings or numbers, no arrays or objects
- Only include metadata that explicitly appears in the document
- Prioritize metadata that truly differentiates this document from others

COMMON DOCUMENT TYPES:
- Invoices: number, supplier, customer, amount, date, status
- Contracts: parties, signature_date, validity, value, area, status
- Reports: author, department, period, type, confidentiality
- Manuals: product, version, language, category
- Emails: sender, recipient, subject, date, priority

UNIVERSAL METADATA (if applicable):
- title: descriptive document title (extracted from content, NOT from filename)
- type: document category
- date: main date (format YYYY-MM-DD)
- author: creator or responsible party
- department: organizational area
- confidentiality: public/internal/confidential/private
- status: active/pending/archived/etc
- tags: keywords (maximum 5, comma-separated)

IMPORTANT ABOUT TITLE:
- Must be extracted from document CONTENT (header, first page, subject)
- DO NOT use the filename as title
- Must be descriptive and professional
- Format: "Document Type - Brief Description"
- Example: "Service Invoice - Microsoft Azure November 2024"

Respond ONLY with valid JSON, without markdown or explanations."""

        # Create analysis prompt - BILINGUAL VERSION
        if language == 'es':
            analysis_prompt = f"""Analiza este documento y extrae metadatos relevantes.

Nombre del archivo: {file.filename}

Proporciona un JSON con los metadatos encontrados. Estructura de ejemplo:
{{
    "titulo": "Factura de Servicios Cloud - Empresa XYZ",
    "tipo": "factura",
    "numero_factura": "INV-2024-001",
    "proveedor": "Empresa XYZ",
    "cliente": "Mi Empresa S.L.",
    "importe": "1500.00",
    "fecha": "2024-11-15",
    "estado": "pendiente"
}}

Recuerda:
- SIEMPRE incluye "titulo" extraído del CONTENIDO del documento
- CALIDAD sobre CANTIDAD: entre 5-12 campos de metadatos útiles (máximo 20)
- Solo campos que realmente ayuden a encontrar o filtrar este documento
- Evita campos obvios o redundantes
- Nombres de campos en minúsculas con guiones bajos
- TODOS los valores de metadatos en ESPAÑOL
- Formato JSON puro sin markdown"""
        else:
            analysis_prompt = f"""Analyze this document and extract relevant metadata.

Filename: {file.filename}

Provide a JSON with the metadata found. Example structure:
{{
    "title": "Cloud Services Invoice - XYZ Company",
    "type": "invoice",
    "invoice_number": "INV-2024-001",
    "supplier": "XYZ Company",
    "customer": "My Company Ltd",
    "amount": "1500.00",
    "date": "2024-11-15",
    "status": "pending"
}}

Remember:
- ALWAYS include "title" extracted from document CONTENT
- QUALITY over QUANTITY: between 5-12 useful metadata fields (maximum 20)
- Only fields that really help find or filter this document
- Avoid obvious or redundant fields
- Field names in lowercase with underscores
- ALL metadata values in ENGLISH
- Pure JSON format without markdown"""

        # Generate content with system instruction using selected model
        if use_text_extraction:
            # Use extracted text for DOCX/XLSX
            logger.info("Generating metadata from extracted text")
            response = client.models.generate_content(
                model=model,
                contents=[
                    types.Content(
                        role='user',
                        parts=[
                            types.Part.from_text(text=f"{analysis_prompt}\n\nDocument content:\n{extracted_text[:10000]}")  # Limit to 10k chars
                        ]
                    )
                ],
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.1
                )
            )
        else:
            # Use Files API for PDF and other supported formats
            logger.info("Generating metadata from uploaded file")
            response = client.models.generate_content(
                model=model,
                contents=[
                    types.Content(
                        role='user',
                        parts=[
                            types.Part.from_uri(
                                file_uri=uploaded_file.uri,
                                mime_type=uploaded_file.mime_type
                            ),
                            types.Part.from_text(text=analysis_prompt)
                        ]
                    )
                ],
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.1
                )
            )

        # Extract JSON from response
        response_text = response.text.strip()

        # Clean response - remove markdown code blocks if present
        if response_text.startswith('```'):
            # Remove ```json and ``` markers
            response_text = response_text.replace('```json', '').replace('```', '').strip()

        # Parse JSON
        suggested_metadata = json.loads(response_text)

        logger.info(f"Suggested metadata: {suggested_metadata}")

        # Clean up temporary files
        try:
            # Only delete from Files API if we uploaded there
            if uploaded_file is not None:
                client.files.delete(name=uploaded_file.name)

            # Always delete local temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except Exception as cleanup_error:
            logger.warning(f"Could not delete temporary file: {cleanup_error}")

        return jsonify({
            'success': True,
            'metadata': suggested_metadata,
            'filename': file.filename
        })

    except json.JSONDecodeError as json_error:
        logger.error(f"Error parsing JSON from Gemini: {json_error}")
        logger.error(f"Response was: {response_text}")
        return jsonify({
            'error': 'Error parsing AI response',
            'details': f'Could not parse JSON: {str(json_error)}'
        }), 500
    except Exception as e:
        logger.error(f"Error suggesting metadata: {str(e)}")
        return jsonify({'error': f'Error analyzing document: {str(e)}'}), 500

# ============================================
# UTILITY ENDPOINTS - Endpoints de utilidad
# ============================================

@app.route('/clear', methods=['POST'])
def clear_conversation():
    global conversation_history
    conversation_history = []
    logger.info("Conversation history cleared")
    return jsonify({'success': True, 'message': 'Conversation cleared'})

@app.route('/files', methods=['GET'])
def get_files():
    return jsonify({
        'success': True,
        'files': uploaded_files,
        'store_name': file_search_store.name if file_search_store else None
    })

@app.route('/current-store-documents', methods=['GET'])
def get_current_store_documents():
    """Get all documents from the current store with metadata"""
    try:
        if not file_search_store:
            return jsonify({
                'success': True,
                'documents': [],
                'store_name': None,
                'message': 'No store selected'
            })

        documents = []
        try:
            for doc in client.file_search_stores.documents.list(parent=file_search_store.name):
                # Extract custom metadata from Gemini
                custom_metadata = {}
                if hasattr(doc, 'custom_metadata') and doc.custom_metadata:
                    for metadata in doc.custom_metadata:
                        key = getattr(metadata, 'key', '')
                        if hasattr(metadata, 'string_value'):
                            custom_metadata[key] = getattr(metadata, 'string_value', '')
                        elif hasattr(metadata, 'numeric_value'):
                            custom_metadata[key] = getattr(metadata, 'numeric_value', 0)

                # Merge with local metadata edits
                for file_info in uploaded_files:
                    if file_info.get('document_id') == doc.name:
                        local_metadata = file_info.get('custom_metadata', {})
                        custom_metadata.update(local_metadata)
                        break

                documents.append({
                    'name': doc.name,
                    'display_name': getattr(doc, 'display_name', 'N/A'),
                    'displayName': getattr(doc, 'display_name', 'N/A'),
                    'state': getattr(doc, 'state', 'UNKNOWN'),
                    'size_bytes': getattr(doc, 'size_bytes', 0),
                    'sizeBytes': getattr(doc, 'size_bytes', 0),
                    'mime_type': getattr(doc, 'mime_type', 'N/A'),
                    'mimeType': getattr(doc, 'mime_type', 'N/A'),
                    'create_time': str(getattr(doc, 'create_time', 'N/A')),
                    'createTime': str(getattr(doc, 'create_time', 'N/A')),
                    'custom_metadata': custom_metadata,
                    'customMetadata': custom_metadata
                })
        except Exception as doc_error:
            logger.warning(f"Error listing documents for current store: {str(doc_error)}")

        return jsonify({
            'success': True,
            'documents': documents,
            'store_name': file_search_store.name,
            'store_display_name': getattr(file_search_store, 'display_name', 'N/A')
        })

    except Exception as e:
        logger.error(f"Error getting current store documents: {str(e)}")
        return jsonify({'error': f'Error getting documents: {str(e)}'}), 500

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        'file_uploaded': file_search_store is not None,
        'conversation_length': len(conversation_history),
        'store_name': file_search_store.name if file_search_store else None,
        'uploaded_files': uploaded_files
    })

# ============================================
# APPLICATION ENTRY POINT - Punto de entrada de la aplicación
# Puerto configurado en 5001
# ============================================

if __name__ == '__main__':
    # Load persisted state on startup - Cargar estado persistido al iniciar
    load_state()
    app.run(debug=True, host='localhost', port=5001)
