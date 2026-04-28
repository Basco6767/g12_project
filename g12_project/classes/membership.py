# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 17:08:07 2026

@author: vasco
"""



from classes.gclass import Gclass



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

        Membership.obj[code] = self
        if code not in Membership.lst:
            Membership.lst.append(code)

    def __str__(self):
        return f"Membership(Uni: {self._university_id}, Assoc: {self._association_id}, Date: {self._registration_date}, Fee: {self._fee})"
