import random
from core.models import DataModel,Vector3
from core import Arbitrator
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
        
        score = 0
        loons = [self.d.starting_cell.copy() for _ in range(self.d.num_balloons)]
        for row in result:
            for i in range(len(loons)):
                loons[i].z += row[i]
                self.d.updatePositionWithWind(loons[i])
            score += self.arbitrator.turn_score(loons)
        print(f"Computed score:  {score}")
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
            with multiprocessing.Pool(20) as pool:
                results = pool.starmap(self._findSolution, [(3, (self.d.turns, 
                                self.d.starting_cell,
                                loonsPos
                                ))
                                for _ in range(20)])
            
            loonsPos.append(results[0][1])
            loonPaths.append(results[0][2])
            
            for r in results:
               
                if r[3] > score and r[0] == True:
                    score = r[3]
                    loonsPos[loon] = r[1]
                    loonPaths[loon]  = r[2]
                    print(f"new Score: {score} at loon {loon}")
            print(f"loon generation: {time.time() - start}")
        start = time.time()
        t = 0
        while (time.time() - start) < 10:
            t+= 1
            for loon in range(self.d.num_balloons):
                
                with multiprocessing.Pool(20) as pool:
                    temp = loonsPos.pop(loon)
                    results = pool.starmap(self._findSolution, [(3, (self.d.turns, 
                                    self.d.starting_cell,
                                    loonsPos, score))
                                    for _ in range(20)])
                    loonsPos.insert(loon, temp)
                
                for r in results:
                    if r[3] > score:
                        score = r[3]
                        loonsPos[loon] = r[1]
                        loonPaths[loon]  = r[2]
                        print(f"new Score: {score} at loon {loon} at turn {t}")
                    elif r[3] * 1.02 > score:
                        if random.randint(0, 8) == 0:
                            score = r[3]
                            loonsPos[loon] = r[1]
                            loonPaths[loon]  = r[2]
                            print(f"new impureties Score: {score} at loon {loon} at turn {t}")



        print(f"score: {score}")

        #Préparation du loonPaths
        
        loonPaths2 = [[] for _ in range(self.d.turns)]
        for row in loonPaths:
            for i in range(len(row)):
                loonPaths2[i].append(row[i])
        return loonPaths2

   
    def _findSolution(self, nb_try: int, args: tuple) -> tuple[bool, list[Vector3], list[int], int]:
        """Essaie nb_try chemins et retourne le meilleur

        Args:
            nb_try (int): Nombre d'itérations
            args (tuple): arguments à passer à la  fonction _explore() pour qu'elle fonctionne

        Returns:
            tuple[bool, list[Vector3], list[int], int]: (etat, loonPosition, path, score)
        """
        
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
            loons (list[Vector3]): Position des autres ballons

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

            loonWindResult = False
            while loonWindResult == False:

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
            
            l = [loons[i][self.d.turns - turn] for i in range(len(loons))]
            Newscore = self.arbitrator.turn_score([newPos] + l) 
          
            #Si c'est le dernier tour:
            if turn == 1:                   
                return (True, [newPos],[choosen], Newscore)                   
            else:
                
                #On n'a pas encore fini: on explore la suite
                nextStep = self._addLoonTurn(turn - 1, newPos, loons)
              
                #Si le next est bloqué à cause d'un ballon, on suppr l'alt change du ballon:
                if nextStep[0] == False:
                    altVariations.remove(choosen)
                    
        

        return (True, [newPos] + nextStep[1], [choosen] +  nextStep[2], Newscore + nextStep[3]) 
    
    def _availableAltitudes(self, place: Vector3) -> list[int]:
        """Return an array of correct altitudes variation for a balloon.
            Buil to avoid Alt <= 0 or Alt > maxAltitude.
        Args:
            place (Vector3): Balloon's position (only Z is used)
        Returns:
            list[int]: list of -1,0,1 with only correct altitudes variations
        """

        if place.z == 0:
            return [0,1]
        if place.z == self.d.altitudes:
            return [-1, 0]
        return [-1, 0, 1] 