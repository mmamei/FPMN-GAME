import requests
import pygame
from pygame.locals import *
import random
from pygame import font

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((20,20))
        self.surf.fill([255,255,255])
        self.rect = self.surf.get_rect()
        self.rect.center = [10, WALL_DY + 12]
        self.v = 1

    def update(self, pressed_keys):

        dx = 0
        dy = 0

        if pressed_keys[K_UP]:
            dy = -self.v
        if pressed_keys[K_DOWN]:
            dy = self.v
        if pressed_keys[K_LEFT]:
           dx  = -self.v
        if pressed_keys[K_RIGHT]:
           dx = self.v
        self.rect.move_ip(dx,dy)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        if pygame.sprite.spritecollideany(self,wall_sprites):
            self.rect.move_ip(-dx,-dy)

        if self.rect.right > 910 and self.rect.top > 560:
            global gameon
            gameon = False
            global maze
            maze = None
            self.kill()

        print(self.rect.right,self.rect.top)





class Wall(pygame.sprite.Sprite):
    def __init__(self,x,y,dx,dy):
        super().__init__()
        self.surf = pygame.Surface((dx,dy))
        self.surf.fill([255,0,0])
        self.rect = self.surf.get_rect()
        self.rect.left = x
        self.rect.top = y





SCREEN_WIDTH = 930
SCREEN_HEIGHT = 700
WALL_DX = 30
WALL_DY = 30

num_enemy_killed = 0

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Variable to keep our main loop running
maze = None
running = True
gameon = False

player = Player()
wall_sprites = pygame.sprite.Group()

# Our main loop!
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event; KEYDOWN is a constant defined in pygame.locals, which we imported earlier
        if event.type == KEYDOWN:
            # If the Esc key has been pressed set running to false to exit the main loop
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_1:
                gameon = True
        # Check for QUIT event; if QUIT, set running to false
        elif event.type == QUIT:
            running = False
    screen.fill([0, 0, 0])
    if not gameon:
        surf = font.Font(None,36).render('Premi 1 per iniziare...', True, [255,255,255])
        screen.blit(surf, (SCREEN_WIDTH/2-surf.get_width()/2, SCREEN_HEIGHT/2))
        if maze == None:
            player = Player()
            wall_sprites = pygame.sprite.Group()
            maze = requests.post('http://www.delorie.com/game-room/mazes/genmaze.cgi',
                          data={'cols': '10', 'rows': '10', 'type': 'text'})


            y = 0


            for l in maze.text.splitlines():
                if not l.startswith('<'):
                    x = 0
                    for c in l:
                        if c != ' ':
                            w = Wall(x, y, WALL_DX, WALL_DY)
                            wall_sprites.add(w)
                        x += WALL_DX
                    y +=WALL_DY




    if gameon:
        player.update(pygame.key.get_pressed())
        screen.blit(player.surf,player.rect)
        for s in wall_sprites:
            screen.blit(s.surf, s.rect)

        #surf = pygame.Surface((20, 20))
        #surf.fill([0, 255, 0])
        #rect = surf.get_rect()
        #rect.center = [910,580]
        #screen.blit(surf, rect)


    pygame.display.flip()
    clock.tick(400)



