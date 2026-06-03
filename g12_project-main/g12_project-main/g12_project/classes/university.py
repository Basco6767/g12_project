# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 17:07:46 2026

@author: Sofia Abreu Teixeira
"""
from .gclass import Gclass


class University(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['_uni_id', '_uni_name', '_foundation_date']
    des = ["ID", 'University Name', 'Foundation Date']

    def __init__(self, uni_id, uni_name, foundation_date):
        super().__init__()

        self._uni_id = uni_id
        self._uni_name = uni_name
        self._foundation_date = foundation_date

        University.obj[self._uni_id] = self
        if self._uni_id not in University.lst:
            University.lst.append(self._uni_id)

    @property
    def uni_id(self):
        return self._uni_id

    @property
    def uni_name(self):
        return self._uni_name

    @property
    def foundation_date(self):
        return self._foundation_date

    def __str__(self):
        return (f"University(ID: {self._uni_id}, "
                f"Name: {self._uni_name}, "
                f"Founded: {self._foundation_date})")
