# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 12:02:29 2026

@author: vasco

Programa de teste das classes (ponto 7).
"""
import os

from classes.university import University
from classes.graduate import Graduate
from classes.association import Association
from classes.membership import Membership


# Caminho da BD resolvido a partir da localização deste ficheiro,
# independentemente do diretório a partir do qual o programa é executado.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "universidades_alumni.db")


def main():
    db = DB_PATH

    print("--- 1. Lendo Base de Dados ---")
    try:
        University.read(db)
        Graduate.read(db)
        Association.read(db)
        Membership.read(db)
    except Exception as e:
        print(f"ERRO durante a leitura: {e}")
        return

    print(f"Dados em memória: {len(University.lst)} Universidades, "
          f"{len(Graduate.lst)} Graduados, "
          f"{len(Association.lst)} Associações, "
          f"{len(Membership.lst)} Memberships.")

    if len(Membership.lst) == 0:
        print("\n--- 2. Lista de Associações ---")
        print("Aviso: A lista de Membership está vazia. Não há nada para navegar.")
    else:
        print("\n--- 2. Lista de Memberships (Navegação) ---")
        m = Membership.first()
        count = 0
        while m and count < 5:
            print(f"Registo {count+1}: Uni ID: {m.university_id} | "
                  f"Assoc ID: {m.association_id}")
            m = Membership.nextrec()
            count += 1

    print("\n--- 3. Teste de Ordenação ---")
    if len(University.lst) > 0:
        # Ordenar por nome (alfabético)
        University.sort("uni_name")
        u = University.first()
        print(f"Primeira universidade (A-Z): {u.uni_name}")

        # Ordenar por data de fundação (cronológico, não alfabético)
        University.sort("foundation_date")
        u = University.first()
        print(f"Universidade mais antiga: {u.uni_name} ({u.foundation_date})")
        u = University.last()
        print(f"Universidade mais recente: {u.uni_name} ({u.foundation_date})")
    else:
        print("Aviso: Nenhuma universidade carregada para ordenar.")

    print("\n--- 4. Teste de Pesquisa (find) ---")
    if len(Graduate.lst) > 0:
        primeiro = Graduate.first()
        encontrados = Graduate.find(primeiro.university_id, "university_id")
        print(f"Graduados da universidade {primeiro.university_id}: "
              f"{len(encontrados)} encontrado(s).")


if __name__ == "__main__":
    main()
