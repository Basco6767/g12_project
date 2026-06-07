# -*- coding: utf-8 -*-
"""
@author: Maria
class Association - derivada de Gclass (padrão lição 5)
"""
from .gclass import Gclass

class Association(Gclass):

    # atributos de classe partilhados por todos os objetos Association
    # obj mapeia cada ID ao objeto, lst guarda a ordem de navegação
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    # att tem os nomes internos dos atributos — usados pela Gclass para gerar SQL automaticamente
    att = ['_association_id', '_designation', '_objective']
    header = 'Associations'
    # des tem os nomes legíveis para mostrar na interface
    des = ['Association ID', 'Designation', 'Objective']

    def __init__(self, association_id, designation, objective):
        super().__init__()
        # se o ID for 0, calcula automaticamente o próximo disponível
        association_id = Association.get_id(association_id)
        self._association_id = association_id
        self._designation = designation
        self._objective = objective
        # regista o objeto no dicionário e acrescenta o ID à lista de navegação
        Association.obj[association_id] = self
        Association.lst.append(association_id)

    # properties e setters para cada atributo — os setters são necessários para o update da Gclass funcionar
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
    @objective.setter
    def objective(self, v):
        self._objective = v
