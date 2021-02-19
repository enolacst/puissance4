#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# this file is supposed to define all the players
__date__ = "12.02.21"
__author__ = "Panetier Camille, Vessière Zoé et Constanceau Enola"
__usage__=""" """

from zec_01 import Board
from abstract_player import Player
import random

#==============================================================================================
class Randy (Player):
    def decision (self, state):
        """reçoit en entrée une situation de jeu et renvoie une action autorisée"""
        self.game.state = state
        if self.game.turn != self.who_am_i:
            print("not my turn to play")
            return None
        return random.choice(self.game.actions)
        
#==============================================================================================
class Human(Player):
    """Actions autorisées"""
    def decision(self, state):
        self.game.state = state
        if self.game.turn != self.who_am_i:
            print("not my turn to play")
            return None
        print(self.game)

        actionValide=False

        while not actionValide :
            print(self.game.actions)
            action = input("quelle est l'action ? ")
            if action in self.game.actions: #vérifie que action proposée est valide
                actionValide=True
                return action
            print('Vous ne pouvez pas jouer cette action')#action impossible

#==============================================================================================
class MinMax(Player):
    lettres=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','Q','R','S','T','U','V','W','X','Y','Z']
    def decision(self, state):
        self.game.state = state
        v={}
        pf=self.get_value('pf')
        #pour chaque a_i dans ACTIONS(s):
        for a in self.game.actions :
          #calculer s_i le nouvel etat a partir de (s,a_i)
            self.game.move(a)
          #v_i = eval_min(s_i, pf-1)
            v[self.lettres.index(a)]=self.__eval_min(self.game.state,(pf-1))
            
        _max=-1000
        action = ''
        for key,value in v.items(): #calcul du max
            if value>_max :
                _max=value
                action=self.lettres[key]
        return action
        #return a_j tel que v_j = max(v_1, .. v_k)

    def __eval_min(self, s, pf):
        v={}
        if self.game.over() or pf==0 :
            return self.estimation()
        else:
            for a in self.game.actions :   
                self.game.move(a)
                v[self.lettres.index(a)]=self.__eval_max(s,pf-1)
                
            _min=1000
            for value in v: #calcul du min
                if value<_min :
                    _min=value
        return _min
          #retourner min(v_1, ... v_k)
           
    def __eval_max(self,s, pf):
        v={}
        if self.game.over() or pf==0 :
            return self.estimation()
        else:
            for a in self.game.actions :
                self.game.move(a)
                v[self.lettres.index(a)]=self.__eval_min(s,pf-1)
            _max=-1000
            for value in v: #calcul du max
                if value>_max :
                    _max=value
        return _max
#==============================================================================================

##class Negamax(Player):
##    lettres=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','Q','R','S','T','U','V','W','X','Y','Z']
##    def decision(self, state):
##        self.game.state = state
##        v={}
##        pf=self.get_value('pf')
##        #pour chaque a_i dans ACTIONS(s):
##        for a in self.game.actions :
##          #calculer s_i le nouvel etat a partir de (s,a_i)
##            self.game.move(a)
##          #v_i = __eval_negamax(s_i, pf-1)
##            v[self.lettres.index(a)]=self.__eval_negamax(self.game.state,(pf-1))
##            
##        _max=-1000
##        action = ''
##        for key,value in v.items(): #calcul du max
##            if value>_max :
##                _max=value
##                action=self.lettres[key]
##        return action
##    
##    def __eval_negamax(self,s, pf):
##        v={}
##        if self.game.over() or pf==0 :
##            return self.estimation()
##        else:
##            for a in self.game.actions :
##                self.game.move(a)
##                v[self.lettres.index(a)]=self.__eval_negamax(s,pf-1)
##
##            _max=-1000
##            for value in v: #calcul du max
##                if value>_max :
##                    _max=value
##        return _max
##  
###==================================
##class AlphaBet(Player):
##    def decision(self, state):
##        self.game.state = state
##        pour chaque a_i dans ACTIONS(s) faire
##         calculer s_i le nouvel etat a partir de (s,a_i)
##         v_i = coupe_alpha(s_i, pf-1, alpha, beta)
##    return a_j tel que v_j = max(v_1, .. v_k)
##
##    def __coupe_alpha(s, pf, alpha, beta):
##        # MIN cherche a diminuer beta
##        if self.game.over() or pf==0 :
##           return self.estimation()
##        else:
##            soit s_1, .. s_k les nouveaux etats construits par (s, a_j)
##            i=1
##            tant que i <= k et alpha < beta faire
##               v_j = coupe_beta(s_j, pf -1, alpha, beta)
##               if v_j <= alpha:
##                   return alpha
##                   beta = min(beta, v_j)
##                    i = i+1
##          
##            return beta
##
##    def __coupe_beta(s, pf, alpha, beta):
##        # MAX cherche a augmenter alpha
##        if self.game.over() or pf==0 :
##           return self.estimation()
##        else :
##            soit s_1, .. s_k les nouveaux etats construits par (s, a_j)
##            i=1
##            while i <= k et alpha < beta :
##                v_j = coupe_alpha(s_j, pf -1, alpha, beta)
##                si v_j >= beta: retourner beta
##                alpha = max(alpha, v_j)
##                i = i+1
##            
##            return alpha
##
##
##
##
