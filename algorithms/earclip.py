import numpy as np
from pointsposition import *
from triangle import Point, Triangle

class EarClipTriangulation:
    """
    Polygon Triangulation with eear clipping method
    """
    def __is_ear(self, v1, v2, v3, polygon):
        return (triangle_area(v1, v2, v3) > 0 and
                contains_no_points(v1, v2, v3, polygon) and
                is_convex(v1, v2, v3) and
                all([(v in polygon) for v in [v1, v2, v3]]))


    def get_ears(self, polygon_vertices):
        """
        Perform triangulation of a given polygon by clipping all ears and returns triangles polygon consists of.
        :param polygon_vertices: array, size=(n, 2)
        :return:
        """
        polygon = []
        ear_triangles = []

        if is_clockwise(polygon):
            polygon.reverse()

        for point in polygon_vertices:
            polygon.append(Point(point[0], point[1]))

        for index, point in enumerate(polygon):
            prev_point_index = index - 1
            prev_point = polygon[prev_point_index]
            next_point_index = (index + 1) % len(polygon)
            next_point = polygon[next_point_index]

            if self.__is_ear(prev_point, point, next_point, polygon):
                triangle = Triangle(prev_point, point, next_point)
                ear_triangles.append(triangle)
        return ear_triangles

    def compute_triangles_area(self, triangles):
        area = 0
        for tr in triangles:
            area += tr.area()
        return area

    def triangulate(self, polygon_vertices):
        """
        Perform triangulation of a given polygon by clipping all ears and returns triangles polygon consists of.
        :param polygon_vertices: array, size=(n, 2)
        :return:
        """
        polygon = []
        triangles = []
        ear_triangles = []
        polygon_vertices = polygon_vertices

        for point in polygon_vertices:
            polygon.append(Point(point[0], point[1]))

        if is_clockwise(polygon):
            polygon.reverse()


        if polygon[0] == polygon[-1]:
            polygon.pop(-1)

        for index, point in enumerate(polygon):
            prev_point_index = index - 1
            prev_point = polygon[prev_point_index]
            next_point_index = (index + 1) % len(polygon)
            next_point = polygon[next_point_index]

            if self.__is_ear(prev_point, point, next_point, polygon):
                triangle = Triangle(prev_point, point, next_point)
                ear_triangles.append(triangle)

        while ear_triangles and len(polygon) >= 3:
            triangle = ear_triangles.pop(0)
            triangles.append(triangle)
            polygon.remove(triangle.p2)

            if len(polygon) > 3:
                prev_index = polygon.index(triangle.p1)
                next_index = polygon.index(triangle.p3)

                prev_vertex = polygon[prev_index - 1]
                next_vertex = polygon[(next_index + 1) % len(polygon)]

                group = [
                    (Triangle(prev_vertex, triangle.p1, triangle.p3)),
                    (Triangle(triangle.p1, triangle.p3, next_vertex))
                ]

                for triangle in group:
                    if self.__is_ear(triangle.p1, triangle.p2, triangle.p3, polygon):
                        if triangle not in ear_triangles:
                            ear_triangles.append(triangle)

            for triangle in ear_triangles:
                if not self.__is_ear(triangle.p1, triangle.p2, triangle.p3, polygon):
                    ear_triangles.remove(triangle)

        return triangles
