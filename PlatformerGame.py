# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 23:02:10 2020

@author: corey
"""
import pygame
from pygame.locals import *
import sys
import random

#Author : Corey
#Date   : 11/18/20
#File   : PlatformerGame.py

"""
Hello! This is my final project, which is a platforming game.
Pretty basic, but I learned loads about hwo games can work internally.
Main of which is framerate and some math to go with game development.

The controls are the left and right arrow keys, And the spacebar.
You can hold down the space bar for greater jumps or let go to close small distances.
"""

pygame.init()
vec = pygame.math.Vector2

HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

#Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128, 255, 40))
        self.rect = self.surf.get_rect(center = (10, 420))
        

        #adding movement
        self.pos = vec((10, 385))
        self.vel = vec(0,0)
        self.acc = vec(0,0) 
    
    #This checks whether the player is colliding with other sprites or is jumping.
    def update(self):
        hits = pygame.sprite.spritecollide(P1, platforms, False)
        if P1.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0
                    self.jumping = False
                    
                    
                self.pos.y = hits[0].rect.top + 1
                self.vel.y = 0
                
    #This makes the character jump
    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -15
            
    #This allows you to make smaller little hops instead of huge jumps every time.
    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < 3:
                self.vel.y = -3
        
   #Creates player movement.     
    def move(self):
        self.acc = vec(0,0.5)
        
        pressed_keys = pygame.key.get_pressed()
        
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
            
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
            
        self.rect.midbottom = self.pos

#Class for platforms to jump on.        
class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50,100), 12))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center = (random.randint(0, WIDTH - 10),
                                                 random.randint(0, HEIGHT - 30)))
        self.speed = random.randint(-1, 1)
        self.moving = True
    #This is supposed to make the platforms move, but I couldn't quite get it working.
    def move(self):
        if self.moving == True:
            self.rect.move_ip(self.speed,0)
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH
                
#This method generates an endless amount of platforms for the player to navigate.
def plat_gen():
    while len(platforms) < 7:
        width = random.randrange(50,100)
        p = platform()
        C = True
        
        while C:
            p= platform()
            p.rect.center = (random.randrange(0, WIDTH - width)
                        ,random.randrange(-50, 0))
            C = check(p, platforms)
            
        platforms.add(p)
        all_sprites.add(p)
        
#This checks where the platforms will spawn so they don't get clustered up and awkward.    
def check(platform, groupies):
    if pygame.sprite.spritecollideany(platform,groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 40 ) and (abs(platform.rect.bottom - entity.rect.top) < 40):
                return True
        C = False
        
#Assigning base values        
PT1 = platform()
P1 = Player()

PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((255,0,0))
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
PT1.moving = False

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

platforms = pygame.sprite.Group()
platforms.add(PT1)

#Spawns in base platforms
for x in range(random.randint(5, 6)):
    pl = platform()
    platforms.add(pl)
    all_sprites.add(pl)
    
#Game Loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                P1.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                P1.cancel_jump()
                
    displaysurface.fill((0, 0, 0))
                
    P1.move()
    plat_gen()
    P1.update()

    
    #Infinite Scrolling screen
    if P1.rect.top <= HEIGHT / 3:
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()
                
    #code to end the game if player falls below the screen
    if P1.rect.top > HEIGHT:
            for entity in all_sprites:
                entity.kill()
                time.sleep(1)
                displaysurface.fill((255,0,0))
                pygame.display.update()
                time.sleep(1)
                pygame.quit()
                sys.exit
    
    
    
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)

    pygame.display.update()
    FramePerSec.tick(FPS)
    
    
"""
I couldn't quite get the platform movement function to work
but the code is there, so with more time to tweak it I could
get it working for sure. Also there is a bug which causes a 
freeze/game crash, haven't found the reason for it, but it's 
rather minimal I've found.
"""
    




