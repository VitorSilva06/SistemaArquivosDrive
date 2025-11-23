# Backend FastAPI - Cadastro de Clientes

## 📋 Pré-requisitos

- Python 3.11+
- Conta Google com acesso ao Drive
- Arquivo `client_secret_*.json` do Google Cloud Console
- Pasta raiz no Drive para armazenar os documentos

## 🚀 Configuração

### 1. Ambiente Virtual

```bash
cd backend
python -m venv env
# Windows
env\Scripts\activate
# Linux/Mac
source env/bin/activate
```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar Google OAuth

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um projeto ou selecione um existente
3. Habilite a **Google Drive API**
4. Crie credenciais OAuth 2.0 (tipo "Aplicativo de desktop")
5. Baixe o arquivo JSON (`client_secret_*.json`)
6. Coloque o arquivo na pasta `backend/`

### 4. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na pasta `backend/`:

```env
# ID da pasta raiz no Google Drive
GOOGLE_DRIVE_ROOT_FOLDER_ID=seu_id_da_pasta_aqui

# (Opcional) Caminho do arquivo client_secret
GOOGLE_CLIENT_SECRET_FILE=client_secret_225116848186-m0i8a6vcoh29nkj0kkvimce1jchevqq4.apps.googleusercontent.com.json

# (Opcional) Configurações de validação
MIN_IMAGE_WIDTH=600
MIN_IMAGE_HEIGHT=400
MIN_FILESIZE_KB=80
MAX_FILESIZE_MB=50

# (Opcional) Logging
LOG_LEVEL=INFO

# (Opcional) CORS
ALLOWED_ORIGINS=*
```

### 5. Primeira Autenticação

Na primeira execução, o sistema abrirá o navegador para autenticação OAuth. 
Após autorizar, o token será salvo em `token.json` para uso futuro.

### 6. Executar o Servidor

```bash
uvicorn main:app --reload
```

O servidor estará disponível em `http://localhost:8000`

## 📁 Estrutura do Projeto

```
backend/
├── __init__.py           # Pacote Python
├── main.py              # Endpoint principal da API
├── config.py            # Configurações centralizadas
├── models.py            # Modelos de dados (Pydantic)
├── utils.py             # Funções utilitárias
├── validators.py        # Validações de entrada
├── drive_service.py     # Serviço do Google Drive
├── image_processor.py   # Processamento de imagens
├── report_generator.py # Geração de relatórios
├── requirements.txt     # Dependências
└── README.md           # Este arquivo
```

## 🔒 Segurança

- Validação de tamanho de arquivos
- Sanitização de nomes de arquivos
- Validação de tipos de arquivo
- Rate limiting (recomendado adicionar em produção)
- CORS configurável

## 📝 Endpoints

### `GET /`
Informações da API

### `GET /health`
Health check

### `POST /api/submit`
Envia documentos do cliente

**Body (multipart/form-data):**
- `nome`: Nome completo
- `telefone`: Telefone
- `servico`: Tipo de serviço
- `field_status`: JSON com status dos campos
- `file_field_map`: JSON com mapeamento arquivo -> campo
- `documentos`: Arquivos (múltiplos)

## 🛠️ Manutenção

### Atualizar Token OAuth

Se o token expirar, delete `token.json` e reinicie o servidor para reautenticar.

### Logs

Logs são exibidos no console. Configure `LOG_LEVEL` no `.env` para controlar verbosidade.

## 🐛 Troubleshooting

### Erro: "Arquivo de credenciais não encontrado"
- Verifique se o arquivo `client_secret_*.json` está na pasta `backend/`
- Ou defina `GOOGLE_CLIENT_SECRET_FILE` no `.env`

### Erro: "GOOGLE_DRIVE_ROOT_FOLDER_ID não configurado"
- Adicione a variável no arquivo `.env`

### Erro de autenticação
- Delete `token.json` e reinicie para reautenticar
- Verifique se a Google Drive API está habilitada no projeto
