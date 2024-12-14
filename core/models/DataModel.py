from dataclasses import dataclass
from typing import List
from .Vector3 import Vector3

@dataclass
class DataModel:
    """
    Class : DataModel
    A data class to represent and manage the data for the Project Loon simulation problem.

    Attributes :
        rows (int) : Number of rows in the grid.
        cols (int) : Number of columns in the grid.
        altitudes (int) : Number of altitudes in the grid.
        num_targets (int) : Number of targets in the grid.
        coverage_radius (int) : The radius of the coverage circle.
        num_balloons (int) : Number of balloons in the grid.
        turns (int) : Number of turns in the simulation.
        starting_cell (Tuple[int, int]) : The starting cell of the simulation.
        target_cells (List[Tuple[int, int]]) : The target cells of the simulation.
        wind_grids (List[List[List[Tuple[int, int]]]]) : The wind vetor grids of the simulation.

    Methods:
        extract_data: Extracts the data from the challenge file and returns a DataModel object.
    """

    def __init__(self, rows: int = 0, cols: int = 0, altitudes: int = 0, num_targets: int = 0, coverage_radius: int = 0, num_balloons: int = 0, turns: int = 0, starting_cell: Vector3 = None, target_cells: list[Vector3] = None, wind_grids: list[List[list[Vector3]]] = None):
        self.rows = rows
        self.cols = cols
        self.altitudes = altitudes
        self.num_targets = num_targets
        self.coverage_radius = coverage_radius
        self.num_balloons = num_balloons
        self.turns = turns
        self.starting_cell = starting_cell if starting_cell is not None else Vector3(0, 0, 0)
        self.target_cells = target_cells if target_cells is not None else []
        self.wind_grids = wind_grids if wind_grids is not None else []

    rows: int
    cols: int 
    altitudes: int 
    num_targets: int 
    coverage_radius: int
    num_balloons: int 
    turns: int
    starting_cell: Vector3
    target_cells: list[Vector3] 
    wind_grids: list[List[list[Vector3]]] 

    @classmethod
    def extract_data(cls, file_path: str) -> "DataModel":
        """
        Class Method : extract_file
        Extracts the data from the challenge file and returns a DataModel object.

        Parameters :
            file_path (str) : The path to the challenge file.

        Returns :
            DataModel : The DataModel object.
        
        Example data file :
            3 5 3 # rows cols altitudes
            2 1 1 5 # target_count cov_radius ballon_count turn_count
            1 2 # launching coordinates
            0 2 # coords target 0
            0 4 # coords target 1
            0 1 0 1 0 1 0 1 0 1 # wind grid
            0 1 0 1 0 1 0 1 0 1
            0 1 0 1 0 1 0 1 0 1
            -1 0 -1 0 -1 0 -1 0 -1 0
            -1 0 -1 0 -1 0 -1 0 -1 0
            -1 0 -1 0 -1 0 -1 0 -1 0
            0 1 0 1 0 1 0 2 0 1
            0 2 0 1 0 2 0 3 0 2
            0 1 0 1 0 1 0 2 0 1
 
        """
        try:
            with open(file_path, 'r') as file:
                 # Parse first line (rows, cols, altitudes)
                rows, cols, altitudes = map(int, file.readline().strip().split('#')[0].split())

                # Parse second line (num_targets, coverage_radius, balloons, turns)
                num_targets, coverage_radius, balloons, turns = map(int, file.readline().strip().split('#')[0].split())

                # Parse third line (starting_cell)
                starting_cell_data = list(map(int, file.readline().strip().split('#')[0].split()))
                starting_cell = Vector3(*starting_cell_data, z=0)  # Default altitude is 0

                # Parse target cells
                target_cells = [
                    Vector3(*map(int, file.readline().strip().split('#')[0].split()), z=0)
                    for _ in range(num_targets)
                ]

                # Parse wind grids
                wind_grids = []
                for _ in range(altitudes):
                    altitude_grid = []
                    for _ in range(rows):
                        row = file.readline().strip().split()
                        # Convert pairs of values into Vector3 objects
                        altitude_grid.append([
                            Vector3(int(row[i]), int(row[i + 1]), z=0)
                            for i in range(0, len(row), 2)
                        ])
                    wind_grids.append(altitude_grid)

            return cls(
                rows=rows,
                cols=cols,
                altitudes=altitudes,
                num_targets=num_targets,
                coverage_radius=coverage_radius,
                num_balloons=balloons,
                turns=turns,
                starting_cell=starting_cell,
                target_cells=target_cells,
                wind_grids=wind_grids,
            )

        except Exception as e:
            raise ValueError(f"Error reading file: {e}")
