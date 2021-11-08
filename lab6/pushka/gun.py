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

#t = 0
dt = 0.5
g = - 10
score = 0 # счет
less_size = 30 
amount_of_bombs = 5 # количество бомб 

def draw_button():
    ''' отрисовка кнопки чтобы стрелять бомбами'''
    f2 = pygame.font.Font(None, 30)
    text3 = f2.render(str(amount_of_bombs), True, BLACK)
    text4 = f2.render("use bomb", True, BLACK)
    screen.blit(text3, (160, 50))
    screen.blit(text4, (50, 50))
    
def draw_count():
    '''отрисовка счета'''
    f1 = pygame.font.Font(None, 30)
    text1 = f1.render(str(score), True, BLACK)
    text2 = f1.render("score:", True, BLACK)
    screen.blit(text1, (460, 50))
    screen.blit(text2, (400, 50))


class Ball:
    def __init__(self, screen: pygame.Surface, obj):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        obj - объект из которого вылетает мяч
        """
        self.screen = screen
        self.x = obj.x
        self.y = obj.y
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
        """отрисовка шара"""
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




class Explosive:
    def __init__(self, screen: pygame.Surface, obj):
        """конструирует бомбы
            obj - объект из которого вылетают бомбы"""
        self.screen = screen
        self.x = obj.x
        self.y = obj.y
        self.r = 5
        self.vx = 0
        self.vy = 0
        self.color = BLACK
        self.live = 30

    def move(self):
        """движение бомбы и отражение от стен"""
        self.x += self.vx*dt
        self.y -= self.vy*dt
        self.vy += g*dt
        if self.x + self.r > 790 or self.x - self.r < 10:
            self.vx = - self.vx

    def draw_explosion(self):
        pass

    def draw(self):
        """отрисовка бомбы"""
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """проверка соударения бомбы с объектом obj"""
        if abs(self.x - obj.x) < self.r + obj.r:
            if abs(self.y - obj.y) < self.r + obj.r:
                return True
            
            else:
                return False
        else:
            return False

class Explosion(pygame.sprite.Sprite):
    def __init__(self, filename):
        """взрыв"""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.center = (10000, 10000)

    def set_cord(self, x, y):
        """установка координат для спрайта взрыва"""
        self.rect.center = (x, y)
        
    
x0 = 0
y0 = 0
class Gun:
    def __init__(self, screen, x, y):
        """пушка(танк)"""
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = x
        self.y = y
        self.vx = 0

    def move_left(self):
        """движение пушки влево"""
        if self.x > 110:
            self.x -= 10
                
    def move_right(self):
        """движение пушки вправо"""
        if self.x < 760:
            self.x += 10
            
    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, self)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10
        
    def fire_with_bomb(self, event):
        """выстрел бомбой
        Происходит при отпускании кнопки мыши.
        """
        global explosive, bullet
        bullet += 1        
        new_explosive = Explosive(self.screen, self)
        new_explosive.r += 5
        self.an = math.atan2((event.pos[1]-new_explosive.y), (event.pos[0]-new_explosive.x))
        new_explosive.vx = 75
        new_explosive.vy = 75
        explosive.append(new_explosive)
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
        """отрисовка пушки(дула)"""
        pygame.draw.line(self.screen, self.color, [self.x, self.y],
                         [self.x + (pygame.mouse.get_pos()[0] - self.x) / less_size ,
                          self.y + (pygame.mouse.get_pos()[1] - self.y) / less_size ],
                          5)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY

class Player(pygame.sprite.Sprite):
    """ танки"""
    def __init__(self, filename, obj):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.center = (obj.x - 10, obj.y)
        
    def move_left(self):
        """движение спрайта танка влево"""
        if self.rect.x > 0:
            self.rect.x -= 10
                
    def move_right(self):
        """"движение спрайта танка вправо"""
        if self.rect.x < 650:
            self.rect.x += 10


class Target:
    def __init__(self):
        """ Инициализация новой цели. """
        self.screen = screen
        self.x = randint(600, 735)
        self.y = randint(300, 550)
        self.r = randint(10, 50)
        self.vx = randint(-20, 20)
        self.vy = randint(-20, 20)
        self.color = RED
        self.live = 1
        
    def move(self):
        """движение цели"""
        self.x += self.vx*dt
        self.y -= self.vy*dt

        if self.x + self.r > 790 or self.x - self.r < 10:
            self.vx = - self.vx
        if self.y + self.r > 600 or self.y - self.r < 10:
            self.vy = - self.vy
            
    def draw(self):
        """отрисовка цели"""
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)


class New_Target:
    def __init__(self):
        """инициализация другого типа цели который вылетает из крана"""
        self.screen = screen
        self.x = 640
        self.y = 120
        self.r = 25
        self.vx = randint(-20, 20)
        self.vy = 50 - randint(-30, 30)
        self.color = BLUE
        self.live = 1
        
        
    def move(self):
        """движение"""
        self.x += self.vx*dt
        self.y += self.vy*dt

        if self.x + self.r > 790 or self.x - self.r < 10:
            self.vx = - self.vx
        if self.y + self.r > 600 or self.y - self.r < 10:
            self.vy = - self.vy
            
    def draw(self):
        """отрисовка"""
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

class Cran(pygame.sprite.Sprite):
    """ краны из которых вылетают мишени"""
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.center = (700, 50)

class Plane(pygame.sprite.Sprite):
    def __init__(self, filename, obj):
        """самолеты с которых сбрасываются торпеды на танк. Их положение зависят от положений танков"""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.center = (obj.x, 50)

    def move(self, x):
        self.rect.x = x

class Enemy_Ball(pygame.sprite.Sprite):
    """торпеды"""
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.center = (100, 100)

        self.vx = 0
        self.vy = 10

        self.x = 0
        self.y = 0

    def set_cord(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        self.x += self.vx*dt
        self.y += self.vy*dt

        self.rect.center = (self.x, self.y)

    def hit_check(self, obj):
        """проверка на попадание торпеды в танк(при попадании игра кончается)"""

        if ((self.x - obj.rect.x - 100)**2 + (self.y - obj.rect.y - 64.5)**2 < 50**2):
            pygame.quit()
            

def button_pressed():
    """проверка на нажатие кнопки чтобы стрелять бомбами"""
    x_pos = pygame.mouse.get_pos()[0]
    y_pos = pygame.mouse.get_pos()[1]
    if x_pos > 20 and x_pos < 200 and y_pos < 60 and y_pos > 40:
        return True
    else:
        return False


#создание окна    
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
explosive = []

move_left_now = 0
move_right_now = 0

clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
gun1 = Gun(screen, 100 , 460)#создание пушки
target1 = Target()#создание цели не вылетающей из крана 
target2 = Target()#создание уели не вылетающей из крана
target3 = New_Target()#вылетает из крана
finished = False
all_sprites = pygame.sprite.Group()#группа спрайтов
player = Player('tank2.png', gun1)#создание танка
all_sprites.add(player)#добавление его в группу спрайтов
expl = Explosion('expl.png')
all_sprites.add(expl)
cran = Cran('cran.png')
all_sprites.add(cran)
plane = Plane('plane.png', gun1)
all_sprites.add(plane)
enemy_ball = Enemy_Ball('torpeda.png')
all_sprites.add(enemy_ball)

enemy_count = 0

while not finished:
    screen.fill(WHITE)
    all_sprites.draw(screen)#
    gun1.draw()
    target1.draw()
    target1.move()
    target2.draw()
    target2.move()
    target3.draw()
    target3.move()
    plane.move(gun1.x - 120)
    #выпускание торпеды каждые 150 кадров
    if (enemy_count % 150 == 0):
        enemy_ball.set_cord(plane.rect.x + 100, plane.rect.y + 100)
        
    enemy_count += 1#подсчет кадров
    
    enemy_ball.move()
    enemy_ball.hit_check(player)
    
    draw_count()
    draw_button()
    for b in balls:
        b.draw()
    pygame.display.update()

    index_to_kill = 'none'#индекс бомбы
    expl.set_cord(10000, 10000)
    
    #отрисовка взрыва для бомбы
    for k in range(len(explosive)):
        explosive[k].draw()
        if explosive[k].x > 300:
            explosive[k].draw_explosion()
            index_to_kill = k
    #удаляет бомбу после взрыва
    if index_to_kill != 'none':
        expl.set_cord(explosive[index_to_kill].x, explosive[index_to_kill].y)
        explosive[index_to_kill].r = 100
        #проверка попали ли цели в радиус поражения взрывом
        if explosive[index_to_kill].hittest(target1) and target1.live:
            target1.live = 0
            score += 1
            target1 = Target()
        if explosive[index_to_kill].hittest(target2) and target2.live:
            target2.live = 0
            score += 1
            target2 = Target()
        if explosive[index_to_kill].hittest(target3) and target3.live:
            target3.live =0
            score += 2
            target3 = New_Target()
            
        explosive.pop(index_to_kill)

    if move_left_now:
        gun1.move_left()
        player.move_left()

    if move_right_now:
        gun1.move_right()
        player.move_right()
        
            
    pygame.display.update()
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        #движение танка    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left_now = 1
                
            if event.key == pygame.K_RIGHT:
                move_right_now = 1

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left_now = 0
                
            if event.key == pygame.K_RIGHT:
                move_right_now = 0
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun1.fire2_start(event)
            if button_pressed() == True:
                if amount_of_bombs > 0:
                    gun1.fire_with_bomb(event)
                    amount_of_bombs -= 1
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            gun1.fire2_end(event)
            
        elif event.type == pygame.MOUSEMOTION:
            gun1.targetting(event)
    #проверка на попадания мячей и бомб в цели                   
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
            score += 2
            target3 = New_Target()
            
    for e in explosive:
        e.move()
        if e.hittest(target1) and target1.live:
            target1.live = 0
            score += 1
            target1 = Target()
        if e.hittest(target2) and target2.live:
            target2.live = 0
            score += 1
            target2 = Target()
        if e.hittest(target3) and target3.live:
            target3.live =0
            score += 2
            target3 = New_Target()
    gun1.power_up()
pygame.quit()
