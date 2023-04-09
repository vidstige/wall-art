import json
from pathlib import Path
from typing import Dict, List

import cairo

from mesh_art.gradient import parse_color


def load_gradients() -> Dict[str, List[str]]:
    with Path('gradients.json').open() as f:
        gradients = json.load(f)
    return {gradient['name']: gradient['colors'] for gradient in gradients}


def gradient_names() -> List[str]:
    return list(load_gradients().keys())


def add_stops_to(name: str, gradient: cairo.LinearGradient):
    gradients = load_gradients()
    colors = gradients[name]
    for i, color in enumerate(colors):
        gradient.add_color_stop_rgb(i / (len(colors) - 1), *parse_color(color))
