const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

canvas.width = 500;
canvas.height = 700;

let score = 0;
let vehicles = [];

// 🎵 Sounds
const burstSound = new Audio("/static/sounds/burst.mp3");
const errorSound = new Audio("/static/sounds/error.mp3");

// 🚗 Load images safely
const imageFiles = [
    "car.png", "taxi.png", "ambulance.png",
    "truck.png", "bus.png"
];

let images = [];
let loadedCount = 0;

imageFiles.forEach(name => {
    let img = new Image();
    img.src = "/static/images/" + name;

    img.onload = () => {
        loadedCount++;
        if (loadedCount === imageFiles.length) {
            startGame();   // 🚀 start ONLY after images load
        }
    };

    img.onerror = () => {
        console.error("Image failed:", name);
    };

    images.push(img);
});

// 🎲 Vehicle
function randomVehicle() {
    return {
        x: Math.random() * 400 + 40,
        y: canvas.height + Math.random() * 200,
        speed: Math.random() * 1.5 + 1,
        number: Math.floor(Math.random() * 10).toString(),
        image: images[Math.floor(Math.random() * images.length)]
    };
}

function generateVehicles(n = 6) {
    vehicles = [];
    for (let i = 0; i < n; i++) {
        vehicles.push(randomVehicle());
    }
}

// 🎨 Draw
function drawVehicle(v) {
    if (v.image.complete) {
        ctx.drawImage(v.image, v.x, v.y, 100, 70);
    } else {
        // fallback rectangle if image not loaded
        ctx.fillStyle = "black";
        ctx.fillRect(v.x, v.y, 100, 50);
    }

    // balloon
    ctx.beginPath();
    ctx.arc(v.x + 50, v.y - 30, 18, 0, Math.PI * 2);
    ctx.fillStyle = "yellow";
    ctx.fill();

    ctx.fillStyle = "black";
    ctx.font = "20px Arial";
    ctx.fillText(v.number, v.x + 42, v.y - 25);
}

// 🔄 Update loop
function update() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let i = 0; i < vehicles.length; i++) {
        let v = vehicles[i];

        v.y -= v.speed * 2;

        if (v.y < -100) {
            vehicles[i] = randomVehicle();
        }

        drawVehicle(v);
    }

    requestAnimationFrame(update);
}

// 🎮 Key press
document.addEventListener("keydown", (e) => {
    let key = e.key;

    if ("0123456789".includes(key)) {
        let matched = false;

        for (let i = 0; i < vehicles.length; i++) {
            if (vehicles[i].number === key && !matched) {
                vehicles[i] = randomVehicle();
                score++;
                burstSound.play();
                matched = true;
            }
        }

        if (!matched) errorSound.play();

        document.getElementById("score").innerText = "Score: " + score;
    }
});

// 🚀 Start game AFTER images load
function startGame() {
    generateVehicles();
    update();
}
