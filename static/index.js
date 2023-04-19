function main() {
    // Creating a GUI with options.
    var gui = new dat.GUI({
        name: 'mesh',
    });
    let settings = {
        'rho': 0.0005,
        'offset': 10,
        'background': true,
        'gradient': 'Neuromancer',
    }
    
    function updateImage() {
        console.log(settings);
        var el = document.getElementById('display');
        el.src = 'mesh.png?' + new URLSearchParams(settings);
    }    
    gui.add(settings, 'rho', 0.0001, 0.001).onChange(updateImage);
    gui.add(settings, 'offset', 0, 128).onChange(updateImage);
    gui.add(settings, 'background').onChange(updateImage);
    gradients = gui.add(settings, 'gradient');

    // load gradient names
    fetch('gradient_names/')
        .then(response => response.json())
        .then(body => gradients.options(body).onChange(updateImage));
}

addEventListener("DOMContentLoaded", main);
