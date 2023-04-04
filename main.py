import cairo
import numpy as np

from mesh_art.gradient import parse_color, sample
from mesh_art.mesh2d import create_mesh

def main():
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 200, 200)
    ctx = cairo.Context(surface)
    (x, y), triangle_indices = create_mesh((5, 5), (200, 200))
    
    x = x + np.random.normal(size=x.shape) * 10
    y = y + np.random.normal(size=y.shape) * 10
    gradient = cairo.LinearGradient(0, 0, 200, 200)

    # https://uigradients.com/#Neuromancer
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