import pygame as pg
from settings import *
import random
from os import path
from map import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        pg.sprite.Sprite.__init__(self)    
        # player attributes
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.can_dash = False
        self.can_jump = False
        self.obtained_quest_items = []
        self.direction = "right"
        # player sprite
        self.image = pg.image.load(path.join(self.game.img_dir, "787.jpg")).convert_alpha()
        self.image = pg.transform.scale(self.image, (int(self.image.get_width() /3 ), int(self.image.get_height() / 3)))
        # player rect and player hitbox rect
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        
    def move(self):
        self.acc = vec(0, 0.5)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC      
            if self.direction == "right":
                self.image = pg.transform.flip(self.image, 1, 0)
                self.direction = "left"
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
            if self.direction == "left":
                self.image = pg.transform.flip(self.image, 1, 0)
                self.direction = "right"
        self.fly()
            
        # apply friction
        self.acc.x += self.vel.x * -PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + PLAYER_ACC * self.acc
    
    def draw(self):
        pg.draw.rect(self.game.map_img, (255, 0 ,0), (self.hit_rect.x, self.hit_rect.y, self.hit_rect.width, self.hit_rect.height), 2)

        
    def fly(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LALT]:
            self.acc = vec(0, 0)
            if keys[pg.K_UP]:
                self.acc.y = -PLAYER_ACC
            if keys[pg.K_DOWN]:
                self.acc.y = PLAYER_ACC
            if keys[pg.K_LEFT]:
                self.acc.x = -PLAYER_ACC      
                if self.direction == "right":
                    self.image = pg.transform.flip(self.image, 1, 0)
                    self.direction = "left"
            if keys[pg.K_RIGHT]:
                self.acc.x = PLAYER_ACC
                if self.direction == "left":
                    self.image = pg.transform.flip(self.image, 1, 0)
                    self.direction = "right"
            self.acc.y += self.vel.y * -PLAYER_FRICTION

    def object_collision(self, direction):
        # horizontal collision
        if direction == 'x':
            hits = pg.sprite.spritecollide(self, self.game.platforms, False, self.collide_hit_rect)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.hit_rect.width / 2
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right + self.hit_rect.width / 2
                self.vel.x = 0
                self.hit_rect.centerx = self.pos.x
        # vertical collision
        if direction == 'y':
            hits = pg.sprite.spritecollide(self, self.game.platforms, False, self.collide_hit_rect)
            if hits:
                if self.vel.y >= 0.5:
                    self.pos.y = hits[0].rect.top - self.hit_rect.height / 2
                    self.can_dash = True
                    self.can_jump = True
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom + self.hit_rect.height / 2
                self.vel.y = 0
                
                self.hit_rect.centery = self.pos.y
        
    def item_collision(self):
        hits = pg.sprite.spritecollide(self, self.game.spikes, False, self.collide_hit_rect)
        if hits:
            print("jaja te moriste pete")
            exit()  
        hits = pg.sprite.spritecollide(self, self.game.quest_items, True, self.collide_hit_rect)
        #MEJORAR ESTA CAGADA
        if hits:
            if type(hits[0]) == Key:
                if hits[0].color == BLUE:
                    self.obtained_quest_items.append("blue_key")
                if hits[0].color == RED:
                    self.obtained_quest_items.append("red_key")
                if hits[0].color == GREEN:
                    self.obtained_quest_items.append("green_key")
                if hits[0].color == YELLOW:
                    self.obtained_quest_items.append("yellow_key")
                    
        hits = pg.sprite.spritecollide(self, self.game.coins, True, self.collide_hit_rect)
        if hits:
            self.game.score += 1
                    
    def update(self):
        self.move()
        
        self.hit_rect.centery = self.pos.y
        self.object_collision('y')
        self.hit_rect.centerx = self.pos.x
        self.object_collision('x')
        self.item_collision()
        
        self.rect.center = self.hit_rect.center
        print(self.rect.center)
        
    def jump(self):
        self.vel.y = -PLAYER_JUMP_SPEED
    
    def dashh(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.vel.x = -PLAYER_DASH_SPEED - self.vel.x*-2
        if keys[pg.K_RIGHT]:
            self.vel.x = PLAYER_DASH_SPEED + self.vel.x*2

    def collide_hit_rect(self, one, two):
        return one.hit_rect.colliderect(two.rect)    



    
class Spritesheet:
    #utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
    
    def get_image(self, height, width, y, x):
        # get an image out of a spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        #image = pg.transform.scale(image, (int(width * 2), int(height * 2)))
        return image

class Floor(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.rect = pg.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect.x = x
        self.rect.y = y

class Spike(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pg.sprite.Sprite.__init__(self)
        self.rect = pg.Rect(x, y, width, height)

class Key(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height, img, color):
        self.game = game
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(path.join(self.game.img_dir, img)).convert_alpha()
        
        self.rect = pg.Rect(x, y, width, height)
        self.image = pg.transform.scale(self.image, (int(width), int(height)))
        self.color = color

class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height, img):
        self.game = game
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(path.join(self.game.img_dir, img)).convert_alpha()
        self.rect = pg.Rect(x, y, width, height)
        #self.image = pg.transform.scale(self.image, (self.rect.width, self.rect.height))
        
        

        #pg.Rect(x, y, width, height)
        #self.rect.x = self.rect.x - width/2
