import cmath, math
import matplotlib.pyplot as plt
import numpy as np

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        if type(other) != Point:
            return False
        return self.x == other.x and self.y == other.y
    
    def __repr__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"
    
    def reflect(pt):
        # Reflect another point
        b = complex(self.x, self.y)
        a = complex(pt.x, pt.y)
        
        t = (1 + b*b.conjugate())/2
        c = (b - t*a)/(t - a*b.conjugate())
        return Point(c.real, c.imag)
    
class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        
        det = start.x*end.y - end.x*start.y
        self.is_line = abs(det) < 0.0000000000001
        
        if self.is_line:
            self.p1 = start
            dist = math.sqrt((start.x - end.x)*(start.x - end.x) + (start.y - end.y)*(start.y - end.y))
            self.p2 = Point((end.x - start.x)/dist, (end.y - start.y)/dist)
        else:
            # This is a circle
            s1 = (1.0 + start.x*start.x + start.y*start.y) / 2.0;
            s2 = (1.0 + end.x*end.x + end.y*end.y) / 2.0;
            self.c = Point ((s1*end.y - s2*start.y) / det,
                     (start.x*s2 - end.x*s1) / det);
            self.r = math.sqrt(self.c.x*self.c.x+self.c.y*self.c.y - 1.0)
    def reflect(self, pt):
        if self.is_line:
            factor = 2*((pt.x - self.p1.x)*self.p2.x + (pt.y - self.p1.y)*self.p2.y)
            result_x = 2*self.p1.x + factor*self.p2.x - pt.x
            result_y = 2*self.p1.y + factor*self.p2.y - pt.y
        else:
            factor = self.r*self.r/((pt.x - self.c.x)*(pt.x - self.c.x) + (pt.y - self.c.y)*(pt.y - self.c.y))
            result_x = self.c.x + factor*(pt.x - self.c.x)
            result_y = self.c.y + factor*(pt.y - self.c.y)
        
        return Point(result_x, result_y)

class Polygon:
    def __init__(self, n):
        self.n = n # Number of Vertices
        vertex = []
        for _ in range(n):
            vertex.append(Point(0, 0))
        self.v = vertex
        
    def center(self, k):
        angle_a = math.pi/self.n
        # angle_b= math.pi/k;
        angle_b = math.pi/self.n
        angle_c = math.pi/2.0
        sin_a = math.sin(angle_a)
        sin_b = math.sin(angle_b)
        s = math.sin(angle_c - angle_b - angle_a)/math.sqrt(1.0 - sin_b*sin_b - sin_a*sin_a)
        for i in range(self.n):
            self.v[i] = Point(s*math.cos((3+2*i)*angle_a), s*math.sin((3+2*i)*angle_a))