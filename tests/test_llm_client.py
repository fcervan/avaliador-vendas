"""Testes do fallback Groq -> Ollama Cloud -> OpenRouter (tudo mockado)."""

from unittest.mock import patch

import pytest

from src.llm_client import DEFAULTS, effective_models, get_llm

KEYS = ["GROQ_API_KEY", "OLLAMA_CLOUD_API_KEY", "OPENROUTER_API_KEY"]
MODELS = ["GROQ_MODEL", "OLLAMA_CLOUD_MODEL", "OPENROUTER_MODEL"]


@pytest.fixture(autouse=True)
def limpa_env(monkeypatch):
    for k in KEYS + MODELS:
        monkeypatch.delenv(k, raising=False)


def test_effective_models_defaults():
    assert effective_models() == {
        "groq": DEFAULTS["GROQ_MODEL"],
        "ollama": DEFAULTS["OLLAMA_CLOUD_MODEL"],
        "openrouter": DEFAULTS["OPENROUTER_MODEL"],
    }


def test_effective_models_respeita_env(monkeypatch):
    monkeypatch.setenv("GROQ_MODEL", "meu-modelo")
    assert effective_models()["groq"] == "meu-modelo"


def test_groq_primeiro(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "k")
    monkeypatch.setenv("OLLAMA_CLOUD_API_KEY", "k")
    monkeypatch.setenv("OPENROUTER_API_KEY", "k")
    llm = get_llm()
    assert type(llm).__name__ == "ChatGroq"


def test_ollama_sem_verbose(monkeypatch):
    monkeypatch.setenv("OLLAMA_CLOUD_API_KEY", "k")
    llm = get_llm(verbose=False)
    assert type(llm).__name__ == "ChatOpenAI"


def test_openrouter(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "k")
    llm = get_llm()
    assert type(llm).__name__ == "ChatOpenAI"


def test_falha_groq_cai_para_ollama(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "k")
    monkeypatch.setenv("OLLAMA_CLOUD_API_KEY", "k")
    with patch("langchain_groq.ChatGroq", side_effect=RuntimeError("boom")):
        llm = get_llm()
    assert type(llm).__name__ == "ChatOpenAI"


def test_falha_ollama_cai_para_openrouter(monkeypatch):
    monkeypatch.setenv("OLLAMA_CLOUD_API_KEY", "k")
    monkeypatch.setenv("OPENROUTER_API_KEY", "k")
    with patch("langchain_openai.ChatOpenAI", side_effect=[RuntimeError("boom"), object()]):
        llm = get_llm()
    assert llm is not None


def test_falha_openrouter_levanta(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "k")
    with patch("langchain_openai.ChatOpenAI", side_effect=RuntimeError("boom")):
        with pytest.raises(RuntimeError):
            get_llm(verbose=False)


def test_sem_chave_levanta():
    with pytest.raises(RuntimeError, match="Nenhuma chave"):
        get_llm(verbose=False)
