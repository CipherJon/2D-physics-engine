"""
Scene editor tool for the physics engine.
This script provides a simple interface for creating or editing simulation scenes.
"""

import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.constraints.distance import DistanceJoint
from src.constraints.revolute import RevoluteJoint
from src.core.body import Body
from src.core.circle import Circle
from src.core.polygon import Polygon
from src.dynamics.world import World
from src.math.vec2 import Vec2


def create_scene() -> World:
    """
    Create a simple scene with a ground and a few dynamic bodies.

    Returns:
        World: The simulation world with the scene.
    """
    # Create a world with gravity
    world = World(Vec2(0.0, 10.0))

    # Add a static ground
    ground = Body(
        shape=Polygon([Vec2(-10, -1), Vec2(10, -1), Vec2(10, 0), Vec2(-10, 0)]),
        is_static=True,
    )
    world.add_body(ground)

    # Add a dynamic circle
    circle = Body(shape=Circle(Vec2(0, 5), 1))
    world.add_body(circle)

    # Add a dynamic polygon
    polygon = Body(shape=Polygon([Vec2(-1, 3), Vec2(1, 3), Vec2(1, 5), Vec2(-1, 5)]))
    world.add_body(polygon)

    # Add a distance joint between the circle and polygon
    joint = DistanceJoint(circle, polygon, Vec2(0, 0), Vec2(0, 0))
    world.add_joint(joint)

    return world


def edit_scene(world: World) -> None:
    """
    Edit the scene by adding or removing bodies and joints.

    Args:
        world (World): The simulation world to edit.
    """
    print("Editing the scene...")
    print("1. Add a body")
    print("2. Remove a body")
    print("3. Add a joint")
    print("4. Remove a joint")
    print("5. Exit")

    while True:
        choice = input("Enter your choice: ")
        if choice == "1":
            add_body(world)
        elif choice == "2":
            remove_body(world)
        elif choice == "3":
            add_joint(world)
        elif choice == "4":
            remove_joint(world)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")


def add_body(world: World) -> None:
    """
    Add a body to the world.

    Args:
        world (World): The simulation world.
    """
    print("Select the shape of the body:")
    print("1. Circle")
    print("2. Polygon")

    shape_choice = input("Enter your choice: ")
    if shape_choice == "1":
        radius = float(input("Enter the radius of the circle: "))
        x = float(input("Enter the x-coordinate of the circle: "))
        y = float(input("Enter the y-coordinate of the circle: "))
        body = Body(shape=Circle(Vec2(x, y), radius))
    elif shape_choice == "2":
        print("Enter the vertices of the polygon (e.g., x1 y1 x2 y2 ...):")
        vertices_input = input("Vertices: ")
        vertices = [float(v) for v in vertices_input.split()]
        vertices_list = [
            Vec2(vertices[i], vertices[i + 1]) for i in range(0, len(vertices), 2)
        ]
        body = Body(shape=Polygon(vertices_list))
    else:
        print("Invalid choice. Body not added.")
        return

    world.add_body(body)
    print("Body added successfully.")


def remove_body(world: World) -> None:
    """
    Remove a body from the world.

    Args:
        world (World): The simulation world.
    """
    bodies = world.get_bodies()
    if not bodies:
        print("No bodies in the world.")
        return

    print("Select a body to remove:")
    for i, body in enumerate(bodies):
        print(f"{i + 1}. {body}")

    body_choice = input("Enter your choice: ")
    try:
        body_index = int(body_choice) - 1
        if 0 <= body_index < len(bodies):
            world.remove_body(bodies[body_index])
            print("Body removed successfully.")
        else:
            print("Invalid choice. Body not removed.")
    except ValueError:
        print("Invalid choice. Body not removed.")


def add_joint(world: World) -> None:
    """
    Add a joint to the world.

    Args:
        world (World): The simulation world.
    """
    bodies = world.get_bodies()
    if len(bodies) < 2:
        print("Not enough bodies to create a joint.")
        return

    print("Select the type of joint:")
    print("1. Distance Joint")
    print("2. Revolute Joint")

    joint_choice = input("Enter your choice: ")
    if joint_choice == "1":
        print("Select the first body:")
        for i, body in enumerate(bodies):
            print(f"{i + 1}. {body}")
        body1_choice = int(input("Enter your choice: ")) - 1

        print("Select the second body:")
        for i, body in enumerate(bodies):
            print(f"{i + 1}. {body}")
        body2_choice = int(input("Enter your choice: ")) - 1

        if 0 <= body1_choice < len(bodies) and 0 <= body2_choice < len(bodies):
            body1 = bodies[body1_choice]
            body2 = bodies[body2_choice]
            joint = DistanceJoint(body1, body2, Vec2(0, 0), Vec2(0, 0))
            world.add_joint(joint)
            print("Distance joint added successfully.")
        else:
            print("Invalid choice. Joint not added.")
    elif joint_choice == "2":
        print("Select the first body:")
        for i, body in enumerate(bodies):
            print(f"{i + 1}. {body}")
        body1_choice = int(input("Enter your choice: ")) - 1

        print("Select the second body:")
        for i, body in enumerate(bodies):
            print(f"{i + 1}. {body}")
        body2_choice = int(input("Enter your choice: ")) - 1

        x = float(input("Enter the x-coordinate of the anchor point: "))
        y = float(input("Enter the y-coordinate of the anchor point: "))

        if 0 <= body1_choice < len(bodies) and 0 <= body2_choice < len(bodies):
            body1 = bodies[body1_choice]
            body2 = bodies[body2_choice]
            joint = RevoluteJoint(body1, body2, Vec2(x, y))
            world.add_joint(joint)
            print("Revolute joint added successfully.")
        else:
            print("Invalid choice. Joint not added.")
    else:
        print("Invalid choice. Joint not added.")


def remove_joint(world: World) -> None:
    """
    Remove a joint from the world.

    Args:
        world (World): The simulation world.
    """
    joints = world.get_joints()
    if not joints:
        print("No joints in the world.")
        return

    print("Select a joint to remove:")
    for i, joint in enumerate(joints):
        print(f"{i + 1}. {joint}")

    joint_choice = input("Enter your choice: ")
    try:
        joint_index = int(joint_choice) - 1
        if 0 <= joint_index < len(joints):
            world.remove_joint(joints[joint_index])
            print("Joint removed successfully.")
        else:
            print("Invalid choice. Joint not removed.")
    except ValueError:
        print("Invalid choice. Joint not removed.")


def run_scene_editor() -> None:
    """
    Run the scene editor to create or edit a simulation scene.
    """
    print("Welcome to the Physics Engine Scene Editor!")
    print("1. Create a new scene")
    print("2. Edit an existing scene")

    choice = input("Enter your choice: ")
    if choice == "1":
        world = create_scene()
    elif choice == "2":
        world = create_scene()  # For simplicity, start with a new scene
    else:
        print("Invalid choice. Exiting.")
        return

    edit_scene(world)
    print("Scene editing complete.")


if __name__ == "__main__":
    run_scene_editor()
