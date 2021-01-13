#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__date__ = "09.01.21"
__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__usage__="""
axioms for connect 4

b = Board(n,m,p)
n > 2 ; m > 2 ; p>=2 et p <= min(n,m)
b.timer == len(b.state)
1st b.turn == J
b.board[x] != 0 iff x in b.state
move -> state/timer/turn
undo -> state/timer/turn
undo(move) = old
b.reset() -> restart

state modifier iff feasible
over()
win() <- cant be tested since always False
"""


import os
import unittest
import random
from  tools import checkTools as chk

class TestDefault(unittest.TestCase):
    """ control basic information """
    def setUp(self):
        self.K = getattr(tp, "Board")
        self.o = self.K()

    def subtest_init(self):
        """ attributes state, timer, board, actions
            methods over(), win()
        """
        self.assertEqual(len(self.o.state), 0, "wrong history")
        self.assertEqual(len(self.o.state), self.o.timer,
                         "timer trouble")
        self.assertEqual(len(self.o.actions), self.o.nbc,
                         "wrong number of actions")
        self.assertEqual(self.o.board.count(0), self.o.nbc*self.o.nbl,
                         "wrong board")
        self.assertFalse(self.o.over(), "wrong detection of end game")
        self.assertFalse(self.o.win(), "wrong detection of winner")

    def test_default(self):
        """ test default values """
        self.assertEqual(self.o.nbl, 6, "wrong lines")
        self.assertEqual(self.o.nbc, 7, "wrong columns")
        self.assertEqual(self.o.stones, 4, "wrong alignment")
        self.assertEqual(self.o.cylinder, False, "wrong map")
        self.subtest_init()
        
class TestBuilder(unittest.TestCase):
    """ check default parameter """
    def setUp(self):
        self.K = getattr(tp, "Board")
        self.args = {1: [(2, 3, 4, True), (3,3,3,True)], 
                     2: [(2, 3, 4, False), (3,3,3, False)],
                     3: [(4, 2, 3, True), (4,3,3,True) ],
                     4: [(4, 4, 4, True), (4,4,4, True) ],
                     5: [(4, 4, 4, False), (4,4,4, False)]
                     }

    def subtest_init(self):
        """ attributes state, timer, board, actions
            methods over(), win()
        """
        self.assertEqual(len(self.o.state), 0, "wrong history")
        self.assertEqual(len(self.o.state), self.o.timer,
                         "timer trouble")
        self.assertEqual(len(self.o.actions), self.o.nbc,
                         "wrong number of actions")
        self.assertEqual(self.o.board.count(0), self.o.nbc*self.o.nbl,
                         "wrong board")
        self.assertFalse(self.o.over(), "wrong detection of end game")
        self.assertFalse(self.o.win(), "wrong detection of winner")
                
        
    def test_set_args(self):
        """ control default values """
        for _a in self.args:
            _v = self.args[_a]
            with self.subTest(args=_v[0]):
                self.o = self.K(*_v[0])
                self.assertEqual(self.o.nbl, _v[1][0], "wrong nbl")
                self.assertEqual(self.o.nbc, _v[1][1], "wrong nbc")
                self.assertEqual(self.o.stones, _v[1][2], "wrong stones")
                self.assertEqual(self.o.cylinder, _v[1][3], "wrong cylinder")
                self.subtest_init()
                
class TestActions(unittest.TestCase):
    """ column selection """
    def setUp(self):
        self.K = getattr(tp, "Board")
        self.o = self.K()

    def test_actions(self):
        """ a filled column cant be selected any more """
        _a = self.o.actions[0]
        _area = self.o.nbl * self.o.nbc
        for i in range(self.o.nbl):
            self.o.move(_a)
            self.assertEqual(self.o.board.count(0), _area - (i+1),
                             "bad number of empty places")
        #
        self.assertEqual(self.o.board.count(0), self.o.nbl * (self.o.nbc -1),
                         "a column should be filled")
        _0 = self.o.actions
        self.assertNotIn(_a, _0,
                         "column '{}' shouldnt be in {}".format(_a, _0))

    
class TestMove(unittest.TestCase):
    """ effect of one move """
    def setUp(self):
        self.K = getattr(tp, "Board")
        self.o = self.K()

    def test_allowed_move(self):
        """ what if move is allowed """
        # no winner, no endgame
        _latt = "state timer turn board".split()
        for i in range(2*(self.o.stones-1)):
            _old = self.o.state, self.o.timer, self.o.turn, self.o.board,\
              self.o.opponent
            _a = random.choice(self.o.actions)
            self.o.move(_a) # this should work
            _new = self.o.state, self.o.timer, self.o.turn, self.o.board,\
              self.o.opponent
            for _att, _o, _n in zip(_latt, _old, _new):
                with self.subTest(step=i, attribute=_att):
                    self.assertNotEqual(_o, _n,
                                        "someting odd at step {} for att={}"
                                        "".format(i,_att))
            self.assertEqual(len(_old[0])+1, len(_new[0]), "move missing")
            self.assertEqual(_old[1]+1, _new[1], "move count trouble")
            self.assertEqual(_old[2], _new[4], "wrong old opp")
            self.assertEqual(_new[2], _old[4], "wrong new opp")
            self.assertEqual(_old[3].count(0), _new[3].count(0)+1,
                             "board trouble")
            
    def test_forbidden_move(self):
        """ what if move is not allowed """
        _a = self.o.actions[0] # pick the first column
        for i in range(self.o.nbl):
            self.o.move(_a)
        _latt = "state timer turn board".split()
        _old = self.o.state, self.o.timer, self.o.turn, self.o.board
        self.o.move(_a) # this shouldnt work
        _new = self.o.state, self.o.timer, self.o.turn, self.o.board
        for _att,o,n in zip(_latt, _old, _new):
            with self.subTest(attribute=_att):
                self.assertEqual(o, n,
                                 "something odd with att {}".format(_att))

class TestUndo(unittest.TestCase):
    """ undoing """
    def setUp(self):
        self.K = getattr(tp, "Board")
        self.o = self.K(3,3,3)

    def test_undo(self):
        """ undo a previous action """
        for a in self.o.actions: self.o.move(a) # fill 1st line
        _a = random.choice(self.o.actions)
        _latt = "state timer turn board".split()
        _old = self.o.state, self.o.timer, self.o.turn, self.o.board
        self.o.move(_a)
        _pre = self.o.state, self.o.timer, self.o.turn, self.o.board
        self.o.undo()
        _post = self.o.state, self.o.timer, self.o.turn, self.o.board
        for att, old, pre, post in zip(_latt, _old, _pre, _post):
            with self.subTest(attribute=att):
                self.assertEqual(old, post, "fix undo {}".format(att))
                self.assertNotEqual(old, pre, "fix move {}".format(att))

class TestReset(unittest.TestCase):
    """ reset """
    def setUp(self):
        self.K = getattr(tp, "Board")
        self.o = self.K()

    def test_reset(self):
        """ undo a previous action """
        _nl, _nc, _st = self.o.nbl, self.o.nbc, self.o.stones
        _old = self.o.state, self.o.timer, self.o.turn, self.o.board
        for a in self.o.actions: self.o.move(a) # fill 1st line
        _a = random.choice(self.o.actions)
        _latt = "state timer turn board".split()
        self.o.reset()
        _new = self.o.state, self.o.timer, self.o.turn, self.o.board
        self.assertEqual(_nl, self.o.nbl, "lines")
        self.assertEqual(_nc, self.o.nbc, "columns")
        self.assertEqual(_st, self.o.stones, "stones")
        for a, o, n in zip(_latt, _old, _new):
            with self.subTest(attribute=a):
                self.assertEqual(o, n, "bad '{}' after reset".format(a))

class TestOverFullBoard(unittest.TestCase):
    """ over full board"""
    def setUp(self):
        self.K = getattr(tp, "Board")
        self.o = self.K(3,3,3)
    def test_over_nomove(self):
        """ after nbl*nbc move, over is True """
        for i in range(3):
            self.o.move('B')
            self.o.move("A")
            self.o.move('C')
        self.assertTrue(self.o.over(),"Expect game is over")
        self.assertEqual(len(self.o.actions), 0, "no more action")
        
class TestStateSetter(unittest.TestCase):
    """ uploading a new state is safe 
        the state considered are no winning cases
    """
    def setUp(self):
        self.K = getattr(tp, "Board")
        self.o = self.K(3,3,3)
        self.st = [ (0,1), (1,1), (0,0), (0,2) ]

    def test_state_ok(self):
        """ a valid state can be set """
        self.o.state = self.st
        self.assertTrue(self.o.timer == 4, "expect timer=4")
        self.assertTrue(self.o.state == tuple(self.st),
                         "values {0.o.state} != {0.st}".format(self))
        self.assertEqual(self.o.board,
                         (1, 1, 2, 0, 2, 0, 0, 0, 0),
                         "board is wrong")
        
    def test_line_outofrange(self):
        """ state contains a tuple with line out of range """
        self.st.append( (4,0) )
        self.o.state = self.st
        self.assertTrue(self.o.timer == 0, "timer is wrong")
        self.assertTrue(self.o.state == (), "state is wrong")
        self.assertEqual(self.o.board.count(0), self.o.nbl*self.o.nbc,
                         "board is wrong")

    def test_column_outofrange(self):
        """ state contains a tuple with col out of range """
        self.st.append( (0,4) )
        self.o.state = self.st
        self.assertTrue(self.o.timer == 0, "timer is wrong")
        self.assertTrue(self.o.state == (), "state is wrong")
        self.assertEqual(self.o.board.count(0), self.o.nbl*self.o.nbc,
                         "board is wrong")

    def test_nonconsecutive_line(self):
        """ state contains a tuple with non-consecutive line """
        self.st.append( (2,0) ) # next place in col 0 should be 1
        self.o.state = self.st
        self.assertTrue(self.o.timer == 0, "timer is wrong")
        self.assertTrue(self.o.state == (), "state is wrong")
        self.assertEqual(self.o.board.count(0), self.o.nbl*self.o.nbc,
                         "board is wrong")

    def test_tuple_seen(self):
        """ state contains 2 identical tuples """
        self.st.append( (1,1) ) # already in st
        self.o.state = self.st
        self.assertTrue(self.o.timer == 0, "timer is wrong")
        self.assertTrue(self.o.state == (), "state is wrong")
        self.assertEqual(self.o.board.count(0), self.o.nbl*self.o.nbc,
                         "board is wrong")
        
    
        
def suite(fname):
    """ permet de récupérer les tests à passer avec l'import dynamique """
    global tp
    klasses = (TestDefault, TestBuilder, TestActions,
               TestMove, TestUndo, TestReset,
               TestOverFullBoard, TestStateSetter, )
    
    try:
        tp = __import__(fname)
    except Exception as _e:
        print(_e)
    sweet = unittest.TestSuite()
    for klass_t in klasses:
        sweet.addTest(unittest.makeSuite(klass_t))
    return sweet


