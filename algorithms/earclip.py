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


class EarClipTriangulation:
    """
    Polygon Triangulation with eear clipping method
    """
    def __is_ear(self, v1, v2, v3, polygon):
        # and all([(v in polygon) for v in [v1, v2, v3]])
        if (self.__triangle_area(v1, v2, v3) > 0 and
                self.__contains_no_points(v1, v2, v3, polygon) and
                self.__is_convex(v1, v2, v3) and
                all([(v in polygon) for v in [v1, v2, v3]])):
            return True
        else:
            return False

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
        if not self.__is_clockwise((v1, v2, v3)) and self.__signed_triangle_area(v1, v2, v3) > 0:
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
        return 1/2 * np.abs(
            (v2.x * v3.y - v2.y * v3.x) -
            (v1.x * v3.y - v1.y * v3.x) +
            (v1.x * v2.y - v1.y * v2.x)
        )

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
        return 1/2 * (
            (p2.x * p3.y - p2.y * p3.x) -
            (p1.x * p3.y - p1.y * p3.x) +
            (p1.x * p2.y - p1.y * p2.x)
        )

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

    def get_ears(self, polygon_vertices):
        """
        Perform triangulation of a given polygon by clipping all ears and returns triangles polygon consists of.
        :param polygon_vertices: array, size=(n, 2)
        :return:
        """
        polygon = []
        triangles = []
        ear_triangles = []

        if self.__is_clockwise(polygon):
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
            area += self.__triangle_area(tr.p1, tr.p2, tr.p3)
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

        if self.__is_clockwise(polygon):
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
