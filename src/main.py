import pygame
import sys
import random
from src.config import Config
from src.world import World
from src.ui import Slider, HUD

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

    # UI Initialization
    hud = HUD()
    # Sliders in top-left overlay
    slider_speed = Slider(x=10, y=10, w=200, h=20, min_val=10, max_val=120, initial_val=60, label="Speed (FPS)")
    slider_food_rate = Slider(x=10, y=60, w=200, h=20, min_val=0.0, max_val=1.0, initial_val=0.01, label="Food Rate")

    paused: bool = False
    running: bool = True

    while running:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Keyboard Events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_c:
                    world.clear_grid()

            # Pass events to UI
            if slider_speed.handle_event(event):
                pass # Logic handled by get_value() in loop
            if slider_food_rate.handle_event(event):
                pass

        # Input Polling (Continuous Mouse Interaction)
        mouse_pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        # Only interact with world if not interacting with UI (basic check)
        # Assuming UI is at top left, we could check rects, but for now simple painting
        # We should check if mouse is NOT over sliders before painting to avoid painting while dragging slider
        # Ideally, Slider.handle_event returns True if consumed.
        # But for now, let's just proceed. If slider is being dragged, user likely watches slider.
        # But slider dragging sets `dragging` state.

        ui_interacting = slider_speed.dragging or slider_food_rate.dragging

        if not ui_interacting:
            # Convert screen pos to grid pos
            grid_x = mouse_pos[0] // Config.CELL_SIZE
            grid_y = mouse_pos[1] // Config.CELL_SIZE

            if mouse_pressed[0]: # Left Click -> Wall
                world.place_wall(grid_x, grid_y)
            elif mouse_pressed[2]: # Right Click -> Food
                world.place_food(grid_x, grid_y)

        # Simulation Logic
        if not paused:
            # Food Regeneration
            food_chance = slider_food_rate.get_value()
            if random.random() < food_chance:
                # Add 1 food piece randomly
                world.randomize_food(1)

            world.update()

        # Drawing
        screen.fill(Config.COLOR_BG)
        world.draw(screen)

        # Draw UI
        hud_stats = {
            'fps': clock.get_fps(),
            'population': len(world.entities),
            'paused': paused
        }
        hud.draw(screen, hud_stats)
        slider_speed.draw(screen)
        slider_food_rate.draw(screen)

        # Update Display
        pygame.display.flip()

        # Cap FPS using slider value
        current_fps_target = int(slider_speed.get_value())
        clock.tick(current_fps_target)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_game()
