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
    parser.add_argument('challenge', type=str,
                        help='challenge definition filename',
                        metavar="challenge.txt")
    
    parser.add_argument('output', type=str, default=None,
                        help='output filename',
                        metavar="sortie.txt")
    
    args = parser.parse_args()
    
    Solver(args.challenge, args.output)


    