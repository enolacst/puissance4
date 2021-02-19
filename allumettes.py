#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Jeu à deux joueurs
Le jeu est constitué de N [1 à 25] allumettes
A tour de rôle 
un joueur retire de 1 à 3 allumettes

2 formes de jeu
A: le perdant est celui qui prend la dernière allumette [True]
B: le gagnant est celui qui prend la dernière allumette [False]
"""

from tools.abstract_game import Board
import random

class Matches(Board):
    def __init__(self, a:int, b:bool):
        self.__board = max(min(25, a), 1), bool(b)
        self.__init_board = self.__board[:]
        super().__init__(*self.__init_board)

    def reset(self):
        super().reset()
        print("matches")
        self.__board = self.__init_board[:]

    @property
    def board(self): return tuple(self.__board)
    @property
    def state(self): return self.board[0]
    @state.setter
    def state(self, cfg:int):
        self.__board = cfg, self.__board[1]
    @property
    def actions(self) -> tuple:
        """ Choose the numer of matches """
        if self.over(): return ()
        return tuple(list(range(1, min(3, self.__board[0])+1)))
    @property
    def winner(self):
        """ defines the winner """
        if self.over():
            return self.turn if self.board[1] else self.opponent
        return None
    def over(self) -> bool:
        """ no move """
        return self.board[0] == 0
    def win(self) -> bool:
        """ no move available """
        return self.over()
    def move(self, action):
        if action in self.actions:
            _old, _rule = self.__board
            self.add_history((self.board, self.timer))
            self.__board = _old - action, _rule
            self.timer += 1
    def undo(self):
        _ = self.pop_history()
        if _ is not None:
            self.__board, self.timer = _

    def __str__(self):
        """ Modification de l'affichage par défaut """
        _msg = """
Il y a {:02} allumettes. Retirez de 1 à 3 allumettes.
Pour gagner vous {} prendre la dernière allumette\n
""".format(self.board[0],
           "ne devez pas" if self.board[1] else "devez")
        return _msg + self.show_msg()
    
    def show_msg(self):
        return ("Coup(s) joué(s) = {}, trait au joueur {}\n"
                "".format(self.timer, self.turn+1))
