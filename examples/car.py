#!/usr/bin/env python3
"""
Example demonstrating a simple car with wheels.
"""

import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

import pygame
from src.core.body import Body
from src.core.circle import Circle
from src.core.polygon import Polygon
from src.constraints.revolute import RevoluteJoint
from src.debug.pygame_draw import PygameDraw
from src.dynamics.world import World
from src.math.vec2 import Vec2

def main():
    # Initialize Pygame
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Car Demo")
    clock = pygame.time.Clock()

    # Create a world
    world = World(Vec2(0.0, 10.0))  # Gravity: (0, 10)

    # Create a static ground
    ground_shape = Polygon(
        [Vec2(-400, -10), Vec2(400, -10), Vec2(400, 0), Vec2(-400, 0)]
    )
    ground = Body(shape=ground_shape, is_static=True)
    world.add_body(ground)

    # Create a car body (chassis)
    chassis_shape = Polygon(
        [
            Vec2(-10, 0),
            Vec2(10, 0),
            Vec2(10, 5),
            Vec2(-10, 5),
        ]
    )
    chassis = Body(shape=chassis_shape, position=Vec2(0, 10))
    world.add_body(chassis)

    # Create two wheels
    wheel1_shape = Circle(Vec2(-8, -2), 3)
    wheel1 = Body(shape=wheel1_shape, mass=1.0)
    world.add_body(wheel1)

    wheel2_shape = Circle(Vec2(8, -2), 3)
    wheel2 = Body(shape=wheel2_shape, mass=1.0)
    world.add_body(wheel2)

    # Attach wheels to the chassis using revolute joints
    joint1 = RevoluteJoint(chassis, wheel1, Vec2(-8, -2))
    world.add_joint(joint1)

    joint2 = RevoluteJoint(chassis, wheel2, Vec2(8, -2))
    world.add_joint(joint2)

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

