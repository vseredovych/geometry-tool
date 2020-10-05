import pygame

GREEN = (107, 228, 0)
WHITE = (255, 255, 255)


class DrawingTool:
    RADIUS = 5
    LINE_WIDTH = 1

    def __init__(self, screen, button_panel, x=0, y=80, width=600, length=800):
        self.board_screen = screen
        self.panel = button_panel
        self.drawing_board_x = x
        self.drawing_board_y = y
        self.drawing_board_width = width
        self.drawing_board_length = length

        self.polygon = []
        self.polygon_finished = False

        self.btn_polygon_draw_name = "draw"
        self.panel.add_button(self.btn_polygon_draw_name)

    def event_actions(self, event):
        mouse_pos = event.pos
        if self.panel.get(self.btn_polygon_draw_name).clicked(mouse_pos):
            self.__draw_button_clicked()

        elif (self.__is_pos_on_board(event.pos)
              and self.panel.get(self.btn_polygon_draw_name).state
              and not self.polygon_finished):

            self.__mouse_clicked(event)

    def draw_points(self, points_str):
        points = self.parse_input(points_str)
        for point in points:
            self.polygon.append(point)
            self.polygon_finished, self.polygon = self.__fix_polygon_end_points()

            if self.polygon_finished:
                self.panel.get(self.btn_polygon_draw_name).disable()

    def parse_input(self, points_str):
        points = []
        for point in points_str:
            t = point.split()
            points.append((int(t[0]), int(t[1])))
        return points

    def draw(self):
        self.__draw_polygon()

        if self.panel.get(self.btn_polygon_draw_name).state and not self.polygon_finished:
            self.__draw_line_animation()

        self.__draw_vertex_circles(self.polygon)

    def clear(self):
        self.panel.get(self.btn_polygon_draw_name).disable()
        self.polygon = []
        self.polygon_finished = False

    def get_polygon(self):
        return self.polygon

    def __mouse_clicked(self, event):
        self.polygon.append(event.pos)
        self.polygon_finished, self.polygon = self.__fix_polygon_end_points()

        if self.polygon_finished:
            self.panel.get(self.btn_polygon_draw_name).disable()

    def __draw_button_clicked(self):
        pass

    def __draw_vertex_circles(self, vertices):
        for vertex in vertices:
            pygame.draw.circle(self.board_screen, GREEN, vertex, self.RADIUS, self.RADIUS)

    def __fix_polygon_end_points(self):
        finished = False

        if len(self.polygon) < 2:
            return finished, self.polygon

        start = self.polygon[0]
        end = self.polygon[-1]

        start_end_distance = ((start[0] - end[0])**2 + (start[1] - end[1])**2) ** (1/2)

        if start_end_distance < self.RADIUS:
            self.polygon.pop(-1)
            self.polygon.append(self.polygon[0])
            finished = True

        return finished, self.polygon

    def __draw_polygon(self):
        if len(self.polygon) > 1:
            pygame.draw.aalines(self.board_screen, WHITE, False, self.polygon, self.RADIUS)
            self.__draw_vertex_circles(self.polygon)

    def __is_pos_on_board(self, mouse_pos):
        x = mouse_pos[0]
        y = mouse_pos[1]
        if (self.drawing_board_x < x < self.drawing_board_x + self.drawing_board_length and
                self.drawing_board_y < y < self.drawing_board_y + self.drawing_board_width):
            return True
        else:
            return False

    def __draw_line_animation(self):
        if len(self.polygon) < 1:
            return

        p1 = self.polygon[-1]
        p2 = pygame.mouse.get_pos()
        pygame.draw.line(self.board_screen, WHITE, p1, p2)
