import requests
import pygame
from pygame.locals import *
import random
from pygame import font

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #self.surf = pygame.Surface((20,20))
        #self.surf.fill([255,255,255])

        self.surf0 = pygame.image.load('images/tank1.png').convert()
        self.surf0.set_colorkey((255, 255, 255), RLEACCEL)
        self.surf0 = pygame.transform.scale(self.surf0, (WALL_DX-10,WALL_DY-10))

        self.surf = pygame.transform.rotate(self.surf0,90)
        self.rect = self.surf.get_rect()
        self.dx = 1
        self.dy = 0

        self.rect.center = [10, WALL_DY + WALL_DY/2]
        self.v = 1

    def update(self, pressed_keys):

        dx = 0
        dy = 0

        if pressed_keys[K_UP]:
            dy = -self.v
            self.surf = pygame.transform.rotate(self.surf0, 180)
        if pressed_keys[K_DOWN]:
            dy = self.v
            self.surf = pygame.transform.rotate(self.surf0, 0)
        if pressed_keys[K_LEFT]:
            dx = -self.v
            self.surf = pygame.transform.rotate(self.surf0, 270)
        if pressed_keys[K_RIGHT]:
            dx = self.v
            self.surf = pygame.transform.rotate(self.surf0, 90)
        self.rect.move_ip(dx,dy)

        if dx != 0 or dy !=0:
            self.dx = dx
            self.dy = dy

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

        if self.rect.right > SCREEN_WIDTH-2*WALL_DX and self.rect.top > SCREEN_HEIGHT-2*WALL_DY:
            global gameon
            gameon = False
            global maze
            maze = None
            self.kill()

        #print(self.rect.right,self.rect.top)

    def fire(self):
        x,y = self.rect.center
        m = Missile(x,y, self.dx, self.dy)
        missiles.add(m)
        all_sprites.add(m)

class Missile(pygame.sprite.Sprite):
    def __init__(self,x,y,dx,dy):
        super().__init__()
        self.surf = pygame.image.load('images/missile.png').convert()
        if dx == -1:
            self.surf = pygame.transform.rotate(self.surf, 180)
        elif dy == 1:
            self.surf = pygame.transform.rotate(self.surf, 270)
        elif dy == -1:
            self.surf = pygame.transform.rotate(self.surf, 90)
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(x,y))
        self.dx = dx
        self.dy = dy
        self.speed = 5

    def update(self):
        print(self.speed,self.dx,self.dy)
        self.rect.move_ip(self.speed*self.dx, self.speed*self.dy)
        if pygame.sprite.spritecollideany(self, wall_sprites):
            self.kill()



class Wall(pygame.sprite.Sprite):
    def __init__(self,x,y,dx,dy):
        super().__init__()
        self.surf = pygame.Surface((dx,dy))
        self.surf.fill([255,0,0])
        self.rect = self.surf.get_rect()
        self.rect.left = x
        self.rect.top = y






WALL_DX = 36
WALL_DY = 36

SCREEN_WIDTH = WALL_DX*(10*3+1)
SCREEN_HEIGHT = WALL_DY*(10*2+1)

num_enemy_killed = 0

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Variable to keep our main loop running
maze = None
running = True
gameon = False

player = Player()
missiles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
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
            if event.key == K_SPACE:
                player.fire()
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

        for m in missiles:
            m.update()

        screen.blit(player.surf,player.rect)
        for s in wall_sprites:
            screen.blit(s.surf, s.rect)
        for m in missiles:
            screen.blit(m.surf, m.rect)
        #surf = pygame.Surface((20, 20))
        #surf.fill([0, 255, 0])
        #rect = surf.get_rect()
        #rect.center = [910,580]
        #screen.blit(surf, rect)


    pygame.display.flip()
    clock.tick(400)



