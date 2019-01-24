import math
import config as c
import pygame as pg
from basetypes import Vector2
from utils import get_line_intersection, clamp
import neural_net

class Car():
    def __init__(self, index):
        self.index = index
        self.rot = 0
        self.steer_angle = 0
        self.pos = Vector2(*c.START_POS)
        self.vel = 2
        self.acceleration = 0
        self.direction = Vector2(1, 0)

        self.time_stuck = 0

        self.image_orig = pg.Surface((c.CAR_W, c.CAR_H))  
        self.image_orig.set_colorkey(c.BLACK)
        pg.draw.rect(self.image_orig, c.GREEN, (0, 0, c.CAR_W, c.CAR_H), 1)
        self.rect = self.image_orig.get_rect()

        self.wheel_image = pg.Surface((12, 3))  
        self.wheel_image.set_colorkey(c.BLACK)
        pg.draw.rect(self.wheel_image, c.WHITE, (0, 0, 12, 3), 0)
        self.wheel_rect = self.wheel_image.get_rect()

        self.sensors = [Sensor(90 - i*45) for i in range(0, 5)]
        self.sensor_origin = Vector2()
        self.update_sensors()

        self.net = neural_net.NeuralNet(2)

        self.collided = False
        self.checkpoint_count = 1
        self.prev_checkpoint_count = 1

        self.time_since_last_checkpoint = 0
        self.total_time = 1

        self.front_left = Vector2()
        self.front_right = Vector2()
        self.back_left = Vector2()
        self.front_left = Vector2()

    def update(self):
        if(not self.collided):
            inputs = [self.sensors[i].length for i in range(5)]
            outputs = self.net.forward_propagation(inputs)

            #self.accelerate(outputs[0])
            self.move()
            self.steer(outputs[1])
            self.rotate()
            self.update_sensors()
            self.update_corner_positions()
            self.checkpoint_collisions()
            self.collided = self.check_collisions()
            self.check_if_stuck()
            if(self.collided):
                c.crashed_cars += 1


    def accelerate(self, delta_accel):
        if(delta_accel < 0.5):
            delta_accel *= -1

        self.acceleration += delta_accel
        self.vel = clamp(2, 4, self.vel + self.acceleration)

    def move(self):
        self.pos += self.direction * self.vel

    def steer(self, factor):
        if(factor < 0.5):
            factor *= -1
        self.steer_angle = clamp(-45, 45, self.steer_angle + factor * 9)
        
    def rotate(self):
        angle = self.steer_angle * self.vel / 25;
        self.rot = (self.rot + angle) % 360
        self.direction.rotate(angle)

    def check_if_stuck(self):
        if(self.prev_checkpoint_count == self.checkpoint_count):
            self.time_stuck += c.delta_time
        else:
            self.time_stuck = 0
        
        if(self.time_stuck > 2000):
            self.collided = True

        self.prev_checkpoint_count = self.checkpoint_count

    def update_corner_positions(self):
        direction_normal = self.direction.get_rotated(90)
        half_width = c.CAR_W / 2
        half_height = c.CAR_H / 2
        self.front_left = self.pos + self.direction * half_width + direction_normal * half_height
        self.front_right = self.pos + self.direction * half_width - direction_normal * half_height
        self.back_right = self.pos - self.direction * half_width - direction_normal * half_height
        self.back_left = self.pos - self.direction * half_width + direction_normal * half_height

    def update_sensors(self):
        self.sensor_origin = self.pos + self.direction * c.CAR_W / 2

        for sensor in self.sensors:
            sensor.direction = self.direction.get_rotated(sensor.angle)

            #End point of sensor if there is no collision
            sensor_end = self.sensor_origin + sensor.direction * c.SENSOR_RANGE

            sensor.end_point = self.getWallIntersection(sensor_end) 

            #No collision
            if(not sensor.end_point):
                sensor.end_point = sensor_end
                sensor.length = c.SENSOR_RANGE
            else:
                sensor.length = Vector2.distance(self.sensor_origin, sensor.end_point)

    def check_collisions(self):
        for i, point in enumerate(c.outer_wall):
            if i != len(c.outer_wall) - 1:
                wall_p1 = Vector2(*point)
                wall_p2 = Vector2(*c.outer_wall[i+1])
                if(self.wall_in_range(wall_p1, wall_p2, 50)):
                    if(self.is_colliding(wall_p1, wall_p2)):
                        return True

        for i, point in enumerate(c.inner_wall):
            if i != len(c.inner_wall) - 1:
                wall_p1 = Vector2(*point)
                wall_p2 = Vector2(*c.inner_wall[i+1])
                if(self.wall_in_range(wall_p1, wall_p2, 50)):
                    if(self.is_colliding(wall_p1, wall_p2)):
                        return True

        return False

    def wall_in_range(self, p1, p2, max_range):
        y_in_range = not (abs(p1.y - self.pos.y) > max_range and 
                          abs(p2.y - self.pos.y) > max_range and
                         (p1.y < self.pos.y and p2.y < self.pos.y or
                          p1.y > self.pos.y and p2.y > self.pos.y))

        x_in_range = not (abs(p1.x - self.pos.x) > max_range and 
                          abs(p2.x - self.pos.x) > max_range and
                         (p1.x < self.pos.x and p2.x < self.pos.x or
                          p1.x > self.pos.x and p2.x > self.pos.x))

        return y_in_range and x_in_range


    def is_colliding(self, p1, p2):
        return (get_line_intersection(self.front_left, self.front_right, p1, p2) or
                get_line_intersection(self.front_right, self.back_right, p1, p2) or
                get_line_intersection(self.back_right, self.back_left, p1, p2) or
                get_line_intersection(self.back_right, self.front_left, p1, p2))

    def checkpoint_collisions(self):
        if(self.checkpoint_count != len(c.checkpoints)):
            checkpoint = c.checkpoints[self.checkpoint_count]

            if(self.is_colliding(Vector2(*checkpoint[0]), Vector2(*checkpoint[1]))):
                self.checkpoint_count += 1
                if(self.checkpoint_count > c.max_checkpoint_count):
                    c.max_checkpoint_count = self.checkpoint_count
                    c.best_of_generation = self.index
                
                self.total_time += self.time_since_last_checkpoint
                self.time_since_last_checkpoint = 0
            else:
                self.time_since_last_checkpoint += c.delta_time

    def getWallIntersection(self, sensor_end):
        intersections = []
        walls = c.outer_wall

        for i, point in enumerate(walls):
            if i != len(walls) - 1:
                wall_p1 = Vector2(*point)
                wall_p2 = Vector2(*walls[i+1])

                if(not self.wall_in_range(wall_p1, wall_p2, c.SENSOR_RANGE + 5)):
                    continue

                intersection = get_line_intersection(self.sensor_origin, sensor_end, wall_p1, wall_p2)
                
                if(intersection):
                    intersections.append(intersection)

        walls = c.inner_wall
        for i, point in enumerate(walls):
            if i != len(walls) - 1:
                wall_p1 = Vector2(*point)
                wall_p2 = Vector2(*walls[i+1])

                intersection = get_line_intersection(self.sensor_origin, sensor_end, wall_p1, wall_p2)
                
                if(intersection):
                    intersections.append(intersection)
        
        if(len(intersections) == 0):
            return None
        else:
            minDistance = None
            minDistanceIntersection = None
            for intersection in intersections:

                distance = Vector2.sqr_distance(intersection, self.pos)
                if(minDistance == None or distance < minDistance):
                    minDistance = distance
                    minDistanceIntersection = intersection
            
            return minDistanceIntersection


    def draw(self):
        self.draw_car()

        if(self.index == c.best_of_generation and not self.collided):
            self.draw_sensors()

    def draw_car(self):
        new_image = pg.transform.rotate(self.image_orig , self.rot)  
        self.rect = new_image.get_rect()  
        self.rect.center = (self.pos.x, self.pos.y) 

        normal_dir = self.direction.get_rotated(90) * c.CAR_H / 2

        new_wheel_image = pg.transform.rotate(self.wheel_image , self.rot)  
        self.wheel_rect = new_wheel_image.get_rect()  
        
        wheel_pos = self.pos - self.direction * 20 + normal_dir
        self.wheel_rect.center = wheel_pos.get_tuple() 
        c.screen.blit(new_wheel_image , self.wheel_rect)

        wheel_pos = self.pos - self.direction * 20 - normal_dir   
        self.wheel_rect.center = wheel_pos.get_tuple() 
        c.screen.blit(new_wheel_image , self.wheel_rect)

        new_wheel_image = pg.transform.rotate(self.wheel_image , self.rot + self.steer_angle)  
        self.wheel_rect = new_wheel_image.get_rect()  
        
        wheel_pos = self.pos + self.direction * 20 + normal_dir
        self.wheel_rect.center = wheel_pos.get_tuple() 
        c.screen.blit(new_wheel_image , self.wheel_rect)

        wheel_pos = self.pos + self.direction * 20 - normal_dir
        self.wheel_rect.center = wheel_pos.get_tuple() 
        c.screen.blit(new_wheel_image , self.wheel_rect)

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


        
