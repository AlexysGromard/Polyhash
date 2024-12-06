from dataclasses import dataclass

@dataclass
class OutputModel:
    """
    Class : OutputModel
    A dataclass to represent and export the output of the simulation.

    Attributes:
        turns (int): The number of turns in the simulation.
        num_balloons (int): The number of balloons in the simulation.
        adjusments (list[list[int]]): A list of lists of integers representing the adjustments made to each balloon.
    
    Methods:
        export_output_file: Writes the output data to a file in the required format.
    """
    turns: int
    num_balloons: int
    adjustments: list[list[int]]

    def export_output_file(self, file_path: str) -> None:
        """
        Writes the output data to a file in the required format.

        Parameters:
            file_path (str): The path to the output file.
        """
        try:
            with open(file_path, 'w') as file:
                for turn in self.adjustments:
                    file.write(" ".join(map(str, turn)) + "\n")
        except Exception as e:
            raise IOError(f"Failed to write output to file: {e}")