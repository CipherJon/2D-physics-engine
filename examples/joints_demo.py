#!/usr/bin/env python3
"""
Example demonstrating various types of joints.
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
from src.constraints.distance import DistanceJoint
from src.debug.pygame_draw import PygameDraw
from src.dynamics.world import World
from src.math.vec2 import Vec2

def main():
    # Initialize Pygame
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Joints Demo")
    clock = pygame.time.Clock()

    # Create a world
    world = World(Vec2(0.0, 10.0))  # Gravity: (0, 10)

    # Create a static ground
    ground_shape = Polygon(
        [Vec2(-400, -10), Vec2(400, -10), Vec2(400, 0), Vec2(-400, 0)]
    )
    ground = Body(shape=ground_shape, is_static=True)
    world.add_body(ground)

    # Create a dynamic circle
    circle1_shape = Circle(Vec2(-10, 20), 2)
    circle1 = Body(shape=circle1_shape)
    world.add_body(circle1)

    # Create another dynamic circle
    circle2_shape = Circle(Vec2(10, 20), 2)
    circle2 = Body(shape=circle2_shape)
    world.add_body(circle2)

    # Connect the two circles with a distance joint
    distance_joint = DistanceJoint(circle1, circle2, Vec2(0, 0), Vec2(0, 0), 10.0)
    world.add_joint(distance_joint)

    # Create a static anchor point
    anchor_shape = Circle(Vec2(0, 30), 0.5)
    anchor = Body(shape=anchor_shape, is_static=True)
    world.add_body(anchor)

    # Connect the first circle to the anchor with a revolute joint
    revolute_joint = RevoluteJoint(anchor, circle1, Vec2(0, 30))
    world.add_joint(revolute_joint)

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
