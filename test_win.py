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

class TestStateSetterWin(unittest.TestCase):
    """ uploading a state where there is a win situation """
    
def suite(fname):
    """ permet de récupérer les tests à passer avec l'import dynamique """
    global tp
    klasses = (TestWinIsOver_333, TestWinIsOver_332, TestStateSetterWin,)
    
    try:
        tp = __import__(fname)
    except Exception as _e:
        print(_e)
    sweet = unittest.TestSuite()
    for klass_t in klasses:
        sweet.addTest(unittest.makeSuite(klass_t))
    return sweet

