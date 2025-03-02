import streamlit as st

page_bg = """
<style>
body {
    background-color: #ff416c;
    background-image: linear-gradient(90deg, #ff416c, #ff4b2b);
    background-size: cover;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AdOnBoard - Futuristic UI</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pixi.js/6.5.8/pixi.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.9.4/lottie.min.js"></script>
    <style>
        body {
            background-color: #0a0a0a;
            color: white;
            font-family: Arial, sans-serif;
            text-align: center;
            overflow: hidden;
        }
        .container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 600;
            flex-direction: column;
        }
        .button {
            padding: 15px 30px;
            border: none;
            border-radius: 30px;
            color: white;
            font-size: 20px;
            cursor: pointer;
            transition: 0.3s;
        }
        .button:hover {
            transform: scale(1.1);
        }
        canvas {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚢 AdOnBoard - The Futuristic Experience</h1>
        <p>Choose your adventure in the world of maritime advertising.</p>
        <button class="button" onclick="startAnimation()">Start Game</button>
    </div>
    <canvas id="bg"></canvas>

    <script>
        // Background Animation using Three.js
        let scene = new THREE.Scene();
        let camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        let renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('bg'), alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        let geometry = new THREE.TorusGeometry(10, 3, 16, 100);
        let material = new THREE.MeshBasicMaterial({ color: 0xff4b2b, wireframe: true });
        let torus = new THREE.Mesh(geometry, material);
        scene.add(torus);

        camera.position.z = 30;

        function animate() {
            requestAnimationFrame(animate);
            torus.rotation.x += 0.01;
            torus.rotation.y += 0.01;
            renderer.render(scene, camera);
        }
        animate();

        function startAnimation() {
            gsap.to(".container", { opacity: 0, duration: 1, onComplete: () => {
                document.querySelector(".container").style.display = "none";
                console.log("Game Started!");
            }});
        }
    </script>
</body>
</html>
