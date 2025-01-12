from ..Algorithm import Algorithm
from core.models import DataModel, Vector3
from core.Arbitrator import Arbitrator
import random
from core.utils import DebugPrinter

Genome =  list[list[int]]
Population = list[Genome]

class GenAlgorithm(Algorithm):
    """
    Genetic Algorithm for solving the balloon navigation and coverage problem.

    Inherits:
        Algorithm: Abstract base class for all algorithms.

    Attributes:
        data (DataModel): Data model containing the problem's grid, wind data, and constraints.
        arbitrator (Arbitrator): Utility class for computing scores based on balloon positions.
    """

    def __init__(self, data: DataModel) -> None:
        """
        Constructor for GenAlgorithm class.

        Args:
            data (DataModel): Data model for the problem.
        """
        super().__init__(data)
        self.arbitrator : Arbitrator = Arbitrator(data)
        self.population_size : int = 30
        self.num_generations : int = 1000
        self.mutation_rate : float = 0.01
        self.crossover_rate : float = 0.8
        self.elitism : float = 0.1
        self.population : Population
        self.out_of_bounds_penalty : int = 1000
        self.back_to_ground_penalty : int = 100
        self.fitness_limit : int = 1000

    def _convert_data(self):
        """
        Converts input data into a format suitable for the algorithm.
        Not required for this implementation but left for extensibility.
        """
        pass
    
    def generate_genome(self) -> Genome:
        """
        Generates a genome for the genetic algorithm.
        """
        return [random.choices([-1, 0, 1], k=self.data.num_balloons) for _ in range(self.data.turns)]
    
    def initialize_population(self) -> None:
        """
        Initializes the population of the genetic algorithm.
        (Generates the genome)

        """
        self.population = [self.generate_genome() for _ in range(self.population_size)]

    def fitness(self, genome: Genome) -> int:
        score = 0
        # Create a local copy of balloon positions for this genome
        balloon_positions = [Vector3(self.data.starting_cell.x, self.data.starting_cell.y, 0) for _ in range(self.data.num_balloons)]
        for turn in genome:
            for i, balloon in enumerate(balloon_positions):
                if balloon.z == 0 and turn[i] == -1:
                    # Ignore invalid descent when on the ground
                    continue
                alt_change = turn[i]
                new_altitude = balloon.z + alt_change
                # Enforce altitude constraints
                if new_altitude < 1 or new_altitude > self.data.altitudes:
                    score -= self.back_to_ground_penalty
                    continue
                balloon.z = new_altitude

                # Apply wind effect and check if the balloon is still in the grid
                if not self.data.updatePositionWithWind(balloon):
                    score -= self.out_of_bounds_penalty
            # Compute score for this turn
            score += self.arbitrator.turn_score(balloon_positions)
        return score

    
    def selection_elitism(self) -> Population:
        """
        Selects the best individuals of the population.
        """
        return sorted(self.population, key=self.fitness, reverse=True)[:int(self.elitism * self.population_size)]
    
    def selection_tournament(self) -> Population:
        """
        Selects the best individuals of the population using tournament selection.
        """
        fitness_scores = [self.fitness(genome) for genome in self.population]
        min_fitness = min(fitness_scores)

        # Normalize scores: shift them into positive range
        normalized_weights = [score - min_fitness + 1 for score in fitness_scores]

        # Select two parents using normalized weights
        return random.choices(population=self.population, k=2, weights=normalized_weights)
    
    def crossover(self, parent1: Genome, parent2: Genome) -> tuple[Genome, Genome]:
        """
        Applies crossover between two parents.
        In the crossover operation, first, we select two parent chromosomes and a crossover point. 
        Based on this selection, we exchange genetic information or chromosomes to generate two new individuals who inherit traits from both parents:
        """
        if random.random() < self.crossover_rate:
            crossover_point = random.randint(1, self.data.turns - 1)
            child1 = [parent1[turn][:crossover_point] + parent2[turn][crossover_point:] for turn in range(self.data.turns)]
            child2 = [parent2[turn][:crossover_point] + parent1[turn][crossover_point:] for turn in range(self.data.turns)]
            return child1, child2
        return parent1, parent2
    
    def mutation(self, genome: Genome) -> Genome:
        """
        Applies mutation to a genome.
        In the mutation operation, for each altitude change (gene) in the genome, 
        a mutation of the gene is performed with a probability of mutation_rate.
        """
        mutated_genome = [list(turn) for turn in genome]
        for i, turn in enumerate(mutated_genome):
            mutated_genome[i] = [
                gene if random.random() > self.mutation_rate else random.choice([-1, 0, 1])
                for gene in turn
            ]
        return mutated_genome


    def run_evolution(self) -> Genome:
        """
        Runs the genetic algorithm.
        """
        DebugPrinter.debug(
            DebugPrinter.header("Genetic Algorithm", "run_evolution", DebugPrinter.STATES["run"]),
            DebugPrinter.message("Running genetic algorithm")
        )
        self.initialize_population()
        for _ in range(self.num_generations):
            DebugPrinter.debug(
                DebugPrinter.message(f"Generation {_}")
            )
            # Select the best individuals
            elite = self.selection_elitism()
            # Best score 
            best_score = self.fitness(elite[0])
            DebugPrinter.debug(
                DebugPrinter.variable("best_score", "int", best_score)
            )
            # Stop if the fitness limit is reached
            if best_score > self.fitness_limit:
                DebugPrinter.debug(
                    DebugPrinter.message("Fitness limit reached")
                )
                break
            # Complete the next generation with children from crossover and mutation
            DebugPrinter.debug(
                DebugPrinter.message("Completing next generation")
            )
            next_generation = elite[:]
            while len(next_generation) < self.population_size:
                parents = self.selection_tournament()
                child1, child2 = self.crossover(parents[0], parents[1])
                next_generation.extend([self.mutation(child1), self.mutation(child2)])
            self.population = next_generation
        return max(self.population, key=self.fitness)
    
    def _process(self):
        return self.run_evolution()
    
    def compute(self) -> list[list[int]]:
        """
        Computes the solution for the problem.
        """
        return self._process()

    

        