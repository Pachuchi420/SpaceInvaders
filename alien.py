import pygame
from os import path

# Path Function
def getFile(fileName):
    return path.join(path.dirname(__file__), fileName)


class Alien(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        file_path = getFile('graphics/' + color + '.png')
        self.original_image = pygame.image.load(file_path).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (42,36))
        self.rect = self.image.get_rect(topleft = (x,y))
        if color == 'red': self.value = 10
        elif color == 'yellow': self.value = 20 
        else: self.value = 30

    def update(self,direction):
        self.rect.x += direction

class Extra(pygame.sprite.Sprite):
    def __init__(self, side, screen_width):
        super().__init__()
        image = pygame.image.load(getFile('graphics/extra.png')).convert_alpha()
        extra_sound = pygame.mixer.Sound(getFile('audio/extra.mp3'))
        self.image = pygame.transform.scale(image,(56,48))
        if side == 'right':
            x = screen_width + 50 
            self.speed = -3
            extra_sound.play()
            extra_sound.set_volume(0.3)
        else:
             x = -50
             self.speed = 3
             extra_sound.play()
             extra_sound.set_volume(0.3)
        self.rect = self.image.get_rect(topleft = (x,50))

    def update(self):
        self.rect.x += self.speed