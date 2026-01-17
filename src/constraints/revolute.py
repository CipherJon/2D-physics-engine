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

        # Hard clamp delta to prevent explosion
        impulse_delta = impulse_delta.clamped(
            -50.0, 50.0
        )  # assume Vec2 has clamped method or implement

        self.impulse += impulse_delta

        # Hard clamp accumulated impulse
        self.impulse = self.impulse.clamped(-200.0, 200.0)

        # Apply with damping
        self.body1.velocity -= self.impulse * self.body1.inverse_mass
        self.body1.angular_velocity -= (
            self.r1.cross(self.impulse) * self.body1.inverse_inertia
        )

        self.body2.velocity += self.impulse * self.body2.inverse_mass
        self.body2.angular_velocity += (
            self.r2.cross(self.impulse) * self.body2.inverse_inertia
        )

        # Conditional damping (only if velocity is high)
        if self.body1.velocity.magnitude() > 30.0:
            self.body1.velocity *= 0.995
            self.body1.angular_velocity *= 0.995
        self.body2.velocity *= 0.98
        self.body2.angular_velocity *= 0.98

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
            # Clamp position error to prevent numerical explosion
            error_magnitude = position_error.magnitude()
            if error_magnitude > 10.0:  # Limit maximum correction
                position_error = position_error * (10.0 / error_magnitude)

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
        invM1 = self.body1.inverse_mass
        invI1 = self.body1.inverse_inertia or 0.0
        invM2 = self.body2.inverse_mass
        invI2 = self.body2.inverse_inertia or 0.0

        # Prevent zero r vectors from making singular matrix
        r1sq = max(self.r1.magnitude_squared(), 1e-8)
        r2sq = max(self.r2.magnitude_squared(), 1e-8)

        # Simplified diagonal K (safe for most cases)
        k = invM1 + invM2 + invI1 * r1sq + invI2 * r2sq
        self.mass_matrix = Mat22([[k, 0.0], [0.0, k]])

        # Safe inverse
        det = k * k  # since off-diagonals 0
        if abs(det) < 1e-10:
            det = 1e-10
        self.inv_mass_matrix = Mat22([[1.0 / k, 0.0], [0.0, 1.0 / k]])

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
