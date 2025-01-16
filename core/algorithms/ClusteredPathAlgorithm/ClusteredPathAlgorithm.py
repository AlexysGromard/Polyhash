from dataclasses import dataclass
import random
from core.models import DataModel, Vector3
from core import Arbitrator
from ..Algorithm import Algorithm
from heapq import heappop, heappush
import math

@dataclass
class Cluster:
    center: Vector3
    targets: list[Vector3]

    def __str__(self):
        return f"Cluster at ({self.center.x}, {self.center.y}) with {len(self.targets)} targets"

class ClusteredPathAlgorithm(Algorithm):
    """
    Class : ClusteredPathAlgorithm
    An algorithm that partitions targets into clusters and performs dynamic assignment of balloons to maximize coverage.

    Attributes:
        data (DataModel): The input data for the algorithm.
        clusters (list[Cluster]): The clusters of targets.
        trajet (list[list[int]]): The trajectory of each balloon.

    Methods:
        _distance: Calculate distance between two points considering cyclic grid.
        _create_clusters: Partition targets into clusters based on coverage radius.
        _a_star_pathfinding: Adaptation of A* algorithm to find the shortest path based on wind vectors.
        _convert_data: Convert input data into clusters and initialize distances.
        _process: Process the clusters and assign balloons to maximize coverage while avoiding overlap.
        compute: Main computation method ensuring correct trajectory format.
    """

    def __init__(self, data: DataModel) -> None:
        super().__init__(data)
        self.clusters: list[Cluster] = []

    def _distance(self, pos1: Vector3, pos2: Vector3) -> float:
        """Calculate distance between two points considering cyclic grid"""
        dx = abs(pos1.x - pos2.x)
        dy = min(abs(pos1.y - pos2.y), self.data.cols - abs(pos1.y - pos2.y))
        return math.sqrt(dx * dx + dy * dy)

    def _create_clusters_knn(self, k: int = 5) -> None:
        # Initialize some random centers using K-means++
        centers = random.sample(self.data.target_cells, 1)
        while len(centers) < k:
            d_squared = []
            # Calculate the distance squared from each target to the nearest center
            for t in self.data.target_cells:
                d_squared.append(min((t.x - c.x) ** 2 + (t.y - c.y) ** 2 for c in centers))
            d_squared_sum = sum(d_squared)
            # Calculate the probability of each target being chosen as the next center
            probabilities = [d / d_squared_sum for d in d_squared]
            new_center = random.choices(self.data.target_cells, probabilities)[0]
            centers.append(new_center)

        # Initialize empty clusters
        clusters = [[] for _ in range(k)]

        # Re-assign clusters until stable (fixed iterations for simplicity)
        for _ in range(100):
            for c in clusters:
                c.clear()
            # Assign each target to the closest center
            for t in self.data.target_cells:
                closest_idx = min(range(k), key=lambda i: (centers[i].x - t.x) ** 2 + (centers[i].y - t.y) ** 2)
                clusters[closest_idx].append(t)
            # Update centers to be the average of assigned targets
            for i in range(k):
                if clusters[i]:
                    avg_x = sum(p.x for p in clusters[i]) / len(clusters[i])
                    avg_y = sum(p.y for p in clusters[i]) / len(clusters[i])
                    centers[i] = Vector3(int(avg_x), int(avg_y))

        # Store clusters in the algorithm's state
        self.clusters = []
        for i, c in enumerate(clusters):
            if len(c) > 50: # Ignore small clusters
                self.clusters.append(Cluster(center=centers[i], targets=c))

        # Print cluster information for debugging
        print(f"\nCreated {len(self.clusters)} clusters:")
        for i, cluster in enumerate(self.clusters):
            print(f"Cluster {i}: {cluster}")

    def _a_star_pathfinding(self, start: Vector3, goal: Vector3) -> list[int]:
        """
        Adaptation of A* algorithm to find the shortest path based on wind vectors.

        Args:
            start (Vector3): Starting position.
            goal (Vector3): Target position.

        Returns:
            list[int]: Altitude changes (-1, 0, +1) to navigate from start to goal.
        """

        # Priority queue to hold the open set of nodes to be evaluated
        open_set = []
        # Push the starting position into the priority queue with initial cost 0
        heappush(open_set, (0, start.z, start, []))  # (cost, altitude, position, path)

        # Set to hold the visited nodes
        visited = set()

        while open_set:
            # Pop the node with the lowest cost from the priority queue
            cost, altitude, current, path = heappop(open_set)

            # If the node has already been visited, skip it
            if (current.x, current.y, altitude) in visited:
                continue
            # Mark the node as visited
            visited.add((current.x, current.y, altitude))

            # If the goal is reached, return the path
            if current.x == goal.x and current.y == goal.y:
                return path

            # Generate neighbors by changing the altitude
            for delta_z in [-1, 0, 1]:
                new_altitude = altitude + delta_z
                # Ensure the new altitude is within the valid range
                if not (1 <= new_altitude <= self.data.altitudes):
                    continue

                # Get the wind vector at the current position and new altitude
                wind = self.data.wind_grids[new_altitude - 1][current.x][current.y]
                new_x = current.x + wind.x
                new_y = (current.y + wind.y) % self.data.cols

                # Ensure the balloon stays within bounds vertically
                if not (0 <= new_x < self.data.rows):
                    continue

                # Create the neighbor node
                neighbor = Vector3(new_x, new_y, new_altitude)
                new_path = path + [delta_z]
                # Calculate the new cost as the sum of the current cost, the step cost (1), and the heuristic
                new_cost = cost + 1 + self._distance(neighbor, goal)

                # Push the neighbor node into the priority queue
                heappush(open_set, (new_cost, new_altitude, neighbor, new_path))

        # If the goal is unreachable, return an empty path
        return []

    def _convert_data(self) -> None:
        """Convert input data into clusters and initialize distances"""
        self._create_clusters_knn(6)

    def _process(self) -> None:
        astar_execution = 0
        """
        Process the clusters and assign balloons to maximize coverage while avoiding overlap.
        Implements a dynamic assignment strategy where balloons are guided between clusters.
        """
        self.trajet = [[0 for _ in range(self.data.num_balloons)] for _ in range(self.data.turns)]

        # Track balloon positions throughout simulation
        balloon_positions = [Vector3(self.data.starting_cell.x, self.data.starting_cell.y, 0)
                            for _ in range(self.data.num_balloons)]

        # Sort clusters by importance (number of targets and distance from start)
        sorted_clusters = sorted(
            self.clusters,
            key=lambda c: (len(c.targets), -self._distance(self.data.starting_cell, c.center)),
            reverse=True
        )

        # Assign initial clusters to balloons
        balloon_assignments = []
        for i in range(self.data.num_balloons):
            balloon_assignments.append({
                'balloon_id': i,
                'target_cluster': None,
                'path': [],
                'turns_in_cluster': 0
            })

        # Process each turn
        for turn in range(self.data.turns):
            print(f"Processing turn {turn}")
            for assignment in balloon_assignments:
                balloon_id = assignment['balloon_id']
                current_pos = balloon_positions[balloon_id]

                # If balloon has no path or has reached its destination
                if assignment['target_cluster'] is None:
                        # Find next best cluster to target
                        best_cluster = None
                        best_score = float('-inf')

                        # Check if the cluster is already targeted by another balloon
                        for cluster in sorted_clusters:
                            if any(a['target_cluster'] == cluster and a['turns_in_cluster'] < 7 for a in balloon_assignments if a != assignment):
                                continue

                            score = len(cluster.targets) / (1 + self._distance(current_pos, cluster.center))
                            if score > best_score:
                                best_score = score
                                best_cluster = cluster
                        # Assign the best cluster to the balloon and calculate path
                        if best_cluster:
                            print(f"Balloon {balloon_id} assigned to cluster at ({best_cluster.center.x}, {best_cluster.center.y})")
                            assignment['target_cluster'] = best_cluster
                            astar_execution += 1
                            assignment['path'] = self._a_star_pathfinding(
                                current_pos,
                                Vector3(best_cluster.center.x, best_cluster.center.y, current_pos.z)
                            )

                # Execute next move if we have a path
                if len(assignment['path']) > 0:
                    altitude_change = assignment['path'].pop(0)
                    self.trajet[turn][balloon_id] = altitude_change

                    assignment['turns_in_cluster'] += 1
                    new_pos = Vector3(current_pos.x, current_pos.y, current_pos.z + altitude_change)
                    if self.data.updatePositionWithWind(new_pos):
                        balloon_positions[balloon_id] = new_pos
                    else:
                        self.trajet[turn][balloon_id] = 0
                        print(f"Balloon {balloon_id} went out of bounds at {new_pos}")

                else:
                    assignment['target_cluster'] = None
                    assignment['turns_in_cluster'] = 0
        print(f"A* executed {astar_execution} times")

    def compute(self) -> list[list[int]]:
        """
        Main computation method ensuring correct trajectory format.
        Returns a list of size T (turns) containing lists of size B (balloons).
        """
        self._convert_data()
        self._process()
        return self.trajet
