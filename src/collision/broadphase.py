import sys

sys.path.append("/media/cipherjon/HDD/Repo/physics-engine/src")

from math.aabb import AABB
from math.vec2 import Vec2


class Broadphase:
    """
    A broad-phase collision detection system to efficiently narrow down potential colliding pairs.
    This implementation uses a simple sweep and prune algorithm.
    """

    def __init__(self):
        """
        Initialize the broad-phase collision detector.
        """
        self.aabbs = []  # List of AABBs for all bodies
        self.pairs = set()  # Set of potential colliding pairs

    def add_aabb(self, aabb):
        """
        Add an AABB to the broad-phase detector.

        Args:
            aabb (AABB): The AABB to add.
        """
        self.aabbs.append(aabb)

    def remove_aabb(self, aabb):
        """
        Remove an AABB from the broad-phase detector.

        Args:
            aabb (AABB): The AABB to remove.
        """
        if aabb in self.aabbs:
            self.aabbs.remove(aabb)

    def update(self):
        """
        Update the broad-phase detector to find potential colliding pairs.
        """
        self.pairs.clear()
        n = len(self.aabbs)

        # Sort AABBs by their left edge
        sorted_aabbs = sorted(self.aabbs, key=lambda aabb: aabb.lower_bound.x)

        for i in range(n):
            aabb_i = sorted_aabbs[i]
            for j in range(i + 1, n):
                aabb_j = sorted_aabbs[j]
                if aabb_i.upper_bound.x < aabb_j.lower_bound.x:
                    break  # No more overlaps for aabb_i
                if self._aabb_overlap(aabb_i, aabb_j):
                    # Add the pair in a sorted order to avoid duplicates
                    pair = tuple(sorted((id(aabb_i), id(aabb_j))))
                    self.pairs.add(pair)

    def _aabb_overlap(self, aabb1, aabb2):
        """
        Check if two AABBs overlap.

        Args:
            aabb1 (AABB): The first AABB.
            aabb2 (AABB): The second AABB.

        Returns:
            bool: True if the AABBs overlap, False otherwise.
        """
        return (
            aabb1.lower_bound.x <= aabb2.upper_bound.x
            and aabb1.upper_bound.x >= aabb2.lower_bound.x
            and aabb1.lower_bound.y <= aabb2.upper_bound.y
            and aabb1.upper_bound.y >= aabb2.lower_bound.y
        )

    def get_potential_pairs(self):
        """
        Get the potential colliding pairs.

        Returns:
            set: A set of tuples representing potential colliding pairs.
        """
        return self.pairs

    def clear(self):
        """
        Clear all AABBs and pairs from the broad-phase detector.
        """
        self.aabbs.clear()
        self.pairs.clear()
