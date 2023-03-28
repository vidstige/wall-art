from typing import Tuple

import cairo
import numpy as np

def parse_color(color: str) -> Tuple[float, float, float]:
    return tuple(c / 255.0 for c in bytearray.fromhex(color.lstrip('#')))


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
        index(ix, iy + 1, stride),
        index(ix, iy, stride),
        index(ix + 1, iy + 1, stride),
    ])
    return (x.ravel(), y.ravel()), np.hstack([top, bottom]).T
    

Vec = Tuple[float]
Color = Tuple[float, float, float]

def dot(a: Vec, b: Vec) -> float:
    return sum(ai*bi for ai, bi in zip(a, b))

def minus(a: Vec, b: Vec) -> float:
    return tuple(ai - bi for ai, bi in zip(a, b))

def project_to_line(a, b, p) -> float:
    ap = minus(p, a)
    ab = minus(b, a)
    return dot(ap, ab) / dot(ab, ab)


def lerp(a: float, b: float, t: float) -> float:
    return a * (1 - t) + b * t


def lerp_color(a: Color, b: Color, t: float) -> Color:
    return tuple(lerp(c0, c1, t) for c0, c1 in zip(a, b))


def sample(gradient: cairo.LinearGradient, p: Tuple[float, float]) -> Color:
    x0, y0, x1, y1 = gradient.get_linear_points()
    t = project_to_line((x0, y0), (x1, y1), p)
    stops = gradient.get_color_stops_rgba()
    for (t0, r0, g0, b0, a0), (t1, r1, g1, b1, a1) in zip(stops, stops[1:]):
        del a0, a1
        if t0 <= t:
            return lerp_color((r0, g0, b0), (r1, g1, b1), (t - t0) / (t1 - t0))


def main():
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 200, 200)
    ctx = cairo.Context(surface)
    (x, y), triangle_indices = create_mesh((5, 5), (200, 200))
    
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