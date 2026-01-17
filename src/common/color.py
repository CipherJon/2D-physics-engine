"""
Color class for handling colors in the physics engine.

This class provides functionality for creating, manipulating, and converting colors.
"""


class Color:
    """
    A class to represent a color with RGBA components.

    Attributes:
        r (float): The red component of the color (0.0 to 1.0).
        g (float): The green component of the color (0.0 to 1.0).
        b (float): The blue component of the color (0.0 to 1.0).
        a (float): The alpha (transparency) component of the color (0.0 to 1.0).
    """

    def __init__(self, r=0.0, g=0.0, b=0.0, a=1.0):
        """
        Initialize a new Color.

        Args:
            r (float): The red component of the color (0.0 to 1.0).
            g (float): The green component of the color (0.0 to 1.0).
            b (float): The blue component of the color (0.0 to 1.0).
            a (float): The alpha (transparency) component of the color (0.0 to 1.0).
        """
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def to_tuple(self):
        """
        Convert the color to a tuple of (r, g, b, a).

        Returns:
            tuple: A tuple containing the RGBA components.
        """
        return (self.r, self.g, self.b, self.a)

    def to_hex(self):
        """
        Convert the color to a hexadecimal string.

        Returns:
            str: A hexadecimal string representing the color.
        """
        return "#{:02x}{:02x}{:02x}".format(
            int(self.r * 255), int(self.g * 255), int(self.b * 255)
        )

    @classmethod
    def from_hex(cls, hex_color):
        """
        Create a Color from a hexadecimal string.

        Args:
            hex_color (str): A hexadecimal string representing the color.

        Returns:
            Color: A new Color instance.
        """
        hex_color = hex_color.lstrip("#")
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        return cls(r, g, b)
