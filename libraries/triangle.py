class Point:
    def __init__(self, x=0, y=0, angle=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def get_coords(self):
        return self.x, self.y


class Triangle:
    def __init__(self, p1=Point(), p2=Point(), p3=Point()):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def __eq__(self, other):
        return self.p1 == other.p1 and self.p2 == other.p2 and self.p3 == other.p3

    def __str__(self):
        return f"[ {self.p1}, {self.p2}, {self.p3} ]"

    def get_points(self):
        return [
            [self.p1.x, self.p1.y],
            [self.p2.x, self.p2.y],
            [self.p3.x, self.p3.y],
        ]

    def area(self):
        """
        Find the area of a triangle. This function uses the 1/2 determinant
        method. Given three points (x1, y1), (x2, y2), (x3, y3):
                    | x1 y1 1 |
        Area = .5 * | x2 y2 1 |
                    | x3 y3 1 |
        :param p1, p2, p3: Point
        :return: float
        """
        return triangle_area(self.p1, self.p2, self.p3)


def signed_triangle_area(p1, p2, p3):
    """
    Gives a triangle area if vertices are listed in counterclockwise
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

def triangle_area(p1, p2, p3):
    """
    Gives a positive triangle area if vertices are listed in counterclockwise
    and negative area if vertices are listed clockwise.
                | x1 y1 1 |
    Area = .5 * | x2 y2 1 |
                | x3 y3 1 |
    :param p1, p2, p3: Point
    :return: float
    """
    return abs(signed_triangle_area(p1, p2, p3))

def compute_triangles_area(triangles):
    area = 0
    for tr in triangles:
        area += tr.area()
    return area
