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
CAR_W = 40
CAR_H = 25
START_POS = (477, 825)
SENSOR_RANGE = 120

POP_SIZE = 16

max_checkpoint_count = 0
crashed_cars = 0
high_scores = [0] * 5
fittest_cars = [0, 1, 2, 3, 4]
generation = 0