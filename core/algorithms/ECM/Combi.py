from core.models import Vector3, DataModel

class Combi:

    def __init__(self):
        pass

    def process(self, explorerData: list[tuple[list[int], list[Vector3], int]]) -> tuple[list[int], list[Vector3], int]:
        """Genère une bonne selection de ballons parmits les exploreurs passés en arguments

        Args:
            explorerData (list[tuple[list[int], list[Vector3], int]]): Liste de tuple 
            des exploreurs comme suit: (Path, BalloonPosition, score)

        Returns:
            tuple[list[int], list[Vector3], int]: (Path, BalloonPosition, score)
        """
        pass


    