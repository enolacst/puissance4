#!/usr/bin/python3
# -*- coding: utf-8 -*-
#

__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__date__ = "19.02.21"
__usage__ = "Project 2021: tests jalon 02: MinMax"

import os
import unittest
from unittest.mock import patch
from  tools import checkTools as chk
from zec_01 import Board as c4

def mock_prn(*args, **kargs):
    """ no output allowed """
    pass

class TestKlass(unittest.TestCase):
    """ Is 'MinMax' correctly setup """
    def test_sub(self):
        """ MinMax is a Player """
        klass = "MinMax"
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
        klass = "MinMax"
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
        

class TestOneStep(unittest.TestCase):
    """ do we find the best move """
    def setUp(self):
        klass = "MinMax"
        chk.check_class(tp, klass)
        self.jeu = c4(p=3, cylinder=True)
        self.K = getattr(tp, klass)
        
    @patch('builtins.print')    
    def test_attak(self, mock_prn):
        """ find the winning play at depth 1..4 """
        pfl = range(1, 5)
        _rep = []
        for pf in pfl:
            self.o = self.K('bidon', self.jeu, pf=pf)
            self.o.who_am_i = 'J'
            self.jeu.reset()
            for _ in range(2):
                self.jeu.move('D') ; self.jeu.move('E')
            _rep.append(self.o.decision(self.jeu.state))
        _val = [_rep[0] == x for x in _rep ]
        self.assertTrue(all(_val),
                        "expected the same answer {}".format(_rep[0]))
        self.assertEqual(_rep[0], 'D',
                         "expected 'D', found {}".format(0))

    @patch('builtins.print')    
    def test_defence(self, mock_prn):
        """ find the key play at depth 2..5 """
        pfl = range(2, 6)
        _rep = []
        for pf in pfl:
            self.o = self.K('bidon', self.jeu, pf=pf)
            self.o.who_am_i = 'J'
            self.jeu.reset()
            self.jeu.move('D') ; self.jeu.move('E')
            self.jeu.move('A') ; self.jeu.move('E')
            _rep.append(self.o.decision(self.jeu.state))
        _val = [_rep[0] == x for x in _rep ]
        self.assertTrue(all(_val),
                        "expected the same answer {}".format(_rep[0]))
        self.assertEqual(_rep[0], 'E',
                         "expected 'E', found {}".format(_rep[0]))

    @patch('builtins.print')    
    def test_blind_spot(self, mock_prn):
        """ cant find the right answer at depth 1 """
        self.o = self.K('bidon', self.jeu, pf=1)
        self.o.who_am_i = 'J'
        self.jeu.move('D') ; self.jeu.move('E')
        self.jeu.move('A') ; self.jeu.move('E')
        _val = self.o.decision(self.jeu.state)
        self.assertEqual(_val, 'A',
                         "Expected 'A', found {}".format(_val))
        
        
        
def suite(fname):
    """ permet de récupérer les tests à passer avec l'import dynamique """
    global tp
    klasses = (TestPrivacy, TestKlass, TestOneStep)
    
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
    


