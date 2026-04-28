# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 17:09:55 2026

@author: vasco
"""

"""
Classe Genérica (Gclass) Padrão
"""
import sqlite3

class Gclass:

    def __init__(self):
        pass

    @classmethod
    def read(cls, database):
        """Lê os dados da base de dados e popula as estruturas internas."""
        cls.db_name = database
        cls.obj.clear()
        cls.lst.clear()

        try:
            conn = sqlite3.connect(cls.db_name)
            cursor = conn.cursor()

            cursor.execute(f"SELECT * FROM {cls.__name__}")
            rows = cursor.fetchall()

            for row in rows:
                cls(*row)

        except sqlite3.Error as e:
            print(f"Erro ao ler a tabela '{cls.__name__}': {e}")
        finally:
            if 'conn' in locals():
                conn.close()

    @classmethod
    def remove(cls, code):
        """Remove o registo pelas chaves na memória e na base de dados."""
        if code in cls.obj:
            del cls.obj[code]
            cls.lst.remove(code)

            try:
                conn = sqlite3.connect(cls.db_name)
                cursor = conn.cursor()
                
           
                pk_column = cls.att[0] 
                if pk_column.startswith('_'):
                    pk_column = pk_column[1:]
                
                cursor.execute(f"DELETE FROM {cls.__name__} WHERE {pk_column} = ?", (code,))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Erro ao remover na base de dados: {e}")
            finally:
                if 'conn' in locals():
                    conn.close()

    @classmethod
    def sort(cls, attrib, reverse=False):
        """Ordena a lista baseada num atributo."""
        if not cls.lst:
            return 
    
   
        exemplo_obj = cls.obj[cls.lst[0]]
        real_attrib = attrib if hasattr(exemplo_obj, attrib) else f"_{attrib}"
        
        
        cls.lst.sort(key=lambda code: getattr(cls.obj[code], real_attrib), reverse=reverse)

    @classmethod
    def current(cls, code):
        if code in cls.lst:
            cls.pos = cls.lst.index(code)
            return cls.obj[code]
        return None

    @classmethod
    def first(cls):
        if cls.lst:
            cls.pos = 0
            return cls.obj[cls.lst[cls.pos]]
        return None

    @classmethod
    def next(cls):
        if cls.pos < len(cls.lst) - 1:
            cls.pos += 1
            return cls.obj[cls.lst[cls.pos]]
        return None  

    @classmethod
    def previous(cls):
        if cls.pos > 0:
            cls.pos -= 1
        if cls.lst:
            return cls.obj[cls.lst[cls.pos]]
        return None

    @classmethod
    def last(cls):
        if cls.lst:
            cls.pos = len(cls.lst) - 1
            return cls.obj[cls.lst[cls.pos]]
        return None
    
    @classmethod
    def find(cls, value, attrib):
        real_attrib = attrib if hasattr(cls.obj[cls.lst[0]], attrib) else f"_{attrib}"
        return [cls.obj[code] for code in cls.lst if getattr(cls.obj[code], real_attrib) == value]
    
    def get_id(self):
   
        pk_attrib = self.__class__.att[0] 
        return getattr(self, pk_attrib)