# IMPORT
import os
from pathlib import Path

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
    
    
    def __init__(self, path :str, output :str, display :bool = False, algo :str = None) -> None:
        """
        Constructeur de la classe Solver

        Args:
            path (str): Chemin du fichier d'entrée des données
            output (str): Chemin du fichier de sortie des données
            display (bool, optional): active ou désactive l'affichage. Defaults to False.
            algo (str, optional): Algorithme à utiliser. Defaults to None.

        Raises:
            ValueError: Le chemin d'entrée n'est pas valide
            ValueError: Output directory does not exist
            ValueError: Invalid display value
            ValueError: Invalid algorithm value
        """
        
        # Vérifier si le chemin d'entrée est valide
        if not path or not Path(path).is_file():
            raise ValueError(f"Invalid input path: {path}")
        
        # Vérifier si le chemin de sortie est dans un répertoire valide
        output_dir = Path(output).parent
        if not output_dir.exists():
            raise ValueError(f"Output directory does not exist: {output_dir}")
        
        # Vérifier si le display est un booléen
        if type(display) is not bool:
            raise ValueError(f"Invalid display value: {display}")
        
        # verifier si l'algorithme est valide
        if type(algo) is not str:
            raise ValueError(f"Invalid algorithm value: {algo}")
        
        
        # si aucun paramètre n'est passé pour l'algorithme, on utilise l'algorithme par défaut
        if algo == None :
            algo = 'Mathis'
        
        
        self.path           :str                = path
        self.output         :str                = output
        
        self.display        :bool               = display
        
        self.trajectories   :list[list]         = []
        
        self.datamodel      :'DataModel'          = DataModel.extract_data(self.path)
        self.algorithm      :Algorithm          = Algorithm.factory(algo)

        
        
        
    def run(self) -> None:
        pass
    
    
    def post_process(self) -> None:
        pass