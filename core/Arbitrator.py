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
    def __init__(self, width: int, height: int, target_cells: list[Vector3], coverage_radius: int):
        '''
        The constructor for Arbitrator class.

        Args:
            width (int): The width of the grid.
            height (int): The height of the grid.
            target_cells (list[Vector3]): The list of target cells.
            coverage_radius (int): The coverage radius of the balloons.
        '''
        self.score: int = 0
        self.target_cells = target_cells
        self.coverage_radius = coverage_radius

        # Initialize the coverage map
        if height > 0 and width > 0:
            self.coverage_map: list[list[int]] = [[0 for _ in range(width)] for _ in range(height)]
        else:
            raise ValueError(f"Invalid grid size: height={height}, width={width}. Both must be > 0.")

    def turn_score(self, balloons: list[Vector3], debug: bool = False) -> int:
        '''
        The function to count the score of a solution for one turn.

        Args:
            balloons (list[vector]): The list of balloons. Vector3(x, y) where x is the row and y is the column.
            debug (bool) (optional): The flag to print debug information.

        Returns:
            int: The score of the solution.
        '''
        def columndist(c1, c2, grid_width) -> int:
            '''
            The function to calculate the distance between two columns.

            Args:
                c1 (int): The first column. 
                c2 (int): The second column.
                grid_width (int): The width of the grid.

            Returns:
                int: The distance between two columns.
            '''
            return min(abs(c1 - c2), grid_width - abs(c1 - c2))

        def is_covered(r, c, u, v, coverage_radius) -> bool:
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
            return (r - u) ** 2 + columndist(c, v, self.get_grid_size()[1]) ** 2 <= coverage_radius ** 2

        # Check if all arguments are provided correctly
        if not balloons or not self.target_cells or self.coverage_radius < 0:
            raise TypeError("Invalid arguments.")

        score = 0

        # Test for each target if it is covered by a balloon
        for target in self.target_cells:
            # Get radius
            u, v = target.x, target.y # Target coordinates
            for balloon in balloons:
                r, c = balloon.x, balloon.y # Balloon coordinates
                # Check if the target is covered by the balloon
                if is_covered(r, c, u, v, self.coverage_radius):
                    if debug:
                        print(f"Balloon at ({r}, {c}) covers target at ({u}, {v})")
                    score += 1
                    break
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