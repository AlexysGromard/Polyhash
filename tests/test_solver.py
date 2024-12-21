# IMPORTS
import unittest

# import local
from core import Solver
from core.models import DataModel, Vector3
from core.algorithms import Algorithm



class TestSolver(unittest.TestCase):

    def test_solver_initialization(self):
        """
        Test that the Solver class initializes correctly.
        """
        solver = Solver(path="test_data.txt", output="output.txt", display=False, algo="Mathis")
        self.assertEqual(solver.path, "test_data.txt")
        self.assertEqual(solver.output, "output.txt")
        self.assertFalse(solver.display)
        self.assertEqual(solver.algorithm.name, "Mathis")

    def test_solver_invalid_path(self):
        """
        Test that an invalid input path raises a ValueError.
        """
        with self.assertRaises(ValueError):
            Solver(path="invalid_path.txt", output="output.txt")

    def test_solver_invalid_output_dir(self):
        """
        Test that an invalid output directory raises a ValueError.
        """
        with self.assertRaises(ValueError):
            Solver(path="test_data.txt", output="/invalid_dir/output.txt")

    def test_solver_invalid_display(self):
        """
        Test that a non-boolean display value raises a ValueError.
        """
        with self.assertRaises(ValueError):
            Solver(path="test_data.txt", output="output.txt", display="not_bool")

    def test_solver_invalid_algo(self):
        """
        Test that a non-string algorithm value raises a ValueError.
        """
        with self.assertRaises(ValueError):
            Solver(path="test_data.txt", output="output.txt", algo=123)

    def test_solver_run(self):
        """
        Test the run method of the Solver class.
        """
        solver = Solver(path="test_data.txt", output="output.txt", display=False, algo="Mathis")
        solver.datamodel = DataModel(
            rows=2, cols=2, altitudes=1, num_targets=0, coverage_radius=0,
            num_balloons=0, turns=1, starting_cell=Vector3(0, 0, 0),
            target_cells=[], wind_grids=[[[Vector3(0, 0, 0)]]]
        )
        solver.algorithm = Algorithm.factory("Mathis")
        solver.algorithm.compute = lambda dm: [[Vector3(0, 0, 0)]]
        solver.run()
        self.assertEqual(solver.trajectories, [[Vector3(0, 0, 0)]])

    def test_solver_post_process(self):
        """
        Test the post_process method of the Solver class.
        """
        solver = Solver(path="test_data.txt", output="output.txt", display=True, algo="Mathis")
        solver.datamodel = DataModel(
            rows=2, cols=2, altitudes=1, num_targets=1, coverage_radius=1,
            num_balloons=1, turns=1, starting_cell=Vector3(0, 0, 0),
            target_cells=[Vector3(1, 1, 0)], wind_grids=[[[Vector3(0, 1, 0)]]]
        )
        solver.trajectories = [[Vector3(0, 0, 0)]]
        solver.post_process()

    def test_solver_post_process_out_of_bounds(self):
        """
        Test that post_process raises an error when a balloon goes out of bounds.
        """
        solver = Solver(path="test_data.txt", output="output.txt", display=False, algo="Mathis")
        solver.datamodel = DataModel(
            rows=2, cols=2, altitudes=1, num_targets=1, coverage_radius=1,
            num_balloons=1, turns=1, starting_cell=Vector3(0, 0, 0),
            target_cells=[Vector3(1, 1, 0)], wind_grids=[[[Vector3(0, 2, 0)]]]
        )
        solver.trajectories = [[Vector3(0, 0, 0)]]
        with self.assertRaises(ValueError):
            solver.post_process()
