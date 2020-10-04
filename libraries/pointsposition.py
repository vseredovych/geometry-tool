import numpy as np
from libraries.triangle import triangle_area, signed_triangle_area


def is_point_inside(pt, v1, v2, v3):
    """
    Check whether the point is inside of triangle
    :param pt, v1, v2, v3: Point
    :return: bool
    """
    total_area = triangle_area(v1, v2, v3)
    area1 = triangle_area(pt, v1, v2)
    area2 = triangle_area(pt, v1, v3)
    area3 = triangle_area(pt, v2, v3)

    return area1 + area2 + area3 <= total_area


def contains_no_points(v1, v2, v3, polygon):
    """
    Check whether ear contains no other points
    :param v1, v2, v3: Point
    :param polygon: bool
    :return:
    """
    for point in polygon:
        if point in (v1, v2, v3):
            continue
        elif is_point_inside(point, v1, v2, v3):
            return False

    return True


def is_convex(v1, v2, v3):
    """
    Check whether ear is convex (Angle < 180 degrees)
    :return: bool
    """
    return not is_clockwise((v1, v2, v3)) and signed_triangle_area(v1, v2, v3) > 0


def is_clockwise(polygon):
    """
    Determines whether polygon is in clockwise order by summing up determinants of all neighboring edges.
    If sum of such determinants > 0 than polygon vertices in clockwise order and if < 0 - counterclockwise.
    :param polygon: array, size(n, 2)
    :return:
    """
    det_sum = 0

    for i, _ in enumerate(polygon):
        point1 = polygon[i]
        point2 = polygon[(i + 1) % len(polygon)]
        det_sum += (point2.x - point1.x) * (point2.y + point1.y)

    return det_sum > 0


def compute_angle(p1, p2, p3):
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
    if is_convex(p1, p2, p3):
        return angle
    else:
        return 360 - angle
