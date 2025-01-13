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

    def _create_clusters(self, max_radius : int, min_size : int) -> None:
        """Partition targets into clusters based on coverage radius"""
        unclustered = self.data.target_cells.copy()

        while unclustered:
            current = unclustered[0]
            cluster_targets = [current]

            # Find all targets within coverage radius
            for target in unclustered[1:]:
                if self._distance(current, target) <= max_radius * 2:
                    cluster_targets.append(target)

            # Calculate cluster center
            center_x = sum(t.x for t in cluster_targets) / len(cluster_targets)
            center_y = sum(t.y for t in cluster_targets) / len(cluster_targets)
            center = Vector3(int(center_x), int(center_y), 0)

            # Create new cluster
            if len(cluster_targets) >= min_size:
                self.clusters.append(Cluster(center, cluster_targets))

            # Remove clustered targets from unclustered list
            for target in cluster_targets:
                unclustered.remove(target)

        # Print cluster information
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


            def heuristic(pos1: Vector3, pos2: Vector3) -> float:
                dx = abs(pos1.x - pos2.x)
                dy = min(abs(pos1.y - pos2.y), self.data.cols - abs(pos1.y - pos2.y))
                return dx + dy

            open_set = []
            heappush(open_set, (0, start.z, start, []))  # (cost, altitude, position, path)
            
            visited = set()

            while open_set:
                cost, altitude, current, path = heappop(open_set)

                if (current.x, current.y, altitude) in visited:
                    continue
                visited.add((current.x, current.y, altitude))

                # If the goal is reached
                if current.x == goal.x and current.y == goal.y:
                    return path

                # Generate neighbors
                for delta_z in [-1, 0, 1]:
                    new_altitude = altitude + delta_z
                    if not (1 <= new_altitude <= self.data.altitudes):
                        continue

                    wind = self.data.wind_grids[new_altitude - 1][current.x][current.y]
                    new_x = current.x + wind.x
                    new_y = (current.y + wind.y) % self.data.cols

                    # Ensure the balloon stays within bounds vertically
                    if not (0 <= new_x < self.data.rows):
                        continue

                    neighbor = Vector3(new_x, new_y, new_altitude)
                    new_path = path + [delta_z]
                    new_cost = cost + 1 + heuristic(neighbor, goal)

                    heappush(open_set, (new_cost, new_altitude, neighbor, new_path))

            # If the goal is unreachable
            return []


    def _convert_data(self) -> None:
        """Convert input data into clusters and initialize distances"""
        self._create_clusters(self.data.coverage_radius, 1)

    def _process(self) -> None:
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
                'current_cluster': None,
                'next_cluster': None,
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
                if not assignment['path']:
                    if assignment['next_cluster'] is None:
                        # Find next best cluster to target
                        best_cluster = None
                        best_score = float('-inf')

                        for cluster in sorted_clusters:
                            if any((a['next_cluster'] == cluster or a['current_cluster'] == cluster) and a['turns_in_cluster'] < 5 for a in balloon_assignments if a != assignment):
                                continue

                            score = len(cluster.targets) / (1 + self._distance(current_pos, cluster.center))
                            if score > best_score:
                                best_score = score
                                best_cluster = cluster

                        if best_cluster:
                            assignment['next_cluster'] = best_cluster
                            assignment['path'] = self._a_star_pathfinding(
                                current_pos,
                                Vector3(best_cluster.center.x, best_cluster.center.y, current_pos.z)
                            )

                # Execute next move if we have a path
                if assignment['path']:
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
                    self.trajet[turn][balloon_id] = 0
                    #print(f"Balloon {balloon_id} has no path")

                # Update cluster assignment if reached destination
                if assignment['next_cluster'] and \
                        self._distance(current_pos, assignment['next_cluster'].center) <= self.data.coverage_radius:
                    assignment['current_cluster'] = assignment['next_cluster']
                    assignment['next_cluster'] = None
                    assignment['turns_in_cluster'] = 0
  

    def compute(self) -> list[list[int]]:
        """
        Main computation method ensuring correct trajectory format.
        Returns a list of size T (turns) containing lists of size B (balloons).
        """
        self._convert_data()
        self._process()
        return self.trajet