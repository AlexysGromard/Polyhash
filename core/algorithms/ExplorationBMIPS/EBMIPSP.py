# IMPORTS
import random
# import local 
from core.models import DataModel,Vector3
from ..Algorithm import Algorithm
from core.Arbitrator import Arbitrator
from ...utils import DebugPrinter
from .MultiProcessing import ParallelExecutor

# CLASS
class EBMIPSP(Algorithm) :
    
    # ATTRIBUTES
    def __init__(self, data) -> None:
        """
        Constructeur de la classe EBMIPS
        """
        super().__init__(data)
        
        self.num_sonde : int = 400 # self.data.num_balloons
        self.explored : list[list[int,list[int]]] = []
        self.nb_save_sonde : int = 10
        

        
    # METHODS
    def compute(self) -> list[list[int]]:
        """
        public
        compute est la méthode qui permet de lancer le calcul de l'algorithme


        Returns:
            list[list[int]]: liste des trajectoires des véhicules
        """
        self.trajet = self._process()
        return self.trajet
    
    def _convert_data(self) -> None:
        """
        protected
        _convert_data est la méthode qui permet de convertir les données du problème en un format utilisable par l'algorithme
        """
        pass
    
    def _process(self) -> list[list[int]]:
        """
        protected
        _process est la méthode qui permet de lancer le processus de calcul de l'algorithme
        
        Returns:
            list[list[int]]: liste des trajectoires des véhicules
        """
        import time
        print('start ParallelExecutor')
        start = time.time()

        
        # Lancer les explorations en parallèle
        explored_chunks = ParallelExecutor.execute_class(self, "_explore")
        print(f"end - {time.time() - start}")

        # Fusionner les résultats
        self.explored = [item for chunk in explored_chunks for item in chunk]
        print(f"nb_solution : {len(self.explored)}")
        
        self._explore_selection()
                   
        
        self._snake()
        
        return self.trajet
    
    
    
    def _explored_avg(self) -> list :
                # Calculer la moyenne de chaque sonde pour les x tours
        for i in range(self.num_sonde):
            self.explored[i][0] = self.explored[i][0] / self.data.turns
            
        return self.explored

    def _explore(self) -> list[tuple[int,list[int]]]:
        
        
        def generate_random_orders(vector: Vector3) -> int:
            """
            Generate random orders for the vector

            Args:
                vector (Vector3): The vector to change the orders of z
                
            Returns:
                int: orders for z
            """
            if vector.z <= 1 :
                return random.choice([0,1])
            elif vector.z == self.data.altitudes :
                return random.choice([-1,0])
            else:
                return random.choice([-1,0,1])
        
        def generate_orders(vector: Vector3, order) -> int:
            """
            Generate orders for the vector, ensuring the order is different from the given one.

            Args:
                vector (Vector3): The vector to change the orders of z
                order (int): The previous order to avoid repeating
            
            Returns:
                int: Orders for z that are different from the given one
            """
            if vector.z <= 1:
                return 0  # Si z est inférieur ou égal à 1, aucun mouvement n'est possible

            # Gérer les ordres en fonction du `order` précédent
            if vector.z == self.data.altitudes:
                return 0 if order != -1 else -1  # Si l'ordre précédent était -1, choisir 0, sinon choisir -1

            # Sinon, choisir un ordre parmi [-1, 0, 1], différent de l'`order`
            return { -1: 0, 0: 1, 1: 0 }[order]

        
        
        sondes = [
                    Vector3(self.data.starting_cell.x, self.data.starting_cell.y, 1) 
                    for _ in range(self.num_sonde)
                    ]
        
        cpt = 0
        arbitre = Arbitrator(self.data)
        
        # executer le premier tour
        for i in range(self.nb_save_sonde):
            # On fait un tour
            # On récupère les sondes
            self.data.updatePositionWithWind(sondes[i])
            
        # recuperer le resultat
        res = arbitre.turn_score(sondes)
        
        self.explored = [[res, [1], False] for _ in range(self.num_sonde)]
        
        nb_bounds = 0
        
        # On explore les sondes pendant x tours
        while cpt < self.data.turns -1 :
            # On fait un tour
            for place, sonde in enumerate(sondes):
                if not self.explored[place][2] :
                # On donne des ordres aleatoires pour chaque sondes entre (-1,0,1) mais si on touche l'alitude max ou min, on reduit les choix
                    order = generate_random_orders(sonde)
                    sonde.z += order
                    
                    is_in = self.data.updatePositionWithWind(sonde)
                    
                    #nb_essaie = 0
                    if not is_in :
                        self.explored[place][2] = not self.explored[place][2]

                        nb_bounds += 1
                    
                    else :

                        # moyenne des resultats
                        self.explored[place][0] += self.arbitre_sonde(sonde)
                        self.explored[place][1].append(order)
                    
            cpt += 1
        print(f'ok ? {nb_bounds}')

            
        self._explored_avg()
        
        # lance le trie
        self._explore_selection()
        
        
        return self.explored
            
    
    def _explore_selection(self):
        """
        protected
        _explore_selection est la méthode qui permet de choisir la meilleure sonde parmis les sondes explorées
        """
        # Filtrer les éléments où la troisième valeur est False
        filtered_explored = [item for item in self.explored if item[2] is False]

        # Trier les données par la première colonne (décroissant)
        self.explored = sorted(filtered_explored, key=lambda item: item[0], reverse=True)[:self.nb_save_sonde + 1]

        print(f'len de sonde save {len(self.explored)}')
        

        
        
    def _snake(self):
        """
        creer des chaine de ballon
        """
        
        def duplicate_and_modify(lst, gap: int) -> list :
            """
            Duplique une liste et modifie chaque duplication en retirant des éléments à la fin 
            et en ajoutant des zéros au début en fonction du pas donné.
            
            Args:
                lst (list): La liste originale.
                gap (int): Nombre d'éléments à retirer à chaque étape.
            
            Returns:
                list: Une liste contenant toutes les duplications modifiées.
            """
            # Crée une copie de la liste originale
            copy = lst[:]
            
            # Retourne la liste avec des zéros au début et les éléments retirés à la fin
            return [0] * gap + copy[:-gap]



        # nombre de pcaker

        nb = self.data.num_balloons // self.nb_save_sonde
        reste = self.data.num_balloons % self.nb_save_sonde  
        
        for i in range(self.nb_save_sonde):  # 10 sondes
            for j in range(nb):  # Nombre de duplications basées sur coverage_radius
                gap = self.data.coverage_radius * (j)
                if gap == 0 :
                    self.trajet.append(self.explored[i][1])
                else :
                    
                    self.trajet.append(duplicate_and_modify(self.explored[i][1], gap ))

        for v in range(reste) :
            gap = self.data.coverage_radius * v
            if  gap == 0 :    
                self.trajet.append(self.explored[self.nb_save_sonde ][1])
            else :
                self.trajet.append(duplicate_and_modify(self.explored[self.nb_save_sonde ][1], gap))


        print(f"len packet snake {len(self.trajet)}")
        print(f"len -> {len(self.trajet[0])} {len(self.trajet[52])}")
        print(f"len -> {len(self.trajet[1])} {len(self.trajet[52])}")
        print(f'exlporateur {len(self.explored[0][1]) } {len(self.explored[10][1]) }')
        print(f' Wath {self.trajet[11]}')

        # transposé
        self.trajet = [[row[k] for row in self.trajet] for k in range(len(self.trajet[0]))]
            
        
        
        
        
    def arbitre_sonde(self, sonde) -> int:
        '''
        The function to count the score of a solution for one turn with a single balloon.

        Args:
            balloon (Vector3): The balloon's position (x, y, z).
            debug (bool) (optional): The flag to print debug information.

        Returns:
            int: The score of the solution.
        '''
        def columndist(c1, c2, grid_width) -> int:
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

        def is_covered(r, c, u, v, coverage_radius) -> bool:
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
            return (r - u) ** 2 + columndist(c, v, self.data.cols) ** 2 <= coverage_radius ** 2

        # Check if the balloon and target_cells are valid
        if not sonde or not self.data.target_cells or self.data.coverage_radius < 0:
            raise TypeError("Invalid arguments.")
        
        score = 0

        # Test for each target if it is covered by the balloon
        for target in self.data.target_cells:
            # Target coordinates
            u, v = target.x, target.y

            # Check if the balloon altitude is not 0
            if sonde.z == 0:
                break

            # Balloon coordinates
            r, c = sonde.x, sonde.y

            # Check if the target is covered by the balloon
            if is_covered(r, c, u, v, self.data.coverage_radius):
                score += 1

        return score

                
                
