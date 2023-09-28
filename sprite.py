import pygame

class SimpleSprite(pygame.sprite.Sprite):
    def __init__(self, surf, pos, group):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -self.rect.height // 2)
        
        
class LongSprite(pygame.sprite.Sprite):
    def __init__(self, surf, pos, group):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-self.rect.width*0.7,
                                        -self.rect.height // 2)
        self.hitbox.bottom = self.rect.bottom - 10