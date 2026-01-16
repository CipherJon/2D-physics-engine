class Shape:
    """
    A base class for all shapes in the physics engine.
    """

    def __init__(self):
        """
        Initialize the shape.
        """
        pass

    def get_vertices(self):
        """
        Get the vertices of the shape.

        Returns:
            list of Vec2: The vertices of the shape.
        """
        raise NotImplementedError("Subclasses must implement this method.")
