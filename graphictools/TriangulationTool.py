import pygame
from algorithms.earclip import EarClipTriangulation
from algorithms.delaunay import DelaunayTriangulation
from algorithms.randommeshgenerator import RandomPointsTriangulation
from algorithms.meshforrectangle import MeshForRectangle
from libraries.triangle import compute_triangles_area

GREEN = (107, 228, 0)
WHITE = (255, 255, 255)


class TriangulationTool:
    LINE_WIDTH = 1
    TRIANGULATION_METHODS = {
        "delaunay": DelaunayTriangulation,
        "random": RandomPointsTriangulation,
        "structured": MeshForRectangle,
        "earclip": EarClipTriangulation
    }

    MESHES = ["random", "structured"]

    def __init__(self, screen, button_panel, text_position, method="earclip"):
        assert method in self.TRIANGULATION_METHODS.keys()

        self.board_screen = screen
        self.panel = button_panel
        self.text_position = text_position

        self.method = method
        self.algorithm = self.TRIANGULATION_METHODS[method]()

        self.polygon_area = 0
        self.triangulation = []
        self.font = pygame.font.SysFont('serif', 12)

        self.btn_triangulate_name = method
        self.panel.add_button(self.btn_triangulate_name)
        self.mesh_points = 0

    def event_actions(self, event, polygon, mesh_points=0):
        mouse_pos = event.pos
        self.mesh_points = mesh_points
        if self.panel.get(self.btn_triangulate_name).clicked(mouse_pos):
            self.__triangulate_button_clicked(polygon)

    def draw(self):
        self.__draw_triangulation()

    def clear(self):
        self.panel.get(self.btn_triangulate_name).disable()
        self.triangulation = []
        self.polygon_area = 0

    def __triangulate_button_clicked(self, polygon):
        if len(polygon) > 2 and (self.method in self.MESHES or not self.triangulation):
            fixed_polygon = [(x, -y) for x, y in polygon]
            if self.method in self.MESHES:
                if int(self.mesh_points) != 0:
                    self.triangulation = self.algorithm.triangulate(fixed_polygon, mesh_num=self.mesh_points)
            else:
                self.triangulation = self.algorithm.triangulate(fixed_polygon)

    def __draw_triangulation(self):
        if self.panel.get(self.btn_triangulate_name).state:
            for tr in self.triangulation:
                start_point = [tr.p1.x, abs(tr.p1.y)]
                end_point = [tr.p2.x, abs(tr.p2.y)]
                pygame.draw.aaline(self.board_screen, GREEN, start_point, end_point, self.LINE_WIDTH)

                start_point = [tr.p1.x, abs(tr.p1.y)]
                end_point = [tr.p3.x, abs(tr.p3.y)]
                pygame.draw.aaline(self.board_screen, GREEN, start_point, end_point, self.LINE_WIDTH)

                start_point = [tr.p2.x, abs(tr.p2.y)]
                end_point = [tr.p3.x, abs(tr.p3.y)]
                pygame.draw.aaline(self.board_screen, GREEN, start_point, end_point, self.LINE_WIDTH)

            # area_text = self.font.render(f'Polygon area: {self.polygon_area}', 1, GREEN)
            # self.board_screen.blit(area_text, self.text_position)

