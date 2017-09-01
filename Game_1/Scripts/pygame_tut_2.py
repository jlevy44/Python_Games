import pygame, numpy as np, sys
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((1024, 768))
clock = pygame.time.Clock()

class PadSprite(pygame.sprite.Sprite):
    normal = pygame.image.load('../Images/pad_normal.png')
    hit = pygame.image.load('../Images/pad_hit.png')
    def __init__(self,number,position):
        pygame.sprite.Sprite.__init__(self)
        self.number = number
        self.rect = pygame.Rect(self.normal.get_rect())
        self.rect.center = position
    def update(self,hit_list):
        if self in hit_list: self.image = self.hit
        else: self.image = self.normal

pads = [
PadSprite(1,(200, 200)),
PadSprite(2,(800, 200)),
PadSprite(3,(200, 600)),
PadSprite(4,(800, 600)),
]
current_pad_number = 0
pad_group = pygame.sprite.RenderPlain(*pads)


class CarSprite(pygame.sprite.Sprite):
    MAX_FORWARD_SPEED = 10
    MAX_REVERSE_SPEED = 10
    ACCELERATION = 2
    TURN_SPEED = 5

    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load(image)
        self.position = position
        self.speed = self.direction = 0
        self.k_left = self.k_right = self.k_down = self.k_up = 0

    def update(self, deltat):
        self.speed += (self.k_up + self.k_down)
        if self.speed > self.MAX_FORWARD_SPEED: self.speed = self.MAX_FORWARD_SPEED
        if self.speed < self.MAX_REVERSE_SPEED: self.speed = self.MAX_REVERSE_SPEED
        self.direction += (self.k_right+self.k_left)

        x,y = self.position
        rad = self.direction * np.pi / 180
        x += -self.speed*np.sin(rad)
        y += -self.speed * np.cos(rad)
        self.position = (x,y)

        self.image = pygame.transform.rotate(self.src_image,self.direction)

        self.rect = self.image.get_rect()
        self.rect.center = self.position

# create car
rect = screen.get_rect()
car = CarSprite('../Images/car.png',rect.center)
car_group = pygame.sprite.RenderPlain(car)
background = pygame.image.load('../Images/raceTrack.png')
screen.blit(background,(0,0))

while 1:
    # user input
    deltat = clock.tick(30)
    for event in pygame.event.get():
        if not hasattr(event,'key'): continue
        down = event.type == pygame.KEYDOWN
        if event.key == pygame.K_RIGHT: car.k_right = down * -5
        elif event.key == pygame.K_LEFT: car.k_left = down * 5
        elif event.key == pygame.K_UP: car.k_up = down * 2
        elif event.key == pygame.K_DOWN: car.k_down = down * -2
        elif event.key == pygame.K_ESCAPE: sys.exit(0)

    # render
    #screen.fill((0,0,0))

    pad_group.clear(screen, background)
    car_group.clear(screen, background)
    car_group.update(deltat)
    pads = pygame.sprite.spritecollide(car, pad_group,False)
    if pads:
        pad = pads[0]
        if pad.number == current_pad_number + 1:
            pad.image = pad.hit
            current_pad_number += 1
    elif current_pad_number == 4:
        for pad in pad_group.sprites(): pad.image = pad.normal
        current_pad_number = 0
    pad_group.update(pads)
    pad_group.draw(screen)
    car_group.draw(screen)
    pygame.display.flip()