from typing import Tuple
from flask import Flask, Response, request

from mesh_art.art import art_png_to

app = Flask(__name__)


def parse_resolution(s: str) -> Tuple[int, int]:
    w, h = s.split('x', 1)
    return int(w), int(h)


def parse_bool(s: str) -> bool:
    return s.lower() in ('yes', 'true', 'y', 'on', '1')


@app.route("/")
def index():
    return app.send_static_file('index.html')


@app.route("/mesh.png")
def mesh():
    resolution = parse_resolution(request.args.get('resolution', '512x512'))
    gradient_name = request.args.get('gradient', 'Neuromancer')
    rho = float(request.args.get('rho', '0.0005'))
    padding = float(request.args.get('padding', '0.15'))
    offset = float(request.args.get('offset', '10'))
    background = parse_bool(request.args.get('background', 'yes'))
    response = Response(content_type='image/png')
    art_png_to(
        response.stream,
        resolution=resolution,
        gradient_name=gradient_name,
        rho=rho,
        padding=padding,
        offset=offset,
        background=background,
    )
    return response
