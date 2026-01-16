#!/usr/bin/env python3
"""
Example demonstrating a ragdoll-like structure using joints.
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
    pygame.display.set_caption("Ragdoll Demo")
    clock = pygame.time.Clock()

    # Create a world
    world = World(Vec2(0.0, 10.0))  # Gravity: (0, 10)

    # Create a static ground
    ground_shape = Polygon(
        [Vec2(-400, -10), Vec2(400, -10), Vec2(400, 0), Vec2(-400, 0)]
    )
    ground = Body(shape=ground_shape, is_static=True)
    world.add_body(ground)

    # Create a head
    head_shape = Circle(Vec2(0, 30), 3)
    head = Body(shape=head_shape)
    world.add_body(head)

    # Create a torso
    torso_shape = Polygon(
        [
            Vec2(-2, 20),
            Vec2(2, 20),
            Vec2(2, 25),
            Vec2(-2, 25),
        ]
    )
    torso = Body(shape=torso_shape)
    world.add_body(torso)

    # Connect head to torso
    head_joint = RevoluteJoint(head, torso, Vec2(0, 25))
    world.add_joint(head_joint)

    # Create arms
    left_arm_shape = Polygon(
        [
            Vec2(-5, 22),
            Vec2(-10, 22),
            Vec2(-10, 20),
            Vec2(-5, 20),
        ]
    )
    left_arm = Body(shape=left_arm_shape)
    world.add_body(left_arm)

    right_arm_shape = Polygon(
        [
            Vec2(5, 22),
            Vec2(10, 22),
            Vec2(10, 20),
            Vec2(5, 20),
        ]
    )
    right_arm = Body(shape=right_arm_shape)
    world.add_body(right_arm)

    # Connect arms to torso
    left_arm_joint = RevoluteJoint(torso, left_arm, Vec2(-2, 22))
    world.add_joint(left_arm_joint)

    right_arm_joint = RevoluteJoint(torso, right_arm, Vec2(2, 22))
    world.add_joint(right_arm_joint)

    # Create legs
    left_leg_shape = Polygon(
        [
            Vec2(-2, 15),
            Vec2(-2, 5),
            Vec2(-5, 5),
            Vec2(-5, 15),
        ]
    )
    left_leg = Body(shape=left_leg_shape)
    world.add_body(left_leg)

    right_leg_shape = Polygon(
        [
            Vec2(2, 15),
            Vec2(2, 5),
            Vec2(5, 5),
            Vec2(5, 15),
        ]
    )
    right_leg = Body(shape=right_leg_shape)
    world.add_body(right_leg)

    # Connect legs to torso
    left_leg_joint = RevoluteJoint(torso, left_leg, Vec2(-2, 15))
    world.add_joint(left_leg_joint)

    right_leg_joint = RevoluteJoint(torso, right_leg, Vec2(2, 15))
    world.add_joint(right_leg_joint)

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
