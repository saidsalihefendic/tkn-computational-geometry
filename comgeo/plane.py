class Point2D():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __lt__(self, other):
        if self.x == other.x:
            return self.y < other.y
        
        return self.x < other.x

    def __add__(self, point):
        return Point2D(self.x + point.x, self.y + point.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __neq__(self, other):
        return self.x != other.x or self.y != other.y

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __repr__(self):
        return "Point2D({}, {})".format(self.x, self.y)

    def __str__(self):
        return "Point2D({}, {})".format(self.x, self.y)

class Vector2D():
    """Forms a representative of the vector from the given Point2D objects"""
    def __init__(self, begin, end):
        self.x = end.x - begin.x
        self.y = end.y - begin.y

    def norm(self):
        return (self.x**2 + self.y**2) ** (1 / 2)

    @staticmethod
    def dot(vector_1, vector_2):
        return vector_1.x * vector_2.x + vector_1.y * vector_2.y

    def __add__(self, vector):
        return Vector2D(Point2D(0, 0), Point2D(self.x + vector.x, self.y + vector.y))

    def __repr__(self):
        return "Vector2D({}, {})".format(self.x, self.y)

    def __str__(self):
        return "Vector2D({}, {})".format(self.x, self.y)

class DirectedEdge():
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end

    def orientation(self, point):
        """Calculates the orientation of a point from perspective of directed edge. Returns -1, if left of directed edge, 0 if collinear and 1 if right of directed edge"""
        p_x = self.begin.x
        p_y = self.begin.y

        q_x = self.end.x
        q_y = self.end.y

        r_x = point.x
        r_y = point.y

        D = q_x * r_y + p_x * q_y + p_y * r_x - q_x * p_y - r_x * q_y - r_y * p_x

        if D > 0:
            return 1
        elif D == 0:
            return 0
        else:
            return -1
        
    def __eq__(self, end):
        return self.begin == self.end
    
    def __neq__(self, end):
        return self.begin != self.end

    def __repr__(self):
        return "DirectedEdge({}, {})".format(str(self.begin), (self.end))