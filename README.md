# Avaliador de Vendas — ideia 1 do backlog

Derivado de `Projetos_Praticos_de_IA/.../avaliador_de_redacao.ipynb`.
Padrão: rubrica 4 etapas + LLM-as-judge + LangGraph condicional + early-exit 0.5 + média ponderada.

- Pesos: saudação 0.15 / descoberta 0.30 / apresentação 0.30 / fechamento 0.25
- Veredito: >=7 aprovado, 5-7 atenção, <5 reprovado
- LLM: OpenRouter → Ollama Cloud → Groq (ver `src/llm_client.py`, `.env.example`)
- Sem mascaramento PII nesta v1 (decisão registrada)

## Uso local
```bash
pip install -r requirements.txt
cp .env.example .env  # preencher chaves
pytest tests/ -q
jupyter notebook notebooks/01_avaliador_vendas.ipynb
```

## Uso Colab
```python
!git clone <url-deste-repo>
%cd avaliador-vendas
!pip install -r requirements.txt -q
# Colab Secrets: OPENROUTER_API_KEY / OLLAMA_CLOUD_API_KEY / GROQ_API_KEY
```

## Estrutura
`notebooks/` didático → `src/` modular → `data/exemplos.csv` (bom/medio/ruim) → `tests/`
