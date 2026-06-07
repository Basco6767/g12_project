# -*- coding: utf-8 -*-
"""
criar_utilizadores.py — cria a tabela Userlogin na base de dados e insere as
contas iniciais. Palavras-passe encriptadas com bcrypt (classe Userlogin).

Correr UMA vez:  python criar_utilizadores.py
"""
import os
import sqlite3

from classes.userlogin import Userlogin

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "universidades_alumni.db")

CONTAS = [
    (1, "root",      "admin", "1234"),
    (2, "vasco",     "users", "vasco123"),
    (3, "sofia",     "users", "sofia123"),
    (4, "tania",     "users", "tania123"),
    (5, "maria",     "users", "maria123"),
    (6, "rodrigo",   "users", "rodrigo123"),
    (7, "professor", "admin", "professor123"),
]


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS Userlogin")
    cur.execute("""CREATE TABLE Userlogin (
        id INTEGER, user TEXT, usergroup TEXT, password TEXT, PRIMARY KEY(id)
    )""")
    for id_, user, usergroup, password in CONTAS:
        cur.execute(
            "INSERT INTO Userlogin (id, user, usergroup, password) VALUES (?,?,?,?)",
            (id_, user, usergroup, Userlogin.set_password(password))
        )
    conn.commit()
    conn.close()
    print("Tabela Userlogin criada/atualizada com", len(CONTAS), "contas.")


if __name__ == "__main__":
    main()
