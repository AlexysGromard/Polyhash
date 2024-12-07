# Start the test with the following command:
# python -m unittest tests/test_arbitrator.py

import unittest

from core.Arbitrator import Arbitrator
from core.models import *

class TestArbitratorInit(unittest.TestCase):
    def test_no_args(self):
        # Test the case where no arguments are passed in argument
        with self.assertRaises(TypeError):
            Arbitrator()

    def test_invalid_grid_size(self):
        # Test the case where the grid size is invalid
        with self.assertRaises(ValueError):
            Arbitrator(0, 0)

    def test_negative_grid_size(self):
        # Test the case where the grid size is negative
        with self.assertRaises(ValueError):
            Arbitrator(-1, -1)

    def test_valid_grid_size(self):
        # Test the case where the grid size is valid
        for values_in, values_out in [
            ((1, 1), [[0]]),
            ((2, 2), [[0, 0], [0, 0]]),
            ((3, 3), [[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
            ((5, 3), [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
        ]:
            with self.subTest(values_in=values_in, values_out=values_out):
                # Run tests
                arbitrator = Arbitrator(*values_in)
                self.assertEqual(arbitrator.get_coverage_map(), values_out)

class TestTurn_score(unittest.TestCase):
    def test_no_args(self):
        # Test the case where no arguments are passed in argument
        arbitrator = Arbitrator(1, 1)
        with self.assertRaises(TypeError):
            arbitrator.turn_score()

    def test_empty_args(self):
        # Test the case where the arguments are empty
        arbitrator = Arbitrator(1, 1)
        with self.assertRaises(TypeError):
            arbitrator.turn_score([], [], -2)

    def test_radius_negative(self):
        # Test the case where the radius is negative
        arbitrator = Arbitrator(1, 1)
        with self.assertRaises(TypeError):
            arbitrator.turn_score([Vector3(0, 0, 0)], [Vector3(0, 0, 0)], -2)

    def test_radius_1(self):
        # Test the case where the grid is 10x10 and the radius is 1
        arbitrator = Arbitrator(10, 10)
        ballons = [
            Vector3(2, 3, 0),
            Vector3(8, 2, 0),
            Vector3(5, 5, 0)
        ]
        targets = [
            Vector3(2, 2, 0),
            Vector3(8, 1, 0),
            Vector3(3, 3, 0),
            Vector3(4, 5, 0),
            Vector3(6, 6, 0),
            Vector3(7, 6, 0),
            Vector3(3, 8, 0)
        ]
        coverage_radius = 1
        res = arbitrator.turn_score(ballons, targets, coverage_radius, False)
        self.assertEqual(res, 4)

    def test_radius_2(self):
        # Test the case where the grid is 10x10 and the radius is 2
        arbitrator = Arbitrator(10, 10)
        ballons = [
            Vector3(5, 5, 0),
            Vector3(8, 3, 0)
        ]
        targets = [
            Vector3(0, 3, 0),
            Vector3(3, 6, 0),
            Vector3(4, 6, 0),
            Vector3(5, 5, 0),
            Vector3(7, 5, 0),
            Vector3(8, 2, 0)
        ]
        coverage_radius = 2
        res = arbitrator.turn_score(ballons, targets, coverage_radius, False)
        self.assertEqual(res, 5)