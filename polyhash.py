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
from core.utils import DebugPrinter

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
    
    # recupere param -display pour spécifier si on affiche ou pas    
    parser.add_argument('-controller', action='store_true', default=False,
                        help='Boolean to display or not (default: False)')
    
    # recupere param -displays pour spécifier les noms des displays à utiliser
    parser.add_argument('-displays', nargs='*', default=[], help='List of display names to use (default: None)')

    # recupere param -debug pour spécifier si on affiche le debugerPrinter
    parser.add_argument('-debug', action='store_true', default=False,
                        help='Enable debugging (default: False)')

    # recupere param -algo pour spécifier l'algorithme à utiliser
    parser.add_argument('-algo', type=str, default=None,
                        help='Algorithm to use (default: Mathis)')    
    
    args = parser.parse_args()
    

    # si le paramètre -debug est passé, on affiche le debugerPrinter
    # verifier si l'algorithme est valide
    if type(args.debug) is not bool and args.debug != None:
        raise TypeError(f"Invalid debug value: {args.debug}")
    else :
        DebugPrinter.set_display(args.debug)
        

    # Début du programme
    solver = Solver(args.challenge, args.output, args.controller, args.displays, args.algo)   # crée une instance de Solver
    solver.run()                                                            # lance les calculs de l'algorithme
    solver.post_process2()                                                   # génère le fichier de sortie et vérifie les résultats

    