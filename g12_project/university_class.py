git config --global user.name "Sofia Abreu Teixeira"
git config --global user.email "up202507000@g.uporto.pt"
"""
Created on Thu Apr  2 17:07:46 2026

@author: Sofia Teixeira
"""
from gclass import Gclass

class University(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['_uni_id', '_uni_name', '_foundation_date']
    des = ["ID", 'University Name', 'Foundation Date']
    path = 'universidades_alumni.db' 

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

        return f"University(ID: {self._uni_id}, Name: {self._uni_name}, Founded: {self._foundation_date})"



  

