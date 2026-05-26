# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 17:08:07 2026

@author: vasco
"""
import sqlite3
from gclass import Gclass


class Membership(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''

    att = ['_university_id', '_association_id', '_registration_date', '_fee']
    des = ['University ID', 'Association ID', 'Registration Date', 'Fee']

    def __init__(self, university_id, association_id, registration_date, fee):
        super().__init__()
        self._university_id = university_id
        self._association_id = association_id
        self._registration_date = registration_date
        self._fee = fee

        code = f"{self._university_id}_{self._association_id}"

        if code not in Membership.obj:
            Membership.obj[code] = self
            Membership.lst.append(code)

    @property
    def university_id(self):
        return self._university_id

    @property
    def association_id(self):
        return self._association_id

    @property
    def registration_date(self):
        return self._registration_date

    @property
    def fee(self):
        return self._fee

    @classmethod
    def remove(cls, code):
        """
        Override do remove para suportar chave composta
        (university_id, association_id). O código tem o formato '{uni}_{assoc}'.
        """
        if code not in cls.obj:
            return False

        del cls.obj[code]
        cls.lst.remove(code)

        try:
            uni_id_str, assoc_id_str = code.split('_', 1)
            uni_id = int(uni_id_str)
            assoc_id = int(assoc_id_str)
        except (ValueError, AttributeError) as e:
            print(f"Erro a interpretar a chave '{code}': {e}")
            return False

        conn = None
        try:
            conn = sqlite3.connect(cls.db_name)
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM Membership "
                "WHERE university_id = ? AND association_id = ?",
                (uni_id, assoc_id)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao remover Membership na base de dados: {e}")
            return False
        finally:
            if conn is not None:
                conn.close()

    def __str__(self):
        return (f"Membership(Uni: {self._university_id}, "
                f"Assoc: {self._association_id}, "
                f"Date: {self._registration_date}, "
                f"Fee: {self._fee})")