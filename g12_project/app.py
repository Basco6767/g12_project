# -*- coding: utf-8 -*-
"""
app.py — Aplicação Flask do Grupo G12 (Fase 2, passo 4).

Mantém a informação da base de dados (CRUD sobre Universidades, Associações
e Graduados) e disponibiliza um painel de análise de dados com Pandas +
Matplotlib (inscrições ao longo do tempo).

Correr com:  python app.py   (e abrir http://127.0.0.1:5000)
"""
import os
from functools import wraps

from flask import (Flask, render_template, request, redirect, url_for, flash,
                   session)

from classes.university import University
from classes.graduate import Graduate
from classes.association import Association
from classes.membership import Membership
from classes.userlogin import Userlogin

import analise
import graficos

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "universidades_alumni.db")

app = Flask(__name__)
app.secret_key = "g12-alumni-secret"

prev_option = ""


def carregar_dados():
    """(Re)carrega todas as classes a partir da BD para memória."""
    University.read(DB_PATH)
    Graduate.read(DB_PATH)
    Association.read(DB_PATH)
    Membership.read(DB_PATH)
    Userlogin.read(DB_PATH)


carregar_dados()


def login_required(f):
    """Decorator que protege uma rota: exige sessão iniciada."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("user") is None:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


# ---------------------------------------------------------------------------
# Login / Logoff / Validação (abordagem da lição 10 — classe Userlogin)
# ---------------------------------------------------------------------------
@app.route("/login")
def login():
    return render_template("login.html", id=0, user="", password="",
                           ulogin=session.get("user"), resul="")


@app.route("/logoff")
def logoff():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/chklogin", methods=["post", "get"])
def chklogin():
    user = request.form["user"]
    password = request.form["password"]
    resul = Userlogin.chk_password(user, password)
    if resul == "Valid":
        session["user"] = user
        return redirect(url_for("index"))
    return render_template("login.html", user=user, password=password,
                           ulogin=session.get("user"), resul=resul)


# ---------------------------------------------------------------------------
# Manutenção de utilizadores (apenas grupo 'admin') — baseado na lição
# ---------------------------------------------------------------------------
@app.route("/Userlogin", methods=["post", "get"])
@login_required
def userlogin():
    global prev_option
    msg = ""
    ulogin = session.get("user")
    user_id = Userlogin.get_user_id(ulogin)
    group = Userlogin.obj[user_id].usergroup
    if group != "admin":
        butshow = "enabled"
        butedit = "disabled"
    option = request.args.get("option")
    if option == "edit":
        butshow = "disabled"
        butedit = "enabled"
    elif option == "delete":
        obj = Userlogin.current(Userlogin.lst[Userlogin.pos])
        if obj.id != user_id:
            Userlogin.remove(obj.id)
            if not Userlogin.previous():
                Userlogin.first()
        else:
            msg = "You cannot delete the same user"
        butshow = "enabled"
        butedit = "disabled"
    elif option == "insert":
        butshow = "disabled"
        butedit = "enabled"
    elif option == "cancel":
        pass
    elif prev_option == "insert" and option == "save":
        user = request.form["user"]
        if len(Userlogin.find(user, "user")) == 0:
            usergroup = request.form["usergroup"]
            password = request.form["password"]
            obj = Userlogin(0, user, usergroup, Userlogin.set_password(password))
            Userlogin.insert(obj.id)
        else:
            msg = "duplicate username"
        Userlogin.last()
    elif prev_option == "edit" and option == "save":
        obj = Userlogin.current(Userlogin.lst[Userlogin.pos])
        if group == "admin":
            obj.usergroup = request.form["usergroup"]
        if request.form["password"] != "":
            obj.password = Userlogin.set_password(request.form["password"])
        Userlogin.update(obj.id)
    elif option == "first":
        Userlogin.first()
    elif option == "previous":
        Userlogin.previous()
    elif option == "next":
        Userlogin.nextrec()
    elif option == "last":
        Userlogin.last()
    elif option == "exit":
        return render_template("index.html", ulogin=session.get("user"),
                               kpis=analise.summary_kpis(), ativo="home")

    prev_option = option
    if group == "admin":
        butshow = "enabled"
        butedit = "disabled"

    if option == "insert" or len(Userlogin.lst) == 0:
        id = 0
        user = ""
        usergroup = ""
        password = ""
    else:
        obj = Userlogin.current(Userlogin.lst[Userlogin.pos])
        id = obj.id
        user = obj.user
        usergroup = obj.usergroup
        password = ""
    return render_template("userlogin.html", butshow=butshow, butedit=butedit,
                           msg=msg, id=id, user=user, usergroup=usergroup,
                           password=password, ulogin=session.get("user"),
                           group=group, ativo="users")


# ---------------------------------------------------------------------------
# Página inicial — painel com KPIs
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    kpis = analise.summary_kpis()
    return render_template("index.html", kpis=kpis, ativo="home",
                           ulogin=session.get("user"))


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
            University.insert(u.uni_id)
            flash(f"Universidade '{nome}' adicionada com sucesso.", "ok")
    except (ValueError, KeyError):
        flash("Dados inválidos no formulário.", "erro")
    return redirect(url_for("universities"))


@app.route("/universities/delete/<int:uni_id>")
def delete_university(uni_id):
    if uni_id in University.obj:
        University.remove(uni_id)
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
            Association.insert(a.association_id)
            flash(f"Associação '{desig}' adicionada.", "ok")
    except (ValueError, KeyError):
        flash("Dados inválidos no formulário.", "erro")
    return redirect(url_for("associations"))


@app.route("/associations/delete/<int:a_id>")
def delete_association(a_id):
    if a_id in Association.obj:
        Association.remove(a_id)
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
# Memberships — inscrições (universidade + associação), listagem e pesquisa
# ---------------------------------------------------------------------------
@app.route("/memberships")
def memberships():
    termo = request.args.get("search", "").strip().lower()

    # Construir linhas enriquecidas com o nome da universidade e a designação
    # da associação (os IDs sozinhos seriam pouco legíveis).
    linhas = []
    for code in Membership.lst:
        m = Membership.obj[code]
        uni = University.obj.get(m.university_id)
        assoc = Association.obj.get(m.association_id)
        linhas.append({
            "university_id": m.university_id,
            "university_name": uni.uni_name if uni else "—",
            "association_id": m.association_id,
            "association_name": assoc.designation if assoc else "—",
            "registration_date": m.registration_date,
            "fee": m.fee,
        })

    if termo:
        linhas = [r for r in linhas
                  if termo in str(r["university_id"]).lower()
                  or termo in str(r["university_name"]).lower()
                  or termo in str(r["association_id"]).lower()
                  or termo in str(r["association_name"]).lower()]

    total = len(linhas)
    return render_template("memberships.html", lista=linhas, termo=termo,
                           total=total, ativo="memberships")


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
    app.run(debug=False)
