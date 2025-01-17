# bfs.py

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
        print(self.graph)
        return 

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