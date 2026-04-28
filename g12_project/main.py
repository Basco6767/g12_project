# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 12:02:29 2026

@author: vasco
"""

from classes.university import University
from classes.graduate import Graduate
from classes.association import Association
from classes.membership import Membership

def main():
    db = "data/universidades_alumni.db"

    print("--- 1. Lendo Base de Dados ---")
    try:
        University.read(db)
        Graduate.read(db)
        Association.read(db)
        Membership.read(db)
    except Exception as e:
        print(f"ERRO durante a leitura: {e}")
        return
    
    print(f"Dados em memória: {len(University.lst)} Universidades, {len(Graduate.lst)} Graduados.")

    if len(Membership.lst) == 0:
        print("\n--- 2. Lista de Associações ---")
        print("Aviso: A lista de Membership está vazia. Não há nada para navegar.")
    else:
        print("\n--- 2. Lista de Associações (Navegação) ---")
        m = Membership.first()
        count = 0
        while m and count < 5:

            u_id = getattr(m, '_university_id', 'N/A')
            a_id = getattr(m, '_association_id', 'N/A')
            print(f"Registo {count+1}: Uni ID: {u_id} | Assoc ID: {a_id}")
            m = Membership.next()
            count += 1

    print("\n--- 3. Teste de Ordenação ---")
    if len(University.lst) > 0:
       
        University.sort("uni_name") 
        u = University.first()
        
       
        nome = u.uni_name
        print(f"Primeira universidade (A-Z): {nome}")
    else:
        print("Aviso: Nenhuma universidade carregada para ordenar.")

if __name__ == "__main__":
    main()
    
