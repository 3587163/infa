import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

rect(screen, (0, 200, 0), (0, 0, 400, 400), 0)
rect(screen, (0, 200, 225), (0, 0, 400, 200), 0)
circle(screen, (255, 255, 0), (350, 0), 75)
#circle(screen, (255, 0, 0), (150, 230), 30, 0)
#circle(screen, (255, 0, 0), (250, 230), 20, 0)
#circle(screen, (0, 0, 0), (150, 230), 30, 1)
#circle(screen, (0, 0, 0), (250, 230), 20, 1)
#circle(screen, (0, 0, 0), (150, 230), 15, 0)
#circle(screen, (0, 0, 0), (250, 230), 10, 0)
rect(screen, (200, 200, 200), (30, 200, 25, 100),0)
circle(screen, (0, 150, 0), (30, 150), 75,0)
ellipse(screen, (0, 150, 0), (-10, 90,100,150),0)
ellipse(screen, (0, 150, 0), (-10, 50,100,150),0)
ellipse(screen, (0, 150, 0), (0, 90,150,100),0)
ellipse(screen, (255, 60, 180), (40, 220,25,20),0)
ellipse(screen, (255, 60, 180), (120, 135,25,20),0)
ellipse(screen, (255, 60, 180), (45, 75,25,20),0)
#polygon(screen, (0, 0, 0), [(225,200), (225,175),
                               #(300, 150), (300,175)])
#polygon(screen, (0, 0, 0), [(100, 150), (100,175),
                               #(175, 200), (175,175)])


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
