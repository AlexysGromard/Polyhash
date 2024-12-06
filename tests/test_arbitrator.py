# Start the test with the following command:
# python -m unittest tests/test_arbitator.py

import unittest

from core.Arbitrator import Arbitrator

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