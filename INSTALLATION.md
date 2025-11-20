# Installation Guide

Complete setup instructions for Gemini File Search Manager.

## 🌍 Available Languages

- [English](INSTALLATION.md)
- [Español](INSTALLATION_ES.md)

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation Steps](#installation-steps)
- [Configuration](#configuration)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)
- [Advanced Setup](#advanced-setup)

---

## Prerequisites

### System Requirements

- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 20.04+)
- **Python**: 3.8 or higher
- **RAM**: Minimum 2 GB available
- **Disk Space**: 500 MB for application + space for your documents
- **Internet Connection**: Required for Gemini API access

### Required Accounts

- **Google AI Studio Account**: Free account for Gemini API access
  - Sign up at: https://ai.google.dev/
  - Generate API key at: https://makersuite.google.com/app/apikey

### Check Python Version

```bash
python --version
# Should output: Python 3.8.0 or higher

# If 'python' doesn't work, try:
python3 --version
```

If Python is not installed:
- **Windows**: Download from https://www.python.org/downloads/
- **macOS**: `brew install python3` (requires Homebrew)
- **Linux**: `sudo apt update && sudo apt install python3 python3-pip`

---

## Installation Steps

### Step 1: Clone the Repository

```bash
# Using Git
git clone https://github.com/yourusername/gemini-file-search-manager.git
cd gemini-file-search-manager

# Or download ZIP
# Download from: https://github.com/yourusername/gemini-file-search-manager/archive/refs/heads/main.zip
# Extract and cd into the folder
```

### Step 2: Navigate to Web App Directory

```bash
cd web_app
```

### Step 3: Create Virtual Environment

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 4: Install Dependencies

```bash
pip install flask flask-cors google-genai python-dotenv werkzeug
```

**Expected output:**
```
Successfully installed flask-3.0.0 flask-cors-4.0.0 google-genai-0.3.0 ...
```

**Alternative - Using requirements.txt (if provided):**
```bash
pip install -r requirements.txt
```

### Step 5: Configure API Key

**Option A: Using .env file (Recommended)**

Create file `.env` in `web_app/` directory:

```bash
# Windows (Command Prompt)
echo GEMINI_API_KEY=your_actual_api_key_here > .env

# Windows (PowerShell)
"GEMINI_API_KEY=your_actual_api_key_here" | Out-File -FilePath .env

# macOS/Linux
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env
```

**Option B: Edit app.py directly (Testing only)**

Open `app.py` and edit line 35:

```python
# Before:
api_key = os.getenv('GEMINI_API_KEY')

# After:
api_key = 'your_actual_api_key_here'
```

**Important**: Never commit API keys to version control. Add `.env` to `.gitignore`.

### Step 6: Run the Application

```bash
python app.py
```

**Expected output:**
```
INFO:werkzeug: * Running on http://localhost:5001
INFO:werkzeug:Press CTRL+C to quit
INFO:werkzeug: * Restarting with stat
INFO:app:Restored file search store: fileSearchStores/rag-app-store-xxx with 0 files
```

### Step 7: Open Browser

Navigate to: `http://localhost:5001`

You should see the Gemini File Search Manager interface.

---

## Configuration

### Environment Variables

Complete `.env` configuration options:

```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional - Application Settings
FLASK_ENV=development              # development or production
FLASK_DEBUG=True                   # True or False
FLASK_PORT=5001                    # Port number

# Optional - File Upload
MAX_CONTENT_LENGTH=104857600       # Max file size in bytes (100MB default)
UPLOAD_FOLDER=uploads              # Temporary upload folder

# Optional - Conversation
MAX_HISTORY=7                      # Conversation history pairs
```

### Application Configuration

Edit constants in `app.py` (lines 23-26):

```python
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'json', 'md', 'py', 'js', 'html', 'css', 'xml', 'csv'}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
MAX_HISTORY = 7
```

To add more file types:
```python
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'json', 'md', 'py', 'js', 'html', 'css', 'xml', 'csv', 'xlsx', 'pptx', 'zip'}
```

### Chunking Configuration

Default chunking settings (adjustable per upload):

```python
# In app.py, lines 166-172
chunking_config = {
    'white_space_config': {
        'max_tokens_per_chunk': 200,    # Increase for longer chunks
        'max_overlap_tokens': 20         # Increase for more context
    }
}
```

Recommended values:
- **Short documents (< 10 pages)**: 200 tokens/chunk, 20 overlap
- **Medium documents (10-50 pages)**: 500 tokens/chunk, 50 overlap
- **Long documents (> 50 pages)**: 1000 tokens/chunk, 100 overlap

### Port Configuration

Change port if 5001 is in use (edit `app.py` line 1012):

```python
# Before:
app.run(debug=True, host='localhost', port=5001)

# After:
app.run(debug=True, host='localhost', port=8080)
```

---

## Verification

### Test 1: Check Application Status

Open browser: `http://localhost:5001/status`

Expected response:
```json
{
  "file_uploaded": false,
  "conversation_length": 0,
  "store_name": null,
  "uploaded_files": []
}
```

### Test 2: Check API Info

Open browser: `http://localhost:5001/api-info`

Expected response:
```json
{
  "success": true,
  "api_key": "AIza...",
  "store_exists": false,
  "store_name": null,
  "file_count": 0,
  "model": "gemini-2.5-flash"
}
```

### Test 3: Upload Test File

1. Open `http://localhost:5001`
2. Click "Elegir Archivo"
3. Select any text file
4. Click "Subir Documento"
5. Wait for success message

### Test 4: Test AI Metadata

1. Click "Elegir Archivo"
2. Select a PDF or DOCX file
3. Click "Sugerir con IA"
4. Verify metadata appears
5. Click "Subir Documento"

### Test 5: Chat Test

1. After uploading, type: "¿Qué dice el documento?"
2. Press "Enviar" or Enter
3. Verify response appears with citations

---

## Troubleshooting

### Issue: API Key Error

**Error**: `ValueError: GEMINI_API_KEY not found`

**Solutions**:
1. Check `.env` file exists in `web_app/` directory
2. Verify `.env` contains: `GEMINI_API_KEY=your_key`
3. No quotes around key value
4. No spaces before or after `=`
5. Restart application after creating `.env`

**Verify API key is loaded**:
```python
# Add to app.py after line 35
print(f"API Key loaded: {api_key[:10]}...")  # Shows first 10 chars
```

---

### Issue: Port Already in Use

**Error**: `OSError: [Errno 48] Address already in use`

**Solutions**:

**Windows**:
```cmd
# Find process using port 5001
netstat -ano | findstr :5001

# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

**macOS/Linux**:
```bash
# Find and kill process
lsof -ti:5001 | xargs kill -9
```

**Alternative**: Change port in `app.py` line 1012

---

### Issue: Module Not Found

**Error**: `ModuleNotFoundError: No module named 'flask'`

**Solutions**:
1. Verify virtual environment is activated (see `(venv)` in prompt)
2. Reinstall dependencies:
   ```bash
   pip install flask flask-cors google-genai python-dotenv werkzeug
   ```
3. Check Python path:
   ```bash
   which python  # macOS/Linux
   where python  # Windows
   ```

---

### Issue: File Upload Timeout

**Error**: `File processing timeout after 120 seconds`

**Solutions**:
1. **Increase timeout** (edit `app.py` line 182):
   ```python
   max_wait = 180  # 3 minutes instead of 2
   ```

2. **Check file size**:
   ```bash
   # File should be < 100 MB
   ls -lh your_file.pdf  # macOS/Linux
   dir your_file.pdf     # Windows
   ```

3. **Reduce chunk size** (smaller chunks = faster processing):
   ```python
   'max_tokens_per_chunk': 100,  # Default is 200
   ```

4. **Check network**:
   - Test API access: `curl https://generativelanguage.googleapis.com/v1beta/models`
   - Verify firewall allows HTTPS

---

### Issue: AI Metadata Suggestion Fails

**Error**: `Error analyzing document` or invalid JSON

**Solutions**:
1. **Verify file is readable**:
   - Not corrupted
   - Not password-protected
   - Supported format (PDF, DOCX, TXT, MD, etc.)

2. **Check model access**:
   ```python
   # Test in Python console
   from google import genai
   client = genai.Client(api_key='your_key')
   models = client.models.list()
   print([m.name for m in models])
   # Should include 'gemini-2.0-flash-exp'
   ```

3. **Check logs**:
   ```python
   # Add to app.py line 880
   logger.info(f"Raw AI response: {response_text}")
   ```

4. **Increase temperature** (if getting inconsistent results):
   ```python
   # Edit app.py line 875
   temperature=0.2  # Default is 0.1
   ```

---

### Issue: Store Not Persisting

**Error**: Store resets after application restart

**Solutions**:
1. **Check `store_state.json` exists**:
   ```bash
   ls -la store_state.json    # macOS/Linux
   dir store_state.json       # Windows
   ```

2. **Check file permissions**:
   ```bash
   # Ensure app can write to directory
   chmod 644 store_state.json  # macOS/Linux
   ```

3. **Verify save_state() is called**:
   ```python
   # Add to app.py after line 213
   logger.info("State saved successfully")
   ```

4. **Check JSON validity**:
   ```bash
   # Validate JSON
   python -m json.tool store_state.json
   ```

---

### Issue: CORS Errors

**Error**: `Access-Control-Allow-Origin header`

**Solutions**:
1. Verify `flask-cors` is installed:
   ```bash
   pip list | grep flask-cors
   ```

2. Check CORS is enabled in `app.py` (line 16):
   ```python
   CORS(app)
   ```

3. For specific origins only:
   ```python
   CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
   ```

---

### Issue: Citations Not Appearing

**Problem**: Chat responses don't show document citations

**Solutions**:
1. **Verify store has documents**:
   - Open `http://localhost:5001/files`
   - Should show uploaded files

2. **Check grounding metadata** (add to `app.py` line 393):
   ```python
   logger.info(f"Grounding metadata: {grounding}")
   ```

3. **Ensure File Search is configured**:
   ```python
   # Verify app.py lines 295-298
   file_search_config = types.FileSearch(
       file_search_store_names=[file_search_store.name]
   )
   ```

---

## Advanced Setup

### Docker Installation (Optional)

Create `Dockerfile` in `web_app/`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t gemini-file-search-manager .
docker run -p 5001:5001 -e GEMINI_API_KEY=your_key gemini-file-search-manager
```

### Production Deployment

**Using Gunicorn** (Linux/macOS):

```bash
# Install Gunicorn
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

**Using Waitress** (Windows):

```bash
# Install Waitress
pip install waitress

# Run
waitress-serve --host=0.0.0.0 --port=5001 app:app
```

### Nginx Reverse Proxy

Create `/etc/nginx/sites-available/gemini-file-search-manager`:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/gemini-file-search-manager /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Systemd Service (Linux)

Create `/etc/systemd/system/gemini-file-search-manager.service`:

```ini
[Unit]
Description=Gemini File Search Manager Application
After=network.target

[Service]
User=your_user
WorkingDirectory=/path/to/gemini-file-search-manager/web_app
Environment="GEMINI_API_KEY=your_key"
ExecStart=/path/to/venv/bin/gunicorn -w 4 -b 127.0.0.1:5001 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable gemini-file-search-manager
sudo systemctl start gemini-file-search-manager
sudo systemctl status gemini-file-search-manager
```

### Environment-Specific Configuration

Create multiple environment files:

**`.env.development`**:
```env
GEMINI_API_KEY=dev_key
FLASK_ENV=development
FLASK_DEBUG=True
MAX_HISTORY=3
```

**`.env.production`**:
```env
GEMINI_API_KEY=prod_key
FLASK_ENV=production
FLASK_DEBUG=False
MAX_HISTORY=10
```

Load specific environment:
```bash
# Development
cp .env.development .env
python app.py

# Production
cp .env.production .env
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

---

## Next Steps

After successful installation:

1. **Read the documentation**:
   - [README.md](README.md) - Project overview
   - [FEATURES.md](FEATURES.md) - Feature details
   - [API_REFERENCE.md](API_REFERENCE.md) - API documentation

2. **Explore the application**:
   - Upload different document types
   - Test AI metadata extraction
   - Try metadata filtering in chat
   - Manage multiple stores

3. **Join the community**:
   - Star the repository
   - Report issues on GitHub
   - Contribute improvements
   - Share your use cases

---

## Support

If you encounter issues not covered here:

1. Check [GitHub Issues](https://github.com/yourusername/gemini-file-search-manager/issues)
2. Review [Troubleshooting](#troubleshooting) section
3. Create new issue with:
   - Error message
   - Steps to reproduce
   - Environment details (OS, Python version)
   - Relevant logs

---

**Installation Complete! 🎉**

You're ready to start using Gemini File Search Manager. Open `http://localhost:5001` and begin uploading documents.
