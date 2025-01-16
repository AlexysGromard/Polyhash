from .models import *

class ArbitratorOpti:
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
     
        self.data = data_model

    def turn_score(self, balloons: list[Vector3], debug: bool = False) -> int:
        '''
        The function to count the score of a solution for one turn.

        Args:
            balloons (list[vector]): The list of balloons. Vector3(x, y) where x is the row and y is the column.
            debug (bool) (optional): The flag to print debug information.

        Returns:
            int: The score of the solution.
        '''
        def columndist(c1, c2) -> int:
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

        def is_covered(r, c, u, v) -> bool:
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
            return (r - u) ** 2 + columndist(c, v) ** 2 <= coverage_radius_sq
        
        # Pre-calculate constants
        coverage_radius_sq = self.data.coverage_radius ** 2
        grid_width = self.data.cols

        #Generate loons grid
        loonGrid = self.sortLoons(balloons)
        sizeX = len(loonGrid)
        sizeY  = len(loonGrid[0])

        score = 0

        # Test for each target if it is covered by a balloon
        for target in self.data.target_cells:
            # Get radius
            u, v = target.x, target.y # Target coordinates
            
            #Look where might be the loons
            caseX = u // self.data.coverage_radius
            caseY = v // self.data.coverage_radius
            if caseX == sizeX:
                caseX -= 1
            if caseY == sizeY:
                caseY -= 1           
            loons = []
            loons += loonGrid[caseX][caseY]
            loons += loonGrid[(caseX + 1) % sizeX][caseY]
            loons += loonGrid[caseX - 1][caseY]
            loons += loonGrid[caseX][caseY - 1]
            loons += loonGrid[caseX][(caseY + 1) % sizeY]
            loons += loonGrid[caseX - 1][caseY - 1]
            loons += loonGrid[caseX - 1][(caseY + 1) % sizeY]
            loons += loonGrid[(caseX + 1) % sizeX][caseY - 1]
            loons += loonGrid[(caseX + 1) % sizeX][(caseY + 1)  % sizeY]
            

            for balloon in loons:
                # Check if the balloon altitude is not 0
                if balloon.z == 0:
                    break
                # Check if the target is covered by the balloon
                if is_covered(balloon.x, balloon.y, u, v):
                    score += 1
                    break
        return score

    def sortLoons(self, loons: list[Vector3]) -> list[list[Vector3]]:
        '''
        Generate a grid where loons are sorted by area of with/height = coverRadius
        Args:
            loons (list[vector]): The list of balloons. Vector3(x, y) where x is the row and y is the column.
            
        Returns:
            list[list[Vector3]]: The grid with the sorted loons.
        '''


        x = self.data.rows // self.data.coverage_radius
        y = self.data.cols // self.data.coverage_radius
        grid = [[[] for i in range(0, y)] for _ in range(0, x)]

        for loon in loons:
            #Loon position in grid
            caseX = loon.x // self.data.coverage_radius      
            caseY = loon.y // self.data.coverage_radius          
            if caseX == x:
                caseX -= 1
            if caseY == y:
                caseY -= 1
            
            #Adding balloon to grid
            grid[caseX][caseY].append(loon)

        return grid 