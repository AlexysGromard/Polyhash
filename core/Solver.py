# IMPORT
import os
import copy
from pathlib import Path


# import local
from .algorithms import Algorithm
from .models import DataModel, Vector3, OutputModel
from .Arbitrator import Arbitrator

from .utils import DebugPrinter
from .utils.display import Display, Simulation2DDisplay




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
    
    
    def __init__(self, path :str, output :str, controller :bool = False, displays :list[str] = [], algo :str = 'Mathis') -> None:
        """
        Constructeur de la classe Solver

        Args:
            path (str): Chemin du fichier d'entrée des données
            output (str): Chemin du fichier de sortie des données
            display (bool, optional): active ou désactive l'affichage. Defaults to False.
            displays (list[str], optional): Liste des noms des displays à utiliser. Defaults to None.
            algo (str, optional): Algorithme à utiliser. Defaults to None.

        Raises:
            ValueError: Le chemin d'entrée n'est pas valide
            ValueError: Output directory does not exist
            TypeError: Invalid display value
            TypeError: Invalid displays value
            TypeError: Invalid algorithm value
        """
        
        # Vérifier si le chemin d'entrée est valide
        if not path or not Path(path).is_file():
            raise ValueError(f"Invalid input path: {path}")
        
        # Vérifier si le chemin de sortie est dans un répertoire valide
        output_dir = Path(output).parent
        if not output_dir.exists():
            raise ValueError(f"Output directory does not exist: {output_dir}")
        
        # Vérifier si le display est un booléen
        if type(controller) is not bool:
            raise TypeError(f"Invalid Typage for display value: {controller}")
        
        # Vérifier que le displays est une liste
        if type(displays) is not list:
            raise TypeError(f"Invalid Typage for displays value: {displays}")
        if len(displays) != 0:
            for display in displays:
                if type(display) is not str:
                    raise TypeError(f"Invalid Typage for displays value: {display}")
        
        # verifier si l'algorithme est valide
        if type(algo) is not str or algo == None:
            raise TypeError(f"Invalid Typage for algorithm value: {algo}")
        
        

        
        
        self.path           :str                = path
        self.output         :str                = output
        
        self.controller     :str                = controller
        
        self.display        :bool               = True if len(displays) != 0 else False
        self.displays       :list[str]          = displays

        self.trajectories   :list[list]         = []
        
        self.datamodel      :'DataModel'        = DataModel.extract_data(self.path)
        self.algorithm      : Algorithm         = Algorithm.factory(algo, data=self.datamodel)
        
        self.__score_history: list[int]         = []
        self.__turn_history : list[list[Vector3]]= []
    # GETTER
    
    def get_totalscore(self) -> int :
        """
        Score total caculer dans __validator

        Returns:
            int: _description_
        """
        return self.__score_history[-1]
        
    def get_score(self) -> list[int] :
        """
        Return le score cumulatif de chaque tour

        Returns:
            list[int]: score cumulatif de chaque tour
        """
        return self.__score_history
    
    
    # METHODE
    
    def run(self) -> None:
        """
        Méthode run qui exécute les calculs et les traitements nécessaires pour résoudre le problème via un algorithme choisi
        """
        self.trajectories = self.algorithm.compute()
        
        # Affichage 
        DebugPrinter.debug(
            DebugPrinter.header("Solver", "run", DebugPrinter.STATES["run"]),
            DebugPrinter.variable("trajectories", "list[list[int]]", self.trajectories, additional_info={"length": len(self.trajectories)})
        )

        return 
    
    
    def post_process(self) -> None:
        self.__controller()
        self.__output()
        self.__display()
        return



    def __controller(self):
        
        # si on ne veux pas controler
        if not self.controller :
            return 
        
        # Initialize Arbitrator and balloons
        abitrator = Arbitrator(self.datamodel)
        balloons = [self.datamodel.starting_cell.copy() for _ in range(self.datamodel.num_balloons)]
        
        DebugPrinter.debug(
            DebugPrinter.header("Solver", "post_process", DebugPrinter.STATES["run"]),
            DebugPrinter.message("Starting post_process", color="yellow"),
            DebugPrinter.variable("balloons_initial", "list[Vector3]", balloons)
        )

        total_score = 0

        for turn in range(self.datamodel.turns):
            DebugPrinter.debug(
                DebugPrinter.message(f"Processing turn {turn}", color="blue")
            )
            
            # Move all balloons for this turn
            for i, balloon in enumerate(balloons):
                # Update altitude
                balloon.z += self.trajectories[turn][i]

                # Apply wind and update position
                is_in = self.datamodel.updatePositionWithWind(balloon)
                
                # if udpate is in out 
                if not is_in:
                    
                    if not (0 <= balloon.z <= self.datamodel.altitudes):
                        raise ValueError(f"Invalid altitude for balloon {i} at turn {turn}")
                    else :
                        DebugPrinter.debug(
                            DebugPrinter.message(f"Balloon {i} out of bounds at turn {turn}", color="red")
                        )
                        raise ValueError("Balloon moved out of bounds")


            self.__turn_history .append([ balloon.copy() for balloon in balloons])
            
            # Calculate and log score
            turn_score = abitrator.turn_score(balloons)
            total_score += turn_score
            self.__score_history.append(total_score)

            DebugPrinter.debug(
                DebugPrinter.variable("turn_score", "int", turn_score),
                DebugPrinter.variable("cumulative_score", "int", total_score)
            )

    def __output(self) -> None :
        # Export results
        output = OutputModel(
            turns=self.datamodel.turns,
            num_balloons=self.datamodel.num_balloons,
            adjustments=self.trajectories
        )
        output.export_output_file(self.output)
        return
    
    def __display(self) -> None :
                # Display results
        if self.display:
            for display_name in self.displays:
                try:
                    match display_name:
                        case "simulation_2d":
                            display = Display.register_display(display_name, Simulation2DDisplay)
                            display = Display.create_display(display_name, self.datamodel, self.__turn_history, self.__score_history)
                        case _:
                            DebugPrinter.debug(DebugPrinter.message(f"Unknown display type '{display_name}'", color="red"))
                            continue
                    display.render()
                except Exception as e:
                    DebugPrinter.message(f"Error while rendering display '{display_name}': {e}", color="red")

    
    def reset(self, algo :str) -> None:
        self.algorithm = Algorithm.factory(algo)
        self.trajectories = []
        
        self.run()
        self.post_process()