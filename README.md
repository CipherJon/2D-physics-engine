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

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.