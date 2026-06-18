# Company settings
COMPANY_NAME = "NVIDIA"
TICKER = "NVDA"
TOPIC = "NVIDIA artificial intelligence data center GPU competitors"

# Data collection settings
NOD = 40
DELAY_TIME = 2

# API URLs
NEWS_ORG_URL = "https://newsapi.org/v2/everything"
ALPHA_URL = "https://www.alphavantage.co/query"
RSS_URL = "https://nvidianews.nvidia.com/releases.xml"

# Embedding model
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# LLM model
LLM_MODEL_NAME = "Qwen/Qwen3-8B"

# Chunking settings
CHUNK_SIZE = 250
CHUNK_OVERLAP = 50

# Retrieval settings
TOP_K = 7

# Strategic intelligence categories
STRATEGIC_QUERIES = {
    "opportunities": [
        "NVIDIA opportunities in artificial intelligence",
        "NVIDIA growth in data centers",
        "NVIDIA product opportunities and new markets",
        "NVIDIA partnerships and AI infrastructure"
    ],

    "risks": [
        "NVIDIA risks and threats",
        "NVIDIA regulatory risk",
        "NVIDIA supply chain issues",
        "NVIDIA competition risk"
    ],

    "competitor_activity": [
        "AMD competition with NVIDIA",
        "Intel competition with NVIDIA",
        "Google Microsoft Amazon AI chips competition",
        "competitors developing AI accelerators and GPUs"
    ],

    "emerging_trends": [
        "emerging AI technology trends",
        "AI data center market trends",
        "GPU cloud computing trends",
        "generative AI infrastructure trends"
    ],

    "company_announcements": [
        "NVIDIA official announcements",
        "NVIDIA product launch",
        "NVIDIA financial announcement",
        "NVIDIA partnership announcement"
    ]
}

EVIDENCE_TOP_K = 7

# RAG settings
RAG_TOP_K = 5

STRATEGIC_EVIDENCE_PER_CATEGORY_IN_PROMPT = 4
MAX_CHARS_PER_EVIDENCE = 900

DEFAULT_CEO_QUESTION = "If you were the CEO of NVIDIA today, what would you do next and why?"

# LLM settings
LLM_MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"
MAX_NEW_TOKENS = 900
TEMPERATURE = 0.2