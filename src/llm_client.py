"""Cliente LLM com fallback: Groq -> Ollama Cloud -> OpenRouter (Groq primeiro por latência)."""
import os


def get_llm():
    """Tenta Groq, depois Ollama Cloud, depois OpenRouter. Erro claro se sem chave."""
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        try:
            from langchain_groq import ChatGroq

            return ChatGroq(
                model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
                api_key=groq_key,
            )
        except Exception:
            pass

    ollama_key = os.getenv("OLLAMA_CLOUD_API_KEY")
    if ollama_key:
        try:
            from langchain_openai import ChatOpenAI

            return ChatOpenAI(
                model=os.getenv("OLLAMA_CLOUD_MODEL", "qwen3:32b"),
                api_key=ollama_key,
                base_url="https://ollama.com/v1",
            )
        except Exception:
            pass

    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    if openrouter_key:
        try:
            from langchain_openai import ChatOpenAI

            return ChatOpenAI(
                model=os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
                api_key=openrouter_key,
                base_url="https://openrouter.ai/api/v1",
            )
        except Exception:
            pass

    raise RuntimeError(
        "Nenhuma chave encontrada. Defina GROQ_API_KEY, "
        "OLLAMA_CLOUD_API_KEY ou OPENROUTER_API_KEY"
    )
