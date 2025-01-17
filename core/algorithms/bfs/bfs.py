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
        self.graph = {}
        for row in range(self.data.height):
            for col in range(self.data.width):
                for alt in range(self.data.altitudes):
                    self.graph[(row, col, alt)] = []

                    # Récupérer le vent
                    wind = self.data.wind_grids[row][col][alt]

                    # Récupérer le nombre de points obtenus si l'on se rend à cette position
                    points = self.arbitrator.


    def compute(self) -> list[list[int]]:
        """
        Compute the algorithm

        Returns:
            list[list[int]]: order of the balloons' movements
        """

        self.graph_generation()
        return self.trajet

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