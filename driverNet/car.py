import config as c
import pygame as pg
from basetypes import Vector2
from utils import get_line_intersection
import math

class Car():
    def __init__(self, pos, rot):
        self.rot = 0
        self.pos = pos
        self.vel = 5
        self.direction = Vector2(1, 0)

        self.image_orig = pg.Surface((c.CAR_W + 1, c.CAR_H + 1))  
        self.image_orig.set_colorkey(c.BLACK)
        pg.draw.rect(self.image_orig, c.GREEN, (0, 0, c.CAR_W, c.CAR_H), 2)
        
        self.rect = self.image_orig.get_rect()

        self.sensors = [Sensor(90 - i*45) for i in range(0, 5)]
        self.sensor_origin = Vector2()

    def update(self):
        self.move()
        self.rotate(2)
        self.updateSensors()

    def updateSensors(self):
        self.sensor_origin = self.pos + self.direction * c.CAR_H

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

    def getWallIntersection(self, walls, sensor_end):
        for i, point in enumerate(walls):
            if i != len(walls) - 1:
                wall_p1 = Vector2(*point)
                wall_p2 = Vector2(*walls[i+1])

                intersection = get_line_intersection(self.sensor_origin, sensor_end, wall_p1, wall_p2)
                
                if(intersection):
                    return intersection
        
        return None

    def move(self):
        self.pos += self.direction * self.vel
        
    def rotate(self, angle):
        self.rot = (self.rot + angle) % 360
        self.direction.rotate(angle)

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


        
