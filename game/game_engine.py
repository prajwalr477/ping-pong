# game/game_engine.py
import pygame
from game.paddle import Paddle
from game.ball import Ball


class GameEngine:
    """Handles the main game logic, state transitions, and rendering."""

    def __init__(self, screen_width: int, screen_height: int):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Pong Game - Enhanced Version")
        self.clock = pygame.time.Clock()

        try:
            pygame.mixer.init()
            self.sounds = {
                "paddle": pygame.mixer.Sound("sounds/paddle_hit.wav"),
                "wall": pygame.mixer.Sound("sounds/wall_bounce.wav"),
                "score": pygame.mixer.Sound("sounds/score.wav"),
            }
        except Exception as e:
            print(f"[Audio Disabled] {e}")
            self.sounds = {}

        # Game entities
        paddle_width, paddle_height = 10, 100
        self.player = Paddle(30, screen_height // 2 - paddle_height // 2, paddle_width, paddle_height, 8)
        self.ai = Paddle(screen_width - 40, screen_height // 2 - paddle_height // 2, paddle_width, paddle_height, 7)
        self.ball = Ball(screen_width // 2, screen_height // 2, 15, 15, screen_width, screen_height)

        # Scores and state
        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.Font(None, 40)
        self.running = True

        # Start directly with replay menu
        self.state = "replay"  # replay → choose best of → start playing
        self.winner = None
        self.target_score = None

    # --- anywhere in GameEngine class (e.g., just below __init__) ---
    def play_sound(self, name: str):
        """Play a sound effect safely if loaded."""
        try:
            if name in self.sounds:
                self.sounds[name].play()
        except Exception:
            pass


    # -----------------------------------------------------
    # Reset functions
    # -----------------------------------------------------
    def reset(self):
        """Reset ball and paddle positions for next round."""
        self.ball.reset()
        self.player.y = self.screen.get_height() // 2 - self.player.height // 2
        self.ai.y = self.screen.get_height() // 2 - self.ai.height // 2

    def full_reset(self):
        """Reset entire game for a new match."""
        self.player_score = 0
        self.ai_score = 0
        self.winner = None
        self.reset()
        self.state = "playing"

    # -----------------------------------------------------
    # Core game logic
    # -----------------------------------------------------
    def handle_collisions(self):
        """Handle ball collisions and scoring."""
        self.ball.check_collision(self.player, self.ai, sound_callback=self.play_sound)

        if self.ball.x <= 0:
            self.ai_score += 1
            self.play_sound("score")
            self.reset()
        elif self.ball.x + self.ball.width >= self.screen.get_width():
            self.player_score += 1
            self.play_sound("score")
            self.reset()

        if self.target_score and (self.player_score >= self.target_score or self.ai_score >= self.target_score):
            self.winner = "Player" if self.player_score > self.ai_score else "AI"
            self.state = "game_over"

    def update_playing_state(self, keys):
        """Handle paddle movement and update the ball."""

        # --- Player Controls ---
        # Allow both Arrow keys and W/S keys simultaneously
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player.move(-self.player.speed, self.screen.get_height())
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player.move(self.player.speed, self.screen.get_height())

        # --- AI Movement ---
        self.ai.auto_track(self.ball, self.screen.get_height())

        # --- Ball Movement & Collisions ---
        self.ball.move(sound_callback=self.play_sound)
        self.handle_collisions()

    # -----------------------------------------------------
    # Rendering
    # -----------------------------------------------------
    def draw_scores(self):
        player_text = self.font.render(str(self.player_score), True, (255, 255, 255))
        ai_text = self.font.render(str(self.ai_score), True, (255, 255, 255))
        self.screen.blit(player_text, (self.screen.get_width() // 4, 20))
        self.screen.blit(ai_text, (3 * self.screen.get_width() // 4, 20))

    def draw_playing_state(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (255, 255, 255), self.player.rect())
        pygame.draw.rect(self.screen, (255, 255, 255), self.ai.rect())
        pygame.draw.ellipse(self.screen, (255, 255, 255), self.ball.rect())
        pygame.draw.aaline(self.screen, (255, 255, 255),
                           (self.screen.get_width() // 2, 0),
                           (self.screen.get_width() // 2, self.screen.get_height()))
        self.draw_scores()
        pygame.display.flip()

    def show_game_over(self):
        self.screen.fill((0, 0, 0))
        over_text = self.font.render(f"Game Over! Winner: {self.winner}", True, (255, 255, 255))
        next_text = self.font.render("Press SPACE for Replay Options", True, (200, 200, 200))
        self.screen.blit(over_text, (self.screen.get_width() // 2 - over_text.get_width() // 2,
                                     self.screen.get_height() // 2 - over_text.get_height() // 2))
        self.screen.blit(next_text, (self.screen.get_width() // 2 - next_text.get_width() // 2,
                                     self.screen.get_height() // 2 + 20))
        pygame.display.flip()

    def show_replay_menu(self):
        """Show Best of 3/5/7 menu at start and after each game."""
        self.screen.fill((0, 0, 0))
        title = self.font.render("Select Match Type:", True, (255, 255, 255))
        option3 = self.font.render("Press 3 for Best of 3", True, (200, 200, 200))
        option5 = self.font.render("Press 5 for Best of 5", True, (200, 200, 200))
        option7 = self.font.render("Press 7 for Best of 7", True, (200, 200, 200))
        exit_text = self.font.render("Press ESC to Exit", True, (200, 200, 200))

        screen_center = self.screen.get_height() // 2
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, screen_center - 80))
        self.screen.blit(option3, (self.screen.get_width() // 2 - option3.get_width() // 2, screen_center - 20))
        self.screen.blit(option5, (self.screen.get_width() // 2 - option5.get_width() // 2, screen_center + 20))
        self.screen.blit(option7, (self.screen.get_width() // 2 - option7.get_width() // 2, screen_center + 60))
        self.screen.blit(exit_text, (self.screen.get_width() // 2 - exit_text.get_width() // 2, screen_center + 120))
        pygame.display.flip()

    # -----------------------------------------------------
    # Main Loop
    # -----------------------------------------------------
    def run(self):
        """Main game loop."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # REPLAY MENU first (now also used for first startup)
                if self.state == "replay" and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        self.target_score = 2  # Best of 3
                        self.full_reset()
                    elif event.key == pygame.K_5:
                        self.target_score = 3  # Best of 5
                        self.full_reset()
                    elif event.key == pygame.K_7:
                        self.target_score = 4  # Best of 7
                        self.full_reset()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False

                elif self.state == "game_over" and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.state = "replay"
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        self.running = False

            # State updates
            if self.state == "playing":
                keys = pygame.key.get_pressed()
                self.update_playing_state(keys)
                self.draw_playing_state()
            elif self.state == "game_over":
                self.show_game_over()
            elif self.state == "replay":
                self.show_replay_menu()

            self.clock.tick(60)

        pygame.quit()
