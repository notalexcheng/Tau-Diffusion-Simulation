// Create scene, camera, and renderer
const scene = new THREE.Scene();
const camera = new THREE.OrthographicCamera(-15, 15, 15, -15, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('simulationCanvas') });
renderer.setSize(800, 800); // Set fixed size for the simulation
renderer.setClearColor(0xffffff, 1);

// Add OrbitControls
const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableZoom = true;

// Set camera position
camera.position.set(0, 0, 50);
camera.lookAt(new THREE.Vector3(0, 0, 0));

// Create a grid of spheres
const sphereSize = 0.2; // Adjust size for visibility
const sphereGeometry = new THREE.SphereGeometry(sphereSize, 16, 16);
const spheres = [];

// Create axes helper
const axesHelper = new THREE.AxesHelper(20); // Adjust size for clarity
scene.add(axesHelper);

// Create grid lines
let lines = [];

function createGridLines() {
    // Remove existing lines from the scene
    lines.forEach(line => scene.remove(line));
    lines.length = 0;

    const lineMaterial = new THREE.LineBasicMaterial({ color: 0x000000, opacity: 0.3, transparent: true });

    function createLine(start, end) {
        const geometry = new THREE.BufferGeometry().setFromPoints([start, end]);
        const line = new THREE.Line(geometry, lineMaterial);
        lines.push(line);
        return line;
    }

    // Create lines along the x, y, and z axes
    for (let x = 0; x <= xSize; x++) {
        for (let y = 0; y <= ySize; y++) {
            for (let z = 0; z <= zSize; z++) {
                // Line along the x-axis
                if (x < xSize) {
                    scene.add(createLine(
                        new THREE.Vector3(x - xSize / 2, y - ySize / 2, z - zSize / 2),
                        new THREE.Vector3(x - xSize / 2 + 1, y - ySize / 2, z - zSize / 2)
                    ));
                }
                // Line along the y-axis
                if (y < ySize) {
                    scene.add(createLine(
                        new THREE.Vector3(x - xSize / 2, y - ySize / 2, z - zSize / 2),
                        new THREE.Vector3(x - xSize / 2, y - ySize / 2 + 1, z - zSize / 2)
                    ));
                }
                // Line along the z-axis
                if (z < zSize) {
                    scene.add(createLine(
                        new THREE.Vector3(x - xSize / 2, y - ySize / 2, z - zSize / 2),
                        new THREE.Vector3(x - xSize / 2, y - ySize / 2, z - zSize / 2 + 1)
                    ));
                }
            }
        }
    }
}

function createSpheres() {
    spheres.forEach(sphere => scene.remove(sphere));
    spheres.length = 0;

    for (let x = 0; x < xSize; x++) {
        for (let y = 0; y < ySize; y++) {
            for (let z = 0; z < zSize; z++) {
                const value = tauArray[x][y][z][tauType];
                const opacity = value/10;

                // Determine the base color based on tauType
                let baseColor;
                switch (tauType) {
                    case 0:
                        baseColor = new THREE.Color("blue");
                        break;
                    case 1:
                        baseColor = new THREE.Color("green");
                        break;
                    case 2:
                        baseColor = new THREE.Color("red");
                        break;
                    case 3:
                        baseColor = new THREE.Color("yellow");
                        break;
                    case 4:
                        baseColor = new THREE.Color("black");
                        break;
                    default:
                        baseColor = new THREE.Color("black"); // Default color if tauType is out of expected range
                }

                const material = new THREE.MeshBasicMaterial({ color: baseColor, transparent: true, opacity: opacity });
                const sphere = new THREE.Mesh(sphereGeometry, material);
                sphere.position.set(x - xSize / 2, y - ySize / 2, z - zSize / 2);
                scene.add(sphere);
                spheres.push(sphere);
            }
        }
    }
}

// Render loop
function animate() {
    requestAnimationFrame(animate);
    controls.update(); // Update controls
    renderer.render(scene, camera);
}
animate();
