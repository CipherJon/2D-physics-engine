import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent))

from src.core.body import Body
from src.core.circle import Circle
from src.core.polygon import Polygon
from src.dynamics.world import World
from src.math.vec2 import Vec2


def test_collision_response():
    """Test collision response between a body and ground."""
    world = World(Vec2(0.0, 10.0))  # Gravity

    # Create a static ground
    ground = Body(
        shape=Polygon([Vec2(-10, -1), Vec2(10, -1), Vec2(10, 0), Vec2(-10, 0)]),
        is_static=True,
        restitution=0.2,
    )
    world.add_body(ground)

    # Create a dynamic body
    body = Body(shape=Circle(Vec2(0, 1), 1), restitution=0.5)
    world.add_body(body)

    print(f"Initial body position: {body.position}")
    print(f"Initial body velocity: {body.velocity}")
    print(f"Body restitution: {body.restitution}")
    print(f"Ground restitution: {ground.restitution}")

    # Step once
    world.step(1.0 / 60.0)

    print(f"After one step:")
    print(f"Body position: {body.position}")
    print(f"Body velocity: {body.velocity}")


if __name__ == "__main__":
    test_collision_response()
