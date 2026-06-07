# -*- coding: utf-8 -*-
"""Pacote com as classes do modelo conceptual."""
from .gclass import Gclass
from .university import University
from .graduate import Graduate
from .association import Association
from .membership import Membership
from .userlogin import Userlogin

__all__ = ["Gclass", "University", "Graduate", "Association", "Membership", "Userlogin"]
