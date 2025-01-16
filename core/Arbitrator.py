# arbitrator.py

from .models import *

class Arbitrator:
    '''
    Arbitrator class counts the score of a solution.

    Attributes:
        score (int): The score of the solution.
        coverage_map (list[list[int]]): The coverage map of the solution.
        target_cells (list[Vector3]): The list of target cells.
        coverage_radius (int): The coverage radius of the balloons.
    '''
    def __init__(self, data_model: DataModel):
        '''
        The constructor for Arbitrator class.

        Args:
            width (int): The width of the grid.
            height (int): The height of the grid.
            target_cells (list[Vector3]): The list of target cells.
            coverage_radius (int): The coverage radius of the balloons.
        '''
        # Validate and initialize attributes
        if not isinstance(data_model.target_cells, list) or not all(isinstance(cell, Vector3) for cell in data_model.target_cells):
            raise TypeError("target_cells must be a list of Vector3 objects.")
        if not isinstance(data_model.coverage_radius, int) or data_model.coverage_radius < 0:
            raise ValueError("coverage_radius must be a non-negative integer.")

        self.score: int = 0
        self.target_cells: list[Vector3] = data_model.target_cells
        self.coverage_radius: int = data_model.coverage_radius

        width: int = data_model.cols
        height: int = data_model.rows

        # Initialize the coverage map
        if height > 0 and width > 0:
            self.coverage_map: list[list[int]] = [[0 for _ in range(width)] for _ in range(height)]
        else:
            raise ValueError(f"Invalid grid size: height={height}, width={width}. Both must be > 0.")
    
    def columndist(self, c1, c2) -> int:
        '''
        The function to calculate the distance between two columns.

        Args:
            c1 (int): The first column. 
            c2 (int): The second column.
            grid_width (int): The width of the grid.

        Returns:
            int: The distance between two columns.
        '''
        return min(abs(c1 - c2), self.get_grid_size()[1] - abs(c1 - c2))

    def is_covered(self, r, c, u, v) -> bool:
        '''
        The function to check if the target is covered by the balloon.

        Args:
            r (int): The row of the target.
            c (int): The column of the target.
            u (int): The row of the balloon.
            v (int): The column of the balloon.
            coverage_radius (int): The coverage radius of the balloon.

        Returns:
            bool: True if the target is covered by the balloon, False otherwise.
        '''
        return (r - u) ** 2 + self.columndist(c, v) ** 2 <= self.coverage_radius ** 2


    def turn_score(self, balloons: list[Vector3], debug: bool = False) -> int:
        '''
        The function to count the score of a solution for one turn.

        Args:
            balloons (list[vector]): The list of balloons. Vector3(x, y) where x is the row and y is the column.
            debug (bool) (optional): The flag to print debug information.

        Returns:
            int: The score of the solution.
        '''

        # Check if all arguments are provided correctly
        if not balloons or not self.target_cells or self.coverage_radius < 0:
            raise TypeError("Invalid arguments.")

        score = 0

        # Test for each target if it is covered by a balloon
        for target in self.target_cells:
            # Get radius
            u, v = target.x, target.y # Target coordinates
            for balloon in balloons:
                # Check if the target is covered by the balloon and the balloon is not at the ground
                if self.is_covered(balloon.x, balloon.y, u, v) and balloon.z != 0:
                    if debug:
                        print(f"Balloon at ({balloon.x}, {balloon.y}) covers target at ({u}, {v})")
                    score += 1
                    break
        return score

    def score_for_ballon(self, balloon: Vector3) -> int:
        '''
        The function to count the score of a solution for one balloon.

        Args:
            balloon (Vector3): The balloon. Vector3(x, y) where x is the row and y is the column.

        Returns:
            int: The score of the solution.
        '''
        score = 0
        for target in self.target_cells:
            u, v = target.x, target.y
            if self.is_covered(balloon.x, balloon.y, u, v) and balloon.z != 0:
                score += 1
        return score

    def print_coverage_map(self):
        '''
        The function to print the coverage map of the solution.
        '''
        for row in self.coverage_map:
            print('  '.join(map(str, row)))

    def get_score(self) -> int:
        '''
        The function to return the score of the solution.
        '''
        return self.score

    def get_coverage_map(self) -> list[list[int]]:
        '''
        The function to return the coverage map of the solution.
        '''
        return self.coverage_map
    
    def get_grid_size(self) -> tuple[int, int]:
        '''
        The function to return the grid size.

        Returns:
            tuple[int, int]: The grid [height, width].
        '''
        return len(self.coverage_map), len(self.coverage_map[0])