#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# this file is supposed to define all the players
__date__ = "08.02.21"
__author__ = "Panetier Camille, Vessière Zoé et Constanceau Enola"
__usage__=""" """

from abstract_player import Player
import random

class Randy:
    def decision (self, state):
        """reçoit en entrée une situation de jeu et renvoie une action autorisée"""
        self.game.state = state
        if self.game.turn != self.who_am_i:
            print("not my turn to play")
            return None
        random.choice

class Humain:
    """Actions autorisées"""
    def decision(self, state):
        self.game.state = state


class MinMax:
    def decision(self, state):
##      pour chaque a_i dans ACTIONS(s) faire
##          calculer s_i le nouvel etat a partir de (s,a_i)
##          v_i = eval_min(s_i, pf-1)
##      return a_j tel que v_j = max(v_1, .. v_k)
##    
##  def __eval_min(s, pf)
##      if s est une feuille :
##          alors retourner estimation()
##      else:
##          soit s_1, .. s_k les nouveaux etat construit par (s, a_j)
##          v_j = eval_max(s_j, pf -1)
##          retourner min(v_1, ... v_k)
##           
##  def __eval_max(s, pf)
##      si s est une feuille alors retourner estimation()
##      sinon
##          soit s_1, .. s_k les nouveaux etat construit par (s, a_j)
##          v_j = eval_min(s_j, pf -1)
##          retourner max(v_1, ... v_k)

class Negamax:
    def decision(self, state):
##        pour chaque a_i dans ACTIONS(s) faire
##            calculer s_i le nouvel etat a partir de (s,a_i)
##            v_i = - eval_negamax(s_i, pf-1)
##        return a_j tel que v_j = max(v_1, .. v_k)
    
    def __eval_negamax(s, pf):
##        si s est une feuille alors retourner estimation()
##        sinon
##           soit s_1, .. s_k les nouveaux etats construits par (s, a_j)
##           v_j = - eval_negamax(s_j, pf -1)
##           retourner max(v_1, ... v_k)
  

class AlphaBet:
    def decision(self, state):
##        pour chaque a_i dans ACTIONS(s) faire
##         calculer s_i le nouvel etat a partir de (s,a_i)
##         v_i = coupe_alpha(s_i, pf-1, alpha, beta)
##    return a_j tel que v_j = max(v_1, .. v_k)

    def __coupe_alpha(s, pf, alpha, beta):
        # MIN cherche a diminuer beta
##        si s est une feuille alors retourner estimation()
##        sinon
##            soit s_1, .. s_k les nouveaux etats construits par (s, a_j)
##            i=1
##            tant que i <= k et alpha < beta faire
##               v_j = coupe_beta(s_j, pf -1, alpha, beta)
##               si v_j <= alpha: retourner alpha
##                   beta = min(beta, v_j)
##                    i = i+1
##            fait
##            retourner beta

    def __coupe_beta(s, pf, alpha, beta):
        # MAX cherche a augmenter alpha
##        si s est une feuille alors retourner estimation()
##        sinon
##            soit s_1, .. s_k les nouveaux etats construits par (s, a_j)
##            i=1
##            tant que i <= k et alpha < beta faire
##                v_j = coupe_alpha(s_j, pf -1, alpha, beta)
##                si v_j >= beta: retourner beta
##                alpha = max(alpha, v_j)
##                i = i+1
##            fait
##            retourner alpha

if __name__ == "__main__":
    main()



