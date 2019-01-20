import pygame as pg
import config as c
from basetypes import *
import car
import track

class Main():
    def __init__(self):
        pg.init()
        c.screen = pg.display.set_mode((c.SCREEN_SIZE.x, c.SCREEN_SIZE.y))
        c.clock = pg.time.Clock()
        c.car = car.Car(Vector2(*c.START_POS), 0)
        c.track = track.Track()

    def draw(self):
        c.screen.fill(c.BLACK)
        c.track.draw()
        c.car.draw()  

    def check_for_quit(self):
        """event manager for quitting the app or going back to menu"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return True

        if c.keys[pg.K_ESCAPE]:
            return True
        return False

    def main_loop(self):
        while True:
            c.delta_time = c.clock.tick(60)
            c.keys = pg.key.get_pressed()

            c.car.update()
            self.draw()

            if self.check_for_quit():
                break

            pg.display.flip()
