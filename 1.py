import pymunk
import pygame
import numpy as np


def create_boundary(space,width,height):
    coords={
        "left":[(0,0),(0,height)],
        "right":[(width,0),(width,height)],
        "top":[(0,height),(width,height)],
        "bot":[(0,0),(width,0)]
    }
    for coord in coords:
        body= pymunk.Body(body_type=pymunk.Body.STATIC)
        shape= pymunk.Segment(body,coords[coord][0],coords[coord][1],5)
        shape.density=.8
        space.add(body,shape)


def create_object(space,position):
    body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
    body.position = position
    shape = pymunk.Circle(body,10)
    shape.density=1
    shape.elasticity = 1-0
    space.add(body,shape)
    return body, shape

def create_map(width,height,n_width=8,n_height=6):
    r=30
    array_width=np.linspace(r, width-r, num=n_width)
    array_height=np.linspace(r, height-r, num=n_height)
    return [(int(a),int(b)) for a in array_width for b in array_height]



def draw_boundary(main_surface,width,height):
    pygame.draw.line(main_surface,(255,255,255),(0,0),(0,height),10)
    pygame.draw.line(main_surface,(255,255,255),(width,0),(width,height),10)
    pygame.draw.line(main_surface,(255,255,255),(0,height),(width,height),10)
    pygame.draw.line(main_surface,(255,255,255),(0,0),(width,0),10)

def draw_objects(main_surface,objects):
    for obj in objects:
        try:
            x,y=int(obj.body.position[0]),int(obj.body.position[1])
            pygame.draw.circle(main_surface,(255,255,255),(x,y),10)
        except:
            continue


def main():
    pygame.init()
    width, height = 800, 600
    n_width,n_height = 8,6
    main_surface = pygame.display.set_mode((width, height))
    clock=pygame.time.Clock()

    space=pymunk.Space()
    space.gravity= 3, 10

    create_boundary(space,width,height)


    objects=[]
    position_map = create_map(width,height,n_width,n_height)
    for position in position_map:
        body,shape=create_object(space,position)
        objects.append(shape)

    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:
            break
        main_surface.fill((0, 0, 0))
        draw_boundary(main_surface,width,height)
        draw_objects(main_surface, objects)
        space.step(1/60)
        pygame.display.update()
        

    pygame.quit()

if __name__=="__main__":
    
    main()