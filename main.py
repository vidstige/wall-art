from typing import Tuple

import cairo
import numpy as np

def index(ix, iy, stride: int):
    return ix + iy * stride

def create_mesh(resolution: Tuple[int, int], size: Tuple[float, float]) -> np.ndarray:
    w, h = resolution
    # vertices
    x, y = np.meshgrid(
        np.linspace(0, size[0], w),
        np.linspace(0, size[1], h),
    )
    # triangles
    ix, iy = np.meshgrid(np.arange(w - 1), np.arange(h - 1))
    ix, iy = ix.ravel(), iy.ravel()
    stride = w
    top = np.vstack([
        index(ix, iy, stride),
        index(ix + 1, iy, stride),
        index(ix + 1, iy + 1, stride),
    ])
    bottom = np.vstack([
        index(ix, iy, stride),
        index(ix + 1, iy + 1, stride),
        index(ix, iy + 1, stride),
    ])
    triangle_indices = np.hstack([top, bottom])
    return (x.ravel(), y.ravel()), triangle_indices.T
    

def main():
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 200, 200)
    ctx = cairo.Context(surface)
    (x, y), triangle_indices = create_mesh((5, 5), (200, 200))
    
    ctx.set_source_rgb(1, 0, 1)

    for i0, i1, i2 in triangle_indices:
        ctx.move_to(x[i0], y[i0])
        ctx.line_to(x[i1], y[i1])
        ctx.line_to(x[i2], y[i2])
        ctx.close_path()
        ctx.fill()
    #ctx.move_to(100, 50)
    #ctx.line_to(50, 150)
    #ctx.line_to(150, 150)
    #ctx.close_path()
    #ctx.fill()

    surface.write_to_png('triangle.png')

main()