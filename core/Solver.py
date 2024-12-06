# IMPORT

# import local
from .algorithms import Algorithm
from .models import DataModel





# CLASS
class Solver:
    """
    Classe Solver
    la classe solver est une classe qui lance le processus de résolution du problème
    
    Attributes:
        path (str): chemin du fichier d'entrée des données
        output (str): chemin du fichier de sortie des données
        
        trajectories (list[list]): liste des trajectoires des véhicules
        
    """
    
    
    def __init__(self, path :str, output :str) -> None:
        """
        Constructeur de la classe Solver

        Args:
            path (str): chemin du fichier d'entrée des données
            output (str): chemin du fichier de sortie des données
        """
        
        
        self.path           :str                = path
        self.output         :str                = output
        
        self.trajectories   :list[list]         = []
        
        self.datamodel      :'DataModel'          = DataModel.extract_data(self.path)
        self.algorithm      :Algorithm          = Algorithm.factory("Mathis")
        print("Solver created")
        print(f"Path: {self.path}")

        print(f"Output: {self.output}")   
        print(f"DataModel: {self.datamodel}")     
        
        
        
    def run(self) -> None:
        pass
    
    
    def post_process(self) -> None:
        pass