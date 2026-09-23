"""Testes do run_local.py com LLM e avaliação mockados (sem rede, sem custo)."""

import sys
from pathlib import Path
from unittest.mock import patch

import pandas as pd

import run_local


def fake_grade(texto, _llm):
    return {
        "saudacao_score": 0.8,
        "descoberta_score": 0.7,
        "apresentacao_score": 0.6,
        "fechamento_score": 0.9,
        "final_score": 7.35,
        "veredito": "aprovado",
        "saudacao_feedback": "ok",
        "descoberta_feedback": "ok",
        "apresentacao_feedback": "ok",
        "fechamento_feedback": "ok",
    }


def escreve_csv(path: Path, coluna="transcricao", linhas=("t1", "t2", "t3")):
    df = pd.DataFrame({"id": [f"id{i}" for i in range(len(linhas))], coluna: list(linhas)})
    df.to_csv(path, index=False)
    return path


def roda_cli(*args):
    sys.argv = ["run_local.py", *args]
    with (
        patch("run_local.get_llm", return_value=object()),
        patch("run_local.grade_transcricao", side_effect=fake_grade),
    ):
        return run_local.main()


def test_sucesso_com_limit(tmp_path):
    entrada = escreve_csv(tmp_path / "in.csv")
    saida = tmp_path / "nested" / "out.csv"
    assert roda_cli("--csv", str(entrada), "--out", str(saida), "--limit", "2") == 0
    df = pd.read_csv(saida)
    assert len(df) == 2
    assert list(df["final"]) == [7.35, 7.35]
    assert set(df["veredito"]) == {"aprovado"}


def test_coluna_customizada(tmp_path):
    entrada = escreve_csv(tmp_path / "in.csv", coluna="fala", linhas=("a",))
    saida = tmp_path / "out.csv"
    assert roda_cli("--csv", str(entrada), "--col", "fala", "--out", str(saida)) == 0
    assert len(pd.read_csv(saida)) == 1


def test_arquivo_inexistente(tmp_path):
    assert roda_cli("--csv", str(tmp_path / "nope.csv"), "--out", str(tmp_path / "o.csv")) == 2


def test_coluna_inexistente(tmp_path):
    entrada = escreve_csv(tmp_path / "in.csv")
    assert (
        roda_cli("--csv", str(entrada), "--col", "col_errada", "--out", str(tmp_path / "o.csv"))
        == 2
    )
