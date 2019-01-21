import pygame as pg
import config as c
from basetypes import *
import car

class Main():
    def __init__(self):
        pg.init()
        c.screen = pg.display.set_mode((c.SCREEN_SIZE.x, c.SCREEN_SIZE.y))
        c.clock = pg.time.Clock()
        c.cars = [car.Car(Vector2(*c.START_POS)) for _ in range(1)]

    def draw(self):
        c.screen.fill(c.BLACK)

        # Draw Track
        pg.draw.aalines(c.screen, c.RED, True, c.inner_wall, 1)
        pg.draw.aalines(c.screen, c.RED, True, c.outer_wall, 1)

        # Draw Checkpoints
        for checkpoint in c.checkpoints:
            p1 = (checkpoint[0][0], checkpoint[0][1])
            p2 = (int(checkpoint[1][0]), int(checkpoint[1][1]))
            pg.draw.line(c.screen, c.WHITE, p1, p2)

        [c.cars[i].draw() for i in range(1)]

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

            [c.cars[i].update() for i in range(1)]
            self.draw()

            if self.check_for_quit():
                break

            #Update the display
            pg.display.flip()
