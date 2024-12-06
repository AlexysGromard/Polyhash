# arbitator.py

class Arbitator:
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

    def turn_score(self, balloons: list[list[int]]) -> int:
        '''
        The function to count the score of a solution.

        Args:
            balloons (list[list[int]]): The list of balloons.
        '''
        return
    
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