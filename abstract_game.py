#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Classe abstraite de jeu à 2 joueurs 
"""
from tools.ezCLI import grid

class Board:
    def __init__(self, *args, **kargs):
        self.__args = args
        self.__kargs = kargs
        self.reset()

    def reset(self):
        """ what should be restarted """
        self.timer = 0
        self.__history = []

    @property
    def arguments(self): return self.__args
    @property
    def key_arguments(self): return self.__kargs.copy()

    @property
    def turn(self):
        return self.timer%2
    @property
    def opponent(self):
        return (self.turn+1)%2

    def add_history(self, value):
        """ store useful info that might be undone """
        self.__history.append(value)
    def pop_history(self):
        """ go one step back """
        if self.__history != []:
            self.timer -= 1
            return self.__history.pop(-1)

    def __repr__(self):
        return ("{0}({1.arguments}, {1.key_arguments})"
                "".format(self.__class__.__name__,self))

    def __str__(self) -> str:
        if not isinstance(self.board[0], (list, tuple)):
            _grid = [ self.board ]
        else:
            _grid = self.board
        
        return grid(_grid, label=True, size=3)+"\n"+self.show_msg()
    def show_msg(self) -> str:
        return ''

    @property
    def winner(self):
        """ the winner of the game """
        return None
    
    @property
    def board(self):
        raise NotImplementedError("board getter: to be defined")
    @property
    def state(self):
        raise NotImplementedError("state getter: to be defined")
    @state.setter
    def state(self, val):
        raise NotImplementedError("state setter: to be defined")
    def over(self) -> bool:
        raise NotImplementedError("over(): to be defined")
    def win(self) -> bool:
        raise NotImplementedError("win(): to be defined")
    @property
    def actions(self):
        raise NotImplementedError("actions getter: to be defined")

    def move(self, act):
        raise NotImplementedError("move(action): to be defined")

    def undo(self):
        raise NotImplementedError("undo(): to be defined")
            
