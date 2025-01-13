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
python polyhash.py ./challenges/challenge.in ./output/sortie.txt
```	

### Commande Complète
La syntaxe complète est

```bash
python polyhash.py ./challenges/challenge.in ./output/sortie.txt -debug -display -displays diplay_3d display_2d -algo algo1
```

**Paramètres** :
- **./challenges/challenge.in** (string):   Fichier d'entrée
- **./output/sortie.txt** (string):         Fichier de sortie
- **-debug** (bool):                        Permet d'afficher les logs 
- **-controller** (bool):                    Permet de ne pas refaire la verification du Solver (gain de performance)
- **-displays** (list[string]):            Permet de choisir les graphiques à afficher (display_3d, display_2d)
- **-algo** (string):                       Permet de choisir l'algorithme à utiliser (algo1, algo2, algo3)

*Pour les bool mettre -debug ou -controller sans valeur, cela revient à mettre True. Donc ne pas mettre -debug False par exemple.*

*Pour les listes mettre -displays display_3d display_2d par exemple. Les valeurs possibles sont display_3d et display_2d.*

# Algorithme



# L'équipe

- RABUSSEAU Mathis - mathis.rabusseau@etu.univ-nantes.fr
- GROMARD Alexys - alexys.gromard@etu.univ-nantes.fr
- FOURNIER Bastien - bastien.fournier@etu.univ-nantes.fr
- JOUAULT Lancelot - lancelot.jouault@etu.univ-nantes.fr
