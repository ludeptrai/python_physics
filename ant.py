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
image=pygame.transform.scale(image,(40,60))
pointer_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
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
        size = (60,40)
        mass = 1.0
        moment = pymunk.moment_for_box(mass, size)
        self.body = pymunk.Body(mass, moment)
        self.body.position = pos
        self.shape = pymunk.Poly.create_box(self.body, size)
        self.shape.friction = 0.3
        
        # rest_angle = math.pi
        # stiffness = 1000
        # damping = 1000.0

        # rotary_spring = pymunk.constraints.DampedRotarySpring(
        # pointer_body, self.body, rest_angle, stiffness, damping
        # )
        # force_spring=pymunk.constraints.DampedSpring(
        #     pointer_body, self.body, pointer_body.position, (30,0), 0, stiffness, damping
        # )
        space.add(self.body, self.shape)
        # self.body = pymunk.Body(mass=1, moment=1000)
        
        # self.body.position = pos
        # self.body.apply_impulse_at_local_point((50, 50), (30, 0))

        # self.shape = pymunk.Segment(self.body, (-50, 0), (50, 0),radius)
        self.shape.elasticity = 0.999
        # space.add(self.body, self.shape)
        # print(self.body.position)

class App:
    def __init__(self):
        pygame.init()
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
        # elif event.type == pygame.MOUSEMOTION:
        #         mouse_pos = pymunk.pygame_util.get_mouse_pos(self.screen)
        #         pointer_body.position = mouse_pos
        #         pointer_body.angle = (pointer_body.position - ant.body.position).angle
                # print(pointer_body.angle)

    def update(self):

        # if (mouse_pos - tank_body.position).get_length_sqrd() < 30 ** 2:
        #     tank_control_body.velocity = 0, 0
        # else:
        # if mouse_delta.dot(tank_body.rotation_vector) > 0.0:
        #     direction = 1.0
        # else:
        #     direction = -1.0
        # dv = Vec2d(30.0 * direction, 0.0)
        # ant.body.velocity = ant.body.rotation_vector.cpvrotate(dv)
        # angle = (pointer_body - tank_body.position).angle
        mpos = pygame.mouse.get_pos()
        mouse_pos = pymunk.pygame_util.from_pygame(Vec2d(*mpos), self.screen)
        mouse_delta = mouse_pos - ant.body.position
        turn = ant.body.rotation_vector.cpvunrotate(mouse_delta).angle
        ant.body.angle=ant.body.angle-turn
        dv = Vec2d(30.0, 0.0)
        ant.body.velocity = ant.body.rotation_vector.cpvrotate(dv)

    def draw(self):
        self.screen.fill(GRAY)
        space.debug_draw(self.draw_options)
        rotated_image = pygame.transform.rotate(image, -ant.body.angle/math.pi*180-90)
        # rotated_image = pygame.transform.rotate(image, 20)
        # pygame.draw.circle(self.screen,(255,255,0),(int(ant.body.position[0]),int(ant.body.position[1])),2)
        # rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)
        self.update()
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