import random
import sys
import os

import pygame
from pygame.locals import *

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


class MouseButtons:
    LEFT = 1
    MIDDLE = 2
    RIGHT = 3
    WHEEL_UP = 4
    WHEEL_DOWN = 5


# settings
block_dimsions = (45, 45) # visual block size
board_dimensions = (10, 20) # num of blocks - do not change
window_title = "Toastris"
framerate = 60
font_name = "Comic Sans MS"
game_icon = "toast.png"

# initialisation
window_size = (block_dimsions[0] * board_dimensions[0], block_dimsions[1] * board_dimensions[1])
window_width, window_height = window_size
os.environ["SDL_VIDEO_CENTERED"] = '1'
pygame.font.init()
pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption(window_title)
pygame.display.set_icon(pygame.image.load(game_icon))
clock = pygame.time.Clock()
title_font = pygame.font.SysFont(font_name, 22)
text_font = pygame.font.SysFont(font_name, 18)

# sprites
sprite_test = pygame.image.load('sprites/sprite_test.png').convert_alpha()

class Block(pygame.sprite.Sprite):
    locked = False

    def __init__(self, image, pos, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.pos = pos

    def update(self, *args):
        if self.locked:
            return
        if self.pos[1] == window_height - block_dimsions[1]:
            self.locked = True
            return
        self.pos[1] += 1
        print(self.pos[1])

    def blit(self, surface):
        surface.blit(self.image, self.pos)


# game state
ended = False
score = 0

# game objects
game_elements = [
    Block(sprite_test, [50, 50])
]

# main loop
while True:
    # events
    events = pygame.event.get()
    for event in events:
        # quit
        if event.type == QUIT:
            sys.exit(0)
        # TODO: keyboard

    if not ended:
        # background
        screen.fill((0, 0, 0, 1))

        # game elements
        for el in game_elements:
            el.update(events)
            el.blit(screen)

        # debug info
        debug_info = text_font.render(f"FPS: {int(clock.get_fps())} | SCORE: {score}", True, pygame.Color('white'))
        screen.blit(debug_info, (50, 50))
    else:
        # game over
        game_over = title_font.render("GAME OVER", True, pygame.Color('white'))
        score = title_font.render(f"SCORE: {score}", True, pygame.Color('white'))
        screen.fill((0, 0, 0, 1))
        screen.blit(game_over, (50, 50))
        screen.blit(score, (50, 75))

    # show
    pygame.display.flip()
    clock.tick(framerate)
