import math, sys
import matplotlib.pyplot as plt
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
    
def linspace(lower, upper, item):
    return [lower + x*(upper-lower)/(item-1) for x in range(item)]

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
                tee = linspace(b, a, 1000)
                x = list(map(lambda t: center.x + radius*math.cos(t), tee))
                y = list(map(lambda t: center.y + radius*math.sin(t), tee))
            
                plt.plot(x, y, 'r-')
                
            else:
                if a > b:
                    tee_1 = linspace(-math.pi, b, 500)
                    tee_2 = linspace(a, math.pi, 500)
                else:
                    tee_1 = linspace(-math.pi, a, 500)
                    tee_2 = linspace(b, math.pi, 500)
                    
                x_1 = list(map(lambda t: center.x + radius*math.cos(t), tee_1))
                y_1 = list(map(lambda t: center.y + radius*math.sin(t), tee_1))
                
                x_2 = list(map(lambda t: center.x + radius*math.cos(t), tee_2))
                y_2 = list(map(lambda t: center.y + radius*math.sin(t), tee_2))
            
                plt.plot(x_1, y_1, 'r-')
                plt.plot(x_2, y_2, 'r-')
                        
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
    fig = plt.figure()
    ang= linspace(0, 2*math.pi, 1000)
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
    
    return fig