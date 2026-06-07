# -*- coding: utf-8 -*-
"""
@author: Maria
class Association - derivada de Gclass (padrão lição 5)
"""
from .gclass import Gclass


class Association(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['_association_id', '_designation', '_objective']
    header = 'Associations'
    des = ['Association ID', 'Designation', 'Objective']

    def __init__(self, association_id, designation, objective):
        super().__init__()
        association_id = Association.get_id(association_id)
        self._association_id = association_id
        self._designation = designation
        self._objective = objective
        Association.obj[association_id] = self
        Association.lst.append(association_id)

    @property
    def association_id(self):
        return self._association_id

    @association_id.setter
    def association_id(self, v):
        self._association_id = v

    @property
    def designation(self):
        return self._designation

    @designation.setter
    def designation(self, v):
        self._designation = v

    @property
    def objective(self):
        return self._objective

    @objective.setter
    def objective(self, v):
        self._objective = v
