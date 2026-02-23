import numpy as np

class boundingBox():
    def __init__(self, center, size):
        self.center = center
        self.size = size
        self.min = center - size/2
        self.max = center + size/2
    
    def contains(self, point):
        position = point.position if isinstance(point, Point) else point

        return (self.min[0] <= position[0] <= self.max[0]) and (self.min[1] <= position[1] <= self.max[1])
    
    def intersects(self, boundingBox):
        return not (boundingBox.max[0] < self.min[0] or boundingBox.min[0] > self.max[0] or boundingBox.max[1] < self.min[1] or boundingBox.min[1] > self.max[1])



class Point():
    def __init__(self, position, data=None):
        self.position = position
        self.data = data

class QuadTree():
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False
        self.northeast = None
        self.northwest = None
        self.southeast = None
        self.southwest = None
    
    def subdivide(self):
        #Calculate the center and size of the current boundary.
        x, y = self.boundary.center
        w, h = self.boundary.size / 2
        
        #Construct four boundaries for the new four quadrants.
        ne_boundary = boundingBox(np.array([x + w/2, y - h/2]), np.array([w, h]))
        nw_boundary = boundingBox(np.array([x - w/2, y - h/2]), np.array([w, h]))
        se_boundary = boundingBox(np.array([x + w/2, y + h/2]), np.array([w, h]))
        sw_boundary = boundingBox(np.array([x - w/2, y + h/2]), np.array([w, h]))

        #Create four new QuadTrees for the four quadrants as our children.
        self.northeast = QuadTree(ne_boundary, self.capacity)
        self.northwest = QuadTree(nw_boundary, self.capacity)
        self.southeast = QuadTree(se_boundary, self.capacity)
        self.southwest = QuadTree(sw_boundary, self.capacity)

        #Set the divided flag to true.
        self.divided = True
    
    def queryFromPoint(self, point, radius, found):
        point = point.position if isinstance(point, Point) else point
        boundary = boundingBox(point, radius)
        found = self.query(boundary, found)
        return found

    def query(self, query_range, found):
        if not self.boundary.intersects(query_range):
            return []
        else:
            for p in self.points:
                if query_range.contains(p):
                    found.append(p)
            if self.divided:
                self.northwest.query(query_range, found)
                self.northeast.query(query_range, found)
                self.southwest.query(query_range, found)
                self.southeast.query(query_range, found)
        return found        

    def insert(self, point):
        if not self.boundary.contains(point):
            return False
        #Check if there's space in this quadrant.
        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        
        #Now check if divided
        if not self.divided:
            self.subdivide()
        
        #try to insert into each quadrant
        if self.northeast.insert(point):
            return True
        elif self.northwest.insert(point):
            return True
        elif self.southeast.insert(point):
            return True
        elif self.southwest.insert(point):
            return True
        return False


def debug():
    # Random points
    points = [Point(np.random.rand(2) * 100) for _ in range(100)]
    boundary = boundingBox(np.array([50, 50]), np.array([100, 100]))
    qt = QuadTree(boundary, 4)
    for p in points:
        qt.insert(p)
    query_point = Point(np.array([50, 50]))
    found_points = qt.queryFromPoint(query_point, 20, [])
    print(f"Found {len(found_points)} points within radius 20 of {query_point.position}")

if __name__ == "__main__":
    debug()
