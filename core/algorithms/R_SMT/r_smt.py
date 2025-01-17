import random
from core.models import DataModel, Vector3
from core import Arbitrator
from ..Algorithm import Algorithm


class RSMT(Algorithm):
    """
    RSMT Algorithm for solving the balloon navigation and coverage problem.

    Inherits:
        Algorithm: Abstract base class for all algorithms.

    Attributes:
        data (DataModel): Data model containing the problem's grid, wind data, and constraints.
        arbitrator (Arbitrator): Utility class for computing scores based on balloon positions.
    """

    def __init__(self, data: DataModel) -> None:
        """
        Constructor for RSMT class.

        Args:
            data (DataModel): Data model for the problem.
        """
        super().__init__(data)
        self.arbitrator = Arbitrator(data)

    def compute(self) -> list[list[int]]:
        """
        Computes the optimal trajectories for the balloons.

        Returns:
            list[list[int]]: A list of altitude changes for each balloon per turn.
        """
        self.trajet = self._process()
        return self.trajet

    def _convert_data(self) -> None:
        """
        Converts input data into a format suitable for the algorithm.
        Not required for this implementation but left for extensibility.
        """
        pass

    def _process(self) -> list[list[int]]:
        """
        Main processing method for computing balloon trajectories.

        Returns:
            list[list[int]]: Optimal altitude adjustments for each balloon.
        """
        r = self._explore(
            self.data.turns,
            [Vector3(self.data.starting_cell.x, self.data.starting_cell.y, 0) for _ in range(self.data.num_balloons)],
            [0] * self.data.turns,
            0
        )
        print(f"score: {r[3]}")
        return r[1]

    def _explore(self, turn: int, balloons: list[Vector3], best: list[int], score: int) -> tuple:
        """
        Explores possible moves recursively for balloons over remaining turns.

        Args:
            turn (int): Number of remaining turns.
            balloons (list[Vector3]): Current positions of the balloons.
            best (list[int]): Best scores for previous turns.
            score (int): Current cumulative score.

        Returns:
            tuple: (state, trajectory, problem_balloon_index, score)
                - state (bool): Whether a valid trajectory was found.
                - trajectory (list[list[int]]): Trajectory of altitude changes for balloons.
                - problem_balloon_index (int | None): Index of a problematic balloon if state is False.
                - score (int): Total score achieved.
        """
        alt_variations = [self._available_altitudes(b) for b in balloons]
        new_balloons = [False] * len(balloons)
        next_step = (False, None, 0, 0)  # (state, trajectory, problem_balloon, score)

        while not next_step[0]:
            chosen = [-10] * len(balloons)  # Placeholder for altitude changes
            new_balloons = [False] * len(balloons)

            for i, balloon in enumerate(balloons):
                while not new_balloons[i]:
                    if not alt_variations[i]:
                        return False, None, i, 0

                    # Choose a random valid altitude variation
                    chosen[i] = random.choice(alt_variations[i])
                    new_balloons[i] = balloon.copy()
                    new_balloons[i].z += chosen[i]

                    # Apply wind movement
                    if new_balloons[i].z > 0:
                        new_balloons[i] = self._next_place(new_balloons[i])

                    # Check if balloon is valid
                    if not new_balloons[i]:
                        alt_variations[i].remove(chosen[i])

            # Calculate current turn score
            current_score = self.arbitrator.turn_score(new_balloons)
            score += current_score

            # Stop exploration if this trajectory is worse than the best
            # Early termination to improve performance

            # if len(best) - turn >= 5 and best[-turn - 5] > score:
            #     return False, False, False, False

            # If this is the last turn, return the result
            if turn == 1:
                return True, [chosen], None, score

            # Explore the next turn recursively
            next_step = self._explore(turn - 1, new_balloons, best, score)

            # Handle problematic balloons
            if not next_step[0]:
                alt_variations[next_step[2]].remove(chosen[next_step[2]])

        return True, [chosen] + next_step[1], None, next_step[3]

    def _available_altitudes(self, balloon: Vector3) -> list[int]:
        """
        Computes valid altitude changes for a balloon.

        Args:
            balloon (Vector3): Current balloon position.

        Returns:
            list[int]: Valid altitude variations (-1, 0, 1).
        """
        if balloon.z == 0:
            return [0, 1]
        return [i for i in (-1, 0, 1) if 0 < balloon.z + i <= self.data.altitudes]

    def _next_place(self, balloon: Vector3) -> Vector3 | bool:
        """
        Computes the next position of a balloon after applying wind.

        Args:
            balloon (Vector3): Current position of the balloon.

        Returns:
            Vector3 | bool: New position of the balloon or False if out of bounds.
        """
        if balloon.z > self.data.altitudes:
            return False
        if balloon.z == 0:
            return balloon

        wind = self.data.wind_grids[balloon.z - 1][balloon.x][balloon.y]
        new_position = Vector3(
            balloon.x + wind.x,
            (balloon.y + wind.y) % self.data.cols,
            balloon.z
        )

        # Check if the balloon is out of bounds vertically
        if new_position.x < 0 or new_position.x >= self.data.rows:
            return False
        return new_position
