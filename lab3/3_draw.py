import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))
def bg():
    rect(screen, (0, 200, 0), (0, 0, 400, 400), 0)
    rect(screen, (0, 200, 255), (0, 0, 400, 200), 0)
#x,y-смещение по вертикали и горизотнали
#a- -1 если не отражаем или 1 если отражаем 
#z- координата оси по x относительно которой отражение
#t,s-сжатие по х и у, k=0 если а=1 и к=1 если а=-1
def tree(x,y,t,s):
    rect(screen, (200, 200, 200), (t*30+x, s*200+y, 25*t, 100*s),0)
    ellipse(screen, (0, 150, 0), (t*(-10)+x, s*50+y, 100*t, s*150),0)
    ellipse(screen, (0, 200, 0), (t*(-10)+x, s*50+y, 100*t, s*150),2)
    ellipse(screen, (0, 150, 0), (t*(-10)+x, s*90+y, t*100, s*150),0)
    ellipse(screen, (0, 200, 0), (t*(-10)+x, s*90+y, t*100, s*150),2)
    ellipse(screen, (0, 150, 0), (t*0+x, s*90+y, t*150, s*100),0)
    ellipse(screen, (0, 200, 0), (t*0+x, s*90+y, t*150, s*100),2)
    ellipse(screen, (0, 150, 0), (t*(-70)+x, s*90+y, 150*t, s*100),0)
    ellipse(screen, (0, 200, 0), (t*(-70)+x, s*90+y, 150*t, s*100),2)
    ellipse(screen, (255, 192, 203), (t*40+x, s*220+y, 25*t,s*20),0)
    ellipse(screen, (255, 192, 203), (t*120+x, s*135+y, 25*t,s*20),0)
    ellipse(screen, (255, 192, 203), (t*45+x, s*75+y,25*t, s*20),0)
    ellipse(screen, (255, 192, 203), (t*(-60)+x, s*135+y, 25*t,s*20),0)
def unic(x,y,z,t,s,a):
    if a==1:
        k=1
    if a==-1:
        k=0
    rect(screen, (255, 255, 255), (2*z-a*t*225+x, 280*s+y, 10*t, 50*s),0)
    rect(screen, (255, 255, 255), (2*z-a*t*280+x, 280*s+y, 10*t, 50*s),0)
    ellipse(screen, (255, 255, 255), (2*z-a*t*(200+100*k)+x, 250*s+y,100*t,50*s),0)
    ellipse(screen, (255, 255, 255), (2*z-a*t*(270+45*k)+x, 200*s+y,45*t ,25*s),0)
    rect(screen, (255, 255, 255), (2*z-a*t*(275+25*k)+x, 220*s+y, 25*t, 55*s),0)
    ellipse(screen, (255, 255, 255), (2*z-a*t*(303+25*k)+x, 205*s+y,25*t ,15*s),0)
    rect(screen, (255, 255, 255), (2*z-a*t*205+x, 280*s+y, 12*t, 55*s),0)
    rect(screen, (255, 255, 255), (2*z-a*t*250+x, 280*s+y, 12*t, 55*s),0)
    polygon(screen, (233, 175, 175), [(2*z-a*t*290+x,175*s+y), (2*z-a*t*295+x,200*s+y), (2*z-a*t*285+x,200*s+y)],0)
    ellipse(screen, (255, 238, 170), (2*z-a*t*(255+25*k)+x, 220*s+y, 25*t ,15*s),0)
    ellipse(screen, (255, 238, 170), (2*z-a*t*(258+22*k)+x, 235*s+y, 22*t ,12*s),0)
    ellipse(screen, (233, 198, 175), (2*z-a*t*(264+25*k)+x, 215*s+y, 25*t ,15*s),0)
    ellipse(screen, (233, 175, 175), (2*z-a*t*(257+20*k)+x, 210*s+y, 20*t ,15*s),0)
    ellipse(screen, (233, 198, 175), (2*z-a*t*(262+25*k)+x, 220*s+y, 25*t ,15*s),0)
    ellipse(screen, (233, 198, 175), (2*z-a*t*(255+25*k)+x, 230*s+y, 25*t ,14*s),0)
    ellipse(screen, (221, 175, 233), (2*z-a*t*(245+24*k)+x, 230*s+y, 24*t ,11*s),0)
    ellipse(screen, (221, 175, 233), (2*z-a*t*(245+23*k)+x, 250*s+y, 23*t ,10*s),0)
    ellipse(screen, (175, 233, 221), (2*z-a*t*(250+25*k)+x, 245*s+y, 25*t ,12*s),0)
    ellipse(screen, (175, 233, 221), (2*z-a*t*(240+21*k)+x, 241*s+y, 21*t ,10*s),0)
    ellipse(screen, (255, 238, 170), (2*z-a*t*(255+25*k)+x, 230*s+y, 25*t ,15*s),0)
    ellipse(screen, (221, 175, 233), (2*z-a*t*(260+24*k)+x, 245*s+y, 24*t ,15*s),0)
    ellipse(screen, (233, 175, 175), (2*z-a*t*(240+25*k)+x, 240*s+y, 25*t ,12*s),0)
    ellipse(screen, (175, 233, 221), (2*z-a*t*(264+25*k)+x, 235*s+y, 25*t ,10*s),0)
    ellipse(screen, (233, 175, 175), (2*z-a*t*(265+25*k)+x, 200*s+y, 25*t ,15*s),0)
    ellipse(screen, (229, 128, 255), (2*z-a*t*(300+7*k)+x, 210*s+y, 7*t, 7*s),0)
    ellipse(screen, (0, 0, 0), (2*z-a*t*(301+4*k)+x, 210*s+y, 4*t, 4*s),0)
    ellipse(screen, (175, 233, 221), (2*z-a*t*(173+23*k)+x, 280*s+y, 23*t ,10*s),0)
    ellipse(screen, (255, 255, 255), (2*z-a*t*(185+2*k)+x, 280*s+y, 2*t , 1*s),0)
    ellipse(screen, (255, 238, 170), (2*z-a*t*(185+25*k)+x, 290*s+y, 25*t ,15*s),0)
    ellipse(screen, (221, 175, 233), (2*z-a*t*(190+24*k)+x, 305*s+y, 24*t ,15*s),0)
    ellipse(screen, (233, 175, 175), (2*z-a*t*(170+25*k)+x, 300*s+y, 25*t ,12*s),0)
    ellipse(screen, (255, 238, 170), (2*z-a*t*(180+22*k)+x, 265*s+y, 22*t ,12*s),0)
    ellipse(screen, (175, 233, 221), (2*z-a*t*(194+25*k)+x, 305*s+y, 25*t ,10*s),0)
    ellipse(screen, (233, 175, 175), (2*z-a*t*(187+20*k)+x, 270*s+y, 20*t ,15*s),0)
    ellipse(screen, (233, 198, 175), (2*z-a*t*(192+25*k)+x, 290*s+y, 25*t ,15*s),0)
    ellipse(screen, (175, 233, 221), (2*z-a*t*(170+21*k)+x, 306*s+y, 21*t ,10*s),0)
    ellipse(screen, (233, 198, 175), (2*z-a*t*(185+25*k)+x, 290*s+y, 25*t ,14*s),0)
    ellipse(screen, (221, 175, 233), (2*z-a*t*(175+24*k)+x, 290*s+y, 24*t ,11*s),0)
    ellipse(screen, (255, 238, 170), (2*z-a*t*(185+25*k)+x, 280*s+y, 25*t ,15*s),0)
    ellipse(screen, (233, 198, 175), (2*z-a*t*(194+25*k)+x, 275*s+y, 25*t ,15*s),0)
    ellipse(screen, (175, 233, 221), (2*z-a*t*(180+25*k)+x, 315*s+y, 25*t ,12*s),0)
    ellipse(screen, (221, 175, 233), (2*z-a*t*(173+23*k)+x, 315*s+y, 23*t ,10*s),0)
    ellipse(screen, (233, 175, 175), (2*z-a*t*(195+25*k)+x, 260*s+y, 25*t ,15*s),0)

bg()
tree(70,0,0.75,0.75)
tree(0,50,0.5,0.75)
tree(80,130,0.75,0.5)
tree(50,200,0.5,0.5)
tree(0,250,0.5,0.5)
unic(0,150,200,0.25,0.25,1)
unic(50,100,0,0.5,0.5,-1)
unic(100,100,200,0.75,0.75,1)
unic(-50,100,0,1,1,-1)
d=0
for r in range (1,51,1):
    circle(screen,(0+5*d,200+1*d,255-5*d),(300,50),75-r)
    d=d+1
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
