import pygame

GREEN = (107, 228, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Button:
    STATELESS_TYPE = "stateless"
    STATEFUL_TYPE = "stateful"
    FONT_SIZE = 13

    def __init__(self, x, y, button_type=STATEFUL_TYPE, width=25, length=50,
                 color_active=GREEN, color_inactive=WHITE, text=""):

        assert button_type in (self.STATELESS_TYPE, self.STATEFUL_TYPE)

        self.x = x
        self.y = y
        self.button_type = button_type
        self.width = width
        self.length = length
        self.color_active = color_active
        self.color_inactive = color_inactive
        self.text = text[0].upper() + text[1:]

        self.font = pygame.font.SysFont('serif', self.FONT_SIZE)
        self.rect = pygame.Rect(self.x, self.y, length, width)
        self.state = False

    def draw(self, screen):
        if self.state:
            pygame.draw.rect(screen, self.color_active, self.rect)
        else:
            pygame.draw.rect(screen, self.color_inactive, self.rect)

        text_sprite = self.font.render(self.text, 1, BLACK)
        coordinates = self.__get_text_coordinates()
        screen.blit(text_sprite, coordinates)

    def toggle(self):
        if self.button_type == self.STATEFUL_TYPE:
            self.state = self.state ^ True

    def disable(self):
        self.state = False

    def enable(self):
        self.state = True

    def clicked(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.toggle()
            return True
        else:
            return False

    def __get_text_coordinates(self):
        text_length, text_height = self.font.size(self.text)
        return (
            self.x + (self.length - text_length) / 2,
            self.y + self.width / 2 - (text_height / 2)
        )
