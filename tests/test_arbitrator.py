# Start the test with the following command:
# python -m unittest tests/test_arbitrator.py

import unittest

from core.Arbitrator import Arbitrator
from core.models import *

class TestArbitratorInit(unittest.TestCase):
    '''
    Test the Arbitrator class constructor
    '''
    def test_no_args(self):
        '''
        Test the case where no arguments are passed in argument

        Expected: TypeError
        '''
        with self.assertRaises(TypeError):
            Arbitrator()

    def test_invalid_grid_size(self):
        '''
        Test the case where the grid size is invalid

        Expected: ValueError
        '''
        with self.assertRaises(ValueError):
            data_model = DataModel(rows=0, cols=0, coverage_radius=0, target_cells=[Vector3(0, 0)])
            Arbitrator(data_model)

    def test_negative_grid_size(self):
        '''
        Test the case where the grid size is negative

        Expected: ValueError
        '''
        with self.assertRaises(ValueError):
            data_model = DataModel(rows=-1, cols=-1, coverage_radius=0, target_cells=[Vector3(0, 0)])
            Arbitrator(data_model)

    def test_valid_grid_size(self):
        '''
        Test the case where the grid size is valid

        Expected: The coverage map is initialized correctly
        '''
        for values_in, values_out in [
            (DataModel(rows=1, cols=1, coverage_radius=0, target_cells=[Vector3(0, 0)]), [[0]]),
            (DataModel(rows=2, cols=2, coverage_radius=0, target_cells=[Vector3(0, 0)]), [[0, 0], [0, 0]]),
            (DataModel(rows=3, cols=3, coverage_radius=0, target_cells=[Vector3(0, 0)]), [[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
            (DataModel(rows=3, cols=5, coverage_radius=0, target_cells=[Vector3(0, 0)]), [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])
        ]:
            with self.subTest(values_in=values_in, values_out=values_out):
                # Run tests
                arbitrator = Arbitrator(values_in)
                self.assertEqual(arbitrator.get_coverage_map(), values_out)
    
    def test_invalid_target_cells(self):
        '''
        Test the case where the target cells are invalid

        Expected: TypeError
        '''
        with self.assertRaises(TypeError):
            Arbitrator(DataModel(rows=1, cols=1, coverage_radius=0, target_cells=0))

    def test_negative_coverage_radius(self):
        '''
        Test the case where the coverage radius is negative

        Expected: ValueError
        '''
        with self.assertRaises(ValueError):
            Arbitrator(DataModel(rows=1, cols=1, coverage_radius=-1, target_cells=[Vector3(0, 0)]))
        
    def test_valid_coverage_radius(self):
        '''
        Test the case where the coverage radius is valid

        Expected: The coverage radius is initialized correctly
        '''
        for values_in, values_out in [
            (DataModel(rows=1, cols=1, coverage_radius=0, target_cells=[Vector3(0, 0)]), 0),
            (DataModel(rows=1, cols=1, coverage_radius=1, target_cells=[Vector3(0, 0)]), 1),
            (DataModel(rows=1, cols=1, coverage_radius=2, target_cells=[Vector3(0, 0)]), 2),
            (DataModel(rows=1, cols=1, coverage_radius=3, target_cells=[Vector3(0, 0)]), 3)
        ]:
            with self.subTest(values_in=values_in, values_out=values_out):
                # Run tests
                arbitrator = Arbitrator(values_in)
                self.assertEqual(arbitrator.coverage_radius, values_out)

class TestTurn_score(unittest.TestCase):
    '''
    Test the turn_score method of the Arbitrator class
    '''
    def test_no_args(self):
        '''
        Test the case where no arguments are passed in argument

        Expected: TypeError
        '''
        arbitrator = Arbitrator(DataModel(rows=1, cols=1, coverage_radius=0, target_cells=[Vector3(0, 0)]))
        with self.assertRaises(TypeError):
            arbitrator.turn_score()

    def test_empty_args(self):
        '''
        Test the case where the arguments are empty

        Expected: TypeError
        '''
        arbitrator = Arbitrator(DataModel(rows=1, cols=1, coverage_radius=0, target_cells=[Vector3(0, 0)]))
        with self.assertRaises(TypeError):
            arbitrator.turn_score([])

    def test_radius_1(self):
        '''
        Test the case where the grid is 10x10 and the radius is 1

        Expected: 4
        '''
        ballons = [
            Vector3(2, 3),
            Vector3(8, 2),
            Vector3(5, 5)
        ]
        targets = [
            Vector3(2, 2),
            Vector3(8, 1),
            Vector3(3, 3),
            Vector3(4, 5),
            Vector3(6, 6),
            Vector3(7, 6),
            Vector3(3, 8)
        ]
        arbitrator = Arbitrator(DataModel(rows=10, cols=10, coverage_radius=1, target_cells=targets)) 
        res = arbitrator.turn_score(ballons)
        self.assertEqual(res, 4)

    def test_radius_2(self):
        '''
        Test the case where the grid is 10x10 and the radius is 2

        Expected: 5
        '''
        ballons = [
            Vector3(5, 5),
            Vector3(3, 8)
        ]
        targets = [
            Vector3(3, 0),
            Vector3(6, 3),
            Vector3(6, 4),
            Vector3(5, 5),
            Vector3(5, 7),
            Vector3(2, 8)
        ]
        arbitrator = Arbitrator(DataModel(rows=10, cols=10, coverage_radius=2, target_cells=targets))
        res = arbitrator.turn_score(ballons, False)
        self.assertEqual(res, 5)
    
    def test_subject(self):
        '''
        Test the case where the grid is 3x5 and the radius is 2 for 5 turns

        Expected: 5
        '''
        ballons_per_turn = [
            Vector3(1, 3),
            Vector3(0, 3),
            Vector3(0, 0),
            Vector3(0, 1),
            Vector3(0, 2)
        ]
        targets = [
            Vector3(0, 2),
            Vector3(0, 4)
        ]
        arbitrator = Arbitrator(DataModel(rows=3, cols=5, coverage_radius=1, target_cells=targets))

        # Run tests
        total_score = 0
        for i in range(5):
            res = arbitrator.turn_score([ballons_per_turn[i]])
            total_score += res

        self.assertEqual(total_score, 5)

    def test_two_ballons_on_same_target_coverage_1(self):
        '''
        Test the case where two ballons are on the same target

        Expected: 2
        '''
        ballons = [
            Vector3(4, 4),
            Vector3(4, 6),
        ]
        targets = [
            Vector3(5, 4),
            Vector3(4, 5),
        ]
        arbitrator = Arbitrator(DataModel(rows=10, cols=10, coverage_radius=1, target_cells=targets))

        # Run tests
        res = arbitrator.turn_score(ballons)
        self.assertEqual(res, 2)

    def test_two_ballons_on_same_target_coverage_2(self):
        '''
        Test the case where two ballons are on the same target

        Expected: 3
        '''
        ballons = [
            Vector3(4, 4),
            Vector3(4, 6),
        ]
        targets = [
            Vector3(3, 5),
            Vector3(4, 5),
            Vector3(4, 6),
        ]
        arbitrator = Arbitrator(DataModel(rows=10, cols=10, coverage_radius=2, target_cells=targets))

        # Run tests
        res = arbitrator.turn_score(ballons)
        self.assertEqual(res, 3)