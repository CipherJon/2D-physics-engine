import os
import sys

# Add the parent directory to the path so we can import from src
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.constraints.revolute import RevoluteJoint
from src.core.body import Body
from src.core.circle import Circle
from src.math.transform import Transform
from src.math.vec2 import Vec2


def test_revolute_joint():
    # Create two bodies with Circle shapes
    body1 = Body(
        Circle(Vec2(0.0, 0.0), 0.5), 1.0, Vec2(0.0, 0.0), Vec2.zero(), 0.0, 0.0
    )
    body2 = Body(
        Circle(Vec2(1.0, 0.0), 0.5), 1.0, Vec2(1.0, 0.0), Vec2.zero(), 0.0, 0.0
    )

    # Create a revolute joint
    anchor = Vec2(0.5, 0.0)
    joint = RevoluteJoint(body1, body2, anchor)

    # Simulate a few steps
    time_step = 1.0 / 60.0
    for i in range(10):
        print(f"\nStep {i + 1}:")
        joint.pre_solve(time_step)
        print(f"Position error: {joint.anchor2 - joint.anchor1}")
        print(f"Bias: {joint.bias}")
        joint.solve_velocity_constraints(time_step)
        print(f"Accumulated impulse: {joint.impulse}")
        joint.solve_position_constraints()

        # Print the positions of the bodies
        print(f"Body1 position: {body1.position}, Body2 position: {body2.position}")


if __name__ == "__main__":
    test_revolute_joint()
