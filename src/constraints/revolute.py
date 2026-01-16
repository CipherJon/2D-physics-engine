import math

from ..core.body import Body
from ..math.vec2 import Vec2


class RevoluteJoint:
    """
    A revolute joint constraint that allows two bodies to rotate around a common anchor point.
    """

    def __init__(self, body1: Body, body2: Body, anchor: Vec2):
        """
        Initialize a revolute joint between two bodies.

        Args:
            body1 (Body): The first body.
            body2 (Body): The second body.
            anchor (Vec2): The anchor point for the joint.
        """
        self.body1 = body1
        self.body2 = body2
        self.anchor = anchor

        # Calculate the local anchor points
        self.local_anchor1 = body1.transform.inverse_transform_point(anchor)
        self.local_anchor2 = body2.transform.inverse_transform_point(anchor)

        # Initialize the joint's properties
        self.bias_factor = 0.2
        self.softness = 0.0

    def pre_solve(self, time_step: float):
        """
        Prepare the joint for solving.

        Args:
            time_step (float): The time step for the simulation.
        """
        # Calculate the world anchor points
        self.anchor1 = self.body1.transform.transform_point(self.local_anchor1)
        self.anchor2 = self.body2.transform.transform_point(self.local_anchor2)

        # Calculate the mass matrix
        self._calculate_mass_matrix()

        # Calculate the bias
        self.bias = self.bias_factor * (self.anchor2 - self.anchor1) / time_step

    def solve_velocity_constraints(self):
        """
        Solve the velocity constraints for the joint.
        """
        # Calculate the relative velocity
        velocity1 = self.body1.velocity + Vec2(
            -self.body1.angular_velocity * self.local_anchor1.y,
            self.body1.angular_velocity * self.local_anchor1.x,
        )
        velocity2 = self.body2.velocity + Vec2(
            -self.body2.angular_velocity * self.local_anchor2.y,
            self.body2.angular_velocity * self.local_anchor2.x,
        )
        relative_velocity = velocity2 - velocity1

        # Calculate the impulse
        impulse = self.mass_matrix.solve(-relative_velocity - self.bias)

        # Apply the impulse
        self.body1.velocity -= impulse * self.body1.inverse_mass
        self.body1.angular_velocity -= (
            impulse.cross(self.local_anchor1) * self.body1.inverse_inertia
        )
        self.body2.velocity += impulse * self.body2.inverse_mass
        self.body2.angular_velocity += (
            impulse.cross(self.local_anchor2) * self.body2.inverse_inertia
        )

    def solve_position_constraints(self):
        """
        Solve the position constraints for the joint.
        """
        # Calculate the position error
        position_error = self.anchor2 - self.anchor1

        # Calculate the impulse
        impulse = self.mass_matrix.solve(-position_error)

        # Apply the impulse
        self.body1.position -= impulse * self.body1.inverse_mass
        self.body1.transform.position = self.body1.position
        self.body1.transform.rotation -= (
            impulse.cross(self.local_anchor1) * self.body1.inverse_inertia
        )
        self.body2.position += impulse * self.body2.inverse_mass
        self.body2.transform.position = self.body2.position
        self.body2.transform.rotation += (
            impulse.cross(self.local_anchor2) * self.body2.inverse_inertia
        )

    def _calculate_mass_matrix(self):
        """
        Calculate the mass matrix for the joint.
        """
        # Calculate the effective mass
        r1_cross = Vec2(-self.local_anchor1.y, self.local_anchor1.x)
        r2_cross = Vec2(-self.local_anchor2.y, self.local_anchor2.x)

        k1 = (
            self.body1.inverse_mass
            + self.body1.inverse_inertia * r1_cross.magnitude_squared()
        )
        k2 = (
            self.body2.inverse_mass
            + self.body2.inverse_inertia * r2_cross.magnitude_squared()
        )

        self.mass_matrix = Mat22([[k1 + k2, 0.0], [0.0, k1 + k2]])

    def get_anchor1(self) -> Vec2:
        """
        Get the anchor point on the first body.

        Returns:
            Vec2: The anchor point on the first body.
        """
        return self.anchor1

    def get_anchor2(self) -> Vec2:
        """
        Get the anchor point on the second body.

        Returns:
            Vec2: The anchor point on the second body.
        """
        return self.anchor2

    def set_anchor(self, anchor: Vec2):
        """
        Set the anchor point for the joint.

        Args:
            anchor (Vec2): The anchor point for the joint.
        """
        self.anchor = anchor
        self.local_anchor1 = self.body1.transform.inverse_transform_point(anchor)
        self.local_anchor2 = self.body2.transform.inverse_transform_point(anchor)

    def get_reaction_force(self, time_step: float) -> Vec2:
        """
        Get the reaction force at the joint.

        Args:
            time_step (float): The time step for the simulation.

        Returns:
            Vec2: The reaction force at the joint.
        """
        return self.impulse / time_step

    def get_reaction_torque(self, time_step: float) -> float:
        """
        Get the reaction torque at the joint.

        Args:
            time_step (float): The time step for the simulation.

        Returns:
            float: The reaction torque at the joint.
        """
        return self.impulse.cross(self.local_anchor1) / time_step
