import math
import pygame
pygame.init()

# Window just so pygame has a surface
screen = pygame.display.set_mode((640, 360))
clock = pygame.time.Clock()

# Init first joystick found
pygame.joystick.init()
if pygame.joystick.get_count() == 0:
    print("No controller detected. Plug in GameCube adapter/controller and try again.")
    raise SystemExit
js = pygame.joystick.Joystick(0)
js.init()
print(f"Using controller: {js.get_name()} with {js.get_numaxes()} axes, {js.get_numbuttons()} buttons")

DEADZONE = 0.15
WALK_SPEED = 3.5
ACCEL = 8.0
DECEL = 10.0

vel_x, vel_y = 0.0, 0.0

def deadzone(value, dz):
    return 0.0 if abs(value) < dz else value

def normalize(x, y):
    mag = math.hypot(x, y)
    if mag == 0:
        return 0.0, 0.0
    return (x / mag, y / mag)

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    # Typical mappings: axis 0 = left X, axis 1 = left Y (Y often inverted)
    raw_x = js.get_axis(0)
    raw_y = js.get_axis(1)

    # Apply deadzone and invert Y so up is positive
    x = deadzone(raw_x, DEADZONE)
    y = -deadzone(raw_y, DEADZONE)

    # Normalize so diagonals aren’t faster
    dir_x, dir_y = normalize(x, y)
    mag = math.hypot(x, y)

    # Read A button (often button 0, but adapters vary)
    a_pressed = js.get_button(0) == 1

    # Print a clean line each frame
    print(f"stick=({dir_x:.2f},{dir_y:.2f}) mag={mag:.2f}  A={a_pressed}", end="\r")

    screen.fill((10, 10, 10))
    pygame.display.flip()
    clock.tick(120)

pygame.quit()
