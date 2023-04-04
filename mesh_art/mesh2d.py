from typing import Tuple

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
        index(ix, iy + 1, stride),
        index(ix, iy, stride),
        index(ix + 1, iy + 1, stride),
    ])
    return (x.ravel(), y.ravel()), np.hstack([top, bottom]).T
    