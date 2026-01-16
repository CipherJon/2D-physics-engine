import math

from ..core.body import Body
from ..math.vec2 import Vec2


class DistanceJoint:
    """
    A distance joint constraint that maintains a fixed distance between two points on two bodies.
    """

    def __init__(
        self,
        body1: Body,
        body2: Body,
        anchor1: Vec2,
        anchor2: Vec2,
        length: float = None,
    ):
        """
        Initialize a distance joint.

        Args:
            body1 (Body): The first body.
            body2 (Body): The second body.
            anchor1 (Vec2): The anchor point on the first body.
            anchor2 (Vec2): The anchor point on the second body.
            length (float): The desired distance between the anchor points.
        """
        self.body1 = body1
        self.body2 = body2
        self.anchor1 = anchor1
        self.anchor2 = anchor2
        self.length = (
            length
            if length is not None
            else (body1.position + anchor1 - body2.position - anchor2).magnitude()
        )
        self.stiffness = 1.0
        self.damping = 0.1

    def __str__(self):
        """
        Return a string representation of the distance joint.
        """
        return f"DistanceJoint(body1={self.body1}, body2={self.body2}, anchor1={self.anchor1}, anchor2={self.anchor2}, length={self.length})"

    def __repr__(self):
        """
        Return a detailed string representation of the distance joint.
        """
        return (
            f"DistanceJoint(body1={repr(self.body1)}, body2={repr(self.body2)}, "
            f"anchor1={repr(self.anchor1)}, anchor2={repr(self.anchor2)}, length={self.length})"
        )

    def solve_velocity_constraints(self, dt: float):
        """
        Solve the velocity constraints for the distance joint.

        Args:
            dt (float): The time step.
        """
        # Get the world anchor points
        world_anchor1 = self.body1.position + self.anchor1
        world_anchor2 = self.body2.position + self.anchor2

        # Calculate the direction vector
        direction = world_anchor2 - world_anchor1
        distance = direction.magnitude()

        if distance == 0:
            return

        direction = direction / distance

        # Calculate the relative velocity
        relative_velocity = (
            self.body2.velocity
            + Vec2(
                -self.body2.angular_velocity * self.anchor2.y,
                self.body2.angular_velocity * self.anchor2.x,
            )
            - self.body1.velocity
            - Vec2(
                -self.body1.angular_velocity * self.anchor1.y,
                self.body1.angular_velocity * self.anchor1.x,
            )
        )

        # Calculate the velocity bias
        velocity_bias = -self.damping * (distance - self.length) / dt

        # Calculate the impulse
        impulse = (velocity_bias - relative_velocity.dot(direction)) / (
            self.body1.inverse_mass
            + self.body2.inverse_mass
            + self.body1.inverse_inertia * self.anchor1.cross(direction) ** 2
            + self.body2.inverse_inertia * self.anchor2.cross(direction) ** 2
        )

        # Apply the impulse
        impulse_vector = direction * impulse

        self.body1.velocity -= impulse_vector * self.body1.inverse_mass
        self.body1.angular_velocity -= self.body1.inverse_inertia * self.anchor1.cross(
            impulse_vector
        )

        self.body2.velocity += impulse_vector * self.body2.inverse_mass
        self.body2.angular_velocity += self.body2.inverse_inertia * self.anchor2.cross(
            impulse_vector
        )

    def solve_position_constraints(self):
        """
        Solve the position constraints for the distance joint.
        """
        # Get the world anchor points
        world_anchor1 = self.body1.position + self.anchor1
        world_anchor2 = self.body2.position + self.anchor2

        # Calculate the direction vector
        direction = world_anchor2 - world_anchor1
        distance = direction.magnitude()

        if distance == 0:
            return

        direction = direction / distance

        # Calculate the position error
        position_error = distance - self.length

        # Calculate the impulse
        impulse = (
            -self.stiffness
            * position_error
            / (
                self.body1.inverse_mass
                + self.body2.inverse_mass
                + self.body1.inverse_inertia * self.anchor1.cross(direction) ** 2
                + self.body2.inverse_inertia * self.anchor2.cross(direction) ** 2
            )
        )

        # Apply the impulse
        impulse_vector = direction * impulse

        self.body1.position -= impulse_vector * self.body1.inverse_mass
        self.body1.rotate(
            -self.body1.inverse_inertia * self.anchor1.cross(impulse_vector)
        )

        self.body2.position += impulse_vector * self.body2.inverse_mass
        self.body2.rotate(
            self.body2.inverse_inertia * self.anchor2.cross(impulse_vector)
        )

    def get_reaction_force(self, dt: float) -> Vec2:
        """
        Get the reaction force of the distance joint.

        Args:
            dt (float): The time step.

        Returns:
            Vec2: The reaction force.
        """
        # Get the world anchor points
        world_anchor1 = self.body1.position + self.anchor1
        world_anchor2 = self.body2.position + self.anchor2

        # Calculate the direction vector
        direction = world_anchor2 - world_anchor1
        distance = direction.magnitude()

        if distance == 0:
            return Vec2.zero()

        direction = direction / distance

        # Calculate the relative velocity
        relative_velocity = (
            self.body2.velocity
            + Vec2(
                -self.body2.angular_velocity * self.anchor2.y,
                self.body2.angular_velocity * self.anchor2.x,
            )
            - self.body1.velocity
            - Vec2(
                -self.body1.angular_velocity * self.anchor1.y,
                self.body1.angular_velocity * self.anchor1.x,
            )
        )

        # Calculate the velocity bias
        velocity_bias = -self.damping * (distance - self.length) / dt

        # Calculate the impulse
        impulse = (velocity_bias - relative_velocity.dot(direction)) / (
            self.body1.inverse_mass
            + self.body2.inverse_mass
            + self.body1.inverse_inertia * self.anchor1.cross(direction) ** 2
            + self.body2.inverse_inertia * self.anchor2.cross(direction) ** 2
        )

        return direction * impulse
