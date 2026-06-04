# -*- coding: utf-8 -*-
"""
app.py — Aplicação Flask do Grupo G12 (Fase 2, passo 4).

Mantém a informação da base de dados (CRUD sobre Universidades, Associações
e Graduados) e disponibiliza um painel de análise de dados com Pandas +
Matplotlib (inscrições ao longo do tempo).

Correr com:  python app.py   (e abrir http://127.0.0.1:5000)
"""
import os

from flask import Flask, render_template, request, redirect, url_for, flash

from classes.university import University
from classes.graduate import Graduate
from classes.association import Association
from classes.membership import Membership

import analise
import graficos

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "universidades_alumni.db")

app = Flask(__name__)
app.secret_key = "g12-alumni-secret"


def carregar_dados():
    """(Re)carrega todas as classes a partir da BD para memória."""
    University.read(DB_PATH)
    Graduate.read(DB_PATH)
    Association.read(DB_PATH)
    Membership.read(DB_PATH)


carregar_dados()


# ---------------------------------------------------------------------------
# Página inicial — painel com KPIs
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    kpis = analise.summary_kpis()
    return render_template("index.html", kpis=kpis, ativo="home")


# ---------------------------------------------------------------------------
# Universidades — listagem, pesquisa, inserção e remoção
# ---------------------------------------------------------------------------
@app.route("/universities")
def universities():
    termo = request.args.get("search", "").strip().lower()
    lista = [University.obj[c] for c in University.lst]
    if termo:
        lista = [u for u in lista
                 if termo in str(u.uni_name).lower()
                 or termo in str(u.uni_id).lower()]
    lista = sorted(lista, key=lambda u: str(u.uni_name).lower())
    return render_template("universities.html", lista=lista,
                           termo=termo, ativo="universities")


@app.route("/universities/add", methods=["POST"])
def add_university():
    try:
        uni_id = int(request.form["uni_id"])
        nome = request.form["uni_name"].strip()
        data = request.form["foundation_date"].strip()
        if uni_id in University.obj:
            flash(f"Já existe uma universidade com o ID {uni_id}.", "erro")
        else:
            u = University(uni_id, nome, data)
            u.write()
            flash(f"Universidade '{nome}' adicionada com sucesso.", "ok")
    except (ValueError, KeyError):
        flash("Dados inválidos no formulário.", "erro")
    return redirect(url_for("universities"))


@app.route("/universities/delete/<int:uni_id>")
def delete_university(uni_id):
    if University.remove(uni_id):
        flash(f"Universidade {uni_id} removida.", "ok")
    else:
        flash(f"Não foi possível remover a universidade {uni_id}.", "erro")
    return redirect(url_for("universities"))


# ---------------------------------------------------------------------------
# Associações — listagem, pesquisa, inserção e remoção
# ---------------------------------------------------------------------------
@app.route("/associations")
def associations():
    termo = request.args.get("search", "").strip().lower()
    lista = [Association.obj[c] for c in Association.lst]
    if termo:
        lista = [a for a in lista
                 if termo in str(a.designation).lower()
                 or termo in str(a.objective).lower()]
    lista = sorted(lista, key=lambda a: str(a.designation).lower())
    return render_template("associations.html", lista=lista,
                           termo=termo, ativo="associations")


@app.route("/associations/add", methods=["POST"])
def add_association():
    try:
        a_id = int(request.form["association_id"])
        desig = request.form["designation"].strip()
        obj = request.form["objective"].strip()
        if a_id in Association.obj:
            flash(f"Já existe uma associação com o ID {a_id}.", "erro")
        else:
            a = Association(a_id, desig, obj)
            a.write()
            flash(f"Associação '{desig}' adicionada.", "ok")
    except (ValueError, KeyError):
        flash("Dados inválidos no formulário.", "erro")
    return redirect(url_for("associations"))


@app.route("/associations/delete/<int:a_id>")
def delete_association(a_id):
    if Association.remove(a_id):
        flash(f"Associação {a_id} removida.", "ok")
    else:
        flash(f"Não foi possível remover a associação {a_id}.", "erro")
    return redirect(url_for("associations"))


# ---------------------------------------------------------------------------
# Graduados — listagem e pesquisa
# ---------------------------------------------------------------------------
@app.route("/graduates")
def graduates():
    termo = request.args.get("search", "").strip().lower()
    lista = [Graduate.obj[c] for c in Graduate.lst]
    if termo:
        lista = [g for g in lista
                 if termo in str(g.graduate_id).lower()
                 or termo in str(g.observations).lower()
                 or termo in str(g.university_id).lower()]
    return render_template("graduates.html", lista=lista,
                           termo=termo, ativo="graduates")


# ---------------------------------------------------------------------------
# Análise + gráficos
# ---------------------------------------------------------------------------
@app.route("/analysis")
def analysis():
    kpis = analise.summary_kpis()
    img_mes = graficos.grafico_inscricoes_por_mes()
    img_ano = graficos.grafico_inscricoes_por_ano()
    img_receita = graficos.grafico_receita_por_ano()

    # tabela de apoio (Pandas -> lista de dicts para o template)
    tabela = analise.fee_per_year().reset_index()
    tabela["sum"] = tabela["sum"].round(0).astype(int)
    tabela["mean"] = tabela["mean"].round(2)
    tabela = tabela.to_dict(orient="records")

    return render_template("analysis.html", kpis=kpis,
                           img_mes=img_mes, img_ano=img_ano,
                           img_receita=img_receita, tabela=tabela,
                           ativo="analysis")


if __name__ == "__main__":
    app.run(debug=True)
