import random

from mesh_art.art import art_png_to
from mesh_art.uigradients import gradient_names

gradient_name = random.choice(gradient_names())
#gradient_name = 'Neuromancer'
#gradient_name = 'Ultra Voilet'
#gradient_name = 'Timber'

art_png_to(
    'output.png',
    resolution=(800, 800),
    gradient_name=gradient_name,
    rho=0.0005,
    padding=0.15,
    offset=10,
    background=True,
)