# game/paddle.py
import pygame

class Paddle:
    """Represents a player or AI paddle."""
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def move(self, dy: int, screen_height: int) -> None:
        """Move paddle vertically within screen bounds."""
        self.y += dy
        self.y = max(0, min(self.y, screen_height - self.height))

    def rect(self) -> pygame.Rect:
        """Return pygame.Rect representing the paddle."""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def auto_track(self, ball, screen_height: int) -> None:
        """Simple AI that smoothly follows the ball."""
        # Smoother tracking - not perfect
        if ball.y + ball.height / 2 < self.y + self.height / 2:
            self.move(-self.speed * 0.8, screen_height)
        elif ball.y + ball.height / 2 > self.y + self.height / 2:
            self.move(self.speed * 0.8, screen_height)
