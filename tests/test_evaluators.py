"""Testes dos nós avaliadores com LLM fake (sem rede)."""

from types import SimpleNamespace

from src.evaluators import (
    calculate_final,
    check_apresentacao,
    check_descoberta,
    check_fechamento,
    check_saudacao,
)


class FakeLLM:
    def __init__(self, content):
        self.content = content

    def invoke(self, _prompt):
        return SimpleNamespace(content=self.content)


def novo_state(texto="transcrição fake"):
    return {
        "transcricao": texto,
        "saudacao_score": 0.0,
        "descoberta_score": 0.0,
        "apresentacao_score": 0.0,
        "fechamento_score": 0.0,
        "saudacao_feedback": "",
        "descoberta_feedback": "",
        "apresentacao_feedback": "",
        "fechamento_feedback": "",
        "final_score": 0.0,
        "veredito": "",
    }


def test_grade_ok_extracao_01():
    st = check_saudacao(novo_state(), FakeLLM("Pontuação: 0.8\nBom rapport"))
    assert st["saudacao_score"] == 0.8
    assert "rapport" in st["saudacao_feedback"]


def test_grade_aceita_escala_010():
    st = check_descoberta(novo_state(), FakeLLM("Pontuação: 9\nÓtima descoberta"))
    assert st["descoberta_score"] == 0.9


def test_grade_parse_falha_zera():
    st = check_apresentacao(novo_state(), FakeLLM("texto sem nota"))
    assert st["apresentacao_score"] == 0.0
    assert "Falha parse" in st["apresentacao_feedback"]


def test_grade_resposta_sem_quebra_de_linha():
    st = check_fechamento(novo_state(), FakeLLM("Pontuação: 0.5"))
    assert st["fechamento_score"] == 0.5
    assert st["fechamento_feedback"]  # feedback = próprio texto


def test_calculate_final_pesos():
    st = novo_state()
    st.update(
        saudacao_score=1.0,
        descoberta_score=1.0,
        apresentacao_score=1.0,
        fechamento_score=1.0,
    )
    out = calculate_final(st)
    assert out["final_score"] == 10.0
    assert out["veredito"] == "aprovado"


def test_calculate_final_ponderada():
    st = novo_state()
    st.update(
        saudacao_score=1.0,
        descoberta_score=0.5,
        apresentacao_score=0.0,
        fechamento_score=0.0,
    )
    out = calculate_final(st)
    assert out["final_score"] == round((0.15 + 0.15) * 10, 2)
    assert out["veredito"] == "reprovado"
