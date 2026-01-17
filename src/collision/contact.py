"""
Contact class for collision detection.

This class represents a contact point between two colliding bodies.
It stores information about the collision such as the normal vector,
penetration depth, and the bodies involved.
"""


class Contact:
    """
    A contact point between two colliding bodies.

    Attributes:
        body_a: The first body involved in the collision.
        body_b: The second body involved in the collision.
        normal: The normal vector of the collision.
        penetration: The depth of penetration.
        contact_point: The point of contact in world coordinates.
        restitution: The coefficient of restitution (bounciness).
        friction: The coefficient of friction.
        persistent: Whether the contact persists across frames.
        normal_impulse: The accumulated normal impulse for warm starting.
        last_separation: The separation from the previous frame.
    """

    # Baumgarte stabilization constants
    BAUMGARTE = 0.1
    SLOP = 0.01

    def __init__(
        self,
        body_a,
        body_b,
        normal,
        penetration,
        contact_point,
        restitution=0.5,
        friction=0.5,
    ):
        """
        Initialize a new Contact.

        Args:
            body_a: The first body involved in the collision.
            body_b: The second body involved in the collision.
            normal: The normal vector of the collision.
            penetration: The depth of penetration.
            contact_point: The point of contact in world coordinates.
            restitution: The coefficient of restitution (bounciness).
            friction: The coefficient of friction.
        """
        self.body_a = body_a
        self.body_b = body_b
        self.normal = normal
        self.penetration = penetration
        self.contact_point = contact_point
        self.restitution = restitution
        self.friction = friction
        self.persistent = True
        self.normal_impulse = 0.0
        self.last_separation = 0.0

    def resolve(self):
        """
        Resolve the collision by applying impulses to the bodies.
        Returns:
            float: The magnitude of the impulse applied
        """
        import logging

        logger = logging.getLogger(__name__)

        logger.info("=== CONTACT RESOLUTION ===")
        logger.info(
            f"Body A (static={self.body_a.is_static}) at {self.body_a.position} vs Body B (static={self.body_b.is_static}) at {self.body_b.position}"
        )
        logger.info(f"Contact normal: {self.normal}")
        logger.info(f"Penetration depth: {self.penetration:.4f}")

        # Debug: Check if this is a resting contact
        # Calculate relative velocity
        relative_velocity = self.body_b.velocity - self.body_a.velocity
        logger.info(f"Relative velocity: {relative_velocity}")

        # Calculate relative velocity along the normal
        velocity_along_normal = relative_velocity.dot(self.normal)
        logger.info(f"Velocity along normal: {velocity_along_normal:.4f}")

        # For resting contacts, we still need to apply an impulse to prevent sinking
        # Only skip if bodies are actually moving apart (velocity_along_normal > 0)
        if velocity_along_normal > 0:
            logger.info("Bodies are moving apart, no impulse applied")
            return 0.0

        # For resting contacts (velocity_along_normal == 0), we still apply impulse
        logger.info("Applying contact impulse for resting or approaching bodies")

        # Calculate restitution with fallback to contact's default value
        e_a = getattr(self.body_a, "restitution", self.restitution)
        e_b = getattr(self.body_b, "restitution", self.restitution)
        e = min(e_a, e_b)
        logger.info(f"Restitution: {e}")

        # Calculate impulse scalar with warm starting
        inv_mass_sum = self.body_a.inverse_mass + self.body_b.inverse_mass
        if abs(inv_mass_sum) < 1e-6:
            logger.warning(f"WARNING: Very small inverse mass sum: {inv_mass_sum}")
            return 0.0

        # For resting contacts, we need to apply an impulse based on penetration
        # to prevent bodies from sinking through each other
        if abs(velocity_along_normal) < 1e-6:
            # Resting contact: apply impulse based on penetration depth
            # Use Baumgarte stabilization to prevent sinking
            baumgarte_factor = 0.2  # Baumgarte stabilization coefficient
            time_step = 1.0 / 60.0  # Assume default time step
            j = (baumgarte_factor / time_step) * self.penetration * inv_mass_sum
            logger.info(f"Resting contact impulse based on penetration: {j:.4f}")
        else:
            # Normal impulse calculation for moving contacts
            j = -(1 + e) * velocity_along_normal
            j /= inv_mass_sum

        j += self.normal_impulse  # Warm starting
        logger.info(f"Impulse scalar: {j:.4f}")

        # Apply impulse
        impulse = j * self.normal
        logger.info(f"Impulse vector: {impulse}")

        # Check if impulse is significant
        if impulse.magnitude() < 1e-6:
            logger.warning(
                f"WARNING: Very small impulse magnitude: {impulse.magnitude():.6f}"
            )

        velocity_change_a = impulse * self.body_a.inverse_mass
        velocity_change_b = impulse * self.body_b.inverse_mass
        logger.info(
            f"Body at {self.body_a.position} velocity change: {velocity_change_a}"
        )
        logger.info(
            f"Body at {self.body_b.position} velocity change: {velocity_change_b}"
        )

        self.body_a.velocity -= velocity_change_a
        self.body_b.velocity += velocity_change_b

        # Store the impulse for warm starting in the next frame
        self.normal_impulse = j

        logger.info(
            f"Updated velocities - body_a at {self.body_a.position}: {self.body_a.velocity}, body_b at {self.body_b.position}: {self.body_b.velocity}"
        )
        logger.info("=== END CONTACT RESOLUTION ===")

        return abs(j)

    def apply_positional_correction(self, dt):
        """
        Apply positional correction using Baumgarte stabilization to prevent bodies from overlapping.
        """
        correction = max(self.penetration + self.SLOP, 0.0)
        position_impulse = (self.BAUMGARTE / dt) * correction * self.normal

        # Apply to both bodies (proportional to inverse mass)
        self.body_a.position += position_impulse * self.body_a.inverse_mass
        self.body_b.position -= position_impulse * self.body_b.inverse_mass
