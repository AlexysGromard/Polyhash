# IMPORT
import os
from pathlib import Path

# import local
from .algorithms import Algorithm
from .models import DataModel, Vector3, OutputModel
from .Arbitrator import Arbitrator

from .utils import DebugPrinter




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
        if type(algo) is not str and algo != None:
            raise ValueError(f"Invalid algorithm value: {algo}")
        
        
        # si aucun paramètre n'est passé pour l'algorithme, on utilise l'algorithme par défaut
        if algo == None :
            algo = 'Mathis'
        
        
        self.path           :str                = path
        self.output         :str                = output
        
        self.display        :bool               = display

        
        self.trajectories   :list[list]         = []
        
        self.datamodel      :'DataModel'        = DataModel.extract_data(self.path)
        self.algorithm      :Algorithm          = Algorithm.factory(algo)

        
        
        
    def run(self) -> None:
        """
        Méthode run qui exécute les calculs et les traitements nécessaires pour résoudre le problème via un algorithme choisi
        """
        self.trajectories = self.algorithm.compute(self.datamodel)
        
        # Affichage 
        DebugPrinter.debug(
            DebugPrinter.header("Solver", "run", DebugPrinter.STATES["run"]),
            DebugPrinter.variable("trajectories", "list[list[int]]", self.trajectories, additional_info={"length": len(self.trajectories)})
        )

        return 
    
    
    def post_process(self) -> None:
        """
        Méthode post_process qui exécute les traitements nécessaires pour générer le fichier de sortie et verifier les résultats de la résolution
        
        Raises:
            ValueError: Sort de la grille
            
        Returns:
            File: Fichier de sortie avec les résultats de la résolution
        
        """

        # Créer un arbitrateur
        abitrator = Arbitrator(self.datamodel.cols, self.datamodel.rows)
        
        
        # Créer une liste de ballons avec les positions initiales
        
        balloons = [self.datamodel.starting_cell.copy() for _ in range(self.datamodel.num_balloons)] 
        

        DebugPrinter.debug(
            DebugPrinter.header("Solver", "post_process", DebugPrinter.STATES["run"]),
            DebugPrinter.message("Starting post_process", color="yellow"),
            DebugPrinter.variable("abitrator", "Arbitrator", abitrator),
            DebugPrinter.variable("balloons", "list[Vector3]", balloons, additional_info={"length": len(balloons)})
        )

            
        
        
        # Pour chaque tour, on déplace les ballons et on calcule le score
        for turn in range(self.datamodel.turns):
            

            # déplacer les ballons 
            for i in range(self.datamodel.num_balloons):
                print(f"-----------------\\\\\-----------------")
                print(f"avant - balloon {i} : {balloons[i]}")
                balloons[i].z += self.trajectories[turn][i]
                print(f"mid - balloon {i}  z + {self.trajectories[turn][i]} - {self.trajectories[turn]} - {turn}"  )
                balloons[i], is_in = self.datamodel.updatePositionWithWind(balloons[i])
                print(f"after - balloon {i} : {balloons[i]} - is_in : {is_in}")
                if not is_in:
                    raise ValueError(f"Sort de la grille")
            
            # calculer le score
            res  = abitrator.turn_score(balloons, self.datamodel.target_cells, self.datamodel.coverage_radius)
            
            DebugPrinter.debug(
                DebugPrinter.header("Solver", "post_process", DebugPrinter.STATES["run"]),
                DebugPrinter.message(f"LOOP turn = {turn}", color="yellow"),
                DebugPrinter.variable("balloons", "list[Vector3]", balloons, additional_info={"length": len(balloons)}),
                DebugPrinter.variable("res", "int", res)
                      
            )             

                      
            
        
        # Exporter les résultats dans le fichier de sortie
        output = OutputModel(turns=self.datamodel.turns, num_balloons=self.datamodel.num_balloons, adjustments=self.trajectories)
        output.export_output_file(self.output)
        
        return

    
    
