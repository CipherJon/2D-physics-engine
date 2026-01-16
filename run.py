#!/usr/bin/env python3
"""
Script to run the physics engine.
This script serves as a convenient way to execute the physics engine from the project root.
"""

import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent))

from src.main import main

if __name__ == "__main__":
    main()
