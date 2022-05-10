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
block_dimsions = (40, 40) # visual block size
board_dimensions = (10, 20) # num of blocks - do not change
window_title = "Toastris"
framerate = 60
tick_length = 30
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
_0_0_toast_4x = pygame.image.load('sprites/0_0_toast_4x.png').convert_alpha()
_0_0_toast_4xs = pygame.image.load('sprites/0_0_toast_4xs.png').convert_alpha()
_0_1_toast_4x = pygame.image.load('sprites/0_1_toast_4x.png').convert_alpha()
_0_2_toast_4x = pygame.image.load('sprites/0_2_toast_4x.png').convert_alpha()
_0_3_toast_4x = pygame.image.load('sprites/0_3_toast_4x.png').convert_alpha()

_0_0_toast_4x = pygame.transform.scale(_0_0_toast_4x, block_dimsions)
_0_0_toast_4xs = pygame.transform.scale(_0_0_toast_4xs, block_dimsions)
_0_1_toast_4x = pygame.transform.scale(_0_1_toast_4x, block_dimsions)
_0_2_toast_4x = pygame.transform.scale(_0_2_toast_4x, block_dimsions)
_0_3_toast_4x = pygame.transform.scale(_0_3_toast_4x, block_dimsions)


class Block:
    locked = False
    accelerated = False
    update_itr = 0
    rotation = 0

    def __init__(self, block_type, pos, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.block_type = block_type
        self.pos = pos

        if block_type == BlockTypes.Line:
            self.pieces = [
                BlockPiece(_0_0_toast_4x, [pos[0], pos[1] + 0*block_dimsions[0]]),
                BlockPiece(_0_1_toast_4x, [pos[0], pos[1] + 1*block_dimsions[0]]),
                BlockPiece(_0_2_toast_4x, [pos[0], pos[1] + 2*block_dimsions[0]]),
                BlockPiece(_0_3_toast_4x, [pos[0], pos[1] + 3*block_dimsions[0]]),
            ]

    def update(self, *args):
        if self.locked:
            return

        # update game tick
        self.update_itr += 1

        # move down by one on game tick
        if (self.accelerated and self.update_itr % int(tick_length/4) == 0) or self.update_itr % tick_length == 0:
            self.pos[1] += block_dimsions[1]

            # stop at bottom
            if self.pos[1] == window_height - block_dimsions[1]*4:
                self.locked = True

        # update pieces
        if self.rotation == 0:
            self.pieces[0].image = _0_0_toast_4x
            self.pieces[0].pos = [self.pos[0], self.pos[1] + 0*block_dimsions[0]]
            self.pieces[1].pos = [self.pos[0], self.pos[1] + 1*block_dimsions[0]]
            self.pieces[2].pos = [self.pos[0], self.pos[1] + 2*block_dimsions[0]]
            self.pieces[3].pos = [self.pos[0], self.pos[1] + 3*block_dimsions[0]]
            self.pieces[0].img_rot = 0
            self.pieces[1].img_rot = 0
            self.pieces[2].img_rot = 0
            self.pieces[3].img_rot = 0
            pass
        elif self.rotation == 1:
            self.pieces[0].image = _0_0_toast_4x
            self.pieces[0].pos = [self.pos[0] + 0*block_dimsions[0], self.pos[1]]
            self.pieces[1].pos = [self.pos[0] + 1*block_dimsions[0], self.pos[1]]
            self.pieces[2].pos = [self.pos[0] + 2*block_dimsions[0], self.pos[1]]
            self.pieces[3].pos = [self.pos[0] + 3*block_dimsions[0], self.pos[1]]
            self.pieces[0].img_rot = 90
            self.pieces[1].img_rot = 90
            self.pieces[2].img_rot = 90
            self.pieces[3].img_rot = 90
            pass
        elif self.rotation == 2:
            self.pieces[0].image = _0_0_toast_4xs
            self.pieces[3].pos = [self.pos[0], self.pos[1] + 0*block_dimsions[0]]
            self.pieces[2].pos = [self.pos[0], self.pos[1] + 1*block_dimsions[0]]
            self.pieces[1].pos = [self.pos[0], self.pos[1] + 2*block_dimsions[0]]
            self.pieces[0].pos = [self.pos[0], self.pos[1] + 3*block_dimsions[0]]
            self.pieces[0].img_rot = 180
            self.pieces[1].img_rot = 180
            self.pieces[2].img_rot = 180
            self.pieces[3].img_rot = 180
            pass
        elif self.rotation == 3:
            self.pieces[0].image = _0_0_toast_4x
            self.pieces[3].pos = [self.pos[0] + 0*block_dimsions[0], self.pos[1]]
            self.pieces[2].pos = [self.pos[0] + 1*block_dimsions[0], self.pos[1]]
            self.pieces[1].pos = [self.pos[0] + 2*block_dimsions[0], self.pos[1]]
            self.pieces[0].pos = [self.pos[0] + 3*block_dimsions[0], self.pos[1]]
            self.pieces[0].img_rot = 270
            self.pieces[1].img_rot = 270
            self.pieces[2].img_rot = 270
            self.pieces[3].img_rot = 270
            pass


    def blit(self, surface):
        for piece in self.pieces:
            piece.blit(surface)

class BlockPiece(pygame.sprite.Sprite):
    locked = False
    update_itr = 0
    accelerated = False
    img_rot = 0

    def __init__(self, image, pos, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.pos = pos

    def update(self, *args):
        pass

    def blit(self, surface):
        surface.blit(pygame.transform.rotate(self.image, self.img_rot), self.pos)

class BlockTypes:
    Line = 0
    Square = 1

# game state
ended = False
paused = False
score = 0

# game objects
game_elements = [
    # Block(sprite_test, [50, 50])
    Block(BlockTypes.Line, [1*block_dimsions[0], 3*block_dimsions[0]])
]

selected_game_element_idxs = [0]

# main loop
while True:
    # events
    events = pygame.event.get()
    for event in events:
        # quit
        if event.type == QUIT:
            sys.exit(0)

        # keyboard down
        elif event.type == 2:
            # space bar - pause
            if event.key == 32:
                paused = not paused

            # left - move left
            elif event.key == 276:
                for idx in selected_game_element_idxs:
                    game_elements[idx].pos[0] -= block_dimsions[0]

            # up - rotate
            elif event.key == 273:
                for idx in selected_game_element_idxs:
                    game_elements[idx].rotation = (game_elements[idx].rotation + 1) % 4

            # right - move right
            elif event.key == 275:
                for idx in selected_game_element_idxs:
                    game_elements[idx].pos[0] += block_dimsions[0]

            # down - accelerate fall
            elif event.key == 274:
                for idx in selected_game_element_idxs:
                    game_elements[idx].accelerated = True

            else:
                print("key:", event.key)

        # keyboard up
        elif event.type == 3:
            # down - stop accelerate fall
            if event.key == 274:
                for idx in selected_game_element_idxs:
                    game_elements[idx].accelerated = False
        else:
            pass
            # print(event.type)

    if not ended:
        # background
        screen.fill((0, 0, 0, 1))

        # lines
        line_color = (80, 80, 80, 80)
        for y in range(block_dimsions[1], window_height, block_dimsions[1]):
            pygame.draw.line(screen, line_color, (0, y), (window_width, y), 1)
        for x in range(block_dimsions[0], window_width, block_dimsions[0]):
            pygame.draw.line(screen, line_color, (x, 0), (x, window_height), 1)

        # game elements
        for el in game_elements:
            if not paused:
                el.update(events)
            el.blit(screen)

        # debug info
        debug_info_txt = f"FPS: {int(clock.get_fps())} | SCORE: {score}{' | PAUSED' if paused else ''}"
        debug_info = text_font.render(debug_info_txt, True, pygame.Color('white'))
        screen.blit(debug_info, (10, 10))
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
