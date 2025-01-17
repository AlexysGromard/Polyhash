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

    def euclidean_distance(self, a, b):
        '''
        Compute the euclidean distance between two points
        '''
        return ((a[0] - b[0])**2 + (a[1] - b[1])**2) ** 0.5

    def create_clusters(self, targets, coverage_radius):
        '''
        Create clusters of targets

        Args:
            targets (list[Vector3]): list of targets
            coverage_radius (float): coverage radius of the balloons
        Returns:
            clusters (list[list[int]]): list of clusters
            cluster_centers (list[Vector3]): list of cluster
        '''
        clusters = []
        visited = set()

        for i, target in enumerate(targets):
            if target in visited:
                continue

            # Create a new cluster
            cluster = [target]
            visited.add(target)

            # Add all targets within the coverage radius
            for j, target2 in enumerate(targets):
                if target2 in visited:
                    continue

                if self.euclidean_distance((target.x, target.y), (target2.x, target2.y)) <= coverage_radius:
                    cluster.append(target2)
                    visited.add(target2)

            clusters.append(cluster)

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