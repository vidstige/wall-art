from typing import Tuple

import cairo
import numpy as np
from scipy.spatial import Delaunay
from PIL import Image

from mesh_art.gradient import sample_gradient
from mesh_art.uigradients import add_stops_to, gradient_names


def sample(pdf: np.ndarray, n: int) -> np.ndarray:
    flat = pdf.flatten()
    indices = np.random.choice(a=flat.size, p=flat, size=n)
    return np.array(list(zip(*np.unravel_index(indices, pdf.shape))))


def points_for(path: str, n: int) -> np.ndarray:
    im = np.array(Image.open(path).convert('L')).T / 255
    clamped = np.clip(im, 0.025, 1 - 0.025)
    pdf = (1 - clamped) / np.sum(1 - clamped)
    return sample(pdf, n) / np.array(pdf.shape)


def pad(points: np.ndarray, padding: float) -> np.ndarray:
    """Pads the 2d-points by a certain amount on each side"""
    return (points * (1 + 2 * padding) - np.array([padding, padding]))


def art_png_to(
        desination,
        resolution: Tuple[int, int], gradient_name: str, rho: float, padding: float,
        offset: float, background: bool):
    np.random.seed(1337)
    width, height = resolution

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)

    n = int(rho * width * height)
    points = np.random.random((n, 2))
    #points = points_for('images/logo.png', n)
    
    # pad
    points = pad(points, padding=padding) * np.array([width, height])

    triangle_indices = Delaunay(points).simplices
    x, y = np.hsplit(points, 2)

    gradient = cairo.LinearGradient(0, 0, width, height)
    add_stops_to(gradient_name, gradient)

    # draw background square
    if background:
        ctx.set_source(gradient)
        ctx.rectangle(0, 0, width, height)
        ctx.fill()

    offsets = np.random.normal(0, offset, (len(triangle_indices), 2))
    for indices, offset in zip(triangle_indices, offsets):
        center = np.mean(np.vstack([x[indices].ravel(), y[indices].ravel()]), axis=-1)
        i0, i1, i2 = indices
        ctx.set_source_rgb(*sample_gradient(gradient, tuple(center + offset)))
        ctx.move_to(x[i0], y[i0])
        ctx.line_to(x[i1], y[i1])
        ctx.line_to(x[i2], y[i2])
        ctx.close_path()
        ctx.fill()

    surface.write_to_png(desination)
