import numpy as np
from queue import SimpleQueue
from scipy.spatial import Delaunay
from libraries.triangle import Point, Triangle, compute_triangles_area
from algorithms.meshforrectangle import MeshForRectangle

class DelaunayTriangulation:
    def __init__(self, max_triangle_area = None):
        self.max_triangle_area = max_triangle_area
  
    def __triangulate(self, polygon_vertices):
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
      
    def triangulate(self, polygon_vertices):
        triangles = self.__triangulate(polygon_vertices)
        
        if (self.max_triangle_area != None):
            triangles = self.split_bad_triangles(triangles)
        
        return triangles
      
    def split_bad_triangles(self, triangles):
        bad_triangle_queue = SimpleQueue()
        good_triangles = []
        
        for triangle in triangles:
            if(self.is_bad(triangle)):
                bad_triangle_queue.put(triangle)
            else:
                good_triangles.append(triangle)
                
        while(not bad_triangle_queue.empty()):
            new_triangles = self.split_triangle(bad_triangle_queue.get())
            
            for triangle in new_triangles:
                if(self.is_bad(triangle)):
                    bad_triangle_queue.put(triangle)
                else:
                    good_triangles.append(triangle)
              
        return good_triangles
    
    def is_bad(self, triangle):
        return triangle.area() > self.max_triangle_area
      
    def split_triangle(self, triangle):
        new_triangles = []
        
        # if triangle has not an acute angle
        # ...
        
        return new_triangles
        
      
            
