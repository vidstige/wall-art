function main() {
    // Creating a GUI with options.
    var gui = new dat.GUI({
        name: 'mesh',
    });
    let settings = {
        'rho': 0.0005,
        'offset': 10,
        'background': true,
    }
    function updateImage() {
        var el = document.getElementById('display');
        el.src = 'mesh.png?' + new URLSearchParams(settings);
    }    
    gui.add(settings, 'rho').onChange(updateImage);
    gui.add(settings, 'offset').onChange(updateImage);
    gui.add(settings, 'background').onChange(updateImage);
}

addEventListener("DOMContentLoaded", main);
