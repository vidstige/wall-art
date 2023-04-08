from typing import Tuple

import cairo


def parse_color(color: str) -> Tuple[float, float, float]:
    return tuple(c / 255.0 for c in bytearray.fromhex(color.lstrip('#')))


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


def sample_gradient(gradient: cairo.LinearGradient, p: Tuple[float, float]) -> Color:
    x0, y0, x1, y1 = gradient.get_linear_points()
    t = project_to_line((x0, y0), (x1, y1), p)
    stops = gradient.get_color_stops_rgba()
    for (t0, r0, g0, b0, a0), (t1, r1, g1, b1, a1) in zip(stops, stops[1:]):
        del a0, a1
        if t0 <= t:
            return lerp_color((r0, g0, b0), (r1, g1, b1), (t - t0) / (t1 - t0))
    _, r, g, b, _ = stops[0]
    return r, g, b
