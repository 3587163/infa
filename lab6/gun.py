import math
from random import choice
from random import randint
import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

dt = 0.5
g = - 10
score = 0
less_size = 50

def draw_count():
    f1 = pygame.font.Font(None, 30)
    text1 = f1.render(str(score), True, BLACK)
    text2 = f1.render("score:", True, BLACK)
    screen.blit(text1, (460, 50))
    screen.blit(text2, (400, 50))


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx*dt
        self.y -= self.vy*dt
        self.vy += g*dt

        if self.x > 790 or self.x < 10:
            self.vx = - self.vx

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if abs(self.x - obj.x) < self.r + obj.r:
            if abs(self.y - obj.y) < self.r + obj.r:
                return True
            else:
                return False
        else:
            return False
        

x0 = 0
y0 = 0
class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 50
        self.y = 460

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if event.pos[0] == 50:
                self.an = 0
            else:
                self.an = math.atan((event.pos[1]-460) / (event.pos[0]-50))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.line(self.screen, self.color, [self.x, self.y],
                         [self.x + abs(pygame.mouse.get_pos()[0] + self.x) / less_size ,
                          self.y - abs(pygame.mouse.get_pos()[1] + self.y) / less_size ],
                          5)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY
            
class Target:
    def __init__(self):
        """ Инициализация новой цели. """
        self.screen = screen
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(2, 50)
        self.vx = randint(-20, 20)
        self.vy = randint(-20, 20)
        self.color = RED
        self.live = 1
        
    def move(self):
        self.x += self.vx*dt
        self.y -= self.vy*dt

        if self.x + self.r > 790 or self.x - self.r < 10:
            self.vx = - self.vx
        if self.y + self.r > 600 or self.y - self.r < 10:
            self.vy = - self.vy
            
    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target1 = Target()
target2 = Target()
target3 = Target()
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target1.draw()
    target1.move()
    target2.draw()
    target2.move()
    target3.draw()
    target3.move()
    draw_count()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
            while less_size > 20:
                less_size -= 5
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
            less_size = 50
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
    for b in balls:
        b.move()
        if b.hittest(target1) and target1.live:
            target1.live = 0
            score += 1
            target1 = Target()
        if b.hittest(target2) and target2.live:
            target2.live = 0
            score += 1
            target2 = Target()
        if b.hittest(target3) and target3.live:
            target3.live = 0
            score += 1
            target3 = Target() 
    gun.power_up()
pygame.quit()
