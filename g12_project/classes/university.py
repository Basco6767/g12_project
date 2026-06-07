# -*- coding: utf-8 -*-
"""
@author: Sofia Abreu Teixeira
class University - derivada de Gclass (padrão lição 5)
"""
import datetime
from .gclass import Gclass


class University(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['_uni_id', '_uni_name', '_foundation_date']
    header = 'Universities'
    des = ['ID', 'University Name', 'Foundation Date']

    def __init__(self, uni_id, uni_name, foundation_date):
        super().__init__()
        uni_id = University.get_id(uni_id)
        self._uni_id = uni_id
        self._uni_name = uni_name
        self._foundation_date = datetime.date.fromisoformat(foundation_date)
        University.obj[uni_id] = self
        University.lst.append(uni_id)

    @property
    def uni_id(self):
        return self._uni_id

    @uni_id.setter
    def uni_id(self, v):
        self._uni_id = v

    @property
    def uni_name(self):
        return self._uni_name

    @uni_name.setter
    def uni_name(self, v):
        self._uni_name = v

    @property
    def foundation_date(self):
        return self._foundation_date

    @foundation_date.setter
    def foundation_date(self, v):
        self._foundation_date = v
