import pygame
from src.config import Config

class Slider:
    def __init__(self, x: int, y: int, w: int, h: int, min_val: float, max_val: float, initial_val: float, label: str) -> None:
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.label = label
        self.dragging = False

        # UI Colors
        self.color_bg = (30, 30, 30)
        self.color_handle = (150, 150, 150)
        self.color_text = (255, 255, 255)

        # Font initialization (lazy load in draw if not done globally,
        # but better to init module font here if pygame is ready)
        if not pygame.font.get_init():
            pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 16)

    def draw(self, surface: pygame.Surface) -> None:
        # Draw Background
        pygame.draw.rect(surface, self.color_bg, self.rect)
        pygame.draw.rect(surface, (100, 100, 100), self.rect, 1) # Border

        # Calculate Handle Position
        range_val = self.max_val - self.min_val
        pct = (self.value - self.min_val) / range_val if range_val > 0 else 0
        handle_x = self.rect.x + (pct * self.rect.width)
        handle_rect = pygame.Rect(handle_x - 5, self.rect.y - 2, 10, self.rect.height + 4)

        # Draw Handle
        pygame.draw.rect(surface, self.color_handle, handle_rect)

        # Draw Label and Value
        val_str = f"{self.value:.2f}"
        text_surf = self.font.render(f"{self.label}: {val_str}", True, self.color_text)
        # Draw text above the slider
        surface.blit(text_surf, (self.rect.x, self.rect.y - 20))

    def handle_event(self, event: pygame.event.Event) -> bool:
        changed = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left click
                if self.rect.collidepoint(event.pos):
                    self.dragging = True
                    self.update_value(event.pos[0])
                    changed = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.update_value(event.pos[0])
                changed = True

        return changed

    def update_value(self, mouse_x: int) -> None:
        # Clamp mouse_x to slider rect
        if mouse_x < self.rect.x:
            mouse_x = self.rect.x
        elif mouse_x > self.rect.right:
            mouse_x = self.rect.right

        # Calculate value
        pct = (mouse_x - self.rect.x) / self.rect.width
        self.value = self.min_val + (pct * (self.max_val - self.min_val))

    def get_value(self) -> float:
        return self.value

class HUD:
    def __init__(self) -> None:
        if not pygame.font.get_init():
            pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 18)
        self.color_text = (255, 255, 255)

    def draw(self, surface: pygame.Surface, world_stats: dict) -> None:
        """
        Renders HUD info.
        world_stats expects keys: 'fps', 'population', 'paused'
        """
        fps = world_stats.get('fps', 0)
        pop = world_stats.get('population', 0)
        paused = world_stats.get('paused', False)

        lines = [
            f"FPS: {int(fps)}",
            f"Population: {pop}",
            f"State: {'PAUSED' if paused else 'RUNNING'}"
        ]

        x = Config.SCREEN_WIDTH - 150
        y = 10

        for line in lines:
            text_surf = self.font.render(line, True, self.color_text)
            surface.blit(text_surf, (x, y))
            y += 22
