import random
from core.models import DataModel,Vector3
from core import Arbitrator
from time import *
import multiprocessing

class RSMTv2:
    def __init__(self, data: DataModel) -> None:
        """
        Constructor for RSMT class.

        Args:
            data (DataModel): Data model for the problem.
        """
        self.d = data

        #super().__init__(data)
        self.arbitator = Arbitrator(data)
        self.d = data

    def compute(self, time=100):
        #Tuning parameters
        self.param_time = time
        
        #Computing the path
        result = self._processMultiprocessing()

        #If the algorithm find a way, it return the path, else it restart the algorithm
        if result[0] == True:
            return result[1]
        
        #The algo didn't find a path, so let's create another algo
        return self.compute()

    
    def _convertData():
        pass

   
    def _processMultiprocessing(self):
        """Fonctionnement de l'algo: cherche (aléatoirement) un meilleur path pour les X premiers
        tours. Ensuite, cherche le meilleur path pour les X tours suivant... Fonctionnement par bloc

        Returns:
           tuple: (etat: bool, path list(list(int)), balloon_pb: int, score: int, listeScore list(int))
        """
        
        
        #Stockage du résultat du path en cours
        fullPath = [True, [],  None, 0,None, [Vector3(self.d.starting_cell.x, self.d.starting_cell.y, 0) for i in range(self.d.num_balloons)]]
        
        #Calcul du pas (les X tours par bloc)
        tours = self.d.turns
        pas = 25
        if tours < 10:
            pas = 12
        elif tours < 30:
            pas = 10
        elif tours < 100 :
            pas = 20

        #Tableau du nombre de tour et temps accordé pour chaque bloc de calcul (en fonction du pas)
        tab = [[pas, self.param_time / (tours / pas)] for _ in range(int(tours / pas) - 1)]

        #On vérifie qu'on a le bon nombre de tour:
        toAdd = tours
        for nbTours, _ in tab:
            toAdd -= nbTours
        tab.append((toAdd,  self.param_time / (tours / pas)))
        
        #On lance les tours de blocs (doit faire {nbTour} tours avec un temps max de {temps})
        for nbTour, temps in tab:

            best = [False, 0, 0, 0, []]
            average = 0
            #Compute a first random solution (the actual best-one)
            for _ in range(20):
                with multiprocessing.Pool(16) as pool:
                    results = pool.starmap(self._explore, [(nbTour, 
                                    fullPath[5],
                                    [0 for _ in  range(self.d.turns)], 
                                    0) for _ in range(8)])
                
                
                for r in results:
                   
                    average += r[3]
                    if r[3] >= best[3]:
                        best = r
            average /= 240
            
            #Check if the exploration find a path (if False, the previous 
            # chunk was wrong: there isn't any way to contiune the path without 
            # having a loon out of the map)
            if best[0] == False:
                print("process dies:")
                return (0, 0, 0, 0, 0)
            

            print(f"Our best is: {best[3]}, and we try: {8} times. Average is: {average}")

            #Adding the chunk to the fullPath
            fullPath[1] = fullPath[1] + best[1]
            fullPath[3]+= best[3]
            fullPath[5] = best[5]
        print(f"Score is: {fullPath[3]}")
        return fullPath

    def _explore(self, turn: int, balls: list[Vector3], best: list[int], score: int, confirmTest = False) -> tuple[bool, list[list[int]], int, int, list[int]]:
        """ Explore un nouveau tour en fonction de la position des ballons et
        du nombre de tour restant.

        Args:
            turn (int): Nb de tours restants
            balls (list[Vector3]): Liste de vector3 avec la position des ballons
            best (list[int]): les scores par tours du meilleur algo trouvé actuellemnt
            score (int): Score actuel (au tour n-1 donc)
            confirmTest (bool) : vrai si l'algo est lancé pour tester les 10 prochains tours (sinon, il vérifiera que l'on peut avancer d'au moins 10 tours)

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
                    loonWindResult = True
                    if newBalls[i].z  > 0:
                        loonWindResult = self.d.updatePositionWithWind(newBalls[i])

                    #Checking if the balloon stay in the map:
                    if not loonWindResult:
                        #Remove the alt variation because it creates a problem:
                        altVariations[i].remove(choosen[i])
                        newBalls[i] = False
           
            #Calculate the score:
            Newscore = score + self.arbitator.turn_score(newBalls)    
          
            #Si c'est le dernier tour:
            if turn == 1:

                if confirmTest == True:
                   
                    return (True, [choosen], None, Newscore, [Newscore], newBalls)
                
                else:
                    
                    #Check that we will be able to move the loon at least 8 turns (avoid to be blocked)
                    tester = self._explore(8, newBalls, best, Newscore, True)
                   

                    if tester[0] == True:
                        #We can move all the loon during 8 turns: we return the path
                        return (True, [choosen], None, Newscore, [Newscore], newBalls)
                    else: 
                        #A loon quit the map during the next 8 turns: we remove this alt variation and find another combination.
                        altVariations[tester[2]].remove(choosen[tester[2]])               
            else:
                
                #On n'a pas encore fini: on explore la suite
                nextStep = self._explore(turn -1, newBalls, best, Newscore, confirmTest)
              
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