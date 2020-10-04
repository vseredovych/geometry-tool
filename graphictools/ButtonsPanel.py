import pygame
from graphictools.Button import Button

GREEN = (107, 228, 0)
DARK_GREEN = (0, 40, 0)
LIGHT_GREEN = (171, 242, 109)
GREY = (179, 179, 179)


class ButtonsPanel:
    DEFAULT_GAP = 20
    DEFAULT_BUTTON_WIDTH = 30
    DEFAULT_BUTTON_LENGTH = 60
    DEFAULT_ACTIVE_COLOR = GREEN
    DEFAULT_INACTIVE_COLOR = LIGHT_GREEN
    DEFAULT_PANEL_COLOR = DARK_GREEN

    def __init__(self, x, y, width=50, length=800,
                 default_gap=DEFAULT_GAP,
                 default_button_width=DEFAULT_BUTTON_WIDTH,
                 default_button_length=DEFAULT_BUTTON_LENGTH,
                 default_active_color=DEFAULT_ACTIVE_COLOR,
                 default_inactive_color=DEFAULT_INACTIVE_COLOR,
                 default_panel_color=DEFAULT_PANEL_COLOR):

        self.width = width
        self.length = length
        self.default_gap = default_gap
        self.default_button_width = default_button_width
        self.default_button_length = default_button_length
        self.default_active_color = default_active_color
        self.default_inactive_color = default_inactive_color
        self.default_panel_color = default_panel_color

        self.buttons = {}
        self.x_position = x + default_gap
        self.y_position = y + default_gap / 2
        self.rect = pygame.Rect(x, y, length, width)

    def add_button(self, name, button_type="stateful", gap=DEFAULT_GAP, width=DEFAULT_BUTTON_WIDTH,
                   length=DEFAULT_BUTTON_LENGTH):
        button = {
            name: Button(self.x_position, self.y_position,
                         button_type=button_type, width=width,
                         length=length, text=name,
                         color_active=self.default_active_color,
                         color_inactive=self.default_inactive_color)
        }
        self.buttons.update(button)

        self.x_position = self.x_position + length + gap

    def draw_panel(self, screen):
        pygame.draw.rect(screen, self.default_panel_color, self.rect)
        for val in self.buttons.values():
            val.draw(screen)

    def disable_buttons(self):
        for button in self.buttons.values():
            button.disable()

    def get(self, name):
        return self.buttons[name]
