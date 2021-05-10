import numpy as np
import pygame, sys
from pygame.locals import *
class gameOfLife:
    def __init__(self,columns,rows):
        self.columns=columns
        self.rows=rows
        self.board=self.create_board()

    def create_board(self):
        # board=np.zeros((self.columns,self.rows))
        board=np.random.randint(0,10,size=(self.columns,self.rows))>8
        return board+0

    def update_board(self):
        new_board = np.copy(self.board)
        for x in range(self.columns):
            for y in range(self.rows):
                neighbors=[self.board[i][j] if i>=0 and i<self.columns\
                                and j>=0 and j<self.rows  else 0\
                                    for i in range(x-1,x+2) for j in range(y-1,y+2)]
                neighbors_num = sum(neighbors)-self.board[x,y] 
                # print(neighbors_num)
                if self.board[x,y]==1:
                    if neighbors_num<2 or neighbors_num>3:
                        new_board[x,y]=0
                elif neighbors_num==3:
                    new_board[x,y]=1
        self.board=new_board.copy()

                        
        # self.board = np.random.randint(0,2,size=(self.columns,self.rows))

    
    def draw_board(self,screen):
        radius=2
        gap=1
        shapes_coords=[]
        for i in range(self.columns):
            for j in range(self.rows):
                if self.board[i,j]==1:
                    shapes_coords.append(((2*i+1)*radius+i*gap, (2*j+1)*radius+j*gap))
        for shape in shapes_coords:
            pygame.draw.circle(screen,random_color(),shape,radius)
            # pygame.draw.rect(screen,(255,0,0),(shape[0]-radius,shape[1]-radius,\
            #     shape[0]+radius,shape[1]+radius))

def random_color():
    return (np.random.randint(255),255,np.random.randint(255))
if __name__=="__main__":
    width,height=800,600
    game=gameOfLife(160,120)
    pygame.init()
    clock = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((width,height))
    pygame.display.set_caption('Hello World!')
    while True: # main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                pass
        DISPLAYSURF.fill((0, 0, 0))
        game.update_board()
        game.draw_board(DISPLAYSURF)
                
        pygame.display.update()
        clock.tick(60)
    # print(game.board)