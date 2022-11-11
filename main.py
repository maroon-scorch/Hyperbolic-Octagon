import math, sys
import matplotlib.pyplot as plt
import numpy as np
from polygon import *

def visualize_vertices(points):
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

# This helped my plot a lot:
# https://www.mathworks.com/matlabcentral/answers/367126-plot-an-arc-on-a-2d-grid-by-given-radius-and-end-points
def visualize_lines(lines):
    for ell in lines:
        pt_1 = ell.start
        pt_2 = ell.end
        
        if ell.is_line:
            plt.plot([pt_1.x, pt_2.x], [pt_1.y, pt_2.y], 'r-')
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
            
                plt.plot(x, y, 'r-')
                
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
            
                plt.plot(x_1, y_1, 'r-')
                plt.plot(x_2, y_2, 'r-')
            # b = ((b - a) % (2*math.pi)) + a
            # print(a)
            # print(b)
            # if abs(b - a) < math.pi:
            #     tee = np.linspace(b, a, num=1000).tolist()
            # else:
            #     tee = np.linspace(a, b, num=1000).tolist()
                        
    # plt.show()
    
def vert_to_edges(points):
    """Given a sequence of vertices, convert them into a list of edges"""
    edges = []
    for idx, point in enumerate(points):
        if idx != len(points) - 1:
            edges.append(Line(point, points[idx + 1]))
    edges.append(Line(points[-1], points[0]))
    return edges

def make_new_polygon(poly, n, s):
    qoly = Polygon(n)
    new_line = Line(poly.v[s], poly.v[int((s + 1) % n)])
    for i in range(n):
        j = (n + s - i + 1) % n;
        qoly.v[j] = new_line.reflect(poly.v[i])
        
    return qoly

def make(vert_num, layer):
    
    ang= np.linspace(0, 2*math.pi, num=1000).tolist()
    xp = list(map(lambda t: math.cos(t), ang))
    yp = list(map(lambda t: math.sin(t), ang))
    plt.plot(xp, yp, 'b-');
    
    poly = Polygon(8)
    poly.center(8)
    
    for i in range(vert_num):
        print(poly.v[i])
    
    visualize_lines(vert_to_edges(poly.v))
    
    poly_list = [poly]
    count = layer
    while count > 1:
        new_list = []
        for p in poly_list:
            for i in range(vert_num):
                temp = make_new_polygon(p, vert_num, i)
                visualize_lines(vert_to_edges(temp.v))
                new_list.append(temp)
        poly_list = new_list
        count = count - 1
    
    plt.show()
  
# The main body of the code:
if __name__ == "__main__":
    iter = int(sys.argv[1])
    make(8, iter)