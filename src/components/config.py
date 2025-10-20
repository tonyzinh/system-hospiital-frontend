# Configurações da API
API_BASE_URL = "http://localhost:8000/api/v1"

# Configurações da UI
PAGE_TITLE = "Sistema Hospitalar"
PAGE_ICON = "🏥"

# Configurações de paginação
ITEMS_PER_PAGE = 10

# Status de resposta HTTP
HTTP_SUCCESS_CODES = [200, 201, 204]

# Configurações do Chat IA
AI_TIMEOUT = 120  # segundos
AI_MAX_RETRIES = 3
AI_MODELS = {
    "default": "llama3.1",
    "advanced": "llama3.1"
}