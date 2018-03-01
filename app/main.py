from __future__ import print_function

import bottle
import os
import math
import copy
import random


SNEK_BUFFER = 3
ID = 'de508402-17c8-4ac7-ab0b-f96cb53fbee8'
SNAKE = 100
ENESNAKE = 10
FOOD = -100
SAFTEY = -1

def eval(location, grid):
    value = 50

    #if out of grid
    if location[0] < 0 or location[1] < 0 or location[0] >= len(grid) or location[1] >= len(grid[0]):
        return value + 1000

    #Add value of grid
    value += grid[location[0]][location[1]]

    return value


def chooseDirect(head, grid):
    #up
    location = [head[0], head[1]-1]
    up = eval(location, grid)
    #down
    location = [head[0], head[1]+1]
    down = eval(location, grid)
    #left
    location = [head[0]-1, head[1]]
    left = eval(location, grid)
    #right
    location = [head[0]+1, head[1]]
    right = eval(location, grid)

    print('Directions: [head: (%i,%i), up: (%i,%i), down: (%i,%i), left: (%i,%i), right: (%i,%i)]' % (head[0], head[1], head[0], head[1]+1, head[0], head[1]-1, head[0]-1, head[1], head[0]+1, head[1]))
    print ('Values: [up: %i, down: %i, left: %i, right: %i]' % (up, down, left, right))


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

def distanceV(p, q):
    dx = abs(p[0] - q[0])
    dy = abs(p[1] - q[1])
    return [dx, dy];

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
    for snek in data['snakes']['data']:
        if snek['id'] == ID:
            mysnake = snek
        for coord in snek['body']['data']:
            grid[coord['x']][coord['y']] += SNAKE
            if coord == snek['body']['data'][0]:
                if coord['y']+1 < data['height']:
                    grid[coord['x']][coord['y']+1] += ENESNAKE
                if coord['y']-1 >= 0:
                    grid[coord['x']][coord['y']-1] += ENESNAKE
                if coord['x']+1 < data['width']:
                    grid[coord['x']+1][coord['y']] += ENESNAKE
                if coord['x']-1 < 0:
                    grid[coord['x']-1][coord['y']] += ENESNAKE


    for f in data['food']['data']:
        grid[f['x']][f['y']] += FOOD-mysnake['health']

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

    head = [snek['body']['data'][0]['x'], snek['body']['data'][0]['y']]

    '''
    # foreach snake
    for enemy in data['snakes']['data']:
        if (enemy['id'] == ID):
            continue
        print('hallo')
        dist = distance(head, [enemy['body']['data'][0]['x'], enemy['body']['data'][0]['y']])
        if dist > SNEK_BUFFER:
            continue
        #if (len(enemy['coords']) > len(snek['coords']) - 1):
        # dodge
        if enemy['body']['data'][0]['y'] < data['height'] - 1:
            grid[enemy['body']['data'][0]['x']][enemy['body']['data'][0]['y'] + 1] += SAFTEY
        if enemy['body']['data'][0]['y'] > 0:
            grid[enemy['body']['data'][0]['x']][enemy['body']['data'][0]['y'] - 1] += SAFTEY

        if enemy['body']['data'][0]['x'] < data['width'] - 1:
            grid[enemy['body']['data'][0]['x'] + 1][enemy['body']['data'][0]['y']] += SAFTEY
        if enemy['coords'][0][0] > 0:
            grid[enemy['body']['data'][0]['x'] - 1][enemy['body']['data'][0]['y']] += SAFTEY
        '''

    #for each food
    for food in data['food']['data']:
        if head[1]+1 < height:
            dist1 = distance([head[0], head[1]+1], [food['x'], food['y']])
            grid[head[0]][head[1]+1] += dist1
        if head[1]-1 >= 0:
            dist2 = distance([head[0], head[1]-1], [food['x'], food['y']])
            grid[head[0]][head[1]-1] += dist2
        if head[0]+1 < width:
            dist3 = distance([head[0]+1, head[1]], [food['x'], food['y']])
            grid[head[0]+1][head[1]] += dist3
        if head[0]-1 >= 0:
            dist4 = distance([head[0]-1, head[1]], [food['x'], food['y']])
            grid[head[0]-1][head[1]] += dist4




    # TODO: Do things with data
    directions = ['up', 'down', 'left', 'right']


    return {
        'move': chooseDirect(head, grid),
        #'move': 'left',
        'taunt': 'battlesnake-python!'
    }



# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '127.0.0.1'), port=os.getenv('PORT', '8080'))
