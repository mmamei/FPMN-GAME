import pygame
from pygame.locals import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

surf = pygame.Surface((75, 25))
surf.fill((255, 255, 255))
rect = surf.get_rect()
rect.center = [100, SCREEN_HEIGHT/2]

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Variable to keep our main loop running
running = True

# Our main loop!
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False


    screen.fill([0,0,0])
    screen.blit(surf, rect)
    pygame.display.flip()



