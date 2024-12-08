# arbitrator.py

from .models import *

class Arbitrator:
    '''
    Arbitrator class counts the score of a solution.

    Attributes:
        score (int): The score of the solution.
        coverage_map (list[list[int]]): The coverage map of the solution.
    '''
    def __init__(self, height: int, width: int):
        '''
        The constructor for Arbitrator class.

        Args:
            height (int): The height of the grid.
            width (int): The width of the grid.
        '''
        self.score: int = 0

        # Initialize the coverage map
        if height > 0 and width > 0:
            self.coverage_map: list[list[int]] = [[0 for _ in range(width)] for _ in range(height)]
        else:
            raise ValueError(f"Invalid grid size: height={height}, width={width}. Both must be > 0.")

    def turn_score(self, balloons: list[Vector3], targets: list[Vector3], coverage_radius: int, debug: bool = False) -> int:
        '''
        The function to count the score of a solution for one turn.

        Args:
            balloons (list[vector]): The list of balloons.
            targets (list[vector]): The list of targets.
            coverage_radius (int) (optional): The coverage radius of the balloon.
            debug (bool) (optional): The flag to print debug information.
        '''
        def columndist(c1, c2, grid_width):
            return min(abs(c1 - c2), grid_width - abs(c1 - c2))

        def is_covered(r, c, u, v, coverage_radius):
            '''
            The function to check if the target is covered by the balloon.

            Args:
                r (int): The row of the target.
                c (int): The column of the target.
                u (int): The row of the balloon.
                v (int): The column of the balloon.
                coverage_radius (int): The coverage radius of the balloon.
            '''
            return (r - u) ** 2 + columndist(c, v, self.get_grid_size()[1]) ** 2 <= coverage_radius ** 2

        # Check if all arguments are provided correctly
        if not balloons or not targets or coverage_radius < 0:
            raise TypeError("Invalid arguments.")

        score = 0

        # Test for each target if it is covered by a balloon
        for target in targets:
            # Get radius
            u, v = target.x, target.y # Target coordinates
            for balloon in balloons:
                r, c = balloon.x, balloon.y # Balloon coordinates
                # Check if the target is covered by the balloon
                if is_covered(r, c, u, v, coverage_radius):
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