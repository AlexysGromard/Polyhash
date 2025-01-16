# NeuralNetwork.py
import random
from math import exp

from core.models import DataModel, Vector3
from core import Arbitrator

def constrain_altitude(raw_value, hauteur_max):
    """Contraint la valeur d'altitude entre 1 et hauteur_max."""
    return int(1 + raw_value * (hauteur_max))


class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size, arbitrator):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.weights_input_hidden = self.initialize_weights(input_size, hidden_size)
        self.weights_hidden_output = self.initialize_weights(hidden_size, output_size)
        self.output_layer = [0] * output_size

        self.arbitrator = arbitrator

    def initialize_weights(self, input_size, output_size):
        # Initialisation aléatoire des poids
        return [[random.random() for _ in range(input_size)] for _ in range(output_size)]

    def feedforward(self, inputs):
        # Propagation avant : calculer la sortie du réseau
        hidden_layer = [sum(inputs[i] * self.weights_input_hidden[j][i] for i in range(self.input_size))
                        for j in range(self.hidden_size)]
        
        # Appliquer une activation (par exemple, sigmoïde)
        self.output_layer = [1 / (1 + exp(-x)) for x in hidden_layer]  # Sigmoïde
        return self.output_layer

    def backpropagate(self, inputs, reward, learning_rate=0.01):
        # Mise à jour des poids en fonction de la récompense
        output_errors = [reward - output for output in self.output_layer]  # Erreur par rapport à la récompense

        # Calcul des gradients et ajustement des poids
        for i in range(self.output_size):
            for j in range(self.hidden_size):
                self.weights_hidden_output[i][j] += learning_rate * output_errors[i] * self.output_layer[j]

        for i in range(self.hidden_size):
            for j in range(self.input_size):
                self.weights_input_hidden[i][j] += learning_rate * output_errors[i] * inputs[j]

    def train(self, data_model, training_data, epochs, learning_rate, hauteur_max):
        """
        Entraînement du réseau de neurones.

        Args:
            data_model (DataModel): Le modèle de données contenant les informations nécessaires.
            training_data (list[tuple[dict, list[float]]]): Données d'entraînement avec le vent et les cibles.
            epochs (int): Nombre d'itérations.
            learning_rate (float): Taux d'apprentissage.
            hauteur_max (int): Hauteur maximale de la carte.
        """
        for epoch in range(epochs):
            total_loss = 0
            total_score = 0  # Score total pour calculer la moyenne

            # Copie de training_data au début de chaque époque
            inputs = training_data[0][0]

            for i in range(data_model.turns):
                # 1. Calculer les prédictions du réseau de neurones
                self.feedforward(inputs)
                predict = self.output_layer

                # 2. Construire la liste des nouvelles positions des ballons prédites par le réseau
                predicted_altitudes = [constrain_altitude(predict[i * 3], hauteur_max) for i in range(data_model.num_balloons)]

                # 3. Mettre à jour les positions des ballons en appliquant l'effet du vent
                for i in range(data_model.num_balloons):
                    inputs[i * 3 + 2] = predicted_altitudes[i]
                    # Créer un objet Vector3 pour chaque ballon avec les nouvelles coordonnées
                    balloon = Vector3(inputs[i * 3], inputs[i * 3 + 1], inputs[i * 3 + 2])

                    # Mettre à jour la position du ballon en fonction du vent
                    data_model.updatePositionWithWind(balloon)

                    # Mettre à jour les coordonnées du ballon dans la liste des inputs
                    inputs[i * 3] = balloon.x
                    inputs[i * 3 + 1] = balloon.y
                    inputs[i * 3 + 2] = balloon.z

                # 5. Calculer le score basé sur les positions mises à jour
                input_for_arbitrator = [Vector3(inputs[i * 3], inputs[i * 3 + 1], inputs[i * 3 + 2]) for i in range(data_model.num_balloons)]
                score = self.arbitrator.turn_score(input_for_arbitrator)

                total_score += score

                # 6. Calculer la perte (loss) et effectuer la rétropropagation
                loss = -score  # L'objectif est de maximiser le score
                self.backpropagate(inputs, score, learning_rate)  # Utilisation du score comme récompense

                total_loss += loss

            # Afficher la perte totale et le score moyen pour l'epoch
            avg_score = total_score / len(training_data)
            print(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss}, Avg Score: {avg_score}")

    def predict(self, data_model, inputs):
        # Donner pour chaque tour la meilleure altitude pour chaque ballon
        trajet = [[] for _ in range(data_model.turns)]
        for turn in range(data_model.turns):
            self.feedforward(inputs)
            predict = self.output_layer

            # Construire la liste des nouvelles positions des ballons prédites par le réseau
            predicted_altitudes = [constrain_altitude(predict[i * 3], data_model.altitudes) for i in range(data_model.num_balloons)]

            # Mettre à jour les positions des ballons en appliquant l'effet du vent
            for i in range(data_model.num_balloons):
                old_altitude = inputs[i * 3 + 2]

                inputs[i * 3 + 2] = predicted_altitudes[i]
                # Créer un objet Vector3 pour chaque ballon avec les nouvelles coordonnées
                balloon = Vector3(inputs[i * 3], inputs[i * 3 + 1], inputs[i * 3 + 2])

                # Mettre à jour la position du ballon en fonction du vent
                data_model.updatePositionWithWind(balloon)

                # Mettre à jour les coordonnées du ballon dans la liste des inputs
                inputs[i * 3] = balloon.x
                inputs[i * 3 + 1] = balloon.y
                inputs[i * 3 + 2] = balloon.z

                # Ajouter la variation d'altitude
                trajet[turn].append(balloon.z - old_altitude)
        return trajet

