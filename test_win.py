#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__date__ = "09.01.21"
__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__usage__="""
axioms for end game detection
"""

import os
import unittest
import random
from  tools import checkTools as chk

def shift(mot:str, alphabet:str,k:int) -> str:
    """ un mot actions
        un alphabet (les colonnes)
        un décalage (k>0 à droite, k<0 à gauche)
        @return le mot décalé
    """
    _sz = len(alphabet)
    return ''.join([alphabet[(alphabet.index(x)+k)%_sz]
                    for x in mot])

class TestWinIsOver_333(unittest.TestCase):
    """ win set over """
    def setUp(self):
        self.K = getattr(tp, 'Board')
        self.o = self.K(3, 3, 3)

    def test_win_set_over(self):
        """
           board (1, 2, 0, 2, 1, 0, 1, 2, 0)
        """
        for i in range(3): self.o.move('A') # JRJ
        for i in range(3): self.o.move('B') # RJR
        self.assertEqual(self.o.board,
                         (1, 2, 0, 2, 1, 0, 1, 2, 0), "board is wrong")
        self.o.move('C')
        self.assertTrue(self.o.win(), "Expected a win")
        self.assertTrue(self.o.over(), "Expected game over")
        self.assertEqual(self.o.actions, (), "No action left")

    def test_nowin(self):
        """
          a simple test for a no win
        """
        _actions = "BABBCC"
        for a in _actions: self.o.move(a)
        self.assertEqual(self.o.board,
                         (2,1,1,0,1,2,0,2,0),
                         "board is wrong")
        self.assertFalse(self.o.win(), "This is not a win")
        self.assertFalse(self.o.over(), "This is not a end game")
        
        
class TestWinIsOver_332(unittest.TestCase):
    """ win set over """
    def setUp(self):
        self.K = getattr(tp, 'Board')
        self.o = self.K(3, 3, 2)

    def test_win_2(self):
        """
            board (0, 1, 0, 0, 2, 0, 0, 0, 0)
        """
        for i in range(2): self.o.move('B')
        self.assertEqual(self.o.board,
                         (0, 1, 0, 0, 2, 0, 0, 0, 0), "board is wrong")
        for a in self.o.actions:
            with self.subTest(choice=a):
                self.o.move(a)
                if a != 'B':
                    self.assertTrue(self.o.win(), "Expected a win")
                    self.assertTrue(self.o.over(), "Expected game over")
                    self.assertEqual(self.o.actions, (), "No action left")
                else:
                    self.assertFalse(self.o.win(), "Expected no win")
                    self.assertFalse(self.o.over(), "Expected no game over")
                    self.assertNotEqual(self.o.actions, (), "actions expected")
                    
                self.o.undo()
                    
    def test_win_3(self):
        """
           board (0, 1, 0, 0, 2, 0, 0, 1, 0)
        """
        self.assertEqual(self.o.board.count(0), 9, "board is not safe")
        for i in range(3): self.o.move('B') # JRJ
        self.assertEqual(self.o.board,
                         (0, 1, 0, 0, 2, 0, 0, 1, 0), "board is wrong")
        
        for a in self.o.actions:
            with self.subTest(choice=a):
                self.o.move(a)
                self.assertTrue(self.o.win(), "Expected a win")
                self.assertTrue(self.o.over(), "Expected game over")
                self.assertEqual(self.o.actions, (), "No action left")
                self.o.undo()

class TestWinNoCylinder(unittest.TestCase):
    """ uploading a state where there is a win situation 
        and board is flat
    """
    def setUp(self):
        self.K = getattr(tp, 'Board')
        self.o = self.K(3, 3, 3)

    def test_line(self):
        """ win on a line """
        for i in range(2): self.o.move('A')
        for i in range(2): self.o.move('B')
        self.assertFalse(self.o.win(), "no win detected")
        self.o.move('C')
        self.assertEqual(self.o.board, (1,1,1,2,2,0,0,0,0),
                         "wrong board")
        self.assertTrue(self.o.win(),"Expect a win bottom row")

    def test_column(self):
        """ win on a column """
        for i in range(2):
            self.o.move('A') ; self.o.move('B')

        self.assertFalse(self.o.win(), "no win detected")
        self.o.move('A')
        self.assertEqual(self.o.board, (1,2,0,1,2,0,1,0,0),
                         "wrong board")
        self.assertTrue(self.o.win(),"Expect a win column 'A'")

    def test_diagonal(self):
        """ win on a diagonal """
        self.o.move('A') ; self.o.move('B') ; self.o.move('B')
        self.o.move('C') ; self.o.move('C') ; self.o.move('A')

        self.assertFalse(self.o.win(), "no win detected")
        self.o.move('C')
        self.assertEqual(self.o.board, (1,2,2,2,1,1,0,0,1),
                         "wrong board")
        self.assertTrue(self.o.win(),"Expect a win on diagonal")
        
class TestWinWithCylinder(unittest.TestCase):
    """ uploading a state where there is a win situation 
        and board is a cylinder
    """
    def setUp(self):
        self.K = getattr(tp, 'Board')
        self.o = self.K(4, 4, 3, True)

    def test_line(self):
        """ win on 1st line """
        for i in range(2): self.o.move('A')
        for i in range(2): self.o.move('B')
        self.assertFalse(self.o.win(), "no win detected")
        self.o.move('D')
        self.assertEqual(self.o.board, (1,1,0,1,
                                        2,2,0,0,
                                        0,0,0,0,
                                        0,0,0,0),
                         "wrong board")
        self.assertTrue(self.o.win(),"Expect a win bottom row")

    def test_diagonal1(self):
        """ win on a diagonal """
        for i in range(3): self.o.move('A')
        for i in range(3): self.o.move('D')

        self.assertFalse(self.o.win(), "no win detected")
        self.o.move('C')
        self.assertEqual(self.o.board,
                         (1,0,1,2,
                          2,0,0,1,
                          1,0,0,2,
                          0,0,0,0),
                         "wrong board")
        self.assertTrue(self.o.win(),"Expect a win on diagonal")

    def test_diagonal2(self):
        """ win on a diagonal """
        for i in range(3): self.o.move('D')
        for i in range(3): self.o.move('A')
        self.assertFalse(self.o.win(), "no win detected")
        self.o.move('B')
        self.assertTrue(self.o.win(),"Expect a win on diagonal")
        

class TestBoard_554(unittest.TestCase):
    def setUp(self):
        self.K = getattr(tp, 'Board')
        self.o = self.K(5,5,4)
        self.oc = self.K(5,5,4,True)
        self.alf = "ABCDE"
        self.m = ("DCCBABBAEAA", "BCCDEDDEAEE",
                  "AB"*3+"A", "AB"*3+"CB",
                  "AABBCCE", "AABBCCCECE")
        self.sol = (True, True, True, True, False, False)
            
    def test_win_fixed(self):
        "6 subtests on a fixed board"
        for m,s in zip(self.m,self.sol):
            self.o.reset()
            with self.subTest(mot=m):
                for x in m: self.o.move(x)
                self.assertEqual(self.o.win(), s,
                                 "expected win=={}".format(s))

    def test_win_fixed_shift_right(self):
        "6 subtests on a fixed board move +1"
        _sol = (True, False, True, True, True, True)
        for m,s in zip(self.m,_sol):
            _m = shift(m,self.alf, +1)
            self.o.reset()
            with self.subTest(mot=_m):
                for x in _m: self.o.move(x)
                self.assertEqual(self.o.win(), s,
                                 "expected win=={}".format(s))

    def test_win_fixed_shift_left(self):
        "6 subtests on a fixed board move -1"
        _sol = (False, True, True, True, False, False)
        for m,s in zip(self.m,_sol):
            _m = shift(m,self.alf, -1)
            self.o.reset()
            with self.subTest(mot=_m):
                for x in _m: self.o.move(x)
                self.assertEqual(self.o.win(), s,
                                 "expected win=={}".format(s))

    def test_win_cylinder(self):
        "6 subtests on a cylinder board"
        for m in self.m:
            self.oc.reset()
            with self.subTest(mot=m):
                for x in m: self.oc.move(x)
                self.assertTrue(self.oc.win(), "expected win")

    def test_win_cylinder_shift_right(self):
        "6 subtests on a cylinder board shift +1"
        for m in self.m:
            _m = shift(m,self.alf, +1)
            self.oc.reset()
            with self.subTest(mot=_m):
                for x in _m: self.oc.move(x)
                self.assertTrue(self.oc.win(), "expected win")

    def test_win_cylinder_shift_left(self):
        "6 subtests on a cylinder board shift -1"
        for m in self.m:
            _m = shift(m,self.alf, -1)
            self.oc.reset()
            with self.subTest(mot=_m):
                for x in _m: self.oc.move(x)
                self.assertTrue(self.oc.win(), "expected win")

                
class TestBoard_P4(unittest.TestCase):
    def setUp(self):
        self.K = getattr(tp, 'Board')
        self.o = self.K()
        self.oc = self.K(cylinder=True)
        self.alf = "ABCDEFG"
        self.m = ("CDDCDDECEBFAFB",
                  "DCCDCCBDBEAFAE")

    def test_win_red_fixed(self):
        """ Red has a win """
        for mot in self.m:
            with self.subTest(mot=mot):
                self.o.reset()
                _0 = len(mot)
                for x in mot: self.o.move(x)
                self.assertEqual(self.o.timer, _0,
                                "wrong timer expect {} found {}"
                                "".format(_0, self.o.timer))
                self.assertTrue(self.o.win(), "expected a win for 'R'")

    def test_nowin_shift_fixed(self):
        """ Shifting a win is no win """
        _s = (-2, 2)
        for _mot,_shift in zip(self.m, _s):
            mot = shift(_mot, self.alf, _shift)
            with self.subTest(mot=mot):
                self.o.reset()
                _0 = len(mot)
                for x in mot: self.o.move(x)
                self.assertEqual(self.o.timer, _0,
                                "wrong timer expect {} found {}"
                                "".format(_0, self.o.timer))
                self.assertFalse(self.o.win(), "Not expecting a win for 'R'")
                
    def test_win_red_cylinder(self):
        """ Red has a win """
        for mot in self.m:
            with self.subTest(mot=mot):
                self.oc.reset()
                _0 = len(mot)
                for x in mot: self.oc.move(x)
                self.assertEqual(self.oc.timer, _0,
                                "wrong timer expect {} found {}"
                                "".format(_0, self.oc.timer))
                self.assertTrue(self.oc.win(), "expected a win for 'R'")

    def test_win_shift_cylinder(self):
        """ Shifting a win is still a win """
        _s = (-2, 2)
        for _mot,_shift in zip(self.m, _s):
            mot = shift(_mot, self.alf, _shift)
            with self.subTest(mot=mot):
                self.oc.reset()
                _0 = len(mot)
                for x in mot: self.oc.move(x)
                self.assertEqual(self.oc.timer, _0,
                                "wrong timer expect {} found {}"
                                "".format(_0, self.oc.timer))
                self.assertTrue(self.oc.win(), "Expecting a win for 'R'")
                
def suite(fname):
    """ permet de récupérer les tests à passer avec l'import dynamique """
    global tp
    klasses = (TestWinIsOver_333, TestWinIsOver_332,
               TestWinNoCylinder, TestWinWithCylinder,
               TestBoard_554, TestBoard_P4)
    
    try:
        tp = __import__(fname)
    except Exception as _e:
        print(_e)
    sweet = unittest.TestSuite()
    for klass_t in klasses:
        sweet.addTest(unittest.makeSuite(klass_t))
    return sweet

