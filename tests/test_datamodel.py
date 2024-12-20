# IMPORT
import unittest
# import local
from core.models import DataModel, Vector3



# TESTS



class TestDataModel(unittest.TestCase):

    def test_next_place_balloon_within_bounds(self):
        """
        Test nextPlaceBalloon method for a balloon staying within bounds.
        """
        wind_grids = [[[Vector3(1, 1, 0), Vector3(0, 0, 0)]]]
        model = DataModel(
            rows=2, cols=2, altitudes=1, num_targets=0, coverage_radius=0,
            num_balloons=0, turns=0, starting_cell=Vector3(0, 0, 0),
            target_cells=[], wind_grids=wind_grids
        )
        balloon = Vector3(0, 0, 1)
        new_position, in_bounds = model.nextPlaceBalloon(balloon)
        self.assertTrue(in_bounds)
        self.assertEqual(new_position, Vector3(0, 0, 1))



    def test_next_place_balloon_out_of_bounds(self):
        """
        Test nextPlaceBalloon method for a balloon moving out of bounds.
        """
        wind_grids = [[[Vector3(-1, 0, 0)]]]
        model = DataModel(
            rows=2, cols=2, altitudes=1, num_targets=0, coverage_radius=0,
            num_balloons=0, turns=0, starting_cell=Vector3(0, 0, 0),
            target_cells=[], wind_grids=wind_grids
        )
        balloon = Vector3(0, 0, 1)
        new_position, in_bounds = model.nextPlaceBalloon(balloon)
        self.assertFalse(in_bounds)
        self.assertEqual(new_position, Vector3(0, 0, 1))



    def test_next_place_balloon_ground_level(self):
        """
        Test nextPlaceBalloon method when the balloon is at ground level.
        """
        wind_grids = [[[Vector3(1, 1, 0)]]]
        model = DataModel(
            rows=2, cols=2, altitudes=1, num_targets=0, coverage_radius=0,
            num_balloons=0, turns=0, starting_cell=Vector3(0, 0, 0),
            target_cells=[], wind_grids=wind_grids
        )
        balloon = Vector3(0, 0, 0)
        new_position, in_bounds = model.nextPlaceBalloon(balloon)
        self.assertTrue(in_bounds)
        self.assertEqual(new_position, Vector3(0, 0, 0))

if __name__ == "__main__":
    unittest.main()
