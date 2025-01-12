# NeuralNetwork.py
import random
import math

from core.models import DataModel, Vector3
from core import Arbitrator

def sigmoid(x: float) -> float:
    '''
    Fonction sigmoïde

    Args:
        x (float): valeur à évaluer
    '''
    return 1 / (1 + math.exp(-x))

# Dérivée de la sigmoïde
def sigmoid_derivative(x: float) -> float:
    '''
    Dérivée de la fonction sigmoïde

    Args:
        x (float): valeur à évaluer
    '''
    return x * (1 - x)

class NeuralNetwork:
    '''
    Réseau de neurones simple

    Attributes:
        input_size (int): taille de la couche d'entrée
        hidden_size (int): taille de la couche cachée
        output_size (int): taille de la couche de sortie

        weights_input_hidden (list[list[float]]): poids entre la couche d'entrée et la couche cachée
        weights_hidden_output (list[list[float]]): poids entre la couche cachée et la couche de sortie

        bias_hidden (list[float]): biais de la couche cachée
        bias_output (list[float]): biais de la couche de sortie
    '''
    def __init__(self, input_size, hidden_size, output_size, arbitrator: Arbitrator) -> None:
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        # Initialisation des poids
        self.weights_input_hidden = [[random.uniform(-1, 1) for _ in range(hidden_size)] for _ in range(input_size)]
        self.weights_hidden_output = [[random.uniform(-1, 1) for _ in range(output_size)] for _ in range(hidden_size)]
        
        # Initialisation des biais
        self.bias_hidden = [random.uniform(-1, 1) for _ in range(hidden_size)]
        self.bias_output = [random.uniform(-1, 1) for _ in range(output_size)]

        self.arbitrator = arbitrator

    def feedforward(self, inputs):
        '''
        Calcul des valeurs pour les couches cachées et de sortie

        Args:
            inputs (list[float]): valeurs d'entrée

        Returns:
            list[float]: valeurs de sortie
        '''
        self.hidden_layer = [0] * self.hidden_size
        for i in range(self.hidden_size):
            self.hidden_layer[i] = sum(inputs[j] * self.weights_input_hidden[j][i] for j in range(self.input_size)) + self.bias_hidden[i]
            self.hidden_layer[i] = sigmoid(self.hidden_layer[i])
        
        # Calcul des valeurs pour la couche de sortie
        self.output_layer = [0] * self.output_size
        for i in range(self.output_size):
            self.output_layer[i] = sum(self.hidden_layer[j] * self.weights_hidden_output[j][i] for j in range(self.hidden_size)) + self.bias_output[i]
            self.output_layer[i] = sigmoid(self.output_layer[i])

        return self.output_layer

    def backpropagate(self, inputs, expected_output, learning_rate):
        '''
        Rétropropagation du gradient

        Args:
            inputs (list[float]): valeurs d'entrée
            expected_output (list[float]): valeurs de sortie attendues
            learning_rate (float): taux d'apprentissage
        '''
        # Calcul de l'erreur
        output_errors = [expected_output[i] - self.output_layer[i] for i in range(self.output_size)]
        hidden_errors = [0] * self.hidden_size
        for i in range(self.hidden_size):
            hidden_errors[i] = sum(output_errors[j] * self.weights_hidden_output[i][j] for j in range(self.output_size))

        # Mise à jour des poids et des biais
        for i in range(self.hidden_size):
            for j in range(self.output_size):
                self.weights_hidden_output[i][j] += learning_rate * output_errors[j] * sigmoid_derivative(self.output_layer[j]) * self.hidden_layer[i]

        for i in range(self.input_size):
            for j in range(self.hidden_size):
                self.weights_input_hidden[i][j] += learning_rate * hidden_errors[j] * sigmoid_derivative(self.hidden_layer[j]) * inputs[i]

        for i in range(self.output_size):
            self.bias_output[i] += learning_rate * output_errors[i] * sigmoid_derivative(self.output_layer[i])

        for i in range(self.hidden_size):
            self.bias_hidden[i] += learning_rate * hidden_errors[i] * sigmoid_derivative(self.hidden_layer[i])

    def train(self, data_model: DataModel, training_data, epochs, learning_rate, hauteur_max):
        """
        Entraînement du réseau de neurones.

        Args:
            data_model (DataModel): Le modèle de données contenant les informations nécessaires.
            training_data (list[tuple[dict, list[float]]]): Données d'entraînement avec le vent et les cibles.
            epochs (int): Nombre d'itérations.
            learning_rate (float): Taux d'apprentissage.
            hauteur_max (int): Hauteur maximale de la carte.
        """
        def constrain_altitude(raw_value, hauteur_max):
            """Contraint la valeur d'altitude entre 1 et hauteur_max."""
            return int(1 + raw_value * (hauteur_max - 1))

        for epoch in range(epochs):
            total_loss = 0
            total_score = 0  # Score total pour calculer la moyenne

            # Copie de training_data au début de chaque époque
            inputs = training_data[0][0]

            for i in range(data_model.turns):
                # print(f"Inputs: {inputs}")
                # 1. Calculer les prédictions du réseau de neurones
                self.feedforward(inputs)
                predict = self.output_layer

                # 2. Construire la liste des nouvelles positions des ballons prédites par le réseau
                predicted_positions = [
                    Vector3(
                        int(predict[i * 3]),  # Coordonnée X
                        int(predict[i * 3 + 1]),  # Coordonnée Y
                        constrain_altitude(predict[i * 3 + 2], hauteur_max)  # Coordonnée Z contrainte
                    ) for i in range(len(predict) // 3)
                ]

                # 3. Mettre à jour les positions des ballons en appliquant l'effet du vent
                for i, balloon in enumerate(predicted_positions):
                    # print(f"old position: {balloon}")
                    data_model.updatePositionWithWind(balloon)
                    # print(f"new position: {balloon}")

                    inputs[i * 3] = balloon.x
                    inputs[i * 3 + 1] = balloon.y
                    inputs[i * 3 + 2] = balloon.z


                # 5. Calculer le score basé sur les positions mises à jour
                score = self.arbitrator.turn_score(predicted_positions)
                print(f"The score is {score}")

                total_score += score

                # 6. Calculer la perte (loss) et effectuer la rétropropagation
                loss = -score  # L'objectif est de maximiser le score
                self.backpropagate(inputs, predict, learning_rate)

                total_loss += loss

            # Afficher la perte totale et le score moyen pour l'epoch
            avg_score = total_score / len(training_data)
            print(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss}, Avg Score: {avg_score}")
