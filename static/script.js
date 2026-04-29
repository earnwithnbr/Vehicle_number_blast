const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

canvas.width = 500;
canvas.height = 700;

let score = 0;
let vehicles = [];

function randomVehicle() {
    return {
        x: Math.random() * 400 + 40,
        y: canvas.height + Math.random() * 200,
        speed: Math.random() * 1 + 0.5,
        number: Math.floor(Math.random() * 10).toString(),
        color: ["red", "blue", "green", "pink", "yellow"][
            Math.floor(Math.random() * 5)
        ]
    };
}

function generateVehicles(n = 6) {
    vehicles = [];
    for (let i = 0; i < n; i++) {
        vehicles.push(randomVehicle());
    }
}

function drawVehicle(v) {
    // vehicle (rectangle instead of image)
    ctx.fillStyle = "black";
    ctx.fillRect(v.x, v.y, 100, 50);

    // balloon
    ctx.beginPath();
    ctx.arc(v.x + 50, v.y - 30, 18, 0, Math.PI * 2);
    ctx.fillStyle = v.color;
    ctx.fill();

    // number
    ctx.fillStyle = "black";
    ctx.font = "20px Arial";
    ctx.fillText(v.number, v.x + 42, v.y - 25);
}

function update() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    vehicles.forEach((v, index) => {
        v.y -= v.speed;

        if (v.y < -100) {
            vehicles[index] = randomVehicle();
        }

        drawVehicle(v);
    });

    requestAnimationFrame(update);
}

document.addEventListener("keydown", (e) => {
    let key = e.key;

    if ("0123456789".includes(key)) {
        let matched = false;

        vehicles.forEach((v, index) => {
            if (v.number === key && !matched) {
                vehicles[index] = randomVehicle();
                score++;
                matched = true;
            }
        });

        document.getElementById("score").innerText = "Score: " + score;
    }
});

generateVehicles();
update();
