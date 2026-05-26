# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, session
from classes.university_class import University
from classes.graduate_class import Graduate
from classes.association_class import Association

app = Flask(__name__)

DB_NAME = 'universidades_alumni.db'

# Carrega todos os dados ao iniciar
University.read(DB_NAME)
Graduate.read(DB_NAME)
Association.read(DB_NAME)

if University.lst:
    University.first()

prev_option = ""
app.secret_key = 'BAD_SECRET_KEY'


# =====================================================================
# 1. ROTA PRINCIPAL: DIPLOMADOS (Com Inserção e Pesquisa Activas)
# =====================================================================
@app.route("/", methods=["POST", "GET"])
def index():
    # --- LOGICA DE INSERÇÃO (POST) ---
    if request.method == "POST":
        action = request.form.get("action")
        if action == "save":
            g_id = int(request.form["graduate_id"])
            u_id = int(request.form["university_id"])
            obs = request.form["observations"]
            
            # Cria a instância (a vossa estrutura de classes trata de guardar na BD através do Graduate)
            novo_graduado = Graduate(g_id, u_id, obs)
            # Como a vossa classe escreve na memória, re-lemos ou guardamos se necessário.
            # Se a vossa classe exigir um Graduate.write(DB_NAME) explícito, a tua amiga pode descomentar a linha abaixo:
            # Graduate.write(DB_NAME)

    # --- LOGICA DE PESQUISA (GET) ---
    termo_pesquisa = request.args.get("search", "").strip().lower()
    lista_graduados_objetos = []
    
    if Graduate.lst:
        for cod in Graduate.lst:
            obj_graduado = Graduate.obj[cod]
            
            if termo_pesquisa:
                # Procura por correspondência no ID ou nas Observações
                id_match = termo_pesquisa in str(obj_graduado.graduate_id).lower()
                obs_match = termo_pesquisa in str(obj_graduado.observations).lower()
                
                if id_match or obs_match:
                    lista_graduados_objetos.append(obj_graduado)
            else:
                lista_graduados_objetos.append(obj_graduado)
            
    return render_template("index.html", 
                           lista_graduados=lista_graduados_objetos, 
                           ulogin=session.get("user"))


# =====================================================================
# 2. ROTA DAS UNIVERSIDADES
# =====================================================================
@app.route("/universities", methods=["POST", "GET"])
def universities():
    global prev_option
    
    butshow, butedit = "enabled", "disabled"
    option = request.args.get("option")
    
    if option == "edit":
        butshow, butedit = "disabled", "enabled"
    elif option == "delete":
        if University.lst:
            code_atual = University.lst[University.pos]
            obj = University.obj[code_atual]
            University.remove(obj.uni_id)
            if not University.previous():
                University.first()
    elif option == "insert":
        butshow, butedit = "disabled", "enabled"
    elif option == 'cancel':
        pass
    elif prev_option == 'insert' and option == 'save':
        u_id = int(request.form["uni_id"])
        name = request.form["uni_name"]
        found_date = request.form["foundation_date"]
        obj = University(u_id, name, found_date)
        University.last()
    elif prev_option == 'edit' and option == 'save':
        if University.lst:
            code_atual = University.lst[University.pos]
            obj = University.obj[code_atual]
            obj._uni_name = request.form["uni_name"]
            obj._foundation_date = request.form["foundation_date"]
        
    elif option == "first":
        University.first()
    elif option == "previous":
        University.previous()
    elif option == "next":
        University.next()
    elif option == "last":
        University.last()
    elif option == 'exit':
        return "<h1 style='font-family:serif; text-align:center; margin-top:100px;'>Obrigado por usar a aplicação do Grupo G12</h1>"
        
    prev_option = option
    
    if option == 'insert' or not University.lst:
        uni_id = ""
        uni_name = ""
        foundation_date = ""
    else:
        if University.pos >= len(University.lst):
            University.pos = 0
        code_atual = University.lst[University.pos]
        obj = University.obj[code_atual]
        uni_id = obj.uni_id
        uni_name = obj.uni_name
        foundation_date = obj.foundation_date
        
    lista_uni_objetos = []
    if University.lst:
        for cod in University.lst:
            lista_uni_objetos.append(University.obj[cod])
        
    return render_template("universities.html", 
                           butshow=butshow, 
                           butedit=butedit, 
                           uni_id=uni_id, 
                           uni_name=uni_name, 
                           foundation_date=foundation_date,
                           lista_universidades=lista_uni_objetos,
                           ulogin=session.get("user"))


# =====================================================================
# 3. ROTA DAS ASSOCIAÇÕES
# =====================================================================
@app.route("/associations", methods=["POST", "GET"])
def associations():
    lista_assoc_objetos = []
    if Association.lst:
        for cod in Association.lst:
            lista_assoc_objetos.append(Association.obj[cod])
            
    return render_template("associations.html", 
                           lista_associacoes=lista_assoc_objetos, 
                           ulogin=session.get("user"))


if __name__ == '__main__':
    app.run(debug=True)
