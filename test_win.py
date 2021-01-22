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
        self.o.move('D')
        for i in range(2): self.o.move('A')
        for i in range(2): self.o.move('B')
        self.o.move('D')

        self.assertFalse(self.o.win(), "no win detected")
        self.o.move('B')
        self.assertEqual(self.o.board,
                         (2,2,0,1,
                          1,1,0,2,
                          0,1,0,0,
                          0,0,0,0),
                         "wrong board")
        self.assertTrue(self.o.win(),"Expect a win on diagonal")
        
    
def suite(fname):
    """ permet de récupérer les tests à passer avec l'import dynamique """
    global tp
    klasses = (TestWinIsOver_333, TestWinIsOver_332,
               TestWinNoCylinder, TestWinWithCylinder)
    
    try:
        tp = __import__(fname)
    except Exception as _e:
        print(_e)
    sweet = unittest.TestSuite()
    for klass_t in klasses:
        sweet.addTest(unittest.makeSuite(klass_t))
    return sweet

