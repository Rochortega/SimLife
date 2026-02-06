class Config:
    """
    Configuration constants for SimLife.
    """
    SCREEN_WIDTH: int = 1280
    SCREEN_HEIGHT: int = 720
    CELL_SIZE: int = 8
    FPS: int = 60

    INITIAL_FOOD_COUNT: int = 500

    # Colors (R, G, B)
    COLOR_BG: tuple[int, int, int] = (10, 10, 10)       # Background (Dark, not pure black)
    COLOR_WALL: tuple[int, int, int] = (100, 100, 100)  # Wall color
    COLOR_FOOD: tuple[int, int, int] = (50, 200, 50)    # Food color

    # Grid Cell Types
    CELL_EMPTY: int = 0
    CELL_WALL: int = 1
    CELL_FOOD: int = 2
