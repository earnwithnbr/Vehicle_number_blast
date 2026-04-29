import pygame
import random
import os

# =========================
# INIT
# =========================
pygame.init()
pygame.mixer.init()

# =========================
# WINDOW
# =========================
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Vehicle Number Blast 🎈🚗")

# =========================
# BASE FOLDER
# =========================
BASE_FOLDER = r"G:\Python_codes\Vehicle Number blast"
IMAGE_FORMATS = (".png", ".jpg", ".jpeg", ".webp")

# =========================
# LOAD NUMBER SOUNDS
# =========================
number_sounds = {}
for i in range(10):
    path = os.path.join(BASE_FOLDER, f"{i}.mp3")
    if os.path.exists(path):
        number_sounds[str(i)] = pygame.mixer.Sound(path)
    else:
        print(f"⚠ Missing sound: {i}.mp3")

# Error sound
error_sound = None
error_path = os.path.join(BASE_FOLDER, "error.mp3")
if os.path.exists(error_path):
    error_sound = pygame.mixer.Sound(error_path)
else:
    print("⚠ Missing sound: error.mp3")

# =========================
# LOAD VEHICLE IMAGES
# =========================
vehicle_images = []
for file in os.listdir(BASE_FOLDER):
    if file.lower().endswith(IMAGE_FORMATS):
        img = pygame.image.load(os.path.join(BASE_FOLDER, file)).convert_alpha()
        img = pygame.transform.smoothscale(img, (100, 70))
        vehicle_images.append(img)

if not vehicle_images:
    raise SystemExit("❌ No vehicle images found!")

# =========================
# FONTS
# =========================
font_big = pygame.font.SysFont("Arial", 26, bold=True)
font_small = pygame.font.SysFont("Arial", 22)

# =========================
# KEY MAP (TOP + NUMPAD)
# =========================
KEY_TO_NUMBER = {
    pygame.K_0: "0", pygame.K_1: "1", pygame.K_2: "2",
    pygame.K_3: "3", pygame.K_4: "4", pygame.K_5: "5",
    pygame.K_6: "6", pygame.K_7: "7", pygame.K_8: "8",
    pygame.K_9: "9",

    pygame.K_KP0: "0", pygame.K_KP1: "1", pygame.K_KP2: "2",
    pygame.K_KP3: "3", pygame.K_KP4: "4", pygame.K_KP5: "5",
    pygame.K_KP6: "6", pygame.K_KP7: "7", pygame.K_KP8: "8",
    pygame.K_KP9: "9",
}

# =========================
# VEHICLE CLASS
# =========================
class Vehicle:
    def __init__(self):
        self.image = random.choice(vehicle_images)
        self.number = str(random.randint(0, 9))
        self.x = random.randint(40, WIDTH - 140)
        self.y = HEIGHT + random.randint(50, 300)
        self.speed = random.uniform(0.4, 0.8)
        self.balloon_color = random.choice([
            (255, 99, 71), (135, 206, 250),
            (144, 238, 144), (255, 182, 193),
            (255, 255, 102)
        ])

    def move(self):
        self.y -= self.speed

    def draw(self):
        # Vehicle
        screen.blit(self.image, (self.x, int(self.y)))

        # Balloon
        bx = self.x + self.image.get_width() // 2
        by = int(self.y) - 35

        pygame.draw.line(screen, (120, 120, 120),
                         (bx, by + 15), (bx, int(self.y)), 2)
        pygame.draw.circle(screen, self.balloon_color, (bx, by), 18)

        num_text = font_big.render(self.number, True, (0, 0, 0))
        screen.blit(
            num_text,
            (bx - num_text.get_width() // 2,
             by - num_text.get_height() // 2)
        )

# =========================
def generate_vehicles(n=6):
    return [Vehicle() for _ in range(n)]

# =========================
# MAIN LOOP
# =========================
def main():
    global WIDTH, HEIGHT, screen

    vehicles = generate_vehicles()
    score = 0
    running = True

    while running:
        screen.fill((230, 245, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

            if event.type == pygame.KEYDOWN and event.key in KEY_TO_NUMBER:
                pressed = KEY_TO_NUMBER[event.key]
                match_found = False

                for v in vehicles:
                    if v.number == pressed:
                        vehicles.remove(v)
                        vehicles.append(Vehicle())
                        score += 1

                        if pressed in number_sounds:
                            number_sounds[pressed].play()

                        match_found = True
                        break

                if not match_found and error_sound:
                    error_sound.play()

        for v in vehicles[:]:
            v.move()
            if v.y < -100:
                vehicles.remove(v)
                vehicles.append(Vehicle())
            else:
                v.draw()

        screen.blit(font_small.render(f"Score: {score}", True, (0, 0, 0)), (20, 20))
        screen.blit(font_small.render("Press 0–9 (Top / NumPad)", True, (0, 0, 0)),
                    (20, HEIGHT - 40))

        pygame.display.update()
        pygame.time.delay(30)

    pygame.quit()

main()
