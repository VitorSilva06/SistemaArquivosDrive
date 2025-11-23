"""Configurações centralizadas da aplicação."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Caminho base do projeto
BASE_DIR = Path(__file__).parent

load_dotenv()

# Google Drive OAuth / Service Account
CLIENT_SECRET_FILE = os.getenv(
    "GOOGLE_CLIENT_SECRET_FILE",
    str(BASE_DIR / "client_secret_225116848186-m0i8a6vcoh29nkj0kkvimce1jchevqq4.apps.googleusercontent.com.json")
)
TOKEN_FILE = os.getenv("GOOGLE_TOKEN_FILE", "token.json")
GOOGLE_DRIVE_ROOT_FOLDER_ID = os.getenv("GOOGLE_DRIVE_ROOT_FOLDER_ID", "")

# Detecta uso de Service Account (produção)
USE_SERVICE_ACCOUNT = bool(os.getenv("GOOGLE_CLIENT_SECRET_JSON"))

# Scopes do Google Drive
SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive.metadata.readonly"
]

# Validação de imagens
MIN_WIDTH = int(os.getenv("MIN_IMAGE_WIDTH", "600"))
MIN_HEIGHT = int(os.getenv("MIN_IMAGE_HEIGHT", "400"))
MIN_FILESIZE_KB = int(os.getenv("MIN_FILESIZE_KB", "80"))
MAX_FILESIZE_MB = int(os.getenv("MAX_FILESIZE_MB", "50"))

# Limites gerais
MAX_FOLDER_NAME_LENGTH = 100
MAX_FILENAME_LENGTH = 200

# Segurança
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
MAX_UPLOAD_SIZE = MAX_FILESIZE_MB * 1024 * 1024  # em bytes

# Validações
MIN_NAME_LENGTH = 3
MIN_PHONE_LENGTH = 10

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Verificações de segurança
if not USE_SERVICE_ACCOUNT and not Path(CLIENT_SECRET_FILE).exists():
    raise FileNotFoundError(
        f"Arquivo de credenciais não encontrado: {CLIENT_SECRET_FILE}. "
        f"Verifique se o arquivo existe em {BASE_DIR}"
    )

if not GOOGLE_DRIVE_ROOT_FOLDER_ID:
    raise ValueError("GOOGLE_DRIVE_ROOT_FOLDER_ID não configurado no .env")

