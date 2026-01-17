"""
Profiler class for performance profiling.

This module provides functionality for profiling the performance of the physics engine.
"""

import time
from collections import defaultdict


class Profiler:
    """
    A class to profile the performance of the physics engine.

    Attributes:
        timers (dict): A dictionary to store timing information.
        enabled (bool): Whether the profiler is enabled.
    """

    def __init__(self, enabled=True):
        """
        Initialize a new Profiler.

        Args:
            enabled (bool): Whether the profiler is enabled.
        """
        self.timers = defaultdict(float)
        self.enabled = enabled

    def start(self, key):
        """
        Start timing for a specific key.

        Args:
            key (str): The key to associate with the timing.
        """
        if not self.enabled:
            return

        self.timers[key] -= time.time()

    def stop(self, key):
        """
        Stop timing for a specific key.

        Args:
            key (str): The key to associate with the timing.
        """
        if not self.enabled:
            return

        self.timers[key] += time.time()

    def reset(self):
        """
        Reset all timing information.
        """
        self.timers.clear()

    def get_timing(self, key):
        """
        Get the timing information for a specific key.

        Args:
            key (str): The key to get the timing for.

        Returns:
            float: The timing information for the key.
        """
        return self.timers.get(key, 0.0)

    def print_timings(self):
        """
        Print all timing information.
        """
        if not self.enabled:
            print("Profiler is disabled.")
            return

        print("Profiler Timings:")
        for key, timing in self.timers.items():
            print(f"{key}: {timing:.6f} seconds")
