"""
Timer class for timing operations.

This module provides functionality for timing operations in the physics engine.
"""

import time


class Timer:
    """
    A class to time operations in the physics engine.

    Attributes:
        start_time (float): The start time of the timer.
        end_time (float): The end time of the timer.
        running (bool): Whether the timer is running.
    """

    def __init__(self):
        """
        Initialize a new Timer.
        """
        self.start_time = 0.0
        self.end_time = 0.0
        self.running = False

    def start(self):
        """
        Start the timer.
        """
        if not self.running:
            self.start_time = time.time()
            self.running = True

    def stop(self):
        """
        Stop the timer.
        """
        if self.running:
            self.end_time = time.time()
            self.running = False

    def reset(self):
        """
        Reset the timer.
        """
        self.start_time = 0.0
        self.end_time = 0.0
        self.running = False

    def elapsed(self):
        """
        Get the elapsed time.

        Returns:
            float: The elapsed time in seconds.
        """
        if self.running:
            return time.time() - self.start_time
        else:
            return self.end_time - self.start_time
