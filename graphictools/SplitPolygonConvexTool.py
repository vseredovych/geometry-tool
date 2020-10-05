import pygame
from algorithms.polygonconvexsplitter import PolygonConvexSplitter

WHITE = (255, 255, 255)


class SplitPolygonConvexTool:
    LINE_WIDTH = 1

    def __init__(self, screen, button_panel):
        self.board_screen = screen
        self.panel = button_panel

        self.split_convex = PolygonConvexSplitter()

        self.diagonals = []

        self.btn_split_name = "split"
        self.panel.add_button(self.btn_split_name)

    def event_actions(self, event, polygon):
        mouse_pos = event.pos
        if self.panel.get(self.btn_split_name).clicked(mouse_pos):
            self.__split_button_clicked(polygon)

    def draw(self):
        self.__draw_convex_split()

    def clear(self):
        self.panel.get(self.btn_split_name).disable()
        self.diagonals = []

    def __split_button_clicked(self, polygon):
        if len(polygon) > 3 and not self.diagonals:
            fixed_polygon = [(x, -y) for x, y in polygon]
            self.diagonals = self.split_convex.split_to_convex(fixed_polygon)

    def __draw_convex_split(self):
        if self.panel.get(self.btn_split_name).state:
            for p1, p2 in self.diagonals:
                start_point = [p1.x, abs(p1.y)]
                end_point = [p2.x, abs(p2.y)]
                pygame.draw.aaline(self.board_screen, WHITE, start_point, end_point, self.LINE_WIDTH)
