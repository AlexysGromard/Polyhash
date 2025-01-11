# IMPORTS
from multiprocessing import Pool, cpu_count
from typing import Callable, Any, Iterable

# CLASS
class ParallelExecutor:
    """
    Classe utilitaire pour gérer l'exécution parallèle de tâches avec multiprocessing.
    """


    _num_processes = cpu_count() #Nombre de coeurs du processeur qui determine le nombre de processus à lancer


    # SETTERS
    @staticmethod
    def set_num_processes(num_processes: int) -> None:
        """
        Définit le nombre de processus à utiliser pour l'exécution parallèle.

        Args:
            num_processes (int): Le nombre de processus à utiliser pour l'exécution parallèle.

        Raises:
            TypeError: la valeur du nombre de processus n'est pas un entier.
            ValueError: la valeur du nombre de processus est inférieure ou égale à 0.
            ValueError: la valeur du nombre de processus est supérieure à 10 * le nombre de coeurs du processeur.
        """
        # Vérification des paramètres
        
        if not isinstance(num_processes, int):
            # Vérifier si le nombre de processus est un entier
            raise TypeError("Le nombre de processus doit être un entier.")
        
        elif num_processes <= 0:
            # Vérifier si le nombre de processus est valide
            raise ValueError("Le nombre de processus doit être supérieur à 0.")
        
        elif num_processes > cpu_count() * 10:
            # Vérifier si le nombre de processus est inférieur ou égal à 10 * le nombre de coeurs du processeur
            raise ValueError(f"Le nombre de processus doit être inférieur ou égal à 10 * le nombre de coeurs du processeur : {cpu_count() * 10}.")
        
        else:
            # Affectation du nombre de processus
            ParallelExecutor._num_processes = num_processes
            
            
    # GETTERS
    @staticmethod
    def get_num_processes() -> int:
        """
        Retourne le nombre de processus utilisé pour l'ex

        Returns:
            int: Le nombre de processus utilisé pour l'exécution parallèle.
        """
        return ParallelExecutor._num_processes



    # CLASS METHODS
    
    
    @classmethod
    def execute(cls, func: Callable, args_list: Iterable[tuple]) -> list[Any]:
        """
        Exécute une fonction en parallèle en utilisant multiprocessing.

        Args:
            func (Callable): La fonction à exécuter en parallèle.
            args_list (Iterable[tuple]): Liste des arguments (sous forme de tuples) 
                                          pour chaque appel de la fonction.

        Returns:
            list[Any]: Liste des résultats retournés par la fonction `func` pour chaque ensemble d'arguments.
        """
        with Pool(processes=cls._num_processes) as pool:
            results = pool.starmap(func, args_list)
        return results
