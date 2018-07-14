def invert_in_circle(center, radius, point):
    x, y = point
    center_x, center_y = center
    square_norm = (x - center_x) ** 2 + (y - center_y) ** 2
    x_inverted = center_x + radius ** 2 * (x - center_x) / square_norm
    y_inverted = center_y + radius ** 2 * (y - center_y) / square_norm
    return (x_inverted, y_inverted)


# a line between two points is computed as the circle arc perpendicular to the
# boundary circle that passes between those points
def line_passing_through(point1, point2):
    pass


# Reflection across a line is computed by inversion in a circle
def reflect_across(line, point):
    pass


# Rotation around the origin
def rotate_around_origin(angle, point):
    pass
