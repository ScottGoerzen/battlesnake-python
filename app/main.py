import bottle
import os
import math
import copy
import random

SNEK_BUFFER = 3
ID = 'de508402-17c8-4ac7-ab0b-f96cb53fbee8'
SNAKE = 10
ENESNAKE = 10
FOOD = -100
SAFTEY = -1

def eval(location, grid):
    value = 50

    #if out of grid
    if location[0] < 0 or location[1] < 0 or location[0] >= len(grid) or location[1] >= len(grid[0]):
        return value + 100

    #Add value of grid
    value += grid[location[0]][location[1]]

    return value


def chooseDirect(head, grid):
    #up
    location = [head[0], head[1]+1]
    up = eval(location, grid)
    #down
    location = [head[0], head[1]-1]
    down = eval(location, grid)
    #left
    location = [head[0]-1, head[1]]
    left = eval(location, grid)
    #right
    location = [head[0]+1, head[1]]
    right = eval(location, grid)

    #find smallest value
    if up < down:
        if up < left:
            if up < right:
                return 'up'
            else:
                return 'right'
        else:
            if left < right:
                return 'left'
            else:
                return 'right'
    else:
        if down < left:
            if down < right:
                return 'down'
            else:
                return 'right'
        else:
            if left < right:
                return 'left'
            else:
                return 'right'

def distance(p, q):
    dx = abs(p[0] - q[0])
    dy = abs(p[1] - q[1])
    return dx + dy;

def closest(items, start):
    closest_item = None
    closest_distance = 10000

    # TODO: use builtin min for speed up
    for item in items:
        item_distance = distance(start, item)
        if item_distance < closest_distance:
            closest_item = item
            closest_distance = item_distance

    return closest_item

def init(data):
    grid = [[0 for col in xrange(data['height'])] for row in xrange(data['width'])]
    for snek in data['snakes']:
        print ('hi')
        if snek[0] == ID:
            mysnake = snek
        for coord in snek['coords']:
            grid[coord[0]][coord[1]] += SNAKE
            if coord == snek['coords'][0]:
                grid[coord[0]][coord[1]+1] += ENESNAKE
                grid[coord[0]][coord[1]-1] += ENESNAKE
                grid[coord[0]-1][coord[1]] += ENESNAKE
                grid[coord[0]+1][coord[1]] += ENESNAKE


    for f in data['food']:
        grid[f[0]][f[1]] += FOOD-mysnake['health']

    return mysnake, grid

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():

    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#00FF00',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url,
        'name': 'Bird Snake'
    }


@bottle.post('/move')
def move():
    global ID
    data = bottle.request.json
    height = data['height']
    width = data['width']
    ID = data['you']['id']


    snek, grid = init(data)

    head = snek['coords'][0]
    '''
    # foreach snake
    for enemy in data['snakes']:
        if (enemy['id'] == ID):
            continue
        dist = distance(['coords'][0], enemy['coords'][0])
        if dist > SNEK_BUFFER:
            continue
        #if (len(enemy['coords']) > len(snek['coords']) - 1):
        # dodge
        if enemy['coords'][0][1] < data['height'] - 1:
            grid[enemy['coords'][0][0]][enemy['coords'][0][1] + 1] += SAFTEY
        if enemy['coords'][0][1] > 0:
            grid[enemy['coords'][0][0]][enemy['coords'][0][1] - 1] += SAFTEY

        if enemy['coords'][0][0] < data['width'] - 1:
            grid[enemy['coords'][0][0] + 1][enemy['coords'][0][1]] += SAFTEY
        if enemy['coords'][0][0] > 0:
            grid[enemy['coords'][0][0] - 1][enemy['coords'][0][1]] += SAFTEY
    
    #for each food
    for food in data['food']:
        dist1 = distance([head[0]][head[1]+1], food)
        dist2 = distance([head[0]][head[1]-1], food)
        dist3 = distance([head[0]+1][head[1]], food)
        dist4 = distance([head[0]-1][head[1]], food)
        grid[head[0]][head[1]+1] -= max(width-dist1[0], height-dist1[1])
        grid[head[0]][head[1]-1] -= max(width-dist2[0], height-dist2[1])
        grid[head[0]+1][head[1]] -= max(width-dist3[0], height-dist3[1])
        grid[head[0]-1][head[1]] -= max(width-dist4[0], height-dist4[1])

    '''


    # TODO: Do things with data
    directions = ['up', 'down', 'left', 'right']

    return {
        #'move': chooseDirect(head, grid),
        'move': 'left',
        'taunt': 'battlesnake-python!'
    }



# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '127.0.0.1'), port=os.getenv('PORT', '8080'))
