import streamlit as st
import streamlit.components.v1 as components

# Set page configuration for better appearance
st.set_page_config(
    page_title="Unit Converter",
    page_icon="⚖️",
    layout="centered"
)

# Custom CSS and Tailwind CSS for styling and animations
st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <style>
    body {
        background-color: #1a1a1a;
        color: #ffffff;
        overflow: hidden;
    }
    .main-container {
        background: rgba(0, 0, 0, 0.5);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 0 25px rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        animation: fadeIn 1s ease-out;
    }
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .stButton>button {
        background: linear-gradient(45deg, #ffffff, #cccccc);
        color: #000000;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
        animation: pulse 2s infinite alternate;
    }
    @keyframes pulse {
        from { box-shadow: 0 0 10px rgba(255, 255, 255, 0.3); }
        to { box-shadow: 0 0 20px rgba(255, 255, 255, 0.6); }
    }
    .stButton>button:hover {
        background: linear-gradient(45deg, #cccccc, #ffffff);
        transform: scale(1.05);
    }
    .stNumberInput, .stSelectbox {
        background: rgba(0, 0, 0, 0.7);
        border: 2px solid #ffffff;
        border-radius: 8px;
        color: #ffffff;
        animation: slideIn 0.5s ease-out;
    }
    @keyframes slideIn {
        0% { opacity: 0; transform: translateX(-20px); }
        100% { opacity: 1; transform: translateX(0); }
    }
    .stNumberInput>label, .stSelectbox>label {
        color: #cccccc;
        font-weight: 500;
        text-shadow: 0 0 5px rgba(255, 255, 255, 0.3);
    }
    .result-box {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
        text-align: center;
        font-size: 1.2rem;
        color: #ffffff;
        box-shadow: 0 0 15px rgba(255, 255, 255, 0.2);
        animation: bounceIn 1s ease-out;
    }
    @keyframes bounceIn {
        0% { opacity: 0; transform: scale(0.5); }
        50% { transform: scale(1.05); }
        100% { opacity: 1; transform: scale(1); }
    }
    #bgCanvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
    }
    </style>
    """, unsafe_allow_html=True)

# Three.js animation script for electric current effect
three_js_script = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/simplex-noise@3.0.1/dist/simplex-noise.min.js"></script>
<script>
const canvas = document.getElementById('bgCanvas');
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true });
renderer.setSize(window.innerWidth, window.innerHeight);

scene.background = new THREE.Color(0x1a1a1a);

const simplex = new SimplexNoise();
const arcs = [];
const sparkSystems = [];
const arcFrequency = 500;
const sparkFrequency = 200;
let lastArcTime = 0;
let lastSparkTime = 0;

const vertexShader = `
    varying vec2 vUv;
    void main() {
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
`;

const fragmentShader = `
    uniform float time;
    uniform vec3 color;
    varying vec2 vUv;
    void main() {
        float intensity = sin(vUv.x * 10.0 + time * 5.0) * 0.5 + 0.5;
        intensity *= sin(vUv.y * 10.0 + time * 3.0) * 0.5 + 0.5;
        gl_FragColor = vec4(color * intensity, intensity);
    }
`;

function createElectricArc() {
    arcs.forEach(arc => scene.remove(arc));
    arcs.length = 0;

    for (let arcIndex = 0; arcIndex < 3; arcIndex++) {
        const segments = 50;
        const points = [];
        const startX = -800;
        const endX = 800;
        const y = (Math.random() - 0.5) * 400;
        const z = (Math.random() - 0.5) * 200;

        points.push(new THREE.Vector3(startX, y, z));
        for (let i = 1; i < segments; i++) {
            const t = i / segments;
            const noise = simplex.noise2D(t * 5, arcIndex + Date.now() * 0.001);
            const x = startX + t * (endX - startX) + noise * 50;
            const yVar = y + noise * 25;
            const zVar = z + noise * 25;
            points.push(new THREE.Vector3(x, yVar, zVar));
        }
        points.push(new THREE.Vector3(endX, y, z));

        const curve = new THREE.CatmullRomCurve3(points);
        const tubeGeometry = new THREE.TubeGeometry(curve, segments, 2, 8, false);

        const material = new THREE.ShaderMaterial({
            vertexShader: vertexShader,
            fragmentShader: fragmentShader,
            uniforms: { time: { value: 0 }, color: { value: new THREE.Color(0xe6f0ff) } },
            transparent: true,
            blending: THREE.AdditiveBlending,
        });

        const arc = new THREE.Mesh(tubeGeometry, material);
        arc.userData.points = points;
        scene.add(arc);
        arcs.push(arc);
    }
}

function createSparks() {
    sparkSystems.forEach(sparks => scene.remove(sparks));
    sparkSystems.length = 0;

    arcs.forEach(arc => {
        const points = arc.userData.points;
        const sparkCount = 10;
        const sparks = new THREE.BufferGeometry();
        const sparkPositions = new Float32Array(sparkCount * 3);
        const sparkColors = new Float32Array(sparkCount * 3);

        for (let i = 0; i < sparkCount * 3; i += 3) {
            const index = Math.floor(Math.random() * points.length);
            const point = points[index];
            const x = point.x + (Math.random() - 0.5) * 15;
            const y = point.y + (Math.random() - 0.5) * 15;
            const z = point.z + (Math.random() - 0.5) * 15;

            sparkPositions[i] = x;
            sparkPositions[i + 1] = y;
            sparkPositions[i + 2] = z;

            const colorT = Math.random();
            sparkColors[i] = 0.8 + 0.2 * colorT;
            sparkColors[i + 1] = 0.8 + 0.2 * colorT;
            sparkColors[i + 2] = 1;
        }

        sparks.setAttribute('position', new THREE.BufferAttribute(sparkPositions, 3));
        sparks.setAttribute('color', new THREE.BufferAttribute(sparkColors, 3));

        const sparkMaterial = new THREE.PointsMaterial({
            size: 12,
            vertexColors: true,
            transparent: true,
            opacity: 1,
            blending: THREE.AdditiveBlending,
        });

        const sparkSystem = new THREE.Points(sparks, sparkMaterial);
        scene.add(sparkSystem);
        sparkSystems.push(sparkSystem);
    });

    scene.background = new THREE.Color(0x444444);
    setTimeout(() => {
        scene.background = new THREE.Color(0x1a1a1a);
    }, 100);

    setTimeout(() => {
        sparkSystems.forEach(sparks => {
            sparks.material.opacity = 0;
            scene.remove(sparks);
        });
    }, 150);
}

camera.position.z = 500;

function animate() {
    requestAnimationFrame(animate);

    const currentTime = Date.now();
    if (currentTime - lastArcTime > arcFrequency) {
        createElectricArc();
        lastArcTime = currentTime;
    }

    if (currentTime - lastSparkTime > sparkFrequency) {
        createSparks();
        lastSparkTime = currentTime;
    }

    arcs.forEach(arc => {
        arc.material.uniforms.time.value = currentTime * 0.001;
        arc.material.opacity = 0.8 + Math.sin(currentTime * 0.01) * 0.2;
    });

    renderer.render(scene, camera);
}
animate();

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});
</script>
<canvas id="bgCanvas"></canvas>
"""

# Embed the Three.js animation
components.html(three_js_script, height=800)

# Title and description
st.title("⚖️ Unit Converter")
st.markdown("Convert units effortlessly between different categories like Length and Temperature!")

# Conversion functions
def convert_length(value, from_unit, to_unit):
    length_units = {
        "meters": 1.0,
        "kilometers": 1000.0,
        "centimeters": 0.01,
        "millimeters": 0.001,
        "miles": 1609.34,
        "yards": 0.9144,
        "feet": 0.3048,
        "inches": 0.0254
    }
    
    value_in_meters = value * length_units[from_unit]
    result = value_in_meters / length_units[to_unit]
    return result

def convert_temperature(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    
    if from_unit == "Celsius":
        celsius = value
    elif from_unit == "Fahrenheit":
        celsius = (value - 32) * 5 / 9
    elif from_unit == "Kelvin":
        celsius = value - 273.15
    
    if to_unit == "Celsius":
        return celsius
    elif to_unit == "Fahrenheit":
        return (celsius * 9 / 5) + 32
    elif to_unit == "Kelvin":
        return celsius + 273.15

# Main container
with st.container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Category selection
    category = st.selectbox("Select Category", ["Length", "Temperature"], help="Choose the type of unit conversion.")

    # Unit options based on category
    if category == "Length":
        units = ["meters", "kilometers", "centimeters", "millimeters", "miles", "yards", "feet", "inches"]
    else:  # Temperature
        units = ["Celsius", "Fahrenheit", "Kelvin"]

    # Input value and unit selection
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        value = st.number_input("Enter Value", value=0.0, step=0.1, format="%.2f", help="Input the value to convert.")
    with col2:
        from_unit = st.selectbox("From Unit", units, help="Select the unit to convert from.")
    with col3:
        to_unit = st.selectbox("To Unit", units, help="Select the unit to convert to.")

    # Convert button
    if st.button("Convert"):
        try:
            if value < 0 and category == "Temperature" and (from_unit == "Kelvin" or to_unit == "Kelvin"):
                st.error("Temperature in Kelvin cannot be negative!")
            else:
                if category == "Length":
                    result = convert_length(value, from_unit, to_unit)
                else:  # Temperature
                    result = convert_temperature(value, from_unit, to_unit)
                
                st.markdown(
                    f'<div class="result-box">{value:.2f} {from_unit} = {result:.2f} {to_unit}</div>',
                    unsafe_allow_html=True
                )
        except Exception as e:
            st.error(f"Error: {str(e)}")

    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit | © 2025")