import requests
from config.settings import CONFIG


def call_llm(prompt: str, mode: str = "smart", system_instruction: str = ""):
    """
    mode='smart' -> Menggunakan model pintar untuk riset/arsitektur
    mode='fast'  -> Menggunakan model eksekusi/lokal untuk koding
    """
    if mode == "smart":
        provider = CONFIG["SMART_PROVIDER"]
        model = CONFIG["SMART_MODEL"]
    else:
        provider = CONFIG["FAST_PROVIDER"]
        model = CONFIG["FAST_MODEL"]

    # Contoh Implementasi pemanggilan Ollama (Lokal - Gratis)
    if provider == "ollama":
        try:
            messages = []
            if system_instruction:
                messages.append(
                    {"role": "system", "content": system_instruction})
            messages.append({"role": "user", "content": prompt})

            response = requests.post(
                f"{CONFIG['OLLAMA_BASE_URL']}/v1/chat/completions",
                json={
                    "model": model,
                    "messages": messages,
                    "stream": False
                },
                timeout=120
            )
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return f"[Error Ollama]: {response.text}"
        except Exception as e:
            return f"[Koneksi Ollama Gagal]: {str(e)} (Pastikan Ollama aktif di PC rumah)"

    # Placeholder untuk Cloud Provider (Google/OpenAI)
    elif provider == "google":
        # Nanti bisa dihubungkan ke official google-generativeai SDK
        return f"[Simulasi Google Gemini API ({model})]: Menerima prompt -> {prompt}"

    return "[Error]: Provider LLM tidak dikenali."
