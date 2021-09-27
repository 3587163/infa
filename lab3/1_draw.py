import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

rect(screen, (120, 120, 120), (0, 0, 400, 400), 0)
circle(screen, (255, 255, 0), (200, 250), 150)
circle(screen, (0, 0, 0), (200, 250), 150,1)
circle(screen, (255, 0, 0), (150, 230), 30, 0)
circle(screen, (255, 0, 0), (250, 230), 20, 0)
circle(screen, (0, 0, 0), (150, 230), 30, 1)
circle(screen, (0, 0, 0), (250, 230), 20, 1)
circle(screen, (0, 0, 0), (150, 230), 15, 0)
circle(screen, (0, 0, 0), (250, 230), 10, 0)
rect(screen, (0, 0, 0), (100, 300, 200, 30),0)
polygon(screen, (0, 0, 0), [(225,225), (225,200),
                               (300, 175), (300,200)])
polygon(screen, (0, 0, 0), [(100, 175), (100,200),
                               (175, 225), (175,200)])


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
