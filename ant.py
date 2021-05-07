import pymunk
from pymunk.pygame_util import *
from pymunk.vec2d import Vec2d

import pygame
from pygame.locals import *

import math
import random
from PIL import Image

space = pymunk.Space()
b0 = space.static_body
size = w, h = 700, 300

GRAY = (220, 220, 220)
RED = (255, 0, 0)
BLUE = (0, 0, 255)