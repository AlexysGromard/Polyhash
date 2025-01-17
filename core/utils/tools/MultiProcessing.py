# IMPORTS
from multiprocessing import Pool, cpu_count
from typing import Callable, Any, Iterable
import copy
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






    @classmethod
    def _worker_method(cls, method_name, instance_data, *args):
        """
        Fonction utilitaire pour appeler une méthode sur une instance d'objet avec sérialisation des attributs.
        
        Args:
            method_name (str): Le nom de la méthode à appeler.
            instance_data (dict): Données de l'instance (attributs).
            *args: Les arguments à passer à la méthode.
        
        Returns:
            Any: Résultat de la méthode appelée.
        """
        # Récupérer la classe et reconstruire l'instance avec les attributs sérialisés
        instance = cls.rebuild_instance_from_data(instance_data)
        method = getattr(instance, method_name)
        return method(*args)
    
    @classmethod
    def execute_class(cls, obj_class: object, method_name: str, *args) -> list:
        """
        Exécute une méthode d'une classe en parallèle.
        
        Args:
            obj_class (object): La classe à instancier pour chaque processus.
            method_name (str): Le nom de la méthode de l'instance à exécuter.
            *args: Les arguments à passer à la méthode.

        Returns:
            list: Liste des résultats retournés par la méthode de l'instance de la classe.
        """
        # Sérialiser les données de l'instance
        instance_data = cls._serialize_instance(obj_class)
        
        # Exécuter les méthodes en parallèle
        with Pool(processes=cls._num_processes) as pool:
            results = pool.starmap(cls._worker_method, [(method_name, instance_data, *args) for _ in range(cls._num_processes)])
        
        return results

    @classmethod
    def _serialize_instance(cls, obj_class: object) -> dict:
        """
        Sérialise l'instance de la classe en extrayant ses attributs.

        Args:
            obj_class (object): L'instance de la classe à sérialiser.

        Returns:
            dict: Données sérialisées de l'instance.
        """
        instance_data = {
            'class_name': obj_class.__class__,
            'attributes': obj_class.__dict__  # Extraire les attributs de l'instance
        }
        return instance_data

    @classmethod
    def _rebuild_instance_from_data(cls, instance_data: dict):
        """
        Reconstruit une instance de la classe à partir des données sérialisées.

        Args:
            instance_data (dict): Données sérialisées de l'instance.
        
        Returns:
            object: Instance reconstruite.
        """
        # Créer une nouvelle instance de la classe et attribuer les valeurs
        class_name = instance_data['class_name']
        instance = class_name.__new__(class_name)
        for attr, value in instance_data['attributes'].items():
            setattr(instance, attr, value)
        return instance
