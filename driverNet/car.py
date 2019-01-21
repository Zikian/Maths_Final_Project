import math
import config as c
import pygame as pg
from basetypes import Vector2
from utils import get_line_intersection, clamp
import neural_net

class Car():
    def __init__(self, pos):
        self.rot = 0
        self.pos = pos
        self.vel = 1.5
        self.direction = Vector2(1, 0)

        self.image_orig = pg.Surface((c.CAR_W + 1, c.CAR_H + 1))  
        self.image_orig.set_colorkey(c.BLACK)
        pg.draw.rect(self.image_orig, c.GREEN, (0, 0, c.CAR_W, c.CAR_H), 2)
        
        self.rect = self.image_orig.get_rect()

        self.sensors = [Sensor(90 - i*45) for i in range(0, 5)]
        self.sensor_origin = Vector2()
        self.updateSensors()

        self.net = neural_net.NeuralNet(5, 5, 2)

        self.collided = False
        self.checkpoint_count = 0

    def update(self):
        if(not self.collided):
            inputs = [1 / self.sensors[i].length for i in range(5)]
            outputs = self.net.forward_propagation(inputs)

            self.accelerate(outputs[0] / 10)
            self.move()
            self.rotate(outputs[1])
            self.updateSensors()
        self.collided = self.checkCollisions()

    def accelerate(self, factor):
        self.vel = clamp(0, 3, self.vel + factor)

    def move(self):
        self.pos += self.direction * self.vel
        
    def rotate(self, angle):
        if(angle < 0.5):
            angle *= -1
        self.rot = (self.rot + angle) % 360
        self.direction.rotate(angle)

    def updateSensors(self):
        self.sensor_origin = self.pos + self.direction * c.CAR_W / 2

        for sensor in self.sensors:
            sensor.direction = self.direction.get_rotated(sensor.angle)

            #End point of sensor if there is no collision
            sensor_end = self.sensor_origin + sensor.direction * c.SENSOR_RANGE

            sensor.end_point = self.getWallIntersection(c.outer_wall, sensor_end) 
            if(not sensor.end_point):
                sensor.end_point = self.getWallIntersection(c.inner_wall, sensor_end)

            #No collision
            if(not sensor.end_point):
                sensor.end_point = sensor_end
                sensor.length = c.SENSOR_RANGE
            else:
                sensor.length = Vector2.distance(self.sensor_origin, sensor.end_point)

    def checkCollisions(self):
        direction_normal = self.direction.get_rotated(90)
        front_left = self.pos + self.direction * c.CAR_W / 2 + direction_normal * c.CAR_H / 2
        front_right = self.pos + self.direction * c.CAR_W / 2 - direction_normal * c.CAR_H / 2
        back_right = self.pos - self.direction * c.CAR_W / 2 - direction_normal * c.CAR_H / 2
        back_left = self.pos - self.direction * c.CAR_W / 2 + direction_normal * c.CAR_H / 2

        for i, point in enumerate(c.outer_wall):
            if i != len(c.outer_wall) - 1:
                wall_p1 = Vector2(*point)
                wall_p2 = Vector2(*c.outer_wall[i+1])

                if(get_line_intersection(front_left, front_right, wall_p1, wall_p2) or
                   get_line_intersection(front_right, back_right, wall_p1, wall_p2) or
                   get_line_intersection(back_right, back_left, wall_p1, wall_p2) or
                   get_line_intersection(back_right, front_left, wall_p1, wall_p2)):
                    return True 

        for i, point in enumerate(c.inner_wall):
            if i != len(c.inner_wall) - 1:
                wall_p1 = Vector2(*point)
                wall_p2 = Vector2(*c.inner_wall[i+1])

                if(get_line_intersection(front_left, front_right, wall_p1, wall_p2) or
                   get_line_intersection(front_right, back_right, wall_p1, wall_p2) or
                   get_line_intersection(back_right, back_left, wall_p1, wall_p2) or
                   get_line_intersection(back_right, front_left, wall_p1, wall_p2)):
                    return True 
               


    def getWallIntersection(self, walls, sensor_end):
        for i, point in enumerate(walls):
            if i != len(walls) - 1:
                wall_p1 = Vector2(*point)
                wall_p2 = Vector2(*walls[i+1])

                intersection = get_line_intersection(self.sensor_origin, sensor_end, wall_p1, wall_p2)
                
                if(intersection):
                    return intersection
        
        return None


    def draw(self):
        self.draw_car_rect() 
        self.draw_sensors()

    def draw_car_rect(self):
        new_image = pg.transform.rotate(self.image_orig , self.rot)  
        self.rect = new_image.get_rect()  
        self.rect.center = (self.pos.x, self.pos.y)     
        c.screen.blit(new_image , self.rect)

    def draw_sensors(self):
        for i in range(0, 5):
            x2 = self.sensors[i].end_point.x
            y2 = self.sensors[i].end_point.y
            pg.draw.circle(c.screen, c.GREEN, (int(x2), int(y2)), 5)
            pg.draw.line(c.screen, c.WHITE, (self.sensor_origin.x, self.sensor_origin.y), (x2, y2), 1)

class Sensor():
    def __init__(self, angle):
        self.angle = angle
        self.direction = Vector2()
        self.end_point = Vector2()
        self.length = None


        
