#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
from abstract_player import Player
from tools.checkTools import check_property
from typing import Sized

try:
    from players import * # les joueurs
except Exception as _e:
    print("Missing players")

# initialisation
if len(sys.argv) == 1:
    param = input("quel est le fichier de description du jeu ? ")
    if not os.path.isfile(param): ValueError("need a python file")
else: param = sys.argv[1]

target = param.split('.')[0]

_out = check_property(target != '','acces au fichier')
print("tentative de lecture de {}".format(target))
try:
    c4 = __import__(target) # revient à faire import XXX as tp
    assert hasattr(c4, 'Board')
except Exception as _e:
    print(_e)
    sys.exit(-1)


class Statistics:
    """ collect information about victories """
    def __init__(self, p1:str, p2:str, g:c4.Board):
        g.reset() # to be sure the names are fine
        self.__game = repr(g)
        self.__colors = (g.turn, g.opponent)
        self.__names = p1, p2
        self.__keys = "pv sigma avg_victories avg_stones".split()
        self.__labels = {self.__keys[i+2]: self.__keys[i]
                         for i in range(2)}
        self.__data = {k:
                       {ident:0 for ident in (p1, p2, g.turn, g.opponent)}
                       for k in self.__keys}
        self.reset()

    def reset(self):
        """ restart data """
        for k in self.__data:
            for q in self.__data[k]: self.__data[k][q] = 0
        self.__count = 0
        self.__built = False

    @property
    def keys(self): return tuple(self.__keys)
    @property
    def subkeys(self): return tuple(self.__data['pv'].keys())
        
    def __repr__(self):
        return "{0}({1}, {2}, {3})".format(self.__class__.__name__,
                             *self.__names, self.__game)
                                             
    def add_result(self, values:Sized, names:Sized):
        """ update pv and sigma information 
            requires pv, sigma in self.__keys
        """

        if len(values) != 2 or len(names) != 2:
            raise ValueError("Rubish data")
        if names[0] not in self.subkeys:
            raise ValueError("wrong information {}".format(names[0]))
        if names[1] not in self.subkeys:
            raise ValueError("wrong information {}".format(names[1]))
        self.__count += 1 ; self.__built = False
        
        if values[0] == 0: # win red
            self.__data['pv'][self.__colors[1]] += 1
            self.__data['pv'][names[1]] += 1
            
        elif values[1] == 0: # win yellow
            self.__data['pv'][self.__colors[0]] += 1
            self.__data['pv'][names[0]] += 1
        else: # draw
            for i in range(2):
                self.__data['pv'][self.__colors[i]] += 1
                self.__data['pv'][names[i]] += 1
        for i in range(2):
            self.__data['sigma'][self.__colors[i]] += values[i]
            self.__data['sigma'][names[i]] += values[i]
            
    def __build_avg(self):
        """ helper to build avg points 
            requires self.__count > 0
        """
        if self.__built: return
        for q in self.__labels:
            _vkey = self.__labels[q]
            for k in self.__data[q]:
                self.__data[q][k] = round(self.__data[_vkey][k]/self.__count,
                                          2)
        self.__built = True


    @property
    def statistics(self):
        if self.__count != 0: self.__build_avg()
        return self.__data.copy()
        
    def main_statistic(self, key=None) -> dict:
        """ provides main statistics """
        if self.__count != 0: self.__build_avg()
        if key is None or key not in self.keys:
            return self.__data.copy()
        return self.__data[key].copy()

    def specific_statistic(self, subkey:str) -> dict:
        """ provides statistic for a specific key """
        if self.__count != 0: self.__build_avg()
        if subkey not in self.subkeys: return {}
        return {key: self.__data[key][subkey]
            for key in self.keys}

def manche(yellow:Player, red:Player, g:c4.Board) -> tuple:
    """
    requires 2 different players and a Board
    requires j.game to be similar to g
    """
    g.reset() # new start
    yellow.who_am_i = g.turn
    red.who_am_i = g.opponent
    while not g.over():
        if g.timer % 2 == 0:
            x = yellow.decision(g.state)
        else:
            x = red.decision(g.state)
        g.move(x)

    print("final Board\n{}".format(g))
    print("waiting ...", end='')
    time.sleep(.5)
    print(" Done")

    if g.win():
        if g.timer % 2 == 0:
            return (0, g.timer)
        else:
            return (g.timer, 0)
    else: # a draw
        return (g.timer/2, g.timer/2)

def partie(yellow:Player, red:Player,
           g:c4.Board, nbManches:int=2) -> Statistics:
    """ given 2 players,  a board and a number N
        runs N manche and return Statistics
    """
    if yellow == red:
        _red = red.clone()
    else:
        _red = red
    stat = Statistics(yellow.name, _red.name, g)
    for i in range(nbManches):
        if i%2 == 0:
            _ = manche(yellow, _red, g)
            stat.add_result(_,(yellow.name, _red.name))
        else:
            _ = manche(_red, yellow, g)
            stat.add_result(_,(_red.name, yellow.name))
    return stat

            
def usage() -> str:
    return """
Vous devez créer un 'Board', par exemple
>>> b = c4.Board(cylinder=True)

Vous devez créer 2 joueurs, par exemple
>>> alea = Randy('alea', b)
>>> moi = Human('mmc', b)

Vous pouvez maintenant opposer les 2 joueurs pour une manche
>>> manche(alea, moi, b)

Qui opposera 'J' (alea) à 'R' (mmc), le résultat sera le
nombre de points de chaque joueur à la fin de la partie

Vous pouvez aussi opposer les 2 joueurs pour plusieurs manches
à chaque manche le premier à jouer change
>>> partie(alea, moi, b, 2)

Il y aura 2 manches alea-mmc, le résultat sera une statistique
(nombre de victoires pour 'J', nombre de victoire pour 'R',
 nombre de victoires pour alea, nombre de victoires pour mmc,
 points totaux obtenus pour 'J', points totaux obtenus pour 'R',
 points totaux obtenus pour alea, points totaux obtenus pour mmc,
 points moyens obtenus pour 'J', points moyens obtenus pour 'R',
 points moyens obtenus pour alea, points moyens obtenus pour mmc)

>>> s = partie(....)
>>> s.statistics # all information
>>> s.main_statistic(key) # key in pv / sigma / avg_victories / avg_stones
>>> s.specific_statistic(key) # key in players names 

>>> g = c4.Board(4,4,3,True)
>>> a = Randy('alea', g)
>>> s = partie(a, a, g, 4)
>>> s.statistics
{'pv': {'alea_01': 3, 'alea_02': 1, 'J': 3, 'R': 1}, 'sigma': {'alea_01': 20, 'alea_02': 7, 'J': 17, 'R': 10}, 'avg_victories': {'alea_01': 0.75, 'alea_02': 0.25, 'J': 0.75, 'R': 0.25}, 'avg_stones': {'alea_01': 5.0, 'alea_02': 1.75, 'J': 4.25, 'R': 2.5}}
>>> s.main_statistic('pv')
{'alea_01': 3, 'alea_02': 1, 'J': 3, 'R': 1}
>>> s.specific_statistic('R')
{'pv': 1, 'sigma': 10, 'avg_victories': 0.25, 'avg_stones': 2.5}

"""

if __name__ == '__main__':
    print(usage())
 
