import pygame
import random 

black = (0,0,0)
white = (255,255,255)
done = False
score = 0
pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("../personajes/astronauta1red.png").convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.speed_y = 0
        self.speed_x = 0     
    
    def changespeed(self, y):
        self.speed_y += y

    def update(self): 
        self.rect.y += self.speed_y
        # mouse_pos = pygame.mouse.get_pos()
        # player.rect.x = 40
        # player.rect.y = mouse_pos[1]

class Meteoro(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("../enemigos/met.png").convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()

    def update(self): 
        self.rect.x -=1
        if self.rect.x <= 0: 
            self.rect.x = 850    

class Laser(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("../shoots/shoot_r_30.png").convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()

    def update(self): 
        self.rect.x += 5 


screen = pygame.display.set_mode([840,600])
fondo = pygame.image.load("../fondos/space2red.png").convert()
clock = pygame.time.Clock()

all_sprites_list = pygame.sprite.Group()
meteoro_list = pygame.sprite.Group()
laser_list = pygame.sprite.Group()

def sec_enemi():
    for i in range(3): 
        meteoro = Meteoro()
        meteoro.rect.x = 800
        meteoro.rect.y = random.randrange(500)

        meteoro_list.add(meteoro)
        all_sprites_list.add(meteoro)

player = Player()
all_sprites_list.add(player)

sound = pygame.mixer.Sound("../music/laser_shoot.mp3")
music_fondo = pygame.mixer.Sound("../music/sunflower.mp3")
music_fondo.play()

while not done: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_UP: 
                player.changespeed(-3)
            if event.key == pygame.K_DOWN: 
                player.changespeed(3)
            if event.key == pygame.K_SPACE:
                laser = Laser()
                laser.rect.y = player.rect.y + 70
                laser.rect.x = player.rect.x + 100 
                all_sprites_list.add(laser)
                laser_list.add(laser)
                sound.play()
            
        if event.type == pygame.KEYUP: 
            if event.key == pygame.K_UP: 
                player.changespeed(3)
            if event.key == pygame.K_DOWN: 
                player.changespeed(-3)
        if not meteoro_list: 
            sec_enemi()
        # if event.type == pygame.MOUSEBUTTONDOWN: 
        #     laser = Laser()
        #     laser.rect.y = player.rect.y + 70
        #     laser.rect.x = player.rect.x + 100 
        #     all_sprites_list.add(laser)
        #     laser_list.add(laser)

    all_sprites_list.update() #importante que vaya antes de llamar a la ventana, es para mover el jugador por el metodo update de la clase
    
    for laser in laser_list: 
        meteoro_hit_list = pygame.sprite.spritecollide(laser, meteoro_list, True) #coliciones de laser y meteoro (elimina meteoro)
        for meteoro in meteoro_hit_list: 
            all_sprites_list.remove(laser) #quita el laser de la lista de sprites
            laser_list.remove(laser) #quita el laser de la lista de laseres
            score += 1
            print(score)
        if laser.rect.x > 840: 
            all_sprites_list.remove(laser) #por si el laser mo choca con nada para que deje de existir esa variable
            laser_list.remove(laser)  

    screen.blit(fondo, [0, 0])
    all_sprites_list.draw(screen) #importante que vaya despues de pintar la ventana 

    pygame.display.flip()
    clock.tick(60)
