# -*- coding: utf-8 -*-
"""
analise.py — Análise de dados do projeto com Pandas (Fase 2, passo 2).
Módulo isolado, independente da web. Centraliza a leitura da base de dados
para DataFrames e os cálculos analíticos (inscrições ao longo do tempo,
receita e fee médio).
Testar diretamente com:  python analise.py
"""
import os
import sqlite3
import pandas as pd
 
# caminho absoluto para a base de dados, independente de onde o script é executado
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "universidades_alumni.db")
 
 
# função privada para centralizar a ligação — não repetir o caminho em cada função
def _connect():
    return sqlite3.connect(DB_PATH)
 
 
def load_memberships():
    """Lê a tabela Membership para um DataFrame, com a data já convertida."""
    with _connect() as conn:
        df = pd.read_sql("SELECT * FROM Membership", conn)
 
    # converte a coluna de datas de texto para datetime do Pandas
    # errors='coerce' transforma datas inválidas em NaT em vez de lançar erro
    df["registration_date"] = pd.to_datetime(
        df["registration_date"], format="ISO8601", errors="coerce"
    )
    return df
 
 
# as restantes tabelas não precisam de tratamento extra, só leitura direta
def load_universities():
    with _connect() as conn:
        return pd.read_sql("SELECT * FROM University", conn)
 
 
def load_associations():
    with _connect() as conn:
        return pd.read_sql("SELECT * FROM Association", conn)
 
 
def load_graduates():
    with _connect() as conn:
        return pd.read_sql("SELECT * FROM Graduate", conn)
 
# Análise principal: inscrições (memberships) ao longo do tempo
def memberships_per_year():
    """Nº de inscrições por ano."""
    df = load_memberships()
    # remove linhas sem data válida antes de agrupar
    serie = df.dropna(subset=["registration_date"]).copy()
    # extrai o ano de cada data e agrupa, contando quantas inscrições há por ano
    serie["ano"] = serie["registration_date"].dt.year
    return serie.groupby("ano").size().rename("inscricoes")
 
 
def memberships_per_month():
    """Nº de inscrições por mês (série temporal contínua ano-mês)."""
    df = load_memberships()
    serie = df.dropna(subset=["registration_date"]).copy()
    # to_period("M") agrupa por mês mantendo a ordem cronológica
    serie["ano_mes"] = serie["registration_date"].dt.to_period("M")
    contagem = serie.groupby("ano_mes").size().rename("inscricoes")
    # converte de Period para timestamp para compatibilidade com gráficos
    contagem.index = contagem.index.to_timestamp()
    return contagem
 
 
def fee_per_year():
    """Receita total e fee médio por ano."""
    df = load_memberships()
    serie = df.dropna(subset=["registration_date"]).copy()
    serie["ano"] = serie["registration_date"].dt.year
    # .agg calcula as três métricas de uma vez em vez de três groupby separados
    return serie.groupby("ano")["fee"].agg(["sum", "mean", "count"])
 
 
def summary_kpis():
    """Conjunto de indicadores-chave para o painel."""
    df = load_memberships()
    validas = df.dropna(subset=["registration_date"])
    por_ano = memberships_per_year()
 
    # int() e round() são necessários porque o Pandas devolve tipos numpy
    # que o Flask não consegue passar diretamente aos templates Jinja
    return {
        "total_memberships":   int(len(df)),
        "total_universidades": int(load_universities().shape[0]),
        "total_associacoes":   int(load_associations().shape[0]),
        "total_graduados":     int(load_graduates().shape[0]),
        "fee_medio":           round(float(df["fee"].mean()), 2),
        "receita_total":       round(float(df["fee"].sum()), 2),
        "ano_pico":            int(por_ano.idxmax()),
        "inscricoes_pico":     int(por_ano.max()),
        "primeira_data":       validas["registration_date"].min().strftime("%d/%m/%Y"),
        "ultima_data":         validas["registration_date"].max().strftime("%d/%m/%Y"),
    }
 
 
# permite testar o módulo diretamente sem precisar de arrancar a aplicação web
if __name__ == "__main__":
    print("=== KPIs ===")
    for chave, valor in summary_kpis().items():
        print(f"  {chave}: {valor}")
    print("\n=== Inscrições por ano ===")
    print(memberships_per_year())
    print("\n=== Receita e fee médio por ano ===")
    print(fee_per_year())
