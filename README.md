# Projet Poly#
Le projet Polyhash est un projet initié par Polytech Nantes. Il s'agit d'un projet de programmation en Python qui a pour but de coordonner des ballons en haute altitude pour fournir un accès à Internet dans des zones ciblées, en utilisant les courants de vent pour les déplacer. Voici les principaux éléments du projet :
##### Contexte :
* **Objectif** : Fournir un accès Internet dans des zones isolées grâce à une flotte de ballons équipés de transmetteurs LTE.
* **Défi principal** : Les ballons ne peuvent pas se déplacer horizontalement par eux-mêmes, mais peuvent ajuster leur altitude pour exploiter les courants de vent.

A terme, l'objectif est de réaliser le meilleur score possible. Pour cela, il est nécessaire de déterminer la trajectoire optimale des ballons pour couvrir le plus de zones possibles.


## Prérequis

Avant de lancer le projet, assurez-vous que Python 3.13.0 et les dépendances nécessaires sont installés :

```bash
pip install -r requirements.txt
```
*Celle ci ne sont pas obliger si on souhaite juste faire fonctionner les algorithmes sans l'affichage*

# Lancer le Projet

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

## Paramètres :
- **./challenges/challenge.in** (str) : Le fichier d'entrée avec les données du défi.
- **./output/sortie.txt** (str) : Le chemin vers l'endroit et nom du fichier de sortie avec les résultats.
- **-debug** (bool) : Affiche les logs pour le débogage.
- **-controller** (bool):  Ne pas refaire la vérification du Solver pour améliorer les performances.
- **-displays** (list[string]): Choisir les graphiques à afficher (`display_3d`, `display_2d`).
- **-algo** (string): Sélectionner l'algorithme à utiliser (`algo1`, `algo2`, `algo3`).

*Pour les bool mettre -debug ou -controller sans valeur, cela revient à mettre True. Donc ne pas mettre -debug False par exemple.*

*Pour les listes mettre -displays display_3d display_2d par exemple. Les valeurs possibles sont display_3d et display_2d.*

## Display

Actuellement nous avons realiser un seul graphique qui est le suivant : `simulation_2d"

`simulation_2d" permet de montrer la carte en 2d sans les altitude avec les cible plus les ballons avec leur rayon fonctionnent tour par tour.
Pour fonctionner il ouvre un server en localhost


# Algorithme

Nous avons realiser different algorthme qui sont plus au moins performant sur les jeux de test et avec des parametrage varié

## Mathis

### parametrage


## Performence
### Performances des Algorithmes

| **Algorithme**   | **Complexité** | **Parallélisme** | **Temps d'exécution par jeu de test (Setup basic)** | **Efficacité moyenne** |
|------------------|----------------|------------------|-----------------------------------------------------|------------------------|
| **Mathis (algo1)**   | Faible         | Aucun            | 1-2 secondes                                        | Moyenne                |
| **Optimisé (algo2)** | Moyenne        | Limité           | 5-10 secondes                                       | Haute                  |
| **Avancé (algo3)**   | Haute          | Fortement parallélisé | 10-20 secondes                                      | Très haute             |



# L'équipe

- RABUSSEAU Mathis - mathis.rabusseau@etu.univ-nantes.fr
- GROMARD Alexys - alexys.gromard@etu.univ-nantes.fr
- FOURNIER Bastien - bastien.fournier@etu.univ-nantes.fr
- JOUAULT Lancelot - lancelot.jouault@etu.univ-nantes.fr
