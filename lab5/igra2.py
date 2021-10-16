import pygame
from pygame.draw import *
from random import randint
from array import *
import numpy as np
pygame.init()

FPS = 3
screen = pygame.display.set_mode((1000, 500))

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN, WHITE]

count = 0

number_of_balls=5
steps_of_time_number = 100
dt=0.05

x=array('f',[])
y=array('f',[])
r=array('f',[])
color= []
vx=array('f',[])
vy=array('f',[])

def more_balls():
    for k in range(number_of_balls):
        x.append(randint(100, 950))
        y.append(randint(100, 400))
        r.append(randint(10, 100))
        color.append(COLORS[randint(0, 5)])
        vx.append(randint(-200,200))
        vy.append(randint(-200,200))
        circle(screen, color[k], (x[k], y[k]), r[k])
        
def more_balls_moving():
    for k in range(number_of_balls):
        if x[k]+r[k]>995 or x[k]-r[k]<5:
            vx[k]=-vx[k]
        if y[k]+r[k]>495 or y[k]-r[k]<5:
            vy[k]=-vy[k]
        x[k]=x[k]+vx[k]*dt
        y[k]=y[k]+vy[k]*dt
        circle(screen, color[k], (x[k], y[k]), r[k])


#drawing count
def draw_count():
    f1 = pygame.font.Font(None, 30)
    text1=f1.render(str(count), True, WHITE)
    text2=f1.render("count:", True, WHITE)
    screen.blit(text1, (560, 50))
    screen.blit(text2, (500, 50))


def new_ball():
    global x, y, r, vx, vy,color
    '''draws a new ball '''
    '''x,y - coordinates of the centre
    r-radius'''
    x = randint(100, 950)
    y = randint(100, 400)
    r = randint(10, 100)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)
    vx = randint(-200,200)
    vy = randint(-200,200)
    
def ball_move():
    global x, y, r, vx, vy,color
    if x+r>995 or x-r<5:
        vx=-vx
    if y+r>495 or y-r<5:
        vy=-vy
    x=x+vx*dt
    y=y+vy*dt
    circle(screen, color, (x, y), r)


m_x=0
m_y=0
def click(event):
    '''finds the position of the mouse
    m_x - coordinate x of the mouse
    m_y - coord y'''
    pos = pygame.mouse.get_pos()
    print(pos)
    m_x = pos[0]
    m_y = pos[1]

def incircle(m_x, m_y, x0, y0):
    for k in range(number_of_balls):
        return ((m_x-x0)**2+(m_y-y0)**2)**(1/2) < r[k]


pygame.display.update()
clock = pygame.time.Clock()
finished = False

#new_ball()
more_balls()
while not finished:
    clock.tick(FPS) 
    draw_count()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for k in range(number_of_balls):
                if incircle(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], x[k],y[k]):
                    count = count + 1


        print(count) 
    pygame.display.update()
    screen.fill(BLACK)
    more_balls_moving()
pygame.quit()
