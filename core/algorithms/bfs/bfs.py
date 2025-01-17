# bfs.py

import random

from collections import deque

from ...models import DataModel,Vector3
from ...utils import DebugPrinter
from ..Algorithm import Algorithm
from core import Arbitrator

class BFS(Algorithm):
    """
    Breadth First Search algorithm

    Attributes:
        data (DataModel): data of the problem
        trajet (list[list[int]]): order of the balloons' movements
    """

    def __init__(self, data: 'DataModel') -> None:
        """
        Constructor of the BFS class

        Args:
            data (DataModel): _description_
        """
        super().__init__(data)
        self.arbitrator = Arbitrator(data)

    def graph_generation(self) -> list[list[int]]:
        """
        Generate the graph of the problem

        Returns:
        """
        # Création des arêtes
        print("Generating graph")
        self.graph = {}
        for row in range(self.data.rows):
            for col in range(self.data.cols):
                for alt in range(self.data.altitudes):
                    self.graph[(row, col, alt)] = []

                    # Récupérer le vent
                    wind = self.data.wind_grids[alt][row][col]

                    # Récupérer la nouvelle position
                    new_row = row + wind.x
                    new_col = col + wind.y

                    # Si la nouvelle position n'est pas dans la grille, on ne l'ajoute pas
                    if new_row < 0 or new_row >= self.data.rows or new_col < 0 or new_col >= self.data.cols:
                        continue

                    # Récupérer le nombre de points obtenus si l'on se rend à cette position
                    points = self.arbitrator.score_for_ballon(Vector3(new_row, new_col, alt)) # C'est le poids de l'arête

                    # Ajouter l'arête
                    self.graph[(row, col, alt)].append(((row, col, alt), points))
        print("Graph generated")

    def compute(self) -> list[list[int]]:
        """
        Compute the algorithm

        Returns:
            list[list[int]]: order of the balloons' movements
        """

        self.graph_generation()

        # Init des variables
        total_points = 0
        trajectory = [[] for _ in range(self.data.turns)]

        # Initialisation des ballons
        ballons = []
        for ballon in range(self.data.num_balloons):
            ballons.append(Vector3(self.data.starting_cell.x, self.data.starting_cell.y, 0))

        for turn in range(self.data.turns):
            itinary = [] # Liste des mouvements des ballons (pour ne pas faire aller 2 ballons sur la même case)
            for i, ballon in enumerate(ballons):
                # On cherche pour la position du ballon, l'altitude qui maximise le score (dans self.graph)
                max_score = 0
                best_alt = 0
                for alt in range(self.data.altitudes):
                    if self.graph[(ballon.x, ballon.y, alt)] and self.graph[(ballon.x, ballon.y, alt)][0][1] > max_score and (ballon.x, ballon.y, alt) not in itinary:
                        max_score = self.graph[(ballon.x, ballon.y, alt)][0][1]
                        best_alt = alt
                # Si best_alt == 0, prendre une altitude aléatoire
                if best_alt == 0:
                    for _ in range(self.data.altitudes):
                        best_alt = random.randint(0, self.data.altitudes - 1)
                        # Vérifier si l'altitude n'a pas déjà été prise et qu'il y a une arête qui part de cette altitude
                        if (ballon.x, ballon.y, best_alt) not in itinary and self.graph[(ballon.x, ballon.y, best_alt)]:
                            break

                # Ajouter l'intinéraire
                itinary.append((ballon.x, ballon.y, best_alt))

                # Ajouter le mouvement à la trajectoire
                # print(f"Ballon {i} : {ballon.x} {ballon.y} {ballon.z} -> {ballon.x} {ballon.y} {best_alt}")
                trajectory[turn].append(best_alt - ballon.z)

                # Mettre à jour la position du ballon
                ballon.z = best_alt

                # Déplacer le ballon
                self.data.updatePositionWithWind(ballon) # Mettre à jour la position du ballon directement dans le paramètre

                ballons[i] = Vector3(ballon.x, ballon.y, ballon.z)

            # Calculer le score
            total_points += self.arbitrator.turn_score(ballons)
        print(f"Total points: {total_points}")
        return trajectory

    def _convert_data(self) -> None:
        """
        Convert the data of the problem to a format usable by the algorithm.
        """
        pass

    def _process(self) -> bool:
        """
        Compute the trajectory of the balloons.

        Returns:
            bool: True if the trajectory is computed, False otherwise
        """
        pass