import pygame
from pygame.locals import *
import random
from pygame import font

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

clock = pygame.time.Clock()

surf = pygame.Surface((75, 25))
surf.fill((255, 255, 255))
rect = surf.get_rect()
rect.center = [10, SCREEN_HEIGHT/2]
v = 1

def update(pressed_keys):
    if pressed_keys[K_UP]:
        rect.move_ip(0, -v)
    if pressed_keys[K_DOWN]:
        rect.move_ip(0, v)
    if pressed_keys[K_LEFT]:
        rect.move_ip(-v, 0)
    if pressed_keys[K_RIGHT]:
        rect.move_ip(v, 0)

    # Keep player on the screen
    if rect.left < 0:
        rect.left = 0
    elif rect.right > SCREEN_WIDTH:
        rect.right = SCREEN_WIDTH
    if rect.top <= 0:
        rect.top = 0
    elif rect.bottom >= SCREEN_HEIGHT:
        rect.bottom = SCREEN_HEIGHT


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Variable to keep our main loop running
running = True

# Our main loop!
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event; KEYDOWN is a constant defined in pygame.locals, which we imported earlier
        if event.type == KEYDOWN:
            # If the Esc key has been pressed set running to false to exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event; if QUIT, set running to false
        elif event.type == QUIT:
            running = False



    pressed_keys = pygame.key.get_pressed()
    update(pressed_keys)


    # This line says "Draw surf onto screen at coordinates x:400, y:300"
    screen.fill([0,0,0])

    screen.blit(surf, rect)

    pygame.display.flip()
    clock.tick(400)



