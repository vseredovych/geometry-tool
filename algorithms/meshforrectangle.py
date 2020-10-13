from libraries.triangle import Triangle, Point

class MeshForRectangle:
    def __init__(self, nx=10, ny=10):
        # number of splits by OX
        self.nx = nx
        # number of splits by OY
        self.ny = ny
  
    def triangulate(self, rectangle_polygon):
        rectangle_polygon = [Point(x[0], x[1])
                             for x in rectangle_polygon]
        
        # rearrange points
        rectangle_polygon = rectangle_polygon[:4]
        rectangle_polygon.sort(key=lambda p: (p.x, p.y))
        rectangle_polygon[-1], rectangle_polygon[-2] = rectangle_polygon[-2], rectangle_polygon[-1]
        '''
        indexes:
        1---------2
        |         |
        |         |
        0---------3
        '''
        
        triangles = []       

        width = rectangle_polygon[3].x - rectangle_polygon[0].x
        height = rectangle_polygon[1].y - rectangle_polygon[0].y
        
        # step by x
        dx = width / self.nx
        
        # step by y
        dy = height / self.ny

        
        left = rectangle_polygon[0].x
        for _ in range(self.nx):
            bottom = rectangle_polygon[0].y
            for __ in range(self.ny):
                # add upper triangle
                triangles.append(Triangle(
                    Point(left, bottom),
                    Point(left + dx, bottom + dy),
                    Point(left, bottom + dy)
                ))
                
                # add bottom triangle
                triangles.append(Triangle(
                    Point(left, bottom),
                    Point(left + dx, bottom + dy),
                    Point(left + dx, bottom)
                ))
                
                bottom += dy
            
            left += dx
              
        return triangles