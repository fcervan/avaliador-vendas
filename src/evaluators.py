"""Nós avaliadores — mesmo padrão do avaliador_de_redacao: prompt Pontuação + regex."""
import re

from langchain_core.prompts import ChatPromptTemplate

try:
    from .rubrics import RUBRICS
except ImportError:
    from rubrics import RUBRICS


def extract_score(content: str) -> float:
    m = re.search(r"Pontuação:\s*(\d+(\.\d+)?)", content)
    if m:
        v = float(m.group(1))
        return v / 10.0 if v > 1.0 else v  # aceita 0-1 ou 0-10
    raise ValueError(f"Não foi possível extrair pontuação de: {content}")


def _grade(llm, criterio: str, transcricao: str):
    prompt = ChatPromptTemplate.from_template(
        "Avalie a etapa '{criterio}' do vendedor na transcrição abaixo.\n"
        "Rubrica: {rubrica}\n"
        "Dê Pontuação entre 0 e 1.\n"
        "Resposta deve começar com 'Pontuação: ' seguida do número, "
        "depois 2 linhas de feedback.\n\nTranscrição: {texto}"
    )
    result = llm.invoke(
        prompt.format(criterio=criterio, rubrica=RUBRICS[criterio], texto=transcricao)
    )
    texto = result.content
    try:
        score = extract_score(texto)
    except ValueError:
        score, texto = 0.0, f"Pontuação: 0.0\nFalha parse. Resposta: {texto}"
    feedback = texto.split("\n", 1)[1] if "\n" in texto else texto
    return score, feedback.strip()


def check_saudacao(state, llm):
    s, f = _grade(llm, "saudacao", state["transcricao"])
    state["saudacao_score"], state["saudacao_feedback"] = s, f
    return state


def check_descoberta(state, llm):
    s, f = _grade(llm, "descoberta", state["transcricao"])
    state["descoberta_score"], state["descoberta_feedback"] = s, f
    return state


def check_apresentacao(state, llm):
    s, f = _grade(llm, "apresentacao", state["transcricao"])
    state["apresentacao_score"], state["apresentacao_feedback"] = s, f
    return state


def check_fechamento(state, llm):
    s, f = _grade(llm, "fechamento", state["transcricao"])
    state["fechamento_score"], state["fechamento_feedback"] = s, f
    return state


def calculate_final(state):
    try:
        from .schemas import PESOS, veredito
    except ImportError:
        from schemas import PESOS, veredito

    final01 = (
        state.get("saudacao_score", 0.0) * PESOS["saudacao"]
        + state.get("descoberta_score", 0.0) * PESOS["descoberta"]
        + state.get("apresentacao_score", 0.0) * PESOS["apresentacao"]
        + state.get("fechamento_score", 0.0) * PESOS["fechamento"]
    )
    state["final_score"] = round(final01 * 10, 2)
    state["veredito"] = veredito(state["final_score"])
    return state
