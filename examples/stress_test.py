#!/usr/bin/env python3
"""
Example demonstrating a stress test with many objects.
"""

import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

import pygame
from src.core.body import Body
from src.core.circle import Circle
from src.core.polygon import Polygon
from src.debug.pygame_draw import PygameDraw
from src.dynamics.world import World
from src.math.vec2 import Vec2

def main():
    # Initialize Pygame
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Stress Test Demo")
    clock = pygame.time.Clock()

    # Create a world
    world = World(Vec2(0.0, 10.0))  # Gravity: (0, 10)

    # Create a static ground
    ground_shape = Polygon(
        [Vec2(-400, -10), Vec2(400, -10), Vec2(400, 0), Vec2(-400, 0)]
    )
    ground = Body(shape=ground_shape, is_static=True)
    world.add_body(ground)

    # Create many dynamic circles for stress testing
    for i in range(20):
        for j in range(10):
            circle_shape = Circle(Vec2(-200 + i * 10, 50 + j * 10), 2)
            circle_body = Body(shape=circle_shape)
            world.add_body(circle_body)

    # Create a debugger to draw the simulation
    debugger = PygameDraw(screen_width, screen_height)

    # Main simulation loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill((0, 0, 0))

        # Step the simulation
        world.step(1.0 / 60.0)

        # Draw the simulation
        debugger.draw_world(world)

        # Update the display
        pygame.display.flip()
        clock.tick(60)

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
```

---

### Summary
I have generated the following example files for your physics engine:

1. **`__main__.py`**: Entry point for running examples.
2. **`bullet.py`**: Demonstrates a high-speed bullet.
3. **`car.py`**: Demonstrates a simple car with wheels.
4. **`friction_test.py`**: Demonstrates friction between objects.
5. **`joints_demo.py`**: Demonstrates various types of joints.
6. **`ragdoll.py`**: Demonstrates a ragdoll-like structure.
7. **`simple_falling.py`**: Demonstrates a simple falling object.
8. **`stacking.py`**: Demonstrates stacking multiple objects.
9. **`stress_test.py`**: Demonstrates a stress test with many objects.

Each example is designed to showcase different features of the physics engine, such as gravity, friction, joints, and collisions. You can run these examples using the `__main__.py` script or directly by executing the individual files.

To run an example, use the following command:
```bash
python -m examples <example_name>
```

For example:
```bash
python -m examples simple_falling
