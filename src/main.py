import pygame
import sys
from src.config import Config
from src.world import World

def run_game() -> None:
    """
    Main entry point for the simulation.
    Initializes Pygame, creates the World, and runs the main loop.
    """
    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
    pygame.display.set_caption("SimLife")

    clock: pygame.time.Clock = pygame.time.Clock()
    world: World = World()

    # Initialize with some food
    world.randomize_food(Config.INITIAL_FOOD_COUNT)

    # Initialize population
    world.spawn_initial_population(Config.INITIAL_POPULATION)

    running: bool = True
    while running:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Logic Update
        world.update()

        # Drawing
        screen.fill(Config.COLOR_BG)
        world.draw(screen)

        # Update Display
        pygame.display.flip()

        # Cap FPS
        clock.tick(Config.FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_game()
