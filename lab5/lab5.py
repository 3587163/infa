import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 1
screen = pygame.display.set_mode((1000, 700))

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

#drawing count
f1 = pygame.font.Font(None, 30)
text1=f1.render(str(count), True, WHITE)
text2=f1.render("count:", True, WHITE)

number_of_balls=randint(3,7)
x = []*number_of_balls
y = []*number_of_balls
r = []*number_of_balls

def new_ball():
    global x, y, r
    '''draws a new ball '''
    '''x,y - coordinates of the centre
    r-radius'''
    x = randint(100, 1100)
    y = randint(100, 900)
    r = randint(10, 100)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)

def more_balls():
    '''add balls'''
    for i in range(0 ,number_of_balls,1):
        x[i] = randint(100, 1100)
        y[i] = randint(100, 900)
        r[i] = randint(10, 100)
        color = COLORS[randint(0, 5)]
        circle(screen, color, (x[i], y[i]), r[i])

#pool=[new_ball() for i in range(number_of_balls)]
#for unit in pool:
   # unit.vx=randint(-20, 20)
   # unit.vy=randint(-20, 20)
   # unit.xt=x+vx*t
    #unit.yt=y+vy*t

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

def incircle(m_x, m_y, x, y):
#    global x, y, r
    return ((m_x-x)**2+(m_y-y)**2)**(1/2) < r
    
 

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(number_of_balls):
                if incircle(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], x[i],y[i]):
                    if r>=50:
                        count = count + 1
                    if r<=20:
                        count = count + 3
                    else:
                        count = count + 2
        print(count)
    more_balls()
#    new_ball()
    screen.blit(text1, (650, 200))
    screen.blit(text2, (590, 200))        
    pygame.display.update()
    screen.fill(BLACK)
pygame.quit()
