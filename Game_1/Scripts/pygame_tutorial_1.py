import pygame, numpy as np, sys
from pygame import *
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((1024,768))
car = pygame.image.load('../Images/car.png')
pygame.display.flip()
clock = pygame.time.Clock()
position = (100, 100)
speed = direction = 0
k_up = k_down = k_left = k_right = 0
TURN_SPEED = 8
ACCELERATION = 20
MAX_FORWARD_SPEED = 45
MAX_REVERSE_SPEED = -2
BLACK = (0,0,0)
fps = 60
while True:
    clock.tick(fps)
    for event in pygame.event.get():
        if not hasattr(event,'key'): continue
        down = event.type == pygame.KEYDOWN
        if event.key == pygame.K_RIGHT: k_right = down * -5
        elif event.key == pygame.K_LEFT: k_left = down * 5
        elif event.key == pygame.K_UP: k_up = down * 2
        elif event.key == pygame.K_DOWN: k_down = down * -2
        elif event.key == pygame.K_ESCAPE: sys.exit(0)
    screen.fill(BLACK)

    speed += (k_up + k_down)
    if speed > MAX_FORWARD_SPEED: speed = MAX_FORWARD_SPEED
    if speed < MAX_REVERSE_SPEED: speed = MAX_REVERSE_SPEED
    direction += (k_right+k_left)

    x,y = position
    rad = direction * np.pi / 180
    x += -speed*np.sin(rad)
    y += -speed * np.cos(rad)
    position = (x,y)

    rotated = pygame.transform.rotate(car,direction)

    rect = rotated.get_rect()
    rect.center = position

    screen.blit(rotated,rect)
    pygame.display.flip()

"""
for i in range(100):
    screen.fill((0, 0, 0))
    screen.blit(car, (i, 0))
    pygame.display.update()
    clock.tick(30"""



pygame.quit()
quit()