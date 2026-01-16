class PhysicsEngineError(Exception):
    """Base class for all physics engine exceptions."""

    pass


class InvalidShapeError(PhysicsEngineError):
    """Raised when an invalid shape is provided."""

    pass


class CollisionError(PhysicsEngineError):
    """Raised when a collision-related error occurs."""

    pass


class ConstraintError(PhysicsEngineError):
    """Raised when a constraint-related error occurs."""

    pass


class InvalidBodyError(PhysicsEngineError):
    """Raised when an invalid body is provided."""

    pass


class SimulationError(PhysicsEngineError):
    """Raised when a simulation-related error occurs."""

    pass
