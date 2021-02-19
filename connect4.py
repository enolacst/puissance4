#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__date__ = "08.01.21"
__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__usage__="""
Board(n, m, p, flag)
>>> n nombre de lignes, m nombre de colonnes, p nombre de pierres à aligner
  flag vrai: terrain cylindrique, faux: terrain borné
Puissance 4 est créé par Board() ou par Board(6, 7, 4, False)

attributs read only
> nbl: number of lines
> nbc: number of columns
> stones: number of stones to align
> cylinder: True cylinder board, False: flat board
> timer: number of stones played
> turn: who plays next move
> actions: allowed moves
> board: internal 1D representation
> winner: the winner of the game

attributs read/write
> state: moves' history

methodes
> move(column): modify the attributes state, board, timer, turn
> undo(): undo the last move and refreshes attributes
> reset(): restart all the attributes 
"""

from tools.ezCLI import grid
from tools.outils import c2p
from typing import Iterable

def main():
    print(__usage__)


class Board:
    """ Base class for the connect 4 """
    __slots__ = ('__data', '__color',)
    def __init__(self, nl:int=6, nc:int=7, p:int=4, cylinder:bool=False):
        """
        nl > 2 ; nc > 2 ; p >= 2 et <= min(nl, nc)
        In fact nc is bound by 26 (see actions)
        """
        _nl, _nc = max(3,nl), max(3, nc)
        self.__data = [_nl, _nc,
                       max(2, min(_nl, _nc, p)), bool(cylinder),
                       0,
                       [], 
                       [0 for i in range(_nc)],
                       [0 for i in range(_nl*_nc)]
                       ]
        self.__color = ".JR"

    def __repr__(self) -> str:
        return ("{0}({1.nbl}, {1.nbc}, {1.stones}, {1.cylinder})"
                "".format(self.__class__.__name__, self))

    def __str__(self) -> str:
        """ display the grid """
        _grid = [ [ self.__color[ self.board[c2p((x,y), self.nbc)] ]
                  for y in range(self.nbc)] for x in range(self.nbl)][::-1]
        _msg = "\n"+self.show_msg()
        return grid(_grid, label=True, size=3)+_msg
    
    @property
    def nbl(self) -> int:
        """ getter: number of lines """
        return self.__data[0]
    @property
    def nbc(self) -> int:
        """ getter: number of columns """
        return self.__data[1]
    @property
    def stones(self) -> int:
        """ getter: number of aligned stones to win """
        return self.__data[2]
    @property
    def cylinder(self) -> bool:
        """ getter: type of board True infinite, False: finite """
        return self.__data[3]
    @property
    def timer(self) -> int:
        """ getter: the number of stones played """
        return self.__data[4]
    @property
    def turn(self) -> str:
        """ getter: who's turn to play """
        return self.__color[self.timer % 2 +1]
    @property
    def opponent(self) -> str:
        """ getter: who's the opponent of the current player """
        return (self.__color[1] if self.turn==self.__color[-1]
                else self.__color[-1])
    @property
    def winner(self):
        """ the winner of the game """
        if self.win(): return self.opponent
        return None
    @property
    def state(self) -> tuple:
        """ getter: the ordered game play """
        return tuple(self.__data[5])
    @state.setter
    def state(self, value:Iterable):
        """ setter: state can be set, if acceptable for the board settings """
        _old = self.__data # store the old information
        self.reset() # restart from scratch
        try: # encapsulation of potential errors
            for _, (_line,_col) in enumerate(value):
                if self.over():
                    raise ValueError("game is over: no more stone allowed")
                
                if _line != self.__data[6][_col]:
                    raise ValueError("found {} expecting {} at column {}"
                                     "".format(_line, self.__data[6][_col],
                                               _col))
                # add to history
                self.__data[5].append( (_line, _col) )
                # update board
                self.__data[7][c2p( (_line, _col), self.nbc)] = self.timer%2 +1
                # update counts
                self.__data[6][_col] += 1
                # update timer
                self.__data[4] += 1
            _ok = True
        except Exception as _e:
            if __debug__:
                print(">>> step {} ({}, {}):".format(_,_line,_col), _e)
            _ok = False
        if not _ok: self.__data = _old # backup
            
    @property
    def actions(self) -> tuple:
        """ getter: the allowed actions of the player """
        _clabel = "ABCDEFGHIJKLMNOQRSTUVWXYZ"
        return (() if self.win()
                else tuple([_clabel[i] for i in range(self.nbc)
                      if self.__data[6][i] < self.nbl]))
    @property
    def board(self) -> tuple:
        """ getter: 1D grid of int 
                    0: empty, 
                    1: 1st player's stone, 
                    2: 2nd player's stone
        """
        return tuple(self.__data[7])

    def move(self, act:str):
        """ change board if act is licit """
        _clabel = "ABCDEFGHIJKLMNOQRSTUVWXYZ"
        if act in self.actions:
            # index of action
            _col = _clabel.index(act)
            # line detection, knowing the column
            _line = self.__data[6][_col]
            # add to history
            self.__data[5].append( (_line, _col) )
            # update board
            self.__data[7][c2p( (_line, _col), self.nbc)] = self.timer%2 +1
            # update counts
            self.__data[6][_col] += 1
            # update timer
            self.__data[4] += 1

    def undo(self):
        """ undo last move. required a move has been done """
        # remove last choice
        _last = self.__data[5].pop(-1)
        # update board
        self.__data[7][c2p(_last, self.nbc)] = 0
        # update counts
        self.__data[6][_last[1]] = _last[0]
        # update timer
        self.__data[4] -= 1

    def reset(self):
        """ restart the 'game' """
        self.__data = [self.nbl, self.nbc,
                       self.stones, self.cylinder,
                       0,
                       [], 
                       [0 for i in range(self.nbc)],
                       [0 for i in range(self.nbl*self.nbc)]
                       ]

    def over(self) -> bool:
        """ return True iff game is over """
        return self.actions == ()

    def win(self) -> bool:
        """ return True iff the last stone is a win """
        return False

    def show_msg(self) -> str:
        """ provides some msg if game is over """
        if self.cylinder:
            _msg = "Board is a cylinder\n"
        else:
            _msg = "Board is flat\n"
        if self.over():
            if not self.win():
                _msg += ("Game is a draw - last stone in {}\n"
                         "".format(self.state[-1]))
            else:
                _msg += ("Game is a win in {} steps for {}\n"
                         "last stone is {}\n"
                         "".format(self.timer, self.opponent, self.state[-1]))
        else:
            _msg += ("Stone(s) on the board {:02d},\n"
                    "{} to play choose among {}\n"
                    "".format(self.timer, self.turn,self.actions))
        return _msg
    
if __name__ == "__main__":
    main()
