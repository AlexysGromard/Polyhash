import random
from core.models import DataModel,Vector3
from testMRArbitre import ArbitatorMR
class RSMT:
    def compute(self, data: 'DataModel'):
        self.d = data
        self.arbitator = ArbitatorMR(data)  
        
        return self._process()
    
    def _convertData():
        pass

    def _process(self):
        
        return self._explore(self.d.turns, 
                             [Vector3(self.d.starting_cell.x, self.d.starting_cell.y, 0) for i in range(self.d.num_balloons)],
                             [0 for _ in  range(self.d.turns)], 
                             #[1, 2, 3, 3, 4],
                             0)[1]

    def _explore(self, turn: int, balls: list[Vector3], best: list[int], score: int) -> tuple:
        """ Explore un nouveau tour en fonction de la position des ballons et
        du nombre de tour restant.

        Args:
            turn (int): Nb de tours restants
            balls (list[Vector3]): Liste de vector3 avec la position des ballons
            best (list[int]): les scores par tours du meilleur algo trouvé actuellemnt
            score (int): Score actuel (au tour n-1 donc)

        Returns:
            tuple: (etat: bool, path list(list(int)), balloon_pb: int, score: int)
        """


        #Compute available altitude variation foreach balloon
        altVariations = []
        for b  in balls:
            altVariations.append(self._availableAltitudes(b))
        
        #New balloons positions:
        newBalls = [False for _ in range(len(balls))]

        #Return state (in order to let the boucle work)
        nextStep = (False, None, 0, 0) #(etat, path, ball causing the problem, score)

        while nextStep[0] == False:

            #Alt variation choosen for this try (False or Vector3)
            choosen = [-10 for _ in range(len(balls))]

            newBalls = [False for _ in range(len(balls))]

            #Choosing a working alt variation for each balloon:
            for i in range(len(balls)):
                
                while newBalls[i] == False:

                    if len(altVariations[i]) ==  0:
                        #No available alt variation for this balloon
                        return (False, None, int(i), 0) #(etat, path, ball causing the problem, score)
                    
                    #Choosing a random correct alt variation for the balloon
                    choosen[i] = altVariations[i][random.randint(0, len(altVariations[i]) - 1)]

                    #Creating a new balloon and apply its alt variation
                    newBalls[i] = balls[i].copy()              
                    newBalls[i].z += choosen[i]

                    #Applying wind movement to the balloon:
                    if newBalls[i].z  > 0:
                        newBalls[i] = self._nextPlace(newBalls[i])

                    #Checking if the balloon stay in the map:
                    if newBalls[i] == False:
                        #Remove the alt variation because it creates a problem:
                        altVariations[i].remove(choosen[i])

            #Calculate the score:
            score += self.arbitator.turnScore(newBalls)

            #Smart part of the algo: check if the best found algo is better than this one
            """if len(best) - turn >=  5:
                if best[0 - turn - 5] > score:
                   return (False, False, False, False) #Complete stop signal
            """
            #Si c'est le dernier tour:
            if turn == 1:
                return (True, [choosen], None, score)
            
            #On n'a pas encore fini: on explore la suite
            nextStep = self._explore(turn -1, newBalls, best, score)

            #Si le next est bloqué à cause d'un ballon, on suppr l'alt change du ballon:
            if nextStep[0] == False:
                print(altVariations[nextStep[2]])
                print(choosen[nextStep[2]])
                print(f"------------------{nextStep[2]}")
                altVariations[nextStep[2]].remove(choosen[nextStep[2]])
        

        return (True, [choosen] +  nextStep[1], None, nextStep[3]) #(etat, path, ball causing pb, score)
    
    
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

    def _nextPlace(self, place: 'Vector3') : 
        """Compute the new position of the balloon after the wind.

        Args:
            d (DataModel): DataModel in order to get the winds.
            place (Vector3): Actual position of the balloon (Z coord. matter)

        Returns:
            Vector3 | False: Return the new position of the balloon OR false if the balloon quit the grid.
        """
        

        #Check si l'altitude est correcte
        if place.z  > self.d.altitudes:
            return False
        if place.z == 0:
            return place
        
        #Changement de position
        wind = self.d.wind_grids[place.z - 1][place.x][place.y]
        new = Vector3(
            place.x +wind.x,
            place.y +wind.y,
            place.z,
        )
        new.y = new.y % self.d.cols

        #Check si le ballon ne sort pas en haut / en bas
        
        if new.x < 0 or new.x >= self.d.rows:
            
            return False
        
        return new