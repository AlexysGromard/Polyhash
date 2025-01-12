# bfs.py

from collections import deque

from ...models import DataModel,Vector3
from ...utils import DebugPrinter
from ..Algorithm import Algorithm

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

    def graph_generation(self) -> list[list[int]]:
        """
        Generate the graph of the problem

        Returns:
            list[list[int]]: graph of the problem
        """
        graph = list()
        queue = deque()
        queue.append(Vector3(0, 0, 1))
        visited = list()

        while queue:
            # Ajout a la queue les autres cases de l'altitude si elles ne sont pas visitées
            current = queue.popleft()
            visited.append(current)

            # Vérifier les cases de l'altitude
            for i in range(1, self.data.cols):
                if Vector3(current.x, current.y, i) not in visited:
                    # Ajout a la queue les autres cases de l'altitude si elles ne sont pas visitées
                    queue.append(Vector3(current.x, current.y, i))
                    # Ajouter l'arete au graphe
                    graph.append([current, Vector3(current.x, current.y, i)])

            # Ajouter l'arete au graphe entre la case actuelle et les cases ou il peut aller avec le vent
            wind = self.data.wind_grids[current.x][current.y][current.z]
            graph.append([current, Vector3(current.x + wind.x, current.y + wind.y, current.z + wind.z)])

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