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
        c.fittest_cars = [None] * 8

    def check_simulation_state(self):
        if(c.crashed_cars == c.POP_SIZE or 
           c.keys[pg.K_RETURN]):
            self.create_next_generation()
            self.reset_simulation()

    def create_next_generation(self):
        newCars = []

        for i in range(8):
            max_score = 0
            for elem in c.cars:
                score = elem.checkpoint_count
                if(score > max_score and elem.index not in c.fittest_cars):
                    max_score = score
                    c.fittest_cars[i] = elem.index

        fittest_cars = []
        fittest_cars += [c.fittest_cars[0]] * 40
        fittest_cars += [c.fittest_cars[1]] * 20
        fittest_cars += [c.fittest_cars[2]] * 10
        fittest_cars += [c.fittest_cars[3]] * 10
        fittest_cars += [c.fittest_cars[4]] * 10
        fittest_cars += [c.fittest_cars[5]] * 10
        fittest_cars += [c.fittest_cars[6]] * 10
        fittest_cars += [c.fittest_cars[7]] * 10

            
        for i in range(8):
            first_parent = random.choice(fittest_cars)
            second_parent = self.get_second_parent(first_parent, fittest_cars)

            child1 = car.Car(len(newCars))
            child1.net.load_params(c.cars[first_parent].net.crossbreed(c.cars[second_parent].net))
            
            child2 = car.Car(len(newCars) + 1)
            child2.net.load_params(c.cars[first_parent].net.crossbreed(c.cars[second_parent].net))

            newCars.append(child1)
            newCars.append(child2)

        for elem in newCars:
            #elem is a car, but "car is already taken by the module car :("
            rand = random.randint(0, 100)
            if(random.randint(0, 100) > 96):
                elem.net.mutate()

        for i in range(c.POP_SIZE - len(newCars) - 5):
            newCars.append(car.Car(len(newCars)))

        for i in range(5):
            newCar = car.Car(len(newCars))
            newCar.net = c.cars[c.fittest_cars[i]].net
            newCars.append(newCar)

        c.cars = newCars
        c.generation += 1
    
    def get_second_parent(self, first_parent, fittest_cars):
        second_parent = random.choice(fittest_cars)
        while True:
            if(second_parent == first_parent):
                second_parent = random.choice(fittest_cars)
            else:
                break

        return second_parent


