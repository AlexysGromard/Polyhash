# Projet Poly#
Le projet Polyhash est un projet initié par Polytech Nantes. Il s'agit d'un projet de programmation en Python qui a pour but de coordonner des ballons en haute altitude pour fournir un accès à Internet dans des zones ciblées, en utilisant les courants de vent pour les déplacer. Voici les principaux éléments du projet :
##### Contexte :
* **Objectif** : Fournir un accès Internet dans des zones isolées grâce à une flotte de ballons équipés de transmetteurs LTE.
* **Défi principal** : Les ballons ne peuvent pas se déplacer horizontalement par eux-mêmes, mais peuvent ajuster leur altitude pour exploiter les courants de vent.

A terme, l'objectif est de réaliser le meilleur score possible. Pour cela, il est nécessaire de déterminer la trajectoire optimale des ballons pour couvrir le plus de zones possibles.

# Fonctionnement du projet

Description du fonctionnement du projet, notamment comment le lancer (paramètres, etc).

### Commande Minimale
La syntaxe générale/minimale est

```sh
polyhash.py ./challenges/challenge.in ./output/sortie.txt
```	

### Commande Complète
La syntaxe complète est

```sh
polyhash.py ./challenges/challenge.in ./output/sortie.txt -display True -algo algo1
```

**Paramètres** :
- **./challenges/challenge.in** (string):   Fichier d'entrée
- **./output/sortie.txt** (string):         Fichier de sortie
- **-display** (bool):                    Permet d'afficher les graphiques de la simulation
- **-algo** (string):                       Permet de choisir l'algorithme à utiliser (algo1, algo2, algo3)

# L'équipe

- RABUSSEAU Mathis - mathis.rabusseau@etu.univ-nantes.fr
- GROMARD Alexys - alexys.gromard@etu.univ-nantes.fr
- FOURNIER Bastien - bastien.fournier@etu.univ-nantes.fr
- JOUAULT Lancelot - lancelot.jouault@etu.univ-nantes.fr
