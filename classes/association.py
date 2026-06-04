# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 17:07:56 2026

@author: Maria
"""
from .gclass import Gclass


class Association(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ""
    att = ["_association_id", "_designation", "_objective"]
    des = ["Association ID", "Designation", "Objective"]

    def __init__(self, association_id, designation, objective):
        super().__init__()
        self._association_id = int(association_id)
        self._designation = designation
        self._objective = objective

        Association.obj[self._association_id] = self
        if self._association_id not in Association.lst:
            Association.lst.append(self._association_id)

    @property
    def association_id(self):
        return self._association_id

    @property
    def designation(self):
        return self._designation

    @property
    def objective(self):
        return self._objective

    def __str__(self):
        return (f"Association(ID: {self._association_id}, "
                f"Designation: {self._designation}, "
                f"Objective: {self._objective})")
