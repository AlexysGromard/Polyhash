import random

class Vector3:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        return NotImplemented

    def __iadd__(self, other):
        if isinstance(other, Vector3):
            self.x += other.x
            self.y += other.y
            self.z += other.z
            return self
        return NotImplemented

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z


class AlgoMathis:

    def compute(self, data: 'DataModel'):
        return self.process(data)

    def __convertData(self):
        pass

    def process(self, d: 'DataModel'):

        #Stocke l'historique
        trajet = []

        #Stocke les positions des ballons
        balloons = [Vector3(d.startCell.x, d.startCell.y, 0) * d.nbBalloons]

        #Boucle principale
        for turn in range(d.turns):

            trajetRow = []

            for balloon in balloons:
                #Changement altitude
                altChange = self.randomAlt(d, balloon)

                trajetRow.append(altChange)

                balloon.z+= altChange

                balloon = self.nextPlace(d, balloon)
            trajet.append(trajetRow)
        return trajet
    
    def randomAlt(self,d: 'DataModel', place: Vector3) -> 'Vector3':
        """Retourne une altitude random correcte pour le ballon"""
        correct = []
        for i in range(-1, 3):
            if 0 < place.z + i < d.alts:
                correct.append(i)
        place.z += correct[random.randint(0, len(correct))]

    def nextPlace(self, d: 'DataModel', place: Vector3) -> Vector3 : 
        """
        Retourne la nouvelle place d'un ballon en fonction de sa position place(Vector3)
        et des vents présents dans d(DataModel)
        Retourne False si le ballon sort de l'écran.    
        """
        

        #Check si l'altitude est correcte
        if place.z > d.nbWinds:
            return False
        
        #Changement de position
        wind = d.winds[place.z][place.x][place.y]
        place += wind
        place.x = place.x % d.cols

        #Check si le ballon ne sort pas en haut / en bas
        if place.y < 0 or place.y >= d.rows:
            return False
        
        return place