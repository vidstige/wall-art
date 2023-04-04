import cairo
import numpy as np
from scipy.spatial import Delaunay

from mesh_art.gradient import parse_color, sample
from mesh_art.mesh2d import create_mesh

def main():
    width, height = 200, 200
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)

    #(x, y), triangle_indices = create_mesh((5, 5), (width, height))
    #x = x + np.random.normal(size=x.shape) * 10
    #y = y + np.random.normal(size=y.shape) * 10

    rho = 0.001
    n = int(rho * width * height)
    points = np.random.random((n, 2)) * np.array([200, 200])
    triangle_indices = Delaunay(points).simplices
    x, y = np.hsplit(points, 2)

    # https://uigradients.com/#Neuromancer
    gradient = cairo.LinearGradient(0, 0, 200, 200)
    gradient.add_color_stop_rgb(0, *parse_color('#f953c6'))
    gradient.add_color_stop_rgb(1, *parse_color('#b91d73'))
    #ctx.set_source(gradient)

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