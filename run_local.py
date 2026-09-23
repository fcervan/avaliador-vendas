"""Avaliador de Vendas em lote — uso local.

Exemplos:
    python run_local.py --csv data/exemplos.csv --out resultados.csv
    python run_local.py --csv meu_dataset.csv --col transcricao --out saidas/rodada1.csv --limit 3

Entrada: CSV com coluna de transcrição (default: transcricao). Colunas id/nivel são opcionais.
Saída: CSV com scores 0-10 por critério + final + veredito + feedbacks.
Chaves via .env (GROQ_API_KEY / OLLAMA_CLOUD_API_KEY / OPENROUTER_API_KEY). Nunca versionar o .env.
"""

import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from dotenv import load_dotenv

load_dotenv()

from src.graph import grade_transcricao  # noqa: E402
from src.llm_client import get_llm  # noqa: E402

CRITERIOS = ["saudacao", "descoberta", "apresentacao", "fechamento"]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Avalia transcrições de vendas em lote.")
    p.add_argument("--csv", required=True, help="CSV de entrada (ex: data/exemplos.csv)")
    p.add_argument(
        "--col", default="transcricao", help="Coluna com a transcrição (default: transcricao)"
    )
    p.add_argument("--out", required=True, help="CSV de saída (ex: resultados.csv)")
    p.add_argument("--limit", type=int, default=None, help="Avalia só as N primeiras linhas")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    src = Path(args.csv)
    if not src.exists():
        print(f"ERRO: arquivo de entrada não encontrado: {src}", file=sys.stderr)
        return 2
    df = pd.read_csv(src)
    if args.col not in df.columns:
        print(f"ERRO: coluna '{args.col}' não existe. Colunas: {list(df.columns)}", file=sys.stderr)
        return 2
    if args.limit is not None:
        df = df.head(args.limit)

    llm = get_llm()
    linhas = []
    for i, row in df.iterrows():
        r = grade_transcricao(str(row[args.col]), llm)
        linha = {
            "id": row.get("id", i),
            "nivel": row.get("nivel", ""),
            "saudacao": round(r["saudacao_score"] * 10, 2),
            "descoberta": round(r["descoberta_score"] * 10, 2),
            "apresentacao": round(r["apresentacao_score"] * 10, 2),
            "fechamento": round(r["fechamento_score"] * 10, 2),
            "final": r["final_score"],
            "veredito": r["veredito"],
        }
        for k in CRITERIOS:
            linha[f"feedback_{k}"] = r.get(f"{k}_feedback", "")
        linhas.append(linha)
        print(f"[{linha['id']}] final={linha['final']:.1f} veredito={linha['veredito']}")

    out = pd.DataFrame(linhas)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(out_path, index=False)
    print(f"\nSalvo em {out_path} ({len(out)} linhas)")
    if len(out):
        print(f"Média final: {out['final'].mean():.1f}")
        print(out["veredito"].value_counts().to_string())
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
