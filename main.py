# main.py
from game.game_engine import GameEngine

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def main():
    game = GameEngine(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.run()

if __name__ == "__main__":
    main()
