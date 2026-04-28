# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 17:07:56 2026

@author: Maria
"""
from classes.gclass import Gclass
class Association(Gclass):
  obj=dict()
  lst=list()
  pos=0
  sortkey=""
  att=["_association_id","_objective","_designation"]
  des=["Association ID","Objective","Designation"]
  def __init__(self, association_id, designation, objective):
    super().__init__()
    self._association_id=int(association_id)
    self._objective=objective
    self._designation=designation
    Association.obj[self._association_id]=self
    Association.lst.append(self._association_id)

  @property
  def association_id(self):
    return self._association_id
  @property
  def objective(self):
    return self._objective
  @property
  def designation(self):
    return self._designation
  def __str__(self):
    return f"Association(ID: {self._association_id}, Designation: {self._designation}, Objective: {self._objective})"
