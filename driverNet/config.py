from basetypes import Vector2
import json

track_data = None
with open('track.json') as data_file:    
    track_data = json.load(data_file)

inner_wall = track_data["innerWall"]
outer_wall = track_data["outerWall"]
checkpoints = track_data["checkpoints"]

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

screen = None
clock = None 
delta_time = 0

SCREEN_SIZE = Vector2(1000, 1000)
CAR_W = 45
CAR_H = 25
START_POS = (477, 825)
SENSOR_RANGE = 150

POP_SIZE = 30

max_checkpoint_count = 0
crashed_cars = 0
fittest_cars = [None] * 8
generation = 0
best_of_generation = None