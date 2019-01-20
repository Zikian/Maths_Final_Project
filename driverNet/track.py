import config as c
from basetypes import Vector2
import pygame as pg

class Track():
    def draw(self):
        pg.draw.aalines(c.screen, c.WHITE, True, c.track_data["innerWall"], 1)
        pg.draw.aalines(c.screen, c.WHITE, True, c.track_data["outerWall"], 1)

    