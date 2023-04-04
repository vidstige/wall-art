import cairo
import numpy as np
from scipy.spatial import Delaunay

from mesh_art.gradient import parse_color, sample
from mesh_art.mesh2d import create_mesh

def main():
    width, height = 512, 512
    padding = 0.25

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)

    #(x, y), triangle_indices = create_mesh((5, 5), (width, height))
    #x = x + np.random.normal(size=x.shape) * 10
    #y = y + np.random.normal(size=y.shape) * 10

    rho = 0.001
    n = int(rho * width * height)
    points = np.random.random((n, 2)) * (1 + 2 * padding) * np.array([width, height]) - np.array([padding, padding])
    triangle_indices = Delaunay(points).simplices
    x, y = np.hsplit(points, 2)

    # https://uigradients.com/#Neuromancer
    gradient = cairo.LinearGradient(0, 0, width, height)
    gradient.add_color_stop_rgb(0, *parse_color('#f953c6'))
    gradient.add_color_stop_rgb(1, *parse_color('#b91d73'))
    
    # draw background square
    ctx.set_source(gradient)
    ctx.rectangle(0, 0, width, height)
    ctx.fill()

    for indices in triangle_indices:
        center = np.mean(np.vstack([x[indices], y[indices]]), axis=-1)
        i0, i1, i2 = indices
        ctx.set_source_rgb(*sample(gradient, tuple(center)))
        ctx.move_to(x[i0], y[i0])
        ctx.line_to(x[i1], y[i1])
        ctx.line_to(x[i2], y[i2])
        ctx.close_path()
        ctx.fill()

    surface.write_to_png('output.png')

main()