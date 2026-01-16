#!/usr/bin/env python3
"""
Example demonstrating a bullet-like object moving at high speed.
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
    pygame.display.set_caption("Bullet Demo")
    clock = pygame.time.Clock()

    # Create a world
    world = World(Vec2(0.0, 10.0))  # Gravity: (0, 10)

    # Create a static ground
    ground_shape = Polygon(
        [Vec2(-400, -10), Vec2(400, -10), Vec2(400, 0), Vec2(-400, 0)]
    )
    ground = Body(shape=ground_shape, is_static=True)
    world.add_body(ground)

    # Create a bullet (small, fast-moving circle)
    bullet_shape = Circle(Vec2(-300, 10), 0.5)
    bullet_body = Body(shape=bullet_shape, mass=0.1)
    bullet_body.velocity = Vec2(50.0, 0.0)  # High horizontal velocity
    world.add_body(bullet_body)

    # Create a target (static polygon)
    target_shape = Polygon([Vec2(300, 0), Vec2(350, 0), Vec2(350, 50), Vec2(300, 50)])
    target = Body(shape=target_shape, is_static=True)
    world.add_body(target)

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
