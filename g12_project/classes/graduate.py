# -*- coding: utf-8 -*-
"""
@author: Tania Tavares
class Graduate - derivada de Gclass (padrão lição 5)
"""
from .gclass import Gclass


class Graduate(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['_graduate_id', '_university_id', '_observations']
    header = 'Graduates'
    des = ['Graduate ID', 'University ID', 'Observations']

    def __init__(self, graduate_id, university_id, observations):
        super().__init__()
        graduate_id = Graduate.get_id(graduate_id)
        self._graduate_id = graduate_id
        self._university_id = int(university_id)
        self._observations = observations
        Graduate.obj[graduate_id] = self
        Graduate.lst.append(graduate_id)

    @property
    def graduate_id(self):
        return self._graduate_id

    @graduate_id.setter
    def graduate_id(self, v):
        self._graduate_id = v

    @property
    def university_id(self):
        return self._university_id

    @university_id.setter
    def university_id(self, v):
        self._university_id = v

    @property
    def observations(self):
        return self._observations

    @observations.setter
    def observations(self, v):
        self._observations = v
