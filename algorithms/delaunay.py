import numpy as np
import sys

from scipy.spatial import Delaunay
from libraries.triangle import Point, Triangle, compute_triangles_area


class DelaunayTriangulation:
    eps = 0.00000001
    _huge = sys.float_info.max
    _tiny = sys.float_info.min

    def triangulate(self, polygon_vertices, mesh_points=0):
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
