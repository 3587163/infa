import pygame
from pygame.draw import *
from random import randint
from array import *
import numpy as np

print('enter your name')
name = input()

pygame.init()

FPS = 7
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
number_of_polygons=5
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
        r.append(randint(10, 50))
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
    
x0=array('f',[])
y0=array('f',[])
color0= []

def more_polygons():
    for k in range(number_of_polygons):
        x0.append(randint(100, 950))
        y0.append(randint(100, 400))
        color0.append(COLORS[randint(0, 5)])
        polygon(screen, color0[k], [(x0[k], y0[k]),(x0[k] + 20, y0[k] + 10), (x0[k] + 20, y0[k] - 10)])
           
def in_polygon(m_x, m_y, xx0, yy0):
    for k in range(number_of_polygons):
        return (m_x > xx0) and (m_x < xx0 + 20) and (yy0 + (m_x - xx0) > m_y) and (yy0 - (m_x - xx0) < m_y)
    
def more_polygons_moving():
    alpha = 0
    da = 1
    R = 2
    for k in range(number_of_polygons):
        if alpha>=360:
            alpha=0
        alpha = alpha + da
        x0[k] = x0[k] + R - R * np.cos(alpha*np.pi/180)
        y0[k] = y0[k] + R * np.sin(alpha*np.pi/180)
        polygon(screen, color0[k], [(x0[k], y0[k]), (x0[k] + 20, y0[k] + 10), (x0[k] + 20, y0[k] - 10)])
    

pygame.display.update()
clock = pygame.time.Clock()
finished = False

more_balls()
more_polygons()
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
            for k in range(number_of_polygons):
                if in_polygon(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], x0[k],y0[k]):
                    count = count - 2
        print(count) 
    pygame.display.update()
    screen.fill(BLACK)
    more_balls_moving()
    more_polygons_moving()
pygame.quit()

c=('i',[])
f = open('5besttable.txt','w')
f.write(name)
f.write(': ')
f.write(str(count))
f.close()
f = open('5besttable.txt','r')
print(*f)
f.close()
