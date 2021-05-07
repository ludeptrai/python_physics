import pymunk
import pygame
import numpy as np

def main():
    pygame.init()
    width, height = 800, 600
    main_surface = pygame.display.set_mode((width, height))
    clock=pygame.time.Clock()

    space=pymunk.Space()
    space.gravity= 0, 10
    position=(400,400)
    body = pymunk.Body()
    body.position = position
    shape = pymunk.Circle(body,10)
    shape.density=1
    space.add(body,shape)
    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:
            break
        main_surface.fill((0, 0, 0))
        # draw_objects(main_surface, objects)
        x,y=int(body.position[0]),int(body.position[1])
        space.step(1/60)
        pygame.draw.circle(main_surface,(255,255,255),(x,y),10)
        pygame.display.update()
    pygame.quit()

if __name__=="__main__":
    main()