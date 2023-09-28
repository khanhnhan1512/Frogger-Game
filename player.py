import pygame, sys
from os import walk
from setting import Setting


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites):
        super().__init__(group)
        # load animation for our player
        self.import_assets()
        self.state = 'down'
        self.frame_index = 0
        self.image = self.animation[self.state][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        # movement
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 200
        # collision
        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.inflate(0, -self.rect.height // 2)
    
    def collision(self, axis):
        if axis == 'horizontal':
            for sprite in self.collision_sprites.sprites():
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
        else:
            for sprite in self.collision_sprites.sprites():
                if sprite.hitbox.colliderect(self.hitbox):
                    if hasattr(sprite, 'name') and sprite.name == 'car':
                        pygame.quit()
                        sys.exit()
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery
                    elif self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery
             
    def import_assets(self):
        self.animation = {}
        for index, folder in enumerate(walk('./MyAssets/graphics/player')):
            # x contains a tuple with 3 elements
            # the first element is the path
            # the second element is a list of directories inside the path
            # the third element is a list of files inside the path
            if index == 0:
                for name in folder[1]:
                    self.animation[name] = []
            else:
                for file in folder[2]:
                    file_path = folder[0].replace('\\', '/') + '/' +file
                    surf = pygame.image.load(file_path).convert_alpha()
                    self.animation[folder[0].split('\\')[-1]].append(surf)
        
    def move(self, dt):
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()
        # Horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')
        # Vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')   
        
    def animated(self, dt):
        if self.direction.length() > 0:
            self.frame_index += 10 * dt
            if self.frame_index >= len(self.animation[self.state]):
                self.frame_index = 0
        else:
            self.frame_index = 0
        self.image = self.animation[self.state][int(self.frame_index)]
    
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.state = 'left'
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.state = 'right'
        else:
            self.direction.x = 0    
        
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.state = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.state = 'down'
        else:
            self.direction.y = 0
    
    def restrict(self):
        if self.rect.left < Setting().width_screen //2:
            self.pos.x = Setting().width_screen //2 + self.rect.width //2
            self.hitbox.left = Setting().width_screen //2
            self.rect.left = Setting().width_screen //2
        elif self.rect.right > Setting().width_map - Setting().width_screen//2:
            self.pos.x = Setting().width_map - Setting().width_screen //2 - self.rect.width //2
            self.hitbox.right = Setting().width_map - Setting().width_screen //2
            self.rect.right = Setting().width_map - Setting().width_screen //2
        elif self.rect.bottom > Setting().height_map - Setting().height_screen//2:
            self.pos.y = Setting().height_map - Setting().height_screen //2 - self.rect.height //2
            self.hitbox.bottom = Setting().height_map - Setting().height_screen //2
            self.rect.bottom = Setting().height_map - Setting().height_screen //2
            
    
    def update(self, dt):
        self.input()
        self.move(dt)
        self.animated(dt)
        self.restrict()

