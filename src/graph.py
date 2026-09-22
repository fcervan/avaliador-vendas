"""Grafo LangGraph com early-exit 0.5 — porta do avaliador_de_redacao."""
from functools import partial

from langgraph.graph import END, StateGraph

try:
    from . import evaluators as ev
    from .schemas import THRESHOLD, SalesState
except ImportError:
    import evaluators as ev
    from schemas import THRESHOLD, SalesState


def build_graph(llm):
    wf = StateGraph(SalesState)
    wf.add_node("saudacao", partial(ev.check_saudacao, llm=llm))
    wf.add_node("descoberta", partial(ev.check_descoberta, llm=llm))
    wf.add_node("apresentacao", partial(ev.check_apresentacao, llm=llm))
    wf.add_node("fechamento", partial(ev.check_fechamento, llm=llm))
    wf.add_node("final", ev.calculate_final)

    wf.add_conditional_edges(
        "saudacao",
        lambda x: "descoberta" if x["saudacao_score"] > THRESHOLD else "final",
    )
    wf.add_conditional_edges(
        "descoberta",
        lambda x: "apresentacao" if x["descoberta_score"] > THRESHOLD else "final",
    )
    wf.add_conditional_edges(
        "apresentacao",
        lambda x: "fechamento" if x["apresentacao_score"] > THRESHOLD else "final",
    )
    wf.add_conditional_edges("fechamento", lambda x: "final")
    wf.set_entry_point("saudacao")
    wf.add_edge("final", END)
    return wf.compile()


def grade_transcricao(transcricao: str, llm) -> dict:
    app = build_graph(llm)
    init: SalesState = {
        "transcricao": transcricao,
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
    return app.invoke(init)
