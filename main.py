import pygame, sys, random
from setting import Setting
from player import Player
from car import Car
from sprite import SimpleSprite, LongSprite


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2(0, 0)
        self.fg = pygame.image.load('MyAssets/graphics/main/overlay.png').convert_alpha()
        self.bg = pygame.image.load('MyAssets/graphics/main/map.png').convert_alpha()

    def customize_draw(self):
        # camera set up
        self.offset.x = player.rect.centerx - Setting().width_screen / 2
        self.offset.y = player.rect.centery - Setting().height_screen / 2
        # Drawing
        display_surf.blit(self.bg, -self.offset)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            new_pos = sprite.rect.topleft - self.offset
            display_surf.blit(sprite.image, new_pos)
        display_surf.blit(self.fg, -self.offset)
    
# basic setup
pygame.init()
display_surf = pygame.display.set_mode((Setting().width_screen, Setting().height_screen))
pygame.display.set_caption("Frogger")
clock = pygame.time.Clock()

# Groups
all_sprites = AllSprites()
obstacle_sprites = pygame.sprite.Group()

# Sprites
player = Player((2000, 3200), all_sprites, obstacle_sprites)
for name, pos_list in Setting().SIMPLE_OBJECTS.items():
    surf = pygame.image.load(f'MyAssets/graphics/objects/simple/{name}.png').convert_alpha()
    for pos in pos_list:
        SimpleSprite(surf, pos, [all_sprites, obstacle_sprites])
for name, pos_list in Setting().LONG_OBJECTS.items():
    surf = pygame.image.load(f'MyAssets/graphics/objects/long/{name}.png').convert_alpha()
    for pos in pos_list:
        LongSprite(surf, pos, [all_sprites, obstacle_sprites])
# Timer
car_timer = pygame.event.custom_type()
pygame.time.set_timer(car_timer, 300)

# Font
font = pygame.font.Font(None, 50)
text_surf = font.render('You Win', True, (255, 255, 255))
text_rect = text_surf.get_rect(center=(Setting().width_screen / 2, Setting().height_screen / 2))

# Sount
bg_sound = pygame.mixer.Sound('MyAssets/audio/music.mp3')
bg_sound.play(loops=-1)

# Game loop
while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == car_timer:
            pos = random.choice(Setting().CAR_POSITION)
            if pos not in Setting().car_pos_list:
                Setting().car_pos_list.append(pos)
                Car(pos, [all_sprites, obstacle_sprites])
            if len(Setting().car_pos_list) > 5:
                del Setting().car_pos_list[0]
    
    # delta time
    dt = clock.tick(60) / 1000        
    
    # Draw
    display_surf.fill((0, 0, 0))
    if player.pos.y >= 870: 
        # all_sprites.draw(display_surf)
        all_sprites.customize_draw()
        all_sprites.update(dt)
    else:
        display_surf.fill('teal')
        display_surf.blit(text_surf, text_rect)
    
    # update
    pygame.display.update()


