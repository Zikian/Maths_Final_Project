import pygame as pg
import config as c
from basetypes import *
import car
import random

class Main():
    def __init__(self):
        pg.init()
        c.screen = pg.display.set_mode((c.SCREEN_SIZE.x, c.SCREEN_SIZE.y))
        c.clock = pg.time.Clock()

        c.cars = [car.Car(i) for i in range(c.POP_SIZE)]

    def draw(self):
        c.screen.fill(c.BLACK)

        # Draw Track
        pg.draw.aalines(c.screen, c.RED, True, c.inner_wall, 1)
        pg.draw.aalines(c.screen, c.RED, True, c.outer_wall, 1)

        # Draw Checkpoints
        for i, checkpoint in enumerate(c.checkpoints):
            if(i >= c.max_checkpoint_count):
                p1 = (checkpoint[0][0], checkpoint[0][1])
                p2 = (int(checkpoint[1][0]), int(checkpoint[1][1]))
                pg.draw.line(c.screen, c.WHITE, p1, p2)

        # Draw info text
        font = pg.font.Font('ComicSans.ttf', 15)
        text = font.render("Generation: " + str(c.generation), True, (255, 255, 255))
        c.screen.blit(text, (10, 10))

        [c.cars[i].draw() for i in range(c.POP_SIZE)]

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

            [c.cars[i].update() for i in range(c.POP_SIZE)]
            self.check_simulation_state()
            self.draw()

            if self.check_for_quit():
                break

            #Update the display
            pg.display.flip()

    def reset_simulation(self):
        c.crashed_cars = 0
        c.max_checkpoint_count = 0
        fittest_cars = [0, 1, 2, 3, 4]
        c.high_scores = [0] * 5

    def check_simulation_state(self):
        if(c.crashed_cars == c.POP_SIZE):
            self.create_next_generation()
            self.reset_simulation()

    def create_next_generation(self):
        newCars = []
        fittest_cars = []
        for i in range(5):
            fittest_cars += [c.fittest_cars[i]] * int(100 / (2*(i+1)))

        for i in range(5):
            first_parent = random.choice(fittest_cars)
            second_parent = self.get_second_parent(first_parent, fittest_cars)

            child1 = car.Car(i)
            child1.net.load_parameters(c.cars[first_parent].net.crossbreed(c.cars[second_parent].net))
            
            child2 = car.Car(i+1)
            child2.net.load_parameters(c.cars[first_parent].net.crossbreed(c.cars[second_parent].net))

            newCars.append(child1)
            newCars.append(child2)

        for i in range(c.POP_SIZE - 13):
            newCars.append(car.Car(13 + i))
        
        for elem in newCars:
            #elem is a car, but "car is already taken by the module car :("
            rand = random.uniform(0, 1000)
            if(rand > 900):
                elem.net.mutate()

        for i in range(3):
            newCar = car.Car(10 + i)
            newCar.net = c.cars[c.fittest_cars[i]].net
            newCars.append(newCar)

        c.cars = newCars
        c.generation += 1
    
    def get_second_parent(self, first_parent, fittest_cars):
        second_parent = random.choice(fittest_cars)
        if(second_parent == first_parent):
            second_parent = self.get_second_parent(first_parent, fittest_cars)

        return second_parent


