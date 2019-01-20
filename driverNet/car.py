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
        self.rot_speed = None
        self.direction = Vector2(0, 1)

        self.image_orig = pg.Surface((c.CAR_W + 1, c.CAR_H + 1))  
        self.image_orig.set_colorkey(c.BLACK)    
        pg.draw.rect(self.image_orig, c.GREEN, (0, 0, c.CAR_W, c.CAR_H), 2)
        
        image = self.image_orig.copy()  
        image.set_colorkey(c.BLACK)  
        self.rect = image.get_rect()
        self.rotate(-90)

        self.sensor_directions = [None for i in range(0, 5)]
        self.sensor_ends = [None for i in range(0, 5)]
        self.sensor_origin = Vector2()

    def update(self):
        self.move()
        self.rotate(2)
        self.updateSensors()

    def updateSensors(self):
        currAngle = 90
        for i in range(0, 5):
            self.sensor_directions[i] = self.direction.getRotated(currAngle)

            sensor_end = self.sensor_origin - self.sensor_directions[i] * c.SENSOR_RANGE
            self.sensor_ends[i] = self.getWallIntersection(c.outer_wall, sensor_end) 
            if(self.sensor_ends[i] == None):
                self.sensor_ends[i] = self.getWallIntersection(c.inner_wall, sensor_end)

            currAngle -= 45

    def getWallIntersection(self, walls, sensor_end):
        for i, point in enumerate(walls):
            if i != len(walls) - 1:
                wallP1 = Vector2(*point)
                wallP2 = Vector2(*walls[i+1])

                intersection = get_line_intersection(self.sensor_origin, sensor_end, wallP1, wallP2)
                if(intersection != None):
                    return intersection
        
        return None
    
    # def innerWallIntersection(self, sensor_end):
    #     pass
    #     intersections = []
    #     for intersection in intersections:
    #         distance = Vector2.distance(self.sensor_origin, intersection)
    #         if(minDistance == None):
    #             minDistance = distance
    #             minDistanceIntersection = intersection
    #         else:
    #             if(distance < minDistance):
    #                 minDistance = distance
    #                 minDistanceIntersection = intersection

    #     return minDistanceIntersection

    def move(self):
        self.pos -= self.direction * self.vel
        
    def rotate(self, angle):
        self.rot += angle
        self.rot %= 360
        self.direction.rotate(angle)

    def draw(self):
        old_center = (self.pos.x, self.pos.y)  
        new_image = pg.transform.rotate(self.image_orig , self.rot)  
        self.rect = new_image.get_rect()  
        self.rect.center = old_center    
        c.screen.blit(new_image , self.rect) 

        self.sensor_origin = Vector2(self.pos.x - self.direction.x * c.CAR_W,
                                     self.pos.y - self.direction.y * c.CAR_W)
        for i in range(0, 5):
            sensor_end = self.sensor_origin - self.sensor_directions[i] * c.SENSOR_RANGE
            
            if(self.sensor_ends[i] != None):
                x2 = self.sensor_ends[i].x
                y2 = self.sensor_ends[i].y
                pg.draw.circle(c.screen, c.GREEN, (int(x2), int(y2)), 5)
            else:
                x2 = sensor_end.x
                y2 = sensor_end.y

            pg.draw.line(c.screen, c.WHITE, (self.sensor_origin.x, self.sensor_origin.y), (x2, y2), 1)


        
