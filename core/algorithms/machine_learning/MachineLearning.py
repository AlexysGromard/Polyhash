# MachineLearning.py
from core.models import DataModel, Vector3
from core import Arbitrator
from ..Algorithm import Algorithm
from .NeuralNetwork import NeuralNetwork

class MachineLearning(Algorithm):
    def __init__(self, data: DataModel) -> None:
        super().__init__(data)
        self.arbitrator = Arbitrator(data)

    def compute(self):
        self.trajet = self._process()
        return self.trajet
    
    def _convert_data(self):
        return super()._convert_data()
    
    def _process(self) -> list[list[int]]:
        '''
        Main processing method for computing balloon trajectories.

        Returns:
            list[list[int]]: Optimal altitude adjustments for each balloon.
        '''
        # Get the balloons' starting positions
        ballons = [Vector3(self.data.starting_cell.x, self.data.starting_cell.y, 0) for _ in range(self.data.num_balloons)]
        vents = self.data.wind_grids
        cibles = self.data.target_cells
        
        def vector3_to_list(vector):
            return [vector.x, vector.y, vector.z]
        
        # Transform the Vector3 objects into a list of integers
        ballons = [vector3_to_list(ballon) for ballon in ballons]
        vents = []
        for row in range(len(vents)):
            for col in range(len(vents[row])):
                vents.append([vector3_to_list(vent) for vent in vents[row][col]])
        cibles = [vector3_to_list(cible) for cible in cibles]

        inputs = [coord for ballon in ballons for coord in ballon] + [coord for vent in vents for coord in vent] + [coord for cible in cibles for coord in cible]

        print(f"Inputs: {inputs}")
        # Sortie cible: altitude pour chaque ballon
        outputs = [0 for _ in range(self.data.num_balloons)]

        # Train the model
        input_size = len(inputs)
        hidden_size = 100
        output_size = self.data.num_balloons * 3

        # Initialize the arbitrator
        arbitrator = Arbitrator(self.data)

        # Initialize the neural network
        nn = NeuralNetwork(input_size, hidden_size, output_size, arbitrator)

        # Données d'entraînement simulées
        training_data = [(inputs, outputs) for _ in range(1000)] # 1000 = nombre d'itérations
        nn.train(self.data, training_data, epochs=1000, learning_rate=0.1, hauteur_max=self.data.altitudes)

        # Prédiction
        predictions = nn.predict(inputs)
        print(f"Predictions: {predictions}")
        return predictions
