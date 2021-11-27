import pygame as pg
import random
import os
from os import path
from settings import *
from sprites import *
from map import *
from interface import *
class Game:
    def __init__(self):
        # initialize window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.load_data()
    
    def decision(self, probability):
        return random.randrange(0, 100) < probability

    def load_data(self):
        self.game_dir = path.dirname(__file__)
        self.img_dir = path.join(self.game_dir, "spritesheets")
        self.map_dir = path.join(self.game_dir, "maps")
        
        #Load character sprite
        #self.character_spritesheet = Spritesheet(path.join(self.img_dir, CHARACTER_SPRITESHEET))
        
        #Load map
        self.map = TiledMap(path.join(self.map_dir, "level1.tmx"))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player_g = pg.sprite.Group()
        self.floor = pg.sprite.Group()
        self.spikes = pg.sprite.Group()
        self.quest_items = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.score = 0
        self.font = pg.font.Font(None, 25)
        self.ui = Ui(self, 300, 500)
        #create object hitboxes
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'floor':
                f = Floor(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                self.platforms.add(f)
            if tile_object.name == 'spike':
                s = Spike(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                self.spikes.add(s)
            if tile_object.name == 'key':
                if tile_object.type == "blue":
                    j = Key(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, "keyBlue.png" ,BLUE)
                    self.quest_items.add(j)
                    self.all_sprites.add(j)
                if tile_object.type == "red":
                    j = Key(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, "keyRed.png" ,RED)
                    self.quest_items.add(j)
                    self.all_sprites.add(j)
                if tile_object.type == "green":
                    j = Key(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, "keyGreen.png" ,GREEN)
                    self.quest_items.add(j)
                    self.all_sprites.add(j)
                if tile_object.type == "yellow":
                    j = Key(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, "keyYellow.png" ,YELLOW)
                    self.quest_items.add(j)
                    self.all_sprites.add(j)
            if tile_object.name == 'coin':
                c = Coin(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, "coinGold.png")
                self.all_sprites.add(c)
                self.coins.add(c)
            if tile_object.name == 'player':
                #spawn player
                self.player = Player(self, tile_object.x, tile_object.y)
                self.all_sprites.add(self.player)

        #create camera
        self.camera = Camera(self, self.map.width, self.map.height)
        self.run()
        
    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        self.camera.update(self.player)
        self.ui.update()
        
    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            # check for key pressed
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP and self.player.can_jump:
                    self.player.jump()
                    self.player.can_jump = False
                if event.key == pg.K_LSHIFT and self.player.can_dash:
                    self.player.dashh()
                    self.player.can_dash = False
                    

    def draw(self):
        # Game Loop - draw
        fps = self.font.render(str(int(self.clock.get_fps())), True, pg.Color('black'))
        # draw map 
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map.rect))
        # draw ui
        self.screen.blit(self.ui.surface, (WIDTH-self.ui.width, 0))
        #draw sprites
        for sprite in self.all_sprites:
                self.screen.blit(sprite.image, self.camera.apply(sprite)) 
                #test - delete later
                if sprite in self.quest_items:
                    #pg.draw.rect(self.map_img, (255, 0 ,0), (sprite.rect.x, sprite.rect.y, sprite.rect.width, sprite.rect.height), 2)
                    pass

        #draw fps
        self.screen.blit(fps, (5,5))
        pg.display.flip()

    def show_start_screen(self):
        # splash/start screen
        pass

    def show_go_screen(self):
        # over/continue
        pass

    def draw_grid(self):
        #draws a grid on the screen
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, BLACK, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, BLACK, (0, y), (WIDTH, y))
    
    def draw_hitbox(self, rect):
        pg.draw.rect(self.screen, (255, 0 ,0), (rect.x, rect.y, 150, 150), 2)

os.environ['SDL_VIDEO_CENTERED'] = '1'
g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()