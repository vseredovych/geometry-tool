import numpy as np
from scipy.spatial import Delaunay
from libraries.triangle import Point, Triangle

class DelaunayTriangulation:
    def triangulate(self, polygon_vertices):
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
