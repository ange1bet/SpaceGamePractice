import pygame
import random

black = (0,0,0)
white = (255,255,255)
done = False
score = 0
music = 0
pygame.init()

screen = pygame.display.set_mode([840,600])
fondo = pygame.image.load("../fondos/space2red.png").convert()
clock = pygame.time.Clock()

meteoro_list = pygame.sprite.Group()
laser_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

class Meteoro(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("../enemigos/met.png").convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()

    def update(self):
        if(self.rect.x==-70):
            self.rect.x=840
        self.rect.x -=1

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("../enemigos/et.png").convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()

    def update(self):
        if(self.rect.x==-70):
            self.rect.x=840
        self.rect.x -=1
        
        
class Laser(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("../shoots/shoot_r_30.png").convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += 5

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("../personajes/astronauta1red.png").convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.speed_y = 0
        self.speed_x = 0

    def changespeed(self,y):
        if(y==0):
            self.speed_y = -3 
        if(y==1):
            self.speed_y = 3   

    def update(self):
        self.rect.y -= self.speed_y
        if(self.rect.y <= 0 ):
            self.rect.y = 0
        if(self.rect.y >= 480):
            self.rect.y = 480

player = Player()
all_sprites_list.add(player)

def sec_enemigos():
    if score <=15:
        for i in range(3): 
            meteoro = Meteoro()
            meteoro.rect.x = 800
            meteoro.rect.y = random.randrange(500)

            meteoro_list.add(meteoro)
            all_sprites_list.add(meteoro)
    else: 
        meteoro = Boss()
        meteoro.rect.x = 800
        meteoro.rect.y = random.randrange(500)

        meteoro_list.add(meteoro)
        all_sprites_list.add(meteoro)
        
sound = pygame.mixer.Sound("../music/laser_shoot.mp3")
music_fondo = pygame.mixer.Sound("../music/sunflower.mp3")
music_boos = pygame.mixer.Sound("../music/YAOSOBI.mp3")
music_fondo.play()
music_fondo.set_volume(0.3)


while not done: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP :
            if event.key == pygame.K_UP:
                player.changespeed(1)
            if event.key == pygame.K_DOWN:
                player.changespeed(0)
            if event.key == pygame.K_SPACE:
                laser = Laser()
                sound.play()
                sound.set_volume(0.1)
                laser.rect.y = player.rect.y + 70
                laser.rect.x = player.rect.x + 100 
                all_sprites_list.add(laser)
                laser_list.add(laser)
        if not meteoro_list:
            sec_enemigos()

    all_sprites_list.update()

    for laser in laser_list: 
        meteoro_hit_list = pygame.sprite.spritecollide(laser, meteoro_list, True) #coliciones de laser y meteoro (elimina meteoro)
        for meteoro in meteoro_hit_list: 
            all_sprites_list.remove(laser) #quita el laser de la lista de sprites
            laser_list.remove(laser) #quita el laser de la lista de laseres
            score += 1
            print(score)
            if score == 10:
                music_boos.play()
                music_boos.set_volume(0.4)
            if score == 15:
                music_fondo.stop()
        if laser.rect.x > 840: 
            all_sprites_list.remove(laser) #por si el laser mo choca con nada para que deje de existir esa variable
            laser_list.remove(laser)

    screen.blit(fondo, [0, 0])
    all_sprites_list.draw(screen) #importante que vaya despues de pintar la ventana 

    pygame.display.flip()
    clock.tick(60)
