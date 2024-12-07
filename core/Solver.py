# IMPORT
import os
from pathlib import Path

# import local
from .algorithms import Algorithm
from .models import DataModel, Vector3, OutputModel
from .Arbitrator import Arbitrator





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
        
        self.datamodel      :'DataModel'        = DataModel.extract_data(self.path)
        self.algorithm      :Algorithm          = Algorithm.factory(algo)

        
        
        
    def run(self) -> None:
        """
        Méthode run qui exécute les calculs et les traitements nécessaires pour résoudre le problème via un algorithme choisi
        """
        self.trajectories = self.algorithm.compute(self.datamodel)
        
        
        print(f"Data Model : ")
        print(f"Rows : {self.datamodel.rows}")
        print(f"Cols : {self.datamodel.cols}")
        print(f"Altitudes : {self.datamodel.altitudes}")
        print(f"Num Targets : {self.datamodel.num_targets}")
        print(f"Coverage Radius : {self.datamodel.coverage_radius}")
        print(f"Num Balloons : {self.datamodel.num_balloons}")
        print(f"Turns : {self.datamodel.turns}")
        
        
        print(f"Trajectories : {self.trajectories}")
        print(f"Trajectories : {len(self.trajectories)}")
        print("Post Process")
        return 
    
    
    def post_process(self) -> None:
        """
        Méthode post_process qui exécute les traitements nécessaires pour générer le fichier de sortie et verifier les résultats de la résolution
        
        Raises:
            ValueError: Sort de la grille
            
        Returns:
            File: Fichier de sortie avec les résultats de la résolution
        
        """
        
        def move_balloon(balloon, altitude) -> 'Vector3':
            # TODO: a voir si l'abitre va calculer le deplacement des ballons via les ordre donner par les trajectoires
            """Provisoire

            Args:
                balloon (Vector3): Position du ballon
                altitude (int): Altitude a ajouter

            Raises:
                ValueError: Sort de la grille

            Returns:
                Vector3: Nouvelle position du ballon
            """
            
            
            # calculer la nouvelle position du ballon avec l'altitude
            balloon.z += altitude
            
            
             #Check si l'altitude est correcte
            if balloon.z > self.datamodel.altitudes:
                return False
            
            
            #Changement de position
            wind = self.datamodel.wind_grids[balloon.z - 1][balloon.x][balloon.y]
            new_balloon = Vector3(
                balloon.x +wind.x,
                balloon.y +wind.y,
                balloon.z +wind.z,
            )
            new_balloon.y = new_balloon.y % self.datamodel.cols

            #Check si le ballon ne sort pas en haut / en bas
            
            if new_balloon.x < 0 or new_balloon.x >= self.datamodel.rows:
            
                raise ValueError(f"")
            
            
            return new_balloon
        
        
        
        # Créer un arbitrateur
        abitrator = Arbitrator(self.datamodel.cols, self.datamodel.rows)
        
        
        # Créer une liste de ballons avec les positions initiales
        balloons = [self.datamodel.starting_cell for i in range(self.datamodel.num_balloons)] 
        
        # Pour chaque tour, on déplace les ballons et on calcule le score
        for turn in range(self.datamodel.turns):
            
            # déplacer les ballons #TODO: Check qu'il n'y a pas d'erreur du changement de position
            balloons = [move_balloon(balloon, self.trajectories[turn][i]) for i, balloon in enumerate(balloons)]
            
            # calculer le score
            res  = abitrator.turn_score(balloons, self.datamodel.target_cells, self.datamodel.coverage_radius)
            
            if self.display:
                print(f"-----------------{turn}-----------------")
                print(f"Turn {turn} - balloon      : {balloons}")
                print(f"Turn {turn} - trajectories : {self.trajectories[turn]}")
                print(f"Turn {turn} - score        : {abitrator.score}")
                print(f"Turn {turn} - turn score   : {res}")
            
        
        # Exporter les résultats dans le fichier de sortie
        output = OutputModel(turns=self.datamodel.turns, num_balloons=self.datamodel.num_balloons, adjustments=self.trajectories)
        output.export_output_file(self.output)
        
        return
    
