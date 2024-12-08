import random
from core.models import DataModel,Vector3

class AlgoMathis:

    def compute(self, data: 'DataModel'):
        d = self.process(data)
        while d == False:
            d = self.process(data)
        return d

    def __convertData(self):
        pass

    def process(self, d:' DataModel'):

        #Stocke l'historique
        trajet = []

        #Stocke les positions des ballons
        balloons = [Vector3(d.starting_cell.x, d.starting_cell.y, 0) for i in range(d.num_balloons)]

        #Boucle principale
        for turn in range(d.turns):
            
            #Stocke la ligne des variations de positions des ballons
            trajetRow = []

            for balloon in balloons:
                print(f"{turn}:({balloon.x}, {balloon.y}, {balloon.z})")
                #Changement altitude
                altChange = self.randomAlt(d, balloon)

               
                old = balloon.z
                balloon.z+= altChange

                b = self.nextPlace(d, balloon)
                if b == False:
                    i = 0
                    while i < 100:
                        i+= 1
                        
                        balloon.z = old
                        altChange = self.randomAlt(d, balloon)           
                        balloon.z+= altChange
                        b = self.nextPlace(d, balloon)
                        if b != False:
                           i = 10000
                        
                    return False
                balloon.x = b.x
                balloon.y = b.y
                balloon.z = b.z
                trajetRow.append(altChange)
                print(f"{turn}:({balloon.x}, {balloon.y}, {balloon.z})")
                
            
            trajet.append(trajetRow)
        return trajet
    
    def randomAlt(self,d: 'DataModel', place: 'Vector3') -> int:
        """Calculate a CORRECT random variation of altitude for the balloon. 

        Args:
            d (DataModel): DataModel (to do not exceed max alt)
            place (Vector3): actual position of the balloon (just the Z coord. is used)

        Returns:
            int: -1|0|1 Correct altitude variation for this balloon (can not be 0 or superior to the max alt).
        """
        correct = []
        for i in range(-1, 2):
            if 0 < place.z + i < d.altitudes:
                correct.append(i)
        return correct[random.randint(0, len(correct) - 1)]

    def nextPlace(self, d: 'DataModel', place: 'Vector3') : 
        """Compute the new position of the balloon after the wind.

        Args:
            d (DataModel): DataModel in order to get the winds.
            place (Vector3): Actual position of the balloon (Z coord. matter)

        Returns:
            Vector3 | False: Return the new position of the balloon OR false if the balloon quit the grid.
        """
        

        #Check si l'altitude est correcte
        if place.z > d.altitudes:
            return False
        
        
        #Changement de position
        wind = d.wind_grids[place.z - 1][place.x][place.y]
        new = Vector3(
            place.x +wind.x,
            place.y +wind.y,
            place.z +wind.z,
        )
        new.y = new.y % d.cols

        #Check si le ballon ne sort pas en haut / en bas
        
        if new.x < 0 or new.x >= d.rows:
           
            return False
        
        return new