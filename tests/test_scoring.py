import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from evaluators import extract_score  # noqa: E402
from schemas import veredito  # noqa: E402


def test_extract_01():
    assert extract_score("Pontuação: 0.8\nBom") == 0.8


def test_extract_010():
    assert extract_score("Pontuação: 8\nBom") == 0.8


def test_veredito():
    assert veredito(7.5) == "aprovado"
    assert veredito(6.0) == "atencao"
    assert veredito(4.9) == "reprovado"
