# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 19:10:10 2026

@author: vasco
"""

import sqlite3
import csv

def importar_graduados(ficheiro_csv, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    
    with open(ficheiro_csv, mode='r', encoding='latin-1') as f:
     
        reader = csv.reader(f, delimiter=';') 
        
        try:
            header = next(reader)
        except StopIteration:
            print("O ficheiro CSV está vazio!")
            return

        
        cursor.execute("DELETE FROM Graduate")
        
        for i, row in enumerate(reader):
          
            if len(row) >= 3:
                cursor.execute("""
                    INSERT OR IGNORE INTO Graduate (graduate_id, university_id, observations)
                    VALUES (?, ?, ?)
                """, (row[8], row[1], row[9]))

            else:
                print(f"Aviso: Linha {i+2} ignorada por falta de colunas: {row}")

    conn.commit()
    conn.close()
    print("Importação concluída com sucesso e tabela limpa!")


importar_graduados('g12_Universities_Alumni.csv', 'universidades_alumni.db')