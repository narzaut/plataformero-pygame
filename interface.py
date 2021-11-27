import pygame as pg
import random
import os
from os import path
from settings import *
from sprites import *
from map import *

    
class Ui:
    def __init__(self, game, width, height):     
        self.game = game
        self.surface = pg.Surface((width, height), pg.SRCALPHA, 32)
        self.width = width
        self.height = height
        self.load_images()
        
        #blit empty keys
        self.surface.blit(self.key_red_disabled, (0, 20)) 
        self.surface.blit(self.key_yellow_disabled, (SPACING, 20))
        self.surface.blit(self.key_green_disabled, (SPACING*2,20))
        self.surface.blit(self.key_blue_disabled, (SPACING*3, 20))

    
    def update(self):
        #replace empty key blit with actual key
        if "blue_key" in self.game.player.obtained_quest_items:
            self.surface.fill(pg.SRCALPHA, (SPACING*3, 20, 44,40))
            self.surface.blit(self.key_blue, (SPACING*3, 20))
        if "green_key" in self.game.player.obtained_quest_items:
            self.surface.fill(pg.SRCALPHA, (SPACING*2, 20, 44,40))
            self.surface.blit(self.key_green, (SPACING*2, 20))
        if "yellow_key" in self.game.player.obtained_quest_items:
            self.surface.fill(pg.SRCALPHA, (SPACING, 20, 44,40))
            self.surface.blit(self.key_yellow, (SPACING, 20))
        if "red_key" in self.game.player.obtained_quest_items:
            self.surface.fill(pg.SRCALPHA, (0, 20, 44,40))
            self.surface.blit(self.key_red, (0, 20))

    def load_images(self):
        #load key sprites
        self.key_red_disabled = pg.image.load(path.join(self.game.img_dir, "hud_keyRed_disabled.png")).convert_alpha()
        self.key_red = pg.image.load(path.join(self.game.img_dir, "hud_keyRed.png")).convert_alpha()
        self.key_yellow_disabled = pg.image.load(path.join(self.game.img_dir, "hud_keyYellow_disabled.png")).convert_alpha()
        self.key_yellow = pg.image.load(path.join(self.game.img_dir, "hud_keyYellow.png")).convert_alpha()
        self.key_green_disabled = pg.image.load(path.join(self.game.img_dir, "hud_keyGreen_disabled.png")).convert_alpha()
        self.key_green = pg.image.load(path.join(self.game.img_dir, "hud_keyGreen.png")).convert_alpha()
        self.key_blue_disabled = pg.image.load(path.join(self.game.img_dir, "hud_keyBlue_disabled.png")).convert_alpha()
        self.key_blue = pg.image.load(path.join(self.game.img_dir, "hud_keyBlue.png")).convert_alpha()   
