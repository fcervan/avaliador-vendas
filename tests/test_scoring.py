from src.evaluators import extract_score
from src.schemas import veredito


def test_extract_01():
    assert extract_score("Pontuação: 0.8\nBom") == 0.8


def test_extract_010():
    assert extract_score("Pontuação: 8\nBom") == 0.8


def test_veredito():
    assert veredito(7.5) == "aprovado"
    assert veredito(6.0) == "atencao"
    assert veredito(4.9) == "reprovado"
