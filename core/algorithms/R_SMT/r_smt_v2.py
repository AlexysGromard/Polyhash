import random
from core.models import DataModel,Vector3
#from core.Arbitrator import Arbitrator
from testMR_Arb_opti import Arbitrator
from time import *
import multiprocessing

class RSMTv2:
    def compute(self, data: 'DataModel'):
        self.d = data
        self.arbitator = Arbitrator(data)  
        
        return self._randomProcess()
    
    def _convertData():
        pass

    def _process(self):
        #On compute un premier tour les 10 prochains
        
        fullPath = [True, [],  None, 0,None, [Vector3(self.d.starting_cell.x, self.d.starting_cell.y, 0) for i in range(self.d.num_balloons)]]
        for i in range(2):
            start = time()
            best = self._explore(10, 
                             fullPath[5],
                             [0 for _ in  range(self.d.turns)], 
                             0)#[1]

            cnt = 1
            while time() - start < 20:
                cnt +=  1
                r = self._explore(10, 
                               fullPath[5],
                                best[4], 
                                0)
                if r[3] > best[3]:
                    best = r
            print(f"Our best is: {best[3]}, and we try: {cnt} times")
            fullPath[1] = fullPath[1] + best[1]
            fullPath[3]+= best[3]
            fullPath[5] = best[5]
        return fullPath
    def tryes(self, tur, temps):
        useLess += 1
        start = time()
        best = self._explore(tur, 
                        self.fullPath[5],
                        [0 for _ in  range(self.d.turns)], 
                        0)#[1]

        cnt = 1
        while time() - start < temps:
            cnt +=  1
            r = self._explore(tur, 
                        self.fullPath[5],
                            best[4], 
                            0)
            if r[3] > best[3]:
                best = r
        if best[0] == False:     
            return (0, 0, 0, 0, 0)
        return best
        
    def _newProcess(self):
        #On compute un premier tourles 10 prochains
        id = random.randint(0,  10000)
        self.fullPath = [True, [],  None, 0,None, [Vector3(self.d.starting_cell.x, self.d.starting_cell.y, 0) for i in range(self.d.num_balloons)]]
        
        first = 200
        
        tab = [(10, 5), (10,5)]
        
        for tur, temps in tab:

            
            with multiprocessing.Pool(8) as pool:
                results = pool.map(self.tryes, [(tur, temps) for _ in range(8)])
            best = results[0]
            for essaie in results:
                if essaie[3] > best[3]:
                    best = essaie
            print(f"Our best is: {best[3]}, and we try: {cnt} times id {id}")
            self.fullPath[1] = self.fullPath[1] + best[1]
            self.fullPath[3]+= best[3]
            self.fullPath[5] = best[5]
        
        
        return self.fullPath

    def _randomProcess(self):
        #On compute un premier tour les 10 prochains
        id = random.randint(0,  10000)
        fullPath = [True, [],  None, 0,None, [Vector3(self.d.starting_cell.x, self.d.starting_cell.y, 0) for i in range(self.d.num_balloons)]]
        
       
        
        tab = [(4, 2) for _ in range(10)]
        for tur, temps in tab:
            start = time()
            best = self._explore(tur, 
                             fullPath[5],
                             [0 for _ in  range(self.d.turns)], 
                             0)#[1]

            cnt = 1
            while time() - start < temps:
                cnt +=  1
                r = self._explore(tur, 
                               fullPath[5],
                                best[4], 
                                0)
                if r[3] > best[3]:
                    #Check si on peut continuer d'avancer:
                    tester = self._explore(5, best[5], best[4], 0)
                    if tester[1] != False:
                        best = r
            if best[0] == False:
                
                return (0, 0, 0, 0, 0)
            print(f"Our best is: {best[3]}, and we try: {cnt} times id {id}")
            fullPath[1] = fullPath[1] + best[1]
            fullPath[3]+= best[3]
            fullPath[5] = best[5]
        return fullPath

    def _explore(self, turn: int, balls: list[Vector3], best: list[int], score: int) -> tuple:
        """ Explore un nouveau tour en fonction de la position des ballons et
        du nombre de tour restant.

        Args:
            turn (int): Nb de tours restants
            balls (list[Vector3]): Liste de vector3 avec la position des ballons
            best (list[int]): les scores par tours du meilleur algo trouvé actuellemnt
            score (int): Score actuel (au tour n-1 donc)

        Returns:
            tuple: (etat: bool, path list(list(int)), balloon_pb: int, score: int, listeScore list(int))
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
                        return (False, None, int(i), 0, None) #(etat, path, ball causing the problem, score)
                    
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
            Newscore = score + self.arbitator.turn_score(newBalls)

          
            #Si c'est le dernier tour:
            if turn == 1:
                return (True, [choosen], None, Newscore, [Newscore], newBalls)
            
            #On n'a pas encore fini: on explore la suite
            nextStep = self._explore(turn -1, newBalls, best, Newscore)

            #Si le next est bloqué à cause d'un ballon, on suppr l'alt change du ballon:
            if nextStep[0] == False:
                altVariations[nextStep[2]].remove(choosen[nextStep[2]])
        

        return (True, [choosen] +  nextStep[1], None, nextStep[3], [Newscore] + nextStep[4], nextStep[5]) #(etat, path, ball causing pb, score)
    
    
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
