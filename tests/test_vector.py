# import
import unittest

# import local
from core.models import Vector3


# TESTS

class TestVector3(unittest.TestCase):

    def test_init(self):
        """
        Test that the Vector3 object is correctly initialized.
        """
        v = Vector3(1, 2, 3)
        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 2)
        self.assertEqual(v.z, 3)

    def test_default_init(self):
        """
        Test that the Vector3 object is correctly initialized with default values.
        """
        v = Vector3()
        self.assertEqual(v.x, 0)
        self.assertEqual(v.y, 0)
        self.assertEqual(v.z, 0)

    def test_init_error(self):
        """
        Test that initializing a Vector3 object with invalid values raises a TypeError.
        """
        with self.assertRaises(TypeError):
            _ = Vector3("invalid", 2, 3)


    def test_add(self):
        """
        Test that the __add__ method correctly adds two Vector3 objects.
        """
        v1 = Vector3(1, 2, 3)
        v2 = Vector3(4, 5, 6)
        result = v1 + v2
        self.assertEqual(result, Vector3(5, 7, 9))

    def test_add_type_error(self):
        """
        Test that adding a non-Vector3 object raises a TypeError.
        """
        v1 = Vector3(1, 2, 3)
        with self.assertRaises(TypeError):
            _ = v1 + "invalid"

    def test_iadd(self):
        """
        Test that the __iadd__ method correctly adds two Vector3 objects in place.
        """
        v1 = Vector3(1, 2, 3)
        v2 = Vector3(4, 5, 6)
        v1 += v2
        self.assertEqual(v1, Vector3(5, 7, 9))

    def test_iadd_type_error(self):
        """
        Test that in-place addition with a non-Vector3 object raises a TypeError.
        """
        v1 = Vector3(1, 2, 3)
        with self.assertRaises(TypeError):
            v1 += "invalid"

    def test_eq(self):
        """
        Test that the __eq__ method correctly compares two Vector3 objects.
        """
        v1 = Vector3(1, 2, 3)
        v2 = Vector3(1, 2, 3)
        v3 = Vector3(4, 5, 6)
        self.assertTrue(v1 == v2)
        self.assertFalse(v1 == v3)

    def test_eq_type_error(self):
        """
        Test that equality comparison with a non-Vector3 object returns False.
        """
        v1 = Vector3(1, 2, 3)
        self.assertFalse(v1 == "invalid")

    def test_copy(self):
        """
        Test that the copy method returns a new object with the same values.
        """
        v1 = Vector3(1, 2, 3)
        v2 = v1.copy()
        self.assertEqual(v1, v2)
        self.assertIsNot(v1, v2)  # Ensure it's a different object

    def test_copy_independence(self):
        """
        Test that modifying the copy does not affect the original object.
        """
        v1 = Vector3(1, 2, 3)
        v2 = v1.copy()
        v2.x = 10
        self.assertNotEqual(v1.x, v2.x)

if __name__ == "__main__":
    unittest.main()
