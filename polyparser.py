#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module de parsing des fichiers d'entrée pour la mise en oeuvre du projet Poly#.
"""
import re

def parse_challenge(filename: str) -> object:
    """Lit un fichier de challenge et extrait les informations nécessaires.

    Vous pouvez choisir la structure de données structurées qui va
    représenter votre challenge: dictionnaire, objet, etc
    """
    with open(filename, 'r') as f:
        # Lire la première ligne, la découper, et convertir les valeurs en entier
        line = f.readline().strip()
        # Strip everything after #
        line = re.sub(r'\s*#.*', '', line)
        rows, columns, altitudes = [ int(v) for v in line.split() ]

        # ...
    challenge = None
    return challenge
