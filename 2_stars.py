import pymunk
import pygame
import random
import sys
from pymunk.pygame_util import DrawOptions

width = 800
height = 600


class Ball:
    def __init__(self, position, space, radius=10):
        self.radius=radius
        self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        self.shape = pymunk.Circle(self.body,self.radius)

        d=20
        self.body.mass = d*radius**3*3.14*4/3#1
        self.shape.density=1
        self.shape.elasticity = 1
        self.shape.body.position = position
        space.add(self.shape, self.body)

    def apply_force(self, target):
        G=.3
        x=target.shape.body.position[0]-self.shape.body.position[0]
        y=target.shape.body.position[1]-self.shape.body.position[1]
        if x!=0 or y!=0:
            R=x**2+y**2
            f=G*self.body.mass*target.body.mass/R
            f_x=f*x
            f_y=f*y
            self.shape.body.apply_force_at_local_point((f_x, f_y), (0, 0))

class Box:
    def __init__(self,space, p0=(0, 0), p1=(width, height), d=4):
        x0, y0 = p0
        x1, y1 = p1
        ps = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        bodies=[]
        for i in range(4):
            bodies.append(pymunk.Body(body_type=pymunk.Body.STATIC))
            segment = pymunk.Segment(bodies[i], ps[i], ps[(i+1) % 4], d)
            segment.elasticity = 1
            segment.friction = 1
            space.add(bodies[i],segment)

def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("The ball drops")
    clock = pygame.time.Clock()
    
    draw_options = DrawOptions(screen)

    space = pymunk.Space()
    boundary = Box(space, (0, 0),(width, height))
    # space.gravity = 0, -100
    balls=[]
    n_balls=20
    for i in range(n_balls):
        balls.append(Ball((random.randint(20, 580), random.randint(20, 580)), space,radius=random.randint(1, 5)))
    balls.append(Ball((400,300), space,radius=20))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)

        """
        This is the code that applies force to the body of the drone
        """
        for i in range(n_balls+1):
            for j in range(n_balls+1):
                balls[i].apply_force(balls[j])
        screen.fill((0, 0, 0))
        space.debug_draw(draw_options)
        space.step(1/60.0)
        pygame.display.update()
        # clock.tick(5)


if __name__ == '__main__':
    sys.exit(main())