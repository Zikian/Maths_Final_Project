from basetypes import Vector2
import json

track_data = None
with open('track.json') as data_file:    
    track_data = json.load(data_file)

inner_wall = track_data["innerWall"]
outer_wall = track_data["outerWall"]

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

screen = None
clock = None 

delta_time = 0

SCREEN_SIZE = Vector2(1000, 1000)
CAR_W = 25
CAR_H = 40
START_POS = (477, 825)
SENSOR_RANGE = 100