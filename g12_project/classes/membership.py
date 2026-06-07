# -*- coding: utf-8 -*-
"""
@author: vasco
class Membership - derivada de Gclass (padrão lição 5).

Caso especial: a tabela Membership tem CHAVE PRIMÁRIA COMPOSTA
(university_id, association_id), que a Gclass genérica não cobre.
Por isso esta classe:
 - usa um identificador interno '_code' = "uni_assoc" como att[0]
   (para as estruturas obj/lst/navegação da Gclass funcionarem);
 - faz override de insert/update/remove para usarem a chave composta real
   na base de dados.
"""
import datetime
from .gclass import Gclass


class Membership(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['_code', '_university_id', '_association_id',
           '_registration_date', '_fee']
    header = 'Memberships'
    des = ['Code', 'University ID', 'Association ID', 'Registration Date', 'Fee']

    def __init__(self, university_id, association_id, registration_date, fee):
        super().__init__()
        self._university_id = int(university_id)
        self._association_id = int(association_id)
        self._registration_date = datetime.date.fromisoformat(registration_date)
        self._fee = float(fee)
        self._code = f"{self._university_id}_{self._association_id}"
        Membership.obj[self._code] = self
        Membership.lst.append(self._code)

    @property
    def code(self):
        return self._code

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

    # --- Overrides para chave composta (a tabela não tem coluna 'code') ---
    @classmethod
    def insert(cls, p):
        obj = cls.obj[p]
        command = (
            f'INSERT INTO {cls.__name__} '
            f'(university_id, association_id, registration_date, fee) VALUES('
            f'{obj._university_id},{obj._association_id},'
            f'"{obj._registration_date}",{obj._fee})'
        )
        cls.sqlexe(command)

    @classmethod
    def update(cls, p):
        obj = cls.obj[p]
        command = (
            f'UPDATE "{cls.__name__}" SET '
            f'registration_date = "{obj._registration_date}", fee = {obj._fee} '
            f'WHERE university_id = {obj._university_id} '
            f'AND association_id = {obj._association_id}'
        )
        cls.sqlexe(command)

    @classmethod
    def remove(cls, p):
        obj = cls.obj[p]
        command = (
            f'DELETE FROM {cls.__name__} '
            f'WHERE university_id = {obj._university_id} '
            f'AND association_id = {obj._association_id}'
        )
        cls.sqlexe(command)
        cls.lst.remove(p)
        del cls.obj[p]
