from settings import *
import pytmx
import pygame as pg
class Map: 
    def __init__(self, filename):
        #MAP
        self.map_data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.map_data.append(line)
        
        self.tilewidth = len(self.map_data[0])
        self.tileheight = len(self.map_data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha = True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile =  ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))
                              
    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        self.rect = temp_surface.get_rect()
        return temp_surface

class Camera:
    def __init__(self, game, width, height):
        self.game = game
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)
    
    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)
    
    def update(self, target):
        x = -target.rect.x + int(WIDTH/2)-target.image.get_width() / 2
        y = -target.rect.y + int(HEIGHT/2+HEIGHT/10)
        self.camera = pg.Rect(x, y, self.width, self.height)