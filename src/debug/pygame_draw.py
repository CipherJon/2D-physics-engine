import pygame

from ..core.body import Body
from ..core.circle import Circle
from ..core.polygon import Polygon
from ..math.transform import Transform
from ..math.vec2 import Vec2


class PygameDraw:
    """
    A class to handle Pygame-based visualization for the physics engine.
    """

    def __init__(self, screen_width=800, screen_height=600, scale=10.0):
        """
        Initialize the Pygame visualization.

        Args:
            screen_width (int): The width of the Pygame screen.
            screen_height (int): The height of the Pygame screen.
            scale (float): The scale factor for converting physics units to screen pixels.
        """
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.scale = scale
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Physics Engine Visualization")
        self.clock = pygame.time.Clock()
        self.running = False

    def start(self):
        """
        Start the Pygame visualization loop.
        """
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((0, 0, 0))
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def draw_body(self, body: Body, color=(255, 255, 255)):
        """
        Draw a physics body.

        Args:
            body (Body): The body to draw.
            color (tuple): The color of the body (R, G, B).
        """
        if isinstance(body.shape, Circle):
            self.draw_circle(body.shape, body.transform, color)
        elif isinstance(body.shape, Polygon):
            self.draw_polygon(body.shape, body.transform, color)

    def draw_circle(self, circle: Circle, transform: Transform, color=(255, 255, 255)):
        """
        Draw a circle.

        Args:
            circle (Circle): The circle to draw.
            transform (Transform): The transformation of the circle.
            color (tuple): The color of the circle (R, G, B).
        """
        center = self._to_screen_coordinates(transform.transform_point(circle.center))
        radius = circle.radius * self.scale
        pygame.draw.circle(
            self.screen, color, (int(center.x), int(center.y)), int(radius), 2
        )

    def draw_polygon(
        self, polygon: Polygon, transform: Transform, color=(255, 255, 255)
    ):
        """
        Draw a polygon.

        Args:
            polygon (Polygon): The polygon to draw.
            transform (Transform): The transformation of the polygon.
            color (tuple): The color of the polygon (R, G, B).
        """
        vertices = [
            self._to_screen_coordinates(transform.transform_point(v))
            for v in polygon.vertices
        ]
        if len(vertices) > 0:
            pygame.draw.polygon(
                self.screen, color, [(int(v.x), int(v.y)) for v in vertices], 2
            )

    def draw_joint(self, joint, color=(255, 0, 0)):
        """
        Draw a joint.

        Args:
            joint: The joint to draw.
            color (tuple): The color of the joint (R, G, B).
        """
        if hasattr(joint, "anchor1") and hasattr(joint, "anchor2"):
            anchor1 = self._to_screen_coordinates(joint.anchor1)
            anchor2 = self._to_screen_coordinates(joint.anchor2)
            pygame.draw.line(
                self.screen,
                color,
                (int(anchor1.x), int(anchor1.y)),
                (int(anchor2.x), int(anchor2.y)),
                2,
            )

    def draw_aabb(self, aabb, color=(0, 255, 0)):
        """
        Draw an axis-aligned bounding box (AABB).

        Args:
            aabb: The AABB to draw.
            color (tuple): The color of the AABB (R, G, B).
        """
        min_vertex, max_vertex = aabb
        min_screen = self._to_screen_coordinates(min_vertex)
        max_screen = self._to_screen_coordinates(max_vertex)
        pygame.draw.rect(
            self.screen,
            color,
            (
                int(min_screen.x),
                int(min_screen.y),
                int(max_screen.x - min_screen.x),
                int(max_screen.y - min_screen.y),
            ),
            1,
        )

    def _to_screen_coordinates(self, point: Vec2):
        """
        Convert physics coordinates to screen coordinates.

        Args:
            point (Vec2): The point in physics coordinates.

        Returns:
            Vec2: The point in screen coordinates.
        """
        return Vec2(
            point.x * self.scale + self.screen_width // 2,
            -point.y * self.scale + self.screen_height // 2,
        )

    def render(self):
        """
        Render the current state of the visualization.
        """
        pygame.display.flip()

    def clear(self):
        """
        Clear the screen.
        """
        self.screen.fill((0, 0, 0))

    def stop(self):
        """
        Stop the Pygame visualization.
        """
        self.running = False
        pygame.quit()
