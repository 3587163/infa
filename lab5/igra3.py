import pygame
from pygame.draw import *
from random import randint
from array import *
import numpy as np

print('enter your name')
name = input()
pygame.init()

FPS = 30
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

count = 0#gained points

number_of_balls = 5
number_of_polygons = 5
dt = 0.05

x = array('f', [])#circle's centre coordinate x
y = array('f', [])#circle's centre coordinate y
r = array('f', [])#radius of the circle
color = []#color of the circle
vx = array('f', [])#speed x
vy = array('f', [])#speed y

def more_balls():
    '''creates balls'''
    for k in range(number_of_balls):
        x.append(randint(100, 950))
        y.append(randint(100, 400))
        r.append(randint(10, 50))
        color.append(COLORS[randint(0, 5)])
        vx.append(randint(-200, 200))
        vy.append(randint(-200, 200))
        circle(screen, color[k], (x[k], y[k]), r[k])
        
def more_balls_moving():
    '''makes all balls move'''
    for k in range(number_of_balls):
        if x[k] + r[k] > 995 or x[k] - r[k] < 5:
            vx[k] = - vx[k]
        if y[k] + r[k] > 495 or y[k] - r[k] < 5:
            vy[k] = - vy[k]
        x[k] = x[k] + vx[k] * dt
        y[k] = y[k] + vy[k] * dt
        circle(screen, color[k], (x[k], y[k]), r[k])


def draw_count():
    '''draws count on the screen'''
    f1 = pygame.font.Font(None, 30)
    text1 = f1.render(str(count), True, WHITE)
    text2 = f1.render("count:", True, WHITE)
    screen.blit(text1, (560, 50))
    screen.blit(text2, (500, 50))


m_x = 0
m_y = 0
def click(event):
    '''
    finds the position of the mouse
    m_x - coordinate x of the mouse
    m_y - coordinate y
    '''
    pos = pygame.mouse.get_pos()
    print(pos)
    m_x = pos[0]
    m_y = pos[1]

def incircle(m_x, m_y, x0, y0):
    '''tells if click was in circle'''
    for k in range(number_of_balls):
        return ((m_x - x0)**2+(m_y - y0)**2)**(1/2) < r[k]
    
x0 = array('f', [])#coordinate x of left point of polygon
y0 = array('f', [])#coordinate y of left point of polygon
color0 = []#color of the polygon

def more_polygons():
    '''creates polygons'''
    for k in range(number_of_polygons):
        x0.append(randint(100, 950))
        y0.append(randint(100, 400))
        color0.append(COLORS[randint(0, 5)])
        polygon(screen, color0[k], [(x0[k], y0[k]),(x0[k] + 20, y0[k] + 10), (x0[k] + 20, y0[k] - 10)])
           
def in_polygon(m_x, m_y, xx0, yy0):
    '''tells if the click was in polygon'''
    for k in range(number_of_polygons):
        return (m_x > xx0) and (m_x < xx0 + 20) and (yy0 + (m_x - xx0) > m_y) and (yy0 - (m_x - xx0) < m_y)

def more_polygons_moving():
    '''makes polygons move'''
    for k in range(number_of_polygons):
        vx0 = randint(-200, 200)
        vy0 = randint(-200, 200)
        if x0[k] > 975 or x0[k] < 5:
            vx0 = -vx0
        if y0[k] > 485 or y0[k] < 15:
            vy0 = -vy0
        x0[k] = x0[k] + vx0 * dt
        y0[k] = y0[k] + vy0 * dt
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
                if incircle(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], x[k], y[k]):
                    count = count + 1
            for k in range(number_of_polygons):
                if in_polygon(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], x0[k], y0[k]):
                    count = count + 2 
    pygame.display.update()
    screen.fill(BLACK)
    more_balls_moving()
    more_polygons_moving()
pygame.quit()


names = [] #[('Sarah', 5), ("Ken", 10), ...]
f1 = open("leader_board.txt", "r")
lines = f1.readlines()

played_before = False #tells if the player is already in the top 5 board
better_than_somebody = False #tells if the player gained more points than somebody in the top 5 board

for line in lines:
    if len(line) < 2:
        break
    line = line.split()
    name_local = line[0]
    if (name_local == name):
        played_before = True
    score_local = int(line[2])
    if (count > score_local):
        better_than_somebody = True
    names.append((name_local, score_local))
    
#replaces the count if player gained more points than before
if better_than_somebody:
    if played_before:
        index = -1#index of the same name
        for k in range(len(names)):
            if (name == names[k][0]):
                index = k       
        if (names[index][1] < count):
            names[index] = (name, count)
            
#replaces the worst player of the board  
    else:
        min_ = min([x[1] for x in names])#minimal score
        index = -1#index of minimal score
        for k in range(len(names)):
            if names[k][1] == min_:
                index = k
        names[index] = (name, count)
        
f1.close()    

#updates the board
f = open('leader_board.txt','w')
for n in range(5):
    f.write(names[n][0])
    f.write(' : ')
    f.write(str(names[n][1]))
    f.write('\n')
f.close()

f = open('leader_board.txt','r')
print(*f)
f.close()
