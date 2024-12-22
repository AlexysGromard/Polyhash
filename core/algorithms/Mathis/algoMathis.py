# IMPORTS
import random

# import local
from ...models import DataModel,Vector3
from ...utils import DebugPrinter
from ..Algorithm import Algorithm

class AlgoMathis(Algorithm):
    """
    Algorithme de Mathis

    Attributes:
        data (DataModel): data of the problem
        trajet (list[list[int]]): order of the balloons' movements
    """
    
    def __init__(self, data: 'DataModel') -> None:
        """
        Constructeur de la classe AlgoMathis

        Args:
            data (DataModel): _description_
        """
        super().__init__(data)


    def compute(self) -> list[list[int]]:
        """
        Compute the trajectory of the balloons.

        Returns:
            list[list[int]]: order of the balloons' movements
        """

        error = self._process()
        i = 0
        # Tant que l'erreur n'est pas résolue et que le nombre d'itérations n'est pas dépassé
        while not error  and i < 1000:
            error = self._process()
            i+=1
        
        return self.trajet

    def _convert_data(self) -> None:
        """
        Convert the data of the problem to a format usable by the algorithm.
        """
        pass

    def _process(self) -> bool:
        """
        Compute the trajectory of the balloons.

        Returns:
            bool: True if the trajectory is computed, False otherwise
        """

        #Stocke les positions des ballons
        balloons = [self.data.starting_cell.copy() for _ in range(self.data.num_balloons)]

        #Boucle principale
        for turn in range(self.data.turns):
            
            #Stocke la ligne des variations de positions des ballons
            trajetRow = []

            for balloon in balloons:
                DebugPrinter.debug(f"{turn}:({balloon.x}, {balloon.y}, {balloon.z})")
                #Changement altitude
                altChange = self.__randomAlt( balloon)

               
                old = balloon.z
                balloon.z+= altChange

                # Mise à jour de la position
                is_in = self.data.updatePositionWithWind(balloon)
                
                # Si le ballon n'est pas dans la carte
                if not is_in : 
                    i = 0
                    
                    # Tant que le ballon n'est pas dans la carte
                    while i < 100:
                        i+= 1
                        
                        
                        balloon.z = old
                        altChange = self.__randomAlt( balloon)           
                        balloon.z+= altChange
                        is_in= self.data.updatePositionWithWind(balloon)
                        
                        # Si le ballon est dans la carte on sort de la boucle
                        if is_in :
                           i = 10000
                        
                    return False
                

                
                
                # Ajout de la variation d'altitude pour le ballon
                trajetRow.append(altChange)
                DebugPrinter.debug(f"{turn}:({balloon.x}, {balloon.y}, {balloon.z})")
                
            # Ajout de la ligne des variations de positions des ballons pour ce tour
            self.trajet.append(trajetRow)
        return True
    
    def __randomAlt(self, place: 'Vector3') -> int:
        """Calculate a CORRECT random variation of altitude for the balloon. 

        Args:
            d (DataModel): DataModel (to do not exceed max alt)
            place (Vector3): actual position of the balloon (just the Z coord. is used)

        Returns:
            int: -1|0|1 Correct altitude variation for this balloon (can not be 0 or superior to the max alt).
        """
        correct = []
        for i in range(-1, 2):
            if 0 < place.z + i < self.data.altitudes:
                correct.append(i)
        return correct[random.randint(0, len(correct) - 1)]

