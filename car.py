import pygame, random
from os import walk

class Car(pygame.sprite.Sprite):
    """A class to spawn cars"""
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.name = 'car'
        self.list_cars = []
        self.import_car()
        self.image = random.choice(self.list_cars)
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.rect.inflate(0, -self.rect.height // 2)
        # Car movement
        self.pos = pygame.math.Vector2(self.rect.center)    
        if self.pos[0] < 300:
            self.direct = pygame.math.Vector2(1, 0)
        else:
            self.direct = pygame.math.Vector2(-1, 0)
            self.image = pygame.transform.flip(self.image, True, False)
        
        self.speed = 300
    
    def import_car(self):
        path = 'MyAssets/graphics/cars'
        for file_car in list(walk(path)):
            for car in file_car[2]:
                surface = pygame.image.load(path + '/' + car).convert_alpha()
                self.list_cars.append(surface)
                
    def update(self, dt):
        self.pos += self.direct*self.speed*dt
        self.hitbox.center = (round(self.pos.x), round(self.pos.y))
        self.rect.center = self.hitbox.center
        if not (-200 < self.rect.x < 3400):
            self.kill()