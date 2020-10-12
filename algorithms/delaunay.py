import numpy as np
import sys

from scipy.spatial import Delaunay
from libraries.triangle import Point, Triangle, compute_triangles_area


class DelaunayTriangulation:
    eps = 0.00000001
    _huge = sys.float_info.max
    _tiny = sys.float_info.min

    def triangulate(self, polygon_vertices, mesh_points=0):
        res = self.generate_random_points(polygon_vertices, int(mesh_points))
        polygon_vertices += res

        points = np.array(polygon_vertices)
        triangulation = Delaunay(points)
        triangles = []
        
        for triangle in points[triangulation.simplices]:
            triangles.append(Triangle(
                Point(triangle[0][0], triangle[0][1]),
                Point(triangle[1][0], triangle[1][1]),
                Point(triangle[2][0], triangle[2][1]))
            )
        return triangles

    def generate_random_points(self, vertices, num):
        if num == 0:
            return []

        if vertices[0] == vertices[-1]:
            print("yes")
            vertices.pop(0)

        points_vertices = [Point(x, y) for x, y in vertices]
        vertices_array = np.array(vertices)

        max_x = np.max(vertices_array[:, 0])
        min_x = np.min(vertices_array[:, 0])
        max_y = np.max(vertices_array[:, 1])
        min_y = np.min(vertices_array[:, 1])

        generated_points = []

        while len(generated_points) <= num:
            point = [
                np.random.randint(low=min_x, high=max_x),
                np.random.randint(low=min_y, high=max_y)
            ]

            if point in vertices:
                continue

            # TODO Contyl
            if all([ abs(point[1] - y) < self.eps for _, y in vertices] ):
                continue

            if self.is_point_inside_polygon(points_vertices, Point(point[0], point[1])):
                generated_points.append(point)

        return generated_points

    def is_point_inside_polygon(self, polygon, point):
        counter = 0
        for i in range(len(polygon)):
            p1 = polygon[i]
            p2 = polygon[(i + 1) % len(polygon)]

            if self.ray_intersects_segment(p1, p2, point):
                counter = counter + 1

        if counter == 0 or counter % 2 == 0:
            return False
        else:
            return True

    def ray_intersects_segment(self, p1, p2, point):
        if p1.y > p2.y:
            buff = p1
            p1 = p2
            p2 = buff

        if point.y == p1.y or point.y == p2.y:
            point.y += self.eps

        if point.y > p2.y or point.y < p1.y or point.x > np.max([p1.x, p2.x]):
            return False
        else:
            if point.x < np.min([p1.x, p2.x]):
                return True
            else:
                if abs(p2.x - p1.x) > self._tiny:
                    m_edge = (p2.y - p1.y) / (p2.x - p1.x)
                else:
                    m_edge = self._huge

                if abs(point.x - p1.x) > self._tiny:
                    m_point = (point.y - p1.y) / (point.x - p1.x)
                else:
                    m_point = self._huge

                if m_point >= m_edge:
                    return True
                else:
                    return False
