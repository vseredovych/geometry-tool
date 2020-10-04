import pygame

from graphictools.ButtonsPanel import ButtonsPanel
from graphictools.DrawingTool import DrawingTool
from graphictools.TriangulationTool import TriangulationTool
from graphictools.SplitPolygonConvexTool import SplitPolygonConvexTool

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    MOUSEBUTTONDOWN
)

from libraries import pointsposition, triangle

GREEN = (107, 228, 0)
DARK_GREEN = (0, 40, 0)
LIGHT_GREEN = (171, 242, 109)
GREY = (179, 179, 179)
BLACK = (0, 0, 0)


class GeometryTool:
    DEFAULT_BOARD_WIDTH = 600
    DEFAULT_BOARD_LENGTH = 800
    DEFAULT_BOARD_COLOR = BLACK

    def __init__(self):
        pygame.init()
        self.running = False

        self.__initialize_board()

        self.drawing_tool = DrawingTool(self.board_screen, self.panel,
                                        x=0, y=50, width=self.board_width - 50, length=self.board_length)
        self.triangulation_tool = TriangulationTool(self.board_screen, self.panel, (self.board_length - 150, 20))
        self.split_polygon_tool = SplitPolygonConvexTool(self.board_screen, self.panel)

        pygame.init()

    def __initialize_board(self, board_width=DEFAULT_BOARD_WIDTH,
                           board_length=DEFAULT_BOARD_LENGTH,
                           color=DEFAULT_BOARD_COLOR):

        self.board_width = board_width
        self.board_length = board_length
        self.board_color = color

        self.font = pygame.font.SysFont('serif', 12)
        self.board_screen = pygame.display.set_mode([self.board_length, self.board_width])

        self.panel = ButtonsPanel(0, 0, width=50, length=self.board_length)

        self.btn_clear_name = "clear"
        self.panel.add_button(self.btn_clear_name, button_type='stateless')

    def __draw_buttons(self):
        self.panel.draw_panel(self.board_screen)

    def __reset_board(self):
        self.drawing_tool.clear()
        self.triangulation_tool.clear()
        self.split_polygon_tool.clear()

    def __clear_screen(self):
        self.board_screen.fill(BLACK)

    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False

                if event.type == MOUSEBUTTONDOWN:
                    if self.panel.get(self.btn_clear_name).clicked(event.pos):
                        self.__reset_board()

                    self.drawing_tool.event_actions(event)

                    if self.drawing_tool.polygon_finished:
                        self.triangulation_tool.event_actions(event, self.drawing_tool.polygon)
                        self.split_polygon_tool.event_actions(event, self.drawing_tool.polygon)

            self.__clear_screen()
            self.__draw_buttons()

            self.drawing_tool.draw()
            self.triangulation_tool.draw()
            self.split_polygon_tool.draw()

            pygame.display.flip()

        self.quit()

    def quit(self):
        pygame.quit()


if __name__ == '__main__':
    geometry_tool = GeometryTool()
    geometry_tool.run()
