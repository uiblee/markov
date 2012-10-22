import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 8
GAME_HEIGHT = 8

#### Put class definitions here ####

class TallTree(GameElement):
    IMAGE = "TallTree"
    SOLID = True

class Cat(GameElement):
    def interact(self, player):
        GAME_BOARD.draw_msg("You saved the Cat! Congratulations, Princess!") 
    IMAGE = "Cat"
    SOLID = False

class DoorClosed(GameElement):
    IMAGE = "DoorClosed"
    SOLID = True

class DoorOpen(GameElement):
    IMAGE = "DoorOpen"
    SOLID = False

class Wall(GameElement):
    IMAGE = "Wall"
    SOLID = False

    def interact(self, player):
        
        GAME_BOARD.del_el(0, 0, player)
        GAME_BOARD.set_el(6, 2, player)

class Character(GameElement):
    IMAGE = "Princess"
    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []

    def next_pos(self, direction):
        if direction == "up":
            next = (self.x, self.y-1)
            return next
        elif direction == "down":
            next = (self.x, self.y+1)
            return next
        elif direction == "left":
            next = (self.x-1, self.y)
            return next
        elif direction == "right":
            next = (self.x+1, self.y)
            return next
                  
        return None

class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d item[s]!" % (len(player.inventory)))

        GAME_BOARD.del_el(6, 1)

        open_door = DoorOpen()
        GAME_BOARD.register(open_door)
        GAME_BOARD.set_el(6, 1, open_door)


####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    tree_positions = [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (1,2), (1,3), (1,7), 
                        (2,0), (2,2), (2,5), (2,6), (2,7), (3,0), (3,4), (3,5), (3,6), (3,7), (4,0), (4,1),
                        (4,2), (4,7), (5,0), (5,1), (5,2), (5,3), (5,4), (5,5), (5,7), (6,7), (7, 0),
                         (7, 1), (7, 2), (7, 3,), (7, 4), (7,5), (7, 6), (7,7), (1,1), (2,1), (3,1), (3,2)]
    trees = []
    
    for pos in tree_positions:
        tree = TallTree()
        GAME_BOARD.register(tree)
        GAME_BOARD.set_el(pos[0], pos[1], tree)
        trees.append(tree)

    trees[-1].SOLID = False
    trees[-2].SOLID = False
    trees[-3].SOLID = False
    trees[-4].SOLID = False

    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(0, 7, PLAYER)
    print PLAYER

    GAME_BOARD.draw_msg("This game is wicked awesome.")

    closed_door = DoorClosed()
    GAME_BOARD.register(closed_door)
    GAME_BOARD.set_el(6,1,closed_door)

    cat = Cat()
    GAME_BOARD.register(cat)
    GAME_BOARD.set_el(6,0,cat)

    gem = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(1,0,gem)

    wall = Wall()
    GAME_BOARD.register(wall)
    GAME_BOARD.set_el(0,0, wall)

def keyboard_handler():
    direction = None

    if KEYBOARD[key.UP]:
        direction = "up"
        
    if KEYBOARD[key.DOWN]:
        direction = "down"

    if KEYBOARD[key.RIGHT]:
        direction = "right"
        
    if KEYBOARD[key.LEFT]:
        direction = "left"

    if direction:
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

        if next_x >= GAME_WIDTH or next_x< 0 or next_y >= GAME_HEIGHT or next_y < 0:
            return None

        existing_el = GAME_BOARD.get_el(next_x, next_y)

        if existing_el:
            existing_el.interact(PLAYER)

        if existing_el is None or not existing_el.SOLID:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)
