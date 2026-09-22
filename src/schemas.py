"""Schemas do Avaliador de Vendas — espelha avaliador_de_redacao.ipynb State."""
from typing import TypedDict


class SalesState(TypedDict):
    transcricao: str
    saudacao_score: float
    descoberta_score: float
    apresentacao_score: float
    fechamento_score: float
    saudacao_feedback: str
    descoberta_feedback: str
    apresentacao_feedback: str
    fechamento_feedback: str
    final_score: float
    veredito: str


PESOS = {
    "saudacao": 0.15,
    "descoberta": 0.30,
    "apresentacao": 0.30,
    "fechamento": 0.25,
}

THRESHOLD = 0.5


def veredito(final_10: float) -> str:
    if final_10 >= 7.0:
        return "aprovado"
    if final_10 >= 5.0:
        return "atencao"
    return "reprovado"
