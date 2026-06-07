# G12 — Gestão de Dados Académicos

Aplicação Flask para gestão e análise da base de dados de universidades,
associações académicas e graduados.

## Introdução

Este documento explica como utilizar o programa, seguindo as boas práticas
de programação.

## Como correr

Este projeto precisa de alguns programas para correr, indicados no ficheiro
`requirements.txt`. Antes de correr o programa pela primeira vez, deve-se fazer:

    pip install -r requirements.txt

Depois disso, pode-se correr o `app.py` e abrir http://127.0.0.1:5000 no browser.

## Estrutura

- `app.py` — aplicação Flask (rotas, CRUD, painel)
- `analise.py` — análise de dados com Pandas
- `graficos.py` — gráficos com Matplotlib
- `main.py` — programa de teste das classes (Fase 1)
- `classes/` — classes do modelo conceptual (derivadas de Gclass)
- `data/` — base de dados SQLite, CSV de origem e notebook de carregamento
- `templates/` / `static/` — interface web (HTML + CSS)
- `diagrama.jpg` — diagrama de classes

## Funcionalidades

1. Flask CRUD — listar, pesquisar, adicionar e remover universidades e
   associações e listar e pesquisar graduados (gravado em SQLite).
2. Análise (Pandas) — inscrições por mês/ano, receita e fee médio por ano.
3. Gráficos (Matplotlib) — barras por ano, receita/fee médio.
4. Interface — painel de KPIs, pesquisa, mensagens de feedback.
