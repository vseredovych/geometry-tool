import numpy as np


class Point:
    def __init__(self, x=0, y=0, angle=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __str__(self):
        return f"({self.x}, {self.y})"

    def get_cords(self):
        return self.x, self.y


class Triangle:
    def __init__(self, p1=Point(), p2=Point(), p3=Point()):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def __eq__(self, other):
        if self.p1 == other.p1 and self.p2 == other.p2 and self.p3 == other.p3:
            return True
        return False

    def __str__(self):
        return f"[ {self.p1}, {self.p2}, {self.p3} ]"

    def get_points(self):
        return [
            [self.p1.x, self.p1.y],
            [self.p2.x, self.p2.y],
            [self.p3.x, self.p3.y],
        ]


class PolygonConvexSplitter:
    def __contains_no_points(self, v1, v2, v3, polygon):
        """
        Check whether ear contains no other points
        :param v1, v2, v3: Point
        :param polygon: bool
        :return:
        """
        for point in polygon:
            if point in (v1, v2, v3):
                continue
            elif self.__is_point_inside(point, v1, v2, v3):
                return False
        return True

    def __is_point_inside(self, pt, v1, v2, v3):
        """
        Check whether the point is inside of triangle
        :param pt, v1, v2, v3: Point
        :return: bool
        """
        total_area = self.__triangle_area(v1, v2, v3)
        area1 = self.__triangle_area(pt, v1, v2)
        area2 = self.__triangle_area(pt, v1, v3)
        area3 = self.__triangle_area(pt, v2, v3)

        if area1 + area2 + area3 > total_area:
            return False
        else:
            return True

    def __is_convex(self, v1, v2, v3):
        """
        Check whether ear is convex (Angle < 180 degrees)
        :return: bool
        """
        if self.__signed_triangle_area(v1, v2, v3) > 0:
            return True
        else:
            return False

    def __triangle_area(self, v1, v2, v3):
        """
        Find the area of a triangle. This function uses the 1/2 determinant
        method. Given three points (x1, y1), (x2, y2), (x3, y3):
                    | x1 y1 1 |
        Area = .5 * | x2 y2 1 |
                    | x3 y3 1 |

        :param v1, v2, v3: Point
        :return: float
        """
        return np.abs(self.__signed_triangle_area(v1, v2, v3))

    def __signed_triangle_area(self, p1, p2, p3):
        """
        Gives a positive triangle area if vertices are listed in counterclockwise
        and negative area if vertices are listed clockwise.
                    | x1 y1 1 |
        Area = .5 * | x2 y2 1 |
                    | x3 y3 1 |
        :param p1, p2, p3: Point
        :return: float
        """
        return 1 / 2 * (
                (p2.x * p3.y - p2.y * p3.x) -
                (p1.x * p3.y - p1.y * p3.x) +
                (p1.x * p2.y - p1.y * p2.x)
        )

    def __is_polygon_convex(self, polygon):
        """
        Check whether polygon is convex
        :return: bool
        """
        if not polygon:
            return False

        convex = True

        for index, point in enumerate(polygon):
            prev_point_index = (index - 1) % len(polygon)
            prev_point = polygon[prev_point_index]
            next_point_index = (index + 1) % len(polygon)
            next_point = polygon[next_point_index]

            convex = convex and self.__is_convex(prev_point, point, next_point)

        return convex

    def __is_clockwise(self, polygon):
        """
        Determines whether polygon is in clockwise order by summing up determinants of all neighboring edges.
        If sum of such determinants > 0 than polygon vertices in clockwise order and if < 0 - counterclockwise.
        :param polygon: array, size(n, 2)
        :return:
        """
        det_sum = 0
        polygon_count = len(polygon)
        for i, _ in enumerate(polygon):
            point1 = polygon[i]
            point2 = polygon[(i + 1) % len(polygon)]
            det_sum += (point2.x - point1.x) * (point2.y + point1.y)
        return det_sum > 0

    def __do_intersect(self, p1, q1, p2, q2):
        o1 = self.__signed_triangle_area(p1, q1, p2) > 0
        o2 = self.__signed_triangle_area(p1, q1, q2) > 0
        o3 = self.__signed_triangle_area(p2, q2, p1) > 0
        o4 = self.__signed_triangle_area(p2, q2, q1) > 0

        if o1 != o2 and o3 != o4:
            return True;
        else:
            return False

    def __do_intersect(self, p1, q1, p2, q2):
        o1 = self.__signed_triangle_area(p1, q1, p2) > 0
        o2 = self.__signed_triangle_area(p1, q1, q2) > 0
        o3 = self.__signed_triangle_area(p2, q2, p1) > 0
        o4 = self.__signed_triangle_area(p2, q2, q1) > 0

        if o1 != o2 and o3 != o4:
            return True;
        else:
            return False

    def __do_intersect_with_edges(self, p1, q1, edges):
        intersect = False

        for edge in edges:
            p2 = edge[0]
            q2 = edge[1]

            if p1 == p2 or p1 == q2 or p2 == q1 or q1 == q2:
                continue

            intersect = intersect or self.__do_intersect(p1, q1, p2, q2)
        return intersect

    def __compute_angle(self, p1, p2, p3):
        a = np.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)
        b = np.sqrt((p2.x - p3.x) ** 2 + (p2.y - p3.y) ** 2)
        c = np.sqrt((p1.x - p3.x) ** 2 + (p1.y - p3.y) ** 2)

        if a == 0 or b == 0:
            return 180

        angle = (180 / 3) * np.arccos(
            (a ** 2 + b ** 2 - c ** 2) / (2 * a * b)
        )
        print(p1, p2, p3)
        print(a, b, c)
        if self.__is_convex(p1, p2, p3):
            return angle
        else:
            return 360 - angle

    def __get_vertex_type(self, p1, p2, p3):
        if p2.y > p1.y and p2.y > p3.y and self.__compute_angle(p1, p2, p3) < 180:
            return "start"
        elif p2.y > p1.y and p2.y > p3.y and self.__compute_angle(p1, p2, p3) > 180:
            return "split"
        elif p2.y <= p1.y and p2.y <= p3.y and self.__compute_angle(p1, p2, p3) < 180:
            return "end"
        elif p2.y <= p1.y and p2.y <= p3.y and self.__compute_angle(p1, p2, p3) > 180:
            return "merge"
        elif (p1.y >= p2.y > p3.y) or (p1.y < p2.y <= p3.y):
            return "regular"

    def __is_edge_exists(self, p1, p2, edges):
        if ([p1, p2] in edges or
                [p2, p1] in edges):
            return True
        else:
            return False

    def __is_vertex_lower(self, vertex, point, edges):
        if (
                point != vertex and
                vertex.y > point.y and
                not self.__is_edge_exists(point, vertex, edges) and
                not self.__do_intersect_with_edges(point, vertex, edges)
        ):
            return True
        else:
            return False

    def __is_vertex_higher(self, vertex, point, edges):
        if (
                point != vertex and
                vertex.y < point.y and
                not self.__is_edge_exists(point, vertex, edges) and
                not self.__do_intersect_with_edges(point, vertex, edges)
        ):
            return True
        else:
            return False

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

        if self.__is_clockwise(polygon):
            polygon.reverse()

        for point in polygon_vertices:
            polygon.append(Point(point[0], point[1]))

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
