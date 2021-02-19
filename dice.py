#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Jeu à deux joueurs
Le jeu est constituée 
- d'un compteur entier (à ne pas dépasser) [entre 7 et 100]
- d'une face visible d'un dé à 6 faces
A tour de rôle 
un joueur choisit de faire une rotation d'un quart de tour du dé
en changeant la face visible
le compteur est décrémenté de cette valeur
* la partie s'arrete quand un joueur fait passer le compteur à une valeur 
  négative
* le gagnant est l'autre joueur

exemple
[ 5, 2]. 
Le joueur qui a le trait peut tourner le dé sur 1, 3, 4 ou 6
S'il choisit le 1, la situation devient [4, 1]
S'il choisit le 3, la situation devient [2, 3]
S'il choisit le 4, la situation devient [1, 4]
S'il choisit le 6, la situation devient [-1, 6]

Dans le dernier cas, le jeu s'arrête (compteur négatif) l'adversaire a gagné
Dans le premier cas [4, 1], l'autre joueur aura le choix entre
les faces 2, 3, 4, et 5 et le processus 
  "choix de la face, décompte de la face" 
continue jusqu'à l'arrêt du jeu
"""

from tools.abstract_game import Board
from typing import Sized
import random

class Dice(Board):
    def __init__(self, a:int, random_state:int=42):
        random.seed(random_state)
        if not isinstance(a, int) : a = random.choice(range(7, 101))
        else: a = max(7, min(100, a))
        b = random.choice(range(1, 7))
        self.__board = a,b
        self.__init_board = self.__board[:]
        super().__init__(*self.__init_board)

    def reset(self):
        super().reset()
        print("dice")
        self.__board = self.__init_board[:]

    @property
    def board(self): return tuple(self.__board)
    @property
    def state(self): return self.board
    @state.setter
    def state(self, cfg:Sized):
        if self.__valid(*cfg): self.__board = cfg
    def __valid(self, *cfg):
        """ is this configuration fine """
        if len(cfg) != 2: return False
        if cfg[0] not in range(-6, 101): return False
        if cfg[1] not in range(1, 7): return False
        if any([not isinstance(x, int) for x in cfg]): return False
        return True
    @property
    def actions(self) -> tuple:
        """ which head should be up """
        if self.over(): return ()
        return tuple([ x for x in range(1,7)
                       if (x != self.board[1] and x+self.board[1] != 7)])
    @property
    def winner(self):
        """ defines the winner """
        if self.over(): return self.turn
        return None
    def over(self) -> bool:
        """ no move """
        return self.board[0] < 0
    def win(self) -> bool:
        """ no move available """
        return self.over()
    def move(self, action):
        if action in self.actions:
            _old,_ = self.__board
            self.add_history((self.board, self.timer))
            self.__board = _old - action, action
            self.timer += 1
    def undo(self):
        _ = self.pop_history()
        if _ is not None:
            self.__board, self.timer = _
    def show_msg(self):
        return ("Coup(s) joué(s) = {}, trait au joueur {}\n"
                "".format(self.timer, self.turn+1))

    def __str__(self):
        """ Modification de l'affichage par défaut """
        _msg = """
A: le compteur à ne pas dépasser
B: la face visible du dé
Tournez le dé d'1/4 de tour: si après coup, A - B < 0 vous avez perdu

"""

        return _msg+super().__str__()
