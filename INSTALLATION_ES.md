# Guía de Instalación

Instrucciones completas de configuración para Gemini File Search Manager.

## Tabla de Contenidos

- [Requisitos Previos](#requisitos-previos)
- [Pasos de Instalación](#pasos-de-instalación)
- [Configuración](#configuración)
- [Verificación](#verificación)
- [Solución de Problemas](#solución-de-problemas)
- [Configuración Avanzada](#configuración-avanzada)

---

## Requisitos Previos

### Requisitos del Sistema

- **Sistema Operativo**: Windows 10+, macOS 10.14+, o Linux (Ubuntu 20.04+)
- **Python**: 3.8 o superior
- **RAM**: Mínimo 2 GB disponibles
- **Espacio en Disco**: 500 MB para la aplicación + espacio para tus documentos
- **Conexión a Internet**: Requerida para acceso a la API de Gemini

### Cuentas Requeridas

- **Cuenta de Google AI Studio**: Cuenta gratuita para acceso a la API de Gemini
  - Regístrate en: https://ai.google.dev/
  - Genera tu API key en: https://aistudio.google.com/app/apikey

### Verificar Versión de Python

```bash
python --version
# Debería mostrar: Python 3.8.0 o superior

# Si 'python' no funciona, intenta:
python3 --version
```

Si Python no está instalado:
- **Windows**: Descarga desde https://www.python.org/downloads/
- **macOS**: `brew install python3` (requiere Homebrew)
- **Linux**: `sudo apt update && sudo apt install python3 python3-pip`

---

## Pasos de Instalación

### Paso 1: Clonar el Repositorio

```bash
# Usando Git
git clone https://github.com/webcomunicasolutions/gemini-file-search-manager.git
cd gemini-file-search-manager

# O descargar ZIP
# Descargar desde: https://github.com/webcomunicasolutions/gemini-file-search-manager/archive/refs/heads/main.zip
# Extraer y entrar en la carpeta
```

### Paso 2: Navegar al Directorio de la Aplicación Web

```bash
cd web_app
```

### Paso 3: Crear Entorno Virtual

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

Deberías ver `(venv)` en tu prompt de terminal.

### Paso 4: Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Salida esperada:**
```
Successfully installed flask-3.0.0 flask-cors-4.0.0 google-genai-1.49.0 ...
```

### Paso 5: Configurar API Key

**Opción A: Usando archivo .env (Recomendado)**

Crea el archivo `.env` en el directorio `web_app/`:

```bash
# Windows (Command Prompt)
copy .env.example .env

# Windows (PowerShell)
Copy-Item .env.example .env

# macOS/Linux
cp .env.example .env
```

Luego edita `.env` y añade tu API key:

```env
GEMINI_API_KEY=tu_api_key_real_aqui
```

**Opción B: Editar app.py directamente (Solo para pruebas)**

Abre `app.py` y edita la línea 35:

```python
# Antes:
api_key = os.getenv('GEMINI_API_KEY')

# Después:
api_key = 'tu_api_key_real_aqui'
```

**Importante**: Nunca hagas commit de API keys en control de versiones. Añade `.env` a `.gitignore`.

### Paso 6: Ejecutar la Aplicación

```bash
python app.py
```

**Salida esperada:**
```
INFO:werkzeug: * Running on http://localhost:5001
INFO:werkzeug:Press CTRL+C to quit
INFO:werkzeug: * Restarting with stat
INFO:app:Restored file search store: fileSearchStores/rag-app-store-xxx with 0 files
```

### Paso 7: Abrir en el Navegador

Navega a: `http://localhost:5001`

Deberías ver la interfaz de Gemini File Search Manager.

---

## Configuración

### Variables de Entorno

Opciones completas de configuración en `.env`:

```env
# Requerido
GEMINI_API_KEY=tu_api_key_de_gemini_aqui

# Opcional - Configuración de la Aplicación
FLASK_ENV=development              # development o production
FLASK_DEBUG=True                   # True o False
FLASK_PORT=5001                    # Número de puerto

# Opcional - Carga de Archivos
MAX_CONTENT_LENGTH=104857600       # Tamaño máx de archivo en bytes (100MB por defecto)
UPLOAD_FOLDER=uploads              # Carpeta de uploads temporales

# Opcional - Conversación
MAX_HISTORY=7                      # Pares de historial de conversación
```

### Configuración de la Aplicación

Edita las constantes en `app.py` (líneas 23-26):

```python
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'json', 'md', 'py', 'js', 'html', 'css', 'xml', 'csv'}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
MAX_HISTORY = 7
```

Para añadir más tipos de archivo:
```python
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'json', 'md', 'py', 'js', 'html', 'css', 'xml', 'csv', 'xlsx', 'pptx', 'zip'}
```

### Configuración de Chunking

Configuración por defecto de chunking (ajustable por upload):

```python
# En app.py, líneas 166-172
chunking_config = {
    'white_space_config': {
        'max_tokens_per_chunk': 200,    # Incrementar para chunks más largos
        'max_overlap_tokens': 20         # Incrementar para más contexto
    }
}
```

Valores recomendados:
- **Documentos cortos (< 10 páginas)**: 200 tokens/chunk, 20 overlap
- **Documentos medianos (10-50 páginas)**: 500 tokens/chunk, 50 overlap
- **Documentos largos (> 50 páginas)**: 1000 tokens/chunk, 100 overlap

### Configuración de Puerto

Cambiar puerto si 5001 está en uso (edita `app.py` línea 1012):

```python
# Antes:
app.run(debug=True, host='localhost', port=5001)

# Después:
app.run(debug=True, host='localhost', port=8080)
```

---

## Verificación

### Prueba 1: Verificar Estado de la Aplicación

Abre en navegador: `http://localhost:5001/status`

Respuesta esperada:
```json
{
  "file_uploaded": false,
  "conversation_length": 0,
  "store_name": null,
  "uploaded_files": []
}
```

### Prueba 2: Verificar Información de la API

Abre en navegador: `http://localhost:5001/api-info`

Respuesta esperada:
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

### Prueba 3: Subir Archivo de Prueba

1. Abre `http://localhost:5001`
2. Haz clic en "Elegir Archivo"
3. Selecciona cualquier archivo de texto
4. Haz clic en "Subir Documento"
5. Espera el mensaje de éxito

### Prueba 4: Probar Metadatos con IA

1. Haz clic en "Elegir Archivo"
2. Selecciona un archivo PDF o DOCX
3. Haz clic en "Sugerir con IA"
4. Verifica que aparezcan los metadatos
5. Haz clic en "Subir Documento"

### Prueba 5: Prueba de Chat

1. Después de subir, escribe: "¿Qué dice el documento?"
2. Presiona "Enviar" o Enter
3. Verifica que aparezca la respuesta con citaciones

---

## Solución de Problemas

### Problema: Error de API Key

**Error**: `ValueError: GEMINI_API_KEY not found`

**Soluciones**:
1. Verifica que el archivo `.env` existe en el directorio `web_app/`
2. Verifica que `.env` contiene: `GEMINI_API_KEY=tu_key`
3. Sin comillas alrededor del valor de la key
4. Sin espacios antes o después de `=`
5. Reinicia la aplicación después de crear `.env`

**Verificar que la API key se carga**:
```python
# Añade a app.py después de la línea 35
print(f"API Key cargada: {api_key[:10]}...")  # Muestra los primeros 10 caracteres
```

### Problema: Puerto en Uso

**Error**: `OSError: [Errno 48] Address already in use`

**Soluciones**:
1. Cambiar puerto en `app.py` (ver Configuración de Puerto arriba)
2. O terminar el proceso que usa el puerto 5001:

**Windows:**
```cmd
netstat -ano | findstr :5001
taskkill /PID [número_de_proceso] /F
```

**macOS/Linux:**
```bash
lsof -ti:5001 | xargs kill -9
```

### Problema: Error de Importación

**Error**: `ModuleNotFoundError: No module named 'flask'`

**Soluciones**:
1. Verifica que el entorno virtual está activado (deberías ver `(venv)`)
2. Reinstala las dependencias:
```bash
pip install -r requirements.txt
```
3. Verifica la instalación:
```bash
pip list
```

### Problema: Error de Archivo No Encontrado

**Error**: `FileNotFoundError: [Errno 2] No such file or directory: 'uploads'`

**Solución**:
```bash
# Desde el directorio web_app/
mkdir uploads
```

### Problema: Error al Cargar Archivo Grande

**Error**: `413 Request Entity Too Large`

**Soluciones**:
1. Verifica el tamaño del archivo (máx 100MB por defecto)
2. Incrementa MAX_FILE_SIZE en `app.py`
3. O divide documentos grandes en partes más pequeñas

### Problema: Sin Respuesta del Chat

**Posibles causas**:
1. No hay documentos cargados en el store
2. API key inválida o expirada
3. Problemas de conexión a internet
4. Límite de rate de la API alcanzado

**Soluciones**:
1. Verifica que los documentos están en estado ACTIVE
2. Prueba la API key en https://aistudio.google.com/app/apikey
3. Verifica tu conexión a internet
4. Espera unos minutos si alcanzaste el límite de rate

### Problema: Metadatos con IA No Funcionan

**Error**: Error al generar metadatos

**Soluciones**:
1. Verifica que el archivo es compatible (PDF, DOCX, TXT, etc.)
2. Archivo no debe estar corrupto
3. Tamaño de archivo debe ser < 100MB
4. Verifica límites de la API de Gemini

---

## Configuración Avanzada

### Ejecutar en Modo Producción

1. Deshabilitar debug en `app.py`:
```python
app.run(debug=False, host='0.0.0.0', port=5001)
```

2. Usar servidor WSGI como Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

### Usar HTTPS

1. Generar certificados SSL:
```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

2. Modificar `app.py`:
```python
app.run(debug=False, host='0.0.0.0', port=5001, ssl_context=('cert.pem', 'key.pem'))
```

### Configurar Almacenamiento Persistente

Por defecto, `store_state.json` almacena el estado. Para usar base de datos:

1. Instalar SQLite support:
```bash
pip install sqlalchemy
```

2. Modificar `app.py` para usar SQLAlchemy (implementación personalizada requerida)

### Configuración de Múltiples Stores

La aplicación soporta múltiples File Search Stores. Para gestionar múltiples stores:

1. Usar el selector de stores en la interfaz
2. O usar la API directamente para crear/listar stores
3. Los stores se persisten automáticamente en `store_state.json`

### Configuración de Logging

Añadir logging detallado en `app.py`:

```python
import logging

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### Variables de Entorno de Producción

Para producción, considera usar:

```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=tu_clave_secreta_aleatoria_aqui
SESSION_TYPE=filesystem
MAX_CONTENT_LENGTH=104857600
PERMANENT_SESSION_LIFETIME=3600
```

---

## Desinstalación

Para eliminar completamente la aplicación:

```bash
# 1. Desactivar entorno virtual
deactivate

# 2. Eliminar directorio del proyecto
cd ..
rm -rf gemini-file-search-manager  # Linux/macOS
rmdir /s gemini-file-search-manager  # Windows

# 3. Opcional: Eliminar stores de Gemini
# Usar la interfaz web o la API para eliminar los File Search Stores
```

---

## Soporte

Si encuentras problemas:

1. Revisa la sección [Solución de Problemas](#solución-de-problemas)
2. Verifica los logs de la aplicación
3. Consulta la [documentación oficial de Gemini](https://ai.google.dev/gemini-api/docs)
4. Abre un issue en GitHub: https://github.com/webcomunicasolutions/gemini-file-search-manager/issues

---

## Próximos Pasos

Después de la instalación exitosa:

1. Lee el [README](README_ES.md) para conocer todas las características
2. Explora la interfaz web y sus 3 pestañas principales
3. Prueba el generador de peticiones HTTP
4. Revisa [CLAUDE.md](CLAUDE.md) para detalles de la API de File Search

---

**Última Actualización**: 19 de Noviembre de 2025
**Versión**: 1.0.0

---

## 🌍 Idiomas Disponibles

- [English](INSTALLATION.md)
- [Español](INSTALLATION_ES.md)
