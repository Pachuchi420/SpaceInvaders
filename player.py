from numpy import short
import pygame 
from os import path
from pygame.constants import KSCAN_SYSREQ 
from laser import Laser


# Path Function
def getFile(fileName):
    return path.join(path.dirname(__file__), fileName)




class Player(pygame.sprite.Sprite):
    
    def __init__(self,pos, constraint, speed):
        super().__init__()

        # Import Sprites
        global static
        global left
        global right
        global shot
        static = pygame.image.load(getFile('graphics/player/player_1.png')).convert_alpha()
        static = pygame.transform.scale(static, (36,42))
        left = pygame.image.load(getFile('graphics/player/player_2.png')).convert_alpha()
        left = pygame.transform.scale(left, (36,42))
        right = pygame.image.load(getFile('graphics/player/player_3.png')).convert_alpha()
        right = pygame.transform.scale(right, (36,42))
        shot = pygame.image.load(getFile('graphics/player/player_4.png')).convert_alpha()
        shot = pygame.transform.scale(shot, (36,42))

        # Import Sound
        global laser_sound
        laser_sound = pygame.mixer.Sound(getFile('audio/laser.wav'))
        

        # Self Properties
        self.image = static
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = speed 
        self.max_x_constraint = constraint
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 400
        self.lasers = pygame.sprite.Group()
    
        
    # Player Movement
    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.image = right
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.image = left
        else: 
            self.image = static
        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            laser_sound.set_volume(0.1)
            laser_sound.play()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()


    # Recharge Function
    def recharge (self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True


    # Screen Constraint
    def constraint(self):   
        if self.rect.left <= 0: 
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint   
    

    # Laser Function
    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center, -8, self.rect.bottom - 10))


    # Self Update / Calls all functions
    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        self.lasers.update()


