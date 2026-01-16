#!/usr/bin/env python3
"""
Entry point for running physics engine examples.
This script allows you to run examples by specifying their names.
"""

import importlib
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m examples <example_name>")
        print("Available examples:")
        print("  - bullet")
        print("  - car")
        print("  - friction_test")
        print("  - joints_demo")
        print("  - ragdoll")
        print("  - simple_falling")
        print("  - stacking")
        print("  - stress_test")
        sys.exit(1)

    example_name = sys.argv[1]
    try:
        module = importlib.import_module(f"examples.{example_name}")
        module.main()
    except ModuleNotFoundError:
        print(f"Example '{example_name}' not found.")
        sys.exit(1)
    except AttributeError:
        print(f"Example '{example_name}' does not have a 'main' function.")
        sys.exit(1)


if __name__ == "__main__":
    main()
