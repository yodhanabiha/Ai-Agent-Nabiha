import os

# Konfigurasi Provider & Model
CONFIG = {
    # Model Pintar untuk Perencanaan / Knowledge / Architect
    "SMART_MODEL": os.getenv("SMART_MODEL", "gemini-1.5-pro"),
    # "google" atau "openai"
    "SMART_PROVIDER": os.getenv("SMART_PROVIDER", "google"),

    # Model Eksekusi untuk Developer / QA
    "FAST_MODEL": os.getenv("FAST_MODEL", "qwen2.5-coder:7b"),
    # "ollama" atau "google"
    "FAST_PROVIDER": os.getenv("FAST_PROVIDER", "ollama"),

    # Endpoint Ollama lokal
    "OLLAMA_BASE_URL": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),

    # API Keys (Ambil dari Environment Variable demi keamanan)
    "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY", ""),
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", "")
}
