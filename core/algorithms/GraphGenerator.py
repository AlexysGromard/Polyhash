from core import Arbitrator
from ..models import Vector3

class GraphGenerator:
    def __init__(self, data):
        """
        Initialize the GraphGenerator with data and an arbitrator.

        Args:
            data: Object containing the grid and wind data.
        """
        self.data = data
        self.arbitrator = Arbitrator(data)
        self.graph = {}

    def graph_generation(self) -> list[list[int]]:
        """
        Generate the graph of the problem, representing possible moves and their scores.

        Returns:
            A dictionary representing the graph where each node is a key, and edges with weights are stored as values.
        """
        print("Generating graph")
        self.graph = {}

        # Iterate over all positions in the 3D grid (rows, columns, altitudes)
        for row in range(self.data.rows):
            for col in range(self.data.cols):
                for alt in range(self.data.altitudes):
                    # Initialize the adjacency list for the current node
                    self.graph[(row, col, alt)] = []

                    # Retrieve wind vector at the current position and altitude
                    wind = self.data.wind_grids[alt][row][col]

                    # Calculate the new position based on the wind vector
                    new_row = row + wind.x
                    new_col = col + wind.y

                    # Check if the new position is within grid bounds
                    if new_row < 0 or new_row >= self.data.rows or new_col < 0 or new_col >= self.data.cols:
                        continue  # Skip invalid positions

                    # Get the score for moving to the new position
                    points = self.arbitrator.score_for_ballon(Vector3(new_row, new_col, alt))  # Edge weight

                    # Add the edge with its weight to the graph
                    self.graph[(row, col, alt)].append(((row, col, alt), points))

        print("Graph generated")
        return self.graph
