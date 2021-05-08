import pymunk
from pymunk.pygame_util import *
from pymunk.vec2d import Vec2d
import math
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

image=pygame.image.load('ant.png')
# image=pygame.transform.scale(image,(50,50))

class Segment:
    def __init__(self, p0, v, radius=10):
        self.body = pymunk.Body()
        self.body.position = p0
        shape = pymunk.Segment(self.body, (0, 0), v, radius)
        shape.density = 0.1
        shape.elasticity = 0.5
        shape.filter = pymunk.ShapeFilter(group=1)
        shape.color = (0, 255, 0, 0)
        space.add(self.body, shape)

class Box:
    def __init__(self, p0=(0, 0), p1=(w, h), d=4):
        x0, y0 = p0
        x1, y1 = p1
        ps = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        for i in range(4):
            segment = pymunk.Segment(b0, ps[i], ps[(i+1) % 4], d)
            segment.elasticity = 1
            segment.friction = 1
            space.add(segment)

class Ant:
    def __init__(self, pos, radius=20):
        size = (50,50)
        mass = 10.0
        moment = pymunk.moment_for_box(mass, size)
        self.body = pymunk.Body(mass, moment)
        self.body.position = pos
        self.shape = pymunk.Poly.create_box(self.body, size)
        # shape.friction = 0.3
        space.add(self.body, self.shape)
        # self.body = pymunk.Body(mass=1, moment=1000)
        
        # self.body.position = pos
        self.body.apply_impulse_at_local_point((500, 0), (0, 5))

        # self.shape = pymunk.Segment(self.body, (-50, 0), (50, 0),radius)
        self.shape.elasticity = 0.999
        # space.add(self.body, self.shape)
        # print(self.body.position)

class App:
    def __init__(self):
        pygame.init()
        self.i=0
        self.screen = pygame.display.set_mode(size)
        self.draw_options = DrawOptions(self.screen)
        self.active_shape = None
        self.selected_shapes = []
        self.pulling = False
        self.running = True
        self.gravity = False
        self.images = []
        self.FPS=300

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.do_event(event)
            self.draw()
            space.step(1/self.FPS)

        pygame.quit()

    def do_event(self, event):
        if event.type == QUIT:
            self.running = False
        elif event.type == KEYDOWN:
            if event.key in (K_q, K_ESCAPE):
                self.running = False


    def draw(self):
        def cal_angle(shape):
            x=shape.a[0]-shape.b[0]
            y=shape.a[1]-shape.b[1]
            return math.atan(y/x)
        self.screen.fill(GRAY)
        space.debug_draw(self.draw_options)
        # print(ant.body.angle)
        # ant.shape.update()
        self.i+=1
        rotated_image = pygame.transform.rotate(image, -ant.body.angle/math.pi*180)
        # rotated_image = pygame.transform.rotate(image, 20)
        # pygame.draw.circle(self.screen,(255,255,0),(int(ant.body.position[0]),int(ant.body.position[1])),2)
        # rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)
        x,y=(int(ant.body.position[0]),int(ant.body.position[1]))
        rotated_rec = rotated_image.get_rect(center = rotated_image.get_rect(center = (x,y)).center)
        self.screen.blit(rotated_image,rotated_rec)
        pygame.display.update()
        
    def draw_bb(self, shape):
        pos = shape.bb.left, shape.bb.top
        w = shape.bb.right - shape.bb.left
        h = shape.bb.top - shape.bb.bottom
        p = to_pygame(pos, self.screen)
        pygame.draw.rect(self.screen, BLUE, (*p, w, h), 1)

if __name__ == '__main__':
    Box()

    r = 20
    x = random.randint(r, w-r)
    y = random.randint(r, h-r)
    ant=Ant((x, y),r)
    App().run()