#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Jeu à 2 joueurs

Le jeu est constitué de 3 lignes d'allumettes
A tour de rôle un joueur
* choisit une ligne
* retire de cette ligne des allumettes

La partie s'arrête quand il n'y a plus d'allumettes

Variantes
> configuration des lignes
1 -> k / k+1 -> 2k / 2k+1 -> 3k
k / random(k+1, 2k) / random(2k+1, 3k)

> nombre d'allumettes à prendre (1 à 3) ou (1 à toutes)
> le gagnant prend la dernière, le perdant prend la dernière
"""

from tools.abstract_game import Board
from typing import Sized
import random

class Marienbad(Board):
    def __init__(self, a:int, variante:int,
                 prise:bool=True, prendre:bool=True):
        """
        a: le nombre d'allumettes de référence entre 5 et 13
        variante: 0/1/2
        prise: True 1 à 3, False 1 à n
        prendre: True 'prendre la dernière pour gagner', 
                 False 'ne pas prendre la dernière pour gagner
        """
        random.seed()
        _a = int(a) if 5 <= a <= 13 else random.choice(range(5, 14))
        _b = variante if variante in range(3) else random.choice(range(3))
        _c, _d = bool(prise), bool(prendre)
        if _b == 0:
            _board = [ _a, 2*_a, 3*_a]
        elif _b == 1:
            _board = [_a, random.randrange(_a+1, 2*_a+1),
                      random.randrange(2*_a+1, 3*_a+1) ]
        else:
            _board = [int(2**(i-2) * _a) for i in range(3)]
        self.__board = _board, _c, _d
        self.__init_board = self.__board[:]
        super().__init__(*self.__init_board)

    def reset(self):
        super().reset()
        print('marienbad')
        self.__board = self.__init_board[:]

        
    @property
    def board(self): return tuple(self.__board[0])
    @property
    def state(self): return self.board
    @state.setter
    def state(self, cfg:Sized):
        if self.__valid(*cfg):
            _, _1, _2 = self.__board
            self.__board = list(cfg), _1, _2
    def __valid(self, *cfg) -> bool:
        """ check that it's fine """
        if len(cfg) != 3: return False
        if any([0 > cfg[i] for i in range(3)]): return False
        if any([cfg[i] > self.__init_board[0][i]
                for i in range(3)]): return False
        if any([not isinstance(x, int) for x in cfg]): return False
        return True
    @property
    def actions(self) -> tuple:
        """ access which box, remove how much matches """
        if self.over(): return ()
        _boxes = "ABC"
        _sz = len(_boxes)
        return tuple([ (_boxes[i], k+1)
                      for i in range(_sz)
                      for k in (range(min(3, self.board[i]))
                                if self.__board[1] else
                                range(1, self.board[i]+1))
                    ])
    def over(self) -> bool:
        """ no more move """
        return sum(self.board)==0
    @property
    def winner(self):
        """ defines the winner """
        return self.opponent if self.__board[-1] else self.turn
    def win(self) -> bool:
        """ the only win is when it's over """
        return self.over()
    def move(self, action:tuple):
        """ action is a tuple of size 2 """
        if action in self.actions:
            _boxes = "ABC"
            i = _boxes.index(action[0])
            j = action[1]
            self.add_history((self.board, self.timer))
            _v, _h, _p = self.__board
            _v[i] -= j
            self.__board = _v, _h, _p
            self.timer += 1
    def undo(self):
        _ = self.pop_history()
        if _ is not None:
            self.state, self.timer = _

    def show_msg(self) -> str:
        return ("Coup(s) joué(s) = {}, trait au joueur {}\n"
                "".format(self.timer, self.turn+1))


    def __str__(self) -> str:
        """ Modification de l'affichage par défaut """
        _prise = ("1 à 3 allumettes" if self.__board[1] else
                  "au moins 1 allumette")
        _prendre = ("devez" if self.__board[-1] else
                    "ne devez pas")
        _msg = """
Vous avez devant vous 3 groupes d'allumettes
A votre tour de jeu vous devez choisir 1 groupe
et, dans ce groupe, vous enlevez {}

Pour gagner vous {} prendre la dernière allumette de la dernière boîte

""".format(_prise, _prendre)

        return _msg + super().__str__()
