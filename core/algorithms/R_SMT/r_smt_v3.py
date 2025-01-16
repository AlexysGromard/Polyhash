import random
from core.models import DataModel,Vector3
from core.Arbitrator import Arbitrator
from time import *
import multiprocessing

class RSMTv3:
    def __init__(self, data: DataModel) -> None:
        """
        Constructor for RSMT class.

        Args:
            data (DataModel): Data model for the problem.
        """
        self.d = data

        #super().__init__(data)
        self.arbitrator = Arbitrator(data)
        self.d = data

    def compute(self, time=100):
        #self.arbitator = Arbitrator(data)

        #Tuning parameters
        self.param_time = time
        
        #Computing the path
        result = self._processMultiprocessing()

        #If the algorithm find a way, it return the path, else it restart the algorithm
        
        return result

    
    def _convertData():
        pass

    
    def _processMultiprocessing(self):
        
        import time
       
        #Stockage des positions des ballons
        loonsPos = []
        loonPaths = []
        score = 0

        for loon in range(self.d.num_balloons):
            start = time.time()
            self._buildCache(loonsPos)
            print(f"cache generation: {time.time() - start}")
            start = time.time()
            with multiprocessing.Pool(8) as pool:
                results = pool.starmap(self._findSolution, [(2, (self.d.turns, 
                                self.d.starting_cell,
                                loonsPos))
                                for _ in range(8)])
            
            loonsPos.append(results[0][1])
            loonPaths.append(results[0][2])
            
            for r in results:
               
                if r[3] > score and r[0] == True:
                    score = r[3]
                    loonsPos[loon] = r[1]
                    loonPaths[loon]  = r[2]
                    print(f"new Score: {score} at loon {loon}")
            print(f"loon generation: {time.time() - start}")
        
        for i in range(0):
            for loon in range(self.d.num_balloons):
                self._buildCache(loonsPos)
                with multiprocessing.Pool(8) as pool:
                    results = pool.starmap(self._findSolution, [(10, (self.d.turns, 
                                    self.d.starting_cell,
                                    loonsPos))
                                    for _ in range(8)])
            
                
                for r in results:
                    if r[3] > score:
                        score = r[3]
                        loonsPos[loon] = r[1]
                        loonPaths[loon]  = r[2]
                        print(f"new Score: {score} at loon {loon} at turn {i}")


        print(f"score: {score}")

        #Préparation du loonPaths
        print(loonPaths)
        loonPaths2 = [[] for _ in range(self.d.turns)]
        for row in loonPaths:
            for i in range(len(row)):
                loonPaths2[i].append(row[i])
        return loonPaths2

    def _findSolution(self, nb_try: int, args: tuple):
        r = self._addLoonTurn(args[0], args[1], args[2])
        score = r[3]
        loonPos = r[1]
        loonPath  = r[2]

        for _ in range(nb_try - 1):  
                r = self._addLoonTurn(args[0], args[1], args[2]) 
                if r[3] > score:
                    score = r[3]
                    loonPos = r[1]
                    loonPath  = r[2]
        return (True, loonPos, loonPath, score)
                



    def _addLoonTurn(self, turn: int, position: Vector3, loons: list[Vector3]) -> tuple[bool,  list[Vector3], list[int], int]:
        """Ajoute un tour à un ballon qui est en position @position
        Empêche le ballon de sortir de la map

        Args:
            turns (int): _description_
            position (Vector3): _description_
            loons (list[Vector3]): _description_

        Returns:
            tuple[bool, list[Vector3], list[int], int]: (etat, loon positions per turn, loon path (-1, 0, +1), score)
        """
        #Compute available altitude variation foreach balloon
        altVariations = self._availableAltitudes(position)
        
        #New balloon positions:
        newPos = False

        #Return state (in order to let the boucle work)
        nextStep = (False, None, 0) #(etat, path, score)

        while nextStep[0] == False:

              
            while newPos == False:

                if len(altVariations) ==  0:
                    #No available alt variation for this balloon
                    return (False, None, 0) #(etat, path, score)
                
                #Choosing a random correct alt variation for the balloon
                choosen = altVariations[random.randint(0, len(altVariations) - 1)]

                #Creating a new balloon and apply its alt variation
                newPos = position.copy()              
                newPos.z += choosen

                #Applying wind movement to the balloon:
                loonWindResult = True
                if newPos.z  > 0:
                    loonWindResult = self.d.updatePositionWithWind(newPos)

                #Checking if the balloon stay in the map:
                if not loonWindResult:
                    #Remove the alt variation because it creates a problem:
                    altVariations.remove(choosen)

            #Calculate the score:
            

            Newscore = self._turnScore(newPos, turn)         
          
            #Si c'est le dernier tour:
            if turn == 1:                   
                return (True, [newPos],[choosen], Newscore)                   
            else:
                
                #On n'a pas encore fini: on explore la suite
                nextStep = self._addLoonTurn(turn - 1, newPos, loons)
              
                #Si le next est bloqué à cause d'un ballon, on suppr l'alt change du ballon:
                if nextStep[0] == False:
                    altVariations.remove(choosen)
        

        return (True, [position] + nextStep[1], [choosen] +  nextStep[2], Newscore + nextStep[3]) 
    
    def _availableAltitudes(self, place: Vector3) -> list[int]:
        """Return an array of correct altitudes variation for a balloon.
            Buil to avoid Alt <= 0 or Alt > maxAltitude.
        Args:
            place (Vector3): Balloon's position (only Z is used)
        Returns:
            list[int]: list of -1,0,1 with only correct altitudes variations
        """

        correct = []
        if place.z == 0:
            return [0,1]
        for i in range(-1, 2):
            if 0 < place.z + i <= self.d.altitudes:
                correct.append(i)
        return correct
    
    def _turnScore(self, balloon: Vector3, turn) -> int:
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
        coverage_radius_sq = self.d.coverage_radius ** 2
        grid_width = self.d.cols

        score = 0

        # Test for each target if it is covered by a balloon
        for target in self.cache_uncoveredCells[0 - turn]:
            # Get radius
            u, v = target.x, target.y # Target coordinates
            
            
            # Check if the balloon altitude is not 0
            if balloon.z != 0:
                    
                # Check if the target is covered by the balloon
                if is_covered(balloon.x, balloon.y, u, v):
                    
                    score += 1
        return score + self.cache_score[0 - turn]

    def _buildCache(self, balloonsPositions: list[list[Vector3]]):
        if len(balloonsPositions) == 0:
            self.cache_uncoveredCells = [self.d.target_cells for _ in range(self.d.turns)]
            self.cache_score = [0 for _ in range(self.d.turns)]
            return
        
        #Cache varialbes:
        self.cache_score = []
        self.cache_uncoveredCells = []

        data = []
        for i in range(7):
            data.append((i, i * (self.d.turns // 8), (i  +1) * (self.d.turns // 8), balloonsPositions))

        data.append((7, 7 * (self.d.turns // 8), self.d.turns, balloonsPositions))

        with multiprocessing.Pool(8) as pool:
                results = pool.starmap(self._buildCacheProccess, data)
        
        for i in range(8):
            for r in results:
                if r[0] == i:
                    self.cache_score+= r[1]
                    self.cache_uncoveredCells += r[2]
                
   
    def _buildCacheProccess(self, id: int, fromTour: int, toTour: int, balloonsPositions: list[list[Vector3]]):
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
        coverage_radius_sq = self.d.coverage_radius ** 2
        grid_width = self.d.cols      

        cache_score = []
        cache_uncoveredCells = []
        
        for tour in range(fromTour, toTour):
            uncoveredCells = []
         
            score = 0
    
            # Test for each target if it is covered by a balloon
            for target in self.d.target_cells:
                # Get radius
                u, v = target.x, target.y # Target coordinates
                isCovered = False
                for balloon in balloonsPositions:
                    # Check if the balloon altitude is not 0
                    if balloon[tour].z != 0:
                    
                        # Check if the target is covered by the balloon
                        if is_covered(balloon[tour].x, balloon[tour].y, u, v):                    
                            score += 1
                            isCovered = True
                            
                            break
                if not isCovered:
                    uncoveredCells.append(target)
            cache_score.append(score)
            cache_uncoveredCells.append(uncoveredCells)
        return (id, cache_score, cache_uncoveredCells)
           