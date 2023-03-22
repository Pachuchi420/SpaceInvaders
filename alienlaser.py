import pygame 
from os import path
from pygame.event import get 

# Path Function
def getFile(fileName):
    return path.join(path.dirname(__file__), fileName)


class AlienLaserClass(pygame.sprite.Sprite):
    def __init__(self, pos, speed, screen_height):
        super().__init__()

        # Importing & Transforming Images
        laser1 = pygame.image.load(getFile('graphics/alienlaser1.png'))
        laser1 = pygame.transform.rotate(laser1, 180)
        laser2 = pygame.image.load(getFile('graphics/alienlaser2.png'))
        laser2 = pygame.transform.rotate(laser2, 180)
        laser3 = pygame.image.load(getFile('graphics/alienlaser3.png'))
        laser3 = pygame.transform.rotate(laser3, 180)
        
        # Self Sprite Work
        self.sprites = []
        self.sprites.append(laser1)
        self.sprites.append(laser2)
        self.sprites.append(laser3)
        self.current_sprite = 0

        # Self Properties
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.height_y_constraint = screen_height
    
    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()


    def update(self):
        self.current_sprite += 0.08

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
        self.rect.y += self.speed
        self.destroy()
