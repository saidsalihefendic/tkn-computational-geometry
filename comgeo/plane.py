from functools import partial
from math import acos

class Point2D():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __lt__(self, other):
        if self.x == other.x:
            return self.y < other.y
        
        return self.x < other.x

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return not self < other

    def __gt__(self, other):
        return not self <= other

    def __add__(self, point):
        return Point2D(self.x + point.x, self.y + point.y)

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

    def contains_point(self, point):
        """Tests whether a point lies on the directed edge"""
        if self.orientation(point) == 0:
            return point >= min(self.begin, self.end) and point <= max(self.begin, self.end)

        return False
    
    def is_collinear(self, directed_edge):
        """Tests whether the directed edge is collinear with another directed edge"""

        return self.orientation(directed_edge.begin) == 0 and self.orientation(directed_edge.end) == 0

    def is_intersecting(self, directed_edge):
        """Tests whether the directed edge intersects with another edge"""
        begin_orientation = self.orientation(directed_edge.begin)
        end_orientation = self.orientation(directed_edge.end)
        
        if(begin_orientation == 0 or end_orientation == 0):
            return self.contains_point(directed_edge.begin) or self.contains_point(directed_edge.end) or directed_edge.contains_point(self.begin) or directed_edge.contains_point(self.end)

        directed_begin_orientation = directed_edge.orientation(self.begin)
        directed_end_orientation = directed_edge.orientation(self.end)

        return begin_orientation != end_orientation and directed_begin_orientation != directed_end_orientation
    
    def __eq__(self, directed_edge):
        return self.begin == directed_edge.begin and self.end == directed_edge.end
    
    def __neq__(self, directed_edge):
        return not self == directed_edge

    def __repr__(self):
        return "DirectedEdge({}, {})".format(str(self.begin), (self.end))


def get_angle_and_distance(point_1, point_2, point_3):
    """Returns the angle of < point_1, point_2, point_3"""
    if point_1 == point_2 or point_1 == point_3 or point_2 == point_3:
        return 0, 0
    
    v1 = Vector2D(point_2, point_1)
    v2 = Vector2D(point_2, point_3)
    
    cosalpha = Vector2D.dot(v1, v2) / (v1.norm() * v2.norm())

    return (acos(cosalpha), v1.norm())


class SimplePolygon():
    def __init__(self, vertices):
        self.vertices = SimplePolygon.sort(vertices)

    def get_reference_point(self):
        leftmost_point = self.vertices[0]
        return Point2D(leftmost_point.x - 1, leftmost_point.y)

    def is_in_polygon(self, point):
        """Returns whether a point is inside the simple polygon or not"""
        reference_point = self.get_reference_point()
        
        reference_segment = DirectedEdge(point, reference_point)

        num_crossings = 0
        
        left_idx = 0
        while left_idx != len(self):
            right_idx = (left_idx + 1) % len(self)
            
            are_crossing = False
            
            if reference_segment.contains_point(self[left_idx]):
                while reference_segment.contains_point(self[right_idx]):
                    right_idx = (right_idx + 1) % len(self)
                    
                    if right_idx == left_idx:
                        break
                
                if left_idx == right_idx:
                    left_idx = len(self)
                    continue
                
                left_endpoint = self[(left_idx - 1) % len(self)]
                right_endpoint = self[(right_idx + 1) % len(self)]
                
                are_crossing = reference_segment.orientation(left_endpoint) != reference_segment.orientation(right_endpoint)
                left_idx = (right_idx + 1) % len(self) if left_idx < (right_idx + 1) % len(self) else len(self) 
            elif reference_segment.contains_point(self[right_idx]):
                left_idx += 1
                continue
            else:
                edge = DirectedEdge(self[left_idx], self[right_idx])
                are_crossing = reference_segment.is_intersecting(edge)
                left_idx += 1
            
            num_crossings = num_crossings + 1 if are_crossing else num_crossings
            
        return num_crossings % 2 == 1

    def __len__(self):
        return len(self.vertices)
    
    def __getitem__(self, i):
        return self.vertices[i] 

    @staticmethod
    def sort(points):
        """Given a list of Point2D, returns the clockwise sorted list that forms simple polygon"""
        if len(points) == 0:
            return []
        
        starting_vertex = min(points)
        reference_point = starting_vertex + Point2D(0, 1)
        
        return sorted(points, key=partial(
            get_angle_and_distance, point_2=starting_vertex, point_3=reference_point
        ))