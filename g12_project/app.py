# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, session
from classes.university_class import University

app = Flask(__name__)

# Nome da base de dados (deve estar na mesma pasta que este app.py)
DB_NAME = 'universidades_alumni.db'

# Carrega os dados do SQLite para a memória
University.read(DB_NAME)

# Posiciona no primeiro registo se existirem dados carregados
if University.lst:
    University.first()

prev_option = ""
app.secret_key = 'BAD_SECRET_KEY'

@app.route("/", methods=["post", "get"])
def index():
    global prev_option
    
    butshow, butedit = "enabled", "disabled"
    option = request.args.get("option")
    
    # --- LOGICA DE MANUTENÇÃO ---
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
        
        # Cria a instância (adiciona automaticamente às estruturas da Gclass)
        obj = University(u_id, name, found_date)
        University.last()
        
    elif prev_option == 'edit' and option == 'save':
        if University.lst:
            code_atual = University.lst[University.pos]
            obj = University.obj[code_atual]
            obj._uni_name = request.form["uni_name"]
            obj._foundation_date = request.form["foundation_date"]
        
    # --- LOGICA DE NAVEGAÇÃO ---
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
    
    # --- PREPARAÇÃO SEGURA DAS VARIÁVEIS ---
    if option == 'insert' or not University.lst:
        uni_id = ""
        uni_name = ""
        foundation_date = ""
    else:
        # Garante que a posição atual está dentro dos limites da lista
        if University.pos >= len(University.lst):
            University.pos = 0
            
        code_atual = University.lst[University.pos]
        obj = University.obj[code_atual]
        uni_id = obj.uni_id
        uni_name = obj.uni_name
        foundation_date = obj.foundation_date
        
    return render_template("index.html", 
                           butshow=butshow, 
                           butedit=butedit, 
                           uni_id=uni_id, 
                           uni_name=uni_name, 
                           foundation_date=foundation_date, 
                           ulogin=session.get("user"))

if __name__ == '__main__':
    app.run(debug=True)