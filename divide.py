#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Jeu à deux joueurs
Le jeu est constituée de 2 boites contenant des jetons
A tour de rôle un joueur 
- choisit une boite, qu'il vide
- répartit les jetons restant dans les deux boites

chaque boite doit contenir au moins un jeton
* la partie s'arrete quand un joueur ne peut pas respecter les règles
* le gagnant est celui qui a empêcher l'autre de jouer

exemple
[ 5, 2]. Le joueur qui a le trait vide la boite A
et répartit les jetons de la boite B
l'adversaire doit jouer avec [1, 1]
il ne peut pas respecter les règles (impossible de répartir le résidu)
la partie s'arrête et le joueur est déclaré perdant
"""

from tools.abstract_game import Board
from typing import Sized
import random

class Divide(Board):
    def __init__(self, a:int, b:int):
        if self.__valid(a,b): self.__board = [a,b]
        else: self.__board = random.choices(range(1,11), k=2)
        self.__init_board = self.__board[:]
        super().__init__(*self.__init_board)

    def reset(self):
        super().reset()
        print("divide")
        self.__board = self.__init_board[:]

    @property
    def board(self): return tuple(self.__board)
    @property
    def state(self): return self.board
    @state.setter
    def state(self, cfg:Sized):
        if self.__valid(*cfg): self.__board = cfg
    def __valid(self, *cfg) -> bool:
        """ is this configuration fine """
        if len(cfg) != 2: return False
        if cfg[0] <= 0 or cfg[1] <= 0: return False
        if any([not isinstance(x, int) for x in cfg]): return False
        return True
    @property
    def actions(self) -> tuple:
        """ which box to remove, how many in 1st box """
        if self.over(): return ()
        _boxes = "AB"
        _sz = len(_boxes)
        return tuple([ (_boxes[i], k)
                       for i in range(_sz)
                       for k in range(1, self.board[(i+1)%2]) ])
    @property
    def winner(self):
        """ defines the winner """
        if self.over(): return self.opponent
        return None
    def over(self) -> bool:
        """ no move """
        return sum(self.board) == 2
    def win(self) -> bool:
        """ no move available """
        return self.over()
    def move(self, action):
        _boxes = "AB"
        if action in self.actions:
            i = _boxes.index(action[0])
            j = action[1]
            k = self.__board[(i+1)%2]-j
            self.add_history((self.board, self.timer))
            self.__board = j,k
            self.timer += 1
    def undo(self):
        _ = self.pop_history()
        if _ is not None:
            self.__board, self.timer = _

    def show_msg(self) -> str:
        return ("Coup(s) joué(s) = {}, trait au joueur {}\n"
                "".format(self.timer, self.turn+1))

    def __str__(self) -> str:
        """ Modification de l'affichage par défaut """
        _msg = """
A & B : 2 boites contenant des jetons

Choisissez une boite qui sera vidée
Répartissez les jetons de l'autre boite dans A & B
- il faut au moins 1 jeton par boite

Le perdant est celui qui ne peut pas respecter les règles

"""
        return _msg+super().__str__()
