import pygame

GREEN = (107, 228, 0)
DARK_GREEN = (0, 40, 0)
LIGHT_GREEN = (171, 242, 109)
GREY = (179, 179, 179)
BLACK = (0, 0, 0)

class InputBox:
    FONT_SIZE = 13

    def __init__(self, x, y, width=25, length=50,
                 color_active=GREEN,
                 color_inactive=LIGHT_GREEN, text=""):

        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.color_active = color_active
        self.color_inactive = color_inactive
        self.text = str(text).encode("utf-8").decode("utf-8")

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

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.clicked(event.pos):
            return

        if event.type == pygame.KEYDOWN:
            if self.state:
                if event.key == pygame.K_RETURN:
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.unicode.isdigit():
                    self.text += event.unicode

    def toggle(self):
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
