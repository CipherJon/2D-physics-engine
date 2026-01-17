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
        # Calculate the world anchor points using local anchors
        self.anchor1 = self.body1.transform.transform_point(self.local_anchor1)
        self.anchor2 = self.body2.transform.transform_point(self.local_anchor2)

        # Calculate the world-space r vectors
        self.r1 = self.anchor1 - self.body1.position
        self.r2 = self.anchor2 - self.body2.position

        print(f"Anchor1: {self.anchor1}, Anchor2: {self.anchor2}")

        # Calculate the mass matrix
        self._calculate_mass_matrix()

        # Calculate the bias to enforce the constraint using Baumgarte stabilization
        position_error = self.anchor2 - self.anchor1
        self.bias = Vec2(
            -(self.bias_factor / time_step) * position_error.x,
            -(self.bias_factor / time_step) * position_error.y,
        )
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

        # Calculate the relative velocity using world-space r vectors
        velocity1 = self.body1.velocity + Vec2.cross_scalar(
            self.body1.angular_velocity, self.r1
        )
        velocity2 = self.body2.velocity + Vec2.cross_scalar(
            self.body2.angular_velocity, self.r2
        )
        relative_velocity = velocity2 - velocity1

        print(f"Relative velocity: {relative_velocity}")

        # Calculate the impulse delta and accumulate for warm-starting
        impulse_delta = self.inv_mass_matrix.solve(-(relative_velocity + self.bias))
        self.impulse += impulse_delta

        print(f"Impulse delta: {impulse_delta}, Accumulated impulse: {self.impulse}")

        # Apply the accumulated impulse for stability
        impulse = self.impulse
        self.body1.velocity -= impulse * self.body1.inverse_mass
        self.body1.angular_velocity -= (
            self.r1.cross(impulse) * self.body1.inverse_inertia
        )
        self.body2.velocity += impulse * self.body2.inverse_mass
        self.body2.angular_velocity += (
            self.r2.cross(impulse) * self.body2.inverse_inertia
        )

        print(f"Updated body1 velocity: {self.body1.velocity}")
        print(f"Updated body2 velocity: {self.body2.velocity}")

        # Add angular constraint to prevent free spinning
        rel_angular_vel = self.body2.angular_velocity - self.body1.angular_velocity
        angular_bias = -(0.2 / time_step) * (
            self.body2.orientation - self.body1.orientation
        )
        angular_impulse = -(rel_angular_vel + angular_bias) / (
            self.body1.inverse_inertia + self.body2.inverse_inertia
        )

        self.body1.angular_velocity += angular_impulse * self.body1.inverse_inertia
        self.body2.angular_velocity -= angular_impulse * self.body2.inverse_inertia

    def solve_position_constraints(self):
        """
        Solve the position constraints for the joint.
        """
        logger.info("Solving position constraints for RevoluteJoint")
        # Calculate the position error
        position_error = self.anchor2 - self.anchor1

        print(f"Position error: {position_error}")

        # Lightweight position correction to prevent drift
        if position_error.magnitude() > 0.005:  # Slop threshold
            correction = Vec2(-0.5 * position_error.x, -0.5 * position_error.y)
            self.body1.position -= correction * self.body1.inverse_mass
            self.body2.position += correction * self.body2.inverse_mass
            # Update transforms
            self.body1.transform.position = self.body1.position
            self.body2.transform.position = self.body2.position

    def _calculate_mass_matrix(self):
        """
        Calculate the mass matrix for the joint.
        """
        # Calculate the effective mass using world-space r vectors
        invM1 = self.body1.inverse_mass
        invI1 = self.body1.inverse_inertia
        invM2 = self.body2.inverse_mass
        invI2 = self.body2.inverse_inertia

        # r1 and r2 are already computed in pre_solve
        r1x = self.r1.x
        r1y = self.r1.y
        r2x = self.r2.x
        r2y = self.r2.y

        # Full K (inverse effective mass) matrix elements with cross terms
        k11 = invM1 + invM2 + invI1 * (r1y * r1y) + invI2 * (r2y * r2y)
        k12 = -invI1 * (r1x * r1y) - invI2 * (r2x * r2y)
        k21 = k12
        k22 = invM1 + invM2 + invI1 * (r1x * r1x) + invI2 * (r2x * r2x)

        self.mass_matrix = Mat22([[k11, k12], [k21, k22]])
        self.inv_mass_matrix = self.mass_matrix.inverse()

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
