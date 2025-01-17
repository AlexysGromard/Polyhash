# CDBA.py

# Local import
from ..Algorithm import Algorithm
from ...models import DataModel
from core import Arbitrator
from ...models import Vector3

class CBBA(Algorithm):
    '''
    Cluster Based Balloon Allocation
    '''

    def euclidean_distance(self, a, b): # TODO : A TESTER
        '''
        Compute the euclidean distance between two points
        '''
        return ((a[0] - b[0])**2 + (a[1] - b[1])**2) ** 0.5

    def wpgma(self, targets, coverage_radius):  # TODO : À TESTER
        '''
        Compute the WPGMA algorithm to create clusters of targets.

        Args:
            targets (list[Vector3]): list of targets
            coverage_radius (float): coverage radius of the balloons
        Returns:
            clusters (list[list[Vector3]]): list of clusters
        '''
        # Initialize the clusters
        clusters = [[target] for target in targets]

        # Initialize the distance matrix
        distance_matrix = [[self.euclidean_distance((t1.x, t1.y), (t2.x, t2.y)) 
                            for t2 in targets] for t1 in targets]

        while len(clusters) > 1:
            # Find the pair of clusters with the smallest distance
            min_distance = float('inf')
            merge_i, merge_j = -1, -1

            for i in range(len(clusters)):
                for j in range(i + 1, len(clusters)):
                    # Compute the average distance between clusters[i] and clusters[j]
                    cluster_distance = sum(
                        distance_matrix[targets.index(clusters[i][k])][targets.index(clusters[j][l])] 
                        for k in range(len(clusters[i])) 
                        for l in range(len(clusters[j]))
                    ) / (len(clusters[i]) * len(clusters[j]))

                    if cluster_distance < min_distance:
                        min_distance = cluster_distance
                        merge_i, merge_j = i, j

            # Check if the distance is less than the coverage radius
            if min_distance > coverage_radius:
                break

            # Merge the two clusters
            clusters[merge_i] += clusters[merge_j]
            clusters.pop(merge_j)

            # Update the distance matrix
            for i in range(len(clusters)):
                if i == merge_i:
                    continue
                new_distance = sum(
                    self.euclidean_distance((p1.x, p1.y), (p2.x, p2.y))
                    for p1 in clusters[merge_i]
                    for p2 in clusters[i]
                ) / (len(clusters[merge_i]) * len(clusters[i]))
                distance_matrix[merge_i][i] = distance_matrix[i][merge_i] = new_distance

        return clusters

    def create_clusters(self, targets, coverage_radius): # TODO : A TESTER
        '''
        Create clusters of targets

        Args:
            targets (list[Vector3]): list of targets
            coverage_radius (float): coverage radius of the balloons
        Returns:
            clusters (list[list[int]]): list of clusters
            cluster_centers (list[Vector3]): list of cluster
        '''
        # Mettre les targets sous forme de points (x, y)
        clusters = self.wpgma(targets, coverage_radius)

        # Calculate the center of each cluster
        cluster_centers = []
        for cluster in clusters:
            center_x = round(sum(v.x for v in cluster) / len(cluster))
            center_y = round(sum(v.y for v in cluster) / len(cluster))
            cluster_centers.append(Vector3(center_x, center_y, 0))

        return clusters, cluster_centers


    def __init__(self, data: 'DataModel') -> None:
        '''
        Constructor of the CDBA class
        '''
        super().__init__(data)
        self.arbitrator = Arbitrator(data)

    def compute(self):
        '''
        Compute the trajectory of the balloons
        '''
        # Create clusters
        clusters, cluster_centers = self.create_clusters(self.data.target_cells, self.data.coverage_radius)
        for cluster in clusters:
            print(f"Cluster: {cluster} et center: {cluster_centers[clusters.index(cluster)]}")
        return []

    def _convert_data(self):
        pass

    def _process(self):
        return super()._process()