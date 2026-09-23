"""Testes de scoring puro (sem LLM, sem rede)."""

import pytest

from src.evaluators import extract_score
from src.schemas import veredito


def test_extract_01():
    assert extract_score("Pontuação: 0.8\nBom") == 0.8


def test_extract_010_converte_para_01():
    assert extract_score("Pontuação: 8\nBom") == 0.8


def test_extract_limite_um():
    assert extract_score("Pontuação: 1.0\nOk") == 1.0


def test_extract_sem_pontuacao_levanta():
    with pytest.raises(ValueError):
        extract_score("Sem nota aqui")


def test_veredito_faixas():
    assert veredito(10.0) == "aprovado"
    assert veredito(7.0) == "aprovado"
    assert veredito(6.99) == "atencao"
    assert veredito(5.0) == "atencao"
    assert veredito(4.99) == "reprovado"
    assert veredito(0.0) == "reprovado"
