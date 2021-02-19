#!/usr/bin/python3
# -*- coding: utf-8 -*-
#

__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__date__ = "19.02.21"
__usage__ = "Project 2021: tests jalon 02: Randy"

import os
import unittest
from unittest.mock import patch
from  tools import checkTools as chk


class TestKlass(unittest.TestCase):
    """ Is 'Randy' correctly setup """
    def test_sub(self):
        """ Randy is a Player """
        klass = "Randy"
        player = "Player"
        chk.check_class(tp, player)
        chk.check_class(tp, klass)
        self.assertTrue(issubclass(getattr(tp, klass),
                                   getattr(tp, player)),
                        "{} should be a subclass of {}".format(klass, player))
        
class TestPrivacy(unittest.TestCase):
    """ all attributes are provided by 'Player' """
    def test_privacy(self):
        """ one expects only to find 'decision' """
        klass = "Randy"
        player = "Player"
        chk.check_class(tp, player)
        chk.check_class(tp, klass)
        _1 = getattr(tp, klass)
        _2 = _1.__dict__
        _4 = "_{}__".format(_1.__name__)
        _3 = _1.__slots__ if hasattr(_1, '__slots__') else None
        self.assertTrue('decision' in _2,
                        "missing decision")
        _latt_public = [x for x in _2 if not x.startswith((_4, '__'))]
        self.assertEqual(len(_latt_public), 1,
                         "{} public methods are too numerous"
                         "".format(_latt_public))
        _latt_slots = ([] if _3 is None else
                       [x for x in _3  if not x.startswith('__')])
        self.assertEqual(len(_latt_slots), 0,
                         "{} public or protected attributes are forbiden"
                         "".format(_latt_slots))
        

def suite(fname):
    """ permet de récupérer les tests à passer avec l'import dynamique """
    global tp
    klasses = (TestPrivacy, TestKlass,)
    
    try:
        tp = __import__(fname)
    except Exception as _e:
        print(_e)
    sweet = unittest.TestSuite()
    for klass_t in klasses:
        sweet.addTest(unittest.makeSuite(klass_t))
    return sweet

if __name__ == "__main__":
    param = input("quel est le fichier à traiter ? ")
    if not os.path.isfile(param): ValueError("need a python file")

    etudiant = param.split('.')[0]

    _out = chk.check_property(etudiant != '','acces au fichier')
    print("tentative de lecture de {}".format(etudiant))
    tp = __import__(etudiant) # revient à faire import XXX as tp

    unittest.main()
    


