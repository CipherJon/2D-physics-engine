"""
SVG export tool for the physics engine.
This script exports visual representations of the physics simulation as SVG files.
"""

import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.core.body import Body
from src.core.circle import Circle
from src.core.polygon import Polygon
from src.math.vec2 import Vec2

def export_world_to_svg(world, filename: str = "simulation.svg") -> None:
    """
    Export the current state of the world to an SVG file.

    Args:
        world: The simulation world to export.
        filename (str): The name of the SVG file to create.
    """
    # Calculate the bounding box of the world
    min_x, min_y, max_x, max_y = calculate_world_bounds(world)

    # Add a margin to the bounding box
    margin = 10.0
    min_x -= margin
    min_y -= margin
    max_x += margin
    max_y += margin

    # Calculate the width and height of the SVG
    width = max_x - min_x
    height = max_y - min_y

    # Create the SVG header
    svg_content = [
        f'<svg width="{width}" height="{height}" viewBox="{min_x} {min_y} {width} {height}" xmlns="http://www.w3.org/2000/svg">'
    ]

    # Add a background rectangle
    svg_content.append(f'<rect x="{min_x}" y="{min_y}" width="{width}" height="{height}" fill="white" stroke="black" stroke-width="1"/>')

    # Add each body to the SVG
    for body in world.get_bodies():
        if isinstance(body.shape, Circle):
            svg_content.append(export_circle_to_svg(body, min_x, min_y))
        elif isinstance(body.shape, Polygon):
            svg_content.append(export_polygon_to_svg(body, min_x, min_y))

    # Close the SVG
    svg_content.append("</svg>")

    # Write the SVG content to the file
    with open(filename, "w") as f:
        f.write("\n".join(svg_content))

def calculate_world_bounds(world) -> tuple:
    """
    Calculate the bounding box of the world.

    Args:
        world: The simulation world.

    Returns:
        tuple: (min_x, min_y, max_x, max_y)
    """
    if not world.get_bodies():
        return (-10, -10, 10, 10)

    min_x = float("inf")
    min_y = float("inf")
    max_x = float("-inf")
    max_y = float("-inf")

    for body in world.get_bodies():
        if isinstance(body.shape, Circle):
            circle = body.shape
            min_x = min(min_x, body.position.x - circle.radius)
            min_y = min(min_y, body.position.y - circle.radius)
            max_x = max(max_x, body.position.x + circle.radius)
            max_y = max(max_y, body.position.y + circle.radius)
        elif isinstance(body.shape, Polygon):
            polygon = body.shape
            vertices = polygon.get_vertices()
            for vertex in vertices:
                min_x = min(min_x, vertex.x)
                min_y = min(min_y, vertex.y)
                max_x = max(max_x, vertex.x)
                max_y = max(max_y, vertex.y)

    return (min_x, min_y, max_x, max_y)

def export_circle_to_svg(body: Body, min_x: float, min_y: float) -> str:
    """
    Export a circle body to SVG.

    Args:
        body (Body): The body to export.
        min_x (float): The minimum x-coordinate of the world.
        min_y (float): The minimum y-coordinate of the world.

    Returns:
        str: The SVG representation of the circle.
    """
    circle = body.shape
    x = body.position.x - min_x
    y = body.position.y - min_y
    radius = circle.radius

    # Flip the y-coordinate to match SVG's coordinate system
    y = (max_y - min_y) - y

    return f'<circle cx="{x}" cy="{y}" r="{radius}" fill="blue" stroke="black" stroke-width="1"/>'

def export_polygon_to_svg(body: Body, min_x: float, min_y: float) -> str:
    """
    Export a polygon body to SVG.

    Args:
        body (Body): The body to export.
        min_x (float): The minimum x-coordinate of the world.
        min_y (float): The minimum y-coordinate of the world.

    Returns:
        str: The SVG representation of the polygon.
    """
    polygon = body.shape
    vertices = polygon.get_vertices()

    # Convert vertices to SVG coordinates
    svg_vertices = []
    for vertex in vertices:
        x = vertex.x - min_x
        y = vertex.y - min_y
        # Flip the y-coordinate to match SVG's coordinate system
        y = (max_y - min_y) - y
        svg_vertices.append(f"{x},{y}")

    vertices_str = " ".join(svg_vertices)

    return f'<polygon points="{vertices_str}" fill="green" stroke="black" stroke-width="1"/>'

def run_export_example() -> None:
    """
    Run an example export of a simple simulation.
    """
    from src.dynamics.world import World

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

    # Export the world to an SVG file
    export_world_to_svg(world, "example_simulation.svg")
    print("Exported simulation to example_simulation.svg")

if __name__ == "__main__":
    run_export_example()
