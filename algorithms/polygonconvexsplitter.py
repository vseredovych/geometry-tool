import numpy as np
from triangle import Point, triangle_area, signed_triangle_area
from pointsposition import compute_angle, is_clockwise

class PolygonConvexSplitter:
    def __do_intersect(self, p1, q1, p2, q2):
        o1 = signed_triangle_area(p1, q1, p2) > 0
        o2 = signed_triangle_area(p1, q1, q2) > 0
        o3 = signed_triangle_area(p2, q2, p1) > 0
        o4 = signed_triangle_area(p2, q2, q1) > 0

        return o1 != o2 and o3 != o4

    def __do_intersect_with_edges(self, p1, q1, edges):
        intersect = False

        for edge in edges:
            p2 = edge[0]
            q2 = edge[1]

            if p1 == p2 or p1 == q2 or p2 == q1 or q1 == q2:
                continue

            intersect = intersect or self.__do_intersect(p1, q1, p2, q2)
        return intersect

    def __get_vertex_type(self, p1, p2, p3):
        if p2.y > p1.y and p2.y > p3.y and compute_angle(p1, p2, p3) < 180:
            return "start"
        elif p2.y > p1.y and p2.y > p3.y and compute_angle(p1, p2, p3) > 180:
            return "split"
        elif p2.y <= p1.y and p2.y <= p3.y and compute_angle(p1, p2, p3) < 180:
            return "end"
        elif p2.y <= p1.y and p2.y <= p3.y and compute_angle(p1, p2, p3) > 180:
            return "merge"
        elif (p1.y >= p2.y > p3.y) or (p1.y < p2.y <= p3.y):
            return "regular"

    def __is_edge_exists(self, p1, p2, edges):
        return [p1, p2] in edges or [p2, p1] in edges

    def __is_vertex_lower(self, vertex, point, edges):
        return (point != vertex and
                vertex.y > point.y and
                not self.__is_edge_exists(point, vertex, edges) and
                not self.__do_intersect_with_edges(point, vertex, edges))

    def __is_vertex_higher(self, vertex, point, edges):
        return (point != vertex and
                vertex.y < point.y and
                not self.__is_edge_exists(point, vertex, edges) and
                not self.__do_intersect_with_edges(point, vertex, edges))
    

    def __get_closest_vertex_higher(self, polygon, edges, vertex):
        closest = Point(0, 0)

        for point in polygon:
            if self.__is_vertex_higher(vertex, point, edges):
                closest = point
                min_dist = abs(point.y - vertex.y)

        for point in polygon:
            if (self.__is_vertex_higher(vertex, point, edges) and
                    abs(point.y - vertex.y) < min_dist):
                closest = point
                min_dist = abs(point.y - vertex.y)
        return closest

    def __get_closest_vertex_lower(self, polygon, edges, vertex):
        closest = Point(0, 0)

        for point in polygon:
            if self.__is_vertex_lower(vertex, point, edges):
                closest = point
                min_dist = abs(point.y - vertex.y)

        for point in polygon:
            if (self.__is_vertex_lower(vertex, point, edges) and
                    abs(point.y - vertex.y) < min_dist):
                closest = point
                min_dist = abs(point.y - vertex.y)
        return closest

    def split_to_convex(self, polygon_vertices):
        """
        Perform triangulation of a given polygon by clipping all ears and returns triangles polygon consists of.
        :param polygon_vertices: array, size=(n, 2)
        :return:
        """
        polygon = []
        polygon_vertices = polygon_vertices

        for point in polygon_vertices:
            polygon.append(Point(point[0], point[1]))

        if is_clockwise(polygon):
            polygon.reverse()

        if polygon[0] == polygon[-1]:
            polygon.pop(-1)

        edges = []
        for index, point in enumerate(polygon):
            next_point_index = (index + 1) % len(polygon)
            next_point = polygon[next_point_index]

            edges.append([point, next_point])

        diagonals = []
        split = []
        merge = []
        for index, point in enumerate(polygon):
            prev_point_index = index - 1
            prev_point = polygon[prev_point_index]

            next_point_index = (index + 1) % len(polygon)
            next_point = polygon[next_point_index]

            vertex_type = self.__get_vertex_type(prev_point, point, next_point)
            if vertex_type == "split":
                closest = self.__get_closest_vertex_higher(polygon, edges, point)
                diagonals.append([point, closest])
                split.append(point)
            elif vertex_type == "merge":
                closest = self.__get_closest_vertex_lower(polygon, edges, point)
                diagonals.append([point, closest])
                merge.append(point)

        return diagonals


straight = Point(0, 5)
p = Point(0, -5)

dist_to_p = abs(p.y - straight.y)
print(dist_to_p)

# star = [(150, 25), (179, 111), (269, 111), (197, 165), (223, 251), (150, 200), (77, 251), (103, 165), (31, 111), (121, 111)]
# leave = [(1, -3), (5, -4), (4, -3), (9, 1), (7, 2), (8, 5), (5, 4), (5, 5), (3, 4), (4, 9), (2, 7), (0, 10), (-2, 7), (-4, 8), (-3, 3), (-5, 6), (-5, 4), (-8, 5), (-7, 2), (-9, 1), (-4, -3), (-5, -4), (0, -3), (2, -7), (2, -6), (1, -3)]
# p = [Point(1, 1), Point(3, -1.5), Point(5, 1), Point(5, 5), Point(3, 3), Point(1, 5)]
p = [(1, 1), (3, -1.5), (5, 1), (5, 5), (3, 3), (1, 5)]

import matplotlib.pyplot as plt


def draw(poly):
    aa = []
    for i in range(0, len(poly)):
        a = poly[i], poly[(i + 1) % len(poly)]
        aa.append(a)
        plt.plot([a[0][0], a[1][0]], [a[0][1], a[1][1]], "r")
    plt.show()

#
# # draw(p)
# #
# splitter = PolygonConvexSplitter()
# # #
# res = splitter.split_to_convex(p)
# [print(str(x)) for x in res]
#
# # a = [Point(1, 1), Point(6, 6)]
# # b = [Point(1, 10), Point(10, 1)]
# # print(splitter.do_intersect(a[0], a[1], b[0], b[1]))
