import pymunk
from pymunk.pygame_util import *
from pymunk.vec2d import Vec2d
import math
import pygame
from pygame.locals import *
from math import copysign 

import math
import random
from PIL import Image

space = pymunk.Space()

b0 = space.static_body
size = w, h = 700, 300

GRAY = (220, 220, 220)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

FPS=30
clock = pygame.time.Clock()
step=0
animation=[]
for i in range(6):
    image=pygame.image.load('ant_animation/4a4362189f264120b360f1257cb2d325Ue5dU1aOqg3mu2U0-{step_}.png'.format(step_=i))
    image=pygame.transform.scale(image,(83,75))
    animation.append(image)

#Boundaries
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
    def __init__(self, pos):
        self.step=0

        size = (60,40)
        mass = 1
        moment = pymunk.moment_for_box(mass, size)
        self.body = pymunk.Body(mass, moment)
        self.body.position = pos
        self.shape = pymunk.Poly.create_box(self.body, size)
        # self.shape.friction = 0.3
        self.shape.elasticity = 0.99
        space.add(self.body, self.shape)
        
    def draw(self,screen):
        mpos = pygame.mouse.get_pos()
        mouse_pos = pymunk.pygame_util.from_pygame(Vec2d(*mpos), screen)
        mouse_delta = mouse_pos - self.body.position
        turn = self.body.rotation_vector.cpvunrotate(mouse_delta).angle
        self.body.angle = self.body.angle-turn#copysign(1, turn)*.002

        if (mouse_pos - self.body.position).get_length_sqrd() < 10 ** 2:
            self.body.velocity = 0, 0
            self.step+=.2
        else:
            dv = Vec2d(20*(math.cos(turn)**2+3), 0.0) # slowdown when turn body
            self.body.velocity = self.body.rotation_vector.cpvrotate(dv)
            self.step+=1

        x, y = int(self.body.position[0]), int(self.body.position[1])
        rotated_image = pygame.transform.rotate(animation[int(self.step//2%6)], -self.body.angle/math.pi*180+90)
        rotated_rec = rotated_image.get_rect(center = rotated_image.get_rect(center = (x,y)).center)
        screen.blit(rotated_image,rotated_rec)

class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.draw_options = DrawOptions(self.screen)
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.do_event(event)
            self.draw()
        pygame.quit()

    def do_event(self, event):
        if event.type == QUIT:
            self.running = False
        elif event.type == KEYDOWN:
            if event.key in (K_q, K_ESCAPE):
                self.running = False
        elif event.type == MOUSEBUTTONDOWN:
            ants.append(Ant(pygame.mouse.get_pos()))

    def draw(self):
        self.screen.fill(GRAY)
        for ant in ants:
            ant.draw(self.screen)
        pygame.display.update()
        clock.tick(FPS)
        space.step(1/FPS)

if __name__ == '__main__':
    Box()
    r = 20
    position = random.randint(r, w-r),random.randint(r, h-r)
    ants=[]
    ants.append(Ant(position))
    App().run()