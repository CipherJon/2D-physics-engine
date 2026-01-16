"""
Benchmarking tool for the physics engine.
This script measures the performance of the physics engine by simulating
a varying number of bodies and constraints.
"""

import sys
import time
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.core.body import Body
from src.core.circle import Circle
from src.dynamics.world import World
from src.math.vec2 import Vec2


def benchmark_world_performance(num_bodies: int, num_steps: int = 100) -> float:
    """
    Benchmark the performance of the world with a given number of bodies.

    Args:
        num_bodies (int): The number of bodies to simulate.
        num_steps (int): The number of simulation steps to perform.

    Returns:
        float: The average time per step in seconds.
    """
    # Create a world with gravity
    world = World(Vec2(0.0, 10.0))

    # Add bodies to the world
    for i in range(num_bodies):
        body = Body(shape=Circle(Vec2(i * 2, 10), 1))
        world.add_body(body)

    # Warm-up: Run a few steps to allow the system to stabilize
    for _ in range(10):
        world.step(1.0 / 60.0)

    # Measure the time taken to perform the simulation steps
    start_time = time.time()
    for _ in range(num_steps):
        world.step(1.0 / 60.0)
    end_time = time.time()

    # Calculate the average time per step
    total_time = end_time - start_time
    average_time_per_step = total_time / num_steps

    return average_time_per_step


def benchmark_with_constraints(
    num_bodies: int, num_constraints: int, num_steps: int = 100
) -> float:
    """
    Benchmark the performance of the world with bodies and constraints.

    Args:
        num_bodies (int): The number of bodies to simulate.
        num_constraints (int): The number of constraints to add.
        num_steps (int): The number of simulation steps to perform.

    Returns:
        float: The average time per step in seconds.
    """
    # Create a world with gravity
    world = World(Vec2(0.0, 10.0))

    # Add bodies to the world
    bodies = []
    for i in range(num_bodies):
        body = Body(shape=Circle(Vec2(i * 2, 10), 1))
        world.add_body(body)
        bodies.append(body)

    # Add constraints (e.g., distance joints)
    for i in range(num_constraints):
        if i + 1 < num_bodies:
            from src.constraints.distance import DistanceJoint

            joint = DistanceJoint(bodies[i], bodies[i + 1], Vec2(0, 0), Vec2(0, 0))
            world.add_joint(joint)

    # Warm-up: Run a few steps to allow the system to stabilize
    for _ in range(10):
        world.step(1.0 / 60.0)

    # Measure the time taken to perform the simulation steps
    start_time = time.time()
    for _ in range(num_steps):
        world.step(1.0 / 60.0)
    end_time = time.time()

    # Calculate the average time per step
    total_time = end_time - start_time
    average_time_per_step = total_time / num_steps

    return average_time_per_step


def run_benchmark() -> None:
    """
    Run a series of benchmarks to measure the performance of the physics engine.
    """
    print("Running physics engine benchmarks...\n")

    # Benchmark with varying numbers of bodies
    body_counts = [10, 50, 100, 200, 500]
    for num_bodies in body_counts:
        avg_time = benchmark_world_performance(num_bodies)
        print(f"Bodies: {num_bodies}, Average time per step: {avg_time:.6f} seconds")

    print("\nBenchmarking with constraints...\n")

    # Benchmark with varying numbers of constraints
    constraint_counts = [10, 20, 50, 100]
    for num_constraints in constraint_counts:
        avg_time = benchmark_with_constraints(50, num_constraints)
        print(
            f"Constraints: {num_constraints}, Average time per step: {avg_time:.6f} seconds"
        )


if __name__ == "__main__":
    run_benchmark()
