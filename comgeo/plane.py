class Point2D():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __lt__(self, other):
        if self.x == other.x:
            return self.y < other.y
        
        return self.x < other.x

    def __repr__(self):
        return "Point2D({}, {})".format(self.x, self.y)


def orientation(point_p, point_q, point_r):
    """Returns orientation of point_r from perspective of segment (point_p, point_q)"""
    value = point_q.x * point_r.y + point_p.x * point_q.y + point_p.y * point_r.x - point_q.x * point_p.y - point_r.x * point_q.y - point_r.y * point_p.x

    if value > 0:
        return 1
    elif value < 0:
        return -1
    else:
        return 0