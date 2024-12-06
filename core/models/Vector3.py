from dataclasses import dataclass


@dataclass
class Vector3:
    """
    Class : Vector3
    A dataclass to represent a 3D vector

    Attributes:
        x (int): The x-coordinate of the vector.
        y (int): The y-coordinate of the vector.
        z (int): The z-coordinate of the vector.
    
    Methods:
        __add__: Adds two Vector3 objects.
        __iadd__: Adds two Vector3 objects in place.
        __eq__: Checks if two Vector3 objects are equal.
    """
    x: int = 0
    y: int = 0
    z: int = 0

    def __add__(self, other: "Vector3") -> "Vector3":
        """
        Adds two Vector3 objects.

        Parameters:
            other (Vector3): The other Vector3 object to add.

        Returns:
            Vector3: The sum of the two Vector3 objects.
        """
        if isinstance(other, Vector3):
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        return NotImplemented

    def __iadd__(self, other: "Vector3") -> "Vector3":
        """
        Adds two Vector3 objects in place.

        Parameters:
            other (Vector3): The other Vector3 object to add.

        Returns:
             Vector3: The sum of the two Vector3 objects.
        """
        if isinstance(other, Vector3):
            self.x += other.x
            self.y += other.y
            self.z += other.z
            return self
        return NotImplemented
    
    def __eq__(self, other: "Vector3") -> bool:
        """
        Checks if two Vector3 objects are equal.

        Parameters:
            other (Vector3): The other Vector3 object to compare.
        
        Returns:
            bool: True if the two Vector3 objects are equal, False otherwise.
        """
        if isinstance(other, Vector3):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return NotImplemented