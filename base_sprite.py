import pygame
from pygame.locals import *
import random
from pygame import font

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.center = [10, SCREEN_HEIGHT/2]
        self.v = 1

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.v)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.v)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.v, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.v, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Variable to keep our main loop running
running = True

player = Player()

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
    player.update(pressed_keys)






    # This line says "Draw surf onto screen at coordinates x:400, y:300"
    screen.fill([0,0,0])

    screen.blit(player.surf, player.rect)

    pygame.display.flip()
    clock.tick(400)



