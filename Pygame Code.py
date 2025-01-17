import pygame
import random

from pygame.locals import (
    RLEACCEL,
    K_UP, 
    K_DOWN, 
    K_LEFT, 
    K_RIGHT, 
    K_ESCAPE, 
    KEYDOWN,
    QUIT,
    K_SPACE) # Button to fire


# Sizing
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

PLAYER_SIZE = (90, 36)
ENEMY_SIZE = (70, 34)
CLOUD_SIZE = (80, 39)
BULLET_SIZE = (40, 40)

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

BULLET_SPEED = 10
BULLET_COLOR = (255, 0, 0)
BULLET_COOLDOWN = 3000


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("jet.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, PLAYER_SIZE)
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.last_shot_time = -BULLET_COOLDOWN # Add variable to track time since last shot

    def update(self, pressed_key, current_time):
        # print(pressed_key)
        if pressed_key[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_key[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_key[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_key[K_RIGHT]:
            self.rect.move_ip(5, 0)

        #Keep player on screen
        if self.rect.left < 0:
          self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
          self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
          self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
          self.rect.bottom = SCREEN_HEIGHT

        # Check if enough time has passed since last shot
        if pressed_key[K_SPACE]:
          time_since_last_shot = current_time - self.last_shot_time
          if time_since_last_shot > BULLET_COOLDOWN: # 3 second cooldown
            self.last_shot_time = current_time
            self.shoot(all_sprites, bullets)
            self.last_shot_time = current_time
      
          
    def shoot(self, all_sprites, bullets):
      bullet = Bullet(self.rect.midtop)
      all_sprites.add(bullet)
      bullets.add(bullet)

class Enemy(pygame.sprite.Sprite):
  def __init__(self):
    super(Enemy, self).__init__()
    self.surf = pygame.image.load("missile.png").convert_alpha()
    self.surf = pygame.transform.scale(self.surf, ENEMY_SIZE)
    self.surf.set_colorkey((255, 255, 255), RLEACCEL)
    self.rect = self.surf.get_rect(
      center=(random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), random.randint(0, SCREEN_HEIGHT),))

    self.speed = random.randint(5, 10)

  def update(self):
    self.rect.move_ip(-self.speed, 0)
    if self.rect.right <0:
      self.kill()


class Cloud(pygame.sprite.Sprite):
  def __init__(self):
    super(Cloud, self).__init__()
    self.surf = pygame.image.load("cloud.png").convert_alpha()
    self.surf = pygame.transform.scale(self.surf, CLOUD_SIZE)
    self.surf.set_colorkey((0, 0, 0), RLEACCEL)
    self.rect = self.surf.get_rect(
      center=(random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), random.randint(0, SCREEN_HEIGHT),))

  def update(self):
    self.rect.move_ip(-5, 0)
    if self.rect.right < 0:
      self.kill()

class Bullet(pygame.sprite.Sprite):
  def __init__(self, center):
    super().__init__()
    self.surf = pygame.image.load("bullet.png").convert_alpha()
    self.surf = pygame.transform.scale(self.surf, BULLET_SIZE)
    self.surf.set_colorkey((0, 0, 0), RLEACCEL)
    self.rect = self.surf.get_rect(center=center)
    
    self.speed = 10
    self.color = (135, 206, 250)

  def update(self):
    if self.rect.bottom < 0:
      self.kill()
  
    self.rect.move_ip(+self.speed, 0)
      
    if pygame.sprite.spritecollide(self, enemies, True):
      self.kill()

    
    
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jet Fighter Game")

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 750)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

player = Player()

enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
              running = False
            # if event.key == K_SPACE:
            #   player.shoot(all_sprites, bullets)

        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:
          new_enemy = Enemy()
          enemies.add(new_enemy)
          all_sprites.add(new_enemy)

        elif event.type == ADDCLOUD:
          new_cloud = Cloud()
          clouds.add(new_cloud)
          all_sprites.add(new_cloud)
            

    screen.fill((135, 206, 250))

    for entity in all_sprites:
      screen.blit(entity.surf, entity.rect)


    if pygame.sprite.spritecollideany(player, enemies):
      player.kill()
      running = False

    # for bullet in bullets:
    #   bullet.update(player.rect.midtop)

    current_time = pygame.time.get_ticks()
    pressed_keys = pygame.key.get_pressed()
    player_pos = player.rect.midtop
    player.update(pressed_keys, current_time)
      
    # screen.blit(player.surf, player.rect)

    
    # if pressed_keys[K_SPACE]:
    #   new_bullet = Bullet(player.rect.midtop)
    #   bullets.add(new_bullet)
    #   all_sprites.add(new_bullet)


    # for entity in all_sprites:
    #   if hasattr(entity, "update"):
    #     entity.update(pressed_keys, current_time)

    # player.update(pressed_keys, pygame.time.get_ticks())
    bullets.update()
    enemies.update()
    clouds.update()

    # screen.fill((135, 206, 250))

    pygame.display.flip()

    clock.tick(30)



pygame.quit()
