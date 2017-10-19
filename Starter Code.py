#!/usr/bin/python
# Toadie
# Code Angel

import sys
import os
import pygame
from pygame.locals import *

import toad
import world
import scoreboard

# Define the colours
BLACK = (0, 0, 0)
DARK_BLUE = (0, 0, 121)

# Define constants
SCREEN_WIDTH = 448
SCREEN_HEIGHT = 512

# Setup
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()
game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Toadie')
pygame.key.set_repeat(500, 200)

clock = pygame.time.Clock()

large_font = pygame.font.SysFont('Helvetica', 24)
score_font = pygame.font.SysFont('Helvetica Bold', 24)