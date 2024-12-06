#IMPORTS
from abc import ABC, abstractmethod

# CLASS
class Algorithm(ABC):
    """
    Algorithm est une classe abstraite qui permet de définir les méthodes et attributs communs à tous les algorithmes
    
    Extends:
        ABC : classe abstraite de python
        
    Attributes:
        trajet (list[list[int]]): liste des trajectoires des véhicules
        data (DataModel): données
    
    methods:
        public:
            compute : méthode qui permet de lancer le calcul de l'algorithme
            
        protected:
            _convert_data : méthode qui permet de convertir les données du problème en un format utilisable par l'algorithme
            _process : méthode qui permet de lancer le processus de calcul de l'algorithme    
    
    Static Methods:
        factory : méthode qui permet de créer une instance de l'algorithme demandé
    """
    
    
    # ATTRIBUTES
    def __init__(self) -> None:
        """
        Constructeur de la classe Algorithm
        """

        
        self.trajet     :list[list[int]]    = []
        self.data       :'DataModel'        = None
        
        
        
        
    # ABSTRACT METHODS
    @abstractmethod
    def compute(self, data:'DataModel') -> list[list[int]]:
        """
        public
        compute est la méthode qui permet de lancer le calcul de l'algorithme

        Args:
            data (DataModel): données du problème

        Returns:
            list[list[int]]: liste des trajectoires des véhicules
        """
        pass
    
    @abstractmethod
    def _convert_data(self) -> None:
        """
        protected
        méthode qui permet de convertir les données du problème en un format utilisable par l'algorithme
        """
        pass
    
    @abstractmethod
    def _process(self) -> None:
        """
        protected
        méthode qui permet de lancer le processus de calcul de l'algorithme
        """
        pass
        
    
    
    
    
    # STATIC METHODS
    @staticmethod
    def factory(algo :str) -> 'Algorithm':
        """
        factory methode qui permet de créer une instance de l'algorithme demandé
        utilise le design pattern factory

        Args:
            algo (str): Nom de l'algorithme à utiliser

        Raises:
            ValueError: L'algo demandé n'existe pas

        Returns:
            Algorithm: instance de l'algorithme demandé
        """
        
        # recherche de l'algorithme demandé
        match algo:
            case "Mathis":
                from .Mathis.algoMathis import AlgoMathis
                return AlgoMathis()
            case _:
                raise ValueError("Algo not found")