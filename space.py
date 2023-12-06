import pygame
from pygame.locals import *
import random
from pygame import font

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ADDENEMY = pygame.USEREVENT + 1

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load('images/jet.png').convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.center = [10, SCREEN_HEIGHT/2]
        self.v = 1
        self.when_hit = -1

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


        if self.when_hit > 0 and pygame.time.get_ticks() - self.when_hit > 100:
            self.kill()
            global gameon
            gameon = False

    def fire(self):
        m = Missile(self.rect.right + 5, self.rect.bottom)
        missiles.add(m)
        all_sprites.add(m)

    def hit(self):
        self.surf = pygame.image.load('images/boom.png').convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.when_hit = pygame.time.get_ticks()


class Missile(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.surf = pygame.image.load('images/missile.png').convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(x,y))
        self.speed = 5

    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()



class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load('images/enemy.png').convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(820, random.randint(0, 600)))
        self.speed = random.randint(1, 2)
        self.when_hit = -1

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
        if self.when_hit > 0 and pygame.time.get_ticks() - self.when_hit > 100:
            self.kill()
            global num_enemy_killed
            num_enemy_killed += 1

    def hit(self):
        self.surf = pygame.image.load('images/boom.png').convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.when_hit = pygame.time.get_ticks()



num_enemy_killed = 0

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Variable to keep our main loop running
running = True
gameon = False

player = Player()
missiles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
clock = pygame.time.Clock()


pygame.time.set_timer(ADDENEMY, 250)

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
        elif gameon and event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    if not gameon:
        num_enemy_killed = 0
        player = Player()
        enemies = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player)
        screen.fill([0, 0, 0])
        surf = font.Font(None,36).render('Premi 1 per iniziare...', True, [255,255,255])

        screen.blit(surf, (SCREEN_WIDTH/2-surf.get_width()/2, SCREEN_HEIGHT/2))

    if gameon:
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)

        for e in enemies:
            e.update()
        for m in missiles:
            m.update()
        if pygame.sprite.spritecollideany(player, enemies):
            player.hit()

        collisions = pygame.sprite.groupcollide(missiles,enemies,True,False)
        for k,v in collisions.items():
            for e in v:
                e.hit()

            #running = False

        # This line says "Draw surf onto screen at coordinates x:400, y:300"
        screen.fill([0,0,0])
        for s in all_sprites:
            screen.blit(s.surf, s.rect)
        score = font.Font(None, 36).render(str(num_enemy_killed), True, [255, 255, 255])
        screen.blit(score, [750,20])

    pygame.display.flip()
    clock.tick(400)



