# Physics Engine

A 2D physics engine written in Python. This project provides a framework for simulating rigid body dynamics, collision detection, and constraints.

## Features

- **Rigid Body Dynamics**: Simulate the motion of rigid bodies under forces like gravity.
- **Collision Detection**: Broad-phase and narrow-phase collision detection using AABB and SAT (Separating Axis Theorem).
- **Constraints and Joints**: Support for distance joints, revolute joints, and more. Recent improvements include better initialization and error handling for joints.
- **Visualization**: Debugging and visualization tools using Pygame.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/physics-engine.git
   cd physics-engine
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running Examples

The project includes several examples to demonstrate the capabilities of the physics engine. To run an example:

```bash
python -m examples.simple_falling
```

### Creating a Custom Simulation

Here's a simple example of how to create a custom simulation:

```python
from src.dynamics.world import World
from src.core.body import Body
from src.core.circle import Circle
from src.math.vec2 import Vec2

# Create a world
world = World(gravity=Vec2(0.0, -9.81))

# Create a body with a circular shape
circle = Circle(center=Vec2(0.0, 10.0), radius=1.0)
body = Body(shape=circle, mass=1.0)

# Add the body to the world
world.add_body(body)

# Step the simulation
for _ in range(100):
    world.step()
```

## Project Structure

- `src/`: Core source code for the physics engine.
  - `collision/`: Collision detection algorithms.
  - `constraints/`: Joint and constraint implementations.
  - `core/`: Core physics classes (e.g., bodies, shapes).
  - `debug/`: Debugging and visualization tools.
  - `dynamics/`: Dynamics and world simulation.
  - `math/`: Mathematical utilities (e.g., vectors, matrices).
- `examples/`: Example simulations.
- `tests/`: Unit tests.
- `docs/`: Documentation.
- `tools/`: Utility tools for benchmarking, visualization, and scene editing.
  - `benchmark.py`: Measure the performance of the physics engine.
  - `export_svg.py`: Export simulation scenes as SVG files.
  - `scene_editor.py`: Create or edit simulation scenes interactively.

## Tools

The `tools/` directory contains utility scripts to assist with development, debugging, and visualization:

### Benchmarking

To measure the performance of the physics engine, run:

```bash
python tools/benchmark.py
```

This script simulates varying numbers of bodies and constraints and reports the average time per step.

### Exporting to SVG

To export a simulation scene as an SVG file, run:

```bash
python tools/export_svg.py
```

This script creates a visual representation of the current state of the simulation, which can be useful for documentation or debugging.

### Scene Editor

To interactively create or edit a simulation scene, run:

```bash
python tools/scene_editor.py
```

This script provides a simple interface for adding or removing bodies and joints, making it easier to set up complex simulations.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.