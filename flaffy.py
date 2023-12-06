import pygame
from pygame.locals import *
import random

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
G = 1
JUMP = -10
VX = -10

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = ['bird', 'birdl', 'bird', 'birdu']
        self.surfX = []
        for i in self.img:
            surf = pygame.transform.scale(ssheet.get_image(i), (50, 50))
            rect = surf.get_rect()
            self.surfX.append(surf)

        self.setImg(0)
        self.rect = self.surf.get_rect()
        self.restart()

    def setImg(self, i):
        self.surf = self.surfX[i]


    def restart(self):
        self.imgi = 0
        self.last_img_update_time = 0
        self.vy = 0
        self.x = 50
        self.y = 1
        self.rect.left = self.x
        self.rect.top = self.y

    def update(self, jump):
        print(self.rect.top,self.vy)
        if pygame.time.get_ticks() - self.last_img_update_time > 50:
            self.imgi = (self.imgi + 1) % len(self.img)
            self.setImg(self.imgi)
            self.last_img_update_time = pygame.time.get_ticks()
        if jump:
            print('jump')
            self.vy += JUMP
            if self.vy > JUMP:
                self.vy = JUMP
        self.vy += G
        self.rect.move_ip(0, self.vy)

        if self.rect.top <= 0:
            self.rect.top = 0
            self.vy = 1
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.vy = 0
    def blit(self):
        screen.blit(self.surf, self.rect)

class Wall(pygame.sprite.Sprite):
    def __init__(self, y, top):
        super().__init__()
        self.surf = ssheet.get_image('wall')
        self.surf = pygame.transform.flip(self.surf, False, top)
        self.surf = pygame.transform.scale(self.surf, (100, SCREEN_HEIGHT))
        self.rect = self.surf.get_rect()
        self.rect.left = SCREEN_WIDTH
        if top:
            self.rect.bottom = y
        else:
            self.rect.top = y

    def update(self):
        self.rect.move_ip(VX,0)

        global score
        if self.rect.right < 0:
            score.score += 1
            self.kill()

    def blit(self):
        screen.blit(self.surf, self.rect)

class SpriteSheet():
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert()
        self.rect = self.sheet.get_rect()
        self.dict = {
            'bg':(0,0,144,256),
            'bird':(114,380,132-114,396-380),
            'birdl':(114,432,132-114,448-432),
            'birdu':(114,380,132-114,396-380),
            'wall':(0,324,26,483-326),
            'gameover': (394, 57, 493-394, 81-57)
        }

    def get_image(self, img):
        x, y, w, h = ssheet.dict[img]
        image = pygame.Surface([w, h]).convert()
        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sheet, (0, 0), (x, y, w, h))
        image.set_colorkey((255,255,255))
        # Return the image
        return image


class Score():
    def __init__(self):
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        self.score = 0
        # Prepare the initial score images.
        self.update()
    def update(self):
        score_str = str(self.score)
        self.surf = self.font.render(score_str, True, self.text_color,[84,192,201])
        self.rect = self.surf.get_rect()
        self.rect.left = SCREEN_WIDTH - 40
        self.rect.top = 20
    def blit(self):
        screen.blit(self.surf,self.rect)




# initialize pygame
pygame.init()

# create the screen object
# here we pass it a size of 800x600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# instantiate our player; right now he's just a rectangle

ssheet = SpriteSheet('images/Mobile - Flappy Bird - Version 12 Sprites.png')
player = Player()
walls = pygame.sprite.Group()
score = Score()


# Variable to keep our main loop running
running = True
gameover = False
ADD_WALL = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_WALL, 2000)
clock = pygame.time.Clock()
# Our main loop!
while running:
    clock.tick(50)
    jump = False
    for event in pygame.event.get():
        # Check for KEYDOWN event; KEYDOWN is a constant defined in pygame.locals, which we imported earlier
        if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
            running = False
        if event.type == KEYDOWN and event.key == pygame.K_SPACE:
            jump = True
        if ((score.score + 1) % 10 == 0):
            print('speedup')
            VX -= 1
            score.score += 1

        if (event.type == ADD_WALL):
            type = random.randint(1, 3)
            y = random.randint(100, 500)
            if type == 1:
                walls.add(Wall(y, True))
            if type == 2:
                walls.add(Wall(y, False))
            if type == 3:
                walls.add(Wall(y, True))
                walls.add(Wall(y + 200, False))

    if pygame.sprite.spritecollideany(player, walls):
        gameover = True
        player.kill()

    if gameover:
        img = ssheet.get_image('gameover')
        img = pygame.transform.scale(img, (200, 100))
        screen.blit(img, ((SCREEN_WIDTH/2)-100, SCREEN_HEIGHT/3))

    if gameover and jump:
        player.restart()
        score.score = 0
        VX = -5
        walls = pygame.sprite.Group()
        gameover = False


    if not gameover:
        player.update(jump)
        walls.update()
        score.update()

        img = ssheet.get_image('bg')
        img = pygame.transform.scale(img,(SCREEN_WIDTH,SCREEN_HEIGHT))
        screen.blit(img, (0, 0))

        player.blit()
        for w in walls:
            w.blit()

        score.blit()

    pygame.display.flip()
