# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 17:09:55 2026

@author: vasco

Classe Genérica (Gclass) Padrão
"""
import sqlite3
from datetime import datetime


class Gclass:
    # NOTA: estes atributos são apenas defaults/contrato. Cada subclasse
    # DEVE redefinir os seus próprios obj/lst/att para não partilhar estado.
    obj = dict()
    lst = list()
    pos = 0
    att = []
    db_name = None

    def __init__(self):
        pass

    @classmethod
    def read(cls, database):
        """Lê os dados da base de dados e popula as estruturas internas."""
        cls.db_name = database
        cls.obj.clear()
        cls.lst.clear()

        conn = None
        try:
            conn = sqlite3.connect(cls.db_name)
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {cls.__name__}")
            rows = cursor.fetchall()
            for row in rows:
                cls(*row)
            return True
        except sqlite3.Error as e:
            print(f"Erro ao ler a tabela '{cls.__name__}': {e}")
            return False
        finally:
            if conn is not None:
                conn.close()

    @classmethod
    def remove(cls, code):
        """
        Remove o registo da memória e da base de dados.
        Suporta apenas PK simples. Classes com chave composta
        (ex: Membership) devem fazer override deste método.
        """
        if code not in cls.obj:
            return False

        del cls.obj[code]
        cls.lst.remove(code)

        conn = None
        try:
            conn = sqlite3.connect(cls.db_name)
            cursor = conn.cursor()

            pk_column = cls.att[0]
            if pk_column.startswith('_'):
                pk_column = pk_column[1:]

            cursor.execute(
                f"DELETE FROM {cls.__name__} WHERE {pk_column} = ?",
                (code,)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao remover na base de dados: {e}")
            return False
        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def _parse_date(value):
        """Tenta converter uma string para datetime para ordenação cronológica.
        Aceita os formatos d/m/yyyy e dd/mm/yyyy. Se falhar, devolve datetime.min
        para que o valor fique no início da ordenação ascendente."""
        if not isinstance(value, str):
            return value
        for fmt in ("%d/%m/%Y", "%d/%m/%y"):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        return datetime.min

    @classmethod
    def sort(cls, attrib, reverse=False, as_date=False):
        """Ordena a lista baseada num atributo.
        Use as_date=True para ordenar strings de datas cronologicamente."""
        if not cls.lst:
            return

        exemplo_obj = cls.obj[cls.lst[0]]
        real_attrib = attrib if hasattr(exemplo_obj, attrib) else f"_{attrib}"

        if as_date:
            key_func = lambda code: cls._parse_date(getattr(cls.obj[code], real_attrib))
        else:
            key_func = lambda code: getattr(cls.obj[code], real_attrib)

        cls.lst.sort(key=key_func, reverse=reverse)

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
        """Devolve o elemento anterior, ou None se já estiver no início."""
        if cls.pos > 0:
            cls.pos -= 1
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
        if not cls.lst:
            return []
        real_attrib = attrib if hasattr(cls.obj[cls.lst[0]], attrib) else f"_{attrib}"
        return [cls.obj[code] for code in cls.lst
                if getattr(cls.obj[code], real_attrib) == value]

    def get_id(self):
        pk_attrib = self.__class__.att[0]
        return getattr(self, pk_attrib)
