#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module principal pour la mise en oeuvre du projet Poly#.
"""

# IMPORT

    # documentation du module argparse:
    # https://docs.python.org/3/library/argparse.html
import argparse


# import local
from core import Solver


# MAIN
if __name__ == "__main__":
    # On fournit ici un exemple permettant de passer un simple
    # argument (le fichier du challenge) en paramètre. N'hésitez pas à
    # compléter avec d'autres paramètres/options, en consultant la


    parser = argparse.ArgumentParser(description='Solve Poly# challenge.')
    
    # recupere param -challenge pour spécifier le fichier de data
    parser.add_argument('challenge', type=str,
                        help='challenge definition filename',
                        metavar="challenge.txt")
    
    # recupere param -output pour spécifier le fichier de sortie
    parser.add_argument('output', type=str, default=None,
                        help='output filename',
                        metavar="sortie.txt")
    
    # recupere param -display pour spécifier si on affiche ou non
    parser.add_argument('-display', type=bool, default=False,
                        help='Boolean to display or not (default: False)')

    # recupere param -algo pour spécifier l'algorithme à utiliser
    parser.add_argument('-algo', type=str, default=None,
                        help='Algorithm to use (default: Mathis)')    
    
    args = parser.parse_args()
    

    
    
    solver = Solver(args.challenge, args.output, args.display, args.algo)   # crée une instance de Solver
    solver.run()                                                            # lance les calculs de l'algorithme
    solver.post_process()                                                   # génère le fichier de sortie et vérifie les résultats

    