# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 17:09:19 2026

@author: Tania Tavares
"""
from gclass import Gclass


class Graduate(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    # Convenção uniforme com prefixo _ como nas restantes classes
    att = ['_graduate_id', '_university_id', '_observations']
    des = ['Graduate ID', 'University ID', 'Observations']

    def __init__(self, graduate_id, university_id, observations):
        super().__init__()
        self._graduate_id = graduate_id
        self._university_id = university_id
        self._observations = observations

        if self._graduate_id not in Graduate.obj:
            Graduate.obj[self._graduate_id] = self
            Graduate.lst.append(self._graduate_id)

    @property
    def graduate_id(self):
        return self._graduate_id

    @property
    def university_id(self):
        return self._university_id

    @property
    def observations(self):
        return self._observations

    def __str__(self):
        return (f"Graduate(ID: {self._graduate_id}, "
                f"Univ ID: {self._university_id}, "
                f"Obs: {self._observations})")