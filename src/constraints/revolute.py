import logging

from ..core.body import Body
from ..math.mat22 import Mat22
from ..math.vec2 import Vec2

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


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
        self.impulse = Vec2(0.0, 0.0)

        print(f"Initialized RevoluteJoint with anchor: {anchor}")

    def pre_solve(self, time_step: float):
        """
        Prepare the joint for solving.

        Args:
            time_step (float): The time step for the simulation.
        """
        logger.info("Pre-solving RevoluteJoint between body1 and body2")
        # Recalculate the local anchor points to ensure they are up-to-date
        self.local_anchor1 = self.body1.transform.inverse_transform_point(self.anchor)
        self.local_anchor2 = self.body2.transform.inverse_transform_point(self.anchor)

        # Calculate the world anchor points
        self.anchor1 = self.body1.transform.transform_point(self.local_anchor1)
        self.anchor2 = self.body2.transform.transform_point(self.local_anchor2)

        print(f"Anchor1: {self.anchor1}, Anchor2: {self.anchor2}")

        # Calculate the mass matrix
        self._calculate_mass_matrix()

        # Calculate the bias to enforce the constraint
        position_error = self.anchor2 - self.anchor1
        self.bias = position_error * (self.bias_factor / time_step)
        print(f"Position error: {position_error}, Bias: {self.bias}")

    def solve_velocity_constraints(self, time_step: float):
        """
        Solve the velocity constraints for the joint.
        """
        logger.info("Solving velocity constraints for RevoluteJoint")
        # Ensure mass_matrix and bias are available
        if not hasattr(self, "mass_matrix"):
            logger.error(
                "mass_matrix not initialized. Call pre_solve before solve_velocity_constraints."
            )
            raise AttributeError(
                "mass_matrix not initialized. Call pre_solve before solve_velocity_constraints."
            )
        if not hasattr(self, "bias"):
            logger.error(
                "bias not initialized. Call pre_solve before solve_velocity_constraints."
            )
            raise AttributeError(
                "bias not initialized. Call pre_solve before solve_velocity_constraints."
            )

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

        print(f"Relative velocity: {relative_velocity}")

        # Calculate the impulse
        impulse = self.mass_matrix.solve(-relative_velocity - self.bias)

        print(f"Impulse: {impulse}")

        # Apply the impulse
        self.body1.velocity -= impulse * self.body1.inverse_mass
        self.body1.angular_velocity -= (
            impulse.cross(self.local_anchor1) * self.body1.inverse_inertia
        )
        self.body2.velocity += impulse * self.body2.inverse_mass
        self.body2.angular_velocity += (
            impulse.cross(self.local_anchor2) * self.body2.inverse_inertia
        )

        print(f"Updated body1 velocity: {self.body1.velocity}")
        print(f"Updated body2 velocity: {self.body2.velocity}")

    def solve_position_constraints(self):
        """
        Solve the position constraints for the joint.
        """
        logger.info("Solving position constraints for RevoluteJoint")
        # Calculate the position error
        position_error = self.anchor2 - self.anchor1

        print(f"Position error: {position_error}")

        # Calculate the impulse to correct the position error
        impulse = self.mass_matrix.solve(-position_error)

        print(f"Position impulse: {impulse}")

        # Apply the impulse to correct the positions
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

        print(f"Updated body1 position: {self.body1.position}")
        print(f"Updated body2 position: {self.body2.position}")

        # Apply position correction to reduce position error
        if position_error.magnitude() > 0.01:  # Small threshold to avoid jitter
            correction = position_error * 0.2
            self.body1.position += correction
            self.body2.position -= correction
            self.body1.transform.position = self.body1.position
            self.body2.transform.position = self.body2.position

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
