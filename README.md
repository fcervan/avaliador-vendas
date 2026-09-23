# Avaliador de Vendas — ideia 1 do backlog

Derivado de `Projetos_Praticos_de_IA/.../avaliador_de_redacao.ipynb`.
Padrão: rubrica 4 etapas + LLM-as-judge + LangGraph condicional + early-exit 0.5 + média ponderada.

- Pesos: saudação 0.15 / descoberta 0.30 / apresentação 0.30 / fechamento 0.25
- Veredito: >=7 aprovado, 5-7 atenção, <5 reprovado
- LLM: Groq → Ollama Cloud → OpenRouter (Groq primeiro, mais rápido — ver `src/llm_client.py`, `.env.example`)
- Sem mascaramento PII nesta v1 (decisão registrada)

## Uso local
```bash
pip install -r requirements.txt
cp .env.example .env  # preencher GROQ_API_KEY (nunca versionar o .env)
pytest tests/ -q
jupyter notebook notebooks/01_avaliador_vendas.ipynb
```

## Uso local em lote (seu dataset)
```bash
python run_local.py --csv data/exemplos.csv --out resultados.csv
python run_local.py --csv meu_dataset.csv --col transcricao --out saidas/rodada1.csv --limit 3
```
Mesmo formato de `data/exemplos.csv` (`id,nivel,transcricao`). Saída com scores 0-10 + final + veredito + feedbacks.

## Uso Colab (HTTPS — SSH não funciona no Colab)
```python
!git clone https://github.com/fcervan/avaliador-vendas.git
%cd avaliador-vendas
# abra notebooks/02_uso_colab.ipynb e dê Run all
# chaves digitadas via getpass na 1ª célula (nada é versionado)
```

## Estrutura
`notebooks/` didático → `src/` modular → `data/exemplos.csv` (bom/medio/ruim) → `tests/`
