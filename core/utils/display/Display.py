
from abc import ABC, abstractmethod
from typing import Any
from core.models import DataModel

class Display(ABC):
    """
    Abstract base class for visualizing a simulation.

    Attributes:
        data_model (DataModel): The simulation data to be visualized.
    """

    _display_types: dict[str, "Display"] = {}

    def __init__(self, data_model: "DataModel"):
        self.data_model = data_model
    
    @abstractmethod
    def render(self, *args: Any) -> None:
        """
        Abstract method to render the visualization.

        This should be implemented by all subclasses that inherit from Display.
        """
        pass


    @staticmethod
    def register_display(display_name: str, display_class: "Display") -> None:
        """
        Registers a display class for the factory method.

        Parameters:
            display_name (str): The name of the display type.
            display_class (Display): The display class to register.
        """
        if not issubclass(display_class, Display):
            raise TypeError(f"{display_class} must be a subclass of Display.")
        Display._display_types[display_name] = display_class

    @staticmethod
    def create_display(display_name: str, data_model: "DataModel", *args: Any) -> "Display":
        """
        Factory Method : Creates a Display object of the specified type.

        Parameters:
            display_name (str): The name of the display type.
            data_model (DataModel): The data model to pass to the display.

        Returns:
            Display: An instance of the requested display type.

        """
        display_class = Display._display_types.get(display_name)
        if display_class is None:
            raise ValueError(f"Display type '{display_name}' is not registered.")
        return display_class(data_model, *args)




