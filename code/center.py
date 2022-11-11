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

def visualize(points):
    """ Given a list of points and a title, draws the curve traced out by it """
    input = map(lambda pt: [pt.x, pt.y], points)
    x_pts, y_pts = zip(*input) #create lists of x and y values
    
    # Plot of the Polygonal Curve
    fig = plt.figure()
    for i in range(0, len(x_pts)):
        plt.plot(x_pts[i], y_pts[i], 'g-o')
    
    # Integer Grid
    # plt.grid()
    plt.show()

# https://www.mathworks.com/matlabcentral/answers/367126-plot-an-arc-on-a-2d-grid-by-given-radius-and-end-points
def visualize_lines(lines):
    fig = plt.figure()
    for ell in lines:
        pt_1 = ell.start
        pt_2 = ell.end
        
        if ell.is_line:
            plt.plot([pt_1.x, pt_2.x], [pt_1.y, pt_2.y], 'k-')
        else:
            # This is a circle:
            center = ell.c
            radius = ell.r
            a = math.atan2(pt_1.y - center.y, pt_1.x - center.x)
            b = math.atan2(pt_2.y - center.y, pt_2.x - center.x)

            if abs(b - a) < math.pi:
                tee = np.linspace(b, a, num=1000).tolist()
                x = list(map(lambda t: center.x + radius*math.cos(t), tee))
                y = list(map(lambda t: center.y + radius*math.sin(t), tee))
            
                plt.plot(x, y)
                
            else:
                if a > b:
                    tee_1 = np.linspace(-math.pi, b, num=500).tolist()
                    tee_2 = np.linspace(a, math.pi, num=500).tolist()
                else:
                    tee_1 = np.linspace(-math.pi, a, num=500).tolist()
                    tee_2 = np.linspace(b, math.pi, num=500).tolist()
                    
                x_1 = list(map(lambda t: center.x + radius*math.cos(t), tee_1))
                y_1 = list(map(lambda t: center.y + radius*math.sin(t), tee_1))
                
                x_2 = list(map(lambda t: center.x + radius*math.cos(t), tee_2))
                y_2 = list(map(lambda t: center.y + radius*math.sin(t), tee_2))
            
                plt.plot(x_1, y_1)
                plt.plot(x_2, y_2)
            # b = ((b - a) % (2*math.pi)) + a
            # print(a)
            # print(b)
            # if abs(b - a) < math.pi:
            #     tee = np.linspace(b, a, num=1000).tolist()
            # else:
            #     tee = np.linspace(a, b, num=1000).tolist()
                        
    plt.show()
    
def vert_to_edges(points):
    """Given a sequence of vertices, convert them into a list of edges"""
    edges = []
    for idx, point in enumerate(points):
        if idx != len(points) - 1:
            edges.append(Line(point, points[idx + 1]))
    edges.append(Line(points[-1], points[0]))
    return edges

def make(vert_num, layer):
    poly = Polygon(8)
    poly.center(8)
    
    for i in range(vert_num):
        print(poly.v[i])
        
    # ell = Line(Point(0, 0), Point(0.1, 0))
    ell = Line(poly.v[0], poly.v[1])
    
    print(ell.is_line)
        
    visualize(poly.v)
    visualize_lines(vert_to_edges(poly.v))
  
# The main body of the code:
if __name__ == "__main__":
    make(8, 3)