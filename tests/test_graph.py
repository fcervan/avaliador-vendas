"""Testes do grafo LangGraph com LLM fake (cobre full-pass + cada early-exit)."""

from types import SimpleNamespace

from src.graph import grade_transcricao


class MapaLLM:
    """Retorna score por critério conforme o nome da etapa no prompt."""

    def __init__(self, scores):
        self.scores = scores

    def invoke(self, prompt):
        texto = str(prompt)
        for criterio, score in self.scores.items():
            if f"'{criterio}'" in texto:  # etapa é interpolada entre aspas; evita "dor descoberta"
                return SimpleNamespace(content=f"Pontuação: {score}\nFeedback {criterio}")
        return SimpleNamespace(content="Pontuação: 0.0\nFallback")


def test_fluxo_completo():
    r = grade_transcricao(
        "t",
        MapaLLM({"saudacao": 0.9, "descoberta": 0.9, "apresentacao": 0.9, "fechamento": 0.9}),
    )
    assert r["final_score"] == 9.0
    assert r["veredito"] == "aprovado"
    assert r["fechamento_score"] == 0.9


def test_early_exit_na_saudacao():
    r = grade_transcricao(
        "t",
        MapaLLM({"saudacao": 0.1, "descoberta": 0.9, "apresentacao": 0.9, "fechamento": 0.9}),
    )
    assert r["descoberta_score"] == 0.0  # nem executou
    assert r["final_score"] == round(0.1 * 0.15 * 10, 2)


def test_early_exit_na_descoberta():
    r = grade_transcricao(
        "t",
        MapaLLM({"saudacao": 0.9, "descoberta": 0.2, "apresentacao": 0.9, "fechamento": 0.9}),
    )
    assert r["apresentacao_score"] == 0.0
    assert r["veredito"] == "reprovado"


def test_early_exit_na_apresentacao():
    r = grade_transcricao(
        "t",
        MapaLLM({"saudacao": 0.9, "descoberta": 0.9, "apresentacao": 0.4, "fechamento": 0.9}),
    )
    assert r["fechamento_score"] == 0.0
    assert r["final_score"] > 0.0
