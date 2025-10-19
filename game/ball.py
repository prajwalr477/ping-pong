# game/ball.py
import pygame
import random


class Ball:
    """Represents the game ball with movement, collision, and reset logic."""

    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.prev_x = x  # track previous x for swept collision
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])
        self.max_speed = 10

    def move(self, sound_callback=None) -> None:
        """Update ball position and handle wall collisions."""
        self.prev_x = self.x  # track previous x for swept collision
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top and bottom walls
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            if sound_callback:
                sound_callback("wall")

    def check_collision(self, player, ai, sound_callback=None) -> None:
        """Check and handle collisions with paddles (with swept collision fix)."""
        ball_rect = self.rect()
        player_rect = player.rect()
        ai_rect = ai.rect()

        # --- Swept collision: player paddle (moving left) ---
        if (
            self.velocity_x < 0
            and self.prev_x >= player_rect.right
            and self.x < player_rect.right
            and self.y + self.height > player_rect.top
            and self.y < player_rect.bottom
        ):
            self.x = player_rect.right
            self.velocity_x = abs(self.velocity_x)
            offset = (self.y + self.height / 2) - (player.y + player.height / 2)
            self.velocity_y = offset / (player.height / 4)
            self.increase_speed()
            if sound_callback:
                sound_callback("paddle")

        # --- Swept collision: AI paddle (moving right) ---
        elif (
            self.velocity_x > 0
            and self.prev_x + self.width <= ai_rect.left
            and self.x + self.width > ai_rect.left
            and self.y + self.height > ai_rect.top
            and self.y < ai_rect.bottom
        ):
            self.x = ai_rect.left - self.width
            self.velocity_x = -abs(self.velocity_x)
            offset = (self.y + self.height / 2) - (ai.y + ai.height / 2)
            self.velocity_y = offset / (ai.height / 4)
            self.increase_speed()
            if sound_callback:
                sound_callback("paddle")

        # --- Regular overlap collision (in case low speed or perfect overlap) ---
        elif ball_rect.colliderect(player_rect):
            self.velocity_x = abs(self.velocity_x)
            self.x = player_rect.right
            offset = (self.y + self.height / 2) - (player.y + player.height / 2)
            self.velocity_y = offset / (player.height / 4)
            self.increase_speed()
            if sound_callback:
                sound_callback("paddle")

        elif ball_rect.colliderect(ai_rect):
            self.velocity_x = -abs(self.velocity_x)
            self.x = ai_rect.left - self.width
            offset = (self.y + self.height / 2) - (ai.y + ai.height / 2)
            self.velocity_y = offset / (ai.height / 4)
            self.increase_speed()
            if sound_callback:
                sound_callback("paddle")

    def increase_speed(self) -> None:
        """Gradually increase speed after paddle hit."""
        self.velocity_x *= 1.05
        self.velocity_y *= 1.05

        # Clamp to max speed
        if abs(self.velocity_x) > self.max_speed:
            self.velocity_x = self.max_speed * (1 if self.velocity_x > 0 else -1)
        if abs(self.velocity_y) > self.max_speed:
            self.velocity_y = self.max_speed * (1 if self.velocity_y > 0 else -1)

    def reset(self) -> None:
        """Reset ball to center and reverse direction."""
        self.x = self.original_x
        self.y = self.original_y
        self.prev_x = self.x
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self) -> pygame.Rect:
        """Return pygame.Rect representing the ball."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
