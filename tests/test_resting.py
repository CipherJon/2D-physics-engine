import sys
from pathlib import Path

# Add the parent directory to the path so we can import from src
sys.path.append(str(Path(__file__).parent.parent))

from src.core.body import Body
from src.core.circle import Circle
from src.core.polygon import Polygon
from src.dynamics.world import World
from src.math.vec2 import Vec2


def test_resting_contact():
    """Minimal test for resting contact."""
    world = World(Vec2(0.0, 0.0))  # No gravity

    # Create ground
    ground = Body(
        shape=Polygon([Vec2(-10, -1), Vec2(10, -1), Vec2(10, 0), Vec2(-10, 0)]),
        is_static=True,
    )
    world.add_body(ground)

    # Create body resting on ground
    body = Body(shape=Circle(Vec2(0, 1), 1))
    body.velocity = Vec2(0, 0)
    world.add_body(body)

    print(f"Initial: body.position={body.position}, body.velocity={body.velocity}")

    # Step once
    world.step(1.0 / 60.0)

    print(f"After step: body.position={body.position}, body.velocity={body.velocity}")


if __name__ == "__main__":
    test_resting_contact()
